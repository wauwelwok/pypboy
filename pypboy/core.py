import settings
import game
import pygame
import pypboy.ui
import os

from pypboy.modules import data
from pypboy.modules import inv
from pypboy.modules import stats
from pypboy.modules import boot
from pypboy.modules import map
from pypboy.modules import radio


GPIO = False
if settings.GPIO_AVAILABLE:
    # import RPI.GPIO as GPIO
    from gpiozero import RotaryEncoder, Button
    GPIO = True

# Specialized game loop
class Pypboy(game.core.Engine):
    currentModule = 0
    prev_fps_time = 0

    def __init__(self, *args, **kwargs):
        super(Pypboy, self).__init__(*args, **kwargs)
        self.init_persitant()   #pass for now
        self.init_modules()     # pass for now
        if GPIO:
            self.init_gpio_controls()

        self.gpio_actions = {}

        self.prev_fps_time = 0

    
    def init_persitant(self):
        # add overlay?
        overlay = pypboy.ui.Overlay()
        self.root_persitant.add(overlay)
        # add scanlines
        # scanlines = pypboy.ui.Scanlines()
        # self.root_persitant.add(scanlines)
        pass

    def init_modules(self):
        self.modules = {"radio": None, "map": None, "data": None, "items": None, "stats": stats.Module(self), "boot": None, "passcode": None}
        self.modules = {
            "radio": radio.Module(self),
            "map": map.Module(self),
            "data": data.Module(self),
            "inv": inv.Module(self),
            "stats": stats.Module(self),
            "boot": boot.Module(self),
            # "passcode": passcode.Module(self)
        }
        self.switch_module(settings.STARTER_MODULE)  # Set the start screen
    

    def init_gpio_controls(self):
        self.rocker = Button(12)
        self.rotarSub = RotaryEncoder(5, 6)
        self.rotarSubBtn = Button(16)
        self.rotarMenu = RotaryEncoder(26, 19)
        self.rotarMenuBtn = Button(13)

        self.last_rotary_value_menu = 0
        self.last_rotary_value_sub = 0
        print("gpio made")
       
    
    def check_gpio_input(self):
        if self.rotarMenuBtn.is_pressed:
            self.running = False
        # if self.rotarSubBtn.is_pressed:
        #     self.handle_action("module_boot")
        if self.rocker.is_pressed:
            print("rocker")
            os.system("sudo shutdown -h now")

        current_value_rotorSub = self.rotarSub.steps
        current_value_rotorMenu = self.rotarMenu.steps
        
        if self.last_rotary_value_menu != current_value_rotorMenu:
            # Deze onderstaande current module logica in init zetten?
            # Heeft niks te maken met gpio input 
            current_module = settings.current_module
            module_set = ["stats", "inv", "data", "map", "radio", "boot"]
            index = module_set.index(current_module)
        # check index of current module
            if self.last_rotary_value_menu < current_value_rotorMenu:
                if index > 0:
                    index -= 1
                    self.handle_action(f"module_{module_set[index]}")
            elif self.last_rotary_value_menu > current_value_rotorMenu:
                if index < 5:
                    index += 1                
                    self.handle_action(f"module_{module_set[index]}")    
            self.last_rotary_value_menu = current_value_rotorMenu

        if self.last_rotary_value_sub != current_value_rotorSub:
            current_module = settings.current_module
            if current_module == "radio":
                if self.last_rotary_value_sub > current_value_rotorSub:
                    self.active.handle_action("dial_up")
               
                else:
                    self.active.handle_action("dial_down")
            if current_module == "map":
                if self.last_rotary_value_sub > current_value_rotorSub:
                    self.active.handle_action("zoom_out")
              
                else:
                    self.active.handle_action("zoom_in")
            if current_module == "inv":
                pass
            self.last_rotary_value_sub = current_value_rotorSub
  

    def switch_module(self, module):
        # if not settings.hide_top_menu:
        if module in self.modules:
            if hasattr(self, "active"):
                self.active.handle_action("pause")
                self.remove(self.active)
            self.active = self.modules[module]
            self.active.parent = self
            self.active.handle_action("resume")
            self.add(self.active)
            settings.current_module = module
        else:
            print("Module '%s' not implemented." % module)
    
    def handle_action(self, action):
        if action.startswith('module_'):
            self.switch_module(action[7:])
            
        else:
            if hasattr(self, 'active'):
                
                self.active.handle_action(action)
                
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:  # Some key has been pressed
            # Persistent Events:
            if event.key == pygame.K_ESCAPE:  # ESC
                self.running = False

            else:
                if event.key in settings.ACTIONS:  # Check action based on key in settings
                    self.handle_action(settings.ACTIONS[event.key])
                    

        elif event.type == pygame.QUIT:
            self.running = False
     
        else:
            if hasattr(self, 'active'):
                self.active.handle_event(event)
  
    def run(self):
        self.running = True
        while self.running:
            if GPIO:
                self.check_gpio_input()
            for event in pygame.event.get():
                self.handle_event(event)
                if hasattr(self, 'active'):
                    self.active.handle_event(event)

            # slow code debugger
            # debug_time = time.time()
            self.render()
        
            #
            # time_past = time.time() - debug_time
            # if time_past:
            #     max_fps = int(1 / time_past)
            #     print("self.render took:", time_past, "max fps:", max_fps)

        try:
            pygame.mixer.quit()
        except Exception as e:
            print(e)