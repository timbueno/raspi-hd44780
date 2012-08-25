#!/usr/bin/python

import hd44780

from subprocess import *
#from time import sleep


class simplelcd(hd44780.HD44780):

    def __init__(self):
        super(simplelcd, self).__init__()

    def get_ip(self):
        cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"

        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate(0)
        return output

    def displayIP(self):
        # Get IP
        ip = self.get_ip()
        #



    def blinkMessage(self, tList, delay):
        # tList is a list containing tuples
        # consisting of both lines on the display
        if len(tList) != 1:
            while True:
                for screen in tList:
                    for line in screen:
                        self.message(line)
                        if line[1] != line:
                            self.cmd(0xC0)
                    sleep(delay)
                    self.clear()
        else:
            self.message(tList[0][0])
            self.cmd(0xC0)
            self.message(tList[0][1])

if __name__ == '__main__':

    lcd = simplelcd()

    #ip = get_ip()
    #ip = ip[0].rstrip()

    tList = [(ip, 'No Blinking')]
    #tList = [('First Line','Second Line'),('Third Line','Fourth Line'),('Fifth Line', 'Sixth Line')]

    lcd.blinkMessage(tList, 2)

    # message = 'IP:%s' % ip
    # lcd.message(message)
    # lcd.cmd(0xC0)
    # message = 'SSH is Ready...'
    # lcd.message(message)