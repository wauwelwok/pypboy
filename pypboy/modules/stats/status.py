from game.core import Entity
import pypboy
import pygame
import game
import settings
import pypboy.ui
import random
import time


class Module(pypboy.SubModule):
    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)

        self.label = "STATUS"
        self.images = []

        self.topmenu = pypboy.ui.TopMenu()
        self.add(self.topmenu)
        self.topmenu.label = "STAT"
        self.topmenu.title = settings.MODULE_TEXT

        self.footer = pypboy.ui.Footer(["NOTIFICATIONS", "POWER", "CUSTOM"])
        self.add(self.footer)

        self.upperfooter = pypboy.ui.UpperFooter(["RADIATION", "CONNECT >"])
        self.add(self.upperfooter)

        self.pipboyanimation = PipboyAnimation()
        self.add(self.pipboyanimation)

        self.prev_time = 0




class PipboyAnimation(game.Entity):
    def __init__(self):
        super(PipboyAnimation, self).__init__((640, 480))
        self.rect[0] = 80

        self.health_array = settings.health_array
        
        self.animation_index = 0
        self.animation_time = 0.125
        self.legs = []
        self.steps = list(range(4)) + list(range(4, 0, -1))
        self.prev_time = 0

        for i in range(1,9):
            image = pygame.image.load(f"images/stats/legs1/{i}.png").convert_alpha()
            self.legs.append(image)
        self.head = pygame.image.load("images/stats/head1/1.png").convert_alpha()

        self.counter = 0
        self.random_array_index = 0

        self.animation()
        self.render_health(0)

    def render_health(self, index):
        health_array = self.health_array[index]
        self.image.fill((0,0,0))
        self.health_pos = [(175,170), (175,280), (320,390), (465,280), (465,170)]
  
        # Health Bars
        pygame.draw.line(self.image, settings.bright_color, (160, 190), (190, 190), 7)
        pygame.draw.line(self.image, settings.bright_color, (160, 300), (190, 300), 7)
        
        pygame.draw.line(self.image, settings.bright_color, (305, 370), (335, 370), 7)

        pygame.draw.line(self.image, settings.bright_color, (450, 190), (480, 190), 7)
        pygame.draw.line(self.image, settings.bright_color, (450, 300), (480, 300), 7)

        index = 0
        for health in health_array:
            health_image = pygame.Surface((30,20))
            health_image.fill((0,0,0))
            pos = self.health_pos[index]
            index +=1

            text = settings.FreeRobotoB[24].render(health, settings.bright_color)
            text_rect = text[0].get_rect(center = pos)
            self.image.blit(text[0], text_rect) 
        
    def animation(self):
        animation_screen = pygame.Surface((120, 250))
             
        self.current_time = time.time()
        self.delta_time = self.current_time - self.prev_time
      
        if self.delta_time >= self.animation_time:
            self.prev_time = self.current_time
            animation_screen.fill((0,0,0))          

            if self.animation_index >= len(self.legs):
                self.animation_index = 0
            self.leg = self.legs[self.animation_index]
            
            animation_screen.blit((self.leg),(1 + self.steps[self.animation_index] // 2 , 68 + self.steps[self.animation_index]) )
            animation_screen.blit((self.head),(29 + self.steps[self.animation_index] // 2 , 0 + self.steps[self.animation_index]))

            self.image.blit(animation_screen, (296-40,115))
            self.animation_index += 1

    def render(self):
        # Change heads / health array numbers every x mins (32 fps * 60 * x mins)
        wait_time = 32 * 60 * settings.wait_time_mins
        if self.counter >= wait_time:
            while True:
                random_int = random.randint(0,6)
                if random_int != self.random_array_index:
                    break
            
            self.random_array_index = random_int
            #  images are marked 1 -> 7
            self.head = pygame.image.load(f"images/stats/head1/{self.random_array_index + 1}.png").convert_alpha()
            self.render_health(self.random_array_index)
            self.counter = 0
        self.counter +=1
            
        self.animation()
     
    


        
