#percorso dns = "C:\Windows\System32\drivers\etc\hosts"
from multiprocessing.resource_sharer import stop
import socket,time,os,random
from flask import Flask, render_template, request,redirect, url_for
import AlphaBot,sqlite3,string,HASH
hash = HASH.Hash()
app = Flask(__name__)
alpha = AlphaBot.AlphaBot()
dizio = {"s": alpha.stop,"f":alpha.ForwardistanceControl,"b":alpha.BackwardistanceControl,"l":alpha.LeftdistanceControl,"r":alpha.RightdistanceControl}
randomico = "".join([string.ascii_letters,string.ascii_lowercase,string.ascii_uppercase,string.digits,string.punctuation]).replace("\\","").replace("/","").replace(".","")
secret = "".join(randomico[random.randint(0,len(randomico)-1)]for _ in range(32))
@app.route(f'/{secret}', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('su') == 'su':
            dist = request.form['dist']
            funzione(f"f,{dist}")
        elif  request.form.get('giu') == 'giu':
            dist = request.form['dist']
            funzione(f"b,{dist}")
        elif  request.form.get('dx') == 'dx':
            gradi = (float(request.form['gradi'])*129)/90
            funzione(f"r,{int(gradi)}")
        elif  request.form.get('sx') == 'sx':
            gradi = (float(request.form['gradi'])*129)/90
            funzione(f"l,{int(gradi)}")
        elif  request.form.get('cmd') == 'cmd':
            cmd = int(request.form['comando'])
            if cmd < 1 or cmd >= 8:print("Errore")
            else:leggiDBEsegui(cmd)
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template("index.html",distanza=alpha.distanzaPercorsa)

def funzione(dato):
    dati = dato.split(",")
    if dati[0] == "s":
        dizio[dati[0]]()
    else:
        dizio[dati[0]](int(dati[1]))
def leggiDBEsegui(dato):
    db = sqlite3.connect("./robot.db")
    cur = db.cursor()
    res = cur.execute(f"SELECT Movimento FROM Movimenti WHERE ID = {dato}")
    dati = str(res.fetchone()[0]).split(";")
    print(dati)
    for dato in dati:
        dati = dato.split(",")
        if dato[0] == "s":
            alpha.stop()
            time.sleep(int(dati[1]))
        else:
            dizio[dati[0]](int(dati[1]))
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
        if dbUser==username:
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
        print(completion)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

def main():
    global dato
    es = os.popen("vcgencmd get_throttled")
    ris = es.read()
    print(ris)
    if ris == "throttled=0x50005":print("SONO SCARICO")
    else:print("TUTTO OK")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("0.0.0.0",5000))
    print("Sto ascoltando...")
    s.listen()
    connection,address = s.accept()
    print(f"Si é connesso: {address[0]}")
    while 1:
        dato = connection.recv(4096).decode().lower()
        print(dato)
        if len(dato) == 1:
            leggiDBEsegui(dato)
        else:
            funzione(dato)
        
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
    main()
