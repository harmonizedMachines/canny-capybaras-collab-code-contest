import curses
import threading
import time
from enum import Enum

import psutil


class ColorPair(Enum):
    """
    Enumerate color pair numbers

    Naming Scheme: fg_on_bg
    """

    black_on_white = 1
    red_on_black = 2
    blue_on_black = 3


def initialize_colors() -> None:
    """Initialize each color pair"""
    curses.init_pair(ColorPair.black_on_white.value, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(ColorPair.red_on_black.value, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.blue_on_black.value, curses.COLOR_BLUE, curses.COLOR_BLACK)


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


def draw_title_window(screen: curses.window, height: int, width: int, y: int, x: int) -> None:
    """
    Draws the title window with the application name

    Parameters:
    screen : curses.window
        The parent window of the title window
    height : int
        The height of the title window
    width : int
        The width of the title window
    y : int
        The absolute y position of the title window
    x : int
        The absolute x position of the title window
    """
    title_win = screen.subwin(height, width, y, x)
    title_win.border()

    title = "XKCD Extractor"
    centered_x = width // 2 - len(title) // 2
    title_win.addstr(1, centered_x, title)


def draw_output_window(screen: curses.window, height: int, width: int, y: int, x: int) -> None:
    """
    Draws the output window with information scraped based on user input

    Parameters:
    screen : curses.window
        The parent window of the output window
    height : int
        The height of the output window
    width : int
        The width of the output window
    y : int
        The absolute y position of the output window
    x : int
        The absolute x position of the output window
    """
    output_win = screen.subwin(height, width, y, x)
    output_win.border(0, 0, 0, 0, curses.ACS_SSSB)

    output_win.addstr(1, 1, "ID: N/A")
    output_win.addstr(2, 1, "Title: N/A")
    output_win.addstr(3, 1, "Caption: N/A")
    output_win.addstr(4, 1, "Image URL: N/A")

    add_str_color(output_win, height - 2, 1, "Back", ColorPair.black_on_white)
    num_results_text = "0/0 Results"

    output_win.addstr(height - 2, width // 2 - len(num_results_text) // 2, num_results_text)

    next_text = "Next"
    add_str_color(output_win, height - 2, width - len(next_text) - 1, next_text, ColorPair.black_on_white)


def draw_input_window(screen: curses.window, height: int, width: int, y: int, x: int) -> None:
    """
    Draws the input window where the user can input data

    Parameters:
    screen : curses.window
        The parent window of the input window
    height : int
        The height of the input window
    width : int
        The width of the input window
    y : int
        The absolute y position of the input window
    x : int
        The absolute x position of the input window
    """
    input_win = screen.subwin(height, width, y, x)
    input_win.border(0, 0, 0, 0, curses.ACS_TTEE, curses.ACS_SBSS, curses.ACS_BTEE)

    comic_id_text = "Comic ID(s):"
    input_win.addstr(1, 1, comic_id_text)
    add_str_color(input_win, 1, len(comic_id_text) + 2, "1", ColorPair.red_on_black)

    output_type_text = "File Format:"
    input_win.addstr(2, 1, output_type_text)
    add_str_color(input_win, 2, len(output_type_text) + 2, "JSON", ColorPair.blue_on_black)


def draw_menu(screen: curses.window) -> None:
    """Draws the entire menu"""
    sh, sw = screen.getmaxyx()
    draw_title_window(screen, 3, sw, 0, 0)
    bottom_win_height = sh - 2
    output_win_width = sw // 2 + 25
    input_win_width = sw - output_win_width + 1
    draw_output_window(screen, bottom_win_height - 1, output_win_width, 2, 0)
    draw_input_window(screen, bottom_win_height - 1, input_win_width, 2, output_win_width - 1)


def draw_status_bar(screen: curses.window) -> None:
    """
    Draws the status bar at the bottom of the screen

    Parameters:
    screen : curses.window
        The parent window of the status bar
    """
    sh, sw = screen.getmaxyx()
    cpu_percent = psutil.cpu_percent()
    status_bar_text = f"Press 'q' to exit | STATUS BAR | CPU Usage: {cpu_percent}%"
    whitespace_width = " " * (sw - len(status_bar_text) - 1)
    add_str_color(screen, sh - 1, 0, status_bar_text, ColorPair.black_on_white)
    add_str_color(screen, sh - 1, len(status_bar_text), whitespace_width, ColorPair.black_on_white)

    screen.attron(curses.color_pair(ColorPair.black_on_white.value))
    screen.insch(sh - 1, sw - 1, " ")  # using insch so doesn't wrap and cause error
    screen.attroff(curses.color_pair(ColorPair.black_on_white.value))


def draw_status_bar_continuously(screen: curses.window, delay: float) -> None:
    """
    Draws the status bar on the screen and refreshes the screen continously with a delay

    Parameters:
    screen : curses.window
        The parent window of the status bar
    delay : float
        The delay in seconds before the status bar is drawn again
    """
    while True:
        draw_status_bar(screen)
        screen.refresh()
        time.sleep(delay)


def resize_handler(screen: curses.window) -> None:
    """
    Called when the terminal is resized

    Parameters:
    screen : curses.window
        The main window
    """
    screen.clear()
    draw_menu(screen)


def main(screen: curses.window) -> None:
    """
    The entry point of the program

    Parameters:
    screen : curses.window
        The main window
    """
    curses.curs_set(0)
    curses.mousemask(curses.BUTTON1_RELEASED)
    initialize_colors()
    draw_menu(screen)
    status_bar_thread = threading.Thread(target=draw_status_bar_continuously, args=(screen, 0.5))
    status_bar_thread.daemon = True
    status_bar_thread.start()

    while True:
        draw_status_bar(screen)
        ch = screen.getch()
        if ch == curses.KEY_RESIZE:
            curses.curs_set(0)
            resize_handler(screen)
        elif ch == ord('q'):
            return


if __name__ == "__main__":
    curses.wrapper(main)
