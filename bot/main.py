import json
import time

import keyboard
import pyautogui

from utils.utils import get_color

COOLDOWN_BEFORE_ASCENDING = 300  # seconds


class Main:
    def __init__(self):
        print("Starting in 3 seconds...")
        time.sleep(3)

        with open("settings/calibration.json") as json_file:
            self.calibration = json.load(json_file)

    def keep_doing_something(self, action: str, seconds: int):
        if action == "building":
            btn = "building_buy_all"
            pyautogui.click(
                x=self.calibration["building_tab"][0][0],
                y=self.calibration["building_tab"][0][1],
            )
        elif action == "research":
            btn = "research_buy_all"
            pyautogui.click(
                x=self.calibration["research_tab"][0][0],
                y=self.calibration["research_tab"][0][1],
            )
        elif action == "clicking":
            btn = "vaga_lume_center"
        else:
            return

        start = time.time()
        while time.time() - start < seconds:
            if keyboard.is_pressed("p"):  # if key 'p' is pressed
                print("Bot stopped, press R to resume")
                keyboard.wait("r")
                print("Bot resumed")
            pyautogui.click(
                x=self.calibration[btn][0][0],
                y=self.calibration[btn][0][1],
            )
            time.sleep(0.1)

    def ascend(self):
        time.sleep(1)
        pyautogui.click(
            x=self.calibration["elixir_tab"][0][0],
            y=self.calibration["elixir_tab"][0][1],
        )
        time.sleep(1)
        pyautogui.click(
            x=self.calibration["elixir_ascend"][0][0],
            y=self.calibration["elixir_ascend"][0][1],
        )
        time.sleep(1)
        pyautogui.click(
            x=self.calibration["elixir_ascend_confirmation"][0][0],
            y=self.calibration["elixir_ascend_confirmation"][0][1],
        )

    def start_bot(self):
        print("Press Ctrl-C to quit.")
        print("Hold P to pause.")
        print("Hold I to get info.")

        try:
            while True:
                start = time.time()
                time.sleep(0.5)
                while time.time() - start < COOLDOWN_BEFORE_ASCENDING:
                    print(time.time() - start)
                    if keyboard.is_pressed("p"):  # if key 'p' is pressed
                        print("Bot stopped, press R to resume")
                        keyboard.wait("r")
                        print("Bot resumed")
                    time.sleep(0.5)
                    self.keep_doing_something("building", 5)
                    time.sleep(0.5)
                    self.keep_doing_something("research", 5)

                    rgb = get_color(
                        self.calibration["is_energy_enabled"][0][0],
                        self.calibration["is_energy_enabled"][0][1],
                    )
                    r = rgb[0]
                    while r != 226:
                        self.keep_doing_something("clicking", 5)
                        rgb = get_color(
                            self.calibration["is_energy_enabled"][0][0],
                            self.calibration["is_energy_enabled"][0][1],
                        )
                        r = rgb[0]

                # Ascend
                self.ascend()
        except KeyboardInterrupt:
            print("\n")
            print("Exiting...")
