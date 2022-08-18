import pygame
pygame.init()

from utils import (pos_sample_to_pixel,
                   pos_pixel_to_sample)

class Square():
    def __init__(self, wave):
        self.wave = wave
        self.wave_rect = self.wave.rect
        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.surf.fill((255,0,0, 50))
        self.width = 50
        self.height = 50
        self.square_rect = self.surf.get_rect()


    def move(self, sample_pos, sound_surface_map):
        # print(self.square_rect)
        pos = pos_sample_to_pixel(sample_pos, sound_surface_map)
        self.square_rect = (pos + self.wave.wave_padding[0],
                            50,
                            50, 50)

    def draw(self):
        return self.surf, self.square_rect
