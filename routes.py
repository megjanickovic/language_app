from flask import Flask, render_template, request, url_for, redirect, json, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)

mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'language_app'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/languages')
def languages():
    query = "SELECT id, language FROM languages"
    cursor.execute(query)
    languages_data = cursor.fetchall()
    return render_template('languages.html', languages_data=languages_data)

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
        return json.dumps({'html':'<span>Enter a language.</span>'})

@app.route('/languages/<int:language>/')
def language(language):
    query = "SELECT language FROM languages WHERE id=%s"
    params = language
    cursor.execute(query, params)
    language_data = cursor.fetchone()
    return render_template('language.html', language=language, language_data=language_data)

@app.route('/languages/<int:language>/words')
def words(language):
    query = "SELECT id, word FROM words WHERE language_id=%s"
    params = language
    cursor.execute(query, params)
    words_data = cursor.fetchall()
    return render_template('words.html', language=language, words_data=words_data)

@app.route('/addWord', methods=['POST'])
def addWord():
    _language_id = request.form['language_id']
    _word = request.form['word']
    _definition = request.form['definition']
    if _language_id and _word and _definition:
        query = "INSERT INTO words(language_id, word, definition) VALUES (%s, %s, %s)"
        params = _language_id, _word, _definition
        cursor.execute(query, params)
        conn.commit()
        return json.dumps({'html':'Word added.'})
    else:
        return json.dumps({'html':'<span>Enter a word and definition.</span>'})

@app.route('/languages/<int:language>/words/<int:word>')
def word(language, word):
    query = "SELECT word, definition FROM words WHERE language_id=%s AND id=%s"
    params = language, word
    cursor.execute(query, params)
    word_data = cursor.fetchone()
    query = "SELECT tag FROM tags, word_tag WHERE word_tag.w=%s AND tags.id=word_tag.t"
    params = word
    cursor.execute(query, params)
    tags = cursor.fetchall()
    return render_template('word.html', language=language, word=word, word_data=word_data, tags=tags)

@app.route('/editDefinition', methods=['POST'])
def editDefinition():
    _id = request.form['id']
    _definition = request.form['definition']
    if _id and _definition:
        query = "UPDATE words SET definition=%s WHERE id=%s"
        params = _definition, _id
        cursor.execute(query, params)
        conn.commit()
        return json.dumps({'html':'Definition updated.'})
    else:
        return json.dumps({'html':'<span>Enter a definition.</span>'})

if __name__ == "__main__":
    app.run()
