#!/usr/bin/python

"""
single level menu
"""

from rpilcdmenu import *
from rpilcdmenu.items import *

def main():
	menu = RpiLCDMenu(26,19,[13, 6, 5, 21])
	function_item1 = FunctionItem("Item 1", fooMethod, [1])
	function_item2 = FunctionItem("Item 2", fooMethod, [2])
	function_item3 = FunctionItem("Item 3", fooMethod, [3])
	function_item4 = FunctionItem("Item 4", fooMethod, [4])
	menu.append_item(function_item1)
	menu.append_item(function_item2)
	menu.append_item(function_item3)
	menu.append_item(function_item4)
	menu.start()
	menu.processEnter()
	menu.processDown()
	menu.processDown()
	menu.processEnter()
	menu.processUp()
	menu.processEnter()

def fooMethod(item_index):
	"""
	sample method with a parameter
	"""
	print("item %d pressed" % (item_index))

if __name__ == "__main__":
    main()
