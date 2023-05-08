import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

WORKING_DIR = os.path.dirname(__file__) + '/'

import pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_icon(pygame.image.load(WORKING_DIR + PATH_TO_MEDIA + "icon.jpg"))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
clock = pygame.time.Clock()

CHESS_SOUNDS = []
for i in range(1, 7):   
    CHESS_SOUNDS.append(pygame.mixer.Sound(WORKING_DIR + PATH_TO_MEDIA + "sfx/checkers" + str(i) + ".wav"))
