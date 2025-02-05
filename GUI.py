from tkinter import *
from PIL import ImageTk,Image
import requests
import json
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Standaard is dit 1000 maar dat vond het programma te weinig dus verhoogt tot dat die het genoeg vond.
sys.setrecursionlimit(4000)

urlJson = 'https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json'
steamKey = 'B99D1FC3DA15306CAB4D188601446F66'

""""
Steam colour codes:
#171a21 donker donker blauw
#66c0f4 licht licht blauw
#1b2838 donker blauw
#2a475e licht blauw
#c7d5e0 grijswit
Label settings: bg = '#2a9df4',fg='white'
                bg = '#187bcd',fg='white'
                bg = '#0197CF',fg='white' (Favoriet)
"""

"""Zorgt ervoor dat je bij het eerste scherm komt en voor wisselingen tussen schermen."""
def startFrame():
    onlineScherm.forget()
    gamesScherm.forget()
    gameLijstScherm.forget()
    vriendengames.forget()
    genreScherm.forget()
    startScherm.pack()
    root.geometry('400x400')
    #optie scherm met wat je wilt zien

"""Zorgt ervoor dat je bij het het vrienden scherm komt en voor wisselingen tussen schermen."""
def onlineVriendenFrame():
    startScherm.forget()
    onlineScherm.pack()
    vriendeninfo(vriendenlijst())
    root.geometry('400x400')
    #vrienden die online zijn moeten getoond worden, ook wat je verwacht wat online komt.

"""Zorgt ervoor dat je bij het game die gespeeld worden scherm komt en voor wisselingen tussen schermen."""
def playedGamesFrame():
    startScherm.forget()
    ingame(vriendenlijst())
    gamesScherm.pack()
    root.geometry('400x400')
    #games die gespeeld worden.

"""Zorgt ervoor dat je bij het json lijst scherm komt en voor wisselingen tussen schermen."""
def gameLijstFrame():
    startScherm.forget()
    gameLijstScherm.pack()
    sortedOnName()
    root.geometry('400x400')
    #Games die in steam staan. Worden uit een json bestand gehaald

"""Zorgt ervoor dat je bij het het vrienden scherm komt en voor wisselingen tussen schermen."""
def vriendengamesFrame():
    startScherm.forget()
    vriendengames.pack()
    statsvriend(gamesplayedreturn)
    root.geometry('400x400')

def genrestatFrame():
    startScherm.forget()
    genreScherm.pack()
    grafiek()
    statswereld()
    root.geometry('400x400')

''''Functie die het json bestand uitleest. Dit schilt in elke andere functie de moeite om het ergens vandaan te halen.
    Met een regel kan iets de content gebruikt.'''
def jsonFunctie():
    response = requests.get(urlJson)
    content = json.loads(response.text)
    return content

"""Haalt de vrienden op via de Steam API. Dit zorgt dus voor live updates. Je krijgt ze hier in nummers. Met de nummers kun je later meer."""
def vriendenlijst():
    json_data_vriendenlijst = requests.get('http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=B99D1FC3DA15306CAB4D188601446F66&steamid=76561198135983674&relationship=friend&format=json')
    json_formatted_vriendenlijst = json.loads(json_data_vriendenlijst.text)
    lijstmetid = []
    for i in json_formatted_vriendenlijst['friendslist']['friends']:
        lijstmetid.append(i['steamid'])
    return lijstmetid
    #dit is een functie die de STEAMIDs in een lijst stopt om te gebruiken voor online vriendeninfo functie hieronder

"""Haalt de vrienden info op. De informatie uit vriendelijst() Wordt hier verder verwerkt."""
def vriendeninfo(lijstmetid):
    vriendenOnline = ''
    vriendenOffline = ''
    vriendenAway = ''
    while len(lijstmetid) != 0:
        lst = lijstmetid
        id = lst[0]
        URL = (' http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B99D1FC3DA15306CAB4D188601446F66&steamids={}&format=json').format(id)
        json_data_vriend = requests.get(URL)
        json_formatted_vriend = json.loads(json_data_vriend.text)

        for i in json_formatted_vriend['response']['players']:
            gebruikersnaam = i['personaname']
            if 1 == i['personastate']:
                vriendenOnline += (f'{gebruikersnaam}\n')
            elif 3 == i['personastate']:
                vriendenAway += (f'{gebruikersnaam}\n')
            else:
                vriendenOffline += (f'{gebruikersnaam}\n')
            lst.remove(lst[0])

            vriendenonlinetonen['text'] = vriendenOnline
            vriendenofflinetonen['text'] = vriendenOffline
            vriendenawaytonen['text'] = vriendenAway
    # FUNCTIE VRIENDEN ONLINE - OFFLINE

