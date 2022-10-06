import random
import arrow
import config
import cassiopeia as cass
from time import sleep
import kill
import PySimpleGUI as sg
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
    sg.one_line_progress_meter(title="Checking match history", current_value=0, max_value=9,orientation='h')
    key='OK for 1 meter'
    meter = sg.QuickMeter.active_meters[key]
    meter.window.DisableClose = False
    


    for z in range(10):
        match = summoner.match_history[z]
        dateOfMatch = match.start.to('US/Pacific')
    
        if not sg.one_line_progress_meter(title="Checking match history", current_value=z, max_value=9, orientation='h'):
            print('no')
        if not (dateCheck(now,dateOfMatch)):
            continue
    
        f += match.duration.seconds
    return f
def check(name,region,lim):
    
    Tlimit = lim
    print("loop")
    t = int(timeAddT(name,region))
    if(t>=Tlimit):
        return True
    return False

def third(x,y,z):
    sg.theme('SandyBeach')
    layout = [[sg.Text('10.0', size=(8, 2), font=('Helvetica', 20),
                justification='center', key='text')],]
    window = sg.Window('Running', layout, finalize=True,grab_anywhere=True)
    p = 10
    while True: 
        # Please try and use as high of a timeout value as you can                               
        event, values = window.read(timeout = 1000) 
        # if user closed the window using X or clicked Quit button
        Flag = False
        if event == sg.WIN_CLOSED:
            break
        if(p == 0):
            p = 10
            print("checking")
            if not (check(x,y,z)):
                Flag = True
        if(Flag):
            continue
        kill.leaguekill()
        p = p - 1
        window['text'].update(p)
        #window.refresh()
    window.close()

sg.theme('GreenMono')
def second(x,y,z):
    layout = [
    [
        sg.Text("Click to Start"),
    ],
    [
        sg.Button("Start",key = "start"),
    ],
        ]
    window = sg.Window("Second Window", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        # 
        if event == "start":
            window.close()
            third(x,y,z)
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
    window = sg.Window("League Addiction", layout,finalize=True)
    while True:
        event, values = window.read()
        if event == "cancel" or event == sg.WIN_CLOSED:
            break
        if event =="sub":
            window.close()
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
