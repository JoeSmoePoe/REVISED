# niepogoda's Reroll Script

About
-----

A simple, intuitive, and powerful script for automating chest rerolls in ***Lee:// Rpg***!

Features
--------

### Automatic Chest Rerolling

Automatically reroll chests in your game until you meet the minimum threshold.

### Customizable Settings

Adjust the minimum chest threshold, delay between rerolls, and keybinds to suit your needs.

### Multi-Quest Support

Support for multiple quests/chests, so you can reroll all your three chests with ease.

### Easy to Use

Simple installation process and straightforward configuration.

Installation
-------------

### Works on Python 3.12.4 | If you encounter any issues, you can try Python 3.10.

### Step 1: Install Required Libraries

Run command:
`pip install -r requirements.txt`

You will want to install right torch version for your pc https://pytorch.org/get-started/locally/

### Step 2: Download the Script

Download the <a href="https://github.com/0e8/niepogodasreroll/releases/latest">latest release</a> of this script.

### Step 3: Configure the Script

Create a new file named <b>config.json</b> in the same directory as the script and add the following configuration:

<code>{
  "minimum_chests": 20,
  "delay": 1,
  "start_keybind": "F2",
  "kill_keybind": "F3"
}</code>

Replace the values with your desired settings.
<i>delay is used in seconds and you can use fractions</i>

You can use the `config.json.example` file as an template.

### Step 4: Run the Script

Run the script using Python, e.g., <code>py main.py</code>

Getting Started
---------------

1. Open quests menu, and add 3 *preferably* the same quests
2. Press the start keybind (F2 by default) to start the script.
3. The script will automatically reroll chests until the minimum chest threshold is met.
4. Press the kill keybind (F3 by default) to exit the script.

Troubleshooting
----------------

Make sure you've installed all required libraries and configured the config.json file correctly.
If you encounter any issues with OCR, try adjusting the OCR settings in the script or increasing the delay between rerolls.
If you encounter any other issues, feel free to open an issue on GitHub.

License
-------

This script is licensed under the MIT License. You are free to use, modify, and distribute it as you see fit.

Acknowledgments
--------------

Thanks to **_tootle** for early testing this script!<br>
Thanks to **lmmortalz** for contributing to this project!

I hope you enjoy using this script!
