import socket
import AlphaBot 

alpha = AlphaBot.AlphaBot()
dizio = {"s": alpha.stop,"f":alpha.forward,"b":alpha.backward,"l":alpha.left,"r":alpha.right}
def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("0.0.0.0",5000))
    print("Sto ascoltando...")
    s.listen()
    connection,address = s.accept()
    while 1:
        dato = connection.recv(4096).decode().lower()
        print(dato)
        if "," in dato:
            dati = dato.split(",")
            dizio[dati[0]](int(dati[1]))
        else:
            dizio[dati[0]]
        
if __name__=="__main__":
    main()