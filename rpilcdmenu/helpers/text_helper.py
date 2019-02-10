
def get_scrolled_line(text, line_number=0):
    """
    :param str text: message to be scrolled
    :param int line_number: which number to start from
    """
    scrolled_text = ''
    char_index = 0
    line_index = 0

    for char in text:
        if line_index == line_number:
            scrolled_text += char

        char_index += 1

        if char_index == 16 or char == '\n':
            if line_index == line_number:
                return scrolled_text
            char_index = 0
            line_index += 1

    return scrolled_text


def get_scrolled_text(text, start_line=0, lines_required=2):
    """
    :param str text: message to be scrolled
    :param int start_line: which number to start from
    :param int lines_required: how many lines are needed
    """
    scrolled_text = ''

    for line in range(start_line, start_line+lines_required):
        scrolled_text += get_scrolled_line(text, line)

    return scrolled_text


def get_text_lines(text):
    """
    :param str text: message to evaluate
    :return int: how many lines the message has
    """
    char_index = 0
    line_counter = 1

    for char in text:
        if char_index == 17 or char == '\n':
            char_index = 0
            line_counter += 1
        char_index += 1

    return line_counter
