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
#summoner = cass.get_summoner(name="nicthequick", region="NA")
#match = summoner.match_history[5]



#checks if the dates of 2 matches are the same
def dateCheck(x,y):
    if(x.year==y.year and x.month==y.month and x.day==y.day): return True
    else: return False

#adds all the time of matches played today
def timeAddT(nam,reg):
    utc = arrow.utcnow()
    now = utc.to('US/Pacific')
    summoner = cass.get_summoner(name=nam, region=reg)
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
    print('Time: '+str(f))
    return f


def countLs(nam,reg):
    summoner = cass.get_summoner(name=nam, region=reg)
    l = 0
    sg.one_line_progress_meter(title="Checking match history", current_value=0, max_value=9,orientation='h')
    key2='OK for 1 meter'
    meter = sg.QuickMeter.active_meters[key2]
    meter.window.DisableClose = False
    utc = arrow.utcnow()
    now = utc.to('US/Pacific')


    for z in range(10):
        
        match = summoner.match_history[z]
        dateOfMatch = match.start.to('US/Pacific')
        if not sg.one_line_progress_meter(title="Checking match history", current_value=z, max_value=9, orientation='h'):
            print('no')
        if not (dateCheck(now,dateOfMatch)):
            continue
        
        if not (match.participants[summoner].team.win):
            l += 1
    print('Losses: '+str(l))
    return l

def third(x,y,z,option):
    sg.theme('SandyBeach')
    if(option==0):
        layout = [
                    [sg.Text('Time Until Next Check:', font=('Helvetica', 20),justification='center'), 
                    sg.Text('0', font=('Helvetica', 20),justification='center', key='count')],

                    [sg.Text('Time Played: ', font=('Helvetica', 20),justification='center'), 
                    sg.Text('0', font=('Helvetica', 20),justification='center', key='amount')],
                ]
    if(option==1):
        layout = [
                    [sg.Text('Time Until Next Check:', font=('Helvetica', 20),justification='center'), 
                    sg.Text('0', font=('Helvetica', 20),justification='center', key='count')],

                    [sg.Text('Losses: ', font=('Helvetica', 20),justification='center'), 
                    sg.Text('0', font=('Helvetica', 20),justification='center', key='amount')],
                ]
    window = sg.Window('Running', layout, finalize=True,grab_anywhere=True)
    p = 0
    Flag = False
    while True:                               
        event, values = window.read(timeout = 1000)
        if event == sg.WIN_CLOSED:
            break
        if(p == 0):
            p = 10
            print("checking")
            Flag = False
            if(option==0):
                t = int(timeAddT(x,y))
                if(t>=z):
                    Flag = True
            if(option==1):
                t = int(countLs(x,y))
                if(t>=z):
                    Flag = True
        window['amount'].update(t)
        p = p - 1
        window['count'].update(p)
        if(Flag):
            continue
        kill.leaguekill()

    window.close()

sg.theme('GreenMono')
def second(x,y,z,option):
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
            third(x,y,z,option)
            break
        
    window.close()


def first(option):
    if(option==0):
        layout = [
        [
            sg.Text("Summoner Name:"),
            sg.In(size=(25, 1)) 
        ],
        [
            sg.Text("Region:"),
            sg.In(size=(6, 1))
        ],
        [
            sg.Text("Limit for Time (seconds):"),
            sg.In(size=(15, 1))
        ],
        [
            sg.Button("Submit",key = "sub"),
            sg.Button("back",key = "back"),
        ],
            ]
    if(option == 1):
        layout = [
        [
            sg.Text("Summoner Name:"),
            sg.In(size=(25, 1)) 
        ],
        [
            sg.Text("Region:"),
            sg.In(size=(6, 1))
        ],
        [
            sg.Text("Limit for Losses:"),
            sg.In(size=(15, 1))
        ],
        [
            sg.Button("Submit",key = "sub"),
            sg.Button("back",key = "back"),
        ],
            ]
    window = sg.Window("League Addiction", layout,finalize=True)
    while True:
        event, values = window.read()
        if event == "cancel" or event == sg.WIN_CLOSED:
            break
        if event =="sub":
            window.close()
            second(values[0],values[1],int(values[2]),option)
        if event == "back":
            window.close()
            gaming()
    window.close()

def gaming():
    layout = [
    [
        sg.Button("Time Limit",key = "tlim"),
    ],
    [
        sg.Button("Loss Limit",key = "Llim"),
    ],
        ]
    window = sg.Window("League Addiction", layout,finalize=True)
    while True:
        event, values = window.read()
        if event == "cancel" or event == sg.WIN_CLOSED:
            break
        if event =="tlim":
            window.close()
            first(0)
        if event =="Llim":
            window.close()
            first(1)
gaming()
#timed("nicthequick","NA",40000)


#print("{name} is a level {level} summoner on the {region} server.".format(name=summoner.name,
#                                                                          level=summoner.level,
#                                                                          region=summoner.region))

#match = summoner.match_history[0]
#champion_played = match.participants[summoner].champion
#lengthOfMatch = match.duration
#print(champion_played.name)
#print(dateOfMatch)
