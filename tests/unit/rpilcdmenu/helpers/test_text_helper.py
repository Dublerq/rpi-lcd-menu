from rpilcdmenu.helpers.text_helper import get_scrolled_line, get_scrolled_text, get_text_lines


def test_get_scrolled_line_returns_requested_line_of_sixteen_characters_given_long_text():
    sample_text = "Lorem ipsum dolor sit amet"
    result = get_scrolled_line(sample_text, 0)

    assert result == "Lorem ipsum dolo"


def test_get_scrolled_line_returns_requested_line_of_characters_given_text_with_newlines():

    result = get_scrolled_text("foo\nbar\nbaz", 2)

    assert result == "baz"


def test_get_scrolled_text_returns_requested_lines_of_sixteen_characters_given_long_text():
    sample_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et"
    result = get_scrolled_text(sample_text, 1)

    assert result == "r sit amet, consectetur adipisci"


def test_get_text_lines_returns_how_many_lines_given_message_has():

    result = get_text_lines("a\nb\ncccccccccccccccc")

    assert result == 3
