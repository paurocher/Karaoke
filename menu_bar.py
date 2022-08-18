import pygame as pg
import MenuFunctions
from pprint import pprint as pp

import utils

pg.init()

BG_COLOR = (20, 20, 20)


class MenuBar:
    """This is where menus are placed.
    It will handle:
      - menu position (each menu entry is placed right of the precedent one. These will be MenuItem instances.)
      - bar thickness
      - bar bg color
      - draw function
      - events:
        - click
        - click and drag
        - mouseup"""

    def __init__(self):
        self.window = utils.WINDOW_ELEMENTS["WINDOW"]
        self.window_rect = self.window.get_rect()
        self.menu_structure = MenuFunctions.MENU_STRUCTURE
        self.thickness = 15
        self.surf = pg.Surface((self.window_rect.w, self.thickness), pg.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.is_open = False
        print(self.rect)

        self.drawing_submenu = None

        self.fill_menu_dict()
        self.build_bar()


    def events(self, event):
        """Implement click and hover.
        When click or button 1 down a trigger is set to True an enables the menu to render.
        Also, it sets a var to the name of the menu rendering. THis menu always renders if we
        hover over its children. Otherwise, it means we have changed from root menu, then it should
        change the var to the new root menu name and ender it.
        Hover just acts like now for the bg color changes."""
        if self.is_open:
            self.rect.h = self.window_rect.h
        else:
            self.rect.h = 15

        # print (event.type)
        mouse_pos = pg.mouse.get_pos()
        # print(mouse_pos)
        if event.type == pg.MOUSEMOTION:
            for path, values in self.menu_structure.items():
                rect = values["rect"]
                if not rect:
                    continue
                if rect.collidepoint(mouse_pos):
                    values["item"].bg_color = values["item"].bg_color_on
                else:
                    values["item"].bg_color = values["item"].bg_color_off
                    # self.hide_children()

        if event.type == pg.MOUSEBUTTONDOWN:
            collision = None
            for path, values in self.menu_structure.items():
                rect = values["rect"]
                if not rect:
                    continue
                #  capture which rect collides, then process it, else hide all
                # submenus
                if rect.collidepoint(mouse_pos):
                    collision = self.menu_structure[path]
                    break
            if collision:
                values["item"].bg_color = values["item"].bg_color_off
                if values["function"]:
                    print("has function")
                    values["function"]()
                    self.drawing_submenu = None
                    self.is_open = False
                    self.rect.h = 15
                    self.hide_children()
                else:
                    print("doesnt have function")
                    self.draw_children(path)
            else:
                print("no collision")
                self.drawing_submenu = None
                self.is_open = False
                self.rect.h = 15
                self.hide_children()

        self.surf = pg.Surface((self.rect.w, self.rect.h), pg.SRCALPHA)

    def fill_menu_dict(self):
        for path, values in self.menu_structure.items():
            pieces = path.split("/")
            root = "/".join(path.split("/")[0:-1])
            name = pieces[-1]
            if root == "":
                root = None
            self.menu_structure[path]["path"] = root
            self.menu_structure[path]["name"] = name
            self.menu_structure[path]["show"] = False  #  wether it is being drawn or not
            self.menu_structure[path]["item"] = MenuItem(name) #  will hold the menu object
            # surf, rect = self.menu_structure[path]["item"].draw()
            self.menu_structure[path]["surf"] = None
            self.menu_structure[path]["rect"] = None
            self.menu_structure[path]["level"] = len(pieces) - 1 #  will hold the menu object
        # pp(self.menu_structure)

    def build_bar(self):
        """Draws the menu bar.
        Makes a list of the buttons of just the menu bar.

        Returns: surface, rect
        """

        roots = [r[1] for r in self.menu_structure.items() if not r[1]["level"]]
        offset = 0
        for i, root in enumerate(roots):
            item = root["item"]
            item.path = root
            item.move(offset, 0)
            surf, rect = root["item"].draw()
            root["surf"] = surf
            root["rect"] = rect
            self.surf.blit(surf, rect)
            root["show"] = True
            # root["item"] = item
            offset += rect.width + 10

    def draw_children(self, parent_path):
        """This is where the children of any clicked menu item are drawn
            Args: parent_path: str: menu path"""
        """Find a way to block this once it has already been drawn once"""
        """Make this draw all parents so we see all the menu structure when going
        down submenus"""
        print("drawing_submenu: ", self.drawing_submenu, "path: ", parent_path)

        # First we determine the clicked item on the menu bar to calculate x
        # and y offsets
        clicked_item = self.menu_structure[parent_path]
        path_root_rect = self.menu_structure[parent_path.split("/")[0]]["rect"]  # rect of the root entry on the menu bar
        # print(path_root_rect)
        if clicked_item["item"].name == self.drawing_submenu:
            return  # blocks redrawing if this menu is already being displayed
        self.drawing_submenu = clicked_item["item"].name  # sets this var to impede drawing if this menu is alredy being displayed
        if not clicked_item["level"]:  # if clicked is a root menu item
            offset_x, offset_y = clicked_item["rect"].x, 15
        else:  # if clicked is not a root menu item
            offset_x, offset_y = clicked_item["rect"].w + clicked_item["rect"].x, clicked_item["rect"].y

        valid_counter = 0
        for path, values in self.menu_structure.items():
            offset_x_submenu = 0
            submenu = ""
            if values["level"] and not values["function"]:
                submenu = "  >"
                offset_x_submenu = 0
            if path.startswith(parent_path) and values["level"] == clicked_item["level"] + 1:
                # children.append(path)
                item = MenuItem(values["name"] + submenu)
                item.path = path
                item.move(offset_x + offset_x_submenu, offset_y + 15 * valid_counter)
                surf, rect = item.draw()
                self.surf.blit(surf, rect)
                self.menu_structure[path]["rect"] = rect
                self.menu_structure[path]["surf"] = surf
                self.menu_structure[path]["show"] = True
                self.menu_structure[path]["item"] = item
                valid_counter += 1
            else:
                if values["level"] > clicked_item["level"]:
                    self.menu_structure[path]["show"] = False
                    self.menu_structure[path]["rect"] = False

    def hide_children(self):
        """Whenever not colliding with a menu, hide the menu
        items that are not needed from the menu_items list"""
        for menu, values in self.menu_structure.items():
            if values["level"]:
                values["show"] = False

    def draw(self):
        # self.surf.fill((0, 0, 60, 10))
        pg.draw.rect(self.surf, BG_COLOR, (0, 0, self.window_rect.w, 15))
        for path, values in self.menu_structure.items():
            if values["show"]:
                surf, rect = values["item"].draw()
                self.surf.blit(surf, rect)
        return self.surf, self.rect


class MenuItem:
    """Menu entry.
    Handles:
      - name
      - parent (if prent is bar it appears in the menu bar. Otherwise, it appears
        as a submenu of another menu)
      - function (specific function or show function to show its children)
      - selected menu bg color (when mouse over it)
      - draw (text, hover)
      - menu font
"""

    def __init__(self, name):
        self.name = name
        self.path = None
        self.font_color = (255, 255, 255)
        self.bg_color_on = (100, 100, 100, 50)
        self.bg_color_off = BG_COLOR
        self.bg_color = self.bg_color_off
        font_name = "courier"
        font_size = 14
        self.font = pg.font.Font(pg.font.match_font(font_name), font_size)
        self.surf = self.font.render(self.name,
                                     True,
                                     self.font_color,
                                     self.bg_color)
        self.rect = self.surf.get_rect()

    def move(self, x, y):
        self.rect = self.rect.move((x, y))

    def draw(self):
        """Draws this specific menu item."""
        self.surf = self.font.render(self.name,
                                     True,
                                     self.font_color,
                                     self.bg_color)
        return self.surf, self.rect

    def events(self):
        self.draw()
