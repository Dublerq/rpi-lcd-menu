
from time import sleep

class RpiLCDMenu(object):

	# commands
	LCD_CLEARDISPLAY        = 0x01
	LCD_RETURNHOME          = 0x02
	LCD_ENTRYMODESET        = 0x04
	LCD_DISPLAYCONTROL      = 0x08
	LCD_CURSORSHIFT         = 0x10
	LCD_FUNCTIONSET         = 0x20
	LCD_SETCGRAMADDR        = 0x40
	LCD_SETDDRAMADDR        = 0x80
 
	# flags for display entry mode
	LCD_ENTRYRIGHT          = 0x00
	LCD_ENTRYLEFT           = 0x02
	LCD_ENTRYSHIFTINCREMENT = 0x01
	LCD_ENTRYSHIFTDECREMENT = 0x00
 
	# flags for display on/off control
	LCD_DISPLAYON           = 0x04
	LCD_DISPLAYOFF          = 0x00
	LCD_CURSORON            = 0x02
	LCD_CURSOROFF           = 0x00
	LCD_BLINKON             = 0x01
	LCD_BLINKOFF            = 0x00
 
	# flags for display/cursor shift
	LCD_DISPLAYMOVE         = 0x08
	LCD_CURSORMOVE          = 0x00
 
	# flags for display/cursor shift
	LCD_DISPLAYMOVE         = 0x08
	LCD_CURSORMOVE          = 0x00
	LCD_MOVERIGHT           = 0x04
	LCD_MOVELEFT            = 0x00
 
	# flags for function set
	LCD_8BITMODE            = 0x10
	LCD_4BITMODE            = 0x00
	LCD_2LINE               = 0x08
	LCD_1LINE               = 0x00
	LCD_5x10DOTS            = 0x04
	LCD_5x8DOTS             = 0x00
	
	def __init__(self, pin_rs=26, pin_e=19, pins_db=[13, 6, 5, 21], GPIO=None):
		"""
		description here
		"""
		if not GPIO:
 			import RPi.GPIO as GPIO
 			GPIO.setwarnings(False)
 		self.GPIO = GPIO
		self.pin_rs = pin_rs
		self.pin_e = pin_e
		self.pins_db = pins_db

		self.GPIO.setmode(GPIO.BCM)
		self.GPIO.setup(self.pin_e, GPIO.OUT)
		self.GPIO.setup(self.pin_rs, GPIO.OUT)
 
		for pin in self.pins_db:
			self.GPIO.setup(pin, GPIO.OUT)
		self.__initDisplay()
		self.clearDisplay()

	def __initDisplay(self):
		self.__write4bits(0x33)  # initialization
		self.__write4bits(0x32)  # initialization
		self.__write4bits(0x28)  # 2 line 5x7 matrix
		self.__write4bits(0x0C)  # turn cursor off 0x0E to enable cursor
		self.__write4bits(0x06)  # shift cursor right
 
		self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF
 
		self.displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS
		self.displayfunction |= self.LCD_2LINE
 
		# Initialize to default text direction (for romance languages)
		self.displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
		self.__write4bits(self.LCD_ENTRYMODESET | self.displaymode)  # set the entry mode
	
	def __write4bits(self, bits, char_mode=False):
		""" Send command to LCD """
		self.__delayMicroseconds(1000)  # 1000 microsecond sleep
		bits = bin(bits)[2:].zfill(8)
		self.GPIO.output(self.pin_rs, char_mode)
		for pin in self.pins_db:
			self.GPIO.output(pin, False)
		for i in range(4):
			if bits[i] == "1":
				self.GPIO.output(self.pins_db[::-1][i], True)
		self.__pulseEnable()
		for pin in self.pins_db:
			self.GPIO.output(pin, False)
		for i in range(4, 8):
			if bits[i] == "1":
				self.GPIO.output(self.pins_db[::-1][i-4], True)
		self.__pulseEnable()

	def __delayMicroseconds(self, microseconds):
        	seconds = microseconds / float(1000000)  # divide microseconds by 1 million for seconds
        	sleep(seconds)

	def __pulseEnable(self):
		self.GPIO.output(self.pin_e, False)
		self.__delayMicroseconds(1)	   # 1 microsecond pause - enable pulse must be > 450ns
		self.GPIO.output(self.pin_e, True)
		self.__delayMicroseconds(1)	   # 1 microsecond pause - enable pulse must be > 450ns
		self.GPIO.output(self.pin_e, False)
		self.__delayMicroseconds(1)	   # commands need > 37us to settle

	def clearDisplay(self):	
		"""
		Clear LCD Screen
		"""
		self.__write4bits(self.LCD_CLEARDISPLAY)  # command to clear display
		self.__delayMicroseconds(3000)  # 3000 microsecond sleep, clearing the display takes a long time

	def message(self, text):
		""" Send string to LCD. Newline wraps to second line"""
		for char in text:
			if char == '\n':
				self.__write4bits(0xC0)  # next line
			else:
				self.__write4bits(ord(char), True)
	
	def longMessage(self, text):
		""" Send long string to LCD. 17 char wraps to second line"""
		i = 0
		for char in text:
			self.__write4bits(ord(char), True)
			i = i+1
			if i == 16:
				self.__write4bits(0xC0) 

	def displayTestScreen(self):
		"""
		Display test screen to see if your LCD screen is wokring
		"""
		self.message('Hum. body 36,6\xDFC\nThis is test')
