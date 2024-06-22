import pypboy
import settings
import game
import pygame

class Module(pypboy.SubModule):
    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)

        self.label = "ATTACHMENT"
        self.images = []

        self.topmenu = pypboy.ui.TopMenu()
        self.add(self.topmenu)
        self.topmenu.label = "INV"
        self.topmenu.title = settings.MODULE_TEXT

        self.inv_array = ["EXT TERMINAL", "RAD METER", "FLASHLIGHT"]
        self.menu = InvMenu(self.inv_array, 0)  
        self.add(self.menu)

        self.footer = pypboy.ui.Footer(["PB-NRML", "ITEMS ATCHD", "INVENTORY"])
        self.add(self.footer)

        self.upperfooter = pypboy.ui.UpperFooter(["MODE", "FAV", "SORT"])
        self.add(self.upperfooter)


class InvMenu(game.Entity):
    def __init__(self, menu_array = [], selected = 0):
        super(InvMenu, self).__init__((700, 300))
        self.rect[1] = 70
        self.rect[0] = 40

        self.source_array = menu_array

        self.index = 0
        self.prev_selection = 0

        self.imagebox = pygame.Surface((240,240))
        self.saved_selection = 0

        self.top_of_menu = 0
        self.max_items = 10

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
        offset = 20

        #  not needed? maybe for handle action? doesnt go offscreen? just use source_array
        self.menu_array = self.source_array[self.top_of_menu:(self.top_of_menu + self.max_items)]
        self.prev_selection = None

        for i in range(len(self.menu_array)):

            text = settings.FreeRobotoB[33].render(f" {self.menu_array[i]} ",  (settings.bright_color))
            
            if self.selected > self.max_items-1:
                self.prev_selection = self.selected
                self.selected = self.selected - self.top_of_menu

            if i == self.selected:
                # pointer animation with wait? from "empty" to "filled"
                selected_rect = (0, offset - 15, 350, text[0].get_size()[1] + 32)
                pygame.draw.rect(self.image, (settings.bright_color), selected_rect, 3)
                selector_dot = (35, offset + 5, 14, 14)
                pygame.draw.rect(self.image, (settings.bright_color), selector_dot, 2)
                
            
            if self.prev_selection:
                self.selected = self.prev_selection
            
            self.image.blit(text[0], (50, offset))
            offset += text[0].get_size()[1] + 36
                
            

    def render(self, *args, **kwargs):
        if settings.hide_main_menu and settings.hide_main_menu != 3:
            settings.hide_main_menu = 3
            self.image.fill(settings.black_color)
            self.saved_selection = self.selected

        elif not settings.hide_main_menu:
            if self.saved_selection:
                self.select(self.saved_selection)
                self.saved_selection = None
