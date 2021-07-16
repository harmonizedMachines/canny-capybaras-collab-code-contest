import curses
import os
import threading
import time

import img2text
import psutil

import xkcd_extractor
from buttons import Button, CyclableButton, EditableButton, HyperlinkButton
from color_pair import ColorPair
from curses_utils import add_str_color


class App():
    """
    A class containing the application's frontend

    Methods:
    start()
        Starts the application
    main(screen : curses.window)
        The entry point of the application
    initialize_colors(screen : curses.window)
        Initializes each color pair
    draw_menu(screen : curses.window, delay : float)
        Draws the entire menu
    draw_status_bar_continuously()
        Draws the status bar on the screen and refreshes the screen continously with a delay
    draw_title_window(screen : curses.window, height : int, width : int, y : int, x : int)
        Draws the title window with the application name
    draw_output_window(screen : curses.window, height : int, width : int, y : int, x : int)
        Draws the output window with information scraped based on user input
    draw_input_window(screen : curses.window, height : int, width : int, y : int, x : int)
        Draws the input window where the user can input data
    draw_status_bar(screen : curses.window)
        Draws the status bar at the bottom of the screen
    Attributes:
    buttons : list[Button]
        A list of every button object
    file_format_button : CyclableButton
        The button that allows the user to change the file format uses when the data is outputted
    """

    file_format_button = CyclableButton(["JSON", "CSV"])
    start_button = CyclableButton(["START", "STOP"])
    comic_id_button = EditableButton()
    next_button = Button()
    back_button = Button()
    comic_url_button = HyperlinkButton()
    image_url_button = HyperlinkButton()
    open_folder_button = Button()
    show_image_button = CyclableButton(["Show Image", "Hide Image"])
    buttons = [
        file_format_button, comic_id_button, start_button,
        next_button, back_button,
        comic_url_button, image_url_button,
        open_folder_button,
        show_image_button,
    ]

    comic_results = None
    comic_results_index = 0

    def start(self) -> None:
        """Starts the application"""
        curses.wrapper(self.main)

    def main(self, screen: curses.window) -> None:
        """
        The entry point of the application

        Parameters:
        screen : curses.window
            The main window
        """
        curses.curs_set(0)
        curses.mousemask(curses.BUTTON1_RELEASED)
        curses.mouseinterval(0)
        self.initialize_colors()
        self.draw_menu(screen)
        status_bar_thread = threading.Thread(target=self.draw_status_bar_continuously, args=(screen, 0.5))
        status_bar_thread.daemon = True
        status_bar_thread.start()

        while True:
            ch = screen.getch()
            if ch == curses.KEY_RESIZE:
                curses.curs_set(0)
                self.draw_menu(screen)
            elif ch == curses.KEY_MOUSE:
                _, mouse_x, mouse_y, _, mouse_state = curses.getmouse()
                if not mouse_state:
                    for button in self.buttons:
                        if not button.try_click(mouse_y, mouse_x):
                            continue
                        if button == self.start_button:
                            if self.start_button.get_current_option() == "STOP":
                                self.draw_menu(screen)
                                file_format = self.file_format_button.get_current_option().lower()
                                self.comic_results = xkcd_extractor.crawl(self.comic_id_button.text, file_format)
                            else:
                                self.comic_results = []
                                self.comic_results_index = 0
                        elif button == self.next_button:
                            self.comic_results_index = (self.comic_results_index + 1) % len(self.comic_results.comics)
                        elif button == self.back_button:
                            self.comic_results_index = (self.comic_results_index - 1) % len(self.comic_results.comics)
                        elif button == self.open_folder_button:
                            image_path = self.comic_results.image_paths[self.comic_results_index]
                            folder_path = '\\'.join(image_path.split('\\')[:-1])
                            os.startfile(folder_path)  # noqa: S606 - Temporary
                    self.draw_menu(screen)
            elif ch == ord('q'):
                return
            else:
                self.comic_id_button.next_character(ch)
                self.draw_menu(screen)

    def initialize_colors(self) -> None:
        """Initializes each color pair"""
        curses.init_pair(ColorPair.black_on_white.value, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(ColorPair.red_on_black.value, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(ColorPair.blue_on_black.value, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(ColorPair.green_on_black.value, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(ColorPair.white_on_black.value, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def draw_menu(self, screen: curses.window) -> None:
        """Draws the entire menu"""
        screen.clear()
        sh, sw = screen.getmaxyx()
        self.draw_title_window(screen, 3, sw, 0, 0)

        bottom_win_height = sh - 2
        output_win_width = sw // 2 + 25
        input_win_width = sw - output_win_width + 1

        self.draw_output_window(screen, bottom_win_height - 1, output_win_width, 2, 0)
        self.draw_input_window(screen, bottom_win_height - 1, input_win_width, 2, output_win_width - 1)

        self.draw_status_bar(screen)

    def draw_status_bar_continuously(self, screen: curses.window, delay: float) -> None:
        """
        Draws the status bar on the screen and refreshes the screen continously with a delay

        Parameters:
        screen : curses.window
            The parent window of the status bar
        delay : float
            The delay in seconds before the status bar is drawn again
        """
        while True:
            self.draw_status_bar(screen)
            screen.refresh()
            time.sleep(delay)

    def draw_title_window(self, screen: curses.window, height: int, width: int, y: int, x: int) -> None:
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

    def draw_output_window(self, screen: curses.window, height: int, width: int, y: int, x: int) -> None:
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

        if self.comic_results:
            page_id = self.comic_results.pages[self.comic_results_index]
            title = self.comic_results.titles[self.comic_results_index]
            alt_text = self.comic_results.scripts[self.comic_results_index]
            comic_url = self.comic_results.comic_urls[self.comic_results_index]
            image_url = self.comic_results.image_urls[self.comic_results_index]
            comic_url_text = "Comic URL:"
            image_url_text = "Image URL:"
            output_win.addstr(4, 1, comic_url_text)
            output_win.addstr(5, 1, image_url_text)

            if len(image_url) + len(image_url_text) + 1 >= width:
                image_url = image_url[:len(image_url) + len(image_url_text) - 5]
                image_url += "..."

            if len(comic_url) + len(comic_url_text) + 1 >= width:
                image_url = image_url[:len(comic_url) + len(comic_url_text) - 10]
                image_url += "..."

            add_str_color(output_win, 4, len(comic_url_text) + 2, comic_url, ColorPair.green_on_black)
            add_str_color(output_win, 5, len(image_url_text) + 2, image_url, ColorPair.green_on_black)
            self.comic_url_button.is_enabled = True
            self.image_url_button.is_enabled = True
            self.comic_url_button.url = comic_url
            self.image_url_button.url = image_url
            self.comic_url_button.set_bounding_box(
                6,
                len(comic_url_text) + 2,
                6,
                len(comic_url_text) + len(comic_url) + 2
            )
            self.image_url_button.set_bounding_box(
                7,
                len(image_url_text) + 2,
                7,
                len(image_url_text) + len(image_url) + 2
            )

            show_image_button_text = self.show_image_button.get_current_option()
            add_str_color(output_win, 6, 1, show_image_button_text, ColorPair.green_on_black)
            self.show_image_button.is_enabled = True
            self.show_image_button.set_bounding_box(
                8,
                1,
                8,
                len(show_image_button_text)
            )

            open_folder_text = "Open Folder"
            open_folder_y = 1
            open_folder_x = width - len(open_folder_text) - 2
            add_str_color(output_win, open_folder_y, open_folder_x, open_folder_text, ColorPair.green_on_black)
            self.open_folder_button.is_enabled = True
            self.open_folder_button.set_bounding_box(
                open_folder_y + 2,
                open_folder_x,
                open_folder_y + 2,
                open_folder_x + len(open_folder_text)
            )

            if show_image_button_text == "Hide Image":
                image_path = self.comic_results.image_paths[self.comic_results_index]
                ascii_img = img2text.img_to_ascii(image_path, width=width - 2, reverse=True)
                lines = ascii_img.split('\n')
                for i, line in enumerate(lines):
                    if i > height - 12:
                        break
                    output_win.addstr(i + 8, 1, line)
        else:
            self.comic_url_button.is_enabled = False
            self.image_url_button.is_enabled = False
            self.show_image_button.is_enabled = False
            self.open_folder_button.is_enabled = False
            page_id = "N/A"
            title = "N/A"
            alt_text = "N/A"
            output_win.addstr(4, 1, "Comic URL: N/A")
            output_win.addstr(5, 1, "Image URL: N/A")
        output_win.addstr(1, 1, f"ID: {page_id}")
        output_win.addstr(2, 1, f"Title: {title}")
        if len(alt_text) + len("Alt Text:") + 1 >= width:
            alt_text = alt_text[:width - len("Alt Text:") - 6]
            alt_text += "..."
        output_win.addstr(3, 1, f"Alt Text: {alt_text}")

        if not self.comic_results:
            num_results_text = "0/0 Results"
        else:
            num_results = len(self.comic_results.comics)
            num_results_text = f"{self.comic_results_index + 1}/{num_results} Results"

        output_win.addstr(height - 2, width // 2 - len(num_results_text) // 2, num_results_text)

        next_text = "Next"
        back_text = "Back"
        next_x = width - len(next_text) - 1
        back_x = 1
        add_str_color(output_win, height - 2, next_x, next_text, ColorPair.black_on_white)
        add_str_color(output_win, height - 2, back_x, "Back", ColorPair.black_on_white)

        self.next_button.set_bounding_box(
            height,
            next_x,
            height,
            next_x + len(next_text)
        )
        self.back_button.set_bounding_box(
            height,
            back_x,
            height,
            back_x + len(back_text)
        )

    def draw_input_window(self, screen: curses.window, height: int, width: int, y: int, x: int) -> None:
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

        start_button_text = self.start_button.get_current_option()
        if start_button_text == "START":
            add_str_color(input_win, 3, 1, start_button_text, ColorPair.green_on_black)
        else:
            add_str_color(input_win, 3, 1, start_button_text, ColorPair.red_on_black)

        self.start_button.set_bounding_box(
            3 + y,
            1,
            3 + y,
            len(start_button_text) + x
        )

        comic_id_text = "Comic ID(s):"
        input_win.addstr(1, 1, comic_id_text)
        numbers = self.comic_id_button.text
        add_str_color(input_win, 1, len(comic_id_text) + 2, numbers, ColorPair.red_on_black)
        if self.comic_id_button.editing:
            add_str_color(input_win, 1, len(comic_id_text) + 2 + len(numbers), "_", ColorPair.white_on_black)
            # add_str_color(input_win, 1, len(comic_id_text) + 2 + len(numbers), " ", ColorPair.black_on_white)

        self.comic_id_button.set_bounding_box(
            1 + y,
            len(comic_id_text) + x - 1,
            1 + y,
            len(comic_id_text) + len(numbers) + x + 1
        )

        output_type_text = "File Format:"
        input_win.addstr(2, 1, output_type_text)
        file_format = self.file_format_button.get_current_option()
        add_str_color(input_win, 2, len(output_type_text) + 2, file_format, ColorPair.blue_on_black)

        self.file_format_button.set_bounding_box(
            2 + y,
            len(output_type_text) + x,
            2 + y,
            len(output_type_text) + len(file_format) + x
        )

    def draw_status_bar(self, screen: curses.window) -> None:
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


if __name__ == "__main__":
    app = App()
    app.start()
