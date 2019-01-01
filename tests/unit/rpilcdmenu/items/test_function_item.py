from rpilcdmenu.items.function_item import FunctionItem


def test_functionitem_action_calls_configured_function_with_regular_args_and_returns_its_result():
    function_item = FunctionItem("Test Item", lambda x: x, [2])
    action_result = function_item.action()
    assert 2 == action_result
    assert 2 == function_item.get_return()


def test_functionitem_action_calls_configured_function_with_keyword_args_and_returns_its_result():
    function_item = FunctionItem("Test Item", lambda x, y: (y, x), None, {'x': 2, 'y': 3})
    action_result = function_item.action()
    assert (3, 2) == action_result
    assert (3, 2) == function_item.get_return()
