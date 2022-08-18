import colorsys
from pygame import gfxdraw as gfxd
from random import randint
import pygame as pg
pg.init()


class TitleBar():
    def __init__(self):
        self.window = None
        self.width = 200
        self.height = 15
        self.bg_color = (20, 20, 20)
        self.fg_color = (200, 200, 200)
        self.title = "Color Picker"
        self.font = pg.font.Font(pg.font.match_font("courier"), 12)
        self.surf = pg.Surface((self.width, self.height))
        self.rect = self.surf.get_rect()
        self.surf.fill(self.bg_color)
        self.close_b_surf = pg.Surface((self.height, self.height), pg.SRCALPHA)
        self.close_b_rect = self.close_b_surf.get_rect()
        self.window_drag = False
        self.mouse_drag_offset = (0, 0)

        self.window_pos = 0, 0

        self.set_contents()

    def set_contents(self):
        # title
        text_surf = self.font.render("Color Picker",
                                     True,
                                     self.fg_color)
        text_rect = text_surf.get_rect()
        text_rect = text_rect.move(self.rect.midtop[0] - text_rect.w/2,
                                   self.rect.midtop[1] + 2)
        self.surf.blit(text_surf, text_rect)

        # close button
        pg.draw.line(self.close_b_surf, self.fg_color, self.close_b_rect.topleft, self.close_b_rect.bottomright, 2)
        pg.draw.line(self.close_b_surf, self.fg_color, self.close_b_rect.bottomleft, self.close_b_rect.topright, 2)
        self.close_b_rect = self.close_b_rect.move(self.rect.topright[0]-self.height - 2, 0)
        self.surf.blit(self.close_b_surf, self.close_b_rect)

    def events(self, event, mouse_pos):
#         print("""TitleBar
# {}""".format(self.rect))
        # print(event)
        if self.close_b_rect.collidepoint(mouse_pos):
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.window.is_open = False


    def move(self, x, y):
        self.rect = self.rect.move((x, y))
        self.draw()

    def draw(self):
        return self.surf, self.rect


