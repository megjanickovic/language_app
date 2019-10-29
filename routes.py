from flask import Flask, render_template, request, url_for, redirect, json, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)

###################### CONNECT TO DATABASE ######################

mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'language_app'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

###################### ROUTES ######################

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

###################### LANGUAGES #####################

@app.route('/languages')
def languages():
    query = "SELECT language_id, language FROM languages"
    cursor.execute(query)
    languages_data = cursor.fetchall()
    return render_template('languages.html', languages_data=languages_data)

@app.route('/languages/<int:language>')
def language(language):
    return render_template('language.html')

@app.route('/addLanguage', methods=['POST'])
def addLanguage():
    _language = request.form['language']
    if _language:
        query = "INSERT INTO languages(language) VALUES (%s)"
        params = _language
        cursor.execute(query, params)
        conn.commit()
        return json.dumps({'html':'Language added.'})
    else:
        return json.dumps({'html':'An error has occurred (/addLanguage)'})

@app.route('/deleteLanguage', methods=['POST'])
def deleteLanguage():
    _language_id = request.form['language_id']
    if _language_id:
        query = "DELETE FROM languages WHERE language_id=%s"
        params = _language_id
        cursor.execute(query, params)
        conn.commit()
        return json.dumps({'html':'Language deleted.'})
    else:
        return json.dumps({'html':'An error has occurred (/deleteLanguage)'})

##################### WORDS #####################

@app.route('/languages/<int:language_id>/words')
def words(language_id):
    query = "SELECT word_id, word FROM words WHERE language_id=%s ORDER BY word"
    params = language_id
    cursor.execute(query, params)
    words_data = cursor.fetchall()
    return render_template('words.html', language_id=language_id, words_data=words_data)

@app.route('/languages/<int:language_id>/words/<int:word_id>')
def word(language_id, word_id):
    query = "SELECT word_id, word, pronunciation, definition FROM words WHERE language_id=%s AND word_id=%s"
    params = language_id, word_id
    cursor.execute(query, params)
    word_data = cursor.fetchone()
    # need to get all tags for language, and what tags this word currently has
    query = "SELECT tags.tag_id, tags.tag, IF(word_tag.word_id=%s, 1, 0) AS taggedAs FROM tags LEFT JOIN word_tag ON tags.tag_id=word_tag.tag_id WHERE tags.language_id=%s"
    params = word_id, language_id
    cursor.execute(query, params)
    tags = cursor.fetchall()
    return render_template('word.html', language_id=language_id, word_data=word_data, tags=tags)

@app.route('/addWord', methods=['POST'])
def addWord():
    _language_id = request.form['language_id']
    _word = request.form['word']
    _pronunciation = request.form['pronunciation'] if request.form['pronunciation'] else None
    _definition = request.form['definition']
    if _language_id and _word and _definition:
        query = "INSERT INTO words(language_id, word, pronunciation, definition) VALUES (%s, %s, %s, %s)"
        params = _language_id, _word, _pronunciation, _definition
        cursor.execute(query, params)
        conn.commit()
        return json.dumps({'html':'Word added.'})
    else:
        return json.dumps({'html':'An error has occurred (/addWord)'})

@app.route('/editWord', methods=['POST'])
def editWord():
    _word = request.form['word']
    _pronunciation = request.form['pronunciation'] if request.form['pronunciation'] else None
    _definition = request.form['definition']
    _word_id = request.form['word_id']
    if _word and _definition and _word_id:
        query = "UPDATE words SET word=%s, pronunciation=%s, definition=%s WHERE word_id=%s"
        params = _word, _pronunciation, _definition, _word_id
        cursor.execute(query, params)
        conn.commit()
        return json.dumps({'html':'Word updated.'})
    else:
        return json.dumps({'html':'An error has occurred (/editWord)'})

@app.route('/deleteWord', methods=['POST'])
def deleteWord():
    _word_id = request.form['word_id']
    if _word_id:
        query = "DELETE FROM words WHERE word_id=%s"
        params = _word_id
        cursor.execute(query, params)
        conn.commit()
        return json.dumps({'html':'Word deleted.'})
    else:
        return json.dumps({'html':'An error has occurred (/deleteWord)'})

##################### TAGS #####################

@app.route('/languages/<int:language_id>/tags')
def tags(language_id):
    query = "SELECT tag_id, tag FROM tags WHERE language_id=%s ORDER BY tag"
    params = language_id
    cursor.execute(query, params)
    tags_data = cursor.fetchall()
    return render_template('tags.html', language_id=language_id, tags_data=tags_data)

@app.route('/addTag', methods=['POST'])
def addTag():
    _language_id = request.form['language_id']
    _tag = request.form['tag']
    if _language_id and _tag:
        query = "INSERT INTO tags(language_id, tag) VALUES (%s, %s)"
        params = _language_id, _tag
        cursor.execute(query, params)
        conn.commit()
        return json.dumps({'html':'Tag added.'})
    else:
        return json.dumps({'html':'An error has occurred (/addTag)'})

@app.route('/deleteTag', methods=['POST'])
def deleteTag():
    _tag_id = request.form['tag_id']
    if _tag_id:
        query = "DELETE FROM tags WHERE tag_id=%s"
        params = _tag_id
        cursor.execute(query, params)
        conn.commit()
        return json.dumps({'html':'Tag deleted.'})
    else:
        return json.dumps({'html':'An error has occurred (/deleteTag)'})

@app.route('/addWordTag', methods=['POST'])
def addWordTag():
    _word_id = request.form['word_id']
    _tag_id = request.form['tag_id']
    if _word_id and _tag_id:
        query = "INSERT INTO word_tag(word_id, tag_id) VALUES (%s, %s)"
        params = _word_id, _tag_id
        cursor.execute(query, params)
        conn.commit()
        return json.dumps({'html':'Tag added.'})
    else:
        return json.dumps({'html':'An error has occurred (/addWordTag)'})

@app.route('/removeWordTag', methods=['POST'])
def removeWordTag():
    _word_id = request.form['word_id']
    _tag_id = request.form['tag_id']
    if _word_id and _tag_id:
        query = "DELETE FROM word_tag WHERE word_id=%s AND tag_id=%s"
        params = _word_id, _tag_id
        cursor.execute(query, params)
        conn.commit()
        return json.dumps({'html':'Tag deleted.'})
    else:
        return json.dumps({'html':'An error has occurred (/removeWordTag)'})

###################### FLASHCARDS ######################

@app.route('/languages/<int:language_id>/flashcards')
def flashcards(language_id):
    query = "SELECT word_id, word, pronunciation, definition FROM words WHERE language_id=%s ORDER BY word"
    params = language_id
    cursor.execute(query, params)
    words_data = cursor.fetchall()
    return render_template('flashcards.html', language_id=language_id, words_data=words_data)
    
###################### END ROUTES ######################

if __name__ == "__main__":
    app.run()
