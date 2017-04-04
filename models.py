#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import CONSTANTS as CONST

Dot = np.array

class Field:
    def __init__(self, dimensions, *initial_objects):
        self.size = dimensions
        self.objects = initial_objects
    
    def __iadd__(self, obj):
        self.objects.append(obj)
    
    def add(self, obj):
        self.objects.append(obj)
    
    def epoch(self):
        for obj in self.objects:
            obj.calc(self.objects)
        
        for obj in self.objects:
            obj.commit()


class Object:
    
    def __init__(self, mass, coords=(0, 0), vector=(0, 0), id=-1):
        self.mass = mass
        self.center = Dot(coords)
        self.vector = Dot(vector)
        self.id = id
    
    def calc(self, objects):
        
        for obj in objects:
            if obj is not self:
                # do the calculus
                pass
        
    def commit(self):
        pass
    
    def __repr__(self):
        return "<Object #{id} at ({0:.2f}; {1:.2f})>".format(*self.center, id=self.id)
    
if __name__ == "__main__":
    a = Object(1, vector=(1, 0), id=1)
    b = Object(10, coords=(20, 20), id=2)
    f = Field((100, 100), a, b)
    for _ in range(20):
        print(a, b)
        f.epoch()