''' Dit is de functie die checkt wie welke game speelt '''
def ingame(lijstmetid):
    ingame = ''
    while len(lijstmetid) != 0:
        lst = lijstmetid
        id = lst[0]
        URL = (' http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B99D1FC3DA15306CAB4D188601446F66&steamids={}&format=json').format(id)
        json_data_ingame = requests.get(URL)
        json_formatted_ingame = json.loads(json_data_ingame.text)

        for i in json_formatted_ingame['response']['players']:
            gebruiker = i['personaname']
            try:
                game = i['gameextrainfo']
                ingame += (f'{gebruiker} speelt {game}\n')
            except:
                pass

            lst.remove(lst[0])

    if not ingame:
        niemand = "Niemand speelt momenteel een game"
        huidigeGametonen['text'] = niemand
    else:
        huidigeGametonen['text'] = ingame

''' Dit is de functie die checkt welke game de afgelopen 2 weken het meest gespeeld zijn in mijn vriendenlijst '''
def gamesplayed(lijstmetid):
    games_played = {}
    while len(lijstmetid) != 0:
        lst = lijstmetid
        id = lst[0]
        URLG = ('http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=B99D1FC3DA15306CAB4D188601446F66&steamid={}&count=1&format=json').format(id)
        json_data_gamesplayed = requests.get(URLG)
        json_formatted_gamesplayed = json.loads(json_data_gamesplayed.text)

        for i in json_formatted_gamesplayed:
            try:
                for i in json_formatted_gamesplayed['response']['games']:
                    gamesp = i['name']
                    playtime = i['playtime_2weeks']
                    if gamesp in games_played:
                        oudevalue = games_played[gamesp]
                        playtime = oudevalue + int(playtime)
                    games_played[gamesp] = round(playtime / 60)
                lst.remove(lst[0])
            except:
                lst.remove(lst[0])

    return games_played

''' Toont aantal uren gespeeld huidige dag '''
def statsvriend(lijstmetid):
    lijstje = gamesplayedreturn
    totaal = sum(lijstje)
    lengte = len(lijstje)
    gemiddelde = round(totaal / lengte, 2)
    range = max(lijstje) - min(lijstje)

    totaalurentonen['text'] = totaal
    gemiddeldurentonen['text'] = gemiddelde
    spreidingsbreedtetonen['text'] = range

''' Toont percentage genres over alle games '''
def statswereld():
    response = requests.get(urlJson)
    content = json.loads(response.text)
    index = 0
    genres = {}
    for item in content:
        genres_split = item['genres'].split(";")
        for genre in genres_split:

            if genre in genres:
                genres[genre] = genres[genre] + 1
            else:
                genres[genre] = 1

    sorteddict = {key: value for key, value in
                  sorted(genres.items(), reverse=True,
                         key=lambda item: item[1])}
    listvalues = list(sorteddict.values())
    listkeys = list(sorteddict.keys())
    sortedvalues = sorted(listvalues, reverse=True)

    genre1 = str(listkeys[0])+ ':' + ' ' + str(round((sortedvalues[0] / sum(sorteddict.values()) * 100), 2)) + '%'
    genre2 = str(listkeys[1])+ ':' + ' ' + str(round((sortedvalues[1] / sum(sorteddict.values()) * 100), 2)) + '%'
    genre3 = str(listkeys[2])+ ':' + ' ' + str(round((sortedvalues[2] / sum(sorteddict.values()) * 100), 2)) + '%'

    genrelabel2['text'] = genre1
    genrelabel3['text'] = genre2
    genrelabel4['text'] = genre3

