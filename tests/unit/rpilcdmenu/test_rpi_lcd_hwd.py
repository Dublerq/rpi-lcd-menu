import pytest
import sys
import datetime
from mock import Mock, MagicMock, patch, call

from rpilcdmenu.rpi_lcd_hwd import RpiLCDHwd


def test_rpilcdhwd_cannot_be_initialized_without_gpio_support():
    with patch.dict(sys.modules, {'RPi.GPIO': None}):
        with pytest.raises(ImportError):
            RpiLCDHwd()


def test_rpilcdhwd_imports_gpio_and_initializes_provided_gpio_pins_in_bcm_mode():
    GPIO_mock = Mock()
    GPIO_mock.setup = Mock()
    GPIO_mock.OUT = 'out'
    GPIO_mock.IN = 'in'
    GPIO_mock.BCM = 'BCM'
    GPIO_mock.setmode = Mock()
    RPi_mock = Mock()
    RPi_mock.GPIO = GPIO_mock

    with patch.dict(sys.modules, {'RPi': RPi_mock, 'RPi.GPIO': Mock()}):
        RpiLCDHwd(1, 2, [3, 4, 5, 6])

        GPIO_mock.setmode.assert_called_once_with(GPIO_mock.BCM)

        setup_calls = [
            call(1, GPIO_mock.OUT),
            call(2, GPIO_mock.OUT),
            call(3, GPIO_mock.OUT),
            call(4, GPIO_mock.OUT),
            call(5, GPIO_mock.OUT),
            call(6, GPIO_mock.OUT)
        ]

        GPIO_mock.setup.assert_has_calls(setup_calls, any_order=True)


def test_rpilcdhwd_initDisplay_configures_proper_lcd_settings():
    RPi_mock = Mock()
    RPi_mock.GPIO = MagicMock()

    with patch.dict(sys.modules, {'RPi': RPi_mock, 'RPi.GPIO': Mock()}):
        lcd = RpiLCDHwd(1, 2, [3, 4, 5, 6])

        lcd.write4bits = Mock()
        lcd.initDisplay()

        assert lcd.write4bits.mock_calls == [
            call(0x33),
            call(0x32),
            call(0x28),
            call(0x0C),
            call(0x06),
            call(0x06),
        ]


def test_rpilcdhwd_initDisplay_configures_proper_lcd_settings():
    RPi_mock = Mock()
    RPi_mock.GPIO = MagicMock()

    with patch.dict(sys.modules, {'RPi': RPi_mock, 'RPi.GPIO': Mock()}):
        lcd = RpiLCDHwd(1, 2, [3, 4, 5, 6])

        lcd.write4bits = Mock()
        lcd.initDisplay()

        assert lcd.write4bits.mock_calls == [
            call(0x33),
            call(0x32),
            call(0x28),
            call(0x0C),
            call(0x06),
            call(0x06),
        ]


def test_rpilcdmenu_write4bits_transfers_data_through_GPIO():
    RPi_mock = Mock()
    RPi_mock.GPIO = Mock()
    RPi_mock.GPIO.output = Mock()

    with patch.dict(sys.modules, {'RPi': RPi_mock, 'RPi.GPIO': Mock()}):
        lcd = RpiLCDHwd(1, 2, [3, 4, 5, 6])

        lcd.delayMicroseconds = Mock()
        lcd.pulseEnable = Mock()

        lcd.write4bits(0x123)
        assert RPi_mock.GPIO.output.mock_calls == [
            call(1, False),
            call(3, False),
            call(4, False),
            call(5, False),
            call(6, False),
            call(6, True),
            call(3, True),
            call(3, False),
            call(4, False),
            call(5, False),
            call(6, False),
            call(3, True)
        ]


def test_rpilcdmenu_delayMicroseconds_waits_given_microseconds():
    RPi_mock = Mock()
    RPi_mock.GPIO = Mock()

    with patch.dict(sys.modules, {'RPi': RPi_mock, 'RPi.GPIO': Mock()}):
        lcd = RpiLCDHwd(1, 2, [3, 4, 5, 6])

        start_time = datetime.datetime.now()

        lcd.delayMicroseconds(10)

        assert (datetime.datetime.now() - start_time).microseconds >= 10


def test_rpilcdmenu_pulseEnable_is_blinking_pin_e():
    RPi_mock = Mock()
    RPi_mock.GPIO = Mock()
    RPi_mock.GPIO.output = Mock()

    with patch.dict(sys.modules, {'RPi': RPi_mock, 'RPi.GPIO': Mock()}):
        lcd = RpiLCDHwd(1, 2, [3, 4, 5, 6])

        lcd.pulseEnable()

        assert RPi_mock.GPIO.output.mock_calls == [call(2, False), call(2, True), call(2, False)]
