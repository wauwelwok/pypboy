import pypboy
import settings
import time
import game
import pygame

class Module(pypboy.SubModule):

    label = "DATA"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)

        self.topmenu = pypboy.ui.TopMenu()
        self.add(self.topmenu)
        self.topmenu.label = "DATA"
        self.topmenu.title = settings.MODULE_TEXT
        

        # self.footer = pypboy.ui.Footer(settings.STATUS_FOOTER)
        self.footer = pypboy.ui.Footer([settings.date, settings.day, ""])
        self.add(self.footer)

        self.upperfooter = pypboy.ui.UpperFooter()
        self.add(self.upperfooter)

        self.clock = Clock()
        self.add(self.clock)


        
class Clock(game.Entity):
    def __init__(self):
        super(Clock, self).__init__()
        self.prev_time = 0
        self.animation_time = 1

        self.image = pygame.Surface((settings.WIDTH, 250))
        # self.rect = self.image.get_rect()
        self.rect[0] = 125
        self.rect[1] = 150
        # self.rect = self.image.get_rect()
        self.clock_length = 448
    
        

    def render(self):
        # wait till new second, then render
        self.current_time = time.time()
        self.delta_time = self.current_time - self.prev_time
      
        if self.delta_time >= self.animation_time:
            self.prev_time = self.current_time

            self.image.fill((settings.black_color))
            text = settings.FreeRobotoB_clock.render(time.strftime("%H:%M"), settings.light_color, settings.black_color)
          
            self.image.blit(text[0], (0,0))
         
            

