import pygame
from pydub import AudioSegment
# from pydub.playback import play
import os

pygame.init()

audio_file_path = "misc_files/Prova numeros.m4a"
audio_file_name = os.path.basename(audio_file_path)
sound = AudioSegment.from_file(audio_file_path)
sound_frames = sound.frame_count()
sound_frame_rate = sound.frame_rate
sound_samples = sound.get_array_of_samples()
sound_miliseconds = len(sound)
sound_channels = sound.channels
sound_loudest = sound.max
print ("""total frames: {}
frame rate: {}
miliseconds {}: 
channels: {}
samples: {}
loudest: {}""".format(sound_frames,
                       sound_frame_rate,
                       sound_miliseconds,
                       sound_channels,
                      len(sound_samples),
                      sound_loudest
                      ))
sound = pygame.mixer.Sound(audio_file_path)

clock = pygame.time.Clock()
wn = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Karaoke")

wave_borders = 10, 10
wave_width = pygame.display.get_window_size()[0] - wave_borders[1] * 2
wave_height = pygame.display.get_window_size()[1] / 2 - wave_borders[1] * 2
wave = pygame.Surface((wave_width,
                       wave_height))
sound_surface_map = len(sound_samples) / wave.get_size()[0]

for i in range(wave_width):
    pygame.draw.line(wave,
                     (255, 255, 255),
                     (i, wave_height / 2),
                     (i, sound_samples[int(i * sound_surface_map)] /
                      sound_loudest * wave_height + (wave_height / 2)))
pygame.draw.line(wave,
                 (255, 255, 255),
                 (0, wave.get_size()[1] / 2),
                 (wave.get_size()[0], wave.get_size()[1] / 2), 1)

# cursor
wave_cursor_surf = pygame.Surface((10, wave.get_height()), pygame.SRCALPHA)
wave_cursor_rect = wave_cursor_surf.get_rect()
wave_cursor_surf.fill((255, 0, 0, 100), wave_cursor_rect)
pygame.draw.polygon(wave_cursor_surf, (255,0,0, 255),
                    ((wave_cursor_rect.topleft),
                     (wave_cursor_rect.topright),
                     (wave_cursor_rect.midtop[0],10)),
                    )
pygame.draw.polygon(wave_cursor_surf, (255,0,0, 255),
                    ((wave_cursor_rect.bottomleft),
                     (wave_cursor_rect.bottomright),
                     (wave_cursor_rect.midbottom[0],
                      wave_cursor_rect.midbottom[1] - 10)),
                    )
pygame.draw.line(wave_cursor_surf, (255,0,0), wave_cursor_rect.midtop,
                 wave_cursor_rect.midbottom)
wave_cursor_rect.x = wave_borders[0] - wave_cursor_rect.width/2
wn.blit(wave, (wave_borders[0], wave_borders[1]))

# cursor postion font
cursor_pos_font = pygame.font.SysFont("courier", 10)

# name of file
print(pygame.font.get_fonts())
font = pygame.font.Font(pygame.font.match_font("courier"), 14)
text_surf = font.render(audio_file_name, False, (100,100,100))
wave.blit(text_surf, (10 , 10))

# play(sound)

def main():
    # program logic
    cursor_drag = False
    cursor_pos_text = "0.0"
    state = True
    while state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sound.play()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if wave_cursor_rect.collidepoint(pos):
                    cursor_drag = True
            if event.type == pygame.MOUSEBUTTONUP:
                cursor_drag = False
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if cursor_drag == True:
                    if pos[0] < (wave_cursor_rect.width / 2 + wave_borders[0]):
                        wave_cursor_rect.x = wave_borders[0] - \
                                             wave_cursor_rect.width / 2
                    elif pos[0] > (wave.get_width() + wave_borders[0]):
                        wave_cursor_rect.centerx = wave.get_width() + \
                                                   wave_borders[0]
                    else:
                        wave_cursor_rect.centerx = pos[0]
                    cursor_pos_text = set_cursor_pos_text(wave_cursor_rect.centerx)

        wn.fill((0,0,0))
        # separator line
        pygame.draw.line(wn,
                         (255, 255, 255),
                         (0, wn.get_size()[1] / 2),
                         (wn.get_size()[0], wn.get_size()[1] / 2), 1)
        # waveform
        wn.blit(wave, (wave_borders[0], wave_borders[1]))
        # cursor
        wn.blit(wave_cursor_surf, (wave_cursor_rect[0], wave_borders[1]))
        # cursor position
        cursor_pos_surf = cursor_pos_font.render(cursor_pos_text,
                                                 False, (100, 100, 100))
        wn.blit(cursor_pos_surf, (wave_cursor_rect.midbottom[0] - cursor_pos_surf.get_width()/2,
                                  wave_cursor_rect.midbottom[1]))
        pygame.display.update()
        clock.tick(30)


    pygame.quit()
    quit()


def set_cursor_pos_text(cursor_pos):
    a = sound_miliseconds // wave.get_rect()[2]
    return str((cursor_pos - wave_borders[0] ) * a)


main()