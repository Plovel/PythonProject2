import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

WD = os.path.dirname(__file__) + '/' # Work Directory
PATH_TO_MEDIA = "media/"

import pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_icon(pygame.image.load(WD + PATH_TO_MEDIA + "icon.jpg"))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
clock = pygame.time.Clock()



PATH_TO_SOUNDS = WD + PATH_TO_MEDIA + "sfx/"

CHESS_SOUNDS = []
BUTTON_UP_SOUNDS = []
BUTTON_DOWN_SOUNDS = []
def InitSounds():
    i = 1
    while True:
        filename = PATH_TO_SOUNDS + f"checkers/checkers{i}.wav"
        if not os.path.isfile(filename): break
        CHESS_SOUNDS.append(pygame.mixer.Sound(filename))
        i += 1

    i = 1
    while True:
        ver = 2
        filename1 = PATH_TO_SOUNDS + f"buttons{ver}/button_up{i}.wav"
        filename2 = PATH_TO_SOUNDS + f"buttons{ver}/button_down{i}.wav"
        if not os.path.isfile(filename1): break
        if not os.path.isfile(filename2): break
        BUTTON_DOWN_SOUNDS.append(pygame.mixer.Sound(filename1))
        BUTTON_UP_SOUNDS.append(pygame.mixer.Sound(filename2))
        i += 1
InitSounds()
