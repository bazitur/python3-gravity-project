#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import CONSTANTS as CONST
from models import Field, Object
from numpy import array

def redistribute_rgb(r, g, b):
    threshold = 255.999
    m = max(r, g, b)
    if m <= threshold:
        return int(r), int(g), int(b)
    total = r + g + b
    if total >= 3 * threshold:
        return int(threshold), int(threshold), int(threshold)
    x = (3 * threshold - total) / (3 * m - total)
    gray = threshold - x * m
    return int(gray + x * r), int(gray + x * g), int(gray + x * b)

class RenderedObject(Object):
    
    def __init__(self, radius=50, color=(12, 163, 49), **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.radius = radius
        self.history = []
    
    def refresh(self):
        super().refresh()
        self.history.append(self.center)
    
    def render(self, surf):
        pygame.draw.circle(surf, self.color, [int(round(x)) for x in self.center], self.radius)


class RenderedField(Field):
    
    def __init__(self, *args):
        super().__init__(*args)
    
    def __render_trace(self, surf, obj):
        for idx, coord in enumerate(obj.history[-300:]):
            if idx != 299:
                pygame.draw.aaline(surf,
                                   redistribute_rgb(*[(1+idx/100)*i for i in obj.color]),
                                   coord,
                                   obj.history[-299+idx])
        pygame.draw.aalines(surf, [0.5 * i for i in obj.color], False, obj.history[-300:])
    
    def render(self):
        global game_display
        for obj in self.objects:
            try:
                self.__render_trace(game_display, obj)
            except: pass
            obj.render(game_display)


WIDTH, HEIGHT = 800, 600
_title = 'Simulation'

black, grey, white = (0, 0, 0), (150, 150, 150), (255, 255, 255)
red, green, blue = (240, 0, 0), (0, 240, 0), (0, 0, 240)

pygame.init()

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(_title)
clock = pygame.time.Clock()

sat = RenderedObject(radius=5, color=red, mass=5, coords=(400., 100.), velocity=[20., 0.], id=1)
earth = RenderedObject(radius=25, mass=1000, coords=(400., 300.), id=2)

field = RenderedField((WIDTH, HEIGHT), sat, earth)

def main():
    main_loop = True

    while main_loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sat.velocity = sat.velocity * 1.1
                elif event.key == pygame.K_DOWN:
                    sat.velocity = sat.velocity / 1.1
        game_display.fill(white)
        
        field.render()
        field.epoch()
        
        pygame.display.update()
        clock.tick(CONST.fps)


if __name__ == '__main__':
    main()