''' De functie die de grafiek creeert met matplotlib en ook op de GUIscherm toont '''
def grafiek():
    response = requests.get(urlJson)
    content = json.loads(response.text)
    index = 0
    genres = {}
    for item in content:
        genres_split = item['genres'].split(";")
        for genre in genres_split:
            if genre in genres:
                genres[genre] = genres[genre] + 1
            else:
                genres[genre] = 1

    sorteddict = {key: value for key, value in sorted(genres.items(), reverse=True, key=lambda item: item[1])}
    count = 0
    most_popular = {}
    for genre in sorteddict:
        if count == 5:
            break
        most_popular[genre] = sorteddict[genre]
        count += 1

    figuur = plt.Figure(figsize=(7,4), dpi=100)
    add = figuur.add_subplot(111)
    toonfiguur = FigureCanvasTkAgg(figuur, master=genreScherm)
    toonfiguur.get_tk_widget().grid(row=5, column=0)
    plt.rcdefaults()
    fig = plt.subplots()
    y_pos = np.arange(len(most_popular))
    add.barh(y_pos,list(most_popular.values()), align='center')
    add.set_yticks(y_pos)
    add.set_yticklabels(list(most_popular.keys()))
    add.invert_yaxis()
    add.set_xlabel('Aantal games in dit genre')
    add.set_title('Populairste genres')

    
"""Is nodig voor de de quicksort. zorgt voor de wisselingen bij de sort."""
def partition(lst, low, high,zoekend):
    getal = (low - 1)
    pivot = lst[high][zoekend]
    for j in range(low, high):
        if lst[j][zoekend] <= pivot:
            getal = getal + 1
            lst[getal], lst[j] = lst[j], lst[getal]
    lst[getal + 1], lst[high] = lst[high], lst[getal + 1]
    return (getal + 1)

"""Is nodig voor de de quicksort"""
def quickSort(lst, low, high,zoekend):
    if len(lst) == 1:
        return lst
    if low < high:
        pi = partition(lst, low, high,zoekend)
        quickSort(lst, low, pi - 1,zoekend)
        quickSort(lst, pi + 1, high,zoekend)
    return lst

''''Functie die een lijst van games van het json bestand op naam sorteert'''
def sortedOnName():
    gamesTonen.delete(0,'end')
    zoek = 'name'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1,zoek)
    for item in range(n):
        gamesTonen.insert('end',arr[item][zoek])
    return

''''Functie die een lijst van games van het json bestand op naam sorteert maar dan reversed'''
def sortedOnNameRevers():
    gamesTonen.delete(0,'end')
    zoek = 'name'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1,zoek)
    for item in range(n):
        gamesTonen.insert('0',arr[item][zoek]) #tijdelijke fix?
    return

''''Functie die een lijst van games van het json bestand op prijs sorteert'''
def sortedOnPrice():
    gamesTonen.delete(0,'end')
    zoek = 'price'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1,zoek)
    for item in range(n):
        gamesTonen.insert('end','€'+str(arr[item][zoek])+'; '+ arr[item]['name'])
    return

''''Functie die een lijst van games van het json bestand op prijs sorteert maar dan reversed '''
def sortedOnPriceRevers():
    gamesTonen.delete(0,'end')
    zoek = 'price'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1,zoek)
    for item in range(n):
        gamesTonen.insert('0','€'+str(arr[item][zoek])+'; '+ arr[item]['name'])
    return

''''Functie die een lijst van games van het json bestand op reviews sorteert die positief zijn'''
def sortedOnReviewPositive():
    gamesTonen.delete(0, 'end')
    zoek = 'positive_ratings'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1, zoek)
    for item in range(n):
        gamesTonen.insert('end', str(arr[item][zoek])+'; '+ arr[item]['name'])
    return

''''Functie die een lijst van games van het json bestand op reviews sorteert die negatief zijn'''
def sortedOnReviewNegative():
    gamesTonen.delete(0, 'end')
    zoek = 'positive_ratings'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1, zoek)
    for item in range(n):
        gamesTonen.insert('0', str(arr[item][zoek])+'; '+ arr[item]['name'])
    return

''''Functie die een lijst van games van het json bestand opzoek waar naam in is gezet. Indien je naam er al voor een deel inzit wordt de game mee genomen.
Indien de lijst leeg is meld die dat (Dus niks gevonden). Er wordt gezocht met lower cases. Hierdoor kun je gewoon alles doorzoeken en gaat die niet pietje precies doen.'''
def sortedGamesZoekendOpNaam():
    gamesTonen.delete(0, 'end')
    zoek = 'name'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1, zoek)
    zoekend = zoekendEntry.get()
    for item in arr:
        item = item['name']
        if zoekend.lower() in item.lower():
            gamesTonen.insert('end',item)
    if gamesTonen.size() == 0:
        string = 'Kan de de game niet vinden...'
        gamesTonen.insert('end',string)
    return

