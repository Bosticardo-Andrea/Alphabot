import socket,time,os,random
from flask import Flask, render_template, request,redirect, url_for
import sqlite3,string,HASH
hash = HASH.Hash()
app = Flask(__name__)
randomico = "".join([string.ascii_letters,string.ascii_lowercase,string.ascii_uppercase,string.digits,string.punctuation])
secret = "".join(randomico[random.randint(0,len(randomico)-1)]for _ in range(32))
@app.route(f'/{secret}', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("ok")
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template("index.html",distanza="ciao")

def validate(username, password):
    completion = False
    con = sqlite3.connect('./robot.db')
    #with sqlite3.connect('static/db.db') as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM utenti")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==hash.creaDigest(username):
            completion=check_password(dbPass, hash.creaDigest(password))
    return completion
def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        print(completion,username,password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

        
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
