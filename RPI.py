#connectie voor RPI is niet neergezet als je deze code draait.

#standaard import
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)



'''Dit is de code voor de led lampjes. Er is nog niet bepaald wat we willen doen maar hier mee kan je al een heel eind komen

De volgende pinnen zijn geclaimed:'''
clock_pin = 19
data_pin = 26

GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(data_pin, GPIO.OUT)


def apa102_send_bytes(clock_pin, data_pin, bytes):
    for byte in bytes:
        for bit in byte:
            if bit == 0:
                GPIO.output(data_pin, GPIO.LOW)
                time.sleep(0.0001)
                GPIO.output(clock_pin, GPIO.HIGH)
                time.sleep(0.0001)
                GPIO.output(clock_pin, GPIO.LOW)
            elif bit == 1:
                GPIO.output(data_pin, GPIO.HIGH)
                time.sleep(0.0001)
                GPIO.output(clock_pin, GPIO.HIGH)
                time.sleep(0.0001)
                GPIO.output(clock_pin, GPIO.LOW)


def apa102(clock_pin, data_pin, colors):
    deBytes = [128, 64, 32, 16, 8, 4, 2, 1]
    apa102_send_bytes(clock_pin, data_pin,
                      [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]])
    binair = [[1, 1, 1, 1, 1, 1, 1, 1]]
    for byte in colors:
        for getal in byte:
            index = 0
            binairsGetal = []
            while getal != 0 and not index > len(deBytes) - 1:
                if getal - deBytes[index] > 0:
                    getal = getal - deBytes[index]
                    index += 1
                    binairsGetal.append(1)
                elif getal - deBytes[index] < 0:
                    index += 1
                    binairsGetal.append(0)
                elif getal - deBytes[index] == 0:
                    binairsGetal.append(1)
                    getal = getal - deBytes[index]
                    break
            count = 0
            for aantalKeer in range(len(binairsGetal), 8):
                count += 1
                binairsGetal.append(0)
            binair.append(binairsGetal)

        apa102_send_bytes(clock_pin, data_pin, binair)
        binair = [[1, 1, 1, 1, 1, 1, 1, 1]]

def vlag(clockPin, dataPin, delay):
    while True:
        for kleur in kleuren:
            apa102(clockPin,dataPin,[kleur for led in range(0,9)])
            time.sleep(delay)

kleuren = [[0, 0, 255], [255, 255, 255], [255, 0, 0]]

vlag(clock_pin, data_pin, 0.5)



"""Dit is de code voor kwispelen"""
def pulse(pin, delay1, delay2):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(delay1)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(delay2)

def servo_pulse(pin_nr, position):
    input = position * 0.00002 + 0.0007
    delay = 0.002
    pulse(pin_nr,input,delay)


def hondje(servo):
    GPIO.setup(servo, GPIO.OUT)
    for kwispel in range(0,3):
        for i in range(0, 60, 1):
            servo_pulse(servo, i)
        for i in range(100, 0, -1):
            servo_pulse(servo, i)

servo = 25
hondje(servo)
