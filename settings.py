import pygame
import pygame.freetype
import os
import datetime

# Set target frames per second
fps = 32
fps_rate = (1/fps)

# Screen size
WIDTH = 800
HEIGHT = 480
FULLSCREEN = False

# Set map module to offline
offline = True

# Date
years_in_future = 273
year = datetime.datetime.now().year + years_in_future
date = f"{datetime.datetime.now().strftime('%d-%m')}-{year}"
day = datetime.datetime.now().strftime("%A").upper()

# Sound 
VOLUME = 0.2

# Raspberry Pi detection
PI = False
if os.name == "posix":
    PI = True
else:
    PI = False
GPIO_AVAILABLE = False

# Init module, current_module for gpio logic
STARTER_MODULE = "inv"
current_module = ""

# array of health bar numbers; change when switch heads in stats animation
# list left up, left down, down, right down, right up of health values
health_array = [
    ["88", "94", "100", "99", "89"],    #1 Normal head
    ["75", "88", "80", "84", "70"],    #2 Sad head
    ["63", "71", "60", "83", "75"],    #3 Dog head
    ["9", "11", "10", "13", "15"],    #4 Skull head
    ["40", "55", "50", "57", "64"],    #5 Mummy head
    ["23", "34", "30", "21", "11"],    #6 Mummy tongue head
    ["2", "6", "1", "9", "7"]     #7 Skull Mummy head
]

# number of minutes to wait to change heads and health
wait_time_mins = 10

# Init fonts
pygame.freetype.init()
FreeRobotoB = {}
FreeRobotoR = {}
TechMono = {}
for x in range(10, 34):
    FreeRobotoB[x] = pygame.freetype.Font('fonts/RobotoCondensed-Bold.ttf', x)
    FreeRobotoR[x] = pygame.freetype.Font('fonts/RobotoCondensed-Regular.ttf', x)
    TechMono[x] = pygame.freetype.Font('fonts/TechMono.ttf', x)
FreeRobotoB_clock = pygame.freetype.Font('fonts/RobotoCondensed-Bold.ttf', 250)

# Deze in core.py oproepen ipv elke module
MODULE_TEXT = ["STAT", "INV", "DATA", "MAP", "RADIO"]

# COLORS
black_color = (0, 0, 0)
bright_color = (0, 230, 0)
light_color = (0, 170, 0)
mid_color = (0, 120, 0)
dim_color = (0, 70, 0)
dark_color = (0, 40, 0)

# Needed for init
hide_top_menu = False
hide_submenu = False
hide_main_menu = False
hide_footer = False
hide_upper_footer = False

# Keyboard actions
ACTIONS = {
    pygame.K_F1: "module_stats",
    pygame.K_F2: "module_inv",
    pygame.K_F3: "module_data",
    pygame.K_F4: "module_map",
    pygame.K_F5: "module_radio",
    pygame.K_F6: "module_boot",
    pygame.K_F7: "module_passcode",
    pygame.K_1: "knob_1",
    pygame.K_2: "knob_2",
    pygame.K_3: "knob_3",
    pygame.K_4: "knob_4",
    pygame.K_5: "knob_5",
    pygame.K_UP: "dial_up",
    pygame.K_DOWN: "dial_down",
    pygame.K_PLUS: "zoom_in",
    pygame.K_EQUALS: "zoom_in",
    pygame.K_MINUS: "zoom_out",
    pygame.K_KP_PLUS: "zoom_in",
    pygame.K_KP_MINUS: "zoom_out",
}

#map
# Open Strett Map settings ? shouldn't need this
WORLD_MAP_FOCUS = 0.07  # Needed to handle the 50k node limit from OSM

# Google maps:
MAP_FOCUS = (-71.0594587, 42.3614408)  # Boston MA
MAP_TYPE = "hybrid"  # Select Hybrid if you want labels and roads, satellite if you want imagry only
MAP_STYLE = "feature:all|geometry.stroke|labels.text.stroke"
WORLD_MAP_ZOOM = 12
LOCAL_MAP_ZOOM = 15
LOAD_CACHED_MAP = False
