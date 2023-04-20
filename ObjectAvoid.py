import time
from Motor import *
import RPi.GPIO as GPIO
from servo import *
from PCA9685 import PCA9685

class objectAvoid:
    def __init__(self):
        GPIO.setwarnings(False)
        self.trigger_pin = 27
        self.echo_pin = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin,GPIO.OUT)
        GPIO.setup(self.echo_pin,GPIO.IN)

    def send_trigger_pulse(self):
        GPIO.output(self.trigger_pin,True)
        time.sleep(0.00015)
        GPIO.output(self.trigger_pin,False)

    def wait_for_echo(self,value,timeout):
        count = timeout
        while GPIO.input(self.echo_pin) != value and count>0:
            count = count-1    

    def get_distance(self):
        distance_cm=[0,0,0,0,0]
        for i in range(3):
            self.send_trigger_pulse()
            self.wait_for_echo(True,10000)
            start = time.time()
            self.wait_for_echo(False,10000)
            finish = time.time()
            pulse_length = finish-start
            distance_cm[i] = pulse_length/0.000058
        distance_cm=sorted(distance_cm)
        return int(distance_cm[2])

    def run_motor(self,L,M,R):
        self.PWM.setMotorModel(400,400,400,400)
        
        # stop the robot if distance is less than 10 cm
        if L < 20 or M < 20 or R < 20:
            self.PWM.setMotorModel(0,0,0,0)
            time.sleep(2.5)
            
    def run(self):
        self.PWM=Motor()
        self.pwm_S=Servo()
        for i in range(30,151,60):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i==30:
                    L = self.get_distance()
                elif i==90:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
        while True:
            for i in range(90,30,-60):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i==30:
                    L = self.get_distance()
                elif i==90:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
                self.run_motor(L,M,R)
            for i in range(30,151,60):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i==30:
                    L = self.get_distance()
                elif i==90:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
                self.run_motor(L,M,R)

ultrasonic = objectAvoid()              
if __name__ == '__main__':
    print ('Object Avoidance')
    try:
        ultrasonic.run()
    except KeyboardInterrupt:  
        PWM.setMotorModel(0,0,0,0)
        ultrasonic.pwm_S.setServoPwm('0',90)



