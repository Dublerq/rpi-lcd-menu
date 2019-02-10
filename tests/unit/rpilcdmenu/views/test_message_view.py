from mock import call, Mock, MagicMock, patch
from rpilcdmenu.views.message_view import MessageView


@patch('rpilcdmenu.views.message_view.get_text_lines')
@patch('rpilcdmenu.views.message_view.get_scrolled_text')
def test_messageview_render_shows_full_message_in_non_scrollable_mode(get_scrolled_text, get_text_lines):
    message_view = MessageView(Mock(), 'Some multi-line\ntext to be shown\n on LCD', False)

    message_view.message = Mock()
    message_view.render()
    message_view.message.assert_called_once_with('Some multi-line\ntext to be shown\n on LCD')


@patch('rpilcdmenu.views.message_view.get_text_lines')
@patch('rpilcdmenu.views.message_view.get_scrolled_text')
def test_messageview_render_shows_only_part_of_text_in_scrollable_mode(get_scrolled_text, get_text_lines):
    get_scrolled_text.return_value = 'Some multi-line\ntext to be shown'
    get_text_lines.return_value = 3

    message_view = MessageView(Mock(), 'Some multi-line\ntext to be shown\n on LCD', True)

    message_view.message = Mock()
    message_view.render()
    message_view.message.assert_called_once_with('Some multi-line\ntext to be shown')


@patch('rpilcdmenu.views.message_view.get_text_lines')
@patch('rpilcdmenu.views.message_view.get_scrolled_text')
def test_messageview_processDown_scrolls_down_given_message(get_scrolled_text, get_text_lines):
    get_scrolled_text.return_value = ' on LCD'
    get_text_lines.return_value = 3

    message_view = MessageView(Mock(), 'Some multi-line\ntext to be shown\n on LCD', True)

    message_view.message = Mock()

    message_view.render()
    message_view.processDown()
    message_view.processDown()
    message_view.processDown()
    message_view.processDown()

    assert message_view.message.mock_calls[-1] == call(' on LCD')


@patch('rpilcdmenu.views.message_view.get_text_lines')
@patch('rpilcdmenu.views.message_view.get_scrolled_text')
def test_messageview_processDown_scrolls_given_message_up_after_scrolling_it_down(get_scrolled_text, get_text_lines):
    get_scrolled_text.return_value = 'Some multi-line\ntext to be shown'
    get_text_lines.return_value = 3

    message_view = MessageView(Mock(), 'Some multi-line\ntext to be shown\n on LCD', True)

    message_view.message = Mock()

    message_view.render()
    message_view.processDown()
    message_view.processDown()
    message_view.processUp()
    message_view.processUp()
    message_view.processUp()

    assert message_view.message.mock_calls[-1] == call('Some multi-line\ntext to be shown')


@patch('rpilcdmenu.views.message_view.get_text_lines')
@patch('rpilcdmenu.views.message_view.get_scrolled_text')
def test_messageview_processEnter_exits_to_parent_menu(get_scrolled_text, get_text_lines):
    parent_menu_mock = MagicMock()

    message_view = MessageView(parent_menu_mock, 'Some multi-line\ntext to be shown\n on LCD', True)
    message_view.processEnter()
    parent_menu_mock.render.assert_called_once()
