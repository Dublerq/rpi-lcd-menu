import mock

from rpilcdmenu.rpi_lcd_submenu import RpiLCDSubMenu


def test_rpilcdmenu_can_be_initialized():
    base_menu_mock = mock.Mock()
    submenu = RpiLCDSubMenu(base_menu_mock)
    assert isinstance(submenu, RpiLCDSubMenu)