'''Functie die voor je binair kan zoeken. De functie is nog nergens mee gekoppeld omdat ik nog niet weet waar die aan gekoppeld moet worden.
Maar hij staat er in ieder geval in. Moet waarschijnlijk nog een beetje bijgewerkt worden zodat je daarwerkelijk je index krijgt inplaats van een boolean.'''
def binaireZoekFunctie(lst,target):
    half = len(lst) // 2
    if len(lst) == 0 or len(lst)== 1 and lst[half] != target:
        return False
    elif lst[half] < target:
        return binaireZoekFunctie(lst[half:],target)
    elif lst[half] > target:
        return binaireZoekFunctie(lst[:half],target)
    else:
        return True

''' Dit is de variabele voor de gehele vriendenlijst die voor sommige functies nodig zijn'''
gehelevriendenlijst = vriendenlijst()
gamesplayedreturn = gamesplayed(gehelevriendenlijst).values()

'''Zegt hoe tkinter wordt gebruikt'''
root = Tk()
root.configure(background='#1b2838',)
root.title('Steam User Interface')
root.iconbitmap('steamicon.ico')
root.minsize(800, 600)
root.maxsize(800, 600)

'''Het begin scherm als je de GUI opent.'''
startScherm = Frame(master=root,bg = '#1b2838')
startScherm.pack()
startSchermWelkomLabel = Label(master=startScherm,text='Welkom!',bg = '#1b2838',fg='white',font=('Arial', 50, 'bold italic'))
startSchermWelkomLabel.grid(pady=30)
startSchermOnline = Button(master=startScherm,text='Vriendenlijst',command=onlineVriendenFrame,bg = '#2a475e',fg='#c7d5e0',width=15, height=2)
startSchermOnline.grid(row=1, column=0,sticky='nesw')
startSchermvriendenstat = Button(master=startScherm,text='Vriendenlijst game statistieken',command=vriendengamesFrame,bg = '#2a475e',fg='#c7d5e0',width=15, height=2)
startSchermvriendenstat.grid(row=4, column=0,sticky='nesw')
startSchermGames = Button(master=startScherm,text='Game activiteit',command=playedGamesFrame,bg = '#2a475e',fg='#c7d5e0', width=15, height=2)
startSchermGames.grid(row=3, column=0, sticky='nesw')
startSchermGameLijst = Button(master=startScherm,text='Games lijst',command=gameLijstFrame,bg = '#2a475e',fg='#c7d5e0', width=15, height=2)
startSchermGameLijst.grid(row=6, column=0,sticky='nesw')
startSchermGamestatistieken = Button(master=startScherm,text='Globale game statistieken',command=genrestatFrame,bg = '#2a475e',fg='#c7d5e0', width=15, height=2)
startSchermGamestatistieken.grid(row=5, column=0,sticky='nesw')
''' Logo Steam in beginscherm '''
logo = ImageTk.PhotoImage(Image.open("steamlogo.png"))
logolabel = Label(master=startScherm, image=logo)
logolabel.grid(row=7, column=0, padx=40, pady=40)

'''Hier staan alle instellingen voor het scherm waar je kunt zien wie online is.'''
onlineScherm = Frame(master=root,bg = '#1b2838')
onlineScherm.pack()
onlineVrienden = Label(master=onlineScherm,text='Momenteel online:    ',bg = '#1b2838',fg='#0197CF',font=(20))
onlineVrienden.grid(row=0, column=0)
vriendenonlinetonen = Label(master=onlineScherm, bg = '#1b2838', fg='white')
vriendenonlinetonen.grid(row=1, column=0)

''' Instellingen voor wie offline zijn '''
offlineVrienden = Label(master=onlineScherm,text='Momenteel offline:',bg = '#1b2838',fg='#0197CF',font=(20))
offlineVrienden.grid(row=0, column=2, pady=50)
vriendenofflinetonen = Label(master=onlineScherm, bg = '#1b2838', fg='white')
vriendenofflinetonen.grid(row=1, column=2)

