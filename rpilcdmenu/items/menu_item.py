class MenuItem(object):
    """
    A generic menu item
    """

    def __init__(self, text, menu=None):
        """
        :ivar str text: The text shown for this menu item
        :ivar RpiLCDMenu menu: The menu which this item belongs to
        """

        if len(text) > 15 or len(text) == 0:
            # removed text length limit for menus as theres a scrolling option
            pass
            # raise NameError('MenuTextTooLong');
        self.text = text
        self.menu = menu

    def __str__(self):
        return "%s" % self.text

    def show(self, index):
        """
        How this item should be displayed in the menu. Can be overridden, but should keep the same pattern
        Default is:
            1 - Item 1
            2 - Another Item
        :param int index: The index of the item in the items list of the menu
        :return: The representation of the item to be shown in a menu
        :rtype: str
        """
        return "%d - %s" % (index + 1, self.text)

    def set_up(self):
        """
        Override to add any setup actions necessary for the item
        """
        pass

    def action(self):
        """
        Override to carry out the main action for this item.
        """
        pass

    def clean_up(self):
        """
        Override to add any cleanup actions necessary for the item
        """
        pass

    def get_return(self):
        """
        Override to change what the item returns.
        Otherwise just returns the same value the last selected item did.
        """
        return self.menu is not None and self.menu.get_return() or None
