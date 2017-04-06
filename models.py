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

Dot = np.array

class Field:
    def __init__(self, dimensions, *initial_objects):
        self.size = dimensions
        self.objects = list(initial_objects)
    
    def __iadd__(self, obj):
        self.objects.append(obj)
    
    def add(self, obj):
        self.objects.append(obj)
    
    def extend(self, objs):
        self.objects.extend(objs)
    
    def epoch(self):
        for obj in self.objects:
            obj.calc(self.objects)
        
        for obj in self.objects:
            obj.refresh()


class Object:
    """
    Abstract Object class.
    """
    def __init__(self, mass=1, coords=(0., 0.), velocity=(0., 0.), id=-1):
        self.mass = mass
        self.center = Dot(coords)
        self.id = id
        self.acceleration = np.array((0., 0.))
        self.velocity = velocity
    
    def __vectorize(self, obj):
        return  np.array(obj.center) - np.array(self.center)
    
    def __distance(self, obj):
        arr = self.center - obj.center
        return (arr[0]**2 + arr[1]**2)**0.5
    
    def calc(self, objects):
        
        for obj in objects:
            if obj is not self:
                distance = self.__distance(obj)
                if distance == 0:
                    raise ModelException("Objects collided.")
                force_scalar = CONST.G * self.mass * obj.mass / distance**2
                unit_vector = self.__vectorize(obj) / distance
                force_vector = force_scalar * unit_vector
                self.acceleration = self.acceleration + force_vector/self.mass
        
    def refresh(self):
        self.velocity = self.velocity + (self.acceleration*CONST.TAU)
        self.center = self.center + self.velocity*CONST.TAU
        self.acceleration = np.array((0., 0.))
    
    def __repr__(self):
        return "<Object #{id} at ({0:.2f}; {1:.2f})>".format(*self.center, id=self.id)


if __name__ == "__main__":
    from json import dump
    a = Object(1, coords=(300., 0.), speed=[30., 0.], id=1)
    b = Object(1000, coords=(300., 100.), id=2)
    f = Field((100, 100), a, b)
    ans1, ans2 = [], []
    for _ in range(1000):
        #print(a.speed, a.center)
        ans1.append(list(a.center))
        ans2.append(list(b.center))
        f.epoch()
    with open("data.json", "w") as doc:
        dump({"ans1": ans1, "ans2": ans2}, doc)