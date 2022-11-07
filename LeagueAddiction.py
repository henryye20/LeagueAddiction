from decimal import Decimal
import arrow
import config
import cassiopeia as cass
import kill
import sys
import PySimpleGUI as sg
import bible
cass.set_riot_api_key(config.api_key)  # This overrides the value set in your configuration/settings.
sg.theme('SystemDefault1')
#summoner = cass.get_summoner(name="nicthequick", region="NA")
#match = summoner.match_history[2]
#try:
#    if not (str(match.queue)=='Queue.ranked_solo_fives'):
#        print('hi')
#except: 
#    print('Weird match type skipping...')


#checks if the dates of 2 matches are the same
def dateCheck(x,y):
    if(x.year==y.year and x.month==y.month and x.day==y.day): return True
    else: return False

#adds all the time of matches played today
def timeAddT(nam,reg,ranked):
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
        if(ranked):
            try:
                if not (str(match.queue)=='Queue.ranked_solo_fives'):
                    continue
            except: 
                print('Weird match type skipping...')
                continue
        if not (dateCheck(now,dateOfMatch)):
            continue
    
        f += match.duration.seconds
    print('Time: '+str(f))
    return f


def countLs(nam,reg,ranked):
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
        if(ranked):
            try:
                q = match.queue
                if not (str(q)=='Queue.ranked_solo_fives'):
                    print(q)
                    continue
            except: 
                print('Weird match type skipping...')
                continue
        if not (dateCheck(now,dateOfMatch)):
            continue
        
        if not (match.participants[summoner].team.win):
            l += 1
    print('Losses: '+str(l))
    return l


def countGs(nam,reg,ranked):
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
        if(ranked):
            try:
                q = match.queue
                if not (str(q)=='Queue.ranked_solo_fives'):
                    print(q)
                    continue
            except: 
                print('Weird match type skipping...')
                continue
        if not (dateCheck(now,dateOfMatch)):
            continue
        g += 1

    print('Games: '+str(g))
    return g

def checkKDA(nam,reg,ranked,assists):
    summoner = cass.get_summoner(name=nam, region=reg)
    r=15
    kda = sys.maxsize
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
        if(ranked):
            try:
                q = match.queue
                if not (str(q)=='Queue.ranked_solo_fives'):
                    print(q)
                    continue
            except: 
                print('Weird match type skipping...')
                continue
        #if not (dateCheck(now,dateOfMatch)):
        #   continue
        matchkda = match.participants[summoner].stats.kda
        if(assists) and (float(matchkda)<kda):
            kda = matchkda
        else:
            kills = match.participants[summoner].stats.kills
            deaths = match.participants[summoner].stats.deaths
            if(deaths==0): 
                tkda = kills
            else: 
                tkda = kills/deaths
            if(float(tkda)<kda):
                kda = tkda
    print('KDA: '+str(kda))
    return kda


