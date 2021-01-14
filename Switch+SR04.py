import RPi.GPIO as GPIO
import time
GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( 0 )
 
print( "input" )
 
led = 18
switch = 23
 
GPIO.setup( led, GPIO.OUT )
GPIO.setup( switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
while True:
   if( GPIO.input( switch ) ):
      GPIO.output( led, GPIO.HIGH )
   else:
      GPIO.output( led, GPIO.LOW )
   time.sleep( 0.1 )

print ("SR04")

GPIO_TRIGGER = 20
GPIO_ECHO = 21
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def afstand():
    
    #True en False zijn andere woorden voor HIGH en LOW
    #Code werkt niet als HIGH of LOW worden geschreven
    GPIO.output(GPIO_TRIGGER, True)
    GPIO.output(GPIO_TRIGGER, False)
    starttijd = time.time()
    stoptijd = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        starttijd = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        stoptijd = time.time()

    t = stoptijd - starttijd
    v = 34300 #snelheid van geluid door de lucht in cm/s
    s = (t * v) / 2
 
    return s

while True:
    s = afstand()
    print ("gemeten afstand =" % s)
    time.sleep(1)
             
    if s < 100:
        print("Speler is online")
    else:
        print ("Speler is offline")
