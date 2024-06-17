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

# Ensure 1920x1080 resolution
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
if screensize != (1920, 1080):
    print("Error: Script is only compatible with 1920x1080 resolution.")
    print("Please adjust your screen resolution to 1920x1080 to use this script.")
    exit()
else:
    print("Passed resolution check: {}".format(screensize))

print("[/] Initializing EasyOCR...")
print("This may take a few seconds...")
reader = easyocr.Reader(['en'])
print("[+] Initializing EasyOCR successful!")

# Load config
try:
    config_file = open("config.json")
except:
    print("[X] Error! config.json not found!")
    print("Please download config.json file and place it in the script's directory.")
    exit()

config = json.load(config_file)
config_file.close()

MINIMUM_CHESTS = config["minimum_chests"]
DELAY = config["delay"]
START_KEYBIND = config["start_keybind"]
KILL_KEYBIND = config["kill_keybind"]
MINIMUM_ENEMIES = config["minimum_enemies"]

print("\n[+] Config loaded!\n\n" + str(config) + "\n\n")

running = True

def getQuests(quest_number):
    print(f"[+] Checking enemies for quest {quest_number}...")
    bbox = {
        1: (900, 352, 1089, 410), # may or may not be the correct imagebox position <3
        2: (900, 450, 1089, 508), # may or may not be the correct imagebox position <3
        3: (900, 546, 1089, 606) # may or may not be the correct imagebox position <3
    }
    
    screenshot = ImageGrab.grab(bbox=bbox[quest_number], include_layered_windows=False, all_screens=False)
    screenshot.save(f'quest{quest_number}.png')

    image = cv2.imread(f'quest{quest_number}.png')
    normalized_image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    gray = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cv2.imwrite(f'quest{quest_number}.png', thresh)

    try:
        OCR_result = reader.readtext(f'quest{quest_number}.png', detail=0, width_ths=1, text_threshold=0.6)
        print(f"[+] Successfully read quest {quest_number} content: {OCR_result}")

        filtered = [re.search(r'\d+', item).group() for item in OCR_result if "Enemies" in item]
    except:
        print(f"[X] Error! OCR {quest_number}")
        filtered = []

    if not filtered:
        filtered = ["0"]

    print(f"\n[!] Found {filtered[0]} enemies in quest {quest_number}\n")

    return int(filtered[0]) >= MINIMUM_ENEMIES

def deleteQuest(quest_number):
    print(f"Deleting quest {quest_number}")
    cancel_positions = {
        1: (nil, nil),  # Replace with actual coordinates for cancel quest 1 cause im noob (totally not lazy :p)
        2: (nil, nil),  # Replace with actual coordinates for cancel quest 2 cause im noob (totally not lazy :p)
        3: (nil, nil)   # Replace with actual coordinates for cancel quest 3 cause im noob (totally not lazy :p)
    }
    pydirectinput.moveTo(*cancel_positions[quest_number])
    pydirectinput.click()
    print(f"[+] Quest {quest_number} deleted. Getting new quest.")
    pydirectinput.moveTo(1000, 500)  # Replace with actual coordinates for getting new quest cause im noob (totally not lazy :p)
    pydirectinput.click()
    time.sleep(1)  # Adjust sleep time as necessary
    return

def getChests(quest_number):
    bbox = {
        1: (900, 352, 1089, 410),
        2: (900, 450, 1089, 508),
        3: (900, 546, 1089, 606)
    }
    
    screenshot = ImageGrab.grab(bbox=bbox[quest_number], include_layered_windows=False, all_screens=False)
    screenshot.save(f'quest{quest_number}.png')

    image = cv2.imread(f'quest{quest_number}.png')
    normalized_image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    gray = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cv2.imwrite(f'quest{quest_number}.png', thresh)

    try:
        OCR_result = reader.readtext(f'quest{quest_number}.png', detail=0, width_ths=1, text_threshold=0.6)
        print(f"[+] Successfully read quest {quest_number} content: {OCR_result}")

        filtered = [re.search(r'\d+', item).group() for item in OCR_result if "Chest" in item]
    except:
        print(f"[X] Error! OCR {quest_number}")
        filtered = []

    if not filtered:
        filtered = ["0"]

    print(f"\n[!] Found {filtered[0]} chests in quest {quest_number}\n")

    return filtered

def reroll(quest_number):
    match quest_number:
        case 1:
            pydirectinput.moveTo(800, 395)
            pydirectinput.moveTo(801, 396)
            pydirectinput.click()
            print("[+] Rerolling chest 1...")
            print("[+] Waiting for chest 1 contents to refresh...")
            return
        case 2:
            pydirectinput.moveTo(800, 495)
            pydirectinput.moveTo(801, 496)
            pydirectinput.click()
            print("[+] Rerolling chest 2...")
            print("[+] Waiting for chest 2 contents to refresh...")
            return
        case 3:
            pydirectinput.moveTo(800, 595)
            pydirectinput.moveTo(801, 596)
            pydirectinput.click()
            print("[+] Rerolling chest 3...")
            print("[+] Waiting for chest 3 contents to refresh...")
            return

def main():
    print("[+] Script loaded!\n > Press " + START_KEYBIND + " to start the process.\n > Press " + KILL_KEYBIND + " to exit.")
    while running:
        time.sleep(0.001)
        if keyboard.is_pressed("END"):
            break

        if keyboard.is_pressed(START_KEYBIND):
            time.sleep(0.2)
            quests = [1, 2, 3]
            quest_enemies_met = {1: False, 2: False, 3: False}

            while not all(quest_enemies_met.values()) and running:
                for quest_num in quests:
                    if not quest_enemies_met[quest_num]:
                        if getQuests(quest_num):
                            quest_enemies_met[quest_num] = True
                            print(f"[+] Quest {quest_num} has the minimum enemies. Moving to the next quest if available.")
                        else:
                            deleteQuest(quest_num)

            for quest_num in quests:
                while int(getChests(quest_num)[0]) < MINIMUM_CHESTS and running:
                    time.sleep(DELAY)
                    reroll(quest_num)

def killswitch():
    global running
    keyboard.wait(KILL_KEYBIND)
    print("\n[+] Exiting...")
    try:
        os.remove("quest1.png")
        os.remove("quest2.png")
        os.remove("quest3.png")
    except:
        pass
    os._exit(0)

time.sleep(1)
os.system("cls")
print("\n\n > niepogoda's REVISED reroll & get quests script < \n\n")

main_thread = threading.Thread(target=main)
main_thread.daemon = True
main_thread.start()

killswitch()
