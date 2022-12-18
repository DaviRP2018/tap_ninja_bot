import json
import time
from ctypes import windll

import keyboard
import pyautogui


class Notion:
    def __init__(self):
        with open("settings/calibration_template.json") as json_file:
            self.calibration = json.load(json_file)

    @staticmethod
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

    def set_calibrate_value(self, json_key, message):
        print(message)
        self.calibration[json_key] = self.get_position_n_color(key="f")

    def default_buttons(self):
        self.set_calibrate_value(
            "is_energy_enabled", "Pick the energy enabled yellow border"
        )
        self.set_calibrate_value(
            "firefly_center", "Press 'F' when the firefly is in the center"
        )

        # Buildings
        self.set_calibrate_value("building_tab", "Press 'F' on building tab")
        self.set_calibrate_value(
            "building_buy_all", "Press 'F' on buy all button"
        )

        # Research
        self.set_calibrate_value("research_tab", "Press 'F' on research tab")
        self.set_calibrate_value(
            "research_buy_all", "Press 'F' on buy all button"
        )

        # Elixir
        self.set_calibrate_value("elixir_tab", "Press 'F' on elixir tab")
        self.set_calibrate_value(
            "elixir_ascend", "Press 'F' on ascension button"
        )
        self.set_calibrate_value(
            "elixir_ascend_confirmation",
            "Press 'F' on ascension confirmation button",
        )

    def calibrate(self):
        with open("settings/calibration.json", "w") as json_file:
            json_file.truncate()

            print("Press Ctrl-C to quit.", end="\n\n")
            print("Press 'F' to pick the color.")
            self.default_buttons()

            json.dump(self.calibration, json_file)
            print("Saved")

    def calibrate_energy(self):
        with open("settings/calibration.json", "w") as json_file:
            self.set_calibrate_value(
                "is_energy_enabled", "Pick the energy enabled yellow border"
            )
            json.dump(self.calibration, json_file)

    def calibrate_firefly(self):
        with open("settings/calibration.json", "w") as json_file:
            self.set_calibrate_value(
                "firefly_center", "Press 'F' when the firefly is in the center"
            )
            json.dump(self.calibration, json_file)
