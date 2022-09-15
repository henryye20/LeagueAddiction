import subprocess

from time import sleep
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
def leaguekill():
        subprocess.call('taskkill /F /IM LeagueClientUx.exe', startupinfo=si)
#leaguekill()