from rpilcdmenu.rpi_lcd_submenu import RpiLCDSubMenu
from rpilcdmenu.helpers.text_helper import get_scrolled_text, get_text_lines


class MessageView(RpiLCDSubMenu):
    def __init__(self, base_menu, text, scrollable=False):
        """
        Initialize MessageView
        :ivar RpiLCDMenu base_menu: The menu which this item belongs to
        :ivar str text: Message to be shown on display
        :ivar bool scrollable: is scrolling allowed
        """

        self.scrollable = scrollable
        self.line_index = 0
        self.text_lines = 0
        self.text = ''

        self.setText(text)

        super(MessageView, self).__init__(base_menu)

    def render(self):
        """
        Render menu
        """
        self.clearDisplay()

        if self.scrollable:
            self.message(get_scrolled_text(self.text, self.line_index))
        else:
            self.message(self.text)

        return self

    def processUp(self):
        if self.line_index > 0 and self.scrollable:
            self.line_index -= 1
            self.render()

        return self

    def processDown(self):
        if self.line_index < self.text_lines - 1 and self.scrollable:
            self.line_index += 1
            self.render()

        return self

    def processEnter(self):
        return self.exit()

    def setText(self, text):
        self.text = text
        self.text_lines = get_text_lines(text)
