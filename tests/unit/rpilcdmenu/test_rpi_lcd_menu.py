from mock import Mock, MagicMock, patch, call
from rpilcdmenu.rpi_lcd_menu import RpiLCDMenu


@patch('rpilcdmenu.rpi_lcd_menu.RpiLCDHwd')
def test_rpilcdmenu_imports_gpio_and_initializes_with_clear_screen(LCDHwdMock):
    LCDHwdMockInstance = MagicMock()
    LCDHwdMock.return_value = LCDHwdMockInstance

    GPIOMock = Mock()
    RpiLCDMenu(1, 2, [3, 4, 5, 6], GPIOMock)

    LCDHwdMock.assert_called_once_with(1, 2, [3, 4, 5, 6], GPIOMock)
    LCDHwdMockInstance.initDisplay.assert_called_once()
    LCDHwdMockInstance.write4bits.assert_called_once_with(LCDHwdMock.LCD_CLEARDISPLAY)
    LCDHwdMockInstance.delayMicroseconds.assert_called_once_with(3000)


@patch('rpilcdmenu.rpi_lcd_menu.RpiLCDHwd')
def test_rpilcdmenu_message_sends_bytes_of_message_to_rpi(LCDHwdMock):
    LCDHwdMockInstance = MagicMock()
    LCDHwdMock.return_value = LCDHwdMockInstance

    menu = RpiLCDMenu()
    LCDHwdMockInstance.reset_mock()

    menu.message("1\n")

    assert LCDHwdMockInstance.write4bits.mock_calls == [call(ord("1"), True), call(0xC0)]


@patch('rpilcdmenu.rpi_lcd_menu.RpiLCDHwd')
def test_rpilcdmenu_longMessage_sends_bytes_of_message_to_rpi(LCDHwdMock):
    LCDHwdMockInstance = MagicMock()
    LCDHwdMock.return_value = LCDHwdMockInstance

    menu = RpiLCDMenu()
    LCDHwdMockInstance.reset_mock()

    menu.longMessage("1")

    LCDHwdMockInstance.write4bits.assert_called_once_with(ord("1"), True)


@patch('rpilcdmenu.rpi_lcd_menu.RpiLCDHwd')
def test_rpilcdmenu_longMessage_breaks_line_after_16_chars(LCDHwdMock):
    LCDHwdMockInstance = MagicMock()
    LCDHwdMock.return_value = LCDHwdMockInstance

    menu = RpiLCDMenu()
    LCDHwdMockInstance.reset_mock()

    menu.longMessage("11111111111111112")

    assert LCDHwdMockInstance.write4bits.mock_calls == [
        call(ord("1"), True) for i in range(16)
    ] + [call(0xC0), call(ord("2"), True)]

@patch('rpilcdmenu.rpi_lcd_menu.RpiLCDHwd')
def test_rpilcdmenu_displayTestScreen_sends_dummy_message_to_rpi(LCDHwdMock):
    LCDHwdMockInstance = MagicMock()
    LCDHwdMock.return_value = LCDHwdMockInstance

    menu = RpiLCDMenu()
    LCDHwdMockInstance.reset_mock()

    menu.displayTestScreen()

    LCDHwdMockInstance.write4bits.assert_called()


@patch('rpilcdmenu.rpi_lcd_menu.RpiLCDHwd')
def test_rpilcdmenu_render_empty_menu(LCDHwdMock):
    LCDHwdMockInstance = MagicMock()
    LCDHwdMock.return_value = LCDHwdMockInstance

    menu = RpiLCDMenu()
    menu.start()
    LCDHwdMockInstance.reset_mock()

    menu.render()

    assert LCDHwdMockInstance.write4bits.mock_calls == [call(LCDHwdMock.LCD_CLEARDISPLAY)] + [
        call(ord(char), True) for char in "Menu is empty"
    ]


@patch('rpilcdmenu.rpi_lcd_menu.RpiLCDHwd')
def test_rpilcdmenu_render_two_items_menu(LCDHwdMock):
    LCDHwdMockInstance = MagicMock()
    LCDHwdMock.return_value = LCDHwdMockInstance

    menu = RpiLCDMenu()
    LCDHwdMockInstance.reset_mock()

    item1Mock = Mock()
    item1Mock.text = "item1"
    item2Mock = Mock()
    item2Mock.text = "item2"

    menu.append_item(item1Mock)
    menu.append_item(item2Mock)

    menu.render()

    assert LCDHwdMockInstance.write4bits.mock_calls == [call(LCDHwdMock.LCD_CLEARDISPLAY)] + [
        call(ord(char), True) for char in ">item1"
    ] + [call(0xC0)] + [
        call(ord(char), True) for char in " item2"
    ]


@patch('rpilcdmenu.rpi_lcd_menu.RpiLCDHwd')
def test_rpilcdmenu_render_multiple_items_menu(LCDHwdMock):
    LCDHwdMockInstance = MagicMock()
    LCDHwdMock.return_value = LCDHwdMockInstance

    menu = RpiLCDMenu()

    item1Mock = Mock()
    item1Mock.text = "item1"
    item2Mock = Mock()
    item2Mock.text = "item2"
    item3Mock = Mock()
    item3Mock.text = "item3"

    menu.append_item(item1Mock)
    menu.append_item(item2Mock)
    menu.append_item(item3Mock)

    menu.processDown()
    LCDHwdMockInstance.reset_mock()
    menu.render()

    assert LCDHwdMockInstance.write4bits.mock_calls == [call(LCDHwdMock.LCD_CLEARDISPLAY)] + [
        call(ord(char), True) for char in ">item2"
    ] + [call(0xC0)] + [
        call(ord(char), True) for char in " item3"
    ]


@patch('rpilcdmenu.rpi_lcd_menu.RpiLCDHwd')
def test_rpilcdmenu_render_multiple_items_rewind_menu(LCDHwdMock):
    LCDHwdMockInstance = MagicMock()
    LCDHwdMock.return_value = LCDHwdMockInstance

    menu = RpiLCDMenu()

    item1Mock = Mock()
    item1Mock.text = "item1"
    item2Mock = Mock()
    item2Mock.text = "item2"
    item3Mock = Mock()
    item3Mock.text = "item3"

    menu.append_item(item1Mock)
    menu.append_item(item2Mock)
    menu.append_item(item3Mock)

    menu.processDown()
    menu.processDown()
    LCDHwdMockInstance.reset_mock()
    menu.render()

    assert LCDHwdMockInstance.write4bits.mock_calls == [call(LCDHwdMock.LCD_CLEARDISPLAY)] + [
        call(ord(char), True) for char in ">item3"
    ] + [call(0xC0)] + [
        call(ord(char), True) for char in " item1"
    ]

