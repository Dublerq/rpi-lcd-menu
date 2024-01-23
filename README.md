# RPI LCD Menu - creating menu on 16x2 LCD with Raspberry PI
[![Build Status](https://travis-ci.org/Dublerq/rpi-lcd-menu.svg?branch=master)](https://travis-ci.org/Dublerq/rpi-lcd-menu)
[![codecov](https://codecov.io/gh/Dublerq/rpi-lcd-menu/branch/master/graph/badge.svg)](https://codecov.io/gh/Dublerq/rpi-lcd-menu)

RPI LCD Menu is a python library for creating multi level menus displayed on 16x2 LCD screens (i.e. hd44780).
Navigation can be easily implemented for any user input (buttons, joysticks, switches, detectors etc.).

This fork implements horizontal scrolling for messages and menus, and a queueing system to avoid corruption.
I'm utilising it as a menu and track display system for a retro hifi project. 

Tested on python 3.7.3+.

# Demo
![Example in-use photo](/doc/rpi-example.jpg)

Configuration used in examples:

![Configuration used in examples](/doc/configuration.png)

# Code examples

Sample snippets are stored in examples directory. Their content is as follows:
* example.py - init screen and display test message to find out if everything is wired correctly
* example2.py - create 1-level menu and test software navigation through entries
* example3.py - create 2-level menu (menu with submenus) and test software navigation through entries
* example4.py - example3.py with physical navigation using analog joystick and buttons (configuration as on image above)
* example5.py - scrollable message view with physical navigation as in example4
