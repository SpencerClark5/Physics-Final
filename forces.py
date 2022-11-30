from xml.etree.ElementTree import PI
import pygame
from pygame.math import Vector2, Vector3
import itertools
import math

class SingleForce:
    def __init__(self, objects_list=[]):
        self.objects_list = objects_list

    def apply(self):
        for obj in self.objects_list:
            force = self.force(obj)
            obj.add_force(force)

    def force(self, obj): # virtual function
        return Vector2(0, 0)


class PairForce:
    def __init__(self, objects_list=[]):
        self.objects_list = objects_list

    def apply(self, grabbed):
        # Loop over all pairs of objects and apply the calculated force
        # to each object, respecting Newton's 3rd Law.  
        # Use either two nested for loops (taking care to do each pair once)
        # or use the itertools library (specifically, the function combinations).
        for obj in self.objects_list:
            if self.objects_list.index(obj) < len(self.objects_list) - 1:
                a = obj
                b = self.objects_list[self.objects_list.index(obj)+1]
                force = self.force(a,b)

            
            if self.objects_list.index(a) > 0 and self.objects_list.index(a) != grabbed:
                a.add_force(force)
            if self.objects_list.index(b) != grabbed:
                b.add_force(force)
        pass

    def force(self, a, b): # virtual function
        return Vector2(0, 0)


class BondForce:
    def __init__(self, window, pairs_list=[]):
        self.window = window
        # pairs_list has the format [[obj1, obj2], [obj3, obj4], ... ]
        self.pairs_list = pairs_list

    def apply(self, grabbed):
        # Loop over all pairs from the pairs list.
        # a is the first, b is the second
        for obj in self.pairs_list:
            if self.pairs_list.index(obj) < len(self.pairs_list) - 1:
                a = obj
                b = self.pairs_list[self.pairs_list.index(obj)+1]
                force = self.force(a,b)
                self.draw(a,b)
        # Apply the force to each member of the pair respecting Newton's 3rd Law.
            if self.pairs_list.index(a) > 0 and self.pairs_list.index(a) != grabbed:
                a.add_force(force)
            if self.pairs_list.index(b) != grabbed:
                b.add_force(-force)
        pass

    def force(self, a, b): # virtual function
        return Vector2(0,0)

# Add Gravity, SpringForce(bond force), SpringRepulsion (pair force), AirDrag(single force)
class Gravity(SingleForce):
    def __init__(self, acc=(0,0), **kwargs):
        self.acc = Vector2(acc)
        super().__init__(**kwargs)

    def force(self, obj):
        return obj.mass*self.acc
        # Note: this will throw an error if the object has infinite mass.
        # Think about how to handle those.


class Friction(SingleForce):
    def __init__(self, objects_list):
        super().__init__(objects_list)

    def force(self, obj):
        frictionCo = 0.3
        mass  = obj.mass
        gravity = 1000
        
        if obj.vel.magnitude() < 3:
            velNorm = Vector2(0,0)
        else:
            velNorm = obj.vel.normalize()

        if obj.vel.magnitude() < 3:
            friction = Vector2(0,0)
        else:
            friction = -frictionCo*mass*gravity*velNorm
        return friction

class SpringForce(BondForce):
    def force(self, a, b):
        rMag = (a.pos - b.pos).magnitude()
        rNorm = (a.pos - b.pos).normalize()
        damp = 2
        v = (a.vel - b.vel)
        natLen = a.radius + b.radius
        springStr = 500
        springForce = (-springStr*(rMag - natLen)-(damp*v).dot(rNorm))*rNorm
        return springForce

    def draw(self, a, b):
        pygame.draw.line(self.window, color= Vector3(100,100,100), start_pos = a.pos, end_pos = b.pos, width= 2)


class AirDrag(SingleForce):
    def force(self, obj):
        dragCo = 0.47
        airDensity = 0.0000000128
        vel = obj.vel
        area = 3.14*(obj.radius)**2
        airDrag = -(dragCo*airDensity*area*vel.magnitude()*vel)/2
        return airDrag

class SpringRepulsion(PairForce):
    def force(self, a, b):
        dist = a.pos - b.pos
        radA = a.radius
        radB = b.radius
        repulse = .1

        if (radA + radB - (dist.magnitude())) > 0:
            repulsion = repulse*((radA + radB) - (dist.magnitude()))*(dist.normalize())
        else:
            repulsion = Vector2(0,0)

        return repulsion
    