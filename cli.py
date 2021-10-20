import sys
import os

from image import DrawImage
from typing import Dict, Tuple, List, Optional

RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def color(text: str, red: int, green: int, blue: int) -> str:
    return f"\033[38;2;{red};{green};{blue}m{text}"


class ImageCLI(object):
    def create_error_message(self, message, suggestion=None, is_fatal=True) -> None:
        print(color(message, *RED))
        if suggestion:
            print(color(suggestion, *YELLOW))
        sys.exit() if is_fatal else None

    def parse_arguments(self) -> Tuple[List[str], Dict[str, str]]:
        sources, parameters = [], {}
        for index, argument in enumerate(sys.argv[1:]):
            is_valid_parameter = argument.startswith("--")
            if not is_valid_parameter:
                sources.append(argument)
                continue
            slices = argument.split("=")
            key, value = slices[0][2:], "=".join(slices[1:])
            if len(key.strip()) == 0:
                self.create_error_message("Empty values")
            parameters.setdefault(key, value)
        return sources, parameters

    def display_image(self):
        command, parameters = self.parse_arguments()
        image_size = self.create_size_tuple(parameters.get("size") or "50x50")
        for source in command:
            self.draw_image(source, parameters)
            print()

    def draw_image(self, filename, size, parameters):
        if not size:
            self.create_error_message(
                f"Invalid size parameter: {parameters.get('size')}"
            )
        try:
            DrawImage().from_file(filename, sie).draw_image() if os.path.isfile(
                filename
            ) else DrawImage.from_url(filename, size).draw_image()
        except Exception as exception:
            self.create_error_message(exception.__str__())

    def create_size_tuple(self, size_string) -> Optional[Tuple[int, int]]:
        slices = size_string.split("x")
        try:
            tuple_size = tuple(map(lambda element: int(element), slices))[:2]
            return tuple_size if len(tuple_size) == 2 else None
        except Exception as exception:
            return None


def main():
    cli = ImageCLI()
    cli.display_image()
