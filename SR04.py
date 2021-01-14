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
