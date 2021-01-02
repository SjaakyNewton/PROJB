#connectie voor RPI is niet neergezet als je deze code draait.

#standaard import
import time
import RPi.GPIO as GPIO
import json
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)



'''Dit is de code voor de led lampjes. Hij reageert nog niet automatische elke minuut. Verder doet die het keurig en reageert die op veranderingen.

!!!LET OP!!!
Er moeten twee files bij zijn om het werken te maken!
Away.txt
Online.txt

De volgende pinnen zijn geclaimed:'''
clock_pin = 19
data_pin = 26

GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(data_pin, GPIO.OUT)

#Pulse naar Ledstrip
def pulseLedStrip(clock_pin, data_pin, bytes):
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

#Ontcijfert de binaire code
def LedStrip(clock_pin, data_pin, colors):
    deBytes = [128, 64, 32, 16, 8, 4, 2, 1]
    pulseLedStrip(clock_pin, data_pin,
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

        pulseLedStrip(clock_pin, data_pin, binair)
        binair = [[1, 1, 1, 1, 1, 1, 1, 1]]

def golfje(clockPin, dataPin, delay,kleuren):
    for golf in range(0,1):
        for kleur in kleuren:
            LedStrip(clockPin,dataPin,[kleur for led in range(0,9)])
            time.sleep(delay)

#Zijn de kleuren die nodig zijn.
online = [[0, 255, 0], [0, 0, 0]]
offline = [[0, 0, 255], [0, 0, 0]]
away = [[0,255,255], [0, 0, 0]]


#VRIENDENLIJST VERZAMELEN ----------------
json_data_vriendenlijst = requests.get('http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=B99D1FC3DA15306CAB4D188601446F66&steamid=76561198135983674&relationship=friend&format=json')
json_formatted_vriendenlijst = json.loads(json_data_vriendenlijst.text)

#Haalt de vrienden ID's op zodat ik daarmee kan checken.
def vriendenOphalen():
    lijstmetid = []
    for i in json_formatted_vriendenlijst['friendslist']['friends']:
        lijstmetid.append(i['steamid'])
    return vriendenChecken(lijstmetid)

#Checkt de status van de vrienden
def vriendenChecken(lijstmetid):
    aantalOnline = 0
    aantalAway = 0
    while len(lijstmetid) != 0:
        lst = lijstmetid
        id = lst[0]
        URL = (' http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B99D1FC3DA15306CAB4D188601446F66&steamids={}&format=json').format(id)
        json_data_vriend = requests.get(URL)
        json_formatted_vriend = json.loads(json_data_vriend.text)
        for status in json_formatted_vriend['response']['players']:
            if 1 == status['personastate']:
                aantalOnline += 1
            elif 3 == status['personastate']:
                aantalAway += 1
            lst.remove(lst[0])

    fileOnline = open('Online.txt','r')
    fileOnlineRead = fileOnline.read()

    fileAway = open('Away.txt','r')
    fileAwayRead = fileAway.read()

    if aantalOnline > int(fileOnlineRead):
        aantalKeer = aantalOnline - int(fileOnlineRead)
        for aantal in range(0,aantalKeer):
            golfje(clock_pin, data_pin, 0.5, online)
    if aantalAway > int(fileAwayRead):
        aantalKeer = aantalAway - int(fileAwayRead)
        for aantal in range(0,aantalKeer):
            golfje(clock_pin, data_pin, 0.5, away)
    totaalNu = aantalOnline + aantalAway
    totaalToen = int(fileOnlineRead) + int(fileAwayRead)
    if totaalNu < totaalToen:
        aantalKeer = totaalToen - totaalNu
        for aantal in range(0,aantalKeer):
            golfje(clock_pin, data_pin, 0.5, offline)
    fileOnline.close()
    fileAway.close()

    fileOnline = open('Online.txt', 'w')
    fileAway = open('Away.txt', 'w')
    fileOnline.write(str(aantalOnline))
    fileAway.write(str(aantalAway))

    fileOnline.close()
    fileAway.close()

vriendenOphalen()

"""
Dit is de code voor kwispelen.

Moet nu nog reageren op de afstandsensor. Dit is een kleine veranderen met een if statment.
"""

#Dit is de pulse functie die een stroom signaal naar de GPIO geeft.
def pulse(pin, delay1, delay2):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(delay1)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(delay2)

#Dit is de data voor waar de servo op moet staan bij zijn kwispels
def servo_pulse(pin_nr, position):
    input = position * 0.00002 + 0.0007
    delay = 0.002
    pulse(pin_nr,input,delay)

#Dit roept het kwispelen aan
def hondje(servo):
    GPIO.setup(servo, GPIO.OUT)
    for kwispel in range(0,3):
        for i in range(0, 60, 1):
            servo_pulse(servo, i)
        for i in range(100, 0, -1):
            servo_pulse(servo, i)

servo = 25
hondje(servo)
