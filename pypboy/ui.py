import game
import pygame
import settings
import time
import os

class Scanlines(game.core.Entity):
    def __init__(self):
        super(Scanlines, self).__init__((720, 129))
        self.image = pygame.image.load('images/scanline.png').convert_alpha()
        self.rectimage = self.image.get_rect()
        self.rect[0] = 40
        self.rect[1] = 0
        self.top = -130
        self.speed = 10
        self.clock = pygame.time.Clock()
        self.animation_time = 0.05
        self.prev_time = 0
        self.dirty = 2

    def render(self, *args, **kwargs):
        self.current_time = time.time()
        self.delta_time = self.current_time - self.prev_time

        if self.delta_time >= self.animation_time:
            self.prev_time = self.current_time
            self.top = self.top + self.speed
            if self.top >= settings.HEIGHT + 130:
                self.top = -130
            self.rect[1] = self.top
        super(Scanlines, self).render(self, *args, **kwargs)
    

class TopMenu(game.Entity):
    def __init__(self, label = None, title = []):
        self.label = None
        self.prev_label = 0
        self.title = []

        super(TopMenu, self).__init__((settings.WIDTH, 40))
        self.rect[1] = 5
        self.saved_label = None 
    
    def render(self):
       
        if settings.hide_top_menu and settings.hide_top_menu != 3:
            self.image.fill(settings.black_color)
            settings.hide_top_menu = 3
            if self.label:
                self.saved_label = self.label
                self.prev_label = None
                self.label = None
        
        elif not settings.hide_top_menu:
            if self.saved_label:
                self.label = self.saved_label
                self.saved_label = None
            
            spacing = 40 
            prev_text_width = 74 #STAT width
            text_pos = 184 - spacing - prev_text_width #Set first location 
            if self.label:
                if self.label != self.prev_label:
                    self.image.fill((settings.black_color)) ## Clear text
                    # self.image.fill(settings.mid_color)

                    for section in self.title:
                        text = settings.FreeRobotoB[28].render(section, settings.bright_color, settings.black_color)
                        text_pos = text_pos + prev_text_width + spacing
                        self.image.blit(text[0], (text_pos, 10))
                        text_rect = text[0].get_rect()
                        prev_text_width = text_rect.width

                        if section == self.label:
                            pygame.draw.line(self.image, settings.bright_color, (40, 35), (text_pos - 11, 35),
                                             2)  # Line from left edge of screen
                            pygame.draw.line(self.image, settings.bright_color, (text_pos + text_rect.width + 10, 35),
                                             (settings.WIDTH-40, 35), 2)  # Line to the right edge of screen
                            pygame.draw.line(self.image, settings.bright_color, (text_pos - 12, 16), (text_pos - 12, 35),
                                             2)  # Left Vert bar
                            pygame.draw.line(self.image, settings.bright_color, (text_pos - 12, 16), (text_pos - 3, 16),
                                             2)  # Left Short bar
                            pygame.draw.line(self.image, settings.bright_color, (text_pos + text_rect.width + 2, 16),
                                             (text_pos + text_rect.width + 11, 16), 2)  # Right Short bar
                            pygame.draw.line(self.image, settings.bright_color, (text_pos + text_rect.width + 10, 16),
                                             (text_pos + text_rect.width + 10, 35), 2)  # Right Vert bar
                        else:
                            pygame.draw.line(self.image, settings.bright_color, (text_pos - 10, 35),
                                             (text_pos + text_rect.width + 10, 35),
                                             2)  # Horizontal Barclass TopMenu(game.Entity):
                self.prev_label = self.label
        

class SubMenu(game.Entity):

    def __init__(self):
        super(SubMenu, self).__init__((settings.WIDTH, 36))
        self.menu = []
        self.rect[0] = 130
        self.rect[1] = 46
        self.prev_time = 0
        self.selected = None
        self.saved_module = None

    def render(self):
        if settings.hide_submenu and settings.hide_submenu != 3:
            settings.hide_submenu = 3
            self.image.fill(settings.black_color)
            self.saved_module = self.selected
        elif not settings.hide_submenu and self.saved_module:
            self.select(self.saved_module)
            self.saved_module = None


    def select(self, module):
        self.selected = module
        self.image.fill(settings.black_color)
        self.textoffset = 18
        

        if not settings.hide_submenu:
            for m in self.menu:
                padding = 3
                text_width = 0
                while text_width < 54:
                    spaces = " ".join([" " for x in range(padding)])
                    text = settings.FreeRobotoR[25].render("%s%s%s" % (spaces, m, spaces), settings.mid_color, (0, 0, 0))
                    text_width = text[0].get_width()
                    padding += 3
                

                if m == self.selected:
                    text = settings.FreeRobotoR[25].render("%s%s%s" % (spaces, m, spaces), settings.bright_color, (0, 0, 0))
                self.image.blit(text[0], (self.textoffset, 0))
                self.textoffset = self.textoffset + text_width


