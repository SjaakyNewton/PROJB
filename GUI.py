import tkinter
import requests
import json

url = 'https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json'

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
    root.geometry('400x400')
    #vrienden die online zijn moeten getoond worden, ook wat je verwacht wat online komt.

def playedGamesFrame():
    startScherm.forget()
    gamesScherm.pack()
    root.geometry('400x400')
    #games die gespeeld worden en mogelijk nu gespeeld worden.

def gameLijstFrame():
    startScherm.forget()
    gameLijstScherm.pack()
    #gamesDieErZijn['text'] = sortedOnName()
    sortedOnName()
    root.geometry('400x400')

def jsonFunctie():
    ''''Functie die het json bestand uitleest. Dit schilt in elke andere functie de moeite om het ergens vandaan te halen.
    Met een regel kan iets de content gebruikt.'''
    response = requests.get(url)
    content = json.loads(response.text)
    return content


def sortedOnName():
    ''''Functie die een lijst van games van het json bestand op naam sorteert'''
    gamesTonen.delete(0,'end')
    content = jsonFunctie()
    game = sorted(content, key=lambda item: item.get('name'))
    string = ''
    for item in game:
        gamesTonen.insert('end',item['name'])
    return string

def sortedOnNameRevers():
    ''''Functie die een lijst van games van het json bestand op naam sorteert maar dan reversed'''
    gamesTonen.delete(0,'end')
    content = jsonFunctie()
    game = sorted(content, key=lambda item: item.get('name'),reverse=True)
    string = ''
    for item in game:
        gamesTonen.insert('end',item['name'])
    return string

def sortedOnPrice():
    ''''Functie die een lijst van games van het json bestand op prijs sorteert'''
    gamesTonen.delete(0, 'end')
    content = jsonFunctie()
    game = sorted(content, key=lambda item: item.get('price'))
    string = ''
    for item in game:
        gamesTonen.insert('end','€'+str(item['price'])+'; '+ item['name'])
    return string

def sortedOnPriceRevers():
    ''''Functie die een lijst van games van het json bestand op prijs sorteert maar dan reversed '''
    gamesTonen.delete(0, 'end')
    content = jsonFunctie()
    game = sorted(content, key=lambda item: item.get('price'),reverse=True)
    string = ''
    for item in game:
        gamesTonen.insert('end','€'+str(item['price'])+'; '+ item['name'])
    return string

def sortedOnReviewPositive():
    ''''Functie die een lijst van games van het json bestand op reviews sorteert die positief zijn'''
    gamesTonen.delete(0, 'end')
    content = jsonFunctie()
    game = sorted(content, key=lambda item: item.get('positive_ratings'),reverse=True)
    string = ''
    for item in game:
        gamesTonen.insert('end',str(item['positive_ratings'])+'; '+ item['name'])
    return string

def sortedOnReviewNegative():
    ''''Functie die een lijst van games van het json bestand op reviews sorteert die negatief zijn'''
    gamesTonen.delete(0, 'end')
    content = jsonFunctie()
    game = sorted(content, key=lambda item: item.get('negative_ratings'),reverse=True)
    string = ''
    for item in game:
        gamesTonen.insert('end',str(item['negative_ratings'])+'; '+ item['name'])
    return string


# def sortedGames():
#     #Een sorteer op de spelnaam


root = tkinter.Tk()
root.configure(background='#1b2838',)
root.title('Steam AI')
#root.maxsize(600,400)


startScherm = tkinter.Frame(master=root,bg = '#1b2838')
startScherm.pack()
startSchermWelkomLabel = tkinter.Label(master=startScherm,text='Welkom!',bg = '#1b2838',fg='white',font=(30))
startSchermWelkomLabel.grid(pady=10)
startSchermOnline = tkinter.Button(master=startScherm,text='Online vrienden',command=onlineVriendenFrame,bg = '#2a475e',fg='#c7d5e0',width=20)
startSchermOnline.grid(row=1, column=0, pady=4,sticky='nesw')
startSchermGames = tkinter.Button(master=startScherm,text='Games',command=playedGamesFrame,bg = '#2a475e',fg='#c7d5e0')
startSchermGames.grid(row=2, column=0, pady=4,sticky='nesw')
startSchermGameLijst = tkinter.Button(master=startScherm,text='Games lijst',command=gameLijstFrame,bg = '#2a475e',fg='#c7d5e0')
startSchermGameLijst.grid(row=3, column=0, pady=4,sticky='nesw')


