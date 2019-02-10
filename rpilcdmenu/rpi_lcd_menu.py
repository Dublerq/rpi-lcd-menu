from rpilcdmenu.base_menu import BaseMenu
from rpilcdmenu.rpi_lcd_hwd import RpiLCDHwd


class RpiLCDMenu(BaseMenu):
    def __init__(self, pin_rs=26, pin_e=19, pins_db=[13, 6, 5, 21], GPIO=None):
        """
        Initialize menu
        """

        self.lcd = RpiLCDHwd(pin_rs, pin_e, pins_db, GPIO)

        self.lcd.initDisplay()
        self.clearDisplay()

        super(self.__class__, self).__init__()

    def clearDisplay(self):
        """
        Clear LCD Screen
        """
        self.lcd.write4bits(RpiLCDHwd.LCD_CLEARDISPLAY)  # command to clear display
        self.lcd.delayMicroseconds(3000)  # 3000 microsecond sleep, clearing the display takes a long time

        return self

    def message(self, text):
        """ Send long string to LCD. 17th char wraps to second line"""
        i = 0
        lines = 0

        for char in text:
            if char == '\n':
                self.lcd.write4bits(0xC0)  # next line
                i = 0
                lines += 1
            else:
                self.lcd.write4bits(ord(char), True)
                i = i + 1

            if i == 16:
                self.lcd.write4bits(0xC0)  # last char of the line
            elif lines == 2:
                break

        return self

    def displayTestScreen(self):
        """
        Display test screen to see if your LCD screen is wokring
        """
        self.message('Hum. body 36,6\xDFC\nThis is test')

        return self

    def render(self):
        """
        Render menu
        """
        self.clearDisplay()

        if len(self.items) == 0:
            self.message('Menu is empty')
            return self
        elif len(self.items) <= 2:
            options = (self.current_option == 0 and ">" or " ") + self.items[0].text
            if len(self.items) == 2:
                options += "\n" + (self.current_option == 1 and ">" or " ") + self.items[1].text
            print(options)
            self.message(options)
            return self

        options = ">" + self.items[self.current_option].text

        if self.current_option + 1 < len(self.items):
            options += "\n " + self.items[self.current_option + 1].text
        else:
            options += "\n " + self.items[0].text

        self.message(options)

        return self
