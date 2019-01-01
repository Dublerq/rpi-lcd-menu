import mock
from rpilcdmenu.items.submenu_item import SubmenuItem


def test_submenuitem_action_starts_submenu():
    submenu_mock = mock.Mock()
    submenu_mock.start = mock.Mock()
    submenu_item = SubmenuItem('submenu', submenu_mock, mock.Mock())
    submenu_item.action()
    submenu_mock.start.assert_called_once()
