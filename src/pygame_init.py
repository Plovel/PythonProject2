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
for i in range(1, 7):
    CHESS_SOUNDS.append(pygame.mixer.Sound(
        PATH_TO_SOUNDS + f"checkers{i}.wav"))

BUTTON_UP_SOUNDS = []
for i in range(1, 2):
    BUTTON_UP_SOUNDS.append(pygame.mixer.Sound(
        PATH_TO_SOUNDS + f"button_up{i}.wav"))

BUTTON_DOWN_SOUNDS = []
for i in range(1, 2):
    BUTTON_DOWN_SOUNDS.append(pygame.mixer.Sound(
        PATH_TO_SOUNDS + f"button_down{i}.wav"))