class Footer(game.Entity):
    def __init__(self, sections=[]):
        super(Footer, self).__init__((720, 30))
        self.sections = sections
        self.padding = 12
        self.text_width = 0
        self.line_1 = None
        self.rect[0] = 40
        self.rect[1] = 450
             

    def render(self):
        if settings.hide_footer and settings.hide_footer != 3:
            self.image.fill(settings.black_color)
            settings.hide_footer = 3
        elif not settings.hide_footer:
            self.image.fill(settings.dark_color)
            self.pos = 48
            powerbar_left = 0
          
            for section in self.sections:
                
                text = settings.FreeRobotoB[25].render(section, settings.bright_color)
                text_length = text[0].get_rect().width

                if section != self.sections[-1]:
                    self.image.blit(text[0], (self.pos, 7))
                    self.pos = self.pos + text_length + self.padding
                    if section == "POWER":
                        powerbar_left = self.pos 

                    if section == self.sections[0]:
                        pygame.draw.line(self.image, (0, 0, 0), (self.pos, 0), (self.pos, 30), 4)
                        self.pos += self.padding
                      
                else:
                    # No text on right side
                    if section == "":
                        break 
                    text_rect = text[0].get_rect()
                    text_rect.right = 720 - (self.padding * 2)
                    text_rect.top = 7
                    self.pos = 720 - text_length - (self.padding * 3)   

                    # Inv, Local and world map has different bg color    
                    if section=="INVENTORY" or section == "LOCAL MAP" or section == "WORLD MAP":
                        pygame.draw.rect(self.image, settings.mid_color, (self.pos, 0, 720 - 20, 30))
                        pass
                    self.image.blit(text[0], text_rect)
                    pygame.draw.line(self.image, (0, 0, 0), (self.pos, 0), (self.pos, 30), 4)
               

                if powerbar_left > 0:
                    powerbar_right = self.pos - self.padding - powerbar_left
                    pygame.draw.rect(self.image, settings.bright_color, (powerbar_left, 9, powerbar_right, 15), 1)
                    pygame.draw.rect(self.image, settings.bright_color, (powerbar_left, 9, powerbar_right - 20, 15))
     

class UpperFooter(game.Entity):
    def __init__(self, sections = []):
        super(UpperFooter, self).__init__((380, 26))
        self.sections = sections
        self.rect[0] = 40
        self.rect[1] = 420
        self.padding = 12

    def render(self):
        self.pos = 48
        if settings.hide_upper_footer and settings.hide_upper_footer != 3:
            self.image.fill(settings.black_color)
            settings.hide_upper_footer = 3
        elif not settings.hide_upper_footer:
            self.image.fill(settings.mid_color)
        
        for section in self.sections:
            text = settings.FreeRobotoR[25].render(section, settings.dark_color)
            text_length = text[0].get_rect().width
    
            self.image.blit(text[0], (self.pos, 5))
            self.pos = self.pos + text_length + self.padding
            
            if section == self.sections[-1]:
                pygame.draw.rect(self.image, settings.black_color, (self.pos, 0, 380, 26))
                
            else:
                pygame.draw.line(self.image, (0, 0, 0), (self.pos, 0), (self.pos, 30), 6)
                self.pos += self.padding
                
        
class Overlay(game.Entity):
    def __init__(self):
        super(Overlay, self).__init__()
        self.image = pygame.surface.Surface((settings.WIDTH, settings.HEIGHT))
        self.overlay = pygame.image.load('images/overlay.png').convert_alpha()
        # Center overlay because png is 720x720
        self.image.blit(self.overlay, (40, 0))
        self.rect = self.image.get_rect()
        

# Menu_array Structure: [["Menu item",Quantity,"Image (or folder for animation")","Description text","Stat Text","Stat Number"],],
# Probably not the correct way to do this.
# class Menu(game.Entity):

#     def __init__(self, menu_array=[], callbacks=[], selected=0):
#         super(Menu, self).__init__((settings.WIDTH - settings.menu_x, 490))
#         self.source_array = menu_array

