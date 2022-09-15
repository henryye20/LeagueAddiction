import random
import datetime
import config
import cassiopeia as cass


<<<<<<< HEAD
def dateCheck():
    print('hi')
cass.set_riot_api_key(config.api_key)  # This overrides the value set in your configuration/settings.
=======

cass.set_riot_api_key("")  # This overrides the value set in your configuration/settings.
>>>>>>> c4b938f4e3deef0371c3e8b31cb66a0c5a74def3

summoner = cass.get_summoner(name="pandacreeper", region="NA")
print("{name} is a level {level} summoner on the {region} server.".format(name=summoner.name,
                                                                          level=summoner.level,
                                                                          region=summoner.region))
person = summoner(name="pandacreeper", region="NA")
match = person.match_history[0]
champion_played = match.participants[person].champion
lengthOfMatch = match.duration
dateOfMatch = match.start
print(champion_played.name)
print(dateOfMatch.format('YYYY-MM-DD'))
dateToday = datetime.date.today()
print(match.type())
print(dateToday.type())
