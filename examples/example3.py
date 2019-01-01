#!/usr/bin/python

"""
multi level menu
"""

from rpilcdmenu import *
from rpilcdmenu.items import *

def main():
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
	menu.debug()
	print "----"
	#press first menu item and scroll down to third one
	menu.processEnter().processDown().processDown()
	#enter submenu, press Item 32, press Back button
	menu.processEnter().processDown().processEnter().processDown().processEnter()
	#press item4 back in the menu
	menu.processDown().processEnter()

def fooFunction(item_index):
	"""
	sample method with a parameter
	"""
	print("item %d pressed" % (item_index))

def exitSubMenu(submenu):
	return submenu.exit();

if __name__ == "__main__":
	main()
