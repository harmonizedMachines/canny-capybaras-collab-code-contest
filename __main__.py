import curses
from typing import Optional


def main(screen: Optional[curses.window]) -> None:
    """
    The entry point of the program

    Parameters:
    screen : curses.window
        The main window
    """
    pass


if __name__ == "__main__":
    curses.wrapper(main)
