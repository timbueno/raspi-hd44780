#!/usr/bin/python

import hd44780

from subprocess import *

def get_ip():
	cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"

	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate(0)
	return output

if __name__ == '__main__':

    lcd = hd44780.HD44780()

    ip = get_ip()
    ip = ip[0].rstrip()


    message = 'IP:%s' % ip
    lcd.message(message)
    #message = '\nSSH is Ready...'
    #lcd.message(message)