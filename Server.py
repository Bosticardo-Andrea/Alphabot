from multiprocessing.resource_sharer import stop
import socket,time,os
from flask import Flask, render_template, request
import AlphaBot,sqlite3
app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('su') == 'su':
            dist = request.form['dist']
            funzione(f"f,{dist}")
        elif  request.form.get('giu') == 'giu':
            dist = request.form['dist']
            funzione(f"b,{dist}")
        elif  request.form.get('dx') == 'dx':
            gradi = request.form['gradi']
            funzione(f"r,{gradi}")
        elif  request.form.get('sx') == 'sx':
            gradi = request.form['gradi']
            funzione(f"l,{gradi}")
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template("index.html",distanza=alpha.distanzaPercorsa)
alpha = AlphaBot.AlphaBot()
dizio = {"s": alpha.stop,"f":alpha.ForwardistanceControl,"b":alpha.BackwardistanceControl,"l":alpha.LeftdistanceControl,"r":alpha.RightdistanceControl}
db = sqlite3.connect("./robot.db")
cur = db.cursor()
def funzione(dato):
    dati = dato.split(",")
    if dati[0] == "s":
        dizio[dati[0]]()
    else:
        dizio[dati[0]](int(dati[1]))
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

        else:
            funzione(dato)
        
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
    main()