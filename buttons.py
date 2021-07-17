import os
from typing import List


class Button():
    """
    Class that handles clickable bounding boxes

    Attributes:
    is_enabled : bool
        If true then the button is clickable
    top_left_y : int
        The absolute top left y position of the button's bounding box
    top_left_x : int
        The absolute top left x position of the button's bounding box
    bottom_right_y : int
        The absolute bottom right y position of the button's bounding box
    bottom_right_x : int
        The absolute bottom right x position of the button's bounding box
    """

    is_enabled = True
    top_left_y = -1
    top_left_x = -1
    bottom_right_y = -1
    bottom_right_x = -1

    def set_bounding_box(self, top_left_y: int, top_left_x: int, bottom_right_y: int, bottom_right_x: int) -> None:
        """Sets the region where the button can be clicked"""
        self.top_left_y = top_left_y
        self.top_left_x = top_left_x
        self.bottom_right_y = bottom_right_y
        self.bottom_right_x = bottom_right_x

    def try_click(self, mouse_y: int, mouse_x: int) -> bool:
        """
        Attempts to click the button by first checking if the mouse intersects with the button

        Returns True if it was successful
        """
        if self.is_intersecting(mouse_y, mouse_x):
            self.on_click()
            return True
        return False

    def is_intersecting(self, y: int, x: int) -> bool:
        """Checks if the coordinates intersect the button's bounding box"""
        return (self.is_enabled
                and self.top_left_y <= y <= self.bottom_right_y and self.top_left_x <= x <= self.bottom_right_x)

    def on_click(self) -> None:
        """Called when the button is clicked"""
        pass


class CyclableButton(Button):
    """
    Variant of the button class that cycles through a list of set options each time it is clicked

    Attributes:
    options : list[str]
        The list of options that the button can cycle through
    current_option_index : int
        The index of the currently selected options
        Starts at 0
    """

    def __init__(self, options: List[str]):
        self.options = options
        self.current_option_index = 0

    def on_click(self) -> None:
        """Called when the button is clicked"""
        self.cycle()

    def cycle(self) -> None:
        """Cycles through to the next button option"""
        self.current_option_index = (self.current_option_index + 1) % len(self.options)

    def get_current_option(self) -> str:
        """Gets the currently select option in the list of options"""
        return self.options[self.current_option_index]


class EditableButton(Button):
    """
    Variant of the button class that allows you to edit text

    Attributes:
    editing : bool
        True when the user can edit the button
        False when the user can't
    text : str
        The editable text that the button contains
    """

    def __init__(self):
        self.editing = False
        self.text = "1"

    def on_click(self) -> None:
        """Called when the button is clicked"""
        self.editing = True

    def next_character(self, ascii_code: int) -> None:
        """
        Attempts to input a character and responds accordingly based on the character inputted

        Backspace - Erases the latest character
        Enter - Disables typing
        Any other character - Added to the button's text

        Returns True if the input was valid
        Returns False otherwise
        """
        if self.editing:
            allowed_text = [',', '-', '*']
            if ascii_code == 8:
                self.text = self.text[:-1]
                return True
            elif ascii_code == 10:
                self.editing = False
                return True
            else:
                if 48 <= ascii_code <= 57 or chr(ascii_code) in allowed_text:
                    self.text += chr(ascii_code)
                    return True
        return False


class HyperlinkButton(Button):
    """
    Variant of the button class that opens a link when clicked on

    url : str
        The URL that should be opened when the button is clicked
    """

    url = ""

    def on_click(self) -> None:
        """Opens the URL when the button is clicked"""
        os.startfile(self.url)  # noqa: S606
