import sys

from bot.main import Main
from utils.utils import calibrate, show_color, show_position


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

        if subcommand == "runbot":
            bot = Main()
            bot.start_bot()
            pass
        elif subcommand == "cee":
            calibrate()
        elif subcommand == "mcc":
            show_color()
        elif subcommand == "mcp":
            show_position()

        else:
            sys.stdout.write("Command not found")


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
