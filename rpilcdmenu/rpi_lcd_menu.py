import queue
import threading
from time import sleep

from rpilcdmenu.base_menu import BaseMenu
from rpilcdmenu.rpi_lcd_hwd import RpiLCDHwd


class RpiLCDMenu(BaseMenu):
    def __init__(self, pin_rs=26, pin_e=19, pins_db=[13, 6, 5, 21], GPIO=None, scrolling_menu=False):
        """
        Initialize menu
        """
        self.lcd_queue = queue.Queue(maxsize=0)
        self.scrolling_menu = scrolling_menu

        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db
        self.GPIO = GPIO

        # start the worker thread
        threading.Thread(target=self.lcd_queue_processor).start()

        super(self.__class__, self).__init__()

    def clearDisplay(self):
        """
        Clear LCD Screen
        """
        self.lcd.write4bits(RpiLCDHwd.LCD_CLEARDISPLAY)  # command to clear display
        self.lcd.delayMicroseconds(3000)  # 3000 microsecond sleep, clearing the display takes a long time

        return self

    def lcd_render(self, render_text):
        i = 0
        lines = 0

        # return home rather than clear the display
        self.lcd.write4bits(RpiLCDHwd.LCD_RETURNHOME)

        for char in render_text:
            if char == '\n':
                self.lcd.write4bits(0xC0)  # next line
                i = 0
                lines += 1
            else:
                self.lcd.write4bits(ord(char), True)
                i = i + 1

            if i == 16:
                self.lcd.write4bits(0xC0)  # last char of the line

    def message(self, text, autoscroll=False):
        """ Send long string to LCD. Long single line messages are split and scrolled if autoscroll is set.
        else the are split and cropped."""

        # clear the existing lcd queue
        with self.lcd_queue.mutex:
            self.lcd_queue.queue.clear()

        try:
            splitlines = text.split('\n')

            # process a single line
            if len(splitlines) < 2:
                line1 = splitlines[0]

                # if there's one line and its longer than 16 characters, split it onto line 2
                len1 = len(line1)
                if len1 > 16:
                    #  // will return an integer
                    half = (len1 // 2)
                    # find the next space after half the string and split at the character after it
                    split = line1.find(' ', half) + 1
                    # split it in half
                    line2 = line1[split:]
                    line1 = line1[0:split]
                    # pad out to length of line 1
                    line2 = line2.ljust(len(line1), ' ')
                else:
                    #  line 2 is nothing if line1 is not more than 16 characters
                    line2 = ''

                # recalculate lengths for srcoller
                len1 = len(line1)
                len2 = len(line2)
                final_text = ("%s\n%s" % (line1, line2))

            # process 2 lines
            elif len(splitlines) == 2:
                # set lengths for scroller but other wise leave the text
                len1 = len(splitlines[0])
                len2 = len(splitlines[1])
                # pad out short lines
                line1 = "{:<16}".format(splitlines[0])
                line2 = "{:<16}".format(splitlines[1])
                final_text = ("%s\n%s" % (line1, line2))

            else:
                # TODO process more than 2 lines. Currently they just get cropped.
                len1 = len(splitlines[0])
                len2 = len(splitlines[1])
                # pad out short lines
                line1 = "{:<16}".format(splitlines[0])
                line2 = "{:<16}".format(splitlines[1])
                final_text = ("%s\n%s" % (line1, line2))

            # scroll messages
            if autoscroll == True:
                # add one to the longest length so it scrolls off screen
                if len1 < len2:
                    text_length = len2
                else:
                    text_length = len1

                # render for 16x2
                fixed_text = self.render_16x2(final_text)
                # render the output
                self.lcd_queue.put((self.lcd_render, fixed_text))

                # only scroll if needed
                if text_length > 16:

                    # add one to the longest length so it scrolls off screen
                    text_length = text_length + 1

                    # show the text for one second
                    sleep(1)

                    # scroll the message right to left
                    # start 1 character in as we've already rendered the first character
                    for index in range(1, text_length):
                        # render at 16x2
                        fixed_text = self.render_16x2(final_text, index)

                        # render the output
                        self.lcd_queue.put((self.lcd_render, fixed_text))

                    # scroll the rest of the way
                    for index in range(0, 16):
                        # render at 16x2
                        fixed_text = self.render_16x2_reverse(final_text, index)

                        # render the output
                        self.lcd_queue.put((self.lcd_render, fixed_text))

                    # render for 16x2
                    fixed_text = self.render_16x2(final_text)

                    # render the output
                    self.lcd_queue.put((self.lcd_render, fixed_text))

                return self

            else:
                # just show the text if theres no autoscroll
                fixed_text = self.render_16x2(final_text)

                # render the output
                self.lcd_queue.put((self.lcd_render, fixed_text))

                return self


        except Exception as e:
            print("Autoscroll error: %s" % e)

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
        if len(self.items) == 0:
            self.message('Menu is empty')
            return self
        elif len(self.items) <= 2:
            options = (self.current_option == 0 and ">" or " ") + self.items[0].text
            if len(self.items) == 2:
                options += "\n" + (self.current_option == 1 and ">" or " ") + self.items[1].text
            # print(options)
            if self.scrolling_menu == True:
                self.message(options, autoscroll=True)
            else:
                self.message(options)
            return self

        options = ">" + self.items[self.current_option].text

        if self.current_option + 1 < len(self.items):
            options += "\n " + self.items[self.current_option + 1].text
        else:
            options += "\n " + self.items[0].text

        if self.scrolling_menu == True:
            self.message(options, autoscroll=True)
        else:
            self.message(options)

        return self

    def render_16x2(self, text, index=0):

        # incoming text will already have been cleaned up and split with a line break
        # by the message function
        try:
            # render incoming text as 16x2 by taking the starting index and adding 16
            # for each line
            lines = text.split('\n')
            line1 = lines[0]
            line2 = lines[1]

            # render from index to 16 characters in
            last_char = index + 16

            # # pad out the text if its less than 16 characters  long
            line1_vfd = "{:<16}".format(line1[index:last_char])
            line2_vfd = "{:<16}".format(line2[index:last_char])

            return ("%s\n%s" % (line1_vfd, line2_vfd))


        except Exception as e:
            print("Render error: %s" % e)

    def render_16x2_reverse(self, text, index=0):

        # incoming text will already have been cleaned up and split with a line break
        # by the message function
        try:
            # render incoming text as 16x2 but right justified. ie add padding to the left.
            # only useful for the reverse scroll
            lines = text.split('\n')
            line1 = lines[0]
            line2 = lines[1]
            # pad out the text if its less than 16 characters long from the left
            line1_vfd = "{:>16}".format(line1[0:index])
            line2_vfd = "{:>16}".format(line2[0:index])

            return ("%s\n%s" % (line1_vfd, line2_vfd))


        except Exception as e:
            print("Render error: %s" % e)

    def lcd_queue_processor(self):

        self.lcd = RpiLCDHwd(self.pin_rs, self.pin_e, self.pins_db, self.GPIO)
        self.lcd.initDisplay()

        # clear it once in case of existing corruption
        self.clearDisplay()

        # process the queue
        while True:
            items = self.lcd_queue.get()
            func = items[0]
            args = items[1:]
            func(*args)

