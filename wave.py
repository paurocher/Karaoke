import pygame
from pydub import AudioSegment
import os

pygame.init()

"""
Loads sound. Plays, stops, plays from set point.
Draws sound.
Draws name of sound.
"""

class Wave():
    def __init__(self, menu_bar, path, padding=(10, 10)):
        self.menu_bar = menu_bar
        self.playing = False
        self.play_pos = 0
        self.pos_after_play = 0
        self.wave_padding = padding
        self.wave_width = 2000
        self.wave_height = 1000
        self.wave = pygame.Surface((self.wave_width,
                                    self.wave_height))
        self.rect = self.wave.get_rect()
        self.wave_scaled = None
        self.rect_scaled = 0, 0, 0, 0
        self.markers_area = 100  # this is temporary and will be driven by the markers bars (markers bar +
        # markers infor bar). So weĺl need to pass the window argument to this class to be able to grab
        # the markers bars properties.
        self.last_click_pos = self.get_click_pos((0, 0))
        self.scaled_click_pos = 0, 0
        self.raw_click_pos = 0, 0
        self.wave_click_pos = 0, 0
        self.sound_click_pos = 0

        self.audio_file_path = path
        self.audio_file_name = os.path.basename(self.audio_file_path)
        self.sound = AudioSegment.from_file(self.audio_file_path)
        self.sound_frames = self.sound.frame_count()
        self.sound_frame_rate = self.sound.frame_rate
        self.sound_samples = self.sound.get_array_of_samples()
        self.sound_milliseconds = len(self.sound)
        self.sound_channels = self.sound.channels
        self.sound_loudest = self.sound.max
        self.sound_surface_map = len(self.sound_samples) / self.wave_width
        # print("Sound samples: ", len(self.sound_samples))
        self.sound = pygame.mixer.Sound(self.audio_file_path)

        pygame.mixer.music.load(self.audio_file_path)

        self.draw_wave()
        self.set_size()
        self.move(0, self.menu_bar.thickness)

    def __str__(self):
        return("""total frames: {}
                frame rate: {}
                miliseconds {}: 
                channels: {}
                samples: {}
                loudest: {}""".format(self.sound_frames,
                                      self.sound_frame_rate,
                                      self.sound_milliseconds,
                                      self.sound_channels,
                                      len(self.sound_samples),
                                      self.sound_loudest
                                      ))

    def draw_wave(self):
        """Draws the waveform on a big surfae that later gets scaled down to
        the appropriate size for the window."""

        self.wave.fill((0,0,0,0))
        for i in range(self.wave_width):
            pygame.draw.line(self.wave,
                             (255, 255, 255),
                             (i, self.wave_height / 2),
                             (i, self.sound_samples[int(i * self.sound_surface_map)] /
                              self.sound_loudest * self.wave_height + (self.wave_height / 2)))
        pygame.draw.line(self.wave,
                         (255, 255, 255),
                         (0, self.wave_height / 2),
                         (self.wave_width, self.wave_height / 2))
        # self.move(0, 0)

    def draw(self):
        return self.wave_scaled, self.rect_scaled

    def move(self, x=0, y=0):
        self.rect_scaled = self.rect_scaled.move((x, y))

    def set_size(self):
        win_width = pygame.display.get_window_size()[0]
        win_height = pygame.display.get_window_size()[1]

        x_pad = self.wave_padding[0]
        y_pad = self.wave_padding[1]

        rect_width = win_width - x_pad * 2
        rect_height = win_height - y_pad * 2 - self.markers_area

        if rect_width < 1:
            rect_width = 1
        if rect_height < 1:
            rect_height = 1

        self.wave_scaled = pygame.transform.smoothscale(self.wave,
                                                        (rect_width,
                                                         rect_height/2)
                                                        )
        self.rect_scaled = self.wave_scaled.get_rect().move((x_pad, y_pad/2))

        self.sound_surface_map = len(self.sound_samples) / self.rect[2]
        # print("Wave surface: ",self.rect )
        # print("Sound surface map: ", self.sound_surface_map)
        self.wave_scaled.blit(self.text(), (-5, 0))

    def text(self):
        """   """

        font = pygame.font.Font(pygame.font.match_font("courier"), 18)
        font.set_bold(True)
        text_surf = font.render(self.audio_file_name,
                                True,
                                (255, 255, 255))
        text_bg = pygame.Surface((text_surf.get_width() + 10,
                                  text_surf.get_height() + 10),
                                 pygame.SRCALPHA)
        text_bg_rect = text_bg.get_rect()
        text_bg.fill((0,0,0,150), (text_bg_rect))
        text_bg.blit(text_surf, (5, 5))

        return text_bg

    def set_play_pos(self, pos):
        """Sets the start pos of the player"""
        # print(pos)
        pos = pos / 44100 / 2
        # print(pos)
        self.play_pos = pos

    def play(self):
        """Plays the sound."""
        # print(self.play_pos)
        pygame.mixer.music.play(start=float(self.play_pos))
        self.playing = True

    def pause(self):
        """Stops te sound from playing."""

        # self.play_pos = self.play_pos + pygame.mixer.music.get_pos() / 1000.
        pygame.mixer.music.pause()
        self.playing = False

    def get_pos(self):
        """Gets where the sound is stopped at."""
        return pygame.mixer.music.get_pos()

    def set_pos(self, pos):
        """Sets the pos of the sound to be played from."""
        pygame.mixer.music.set_pos(pos)

    def get_click_pos(self, click_pos):
        """Transform mouse click position from window to wave surface
        coordinates"""
        # print(self.rect)
        click_pos_wave_x = click_pos[0] - self.rect_scaled[0]
        if click_pos_wave_x > self.rect_scaled[2]:
            click_pos_wave_x = self.rect_scaled[2]
        if click_pos_wave_x < 0:
            click_pos_wave_x = 0

        click_pos_wave_y = click_pos[1] - self.rect_scaled[1]
        if click_pos_wave_y > self.rect_scaled[3]:
            click_pos_wave_y = self.rect_scaled[3]
        if click_pos_wave_y < 0:
            click_pos_wave_y = 0

        self.scaled_click_pos = click_pos_wave_x, click_pos_wave_y
        return self.scaled_click_pos

    def x_to_sample(self, coord):
        """Remaps a coordinate to sound sample."""
        return int(coord * self.sound_surface_map)

    def sample_to_x(self, sample):
        """Remaps a sample number to x coordinate."""
        return int(sample / self.sound_surface_map)

    def set_mouse_pos_vars(self, pos):
        self.raw_click_pos = pos
        self.wave_click_pos = self.get_click_pos(self.raw_click_pos)
        self.sound_click_pos = self.x_to_sample(self.wave_click_pos[0])
