#!/usr/bin/python

from hd44780 import HD44780

from subprocess import *
from time import sleep


class Simplelcd(HD44780):

    def __init__(self):
        super(Simplelcd, self).__init__()

    def get_ip(self):
        cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"

        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate(0)
        output = output[0].rstrip()
        return output

    def displayIP(self):
        # Get IP
        ip = self.get_ip()
        # Send to screen
        ip = 'IP:%s' % ip
        sTuple = (ip, 'It worked!')


    def blinkMessage(self, tList, delay):
        # tList is a list containing tuples
        # consisting of both lines on the display
        self.clear()
        if len(tList) != 1:
            while True:
                for screen in tList:
                    self.message(screen[0])
                    self.cmd(0xC0)
                    self.message(screen[1])    
                    sleep(delay)
                    self.clear()
        else:
            self.message(tList[0][0])
            self.cmd(0xC0)
            self.message(tList[0][1])

    def screen(self, sTuple):
        for char in sTuple[0]:
            self.cmd(ord(char),True)
        self.cmd(0xC0)
        for char in sTuple[1]:
            self.cmd(ord(char),True)

if __name__ == '__main__':

    lcd = Simplelcd()

    tList = [('Cool', 'No Blinking'),('just', 'kidding')]
    #tList = [('First Line','Second Line'),('Third Line','Fourth Line'),('Fifth Line', 'Sixth Line')]

    lcd.blinkMessage(tList, 2)

    # message = 'IP:%s' % ip
    # lcd.message(message)
    # lcd.cmd(0xC0)
    # message = 'SSH is Ready...'
    # lcd.message(message)