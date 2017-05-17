#!/usr/bin/python

"""
multi level menu
"""

from rpilcdmenu import *
from rpilcdmenu.items import *

def main():
	menu = RpiLCDMenu(26,19,[13, 6, 5, 21])

	function_item1 = FunctionItem("Item 1", fooMethod, [1])
	function_item2 = FunctionItem("Item 2", fooMethod, [2])
	menu.append_item(function_item1)
	menu.append_item(function_item2)

	submenu = RpiLCDSubMenu(menu)
	submenu_item = SubmenuItem("SubMenu (3)", submenu, menu)
	menu.append_item(submenu_item)

	submenu.append_item( FunctionItem("Item 31", fooMethod, [31]))
	submenu.append_item( FunctionItem("Item 32", fooMethod, [32]))
	submenu.append_item( FunctionItem("Item 33", fooMethod, [33]))

	menu.append_item(FunctionItem("Item 4", fooMethod, [4]))

	menu.start()
	menu.debug()
	print "----"
	menu.processEnter()
	menu.processDown()
	menu.processDown()
	menu.processEnter()
	submenu.processDown()
	submenu.processEnter()
	#menu.processUp()
	#menu.processEnter()

def fooMethod(item_index):
	"""
	sample method with a parameter
	"""
	print("item %d pressed" % (item_index))

if __name__ == "__main__":
    main()
