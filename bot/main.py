import json
import time
from ctypes import windll
from typing import List, Tuple

import keyboard
import pyautogui

DEFAULT_COOLDOWN_BEFORE_ASCENDING = 300  # seconds


class Main:
    def __init__(self, ascension_cooldown, ascend):
        self.ascend_count = 0
        self.ascension_cooldown = ascension_cooldown
        self.ascend = ascend
        self.dc = 0

        self.show_configs()

        print("Starting in 3 seconds...")
        time.sleep(3)

        with open("settings/calibration.json") as json_file:
            self.calibration = json.load(json_file)
        with open("settings/chalenge.json") as json_file:
            self.chalenge_file = json.load(json_file)

    def show_configs(self):
        print("ascension_cooldown:", self.ascension_cooldown)
        print("ascend:", self.ascend)

    def get_rgb(self, x: int, y: int) -> List[int]:
        """Get RGB based on position"""
        dc_ready = windll.user32.GetDC(0)
        self.dc = dc_ready or self.dc  # This should at least fix? the error
        # with this dawg. For some reason this only returns 0 after a period
        # of time
        if not dc_ready:
            print(f"dc_ready is {dc_ready}")
            print(f"self.dc is now {self.dc}")
        rgb = windll.gdi32.GetPixel(self.dc, x, y)
        r = rgb & 0xFF
        g = (rgb >> 8) & 0xFF
        b = (rgb >> 16) & 0xFF
        return [r, g, b]

    def get_color(self, json_key: str) -> List[int]:
        """Get RGB based on json key"""
        r, g, b = self.get_rgb(
            self.calibration[json_key][0][0],
            self.calibration[json_key][0][1],
        )
        return [r, g, b]

    @staticmethod
    def raw_click(x: int, y: int) -> None:
        """Click based on position"""
        pyautogui.click(
            x=x,
            y=y,
        )

    def click(self, json_key: str, chalenge_mode=False) -> None:
        """
        Click based on json key

        :param json_key: The json key
        :param chalenge_mode: If is chalenge mode
        """
        if chalenge_mode:
            self.raw_click(
                x=self.chalenge_file[json_key][0][0],
                y=self.chalenge_file[json_key][0][1],
            )
        else:
            self.raw_click(
                x=self.calibration[json_key][0][0],
                y=self.calibration[json_key][0][1],
            )

    def watch(self):
        self.check_pause_quit()
        self.check_firefly()

    @staticmethod
    def check_pause_quit() -> None:
        """Checks if user pressed P or K"""
        if keyboard.is_pressed("p"):
            print("Bot stopped, press R to resume")
            keyboard.wait("r")
            print("Bot resumed")
        if keyboard.is_pressed("k"):
            raise KeyboardInterrupt

    def check_firefly(self) -> None:
        """
        Click 7 position in the center
        """
        x = self.calibration["firefly_center"][0][0]
        y = self.calibration["firefly_center"][0][1]
        y_increment = y // 5
        new_ys = [
            y - (3 * y_increment),
            y - (2 * y_increment),
            y - y_increment,
            y,
            y + y_increment,
            y + (2 * y_increment),
            y + (3 * y_increment),
        ]
        for new_y in new_ys:
            self.raw_click(x, new_y)

    def keep_doing_something(self, action: str, seconds: int) -> None:
        """

        :param action: The action to keep doing
        :param seconds: How many seconds it will keep doing the action
        :return: None
        """
        start = time.time()
        match action:
            case "building":
                self.click("building_tab")
                while time.time() - start < seconds:
                    self.watch()
                    self.click("building_buy_all")
            case "research":
                self.click("research_tab")
                while time.time() - start < seconds:
                    self.watch()
                    self.click("research_buy_all_1")
                    self.click("research_buy_all_2")
            case "clicking":
                while time.time() - start < seconds:
                    self.watch()
                    self.click("firefly_center")
            case _:
                return

    def ascend(self) -> None:
        """Method to ascend"""
        self.ascend_count += 1
        time.sleep(0.5)
        self.click("elixir_tab")
        time.sleep(0.5)
        self.click("elixir_ascend")
        time.sleep(0.5)
        self.click("elixir_ascend_confirmation")

    def start_bot(self) -> None:
        """Main entry function to run the bot"""
        print("Press 'K' to quit.")
        print("Press 'P' to pause.")

        try:
            while True:
                if self.ascend:
                    # Ascend
                    self.ascend()

                start = time.time()
                time.sleep(0.5)
                while time.time() - start < self.ascension_cooldown:
                    print(time.time() - start)
                    self.watch()
                    self.keep_doing_something("building", 5)
                    self.keep_doing_something("research", 5)
                    keyboard.send("q")
                    keyboard.send("w")
        except KeyboardInterrupt:
            print("\n")
            print("Exiting...")


class Chalenge:
    def detect_color_change(self, last_color, x, y) -> Tuple[List[int], bool]:
        print("last_color", last_color)
        r, g, b = self.get_rgb(x, y)
        print(r)
        print(g)
        print(b)

        red_diff = abs(r - last_color[0])
        print("red_diff", red_diff)
        green_diff = abs(g - last_color[1])
        print("green_diff", green_diff)
        blue_diff = abs(b - last_color[2])
        print("blue_diff", blue_diff)
        print(
            any(
                [
                    red_diff > r * 1.1,
                    green_diff > g * 1.1,
                    blue_diff > b * 1.1,
                ]
            )
        )
        last_color = [r, g, b]
        return last_color, any(
            [
                red_diff > r,
                green_diff > g,
                blue_diff > b,
            ]
        )

    def chalenge(self):
        print("Press 'K' to quit.")
        print("Press 'P' to pause.")

        last_color = (255, 255, 255)
        try:
            while True:
                self.watch()
                last_color, color_change = self.detect_color_change(
                    last_color,
                    self.chalenge_file["front"][0][0],
                    self.chalenge_file["front"][0][1],
                )
                if color_change:
                    self.click("front", True)
        except KeyboardInterrupt:
            print("\n")
            print("Exiting...")
