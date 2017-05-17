class BasicMenu(object):
    """
    A generic menu
    """
    def __init__(self, parent=None):
        """
        Initialzie basic menu
        """
        self.items = list()
        self.parent = parent

    def start(self):
        """
        Start and render menu
        """
        self.current_option = 0
        self.selected_option = -1
        self.clearDisplay()
        self.render()

    def debug(self, level=1):
        """
        print menu items in console
        """
        for item in self.items:
            if hasattr(item,'submenu') and isinstance(item.submenu,BasicMenu):
                print "|" + "--" * (level+1) + "[" + "%s" % (item.__str__())  + "]"
                item.submenu.debug(level+1)
            else:
                print "|" + "--" * level + ">" + "%s" % (item.__str__())

    def append_item(self, item):
        """
        Add an item to the end of the menu
        :param MenuItem item: The item to be added
        """
        item.menu = self
        self.items.append(item)

    def render(self):
        """
        Render menu
        """
        pass

    def clearDisplay(self):
        """
        Clear the screen
        """
        pass

    def processUp(self):
        """
        User triggered up event
        """
        if self.current_option == 0:
            self.current_option = len(self.items) - 1
        else:
            self.current_option -= 1
        self.render()

    def processDown(self):
        """
        User triggered down event
        """
        if self.current_option == len(self.items) - 1:
            self.current_option = 0
        else:
            self.current_option += 1
        self.render()

    def processEnter(self):
        """
        User triggered enter event
        """
        self.items[self.current_option].action()
