#!/usr/bin/python

#
# USEFUL COMMANDS
#
# self.cmd(command)
#
#    0x0C    Turns ON the LCD, no cursor
#    0x08    Turns OFF the LCD
#    0x0E    Turns on the LCD with a SOLD cursor
#    0x0F    Turns on the LCD with a BLINK cursor
# 
# Positions within line can be set
# by adding an offset
# example: 0x82 moves the cursor to
# the third position on the first line
#
#    0x80    Moves cursor to LINE 1
#    0xC0    Moves cursor to LINE 2
#    0x94    Moves cursor to LINE 3
#    0xD4    Moves cursor to LINE 4
#
#
# Reference:
#        http://joshuagalloway.com/lcd.html
#        http://en.wikipedia.org/wiki/Hitachi_HD44780_LCD_controller
#        http://letsmakerobots.com/node/4240


import RPi.GPIO as GPIO
from time import sleep

#
# 4 Bit Mode 
#
class HD44780:

    def __init__(self, pin_rs=24, pin_e=23, pins_db=[4, 17, 21, 22]):

        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db

        # Set pinmodes (All output)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)
        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT)

        # Initialize the LCD
        self.clear()
        sleep(0.002)

    #
    # Initialize and clear lcd
    #
    def clear(self):
        """ Blank / Reset LCD """

        self.cmd(0x33) # Initialize lcd 
        self.cmd(0x32) # Four-bit mode
        self.cmd(0x28) # Set interface, 2 Lines
        self.cmd(0x0C) # Turn on Display
        self.cmd(0x06) # Set cursor move direction right
        self.cmd(0x01) # Clear and home display
        sleep(0.002)

    #
    # 4-Bit Write Sequence
    #
    def cmd(self, bits, char_mode=False):
        """ Send command to LCD """

        sleep(0.001)
        bits=bin(bits)[2:].zfill(8)

        # Set rs pin: command mode (0) or data mode (1)
        GPIO.output(self.pin_rs, char_mode)

        # Set data pins low (reset)
        for pin in self.pins_db:
            GPIO.output(pin, False)

        # Send the first four bits [1101]0110
        for i in range(4):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i], True)

        # Toggle EN pin to get
        # ready for next nibble
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        # Set data pins low (reset)
        for pin in self.pins_db:
            GPIO.output(pin, False)

        # Send the last four bits 1101[0110]
        for i in range(4,8):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i-4], True)

        # Toggle EN pin to finish writing
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

    #
    # Write string to LCD
    #
    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""

        for char in text:
            if char == '\n':
                self.cmd(0xC0) # next line
            else:
                self.cmd(ord(char),True)

if __name__ == '__main__':

    lcd = HD44780()

    lcd.message("I'm Raspberry Pi\n  Take a byte!")
