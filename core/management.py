import sys

from bot.main import Main
from bot.notion import Notion
from utils.utils import show_color, show_position


class ManagementUtility:
    """
    Encapsulate the logic of the manage.py utilities.
    """

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]

    def execute(self):
        """
        Run given command-line arguments.
        """
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = "help"  # Display help if no arguments were given.

        match subcommand:
            case "runbot":
                bot = Main()
                bot.start_bot()
            case "cha":
                bot = Main()
                bot.chalenge()
            case "cee":
                notion = Notion()
                notion.calibrate()
            case "ce":
                notion = Notion()
                notion.calibrate_energy()
            case "cf":
                notion = Notion()
                notion.calibrate_firefly()
            case "cc":
                notion = Notion()
                notion.calibrate_chalenge()
            case "sc":
                show_color()
            case "sp":
                show_position()
            case _:
                sys.stdout.write("Command not found")


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
