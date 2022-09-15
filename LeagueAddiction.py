import random
import arrow
import config
import cassiopeia as cass
limit = 1
cass.set_riot_api_key(config.api_key)  # This overrides the value set in your configuration/settings.
summoner = cass.get_summoner(name="nicthequick", region="NA")

def dateCheck(x,y):
    if(x.year==y.year and x.month==y.month and x.day==y.day): return True
    else: return False
def timeAdd():
    for z in range(20):
        print(summoner.match_history[z].duration)


print("{name} is a level {level} summoner on the {region} server.".format(name=summoner.name,
                                                                          level=summoner.level,
                                                                          region=summoner.region))

match = summoner.match_history[0]
champion_played = match.participants[summoner].champion
lengthOfMatch = match.duration
dateOfMatch = match.start.to('US/Pacific')
print(champion_played.name)
print(dateOfMatch)
#.format('YYYY-MM-DD')
utc = arrow.utcnow()
now = utc.to('US/Pacific')
print(match.duration)
print(now)
print(dateCheck(dateOfMatch,now))
timeAdd()
