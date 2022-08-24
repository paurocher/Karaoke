import pygame
pygame.init()

from utils import (pos_sample_to_pixel,
                   pos_pixel_to_sample)
import utils

class Cursor():
    def __init__(self):
        self.wave = utils.WINDOW_ELEMENTS["WAVE"]
        self.wave_rect = self.wave.rect_scaled
        self.cursor_W = 15
        self.fg_color = (255, 0, 0, 255)
        self.bg_color = (255, 0, 0, 75)
        self.cursor_surf = pygame.Surface((self.cursor_W,
                                           300),
                                          pygame.SRCALPHA)
        self.cursor_rect = self.cursor_surf.get_rect()
        self.cursor_surf.fill(self.bg_color, self.cursor_rect)
        pygame.draw.polygon(self.cursor_surf, self.fg_color,
                          ((self.cursor_rect.topleft),
                           (self.cursor_rect.topright),
                           (self.cursor_rect.midtop[0], 10)),
                          )
        pygame.draw.polygon(self.cursor_surf, self.fg_color,
                          ((self.cursor_rect.bottomleft),
                           (self.cursor_rect.bottomright),
                           (self.cursor_rect.midbottom[0],
                            self.cursor_rect.midbottom[1] - 10)),
                          )
        pygame.draw.line(self.cursor_surf,
                       self.fg_color,
                       self.cursor_rect.midtop,
                       self.cursor_rect.midbottom)

        self.cursor_surf_scale = self.cursor_surf
        self.cursor_rect_scale = self.cursor_rect

        self.pos = 0

    def get_rect(self, wave_rect, click_pos=None):
        """Solves the rect for the cursor where the mouse is dragging it."""
        self.cursor_rect = wave_rect.copy()
        if not click_pos:
            click_pos = self.cursor_rect[0], 0
        self.cursor_rect[0] = click_pos[0]
        # print (wave_rect, click_pos)
        return self.cursor_rect
    
    def move(self, sample_pos):

        sound_surface_map = self.wave.sound_surface_map
        self.pos = pos_sample_to_pixel(sample_pos, sound_surface_map)
        self.cursor_surf_scale = pygame.transform.smoothscale(
            self.cursor_surf, (self.cursor_W, self.wave_rect[3]))
        self.cursor_rect_scale = pygame.Rect(self.pos + self.wave.wave_padding[0] - self.cursor_W / 2,
                                             self.wave_rect[1],
                                             100,
                                             self.wave_rect[3])
        print("sample pos: ", sample_pos, "wav.sound_surface_map: ", self.wave.sound_surface_map,
              "pos: ", self.pos)

    def scale(self):
        self.cursor_surf_scale = pygame.transform.smoothscale(
            self.cursor_surf, (self.cursor_W, self.wave.rect_scaled[3]))
        self.cursor_rect_scale = pygame.Rect(self.pos + self.wave.wave_padding[0] - self.cursor_W / 2,
                                             self.wave.rect_scaled[1],
                                             100,
                                             self.wave.rect_scaled[3])

    def draw(self):
        self.scale()
        # print(self.pos)
        return self.cursor_surf_scale, self.cursor_rect_scale

    def draw_pos(self):
        # cursor postion text
        cursor_pos_font = pygame.font.SysFont("courier", 18)
        cursor_pos_font.set_bold(True)
        cursor_pos_surf = cursor_pos_font.render(str(self.wave.sound_click_pos),
                                                 True, (255, 255, 255))
        cursor_pos_rect = cursor_pos_surf.get_rect()
        cursor_pos_rect = cursor_pos_rect.move(self.wave.wave_padding[0], self.wave.rect[3]-cursor_pos_rect[3])
        return cursor_pos_surf, cursor_pos_rect