#         self.prev_time = 0
#         self.prev_fps_time = 0
#         self.clock = pygame.time.Clock()
#         self.animation_time = 0.2
#         self.index = 0
#         self.top_of_menu = 0
#         self.max_items = 10
#         self.menu_array = self.source_array[self.top_of_menu:self.max_items]  # List the array for display
#         self.prev_selection = 0

#         self.descriptionbox = pygame.Surface((360, 300))
#         self.imagebox = pygame.Surface((240, 240))

#         self.saved_selection = 0

#         try:
#             self.callbacks = callbacks
#             # print("self.callbacks = ", self.callbacks)
#         except:
#             self.callbacks = []

#         # self.arrow_img_up = load_svg("./images/inventory/arrow.svg", 26, 26)
#         # self.arrow_img_down = pygame.transform.flip(self.arrow_img_up, False, True)

#         self.selected = selected
#         self.select(self.selected)

#         if settings.SOUND_ENABLED:
#             self.dial_move_sfx = pygame.mixer.Sound('sounds/pipboy/RotaryVertical/UI_PipBoy_RotaryVertical_01.ogg')
#             self.dial_move_sfx.set_volume(settings.VOLUME)

#     def select(self, item):
#         if not settings.hide_main_menu:
#             self.selected = item
#             self.redraw()
#             if len(self.callbacks) > item and self.callbacks[item]:
#                 self.callbacks[item]()

#     def handle_action(self, action):
#         if not settings.hide_main_menu:
#             if action == "dial_up":
#                 # print("Dial up")
#                 if self.selected > 0:
#                     if settings.SOUND_ENABLED:
#                         self.dial_move_sfx.play()
#                     self.selected -= 1
#                     self.select(self.selected)

#             if action == "dial_down":
#                 # print("Dial down")
#                 if self.selected < len(self.source_array) - 1:
#                     self.selected += 1
#                     if settings.SOUND_ENABLED:
#                         self.dial_move_sfx.play()
#                     self.select(self.selected)

#     def redraw(self):
#         self.image.fill((0, 0, 0))
#         offset = 38

#         # print("Selected - ",self.selected)
#         if self.selected > self.max_items - 1:
#             self.top_of_menu = self.selected - self.max_items + 1
#             self.menu_array = self.source_array[
#                               self.top_of_menu:(self.top_of_menu + self.max_items)]  # List the array for display
#             # print("Selection off screen")
#         else:
#             self.top_of_menu = 0
#             self.menu_array = self.source_array[
#                               self.top_of_menu:(self.top_of_menu + self.max_items)]  # List the array for display
#             self.prev_selection = None
#         # print("top of menu = ", self.top_of_menu)

#         for i in range(len(self.menu_array)):
#             if self.selected > self.max_items - 1:
#                 self.prev_selection = self.selected
#                 self.selected = self.selected - self.top_of_menu

#             if i == self.selected:
#                 # print("Selected Index = ", i)
#                 text = settings.FreeRobotoB[30].render(" %s " % self.menu_array[i][0], (0, 0, 0),
#                                                    (settings.bright_color))
#                 try:
#                     number = settings.FreeRobotoB[30].render(" %s " % self.menu_array[i][1], (0, 0, 0),
#                                                          (settings.bright_color))
#                 except:
#                     number = ""

#                 selected_rect = (0, offset, settings.menu_x + 330, text[0].get_size()[1])
#                 pygame.draw.rect(self.image, (settings.bright_color), selected_rect)

#                 self.images = []
#                 try:  # Try loading a image if there is one
#                     self.image_url = self.menu_array[i][2]
#                     if os.path.isdir(self.image_url):
#                         for filename in sorted(os.listdir(self.image_url)):
#                             if filename.endswith(".png"):
#                                 filename = self.image_url + "/" + filename
#                                 self.images.append(pygame.image.load(filename).convert_alpha())
#                                 self.frameorder = []
#                                 # print(filename)
#                             if filename.endswith(".svg"):
#                                 pass
#                                 # svg_surface = load_svg(self.image_url + "/" + filename, self.imagebox.get_width(),
#                                 #                        self.imagebox.get_height())
#                                 # self.images.append(svg_surface)
#                                 # self.frameorder = []
#                                 # print(filename)
#                             if filename == "frameorder.py":
                                
#                                 pass
#                                 # url = self.image_url + "/" + filename
#                                 # # print ("url =",url)
                               
#                                 # #  fil == Load + initialized module implemented as py source file; return its module object

#                                 # file = imp.load_source("frameorder.py",
#                                 #                        os.path.join(self.image_url, "frameorder.py"))
#                                 # self.frameorder = file.frameorder
#                                 # self.frame = 0

