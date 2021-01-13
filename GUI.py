from tkinter import *
from PIL import ImageTk,Image
import requests
import json
import os
import sys

sys.setrecursionlimit(4000)

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

url = 'https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json'
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

def startFrame():
    onlineScherm.forget()
    gamesScherm.forget()
    gameLijstScherm.forget()
    startScherm.pack()
    root.geometry('400x400')
    #optie scherm met wat je wilt zien

def onlineVriendenFrame():
    startScherm.forget()
    onlineScherm.pack()
    vriendeninfo(vriendenlijst())
    root.geometry('400x400')
    #vrienden die online zijn moeten getoond worden, ook wat je verwacht wat online komt.

def playedGamesFrame():
    startScherm.forget()
    ingame(vriendenlijst())
    gamesScherm.pack()
    root.geometry('400x400')
    #games die gespeeld worden en mogelijk nu gespeeld worden.

def gameLijstFrame():
    startScherm.forget()
    gameLijstScherm.pack()
    #gamesDieErZijn['text'] = sortedOnName()
    sortedOnName()
    root.geometry('400x400')
    #Games die in steam staan. Worden uit een json bestand gehaald

def jsonFunctie():
    ''''Functie die het json bestand uitleest. Dit schilt in elke andere functie de moeite om het ergens vandaan te halen.
    Met een regel kan iets de content gebruikt.'''
    response = requests.get(url)
    content = json.loads(response.text)
    return content

def vriendenlijst():
    json_data_vriendenlijst = requests.get('http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=B99D1FC3DA15306CAB4D188601446F66&steamid=76561198135983674&relationship=friend&format=json')
    json_formatted_vriendenlijst = json.loads(json_data_vriendenlijst.text)
    lijstmetid = []
    for i in json_formatted_vriendenlijst['friendslist']['friends']:
        lijstmetid.append(i['steamid'])
    return lijstmetid
    #dit is een functie die de STEAMIDs in een lijst stopt om te gebruiken voor online vriendeninfo functie hieronder

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

def partition(arr, low, high,zoekend):
    i = (low - 1)
    pivot = arr[high][zoekend]
    for j in range(low, high):
        if arr[j][zoekend] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)

def quickSort(arr, low, high,zoekend):
    if len(arr) == 1:
        return arr
    if low < high:
        pi = partition(arr, low, high,zoekend)
        quickSort(arr, low, pi - 1,zoekend)
        quickSort(arr, pi + 1, high,zoekend)
    return arr

def sortedOnName():
    ''''Functie die een lijst van games van het json bestand op naam sorteert'''
    gamesTonen.delete(0,'end')
    zoek = 'name'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1,zoek)
    for item in range(n):
        gamesTonen.insert('end',arr[item][zoek])
    return

def sortedOnNameRevers():
    ''''Functie die een lijst van games van het json bestand op naam sorteert maar dan reversed'''
    gamesTonen.delete(0,'end')
    zoek = 'name'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1,zoek)
    for item in range(n):
        gamesTonen.insert('0',arr[item][zoek]) #tijdelijke fix?
    return

def sortedOnPrice():
    ''''Functie die een lijst van games van het json bestand op prijs sorteert'''
    gamesTonen.delete(0,'end')
    zoek = 'price'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1,zoek)
    for item in range(n):
        gamesTonen.insert('end','€'+str(arr[item][zoek])+'; '+ arr[item]['name'])
    return

def sortedOnPriceRevers():
    ''''Functie die een lijst van games van het json bestand op prijs sorteert maar dan reversed '''
    gamesTonen.delete(0,'end')
    zoek = 'price'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1,zoek)
    for item in range(n):
        gamesTonen.insert('0','€'+str(arr[item][zoek])+'; '+ arr[item]['name'])
    return

def sortedOnReviewPositive():
    ''''Functie die een lijst van games van het json bestand op reviews sorteert die positief zijn'''
    gamesTonen.delete(0, 'end')
    zoek = 'positive_ratings'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1, zoek)
    for item in range(n):
        gamesTonen.insert('end', str(arr[item][zoek])+'; '+ arr[item]['name'])
    return

def sortedOnReviewNegative():
    ''''Functie die een lijst van games van het json bestand op reviews sorteert die negatief zijn'''
    gamesTonen.delete(0, 'end')
    zoek = 'positive_ratings'
    arr = jsonFunctie()
    n = len(arr)
    quickSort(arr, 0, n - 1, zoek)
    for item in range(n):
        gamesTonen.insert('0', str(arr[item][zoek])+'; '+ arr[item]['name'])
    return


def sortedGamesZoekendOpNaam():
    ''''Functie die een lijst van games van het json bestand opzoek waar naam in is gezet. Indien je naam er al voor een deel inzit wordt de game mee genomen.
    Indien de lijst leeg is meld die dat (Dus niks gevonden). Er wordt gezocht met lower cases. Hierdoor kun je gewoon alles doorzoeken en gaat die niet pietje precies doen.'''
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

