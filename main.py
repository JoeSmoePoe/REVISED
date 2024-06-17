import ctypes
import easyocr
import re
import time
import threading
import pydirectinput
import keyboard
import cv2
import json
import os

from PIL import Image, ImageGrab

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
if (screensize != (1920, 1080)):
    print("\n\n[X] Error! Script is only compatible with 1920x1080 resolution.\n\n")
else:
    print("\n\n[+] Passed resolution check. " + str(screensize) + "\n\n")

print("[/] Initializing EasyOCR...")
reader = easyocr.Reader(['en'])
print("[+] Initializing EasyOCR successful!")

try:
    config_file = open("config.json")
except:
    print("[X] Error! config.json not found!")
    exit()

config = json.load(config_file)

MINIMUM_CHESTS = config["minimum_chests"]
DELAY = config["delay"]
KEYBIND = config["keybind"]

print("\n[+] Config loaded!\n\n" + str(config) + "\n\n")

running = True

def getChests(quest_number):
    match quest_number:
        case 1:
            quest1_screenshot = ImageGrab.grab(bbox=(900, 352, 1089, 410), include_layered_windows=False, all_screens=False)
            quest1_screenshot.save('quest1.png')

            image = cv2.imread("quest1.png")
            normalized_image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
            gray = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255,
                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            cv2.imwrite("quest1.png", thresh)

            try:
                OCR_result = reader.readtext('quest1.png', detail = 0, width_ths = 1, text_threshold = 0.6)
                print("[+] Successfully read quest 1 content: " + str(OCR_result))

                filtered = [re.search(r'\d+', item).group() for item in OCR_result if "Chest" in item]
                print("[+] Successfully filtered quest content")
            except:
                print("[X] Error! OCR #1")
                filtered = []

            if (filtered == []):
                filtered = ["0"]

            print("\n[!] " + str(filtered[0]) + " chests found in quest 1\n")

            return filtered
        case 2:
            quest2_screenshot = ImageGrab.grab(bbox=(900, 450, 1089, 508), include_layered_windows=False, all_screens=False)
            quest2_screenshot.save('quest2.png')

            image = cv2.imread("quest2.png")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255,
                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cv2.imwrite("quest2.png", thresh)

            try:
                OCR_result = reader.readtext('quest2.png', detail = 0, width_ths = 1, text_threshold = 0.6)
                print("[+] Successfully read quest 2 content: " + str(OCR_result))

                filtered = [re.search(r'\d+', item).group() for item in OCR_result if "Chest" in item]
                print("[+] Successfully filtered quest content")
            except:
                print("[X] Error! OCR #2")
                filtered = []

            if (filtered == []):
                filtered = ["0"]

            print("\n[!] " + str(filtered[0]) + " chests found in quest 2\n")

            return filtered

        case 3:
            quest3_screenshot = ImageGrab.grab(bbox=(900, 546, 1089, 606), include_layered_windows=False, all_screens=False)
            quest3_screenshot.save('quest3.png')

            image = cv2.imread("quest3.png")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255,
                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cv2.imwrite("quest3.png", thresh)

            try:
                OCR_result = reader.readtext('quest3.png', detail = 0, width_ths = 1, text_threshold = 0.6)
                print("[+] Successfully read quest 3 content: " + str(OCR_result))

                filtered = [re.search(r'\d+', item).group() for item in OCR_result if "Chest" in item]
                print("[+] Successfully filtered quest content")
            except:
                print("[X] Error! OCR #3")
                filtered = []

            if (filtered == []):
                filtered = ["0"]

            print("\n[!] " + str(filtered[0]) + " chests found in quest 3\n")

            return filtered


        case _:
            return
        
def reroll(quest_number):
    match quest_number:
        case 1:
            pydirectinput.moveTo(800, 395)
            pydirectinput.moveTo(801, 396)
            pydirectinput.click()

            print("[+] Successfully rerolled chest 1")
            return
        case 2:
            pydirectinput.moveTo(800, 495)
            pydirectinput.moveTo(801, 496)
            pydirectinput.click()

            print("[+] Successfully rerolled chest 2")
            return
        case 3:
            pydirectinput.moveTo(800, 595)
            pydirectinput.moveTo(801, 596)
            pydirectinput.click()

            print("[+] Successfully rerolled chest 3")
            return

def main():
    print("[+] Script loaded!\n > Press " + KEYBIND + " to start rerolling.\n > Press END to exit.")
    while running:
        time.sleep(0.001)
        if (keyboard.is_pressed("END")): break

        if (keyboard.is_pressed(KEYBIND)):
            time.sleep(0.2)

            while (int(getChests(1)[0]) < MINIMUM_CHESTS and running):
                time.sleep(DELAY)
                reroll(1)

            while (int(getChests(2)[0]) < MINIMUM_CHESTS and running):
                time.sleep(DELAY)
                reroll(2)

            while (int(getChests(3)[0]) < MINIMUM_CHESTS and running):
                time.sleep(DELAY)
                reroll(3)

def killswitch():
    global running

    keyboard.wait('END')
    print("\n\n[!] Exiting...")
    
    os.remove("quest1.png")
    os.remove("quest2.png")
    os.remove("quest3.png")
    os._exit(0)

time.sleep(1)
os.system("cls")
print("\n\n > niepogoda's reroll script < \n\n")

main_thread = threading.Thread(target=main)
main_thread.start()

killswitch()