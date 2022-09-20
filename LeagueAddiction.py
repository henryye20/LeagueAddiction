import random
import arrow
import config
import cassiopeia as cass
from time import sleep
import kill
import PySimpleGUIQt as sg
import LeagueAddiction as la
global stop 
stop = False
Mlimit = -1
cass.set_riot_api_key(config.api_key)  # This overrides the value set in your configuration/settings.
summoner = cass.get_summoner(name="nicthequick", region="NA")

utc = arrow.utcnow()
now = utc.to('US/Pacific')

#checks if the dates of 2 matches are the same
def dateCheck(x,y):
    if(x.year==y.year and x.month==y.month and x.day==y.day): return True
    else: return False

#adds all the time of matches played today
def timeAddT(nam,reg):
    summoner = cass.get_summoner(name=nam, region=reg)
    total = 0
    f = 0
    for z in range(10):
        match = summoner.match_history[z]
        dateOfMatch = match.start.to('US/Pacific')
        
        if not (dateCheck(now,dateOfMatch)):
            continue
    
        f += match.duration.seconds
    return f

def timed(name,region,lim):
    #checks if totaltime played today is greater than the limit every 10 min
    Tlimit = lim
    while not stop:
        print("loop")
        flag = True
        t = timeAddT(name,region)
        if(t==-10): 
            print('ended early')
            break 
        p = 0
        while(t>Tlimit):
            kill.leaguekill()
            sleep(1)
            p += 1
            if(stop):break
            if(p==120):
                flag = False
                break
        if(stop):break
        if flag: sleep(2)   

sg.theme('GreenMono')
def second(x,y,z):
    layout = [
    [
        sg.Text("Click to Start"),
    ],
    [
        sg.Button("Start",key = "start"),
    ],
    [
        sg.Button("Stop",key = "stop"),
    ],
        ]
    window = sg.Window("Second Window", layout)
    stop = False
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        #doesnt work 
        if event == "start":
            stop = False
        if event == "stop":
            stop = True
            break
        
    window.close()


def first():
    layout = [
    [
        sg.Text("Input Summoner Name:"),
        sg.In(size=(25, 1)) 
    ],
    [
        sg.Text("Input Region:"),
        sg.In(size=(6, 1))
    ],
    [
        sg.Text("Input Limit (seconds):"),
        sg.In(size=(15, 1))
    ],
    [
        sg.Button("Submit",key = "sub"),
    ],
        ]
    window = sg.Window("League Addiction", layout)
    while True:
        event, values = window.read()
        if event == "cancel" or event == sg.WIN_CLOSED:
            break
        if event =="sub":
            second(values[0],values[1],int(values[2]))
               
    window.close()
first()
#timed("nicthequick","NA",40000)


#print("{name} is a level {level} summoner on the {region} server.".format(name=summoner.name,
#                                                                          level=summoner.level,
#                                                                          region=summoner.region))

#match = summoner.match_history[0]
#champion_played = match.participants[summoner].champion
#lengthOfMatch = match.duration
#print(champion_played.name)
#print(dateOfMatch)
