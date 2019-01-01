from rpilcdmenu import RpiLCDMenu


class RpiLCDSubMenu(RpiLCDMenu):
    def __init__(self, base_menu):
        """
        Initialize SubMenu
        """
        self.GPIO = base_menu.GPIO
        self.pin_rs = base_menu.pin_rs
        self.pin_e = base_menu.pin_e
        self.pins_db = base_menu.pins_db

        self.displaycontrol = base_menu.displaycontrol
        self.displayfunction = base_menu.displayfunction
        self.displaymode = base_menu.displaymode
        super((self.__class__.__bases__)[0], self).__init__()
