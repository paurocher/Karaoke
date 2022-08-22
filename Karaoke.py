import pygame
from wave import Wave
from cursor import Cursor
from square import Square
from color_picker import create_cp_window
from menu_bar import MenuBar
import MenuFunctions
import utils

"""Text will not have lines. Itś going to be only one string that will be
chopped down to a max of 2 lines. Also scaled up or down t adapt to screen and window sizes.
Again, I will have to scale up or down the marker postions so they follow the scale and position (line 1 or 2) of the text."""

pygame.init()
DISPLAY_W, DISPLAY_H = 800, 400
CANVAS = pygame.Surface((DISPLAY_W, DISPLAY_H), pygame.SRCALPHA)
WINDOW = pygame.display.set_mode((DISPLAY_W, DISPLAY_H), pygame.RESIZABLE, pygame.SRCALPHA)
WINDOW_RECT = WINDOW.get_rect()
utils.WINDOW_ELEMENTS["WINDOW"] = WINDOW
RUNNING = True
CLOCK = pygame.time.Clock()
CURSOR_DRAG_WAVE = False
CURSOR_DRAG_CP = False

MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

pygame.display.set_caption("Karaoke")

# create menu bar
menu_bar = MenuBar()
utils.WINDOW_ELEMENTS["menu_bar"] = menu_bar


# create wave
wave = Wave(menu_bar,
            path="./misc_files/Prova numeros.mp3",
            padding=(0,0),
            )
utils.WINDOW_ELEMENTS["WAVE"] = wave
print(wave)

# create cursor
cursor = Cursor()
cursor_surface = cursor.draw()[0]
cursor_rect = cursor.draw()[1]
cursor.move(0)
utils.WINDOW_ELEMENTS["CURSOR"] = cursor

square = Square(wave)

# color picker
cp_win = create_cp_window(WINDOW_RECT)
utils.WINDOW_ELEMENTS["CP_WIN"] = cp_win

while RUNNING:
    CLOCK.tick(60)
    # print(menu_bar.is_open)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

        if event.type == pygame.VIDEORESIZE:
            wave.set_size()
            # wave.get_click_pos(wave.last_click_pos)
            # print(wave.last_click_pos, wave.scaled_click_pos)
            cursor.move(wave.sound_click_pos)
            # square.move(15000, wave.sound_surface_map)
            DISPLAY_W, DISPLAY_H = event.w, event.h
            # print("\n\n")
            # print("Window size: ", DISPLAY_W, DISPLAY_H)
            # print("Square rect: ", square.square_rect)
            # cp_win.events(event)

        if cp_win.is_open:
            cp_win.events(event)
            continue
        elif menu_bar.is_open:
            menu_bar.events(event)
            continue

        if event.type == MUSIC_END:
            wave.playing = False
            # wave.play_pos = 0

        if event.type == pygame.KEYDOWN:
            if cp_win.is_open:
                cp_win.events(event)
            else:
                if event.key == pygame.K_SPACE:
                    if wave.playing == False:
                        wave.play()
                    else:
                        wave.pause()
                        # print(wave.play_pos, wave.sound_milliseconds)
                if event.key == pygame.K_q:
                    RUNNING = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if wave.rect.collidepoint(pos):
                wave.set_mouse_pos_vars(pos)
                wave.set_play_pos(wave.sound_click_pos)
                if wave.playing:
                    wave.play()
                cursor.move(wave.sound_click_pos)
                # wave.last_click_pos = click_pos
                if cursor.cursor_rect_scale.collidepoint(wave.raw_click_pos):
                    CURSOR_DRAG_WAVE = True
            elif menu_bar.rect.collidepoint(mouse_pos):
                menu_bar.is_open = True
                menu_bar.events(event)
            # if cp_rect.collidepoint(pos):
            #     CURSOR_DRAG_CP = True
            #     cp.sample(pos)

        if event.type == pygame.MOUSEBUTTONUP:
            CURSOR_DRAG_WAVE, CURSOR_DRAG_CP = False, False

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if menu_bar.rect.collidepoint(mouse_pos):
                menu_bar.is_open = True
                menu_bar.events(event)
            if cp_win.is_open:
                pass
                cp_win.events(event)
            else:
                if CURSOR_DRAG_WAVE:
                    wave.set_mouse_pos_vars(pygame.mouse.get_pos(mouse_pos))
                    cursor.move(wave.sound_click_pos)
                    wave.set_play_pos(wave.sound_click_pos)
                    if wave.playing:
                        wave.play()
                #         cursor_pos_text = set_cursor_pos_text(wave_cursor_rect.centerx)
                # elif CURSOR_DRAG_CP:
                #     if cp_rect.collidepoint(mouse_pos):
                #         cp.sample(pos)

    WINDOW.fill((0,0,0,0))
    pygame.draw.line(WINDOW,
                     (50, 50, 50),
                     (0, wave.rect[3]),
                     (DISPLAY_W, wave.rect[3]))
    WINDOW.blit(*wave.draw())
    WINDOW.blit(*cursor.draw_pos())
    WINDOW.blit(*cursor.draw())
    pygame.draw.line(WINDOW,
                     (255, 255, 255),
                     (0, DISPLAY_H / 2),
                     (DISPLAY_W, DISPLAY_H / 2))
    WINDOW.blit(*menu_bar.draw())
    WINDOW.blit(*square.draw())
    if cp_win.is_open:
        WINDOW.blit(*cp_win.draw())


    pygame.display.update()

pygame.quit()
quit()
