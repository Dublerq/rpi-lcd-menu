from mock import Mock, MagicMock, patch
from rpilcdmenu.items.message_item import MessageItem


@patch('rpilcdmenu.items.message_item.MessageView')
def test_messageitem_action_starts_message_view(message_view_mock):
    message_view_instance = MagicMock()
    message_view_mock.return_value = message_view_instance
    message_item = MessageItem('a message', Mock(), Mock())
    message_item.action()
    message_view_instance.start.assert_called_once()
