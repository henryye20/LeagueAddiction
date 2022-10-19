from decimal import Decimal
import arrow
import config
import cassiopeia as cass
import kill
import PySimpleGUI as sg
global stop 
stop = False
Mlimit = -1
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
                    sg.Text('0', font=('Helvetica', 20),justification='center', key='count'),
                    sg.Text(('limit: ' + str(z)) , font=('Helvetica', 20))],

                    [sg.Text('Time Played: ', font=('Helvetica', 20),justification='center'), 
                    sg.Text('0 hr(s)', font=('Helvetica', 15), key='h'),
                    sg.Text('0 min(s)', font=('Helvetica', 15), key='m'),
                    sg.Text('0 sec(s): ', font=('Helvetica', 15), key='s')],
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
            Flag = True
            if(option==0):
                t = int(timeAddT(x,y))
                if(t>=z):
                    Flag = False
                window['h'].update(str(int(t/3600))+' hr(s)')
                window['m'].update(str(int(t/60))+' min(s)')
                window['s'].update(str(int(float(Decimal(str(t/60)) % 1)*60))+' sec(s)')
            if(option==1):
                t = int(countLs(x,y))
                if(t>=z):
                    Flag = False
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
        hrlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',]
        minlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
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
            sg.In(key='-Limit-',size=(15, 1))
        ],
        [
            sg.Button("Submit",key = "sub"),
            sg.Button("back",key = "back"),
        ],
            ]
    window = sg.Window("League Addiction", layout,finalize=True)
    while True:
        event, values = window.read()
        values['-Limit-'] = (int(values['-H-'])*3600 + int(values['-M-'])*60)
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