class ColorWheel():
    def __init__(self):
        self.surf = pg.Surface((500, 500), pg.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.surf.fill((0, 0, 0, 0))
        self.pixel = pg.Surface((1, 1))
        self.rad = 245
        self.fill_hsv()
        self.scale(200, 200)

        self.selected_color = (0, 0, 0)

        self.window = None

    def fill_hsv(self):
        center = pg.Vector2(self.rect.center)
        vec = pg.Vector2()

        for rad in range(self.rad):
            for angle in range (360):
                vec.from_polar((rad, angle))
                pix_size = rad / 50
                if pix_size < 6:
                    pix_size = 6
                col_surf = pg.transform.scale(self.pixel, (
                    pix_size, pix_size))
                col_rect = col_surf.get_rect()
                x, y = (center+vec)
                col_rect = col_rect.move((x, y))
                col = (angle/360, rad/self.rad, 1.)
                col = colorsys.hsv_to_rgb(*col)
                col_surf.fill((col[0]*255, col[1]*255, col[2]*255))
                self.surf.blit(col_surf, col_rect)

    def sample(self, pos):
        x, y = pos
        x = x - self.rect[0]
        y = y - self.rect[1] - self.window.title_bar.height
        self.selected_color = self.surf.get_at((x, y))
        self.window.text_r.string = str(self.selected_color[0])
        self.window.text_g.string = str(self.selected_color[1])
        self.window.text_b.string = str(self.selected_color[2])

    def events(self, event, mouse_pos):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 or \
                event.type == pg.MOUSEMOTION:
            mouse_pos_offsett = mouse_pos[0] + self.rect[0], \
                                mouse_pos[1] + self.rect[1]
            self.sample(mouse_pos_offsett)

    def move(self, x, y):
        self.rect = self.rect.move(x, y)
        self.draw()

    def scale(self, w, h):
        # smoothscale breaks the color values and rgb doesnt go higher tha 253!
        # that is why I am using a scale ...
        self.surf = pg.transform.scale(self.surf, (w, h))
        self.rect = self.surf.get_rect()

    def draw(self):
        return self.surf, self.rect


class Slider():
    def __init__(self):
        self.surf = pg.Surface((200, 15))
        self.rect = self.surf.get_rect()

        pg.draw.rect(self.surf, (20, 20, 20), self.rect, 5)

    def events(self, event, mouse_pos):
#         print("""Slider
# {}""".format(self.rect))
        pass

    def move(self, x, y):
        self.rect = self.rect.move((x, y))

    def draw(self):
        return self.surf, self.rect


class TextBox:
    def __init__(self, window):
        self.window = window
        self.surf = pg.Surface((40, 20))
        self.orig_rect = self.surf.get_rect()
        self.rect = self.surf.get_rect()
        
        self.active_color = (0, 50, 50)
        self.inactive_color = (10, 10, 10)
        self.bg_color = self.inactive_color
        self.text_color = (255, 255, 255)
        self.font = pg.font.Font(pg.font.match_font("courier"), 12)
        self.string = "0"

        # self.draw()
        self.valid_keys = [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4,
                           pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]

    def set_active(self):
        self.bg_color = self.active_color
        # self.draw()

    def set_inactive(self):
        self.bg_color = self.inactive_color
        # self.draw()

    def events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in self.valid_keys:
                if self.validate_string(event.unicode):
                    self.string += str(event.unicode)
                    self.string = self.string.lstrip("0")
                    if self.string == "": self.string = "0"
                    self.draw()
            elif event.key == pg.K_BACKSPACE:
                self.string = "0"
                self.draw()

    def validate_string(self, extra_number):
        if int(self.string + extra_number) > 255:
            return False
        return True

    def update_selected_color(self):
        self.window.selected_color.bg_color = (int(self.window.text_r.string),
                                               int(self.window.text_g.string),
                                               int(self.window.text_b.string),
                                               0
                                               )

    def move(self, x, y):
        self.rect = self.rect.move(x, y)
        self.draw()

    def draw(self):
        self.surf.fill(self.bg_color)
        text_surf = self.font.render(self.string,
                                     True,
                                     "white")
        text_rect = text_surf.get_rect()
        text_rect = text_rect.move(self.orig_rect.center[0] - text_rect[2]/2,
                                   self.orig_rect[1] + text_rect[3]/2 - 2)
        self.surf.blit(text_surf, text_rect)

        pg.draw.rect(self.surf, "white", self.orig_rect, 1)

        self.update_selected_color()

        return self.surf, self.rect


class SelectedColor:
    def __init__(self):
        self.surf = pg.Surface((10, 10))
        self.orig_rect = self.surf.get_rect()
        self.rect = self.surf.get_rect()
        self.bg_color = (0, 0, 200, 0)
        self.draw()

    def move(self, x, y):
        self.rect = self.rect.move(x, y)
        self.draw()

    def scale(self, w, h):
        self.surf = pg.transform.scale(self.surf, (w, h))
        self.rect = self.surf.get_rect()
        self.draw()

    def events(self, event):
        pass

    def draw(self):
        self.surf.fill(self.bg_color)
        rect = (0,0,
                self.rect[2],
                self.rect[3])
        pg.draw.rect(self.surf, "white", rect, 1)
        return self.surf, self.rect


class ColorSamples:
    def __init__(self, window):
        self.window = window
        self.rows = 5
        self.columns = 5
        self.total_cells = self.rows * self.columns

        self.samples = {}
        # print(self.rect_container)

        # color samples surface
        self.surf_col = None
        self.rect_col = None
        self.find_dimensions()
        self.draw_grid()

        # selection rectangle surface
        self.surf_select = pg.Surface((self.rect_col.w, self.rect_col.h), pg.BLEND_ADD)
        self.rect_select = self.surf_col.get_rect()
        self.surf_select.blit(self.surf_col, self.rect_col)

        self.draw()
        # print(self.samples)

    def events(self, event, mouse_pos):
        mouse_pos_x = mouse_pos[0] - self.rect_select.x
        mouse_pos_y = mouse_pos[1] - self.rect_select.y
        # print(event)
        # print(mouse_pos, mouse_pos_x, mouse_pos_y)
        for sample, color in self.samples.items():
            rect = pg.Rect(sample)
            # print("sample ", sample)
            if rect.collidepoint((mouse_pos_x, mouse_pos_y)):
                self.draw_selected_outline(sample)
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.window.selected_color.bg_color = color
                    self.window.text_r.string = str(color[0])
                    self.window.text_g.string = str(color[1])
                    self.window.text_b.string = str(color[2])


    def find_dimensions(self):
        topleft = self.window.text_r.rect.bottomleft
        bottomright = self.window.rect.bottomright

        self.surf_col = pg.Surface((bottomright[0] - topleft[0] - 10,
                                bottomright[1] - topleft[1] - 10))
        self.rect_col = self.surf_col.get_rect()

    def draw_grid(self):
        """This will need to read a color list and color each cell
        accordingly"""
        """Also this needs to draw on an independent surface so we can blit it
        to self.surf then draw the selection rectangle over it without needing to
        rebuid this color char surface each time.
        It will only be redrawn if one of the sample gets a new color."""

        mult_x = self.rect_col.width / self.columns
        mult_y = self.rect_col.height / self.rows

        for row in range(self.rows):
            move_x = mult_x * row
            for column in range(self.columns):
                move_y = mult_y * column
                rect = pg.Rect(move_x, move_y, mult_x, mult_y)
                color = (randint(0, 255), randint(0, 255), randint(0, 255))
                self.samples[tuple(rect)] = color
                pg.draw.rect(self.surf_col, color, rect, 0, 0)

    def draw_selected_outline(self, sample):
        # self.surf_select.fill((50,0,0, 10))
        # self.surf_select.blit(self.surf_col, self.rect_col)
        self.surf_select = self.surf_col.copy()
        pg.draw.rect(self.surf_select, (255,255,255), sample, 2, pg.BLEND_ADD)
        self.draw()

    def move(self, x, y):
        self.rect_col = self.rect_col.move(x, y)
        self.rect_select = self.rect_select.move(x, y)
        self.draw()

    def draw(self):
        # self.surf_col.fill((0,0,0,0))
        # self.surf_col.blit(self.surf_select, self.rect_select)

        return self.surf_select, self.rect_select


class ResizeKnob():
    def __init__(self):
        self.width, self.height = 15, 15
        self.surf = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.rect = self.surf.get_rect()

        pg.draw.line(self.surf, (255, 255, 255),
                     self.rect.bottomleft,self.rect.topright,
                     2)
        pg.draw.line(self.surf, (255, 255, 255),
                     self.rect.midleft, self.rect.midtop,
                     2)
        pg.draw.line(self.surf, (255, 255, 255),
                     self.rect.topleft, self.rect.topleft,
                     2)

    def resize(self):
        pass

    def events(self, event, mouse_pos):
#         print("""Resize
# {}""".format(self.rect))
        pass

    def move(self, x, y):
        self.rect = self.rect.move((x, y))

    def draw(self):
        return self.surf, self.rect


class CPWindow():
    """The window that contains:
        - Title Bar
        - Color Wheel
        - Color Value
        - Selected Color
        - Color Samples"""

    def __init__(self,
                 resize_knob,
                 parent_win):

        self.size = 200, 400

        self.surf = pg.Surface(self.size)
        self.rect = self.surf.get_rect()
        self.is_open = False

        self.title_bar = TitleBar()
        self.title_bar.window = self
        self.title_bar.move(0, 0)

        self.color_wheel = ColorWheel()
        self.color_wheel.window = self
        self.color_wheel.move(0, self.title_bar.height)

        self.slider = Slider()
        self.slider.move(*self.color_wheel.rect.bottomleft)

        self.selected_color = SelectedColor()


        self.text_r = TextBox(self)
        self.text_g = TextBox(self)
        self.text_b = TextBox(self)
        self.text_r.move(*self.slider.rect.bottomleft)
        self.text_g.move(self.slider.rect.bottomleft[0] + 40, self.slider.rect.bottomleft[1])
        self.text_b.move(self.slider.rect.bottomleft[0] + 80, self.slider.rect.bottomleft[1])

        gap = self.rect.topright[0] - self.text_b.rect.topright[0]
        self.selected_color.scale(gap, self.text_b.rect.height)
        self.selected_color.move(*self.text_b.rect.topright)

        self.color_samples = ColorSamples(self)
        self.color_samples.move(self.text_r.rect.bottomleft[0] + 5,
                                self.text_r.rect.bottomleft[1] + 5)

        self.resize_knob = resize_knob
        self.resize_knob.move(
            0 + self.rect.bottomright[0] - self.resize_knob.width,
            0 + self.rect.bottomright[1] - self.resize_knob.height)


        self.parent_win = parent_win

        # event states
        self.mouse_drag_offset = (0, 0)
        self.mouse_pos_offset = (0, 0)
        self.window_drag = False
        self.LMB = False
        self.active_text_box = None


        self.layout((0, 0))


    def set_mouse_pos_offset(self, mouse_pos):
        self.mouse_pos_offset = mouse_pos[0] - self.rect[0], mouse_pos[1] - self.rect[1]

    def events(self, event):
        # print(event)
        mouse_pos = pg.mouse.get_pos()
        # print(mouse_pos)

        # print(mouse_pos_offsett, "\n")

        if event.type == pg.MOUSEBUTTONUP:
            self.window_drag = False
            self.LMB = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.LMB = True
            self.set_mouse_pos_offset(mouse_pos)
            self.mouse_drag_offset = (mouse_pos[0],
                                      mouse_pos[1])
            # if self.color_samples.rect_col.collidepoint(self.mouse_pos_offset):
            self.color_samples.events(event, self.mouse_pos_offset)

            if self.title_bar.rect.collidepoint(self.mouse_pos_offset):
                self.window_drag = True

            if self.color_wheel.rect.collidepoint(self.mouse_pos_offset):
                self.color_wheel.events(event, self.mouse_pos_offset)

            self.active_text_box = None
            for text_box in [self.text_r, self.text_g, self.text_b]:
                if text_box.rect.collidepoint(self.mouse_pos_offset):
                    self.active_text_box = text_box
                    text_box.set_active()
                    continue
                else:
                    text_box.set_inactive()
                    continue



        if event.type == pg.KEYDOWN and self.active_text_box:
            self.active_text_box.events(event)

        if event.type == pg.MOUSEMOTION:
            self.set_mouse_pos_offset(mouse_pos)
            if self.window_drag == 1:
                self.layout((mouse_pos[0] - self.mouse_pos_offset[0],
                             mouse_pos[1] - self.mouse_pos_offset[1]))
            # print(self.color_samples.rect, self.mouse_pos_offset)
            if self.color_samples.rect_col.collidepoint(self.mouse_pos_offset):
                self.color_samples.events(event, self.mouse_pos_offset)
            if self.color_wheel.rect.collidepoint(self.mouse_pos_offset):
                if self.LMB:
                    self.color_wheel.events(event, self.mouse_pos_offset)
        if self.title_bar.rect.collidepoint(self.mouse_pos_offset):
            self.title_bar.events(event, self.mouse_pos_offset)



        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.is_open = False


        #
        # elif self.slider.rect.collidepoint(self.mouse_pos_offset):
        #     # print(element)
        #     self.slider.events(event, self.mouse_pos_offset)
        #
        # elif self.resize_knob.rect.collidepoint(self.mouse_pos_offset):
        #     # print(element)
        #     self.resize_knob.events(event, self.mouse_pos_offset)

    def layout(self, pos):
        x, y = pos
        self.rect[0] = x
        self.rect[1] = y
        # self.color_wheel.move(0, 0)
        # self.title_bar.move(0, 0)
        # self.slider.move(0, 0)
        # self.resize_knob.move(0, 0)

    def draw(self):
        self.surf.fill((0, 0, 0))
        self.surf.blit(*self.color_wheel.draw())
        self.surf.blit(*self.title_bar.draw())
        self.surf.blit(*self.slider.draw())
        self.surf.blit(*self.text_r.draw())
        self.surf.blit(*self.text_g.draw())
        self.surf.blit(*self.text_b.draw())
        self.surf.blit(*self.selected_color.draw())
        self.surf.blit(*self.color_samples.draw())
        self.surf.blit(*self.resize_knob.draw())
        pg.draw.rect(self.surf,
                     (255, 255, 255),
                     (0, 0, self.rect.w, self.rect.h),
                     1,
                     0,
                     0, 0, 10, 10)
        return self.surf, self.rect


def create_cp_window(parent_win):
    window = CPWindow(ResizeKnob(),
                       parent_win)
    return window