import pytest
import mock
from rpilcdmenu.items.menu_item import MenuItem


def test_menuitem_throws_exception_when_title_is_too_long():
    with pytest.raises(NameError):
        MenuItem("Definetely Too Long Text To Display")


def test_menuitem_can_return_its_title_as_string():
    menu_item = MenuItem("an Item")
    assert "an Item" == menu_item.__str__()


def test_menuitem_show_return_menu_representaiton():
    menu_item = MenuItem("an Item")
    assert "3 - an Item" == menu_item.show(2)


def test_menuitem_has_set_up_method():
    menu_item = MenuItem("an Item")
    assert None == menu_item.set_up()


def test_menuitem_has_action_method():
    menu_item = MenuItem("an Item")
    assert None == menu_item.action()


def test_menuitem_has_cleanup_method():
    menu_item = MenuItem("an Item")
    assert None == menu_item.clean_up()


def test_menuitem_get_return_returns_parent_menu_value_given_parent_menu():
    parent_menu_mock = mock.Mock()
    parent_menu_mock.get_return.return_value=123

    menu_item = MenuItem("an Item", parent_menu_mock)

    assert 123 == menu_item.get_return()


def test_menuitem_get_return_returns_None_given_no_parent_menu():
    menu_item = MenuItem("an Item")
    assert None == menu_item.get_return()
