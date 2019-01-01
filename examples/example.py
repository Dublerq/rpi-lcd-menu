#!/usr/bin/python

"""
test if lcd display is connected to raspberry on default pins 
"""

from rpilcdmenu import *

def main():
	menu = RpiLCDMenu(26,19,[13, 6, 5, 21])
	menu.displayTestScreen()

if __name__ == "__main__":
	main()
