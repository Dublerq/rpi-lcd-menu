import pytest
import sys
from mock import mock, patch

from rpilcdmenu import RpiLCDMenu

def test_rpilcdmenu_cannot_be_initialized_without_gpio_support():
    with mock.patch.dict(sys.modules, {'RPi.GPIO': None}):
        with pytest.raises(ImportError):
            menu = RpiLCDMenu()

def test_rpilcdmenu_can_be_initialized():
    with mock.patch.dict(sys.modules, {'RPi': mock.MagicMock(), 'RPi.GPIO': mock.MagicMock()}):
        menu = RpiLCDMenu(26, 19, [13, 6, 5, 21])
        assert isinstance(menu, RpiLCDMenu)