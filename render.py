#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import CONSTANTS as CONST

WIDTH, HEIGHT = 800, 600
_title = 'Title'

black, grey, white = (0, 0, 0), (150, 150, 150), (255, 255, 255)
red, green, blue = (240, 0, 0), (0, 240, 0), (0, 0, 240)

pygame.init()

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(_title)
clock = pygame.time.Clock()

def main():
    def draw_environment():
        game_display.fill(white)
        pygame.display.update()

    main_loop = True

    while main_loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False

        # your code goes here

        draw_environment()
        clock.tick(CONST.fps)


if __name__ == '__main__':
    main()
