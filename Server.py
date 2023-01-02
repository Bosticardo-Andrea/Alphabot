from multiprocessing.resource_sharer import stop
import socket,time,os

import AlphaBot,sqlite3
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
    main()