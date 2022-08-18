import colorsys
import pygame as pg
pg.init()

class ColorPicker():
    def __init__(self):
        self.surf = pg.Surface((700, 20))
        self.rect = self.surf.get_rect()
        self.surf.fill((200, 0, 0))
        self.fill_hsv()

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def fill_hsv(self):
        pa = pg.PixelArray(self.surf)
        # print(pa)
        h_norm = 360 / self.rect.width
        v_norm = 100 / self.rect.height
        for y in range (self.rect.height):
            for x in range (self.rect.width):
                # print(x, y)
                col = (h_norm*x/360, 1., 1.)
                print(col)
                col = colorsys.hsv_to_rgb(*col)
                pa[x, y] = (col[0]*255, col[1]*255, col[2]*255)

    def draw(self):
        return self.surf, self.rect