from .menu_item import MenuItem
from rpilcdmenu.views import MessageView


class MessageItem(MenuItem):
    """
    A menu item to open a submenu
    """

    def __init__(self, text, message, menu, scrollable=False):
        """
        :ivar str text: Message to be shown on display
        :ivar RpiLCDMenu menu: The menu which this item belongs to
        :ivar bool scrollable: is scrolling allowed
        """
        super(MessageItem, self).__init__(text, menu)

        self.view = MessageView(menu, message, scrollable)

        if menu:
            self.view.parent = menu

    def action(self):
        """
        On MessageItem click
        """
        return self.view.start()
