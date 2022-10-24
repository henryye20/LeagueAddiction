from decimal import Decimal
import arrow
import config
import cassiopeia as cass
import kill
import random
import PySimpleGUI as sg
import bible
cass.set_riot_api_key(config.api_key)  # This overrides the value set in your configuration/settings.
#summoner = cass.get_summoner(name="nicthequick", region="NA")
#match = summoner.match_history[5]
#a = 5.1
#print(int(a))
#b = str(float(Decimal(str(a/60)) % 1)*60)
#print(b)

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
    r = 15
    sg.one_line_progress_meter(title="Checking match history", current_value=0, max_value=r-1,orientation='h')
    key='OK for 1 meter'
    meter = sg.QuickMeter.active_meters[key]
    meter.window.DisableClose = False
    

    for z in range(r):
        match = summoner.match_history[z]
        dateOfMatch = match.start.to('US/Pacific')
    
        if not sg.one_line_progress_meter(title="Checking match history", current_value=z, max_value=r-1, orientation='h'):
            print('no')
        if not (dateCheck(now,dateOfMatch)):
            continue
    
        f += match.duration.seconds
    print('Time: '+str(f))
    return f


def countLs(nam,reg):
    summoner = cass.get_summoner(name=nam, region=reg)
    l = 0
    r = 15
    sg.one_line_progress_meter(title="Checking match history", current_value=0, max_value=r-1,orientation='h')
    key2='OK for 1 meter'
    meter = sg.QuickMeter.active_meters[key2]
    meter.window.DisableClose = False
    utc = arrow.utcnow()
    now = utc.to('US/Pacific')

    for z in range(r):
        
        match = summoner.match_history[z]
        dateOfMatch = match.start.to('US/Pacific')
        if not sg.one_line_progress_meter(title="Checking match history", current_value=z, max_value=r-1, orientation='h'):
            print('no')
        if not (dateCheck(now,dateOfMatch)):
            continue
        
        if not (match.participants[summoner].team.win):
            l += 1
    print('Losses: '+str(l))
    return l

def countGs(nam,reg):
    summoner = cass.get_summoner(name=nam, region=reg)
    g = 0
    r = 15
    sg.one_line_progress_meter(title="Checking match history", current_value=0, max_value=r-1,orientation='h')
    key2='OK for 1 meter'
    meter = sg.QuickMeter.active_meters[key2]
    meter.window.DisableClose = False
    utc = arrow.utcnow()
    now = utc.to('US/Pacific')

    for z in range(r):
        
        match = summoner.match_history[z]
        dateOfMatch = match.start.to('US/Pacific')
        if not sg.one_line_progress_meter(title="Checking match history", current_value=z, max_value=r-1, orientation='h'):
            print('no')
        if not (dateCheck(now,dateOfMatch)):
            continue
        g += 1

    print('Games: '+str(g))
    return g


