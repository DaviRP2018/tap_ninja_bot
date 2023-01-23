import sys

from bot.main import DEFAULT_COOLDOWN_BEFORE_ASCENDING, Chalenge, Main
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

        try:
            ascension_cooldown = int(self.argv[2])
        except (IndexError, ValueError):
            ascension_cooldown = DEFAULT_COOLDOWN_BEFORE_ASCENDING

        try:
            ascend_enabled = bool(self.argv[3])
        except (IndexError, ValueError):
            ascend_enabled = False

        match subcommand:
            case "runbot":
                bot = Main(ascension_cooldown, ascend_enabled)
                bot.start_bot()
            case "cha":
                bot = Chalenge()
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
