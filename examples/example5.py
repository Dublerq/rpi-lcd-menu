#!/usr/bin/python

"""
menu with message view and physical steering
"""

from rpilcdmenu import *
from rpilcdmenu.items import *
import RPi.GPIO as GPIO
import smbus
import time


def main():
    # configure standard button
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    prev_button = 0

    # create menu as in example3
    menu = RpiLCDMenu(26, 19, [13, 6, 5, 21])

    menu.append_item(
        MessageItem('message item',
                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut '
                    'labore et dolore magna aliqua.',
                    menu,
                    True)
    )

    menu.start()

    # configure physical analog joystick via adc converter over i2c
    address = 0x48
    a0 = 0x40  # output of y axis
    bus = smbus.SMBus(1)

    while True:
        bus.write_byte(address, a0)
        y = bus.read_byte(address) * 3.3 / 255

        if y > 2.5:
            menu = menu.processUp()
            time.sleep(0.25)
        elif y < 0.7:
            menu = menu.processDown()
            time.sleep(0.25)

        # physical button
        button = GPIO.input(27)
        if prev_button == 0 and button != 0:
            menu = menu.processEnter()

        prev_button = button

        time.sleep(0.25)


def exit_sub_menu(submenu):
    return submenu.exit()


if __name__ == "__main__":
    main()