def third(x,y,z,option,ranked,assists):
    
    if(option==0):
        h = (int(z/3600))
        layout = [
                    [sg.Text('User: ' + str(x), justification='center')],

                    [sg.Text('Time Until Next Check:', justification='center'), 
                    sg.Text('0', justification='center', key='count'),
                    sg.Text(('limit: ' + str(h)+ 'hr(s)')),
                    sg.Text(('' + str(int(z/60)-(60*h))+ 'min(s)'))],

                    [sg.Text('Time Played: ', justification='center'), 
                    sg.Text('0 hr(s)', key='h'),
                    sg.Text('0 min(s)', key='m'),
                    sg.Text('0 sec(s): ', key='s'),
                    sg.Text(':)',text_color='green',key='-k-')],

                    [sg.Text(bible.getRandVerse())]
                ]
    if(option==1):
        layout = [
                    [sg.Text('User: ' + str(x), justification='center')],
                    [sg.Text('Time Until Next Check:', justification='center'), 
                    sg.Text('0', justification='center', key='count'),
                    sg.Text(('limit: ' + str(z)+ ' Ls') , )],

                    [sg.Text('Losses: ', justification='center'), 
                    sg.Text('0', justification='center', key='amount'),
                    sg.Text(':)',text_color='green',key='-k-')],

                    [sg.Text(bible.getRandVerse())]
                ]
    if(option==2):
        layout = [
                    [sg.Text('User: ' + str(x), justification='center')],
                    [sg.Text('Time Until Next Check:', justification='center'), 
                    sg.Text('0', justification='center', key='count'),
                    sg.Text(('limit: ' + str(z)+ ' Game(s)'))],

                    [sg.Text('Games: ', justification='center'), 
                    sg.Text('0', justification='center', key='amount'),
                    sg.Text(':)',text_color='green',key='-k-')],

                    [sg.Text(bible.getRandVerse())]
                ]
    if(option==3):
        layout = [
                    [sg.Text('User: ' + str(x), justification='center')],
                    [sg.Text('Time Until Next Check:', justification='center'), 
                    sg.Text('0', justification='center', key='count'),
                    sg.Text(('KDAlimit: ' + str(z)))],

                    [sg.Text('Lowest KDA: ', justification='center'), 
                    sg.Text('no games today', justification='center', key='amount'),
                    sg.Text(':)',text_color='green',key='-k-')],

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
            p = 60
            print("checking")
            Flag = True
            if(option==0):
                t = int(timeAddT(x,y,ranked))
                if(t>=z):
                    Flag = False
                    window['-k-'].update('killing',text_color='red')
                h = int(t/3600)
                if(Flag): sg.Text(':)',text_color='green',key='-k-')
                window['h'].update(str(h)+' hr(s)')
                window['m'].update(str(int(t/60)-(60*h))+' min(s)')
                window['s'].update(str(int(float(Decimal(str(t/60)) % 1)*60))+' sec(s)')
            if(option==1):
                t = int(countLs(x,y,ranked))
                if(t>=z):
                    Flag = False
                    window['-k-'].update('killing',text_color='red')
                window['amount'].update(t)
            if(option==2):
                g = int(countGs(x,y,ranked,))
                if(g>=z):
                    Flag = False
                    window['-k-'].update('killing',text_color='red')
                window['amount'].update(g)
            if(option==3):
                kda = float(checkKDA(x,y,ranked,assists))
                if(kda<z):
                    Flag = False
                    window['-k-'].update('killing',text_color='red')
                if not (kda>=sys.maxsize):
                    window['amount'].update(kda)
        p = p - 1
        window['count'].update(p)
        if(Flag):
            continue
        kill.leaguekill()

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
            sg.In(key='-Region-',size=(6, 1)),
            sg.Checkbox('Check Ranked ONLY', default=False, key="-Ranked-")
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
            sg.In(key='-Region-',size=(6, 1)),
            sg.Checkbox('Check Ranked ONLY', default=False, key="-Ranked-")
        ],
        [
            sg.Text("Limit for Losses:"),
            sg.In(key='-Limit-',size=(8, 1)),
            
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
            sg.In(key='-Region-',size=(6, 1)),
            sg.Checkbox('Check Ranked ONLY', default=False, key="-Ranked-")
            
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
    if(option == 3):
        layout = [
        [
            sg.Text("Summoner Name:"),
            sg.In(key='-Name-',size=(25, 1)) 
        ],
        [
            sg.Text("Region:"),
            sg.In(key='-Region-',size=(6, 1)),
            sg.Checkbox('Check Ranked ONLY', default=False, key="-Ranked-")
        ],
        [
            sg.Text("KDALimit for Games: "),
            sg.In(key='-Limit-',size=(8, 1)),
            sg.Checkbox('Count Assists as kills', default=True, key="-Assists-")
        ],
        [
            sg.Button("Submit",key = "sub"),
            sg.Button("back",key = "back"),
        ],
            ]
    window = sg.Window("League Addiction", layout,finalize=True)
    while True:
        event, values = window.read()
        if event == "back":
            window.close()
            start()
        if event == "cancel" or event == sg.WIN_CLOSED:
            break
        
        if event =="sub":
            window.close()
            if(option ==0): values['-Limit-'] = (int(values['-H-'])*3600 + int(values['-M-'])*60)
            if(option ==3): 
                third(values['-Name-'],values['-Region-'],float(values['-Limit-']),option,values['-Ranked-'],values['-Assists-'])
                break
            third(values['-Name-'],values['-Region-'],int(values['-Limit-']),option,values['-Ranked-'],False)
    window.close()

def start():
    layout = [
    [
        sg.Button("Time Limit",key = "tlim",font=('bold')),
    ],
    [
        sg.Button("Loss Limit",key = "Llim",font=('bold')),
    ],
    [
        sg.Button("Game Limit",key = "Glim",font=('bold')),
    ],
    [
        sg.Button("KDA Limit",key = "kdalim",font=('bold')),
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
        if event =="kdalim":
            window.close()
            first(3)
start()
#timed("nicthequick","NA",40000)


#print("{name} is a level {level} summoner on the {region} server.".format(name=summoner.name,
#                                                                          level=summoner.level,
#                                                                          region=summoner.region))

#match = summoner.match_history[0]
#champion_played = match.participants[summoner].champion
#lengthOfMatch = match.duration
#print(champion_played.name)
#print(dateOfMatch)
