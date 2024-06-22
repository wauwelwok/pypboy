import pygame
import pypboy
import settings
import requests
import game
import threading
import io
import numpy as np
import config


class Module(pypboy.SubModule):
    label = "LOCAL MAP"
    zoom = settings.LOCAL_MAP_ZOOM
    map_top_edge = 128
    map_type = settings.MAP_TYPE
    map_width = 720
    map_height = 545
    map_rect = pygame.Rect(0, (map_width - 720) / 2, map_width, map_height - 45)

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        # self.mapgrid = Map(self.map_width,self.map_height)

        if (settings.LOAD_CACHED_MAP):
            print("Loading cached map")
            self.mapgrid = Map(self.map_width,self.map_height,self.map_rect, "Loading cached map")
            self.mapgrid.load_map(settings.MAP_FOCUS, self.zoom, self.map_width, self.map_height, self.map_type)
        else:
            print("Loading map from the internet")
            self.mapgrid = Map(self.map_width,self.map_height,self.map_rect, "Loading map from the internet")
            self.mapgrid.fetch_map(settings.MAP_FOCUS, self.zoom, self.map_width, self.map_height, self.map_type)

        self.add(self.mapgrid)
        self.mapgrid.rect[0] = 0
        self.mapgrid.rect[1] = self.map_top_edge

        self.topmenu = pypboy.ui.TopMenu()
        self.add(self.topmenu)
        self.topmenu.label = "MAP"
        self.topmenu.title = settings.MODULE_TEXT


        self.footer = pypboy.ui.Footer(["10.23.2287", "EVENING", "LOCAL MAP"])
        self.add(self.footer)

    def handle_action(self, action, value=0):
        if action == "zoom_in":
            self.zoomMap(1)
        if action == "zoom_out":
            self.zoomMap(-1)

    # def handle_resume(self):
    #     super(Module, self).handle_resume()

    def zoomMap(self, zoomFactor):
        self.zoom = self.zoom + zoomFactor
        if settings.LOAD_CACHED_MAP:
            print("Loading cached map")
            self.mapgrid.load_map(settings.MAP_FOCUS, self.zoom, self.map_width, self.map_height, self.map_type)
        else:
            print("Loading map from the internet")
            self.mapgrid.fetch_map(settings.MAP_FOCUS, self.zoom, self.map_width, self.map_height, self.map_type)

        self.add(self.mapgrid)
        self.mapgrid.rect[0] = 0
        self.mapgrid.rect[1] = self.map_top_edge

class Map(game.Entity):
    _mapper = None
    _transposed = None
    _size = 0
    _fetching = None
    _map_surface = None
    _loading_size = 0
    _render_rect = None

    def __init__(self, width, height, render_rect=None, loading_type="Loading map...", *args, **kwargs):
        super(Map, self).__init__((width, height), *args, **kwargs)
        self._size = width
        self._map_surface = pygame.Surface((width, height))
        self._render_rect = render_rect
        text = settings.FreeRobotoB[14].render(loading_type, settings.bright_color, (0, 0, 0))
        self.image.blit(text[0], (10, 10))

    def fetch_map(self, position, zoom, width, height, map_type):
        self._fetching = threading.Thread(target=self._internal_fetch_map, args=(position, zoom, width, height, map_type))
        self._fetching.start()

    def _internal_fetch_map(self, position, zoom, width, height, map_type):
        self.map_image = None
        lat = str(position[0])
        long = str(position[1])
        url = ("https://maps.googleapis.com/maps/api/staticmap?center=" + long + "," + lat +
               "&zoom=" + str(zoom) + "&size="
               + str(int(width/2)) + "x" + str(int(height/2))
               + "&scale=2"
               # + "&maptype=" + str(map_type)
               # + "&style=" + str(settings.MAP_STYLE)
               #+ "&markers=color:blue%7Clabel:S%7C40.702147,-74.015794" +
               #+ "&markers=color:green%7Clabel:G%7C40.711614,-74.012318" +
               #+  "&markers=color:red%7Clabel:C%7C40.718217,-73.998284" +
               + "&key=" + config.googlemaps_token
               + "&map_id=f1a13570cd60f576"

               )
                # Note the API string here is restricted you will need your own API string

        print("Loading map image from:" + url)

        try:
            r = requests.get(url)
            map_image = io.BytesIO(r.content)
        except:
            print ("Failed to load map image")
        if map_image:
            map_surf = pygame.image.load(map_image).convert()  # byte image to -> Surface


            arr = pygame.surfarray.pixels3d(map_surf)
            mean_arr = np.dot(arr[:, :, :], [0.216, 0.587, 0.144])
            mean_arr3d = mean_arr[..., np.newaxis]
            new_arr = np.repeat(mean_arr3d[:, :, :], 3, axis=2)
            map_surf = pygame.surfarray.make_surface(arr)

            map_surf.fill((0, 230, 0), None, pygame.BLEND_RGBA_MULT)
            self._map_surface.blit(map_surf, (0, 0))

            # svg_surface = load_svg("./images/map_icons/Player_Marker.svg", 40, 40)
            svg_surface = pygame.image.load("./images/map_icons/Player_Marker.svg").convert_alpha()
            svg_surface.fill(settings.bright_color, None, pygame.BLEND_RGBA_MULT)
            self._map_surface.blit(svg_surface, (settings.WIDTH / 2 - 20, self._render_rect.centery - 20))

        else:
            print("No map image")

        self.redraw_map()


    def load_map(self, position, zoom, isWorld):
        self._fetching = threading.Thread(target=self._internal_load_map, args=(position, zoom, isWorld))
        self._fetching.start()

    def _internal_load_map(self, position, zoom, isWorld):
        self._mapper.load_map_coordinates(position, zoom, isWorld)
        self.redraw_map()

    def move_map(self, x, y):
        self._render_rect.move_ip(x, y)

    def redraw_map(self, coef=1):
        self.image.fill((0, 0, 0))

        self.image.blit(self._map_surface, (0, 0), area=self._render_rect)