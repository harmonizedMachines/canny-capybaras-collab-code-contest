from abc import ABC, abstractmethod
from typing import List


class Button(ABC):
    """
    Class that handles clickable bounding boxes
    Attributes:
    top_left_y : int
        The absolute top left y position of the button's bounding box
    top_left_x : int
        The absolute top left x position of the button's bounding box
    bottom_right_y : int
        The absolute bottom right y position of the button's bounding box
    bottom_right_x : int
        The absolute bottom right x position of the button's bounding box
    """

    def set_bounding_box(self, top_left_y: int, top_left_x: int, bottom_right_y: int, bottom_right_x: int) -> None:
        """Sets the region where the button can be clicked"""
        self.top_left_y = top_left_y
        self.top_left_x = top_left_x
        self.bottom_right_y = bottom_right_y
        self.bottom_right_x = bottom_right_x

    def try_click(self, mouse_y: int, mouse_x: int) -> None:
        """Attempts to click the button by first checking if the mouse intersects with the button"""
        if self.is_intersecting(mouse_y, mouse_x):
            self.on_click()

    def is_intersecting(self, y: int, x: int) -> bool:
        """Checks if the coordinates intersect the button's bounding box"""
        return self.top_left_y <= y <= self.bottom_right_y and self.top_left_x <= x <= self.bottom_right_x

    @abstractmethod
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
    options : list[str]
        The list of options that the button can cycle through
    current_option_index : int
        The index of the currently selected options
        Starts at 0
    """
    def __init__(self):
        self.editing = False
        self.text = "1"

    def on_click(self) -> None:
        """Called when the button is clicked"""
        self.editing = True

    def get_current_option(self) -> str:
        """Gets the currently shown option"""
        return self.text

    def next_charachter(self, ascii_code: int) -> None:
        if self.editing:
            if ascii_code == 8:
                self.text = self.text[:-1]
            elif ascii_code == 10:
                self.editing = False
            else:
                self.text += chr(ascii_code)