def binaireZoekFunctie(lst,target):
    '''Functie die voor je binair kan zoeken. De functie is nog nergens mee gekoppeld omdat ik nog niet weet waar die aan gekoppeld moet worden.
    Maar hij staat er in ieder geval in. Moet waarschijnlijk nog een beetje bijgewerkt worden zodat je daarwerkelijk je index krijgt inplaats van een boolean.'''
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

'''Zegt hoe tkinter wordt gebruikt'''
root = Tk()
root.configure(background='#1b2838',)
root.title('Steam AI')
root.iconbitmap('steamicon.ico')
root.minsize(700, 500)
root.maxsize(700, 500)

'''Het begin scherm als je de GUI opent.'''
startScherm = Frame(master=root,bg = '#1b2838')
startScherm.pack()
startSchermWelkomLabel = Label(master=startScherm,text='Welkom!',bg = '#1b2838',fg='white',font=('Arial', 50, 'bold italic'))
startSchermWelkomLabel.grid(pady=30)
startSchermOnline = Button(master=startScherm,text='Vriendenlijst',command=onlineVriendenFrame,bg = '#2a475e',fg='#c7d5e0',width=15, height=2)
startSchermOnline.grid(row=1, column=0, pady=15,sticky='nesw')
startSchermGames = Button(master=startScherm,text='Game activiteit',command=playedGamesFrame,bg = '#2a475e',fg='#c7d5e0', width=15, height=2)
startSchermGames.grid(row=2, column=0, pady=15,sticky='nesw')
startSchermGameLijst = Button(master=startScherm,text='Games lijst',command=gameLijstFrame,bg = '#2a475e',fg='#c7d5e0', width=15, height=2)
startSchermGameLijst.grid(row=3, column=0, pady=15,sticky='nesw')
''' Logo Steam in beginscherm '''
logo = ImageTk.PhotoImage(Image.open("steamlogo.png"))
logolabel = Label(master=startScherm, image=logo)
logolabel.grid(row=4, column=0, padx=40)

'''Hier staan alle instellingen voor het scherm waar je kunt zien wie online is. Moet nog gekoppeld worden aan Steam API.'''
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

'''  Instellingen voor degene die mogelijk online zijn  '''
mogelijkOnline = Label(master=onlineScherm,text='Deze vrienden zijn nu vaak online:',bg = '#0197CF',fg='white')
#mogelijkOnline.grid(pady=3,sticky='nesw')

''' Terugknop onlinescherm'''
terugButton = Button(master=onlineScherm, text ='Terug',command=startFrame,bg = '#2a475e',fg='#c7d5e0')
terugButton.grid(row=2, column=1)

'''Hier staan alle instellingen voor het scherm waar je kunt zien welke games gespeeld worden. Moet nog gekoppeld worden aan Steam API.'''
gamesScherm = Frame(master=root,bg = '#1b2838')
gamesScherm.pack()
gamesNuGespeeld = Label(master=gamesScherm,text='Huidig gespeelde games:',font=('bold italic', 18) ,bg = '#1b2838',fg='white')
gamesNuGespeeld.grid(row=0, column=0, pady=10, padx=10)
huidigeGametonen = Label(master=gamesScherm, bg = '#1b2838',fg='white')
huidigeGametonen.grid(pady=3,sticky='nesw')

#Dit moet nog gekoppeld worden met de API daarom heb ik iets hier wegghaald. Ook omdat ik de jsonFunctie heb aangepast.
gamesMogelijkGespeeld = Label(master=gamesScherm,text='Mogelijke gespeelde games:',font=('bold italic', 18),bg = '#1b2838',fg='white')
gamesMogelijkGespeeld.grid(row=0, column=2, pady=10, padx=10)
terugButton = Button(master=gamesScherm, text ='Terug',command=startFrame,bg = '#2a475e',fg='#c7d5e0')
terugButton.grid(sticky='nesw')

'''Hier staan alle instellingen voor het zoeken van games in een game lijst die door school is geleverd met een json bestand.'''
gameLijstScherm = Frame(master=root,bg = '#1b2838')
gameLijstScherm.pack()
scrolbar = Scrollbar(master=gameLijstScherm)
scrolbar.grid(row=1,column=2,sticky='nesw')
gamesDieErZijn = Label(master=gameLijstScherm,bg = '#1b2838',fg='white',text='Alle games: ',font=(20))
gamesDieErZijn.grid(row=0, pady=4,columnspan=2)
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
zoekendButton = Button(master=gameLijstScherm,command=sortedGamesZoekendOpNaam)
zoekendButton.grid(row=5,column=2,sticky='nesw')
terugButton = Button(master=gameLijstScherm, text ='Terug',command=startFrame,bg = '#2a475e',fg='#c7d5e0')
terugButton.grid(row=6,sticky='nesw', pady=4,columnspan=2)


startScherm.forget()
onlineScherm.forget()
gamesScherm.forget()
gameLijstScherm.forget()

startFrame()

root.mainloop()
