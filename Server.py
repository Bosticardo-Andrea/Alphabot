from multiprocessing.resource_sharer import stop
import socket,time,os
import AlphaBot 
alpha = AlphaBot.AlphaBot()
dizio = {"s": alpha.stop,"f":alpha.forward,"b":alpha.backward,"l":alpha.left,"r":alpha.right}
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
        dati = dato.split(",")
        if dati[0] == "r" or dati[0] == "l":
            dizio[dati[0]]()
            time.sleep(int(dati[1]))
            alpha.stop()
        elif int(dati[1]) == 0:
            if int(dati[2]) == 0:
                dizio[dati[0]]()
            else:
                dizio[dati[0]](int(dati[2]))
        else:
            dizio[dati[0]](int(dati[2]))
            time.sleep(int(dati[1]))
            alpha.stop()
        
if __name__=="__main__":
    main()