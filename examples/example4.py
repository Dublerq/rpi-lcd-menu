#!/usr/bin/python

"""
multi level menu with physical steering
"""

from rpilcdmenu import *
from rpilcdmenu.items import *
import RPi.GPIO as GPIO
import smbus
import time

def main():
	#configure standard button
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	prev_button = 0

	#create menu as in example3
	menu = RpiLCDMenu(26,19,[13, 6, 5, 21])

	function_item1 = FunctionItem("Item 1", fooFunction, [1])
	function_item2 = FunctionItem("Item 2", fooFunction, [2])
	menu.append_item(function_item1).append_item(function_item2)

	submenu = RpiLCDSubMenu(menu)
	submenu_item = SubmenuItem("SubMenu (3)", submenu, menu)
	menu.append_item(submenu_item)

	submenu.append_item( FunctionItem("Item 31", fooFunction, [31])).append_item( FunctionItem("Item 32", fooFunction, [32]))
	submenu.append_item( FunctionItem("Back", exitSubMenu, [submenu]))

	menu.append_item(FunctionItem("Item 4", fooFunction, [4]))

	menu.start()

	#configure physical analog joystick via adc converter over i2c
	address = 0x48
	A0 = 0x40
	A1 = 0x41
	A2 = 0x42
	A3 = 0x43
	bus = smbus.SMBus(1)
	while True:
		bus.write_byte(address,A0)
		x = bus.read_byte(address)*3.3/255
		bus.write_byte(address,A1)
		y = bus.read_byte(address)*3.3/255
		if (y > 2.5):
			menu = menu.processUp()
			time.sleep(0.5)
		elif (y < 0.7):
			menu = menu.processDown()
			time.sleep(0.5)

		#physical button
		button = GPIO.input(27)
		if (prev_button == 0 and button != 0):
			menu = menu.processEnter()
		prev_button = button

        time.sleep(0.25)

def fooFunction(item_index):
	"""
	sample method with a parameter
	"""
	print("item %d pressed" % (item_index))

def exitSubMenu(submenu):
	return submenu.exit()

if __name__ == "__main__":
    main()
