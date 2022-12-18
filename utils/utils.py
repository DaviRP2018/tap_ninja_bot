import json
import time
from ctypes import windll

import keyboard
import pyautogui


def show_color():
    """Show color where pointer is"""
    print("Press Ctrl-C to quit.")
    dc = windll.user32.GetDC(0)
    try:
        while True:
            x, y = pyautogui.position()
            rgb = windll.gdi32.GetPixel(dc, x, y)
            r = rgb & 0xFF
            g = (rgb >> 8) & 0xFF
            b = (rgb >> 16) & 0xFF
            color = "{} {} {}".format(r, g, b)
            print(color, end="")
            print("\b" * len(color), end="", flush=True)
    except KeyboardInterrupt:
        return


def show_position():
    """Show position where pointer is"""
    print("Press Ctrl-C to quit.")
    try:
        while True:
            x, y = pyautogui.position()
            position_str = "X: " + str(x).rjust(4) + " Y: " + str(y).rjust(4)
            print(position_str, end="")
            print("\b" * len(position_str), end="", flush=True)
    except KeyboardInterrupt:
        return


def get_position_n_color(key):
    time.sleep(1)
    dc = windll.user32.GetDC(0)
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == key:
            x, y = pyautogui.position()
            rgb = windll.gdi32.GetPixel(dc, x, y)
            r = rgb & 0xFF
            g = (rgb >> 8) & 0xFF
            b = (rgb >> 16) & 0xFF
            return [(x, y), (r, g, b)]


def set_calibrate_value(message):
    print(message)
    return get_position_n_color(key="f")


def calibrate():
    """"""
    with open("settings/calibration_template.json") as json_file:
        calibration = json.load(json_file)
    with open("settings/calibration.json", "w") as json_file:
        json_file.truncate()

        print("Press Ctrl-C to quit.", end="\n\n")
        print("Press 'F' to pick the color.")

        calibration["is_energy_enabled"] = set_calibrate_value(
            "Pick the energy enabled yellow border"
        )
        calibration["vaga_lume_center"] = set_calibrate_value(
            "Press 'F' when the vaga-lume is in the center"
        )

        # Buildings
        calibration["building_tab"] = set_calibrate_value(
            "Press 'F' on building tab"
        )
        calibration["building_buy_all"] = set_calibrate_value(
            "Press 'F' on buy all button"
        )

        # Research
        calibration["research_tab"] = set_calibrate_value(
            "Press 'F' on research tab"
        )
        calibration["research_buy_all"] = set_calibrate_value(
            "Press 'F' on buy all button"
        )

        # Elixir
        calibration["elixir_tab"] = set_calibrate_value(
            "Press 'F' on elixir tab"
        )
        calibration["elixir_ascend"] = set_calibrate_value(
            "Press 'F' on ascension button"
        )
        calibration["elixir_ascend_confirmation"] = set_calibrate_value(
            "Press 'F' on ascension confirmation button"
        )

        json.dump(calibration, json_file)
        print("Saved")


def get_color(x, y):
    """Return a list containing the RGB of a given position"""
    dc = windll.user32.GetDC(0)
    rgb = windll.gdi32.GetPixel(dc, x, y)
    r = rgb & 0xFF
    g = (rgb >> 8) & 0xFF
    b = (rgb >> 16) & 0xFF
    return [r, g, b]
