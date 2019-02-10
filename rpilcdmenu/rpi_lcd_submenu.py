from rpilcdmenu import RpiLCDMenu


class RpiLCDSubMenu(RpiLCDMenu):
    def __init__(self, base_menu):
        """
        Initialize SubMenu
        """
        self.lcd = base_menu.lcd

        super((self.__class__.__bases__)[0], self).__init__()
