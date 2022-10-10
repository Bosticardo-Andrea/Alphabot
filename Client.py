#client TCP che permette di mandare comandi basilari all' alphabot
import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.0.129",5000))
    while True:
        comando = input("inserisci comando: ")
        if comando in ["f","b","l","r","s"]:
            if comando in ["f","b"]:
                speed = input("inserisci speed (ideale: 40): ")
                if int(speed) > 0 and int(speed) < 100:
                    s.sendall("".join(comando + "," + speed).encode())
            else:
                s.sendall(comando.encode())

if __name__ == "__main__":
    main()
