from rpilcdmenu import RpiLCDMenu


class RpiLCDSubMenu(RpiLCDMenu):
    def __init__(self, base_menu):
        """
        Initialize SubMenu
        """
        self.lcd = base_menu.lcd
        self.scrolling_menu = base_menu.scrolling_menu
        self.lcd_queue = base_menu.lcd_queue

        super(RpiLCDMenu, self).__init__(base_menu)
