#!/usr/bin/python

import hd44780

from subprocess import *
from time import sleep

def get_ip():
    cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"

    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate(0)
    return output

def blinkMessage(tList, delay, lcd):
    # tList is a list containing tuples
    # consisting of both lines on the display
    if tList != 1:
        while True:
            for screen in tList:
                for line in screen:
                    lcd.message(line)
                    if line[1] != line:
                        lcd.cmd(0xC0)
                sleep(delay)
                lcd.clear()
    else:
        lcd.message(tList[0][0])
        lcd.cmd(0xC0)
        lcd.message(tList[0][1])

if __name__ == '__main__':

    lcd = hd44780.HD44780()

    ip = get_ip()
    ip = ip[0].rstrip()

    tList = [('Only Page', 'No Blinking')]
    #tList = [('First Line','Second Line'),('Third Line','Fourth Line'),('Fifth Line', 'Sixth Line')]

    blinkMessage(tList, 2, lcd)

    # message = 'IP:%s' % ip
    # lcd.message(message)
    # lcd.cmd(0xC0)
    # message = 'SSH is Ready...'
    # lcd.message(message)