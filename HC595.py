import RPi.GPIO as GPIO
import time
GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( 0 )

print( "hc595 walk" )

shift_clock_pin = 5
latch_clock_pin = 6
data_pin = 13

GPIO.setup( shift_clock_pin, GPIO.OUT )
GPIO.setup( latch_clock_pin, GPIO.OUT )
GPIO.setup( data_pin, GPIO.OUT )

def hc595( shift_clock_pin, latch_clock_pin, data_pin, value, delay ):
    for i in range (0, 8):
      if value % 2 == 1:
         GPIO.output(data_pin, GPIO.HIGH)
         time.sleep(0.5)
      
      GPIO.output(shift_clock_pin, GPIO.HIGH)
      GPIO.output(shift_clock_pin, GPIO.LOW)
      GPIO.output(latch_clock_pin, GPIO.HIGH)
      GPIO.output(latch_clock_pin, GPIO.LOW)

    time.sleep(delay)
   
   
delay = 0.1
while True:
   hc595( shift_clock_pin, latch_clock_pin, data_pin,   1, delay )
   hc595( shift_clock_pin, latch_clock_pin, data_pin,   2, delay )
   hc595( shift_clock_pin, latch_clock_pin, data_pin,   4, delay )
   hc595( shift_clock_pin, latch_clock_pin, data_pin,   8, delay )
   hc595( shift_clock_pin, latch_clock_pin, data_pin,  16, delay )
   hc595( shift_clock_pin, latch_clock_pin, data_pin,  32, delay )
   hc595( shift_clock_pin, latch_clock_pin, data_pin,  64, delay )
   hc595( shift_clock_pin, latch_clock_pin, data_pin, 128, delay )
