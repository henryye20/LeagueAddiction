import PySimpleGUI as sg
from time import sleep

sg.theme('Dark Blue 3')
sg.one_line_progress_meter(title="test", current_value=0, max_value=200, no_button=False)
key='OK for 1 meter'
meter = sg.QuickMeter.active_meters[key]
meter.window.DisableClose = False

for i in range(1, 200):
    sleep(0.1)
    if not sg.one_line_progress_meter(title="test", current_value=i, max_value=200, no_button=False):
        print('returned false')
        break