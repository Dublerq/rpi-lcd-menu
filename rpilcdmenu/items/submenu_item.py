from .menu_item import MenuItem

class SubmenuItem(MenuItem):
    """
    A menu item to open a submenu
    """

    def __init__(self, text, submenu, menu=None):
        """
        :ivar CursesMenu self.submenu: The submenu to be opened when this item is selected
        """
        super(SubmenuItem, self).__init__(text=text, menu=menu)

        self.submenu = submenu
        if menu:
            self.submenu.parent = menu

    def set_menu(self, menu):
        """
        Sets the menu of this item.
        Should be used instead of directly accessing the menu attribute for this class.
        :param CursesMenu menu: the menu
        """
        self.menu = menu
        self.submenu.parent = menu

    def set_up(self):
        """
        This class overrides this method
        """
        self.menu.pause()
        self.menu.clear_screen()

    def action(self):
        """
        This class overrides this method
        """
        print "starting submenu"
        return self.submenu.start()

    def clean_up(self):
        """
        This class overrides this method
        """
        self.submenu.join()
        self.menu.clear_screen()
        self.menu.resume()

    def get_return(self):
        """
        :return: The returned value in the submenu
        """
        return self.submenu.returned_value
