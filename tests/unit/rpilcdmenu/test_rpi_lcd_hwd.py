import pytest
import sys
from mock import Mock, MagicMock, patch, call

from rpilcdmenu.rpi_lcd_hwd import RpiLCDHwd


def test_rpilcdmenu_cannot_be_initialized_without_gpio_support():
    with patch.dict(sys.modules, {'RPi.GPIO': None}):
        with pytest.raises(ImportError):
            RpiLCDHwd()


def test_rpilcdmenu_imports_gpio_and_initializes_provided_gpio_pins_in_bcm_mode():
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
