import pypboy
import settings
import game
import pygame
import time

class Module(pypboy.SubModule):

    label = "radio"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)

        self.topmenu = pypboy.ui.TopMenu()
        self.add(self.topmenu)
        self.topmenu.label = "RADIO"
        self.topmenu.title = settings.MODULE_TEXT

        # self.footer = pypboy.ui.Footer(settings.STATUS_FOOTER)
        self.footer = pypboy.ui.Footer([])
        self.add(self.footer)

        # For now, only the menu, no sounds ! Maybe waveform to suggest playback


        self.stations_array = ["Vault 33 Radio", "NCRR440", "GALAXY NEWS RADIO"]
        self.menu = RadioMenu(self.stations_array, 0)  
        self.add(self.menu)

        self.grid = Grid()
        self.add(self.grid)

# Based on youtube Pipboy visualizer from Prime Videos
class Grid(game.Entity):
    def __init__(self):
        super(Grid, self).__init__((542, 140))
        self.rect[0] = 130
        self.rect[1] = 280
        self.image.fill((0,0,0))

        grid_y_lines = 7
        grid_x_lines = 19
        short_lines = 28

        

        for i in range(grid_x_lines): 
            offset = 30
            if i == 18:
                pygame.draw.line(self.image, settings.light_color, (offset*i, 0), (offset*i, 140), 2)
            else:
                pygame.draw.line(self.image, settings.dark_color, (offset*i, 0), (offset*i, 140))
        
        for i in range(grid_y_lines):
            offset = 23
            if i == 3 or i == 6:
                pygame.draw.line(self.image, settings.light_color, (0, offset*i), (540, offset*i), 2)
            else:
                pygame.draw.line(self.image, settings.dark_color, (0, offset*i), (540, offset*i))
        
        offset_short_lines = 6
        for i in range(short_lines):
            long_line = 13
            short_line = 8
            if i % 2 == 0:
                pygame.draw.line(self.image, settings.light_color, (offset_short_lines, 140-long_line), (offset_short_lines, 140), 2)
            else:
                pygame.draw.line(self.image, settings.light_color, (offset_short_lines, 140-short_line), (offset_short_lines, 140), 2)
            offset_short_lines += 19
        
        # Baby rects in upper corners
        baby_rect = (5, 5, 8, 8)
        pygame.draw.rect(self.image, (settings.light_color), baby_rect)
        baby_rect = (540 - 8 - 5, 5, 8, 8)
        pygame.draw.rect(self.image, (settings.light_color), baby_rect)
        
     
     
class RadioMenu(game.Entity):
    def __init__(self, menu_array = [], selected = 0):
        super(RadioMenu, self).__init__((700, 300))
        self.rect[1] = 60
        self.rect[0] = 70

        self.source_array = menu_array

        self.index = 0
        self.prev_selection = 0

        self.imagebox = pygame.Surface((240,240))
        self.saved_selection = 0

        self.top_of_menu = 0
        self.max_items = 10

        # skip scrolling,

        # For the init
        self.selected = selected
        self.select(self.selected)

        if settings.SOUND_ENABLED:
            self.dial_move_sfx = pygame.mixer.Sound('sounds/pipboy/RotaryVertical/UI_PipBoy_RotaryVertical_01.ogg')
            self.dial_move_sfx.set_volume(settings.VOLUME)

    def select(self, item):
        if not settings.hide_main_menu:
            self.selected = item
            self.redraw()
            # if statement
    
    def handle_action(self, action):
        if not settings.hide_main_menu:
            if action == "dial_up":
                # print("Dial up")
                if self.selected > 0:
                    if settings.SOUND_ENABLED:
                        self.dial_move_sfx.play()
                    self.selected -= 1
                    self.select(self.selected)

            if action == "dial_down":
                # print("Dial down")
                if self.selected < len(self.source_array) - 1:
                    self.selected += 1
                    if settings.SOUND_ENABLED:
                        self.dial_move_sfx.play()
                    self.select(self.selected)

    def redraw(self):
        self.image.fill((0,0,0))
        offset = 5

        #  not needed? maybe for handle action? doesnt go offscreen? just use source_array
        self.menu_array = self.source_array[self.top_of_menu:(self.top_of_menu + self.max_items)]
        self.prev_selection = None

        for i in range(len(self.menu_array)):
            
            if self.selected > self.max_items-1:
                self.prev_selection = self.selected
                self.selected = self.selected - self.top_of_menu

            if i == self.selected:
                text = settings.FreeRobotoR[24].render(f" {self.menu_array[i]} ",  (settings.dark_color))
                # rectangle + pointer block
                selected_rect = (0, offset - 5, 300, text[0].get_size()[1] + 10)
                pygame.draw.rect(self.image, (settings.bright_color), selected_rect)
                selector_dot = (10, offset + 5, 8, 6)
                pygame.draw.rect(self.image, (settings.dark_color), selector_dot)
            else:
                text = settings.FreeRobotoR[24].render(f" {self.menu_array[i]} ",  (settings.bright_color))

            if self.prev_selection:
                self.selected = self.prev_selection
            
            self.image.blit(text[0], (20, offset))
            offset += text[0].get_size()[1] + 18
                
            

    def render(self, *args, **kwargs):
        if settings.hide_main_menu and settings.hide_main_menu != 3:
            settings.hide_main_menu = 3
            self.image.fill(settings.black_color)
            self.saved_selection = self.selected

        elif not settings.hide_main_menu:
            if self.saved_selection:
                self.select(self.saved_selection)
                self.saved_selection = None