#                     else:
#                         pass
#                         # if self.image_url:
#                         #     self.frameorder = []
#                         #     # self.imagebox.fill(settings.black)
#                         #     if self.image_url.endswith(".svg"):
#                         #         graphic = load_svg(self.image_url, self.imagebox.get_width(),
#                         #                            self.imagebox.get_height())
#                         #         self.imagebox.blit(graphic, (0, 0))
#                         #         self.image.blit(self.imagebox, (400, 0))
#                         #     else:
#                         #         graphic = pygame.image.load(self.image_url).convert_alpha()
#                         #         self.image.blit(graphic, (0, 0))



#                 except:
#                     self.image_url = ""

#                 try:
#                     description = self.menu_array[i][3]
#                 except:
#                     description = ""

#                 # if description:
#                 #     self.descriptionbox.fill((0, 0, 0))
#                 #     # description = settings.RobotoB[24].render(self.description[i], True, (settings.bright), (0, 0, 0))
#                 #     word_wrap(self.descriptionbox, description, settings.FreeRobotoR[20])
#                 #     self.image.blit(self.descriptionbox, (settings.description_box_x, settings.description_box_y))

#                 try:
#                     stats = self.menu_array[i][4]
#                 except:
#                     stats = ""

#                 if stats:
#                     stat_offset = 0
#                     self.descriptionbox.fill((0, 0, 0))
#                     for each in stats:
#                         stat_text = settings.FreeRobotoB[30].render(" %s " % each[0], (settings.bright_color),
#                                                                 (settings.dark_color))
#                         stat_number = settings.FreeRobotoB[30].render(" %s " % each[1],  (settings.bright_color),
#                                                                   (settings.dark_color))
#                         stat_rect = (0, stat_offset, 350, stat_text[0].get_size()[1])
#                         pygame.draw.rect(self.descriptionbox, (settings.dark_color), stat_rect)
#                         self.descriptionbox.blit(stat_text[0], (0, stat_offset))
#                         self.descriptionbox.blit(stat_number[0], (350 - stat_number[0].get_size()[0], stat_offset))
#                         stat_offset += stat_text[0].get_size()[1] + 6

#                     self.image.blit(self.descriptionbox, (settings.description_box_x, settings.description_box_y))

#             else:
#                 text = settings.FreeRobotoB[30].render(" %s " % self.menu_array[i][0], (settings.bright_color),
#                                                    (0, 0, 0))
#                 try:
#                     number = settings.FreeRobotoB[30].render(" %s " % self.menu_array[i][1], (settings.bright_color),
#                                                          (0, 0, 0))
#                 except:
#                     number = None

#             if self.prev_selection:
#                 self.selected = self.prev_selection

#             self.image.blit(text[0], (settings.menu_x, offset))

#             if number:
#                 self.image.blit(number[0], (settings.menu_x + 330 - number[0].get_size()[0], offset))
#             offset += text[0].get_size()[1] + 6

#         # Handle the up/down arrows for long lists
#         # if len(self.source_array) > len(self.menu_array):
#         #     if self.top_of_menu != 0:
#         #         self.image.blit(self.arrow_img_up, (20, 6))

#         # if len(self.source_array) > len(self.menu_array):
#         #     if self.top_of_menu != len(self.source_array) - self.max_items:
#         #         self.image.blit(self.arrow_img_down, (20, 454))

#     def render(self, *args, **kwargs):
#         if settings.hide_main_menu and settings.hide_main_menu != 3:
#             settings.hide_main_menu = 3
#             self.image.fill(settings.black_color)
#             self.saved_selection = self.selected

#         elif not settings.hide_main_menu:
#             if self.saved_selection:
#                 self.select(self.saved_selection)
#                 self.saved_selection = None

#             self.current_time = time.time()
#             self.delta_time = self.current_time - self.prev_time

#             if hasattr(self, 'images') and self.images:  # If there is an animation list
#                 if self.delta_time >= self.animation_time:
#                     self.prev_time = self.current_time

#                     self.imagebox.fill((0, 0, 0))

#                     if self.index >= len(self.images):
#                         self.index = 0

#                     if self.frameorder:  # Support non-linear frames
#                         if self.frame >= len(self.frameorder):
#                             self.frame = 0
#                         self.index = self.frameorder[self.frame]
#                         self.frame += 1

#                     self.file = self.images[self.index]
#                     self.imagebox.blit(self.file, (0, 0))
#                     self.imagebox.fill(settings.bright_color, None, pygame.BLEND_RGBA_MULT)
#                     self.image.blit(self.imagebox, (400, 0))

#                     self.index += 1