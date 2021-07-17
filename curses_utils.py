import curses

from color_pair import ColorPair


def add_str_color(screen: curses.window, y: int, x: int, string: str, color_pair: ColorPair) -> None:
    """
    Wraps curses.window.addstr but adds the string in a passed color

    Parameters:
    screen : curses.window
        The window that the string should be added to
    y : int
        The relative (to the screen) y position of the string
    x : int
        The relative (to the screen) x position of the string
    color_pair: ColorPair
        The corresponding enum key for the desired color
    """
    screen.attron(curses.color_pair(color_pair.value))
    screen.addstr(y, x, string)
    screen.attroff(curses.color_pair(color_pair.value))


def ins_ch_color(screen: curses.window, y: int, x: int, character: str, color_pair: ColorPair) -> None:
    """
    Wraps curses.window.insch but draws the character in a passed color

    Parameters:
    screen : curses.window
        The window that the character should be added to
    y : int
        The relative (to the screen) y position of the character
    x : int
        The relative (to the screen) x position of the character
    color_pair: ColorPair
        The corresponding enum key for the desired color
    """
    screen.attron(curses.color_pair(color_pair.value))
    screen.insch(y, x, character)
    screen.attroff(curses.color_pair(color_pair.value))
