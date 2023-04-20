import time 
from Motor import *
from ObjectAvoid import objectAvoid
import RPi.GPIO as GPIO

class Road_Tracker:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        self.obstacle_detector = objectAvoid()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01, GPIO.IN)
        GPIO.setup(self.IR02, GPIO.IN)
        GPIO.setup(self.IR03, GPIO.IN)

    def run(self):
        while True:
            self.linePo = 0x00
            if GPIO.input(self.IR03) == True:
                self.linePo = (self.linePo | 1)
            if GPIO.input(self.IR02) == True:
                self.linePo = (self.linePo | 2)
            if GPIO.input(self.IR01) == True:
                self.linePo = (self.linePo | 4)

            if self.obstacle_detector.get_distance() < 20: 
                PWM.setMotorModel(0, 0, 0, 0)
                while self.obstacle_detector.get_distance() < 20:
                    time.sleep(0.1)
            else:
                if self.linePo == 0:
                    PWM.setMotorModel(0, 0, 0, 0)
                elif self.linePo == 1:
                    PWM.setMotorModel(2500, 2500, -1500, -1500)
                elif self.linePo == 2:
                    PWM.setMotorModel(800, 800, 800, 800)
                elif self.linePo == 3:
                    PWM.setMotorModel(4000, 4000, -2000, -2000)
                elif self.linePo == 4:
                    PWM.setMotorModel(-1500, -1500, 2500, 2500)
                elif self.linePo == 6:
                    PWM.setMotorModel(-2000, -2000, 4000, 4000)
                elif self.linePo == 7:
                    PWM.setMotorModel(0, 0, 0, 0)
        
road_tracker = Road_Tracker()
if __name__ == '__main__': 
    print('Road Tracker') 
    try: 
        road_tracker.run() 
    except KeyboardInterrupt: 
        PWM.setMotorModel(0,0,0,0)