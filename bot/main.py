import json
import time
from ctypes import windll

import keyboard
import pyautogui

COOLDOWN_BEFORE_ASCENDING = 300  # seconds


class Main:
    def __init__(self):
        self.last_firefly_position_color = [
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
        ]
        print("Starting in 3 seconds...")
        time.sleep(3)

        with open("settings/calibration.json") as json_file:
            self.calibration = json.load(json_file)

    @staticmethod
    def get_rgb(x, y):
        dc = windll.user32.GetDC(0)
        rgb = windll.gdi32.GetPixel(dc, x, y)
        r = rgb & 0xFF
        g = (rgb >> 8) & 0xFF
        b = (rgb >> 16) & 0xFF
        return [r, g, b]

    def get_color(self, json_key):
        """Return a list containing the RGB of a given position"""
        r, g, b = self.get_rgb(
            self.calibration[json_key][0][0],
            self.calibration[json_key][0][1],
        )
        return [r, g, b]

    @staticmethod
    def raw_click(x, y):
        pyautogui.click(
            x=x,
            y=y,
        )

    def click(self, json_key):
        self.raw_click(
            x=self.calibration[json_key][0][0],
            y=self.calibration[json_key][0][1],
        )

    @staticmethod
    def check_pause_quit():
        if keyboard.is_pressed("p"):
            print("Bot stopped, press R to resume")
            keyboard.wait("r")
            print("Bot resumed")
        if keyboard.is_pressed("k"):
            raise KeyboardInterrupt

    def check_firefly(self):
        x = self.calibration["firefly_center"][0][0]
        y = self.calibration["firefly_center"][0][1]
        y_increment = y // 10
        for i in range(0, 6):
            if i < 3:
                new_y = y - y_increment
            elif i == 3:
                new_y = y
            else:
                new_y = y + y_increment

            r, g, b = self.get_rgb(x, new_y)

            red_diff = abs(r - self.last_firefly_position_color[i][0])
            green_diff = abs(g - self.last_firefly_position_color[i][1])
            blue_diff = abs(b - self.last_firefly_position_color[i][2])
            if any(
                [
                    red_diff > r * 1.5,
                    green_diff > g * 1.5,
                    blue_diff > b * 1.5,
                ]
            ):
                self.raw_click(x, new_y)
            self.last_firefly_position_color[i] = (r, g, b)

    def keep_doing_something(self, action: str, seconds: int):
        match action:
            case "building":
                btn = "building_buy_all"
                self.click("building_tab")
            case "research":
                btn = "research_buy_all"
                self.click("research_tab")
            case "clicking":
                btn = "firefly_center"
            case _:
                return

        start = time.time()
        while time.time() - start < seconds:
            self.check_pause_quit()
            self.check_firefly()
            self.click(btn)
            time.sleep(0.1)

    def ascend(self):
        time.sleep(0.5)
        self.click("elixir_tab")
        time.sleep(0.5)
        self.click("elixir_ascend")
        time.sleep(0.5)
        self.click("elixir_ascend_confirmation")

    def start_bot(self):
        print("Press 'K' to quit.")
        print("Press 'P' to pause.")

        try:
            while True:
                start = time.time()
                time.sleep(0.5)
                while time.time() - start < COOLDOWN_BEFORE_ASCENDING:
                    print(time.time() - start)
                    self.check_pause_quit()
                    self.check_firefly()
                    time.sleep(0.5)
                    self.keep_doing_something("building", 5)
                    time.sleep(0.5)
                    self.keep_doing_something("research", 5)

                    rgb = self.get_color("is_energy_enabled")
                    r = rgb[0]
                    energy_disabled_red_color = self.calibration[
                        "is_energy_enabled"
                    ][1][0]
                    while r == energy_disabled_red_color:
                        self.keep_doing_something("clicking", 5)
                        rgb = self.get_color("is_energy_enabled")
                        r = rgb[0]

                # Ascend
                self.ascend()
        except KeyboardInterrupt:
            print("\n")
            print("Exiting...")