def third(x,y,z,option):
    sg.theme('SandyBeach')
    if(option==0):
        h = (int(z/3600))
        layout = [
                    [sg.Text('User: ' + str(x), font=('Helvetica', 20),justification='center')],

                    [sg.Text('Time Until Next Check:', font=('Helvetica', 20),justification='center'), 
                    sg.Text('0', font=('Helvetica', 20),justification='center', key='count'),
                    sg.Text(('limit: ' + str(h)+ 'hr(s)') , font=('Helvetica', 20)),
                    sg.Text(('' + str(int(z/60)-(60*h))+ 'min(s)') , font=('Helvetica', 20))],

                    [sg.Text('Time Played: ', font=('Helvetica', 20),justification='center'), 
                    sg.Text('0 hr(s)', font=('Helvetica', 15), key='h'),
                    sg.Text('0 min(s)', font=('Helvetica', 15), key='m'),
                    sg.Text('0 sec(s): ', font=('Helvetica', 15), key='s'),
                    sg.Text(':)',text_color='green',font=('Helvetica', 20),key='-k-')],

                    [sg.Text(bible.getRandVerse())]
                ]
    if(option==1):
        layout = [
                    [sg.Text('User: ' + str(x), font=('Helvetica', 20),justification='center')],
                    [sg.Text('Time Until Next Check:', font=('Helvetica', 20),justification='center'), 
                    sg.Text('0', font=('Helvetica', 20),justification='center', key='count'),
                    sg.Text(('limit: ' + str(z)+ ' Ls') , font=('Helvetica', 20))],

                    [sg.Text('Losses: ', font=('Helvetica', 20),justification='center'), 
                    sg.Text('0', font=('Helvetica', 20),justification='center', key='amount'),
                    sg.Text(':)',text_color='green',font=('Helvetica', 20),key='-k-')],

                    [sg.Text(bible.getRandVerse())]
                ]
    if(option==2):
        layout = [
                    [sg.Text('User: ' + str(x), font=('Helvetica', 20),justification='center')],
                    [sg.Text('Time Until Next Check:', font=('Helvetica', 20),justification='center'), 
                    sg.Text('0', font=('Helvetica', 20),justification='center', key='count'),
                    sg.Text(('limit: ' + str(z)+ ' Game(s)') , font=('Helvetica', 20))],

                    [sg.Text('Games: ', font=('Helvetica', 20),justification='center'), 
                    sg.Text('0', font=('Helvetica', 20),justification='center', key='amount'),
                    sg.Text(':)',text_color='green',font=('Helvetica', 20),key='-k-')],

                    [sg.Text(bible.getRandVerse())]
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
            Flag = True
            if(option==0):
                t = int(timeAddT(x,y))
                if(t>=z):
                    Flag = False
                    window['-k-'].update('killing',text_color='red')
                h = int(t/3600)
                if(Flag): sg.Text(':)',text_color='green',key='-k-')
                window['h'].update(str(h)+' hr(s)')
                window['m'].update(str(int(t/60)-(60*h))+' min(s)')
                window['s'].update(str(int(float(Decimal(str(t/60)) % 1)*60))+' sec(s)')
            if(option==1):
                t = int(countLs(x,y))
                if(t>=z):
                    Flag = False
                    window['-k-'].update('killing',text_color='red')
                window['amount'].update(t)
            if(option==2):
                g = int(countGs(x,y))
                if(g>=z):
                    Flag = False
                    window['-k-'].update('killing',text_color='red')
                window['amount'].update(g)
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
            sg.In(key='-Name-',size=(25, 1)) 
        ],
        [
            sg.Text("Region:"),
            sg.In(key='-Region-',size=(6, 1))
        ],
        [
            sg.Text("Limit for Time:"),
            sg.In(key='-H-',size=(6, 1)),
            sg.Text("hr(s)"),
            sg.In(key='-M-',size=(6, 1)),
            sg.Text("min(s)"),
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
            sg.In(key='-Name-',size=(25, 1)) 
        ],
        [
            sg.Text("Region:"),
            sg.In(key='-Region-',size=(6, 1))
        ],
        [
            sg.Text("Limit for Losses:"),
            sg.In(key='-Limit-',size=(8, 1))
        ],
        [
            sg.Button("Submit",key = "sub"),
            sg.Button("back",key = "back"),
        ],
            ]
    if(option == 2):
        layout = [
        [
            sg.Text("Summoner Name:"),
            sg.In(key='-Name-',size=(25, 1)) 
        ],
        [
            sg.Text("Region:"),
            sg.In(key='-Region-',size=(6, 1))
        ],
        [
            sg.Text("Limit for Games: "),
            sg.In(key='-Limit-',size=(8, 1))
        ],
        [
            sg.Button("Submit",key = "sub"),
            sg.Button("back",key = "back"),
        ],
            ]
    window = sg.Window("League Addiction", layout,finalize=True)
    while True:
        event, values = window.read()

        if(option ==0): values['-Limit-'] = (int(values['-H-'])*3600 + int(values['-M-'])*60)
        if event == "cancel" or event == sg.WIN_CLOSED:
            break
        if event =="sub":
            window.close()
            second(values['-Name-'],values['-Region-'],int(values['-Limit-']),option)
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
    [
        sg.Button("Game Limit",key = "Glim"),
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
        if event =="Glim":
            window.close()
            first(2)
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
