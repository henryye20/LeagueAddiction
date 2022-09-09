import random
import datetime
import cassiopeia as cass



cass.set_riot_api_key("RGAPI-7a90ab5a-fdeb-47d5-ab09-c69fee9e3bc8")  # This overrides the value set in your configuration/settings.

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
print(dateToday)
