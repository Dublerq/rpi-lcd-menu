from .menu_item import MenuItem

class SubmenuItem(MenuItem):
    """
    A menu item to open a submenu
    """

    def __init__(self, text, submenu, menu=None):
        """
        :ivar BasicMenu self.submenu: The submenu to be opened when this item is selected
        """
        super(SubmenuItem, self).__init__(text=text, menu=menu)

        self.submenu = submenu
        if menu:
            self.submenu.parent = menu

    def action(self):
        """
        On Subitem click
        """
        return self.submenu.start()
