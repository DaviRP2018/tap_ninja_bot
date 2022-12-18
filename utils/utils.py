import json
import time
from ctypes import windll

import keyboard
import pyautogui


def show_color():
    """Show color where pointer is"""
    print('Press Ctrl-C to quit.')
    dc = windll.user32.GetDC(0)
    try:
        while True:
            x, y = pyautogui.position()
            rgb = windll.gdi32.GetPixel(dc, x, y)
            r = rgb & 0xff
            g = (rgb >> 8) & 0xff
            b = (rgb >> 16) & 0xff
            color = "{} {} {}".format(r, g, b)
            print(color, end='')
            print('\b' * len(color), end='', flush=True)
    except KeyboardInterrupt:
        return


def show_position():
    """Show position where pointer is"""
    print('Press Ctrl-C to quit.')
    try:
        while True:
            x, y = pyautogui.position()
            position_str = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(position_str, end='')
            print('\b' * len(position_str), end='', flush=True)
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

        calibration["is_energy_enabled"] = set_calibrate_value("Pick the energy enabled yellow border")
        calibration["vaga_lume_center"] = set_calibrate_value("Press 'F' when the vaga-lume is in the center")

        # Buildings
        calibration["building_tab"] = set_calibrate_value("Press 'F' on building tab")
        calibration["building_buy_all"] = set_calibrate_value("Press 'F' on buy all button")

        # Research
        calibration["research_tab"] = set_calibrate_value("Press 'F' on research tab")
        calibration["research_buy_all"] = set_calibrate_value("Press 'F' on buy all button")

        # Elixir
        calibration["elixir_tab"] = set_calibrate_value("Press 'F' on elixir tab")
        calibration["elixir_ascend"] = set_calibrate_value("Press 'F' on ascension button")
        calibration["elixir_ascend_confirmation"] = set_calibrate_value("Press 'F' on ascension confirmation button")

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

#
# def upgrade_all():
#     scroll_hero_up_maximum()
#     time.sleep(1 / 2)
#     scroll_hero_down_maximum()
#     time.sleep(1 / 2)
#     # Check if button is where it is supposed to be
#     with open("settings/positions.json") as f:
#         positions = json.load(f)
#         with open("settings/calibration.json") as json_file:
#             colors = json.load(json_file)
#             if (
#                     get_color(
#                         positions["hero_buy_all_upgrades"][0],
#                         positions["hero_buy_all_upgrades"][1],
#                     )
#                     == colors["hero_buy_all_upgrades"]
#             ):
#                 pyautogui.click(
#                     positions["hero_buy_all_upgrades"][0],
#                     positions["hero_buy_all_upgrades"][1],
#                 )
#             else:
#                 time.sleep(5)
#                 upgrade_all()
#
#
# def hire_all_relevant_heroes():
#     with open("settings/positions.json") as json_file:
#         positions = json.load(json_file)
#     relevant_heroes_pos_with_scrolls = [
#         positions["hero_cid"],
#         positions["hero_treebeast"],
#         positions["hero_ivan"],
#         positions["hero_brittany"],
#         positions["hero_fisherman"],
#         positions["hero_betty"],
#         positions["hero_samurai"],
#         positions["hero_leon"],
#         positions["hero_seer"],
#         positions["hero_alexa"],
#         positions["hero_natalia"],
#         positions["hero_mercedes"],
#         positions["hero_bobby"],
#         positions["hero_broyle"],
#         positions["hero_george"],
#         positions["hero_midas"],
#         positions["hero_referigerator"],
#         positions["hero_abaddon"],
#         positions["hero_mazhu"],
#         positions["hero_amenhotep"],
#         positions["hero_beastlord"],
#         positions["hero_athena"],
#         positions["hero_aphrodite"],
#         positions["hero_shinatobe"],
#         positions["hero_grant"],
#         positions["hero_frostleaf"],
#     ]
#     scroll_hero_up_maximum()
#     time.sleep(1 / 2)
#     # change to hire MAX
#     for i in range(0, 4):
#         pyautogui.press("t")
#         time.sleep(1 / 2)
#     for item in relevant_heroes_pos_with_scrolls:
#         if isinstance(item, int):
#             for i in range(0, item):
#                 scroll_hero_down()
#                 time.sleep(1 / 2)
#         else:
#             pyautogui.click(item[0], item[1])
#             time.sleep(1 / 2)
#     pyautogui.press("t")
#
#
# def reset_auto_clickers():
#     pyautogui.keyDown("c")
#     time.sleep(1 / 2)
#     with open("settings/positions.json") as json_file:
#         positions = json.load(json_file)
#         pyautogui.click(positions["auto_clicker"][0], positions["auto_clicker"][1])
#     time.sleep(1 / 2)
#     pyautogui.keyDown("c")
#
#
# def set_auto_clickers_to_damage():
#     pyautogui.keyDown("c")
#     with open("settings/positions.json") as json_file:
#         positions = json.load(json_file)
#         for i in range(1, NUMBER_OF_AUTO_CLICKERS):
#             pyautogui.click(positions["gold_pickup"][2], positions["gold_pickup"][0])
#             time.sleep(1)
#     pyautogui.keyUp("c")
#
#
# def set_auto_clicker_hire_hero(hero_pos):
#     pyautogui.keyDown("c")
#     time.sleep(1 / 2)
#     pyautogui.click(hero_pos[0], hero_pos[1])
#     time.sleep(1 / 2)
#     pyautogui.keyDown("c")
