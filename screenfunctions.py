from subprocess import *


class SysStatScreen(object):

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
        return sTuple