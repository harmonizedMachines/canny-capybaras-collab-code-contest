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
