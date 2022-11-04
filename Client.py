#client TCP che permette di mandare comandi basilari all' alphabot
import socket,keyboard,time
def comandiScritti(s):
     while 1:
        comando = input("inserisci comando: ")
        if comando in ["f","b","l","r","s"]:
            if comando == "s":
                s.sendall("".join(comando + ",0").encode())
            else:
                tempo = int(input("inserisci un intero per i secondi e 0 per INFINITO: "))
                if comando in ["f","b"]:
                    speed = input("inserisci speed (ideale: 40): ")
                    if int(speed) > 0 and int(speed) < 100:
                        s.sendall("".join(comando + "," + str(tempo)+ "," + speed).encode())
                    elif comando in ["r","l"]:
                        s.sendall("".join(comando + "," + str(tempo)).encode())
def comandiDaTastiera(s):
    dizioComadi = {"space":"s","w":"f","s":"b","a":"l","d":"r",}
    while 1:
        s.sendall(dizioComadi[keyboard.read_key()])
        time.sleep(0.1)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.0.129",5000))
    risp = input("Vuoi scrivere i comandi oppure comandare il robot da tastiera [s/t]: ").lower()
    while risp != "s" and risp != "t":
        risp = input("Risposta sbagliata\n\nVuoi scrivere i comandi oppure comandare il robot da tastiera [s/t]: ").lower()
    if risp == "s":
        comandiScritti(s)
    else:
        comandiDaTastiera(s)

if __name__ == "__main__":
    main()