onlineScherm = tkinter.Frame(master=root,bg = '#1b2838')
onlineScherm.pack()
onlineVrienden = tkinter.Label(master=onlineScherm,text='Momenteel online:',bg = '#1b2838',fg='#0197CF',font=(20))
onlineVrienden.grid(pady=3,sticky='nesw')
mogelijkOnline = tkinter.Label(master=onlineScherm,text='Deze vrienden zijn nu vaak online:',bg = '#0197CF',fg='white')
#mogelijkOnline.grid(pady=3,sticky='nesw')
terugButton = tkinter.Button(master=onlineScherm, text ='Terug',command=startFrame,bg = '#2a475e',fg='#c7d5e0')
terugButton.grid(sticky='nesw')


gamesScherm = tkinter.Frame(master=root,bg = '#1b2838')
gamesScherm.pack()
gamesNuGespeeld = tkinter.Label(master=gamesScherm,text='Games die nu gespeeld worden:',bg = '#0197CF',fg='white')
gamesNuGespeeld.grid(pady=3,sticky='nesw')
huidigeGame = tkinter.Label(master=gamesScherm, text='Dit is tijdelijk weg gehaald door Isaak',bg = '#0197CF',fg='white')
huidigeGame.grid(pady=3,sticky='nesw')
#Dit moet nog gekoppeld worden met de API daarom heb ik iets hier wegghaald. Ook omdat ik de jsonFunctie heb aangepast.

gamesMogelijkGespeeld = tkinter.Label(master=gamesScherm,text='Games die nu mogelijk gespeeld worden:',bg = '#0197CF',fg='white')
gamesMogelijkGespeeld.grid(pady=3,sticky='nesw')
terugButton = tkinter.Button(master=gamesScherm, text ='Terug',command=startFrame,bg = '#2a475e',fg='#c7d5e0')
terugButton.grid(sticky='nesw')


gameLijstScherm = tkinter.Frame(master=root,bg = '#1b2838')
gameLijstScherm.pack()
scrolbar = tkinter.Scrollbar(master=gameLijstScherm)
scrolbar.grid(row=1,column=2,sticky='nesw')
gamesDieErZijn = tkinter.Label(master=gameLijstScherm,bg = '#1b2838',fg='white',text='Alle games: ',font=(20))
gamesDieErZijn.grid(row=0, pady=4,columnspan=2)
gamesTonen = tkinter.Listbox(master=gameLijstScherm,bg = '#0197CF',fg='white',yscrollcommand=scrolbar.set,width=50)
gamesTonen.grid(row=1,columnspan=2,sticky='nesw')
scrolbar.config(command=gamesTonen.yview)
sorteerOpNaamA = tkinter.Button(master=gameLijstScherm,text='Sorteer op naam A-Z',command=sortedOnName,bg = '#2a475e',fg='#c7d5e0')
sorteerOpNaamA.grid(row=2,sticky='nesw', pady=4)
sorteerOpNaamZ = tkinter.Button(master=gameLijstScherm,text='Sorteer op naam Z-A',command=sortedOnNameRevers,bg = '#2a475e',fg='#c7d5e0')
sorteerOpNaamZ.grid(row=2,column=1,sticky='nesw', pady=4)
sorteerOpPrijsLaag = tkinter.Button(master=gameLijstScherm,text='Sorteer op Prijs(Laag)',command=sortedOnPrice,bg = '#2a475e',fg='#c7d5e0')
sorteerOpPrijsLaag.grid(row=3,sticky='nesw', pady=4)
sorteerOpPrijsHoog = tkinter.Button(master=gameLijstScherm,text='Sorteer op Prijs(Hoog)',command=sortedOnPriceRevers,bg = '#2a475e',fg='#c7d5e0')
sorteerOpPrijsHoog.grid(row=3,column=1,sticky='nesw', pady=4)
sorteerOpPositief = tkinter.Button(master=gameLijstScherm,text='Sorteer op Positief',command=sortedOnReviewPositive,bg = '#2a475e',fg='#c7d5e0')
sorteerOpPositief.grid(row=4,sticky='nesw', pady=4)
sorteerOpnegatief = tkinter.Button(master=gameLijstScherm,text='Sorteer op Negatief',command=sortedOnReviewNegative,bg = '#2a475e',fg='#c7d5e0')
sorteerOpnegatief.grid(row=4,column=1,sticky='nesw', pady=4)
terugButton = tkinter.Button(master=gameLijstScherm, text ='Terug',command=startFrame,bg = '#2a475e',fg='#c7d5e0')
terugButton.grid(row=6,sticky='nesw', pady=4,columnspan=2)


startScherm.forget()
onlineScherm.forget()
gamesScherm.forget()
gameLijstScherm.forget()

startFrame()

root.mainloop()
