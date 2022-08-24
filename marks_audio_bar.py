import pygame as pg
import utils

from pprint import pprint as pp


class MarksAudioBar():
    def __init__(self):
        font_color = (100, 100, 100)
        bg_color = (60, 60, 60)
        font_name = "courier"
        self.thickness = 16
        self.window = utils.WINDOW_ELEMENTS["WINDOW"]
        self.wave = utils.WINDOW_ELEMENTS["WAVE"]
        font = pg.font.Font(pg.font.match_font(font_name), 15)
        self.text_surf = font.render("marks_audio_bar",
                           True,
                           font_color,
                           bg_color)
        self.text_rect = self.text_surf.get_rect()

    def draw(self):

        window_rect = self.window.get_rect()
        surf_bg = pg.Surface((window_rect[2], self.thickness))
        rect_bg = surf_bg.get_rect()
        self.text_rect.midtop = rect_bg.midtop
        surf_bg.fill((30, 30, 30))
        surf_bg.blit(self.text_surf, self.text_rect)
        pg.draw.line(surf_bg, (100, 100, 100),
                     (0, rect_bg.bottomleft[1] - 1),
                     (rect_bg.bottomright[0], rect_bg.bottomright[1] - 1))
        rect_bg.topleft = (0, utils.WINDOW_ELEMENTS["WAVE"].rect_scaled[3] + utils.WINDOW_ELEMENTS["MENU_BAR"].thickness)

        return surf_bg, rect_bg
