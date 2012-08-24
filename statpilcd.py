#!/usr/bin/python

import hd44780

from subprocess import *

def get_ip():
	cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"

	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate(0)
	return output