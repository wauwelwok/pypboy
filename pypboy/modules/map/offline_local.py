import pygame
import pypboy
import settings
import game
import os


class Module(pypboy.SubModule):
    label = "map"
    # do i need this var here?? also, set in settings?
    zoom = 3
        
    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        
        self.topmenu = pypboy.ui.TopMenu()
        self.add(self.topmenu)
        self.topmenu.label = "MAP"
        self.topmenu.title = settings.MODULE_TEXT

        self.map = Map(self.zoom)
        self.add(self.map)

        self.footer = pypboy.ui.Footer([settings.date, settings.day, "LOCAL MAP"])
        self.add(self.footer)

    def handle_action(self, action, value=0):
        if action == "zoom_in":
            self.zoomMap(1)
        if action == "zoom_out":
            self.zoomMap(-1)
    
    # def handle_resume(self):
    #     super(Module, self).handle_resume()
    
    def zoomMap(self, zoomFactor):
        # set so zoom between 0 - 20 ?
        self.zoom = self.zoom + zoomFactor

        # render a new map with this zoom IF zoom.png exists
        file = f"images/map/{self.zoom}.png"
        if os.path.exists(file):
            self.map.redraw_map(self.zoom)
        

class Map(game.Entity):
    def __init__(self, zoom):
        super(Map, self).__init__()
        map_width = 720
        map_height = 400
        self.map_zoom = zoom
        self.image = pygame.Surface((map_width, map_height))
        map = pygame.image.load(f"images/map/{zoom}.png")

        self.rect = self.image.get_rect()
        self.rect[0] = 40
        self.rect.top = 50
        self.image.blit(map, (0,0))
    
    def redraw_map(self, zoom):
        self.image.fill((0, 0, 0))
        map = pygame.image.load(f"images/map/{zoom}.png")
        self.image.blit(map, (0,0))

        
           



