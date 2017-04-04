#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import CONSTANTS as CONST
from scipy.spatial.distance import euclidean

class ModelException(Exception):
    """
    Generic class for gravity model exceptions.
    """
    pass

class Dot(list):
    def __init__(self, *args):
        super().__init__(*args)
    
    def dist(self, other):
        return euclidean(self, other)


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
            obj.refresh()


class Object:
    """
    Abstract Object class.
    """
    def __init__(self, mass, coords=(0, 0), acceleration=np.array((0., 0.)), id=-1):
        self.mass = mass
        self.center = Dot(coords)
        self.id = id
        self.acceleration = acceleration
    
    def __vectorize(self, obj):
        return  np.array(obj.center) - np.array(self.center)
    
    def calc(self, objects):
        
        for obj in objects:
            if obj is not self:
                distance = self.center.dist(obj.center)
                force_scalar = CONST.G * self.mass * obj.mass / distance**2
                unit_vector = self.__vectorize(obj) / distance
                force_vector = force_scalar * unit_vector
                self.acceleration += force_vector / self.mass
        
    def refresh(self):
        print(self.id,": acceleration is:", self.acceleration)
        # moving there somehow?
    
    def __repr__(self):
        return "<Object #{id} at ({0:.2f}; {1:.2f})>".format(*self.center, id=self.id)


if __name__ == "__main__":
    a = Object(1, coords=(1, 0), id=1)
    b = Object(10, coords=(20, 20), id=2)
    f = Field((100, 100), a, b)
    for _ in range(20):
        print(a, b)
        f.epoch()