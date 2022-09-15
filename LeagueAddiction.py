import random
import arrow
import config
import cassiopeia as cass
from time import sleep
import kill
limit = -1
cass.set_riot_api_key(config.api_key)  # This overrides the value set in your configuration/settings.
summoner = cass.get_summoner(name="nicthequick", region="NA")

utc = arrow.utcnow()
now = utc.to('US/Pacific')

#checks if the dates of 2 matches are the same
def dateCheck(x,y):
    if(x.year==y.year and x.month==y.month and x.day==y.day): return True
    else: return False

#adds all the time of matches played today
def timeAddT():
    total = 0
    f = 0.0
    for z in range(11):
        match = summoner.match_history[z]
        dateOfMatch = match.start.to('US/Pacific')

        if not (dateCheck(now,dateOfMatch)):
            continue

        f += match.duration.seconds
    return f

Flag = False
Flag2 = False
First = True
while(True):
    t = timeAddT()
    p = 0
    if(Flag):
        sleep(3600)
    
    while(t>limit):
        kill.leaguekill()
        sleep(2)
        p += 2
        if(p==3600):
            Flag2 = True
            break
    if(Flag2):
        Flag = False
        Flag2 = False
        continue
    if(First):
        sleep(3600)
        First = False
    Flag = True

#print("{name} is a level {level} summoner on the {region} server.".format(name=summoner.name,
#                                                                          level=summoner.level,
#                                                                          region=summoner.region))

#match = summoner.match_history[0]
#champion_played = match.participants[summoner].champion
#lengthOfMatch = match.duration
#print(champion_played.name)
#print(dateOfMatch)
