#!/usr/bin/python

from rpilcdmenu import *

def main():
	menu = RpiLCDMenu(26,19,[13, 6, 5, 21])
	menu.displayTestScreen()

if __name__ == "__main__":
    main()