'''  Instellingen voor wie afwezig zijn '''
awayVrienden = Label(master=onlineScherm,text='Momenteel afwezig:    ',bg = '#1b2838',fg='#0197CF',font=(20))
awayVrienden.grid(row=0, column=1)
vriendenawaytonen = Label(master=onlineScherm, bg = '#1b2838', fg='white')
vriendenawaytonen.grid(row=1, column=1)

''' Terugknop onlinescherm'''
terugButton = Button(master=onlineScherm, text ='Terug',command=startFrame,bg = '#2a475e',fg='#c7d5e0')
terugButton.grid(row=2, column=1)

'''Hier staan alle instellingen voor het scherm waar je kunt zien welke games gespeeld worden.'''
gamesScherm = Frame(master=root,bg = '#1b2838')
gamesScherm.pack()
gamesNuGespeeld = Label(master=gamesScherm,text='Game activiteit vrienden',font=('Arial',40, 'bold italic'),bg = '#1b2838',fg='#0197CF')
gamesNuGespeeld.grid(row=1, column=0)
gamesbericht = Label(master=gamesScherm, text='Hier kun je zien welke games jouw vrienden momenteel spelen!', font=('Arial', 10),bg = '#1b2838',fg='#0197CF')
gamesbericht.grid(row=2, column=0)
huidigeGametonen = Label(master=gamesScherm, bg = '#1b2838',fg='white', font=('Arial', 15))
huidigeGametonen.grid(row=3, column=0, pady=20, padx=10)
terugButton = Button(master=gamesScherm, text ='Terug',command=startFrame,bg = '#2a475e',fg='#c7d5e0')
terugButton.grid(row=4, column=0)
''' Dit is de lege grid zodat ik sommige dingen goed kan placeren '''
tussengrid = Label(master=gamesScherm, bg = '#1b2838')
tussengrid.grid(row=2, column=1)
legegrid = Label(master=gamesScherm, bg = '#1b2838')
legegrid.grid(row=0, column=0, pady=20)

''' Scherm voor vrienden speeltijd-, gamestatistieken  '''
vriendengames = Frame(master=root, bg='#1b2838')
vriendengames.pack()
vriendengameswel = Label(master=vriendengames, text='Gaminggedrag van vrienden',font=('Arial',40, 'bold italic'),bg='#1b2838', fg='#0197CF')
vriendengameswel.grid(row=0,column=0, pady=20)
totaaluren = Label(master=vriendengames, text='Totaal gespeelde uren afgelopen 2 weken', bg='#1b2838', fg='#c7d5e0', font=('Arial', 12))
totaaluren.grid(row=1, column=0)
totaalurentonen = Label(master=vriendengames, bg='#1b2838', fg='#187bcd')
totaalurentonen.grid(row=2, column=0)
gemiddelduren = Label(master=vriendengames, text='Gemiddeld gespeelde uren afgelopen 2 weken', bg='#1b2838', fg='#c7d5e0', font=('Arial', 12))
gemiddelduren.grid(row =3, column=0)
pervriend = Label(master=vriendengames, text='(per vriend)', bg='#1b2838', fg='#c7d5e0')
pervriend.grid(row=4, column=0)
gemiddeldurentonen = Label(master=vriendengames, bg='#1b2838', fg='#187bcd')
gemiddeldurentonen.grid(row=5, column=0)
spreidingsbreedte = Label(master=vriendengames, text='Spreidingsbreedte tussen de minst- en meest gespeelde games', bg='#1b2838', fg='#c7d5e0', font=('Arial', 12))
spreidingsbreedte.grid(row=6, column=0)
inuren = Label(master=vriendengames, text='(in uren)', bg='#1b2838', fg='#c7d5e0')
inuren.grid(row=7, column=0)
spreidingsbreedtetonen = Label(master=vriendengames, bg='#1b2838', fg='#187bcd')
spreidingsbreedtetonen.grid(row=8, column=0)
terugButton = Button(master=vriendengames, text ='Terug',command=startFrame,bg = '#2a475e',fg='#c7d5e0')
terugButton.grid(row=9, column=0, pady=50)

