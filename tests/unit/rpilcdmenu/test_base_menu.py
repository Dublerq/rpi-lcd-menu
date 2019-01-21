import mock
from rpilcdmenu.base_menu import BaseMenu

def test_basemenu_can_be_initialized_entered_and_exited():
    base_menu = BaseMenu(mock.Mock())
    base_menu.start()
    base_menu.exit()


def test_basemenu_can_append_scroll_and_select_menuitems():
    base_menu = BaseMenu()
    base_menu.start()

    menuitem_mock = mock.Mock()
    target_menuitem_mock = mock.Mock()
    target_menuitem_mock.action = mock.Mock()

    base_menu.append_item(menuitem_mock)
    base_menu.append_item(target_menuitem_mock)

    base_menu.processDown()
    base_menu.processDown()
    base_menu.processUp()
    base_menu.processUp()
    base_menu.processDown()

    base_menu.processEnter()

    target_menuitem_mock.action.assert_called_once()


def test_basemenu_process_process_enter_renders_submenu_when_submenu_item_selected():
    base_menu = BaseMenu()
    base_menu.start()

    submenu_mock = mock.Mock()
    submenu_mock.__class__ = BaseMenu

    menuitem_mock = mock.Mock()
    menuitem_mock.action = mock.Mock()
    menuitem_mock.action.return_value = submenu_mock

    base_menu.append_item(menuitem_mock)

    assert submenu_mock == base_menu.processEnter()


def test_basemenu_clearDisplay_exists():
    base_menu = BaseMenu(mock.Mock())
    base_menu.clearDisplay()


def test_basemenu_debug_returns_subitem_debug_info():
    base_menu = BaseMenu()
    base_menu.start()

    menuitem_mock = mock.Mock()
    submenuitem_mock = mock.Mock()
    submenuitem_mock.submenu = mock.Mock()
    submenuitem_mock.submenu.debug = mock.Mock()
    submenuitem_mock.submenu.__class__ = BaseMenu
    base_menu.append_item(menuitem_mock)
    base_menu.append_item(submenuitem_mock)

    base_menu.debug()
    submenuitem_mock.submenu.debug.assert_called_once()
