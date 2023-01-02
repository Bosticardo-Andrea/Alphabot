import time
import RPi.GPIO as GPIO


class AlphaBot(object):
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.speedA=70
        self.speedB=70


        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(8, GPIO.IN)
        GPIO.setup(7, GPIO.IN)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.speedA)
        self.PWMB.start(self.speedB)
        self.stop()

    def right(self):
        self.PWMA.ChangeDutyCycle(self.speedA)
        self.PWMB.ChangeDutyCycle(self.speedB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def stop(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def left(self):
        self.PWMA.ChangeDutyCycle(self.speedA)
        self.PWMB.ChangeDutyCycle(self.speedB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def forward(self):
        self.PWMA.ChangeDutyCycle(self.speedA)
        self.PWMB.ChangeDutyCycle(self.speedB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def backward(self):
        self.PWMA.ChangeDutyCycle(self.speedA)
        self.PWMB.ChangeDutyCycle(self.speedB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        
    def set_pwm_a(self, value):
        self.speedA = value
        self.PWMA.ChangeDutyCycle(self.speedA)

    def set_pwm_b(self, value):
        self.speedB = value
        self.PWMB.ChangeDutyCycle(self.speedB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)
    def BackwardistanceControl(self,distance=1000):
        ultimoStato = [GPIO.input(8),GPIO.input(7)]
        contaStati,statiTotali,statiPerRotazione,contaRotazioni = [0,0],[0,0],40,[0,0]
        distazaPerStep = 207/statiPerRotazione
        while 1:
            statoCorrente = [GPIO.input(8),GPIO.input(7)]
            self.forward()
            #print(statoCorrente,ultimoStato,contaStati,statiTotali,contaRotazioni)
            if statoCorrente[0] != ultimoStato[0]:
                ultimoStato[0] = statoCorrente[0]
                contaStati[0]+=1
                statiTotali[0] +=1
            if statoCorrente[1] != ultimoStato[1]:
                ultimoStato[1] = statoCorrente[1]
                contaStati[1]+=1
                statiTotali[1] +=1
            while contaStati[0] > contaStati[1] or contaStati[1] > contaStati[0]:
                if contaStati[0] > contaStati[1]:
                    self.PWMA.ChangeDutyCycle(self.speedA)
                    self.PWMB.ChangeDutyCycle(self.speedB)
                    GPIO.output(self.IN1, GPIO.LOW)
                    GPIO.output(self.IN2, GPIO.HIGH)
                    GPIO.output(self.IN3, GPIO.LOW)
                    GPIO.output(self.IN4, GPIO.LOW)
                elif contaStati[1] > contaStati[0]:
                    self.PWMA.ChangeDutyCycle(self.speedA)
                    self.PWMB.ChangeDutyCycle(self.speedB)
                    GPIO.output(self.IN1, GPIO.LOW)
                    GPIO.output(self.IN2, GPIO.LOW)
                    GPIO.output(self.IN3, GPIO.HIGH)
                    GPIO.output(self.IN4, GPIO.LOW)
                statoCorrente = [GPIO.input(8),GPIO.input(7)]
                if statoCorrente[0] != ultimoStato[0]:
                    ultimoStato[0] = statoCorrente[0]
                    contaStati[0]+=1
                    statiTotali[0] +=1
                if statoCorrente[1] != ultimoStato[1]:
                    ultimoStato[1] = statoCorrente[1]
                    contaStati[1]+=1
                    statiTotali[1] +=1
            if contaStati[0] == statiPerRotazione:
                statoCorrente[0] = 0
                contaRotazioni[0] += 1 
                contaStati[0] = 0
            if contaStati[1] == statiPerRotazione:
                statoCorrente[1] = 0
                contaRotazioni[1] += 1 
                contaStati[1] = 0
            if distazaPerStep * statiTotali[0] >= distance or distazaPerStep * statiTotali[1] >= distance:
                print(f"distanza percorsa {int(distazaPerStep * statiTotali[0])},{distazaPerStep * statiTotali[1]}")
                self.stop()
                break
    def ForwardistanceControl(self,distance=1000):
        ultimoStato = [GPIO.input(8),GPIO.input(7)]
        contaStati,statiTotali,statiPerRotazione,contaRotazioni = [0,0],[0,0],40,[0,0]
        distazaPerStep = 207/statiPerRotazione
        while 1:
            statoCorrente = [GPIO.input(8),GPIO.input(7)]
            self.backward()
            #print(statoCorrente,ultimoStato,contaStati,statiTotali,contaRotazioni)
            if statoCorrente[0] != ultimoStato[0]:
                ultimoStato[0] = statoCorrente[0]
                contaStati[0]+=1
                statiTotali[0] +=1
            if statoCorrente[1] != ultimoStato[1]:
                ultimoStato[1] = statoCorrente[1]
                contaStati[1]+=1
                statiTotali[1] +=1
            while contaStati[0] > contaStati[1] or contaStati[1] > contaStati[0]:
                if contaStati[0] > contaStati[1]:
                    self.PWMA.ChangeDutyCycle(self.speedA)
                    self.PWMB.ChangeDutyCycle(self.speedB)
                    GPIO.output(self.IN1, GPIO.HIGH)
                    GPIO.output(self.IN2, GPIO.LOW)
                    GPIO.output(self.IN3, GPIO.LOW)
                    GPIO.output(self.IN4, GPIO.LOW)
                elif contaStati[1] > contaStati[0]:
                    self.PWMA.ChangeDutyCycle(self.speedA)
                    self.PWMB.ChangeDutyCycle(self.speedB)
                    GPIO.output(self.IN1, GPIO.LOW)
                    GPIO.output(self.IN2, GPIO.LOW)
                    GPIO.output(self.IN3, GPIO.LOW)
                    GPIO.output(self.IN4, GPIO.HIGH)
                statoCorrente = [GPIO.input(8),GPIO.input(7)]
                if statoCorrente[0] != ultimoStato[0]:
                    ultimoStato[0] = statoCorrente[0]
                    contaStati[0]+=1
                    statiTotali[0] +=1
                if statoCorrente[1] != ultimoStato[1]:
                    ultimoStato[1] = statoCorrente[1]
                    contaStati[1]+=1
                    statiTotali[1] +=1
            if contaStati[0] == statiPerRotazione:
                statoCorrente[0] = 0
                contaRotazioni[0] += 1 
                contaStati[0] = 0
            if contaStati[1] == statiPerRotazione:
                statoCorrente[1] = 0
                contaRotazioni[1] += 1 
                contaStati[1] = 0
            if distazaPerStep * statiTotali[0] >= distance or distazaPerStep * statiTotali[1] >= distance:
                print(f"distanza percorsa {int(distazaPerStep * statiTotali[0])}")
                self.stop()
                break
    def LeftdistanceControl(self,angle=129):
        ultimoStato = [GPIO.input(7)]
        contaStati,statiTotali,statiPerRotazione,contaRotazioni = [0,0],[0,0],40,[0,0]
        distazaPerStep = 207/statiPerRotazione
        while 1:
            statoCorrente = [GPIO.input(7)]
            self.left()
            #print(statoCorrente,ultimoStato,contaStati,statiTotali,contaRotazioni)
            if statoCorrente[0] != ultimoStato[0]:
                ultimoStato[0] = statoCorrente[0]
                contaStati[0]+=1
                statiTotali[0] +=1
            if contaStati[0] == statiPerRotazione:
                statoCorrente[0] = 0
                contaRotazioni[0] += 1 
                contaStati[0] = 0
            if distazaPerStep * statiTotali[0] >= angle:
                print(f"distanza percorsa {int(distazaPerStep * statiTotali[0])}")
                self.stop()
                break
    def RightdistanceControl(self,angle=129):
        ultimoStato = [GPIO.input(7)]
        contaStati,statiTotali,statiPerRotazione,contaRotazioni = [0,0],[0,0],40,[0,0]
        distazaPerStep = 207/statiPerRotazione
        while 1:
            statoCorrente = [GPIO.input(7)]
            self.right()
            #print(statoCorrente,ultimoStato,contaStati,statiTotali,contaRotazioni)
            if statoCorrente[0] != ultimoStato[0]:
                ultimoStato[0] = statoCorrente[0]
                contaStati[0]+=1
                statiTotali[0] +=1
            if contaStati[0] == statiPerRotazione:
                statoCorrente[0] = 0
                contaRotazioni[0] += 1 
                contaStati[0] = 0
            if distazaPerStep * statiTotali[0] >= angle:
                print(f"distanza percorsa {int(distazaPerStep * statiTotali[0])}")
                self.stop()
                break
if __name__ == '__main__':

    Ab = AlphaBot()
    Ab.forward()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