'''' Hier staan alle instellingen voor de globale statistieken '''
genreScherm = Frame(master=root, bg='#1b2838')
genreScherm.pack()
genrelabel1 = Label(master=genreScherm, bg = '#1b2838',fg='white',text='Populairste genres ',font=('Arial',30, 'bold italic'))
genrelabel1.grid(row=0, column=0)
genrelabel2 = Label(master=genreScherm, bg = '#1b2838',fg='white',font=('Arial',12, 'bold italic'))
genrelabel2.grid(row=2, column=0)
genrelabel3 = Label(master=genreScherm, bg = '#1b2838',fg='white',font=('Arial',12, 'bold italic'))
genrelabel3.grid(row=3, column=0)
genrelabel4 = Label(master=genreScherm, bg = '#1b2838',fg='white',font=('Arial',12, 'bold italic'))
genrelabel4.grid(row=4, column=0)
genrewelkom = Label(master=genreScherm, bg = '#1b2838',fg='white',text='in procenten van totale aantal games:' ,font=('Arial',12, 'bold italic'))
genrewelkom.grid(row=1, column=0)

terugButton = Button(master=genreScherm, text ='Terug',command=startFrame,bg = '#2a475e',fg='#c7d5e0')
terugButton.grid(row=6, column=0, pady=5)

'''Hier staan alle instellingen voor het zoeken van games in een game lijst die door school is geleverd met een json bestand.'''
gameLijstScherm = Frame(master=root,bg = '#1b2838')
gameLijstScherm.pack()
scrolbar = Scrollbar(master=gameLijstScherm)
scrolbar.grid(row=1,column=2,sticky='ns')
gamesDieErZijn = Label(master=gameLijstScherm,bg = '#1b2838',fg='white',text='Alle games: ',font=('Arial',40, 'bold italic'))
gamesDieErZijn.grid(row=0, pady=30,columnspan=2)
gamesTonen = Listbox(master=gameLijstScherm,bg = '#0197CF',fg='white',yscrollcommand=scrolbar.set,width=50)
gamesTonen.grid(row=1,columnspan=2,sticky='nesw')
scrolbar.config(command=gamesTonen.yview)
sorteerOpNaamA = Button(master=gameLijstScherm,text='Sorteer op naam A-Z',command=sortedOnName,bg = '#2a475e',fg='#c7d5e0')
sorteerOpNaamA.grid(row=2,sticky='nesw', pady=4)
sorteerOpNaamZ = Button(master=gameLijstScherm,text='Sorteer op naam Z-A',command=sortedOnNameRevers,bg = '#2a475e',fg='#c7d5e0')
sorteerOpNaamZ.grid(row=2,column=1,sticky='nesw', pady=4)
sorteerOpPrijsLaag = Button(master=gameLijstScherm,text='Sorteer op Prijs(Laag)',command=sortedOnPrice,bg = '#2a475e',fg='#c7d5e0')
sorteerOpPrijsLaag.grid(row=3,sticky='nesw', pady=4)
sorteerOpPrijsHoog = Button(master=gameLijstScherm,text='Sorteer op Prijs(Hoog)',command=sortedOnPriceRevers,bg = '#2a475e',fg='#c7d5e0')
sorteerOpPrijsHoog.grid(row=3,column=1,sticky='nesw', pady=4)
sorteerOpPositief = Button(master=gameLijstScherm,text='Sorteer op Positief',bg = '#2a475e',fg='#c7d5e0',command=sortedOnReviewPositive)
sorteerOpPositief.grid(row=4,sticky='nesw', pady=4)
sorteerOpnegatief = Button(master=gameLijstScherm,text='Sorteer op Negatief',command=sortedOnReviewNegative,bg = '#2a475e',fg='#c7d5e0')
sorteerOpnegatief.grid(row=4,column=1,sticky='nesw', pady=4)
zoekendEntry = Entry(master=gameLijstScherm)
zoekendEntry.grid(row=5,sticky='nesw', pady=4,columnspan=2)

zoekendButton = Button(master=gameLijstScherm,command=sortedGamesZoekendOpNaam, text='Zoek' , bg='#2a475e', fg='white')
zoekendButton.grid(row=5,column=2, padx=10)

terugButton = Button(master=gameLijstScherm, text ='Terug',command=startFrame,bg = '#2a475e',fg='#c7d5e0')
terugButton.grid(row=6,sticky='nesw', pady=4,columnspan=2)


startScherm.forget()
onlineScherm.forget()
gamesScherm.forget()
gameLijstScherm.forget()

startFrame()

root.mainloop()
