import pygame
from pygame.constants import *
from pygame.math import Vector2, Vector3
import random
import math

from sqlalchemy import null
from physics_objects import Circle  # copy in physics_objects.py from your previous project
from forces import *
from contact import *

# INITIALIZE PYGAME AND OPEN WINDOW
pygame.init()
window = pygame.display.set_mode(flags=FULLSCREEN)

# SETUP TIMING
fps = 60
dt = 1/fps
clock = pygame.time.Clock()

class Beanbag:
    def __init__(self, color=Vector3(255,255,255), pos=Vector2(0,0), launchOrigin=null):
        self.color = color
        self.pos = pos
        self.launchOrigin = launchOrigin

        self.bag = []

        self.centralSec = null
        self.centralIndex = 0
        self.backCount = 0
        self.forCount = 0

        self.sec1 = Circle(window, mass=1, pos=Vector2(pos), radius=4, vel=Vector2(0,0), color=Vector3(color), isBeanbag=True)
        self.sec2 = Circle(window, mass=1, pos=Vector2(pos+Vector2(10,0)), radius=4, vel=Vector2(0,0), color=Vector3(color), isBeanbag=True)
        self.sec3 = Circle(window, mass=1, pos=Vector2(pos+Vector2(20,0)), radius=4, vel=Vector2(0,0), color=Vector3(color), isBeanbag=True)
        self.sec4 = Circle(window, mass=1, pos=Vector2(pos+Vector2(30,0)), radius=4, vel=Vector2(0,0), color=Vector3(color), isBeanbag=True)

        self.bag.append(self.sec1)
        self.bag.append(self.sec2)
        self.bag.append(self.sec3)
        self.bag.append(self.sec4)
    
    def AddSecsToList(self, list=[]):
        list.append(self.sec1)
        list.append(self.sec2)
        list.append(self.sec3)
        list.append(self.sec4)

    def MoveBagTo(self, newPos=Vector2):
        self.sec1.pos = Vector2(newPos)
        self.sec2.pos = Vector2(newPos+Vector2(10,0))
        self.sec3.pos = Vector2(newPos+Vector2(20,0))
        self.sec4.pos = Vector2(newPos+Vector2(30,0))

        self.sec1.vel = Vector2(0,0)
        self.sec2.vel = Vector2(0,0)
        self.sec3.vel = Vector2(0,0)
        self.sec4.vel = Vector2(0,0)


    def UpdateCollisions(self):
        # collisions
        overlap = False
        contacts: list[Contact] = []
        coeff_of_friction = 0

        # check for contact with any other objects
        for a, b in itertools.combinations(self.bag, 2):
            resolve = True

            if (a == self.sec1 or a == self.sec2 or a == self.sec3 or a == self.sec4) and (b == self.sec1 or b == self.sec2 or b == self.sec3 or b == self.sec4):
                resolve = True
                c: Contact = generate(a, b, resolve=resolve, friction=coeff_of_friction)

            else:
                c: Contact = generate(a, b, resolve=resolve, friction=coeff_of_friction)

            if c.overlap > 0:
                overlap = True
                contacts.append(c)



    def Update(self, grabbedObj=null, objectsList=[], slingshot=[], ballGrabbed=False):
        if self.centralSec != null:
            self.backCount = self.bag.index(self.centralSec)
            self.forCount = self.bag.index(self.centralSec)

        if grabbedObj != null:
            for sec in self.bag: 
                if sec == objectsList[grabbedObj]:
                    self.centralSec = sec
                    self.centralIndex = self.bag.index(sec)
                    self.backCount = self.bag.index(sec)
                    self.forCount = self.bag.index(sec)
                    if len(slingshot) < 2:
                        slingshot.append(sec)
                        if not ballGrabbed:
                            ballGrabbed = True
            
        if self.centralSec != null:
            if self.backCount > 0 or self.forCount < len(self.bag)-1:
                while self.backCount > 0 or self.forCount < len(self.bag)-1:
                    if self.backCount > 0:
                        current = self.bag[self.backCount]
                        prev = self.bag[self.backCount-1]

                        prevdist = Vector2(current.pos - prev.pos)
                        prevangle = math.atan2(prevdist.y, prevdist.x)

                        if (current.pos - Vector2(prev.pos)).magnitude() > (current.radius + prev.radius):
                            prev.pos = current.pos - Vector2((math.cos(prevangle)*((current.radius + prev.radius))),(math.sin(prevangle)*((current.radius + prev.radius))))
                        # if bag.index(current) == bag.index(centralSec):
                        if (current.pos - Vector2(prev.pos)).magnitude() < (current.radius + prev.radius):
                            prev.pos = current.pos - Vector2((math.cos(prevangle)*((current.radius + prev.radius))),(math.sin(prevangle)*((current.radius + prev.radius))))
                            

                        self.backCount -= 1
                    
                    if self.forCount < len(self.bag)-1:
                        current = self.bag[self.forCount]
                        next = self.bag[self.forCount+1]

                        nextdist = Vector2(current.pos - next.pos)
                        nextangle = math.atan2(nextdist.y, nextdist.x)

                        if (current.pos - Vector2(next.pos)).magnitude() > (current.radius + next.radius):
                            next.pos = current.pos - Vector2((math.cos(nextangle)*((current.radius + next.radius))),(math.sin(nextangle)*((current.radius + next.radius))))
                        # if bag.index(current) == bag.index(centralSec):
                        if (current.pos - Vector2(next.pos)).magnitude() < (current.radius + next.radius):
                            next.pos = current.pos - Vector2((math.cos(nextangle)*((current.radius + next.radius))),(math.sin(nextangle)*((current.radius + next.radius))))
                        
                        self.forCount += 1
        else:
            for sec in self.bag:
                if self.bag.index(sec) < len(self.bag) - 1:
                    current = sec
                    next = self.bag[self.bag.index(sec)+1]

                nextdist = Vector2(current.pos - next.pos)
                nextangle = math.atan2(nextdist.y, nextdist.x)

                if (current.pos - Vector2(next.pos)).magnitude() > (current.radius + next.radius):
                    next.pos = current.pos - Vector2((math.cos(nextangle)*((current.radius + next.radius))),(math.sin(nextangle)*((current.radius + next.radius))))

        
