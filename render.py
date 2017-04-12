#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import CONSTANTS as CONST
from models import Field, Object
from numpy import array
from random import randint as rint
from random import random


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
        a = 200
        start_idx = len(obj.history)-a if a<len(obj.history) else 0
        for idx, coord in enumerate(obj.history[start_idx:]):
            if idx != 0:
                pygame.draw.aaline(surf,
                                   redistribute_rgb(*[(2-idx/a)*1.5*i for i in obj.color]),
                                   coord,
                                   obj.history[start_idx+idx-1])
    
    def render(self):
        global game_display
        for obj in self.objects:
            self.__render_trace(game_display, obj)
            obj.render(game_display)


WIDTH, HEIGHT = 800, 600
_title = 'Simulation'

black, grey, white = (0, 0, 0), (150, 150, 150), (255, 255, 255)
red, green, blue = (240, 15, 15), (0, 240, 0), (0, 0, 240)

pygame.init()

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(_title)
clock = pygame.time.Clock()

mercury = RenderedObject(radius=3, color=blue, mass=1, coords=(400., 370.), velocity=[45, 0.], id=0)
venus = RenderedObject(radius=6, color=green, mass=10, coords=(400., 380.), velocity=(35., 0.), id=1)
earth = None
mars = None
sun = RenderedObject(radius=25, mass=1000, coords=(400., 300.), id=2, color=(240, 150, 0), moveable=False)

field = RenderedField((WIDTH, HEIGHT), mercury, venus, sun)
field.extend([RenderedObject(radius=rint(3, 10), color=(rint(1, 255),rint(1, 255),rint(1, 255)), velocity=(random()*50-25, random()*50-25), coords=(rint(10, 790), rint(10, 590)), mass=float(rint(1, 100))) for _ in range(10)])

def main():
    main_loop = True

    while main_loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False
                
        game_display.fill(white)
        
        field.render()
        field.epoch()
        
        pygame.display.update()
        clock.tick(CONST.fps)

if __name__ == '__main__':
    main()
