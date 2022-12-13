 #imports
import os
import pygame
import math
from pygame import *
from pygame.math import Vector2,Vector3
from pygame.locals import *
from forces import *
from physics_objects import *
from contact import *
from sqlalchemy import null
from beanbag import *

#clear terminal before you run
os.system("cls||clear")

#initialize pygame and open window
pygame.init()
width, height = 1920, 1080
window = pygame.display.set_mode([width, height])

fontpath = pygame.font.match_font("arial")
font = pygame.font.SysFont('arial', round(window.get_width()/30))

#timing
fps = 1000
dt = 1 / fps
clock = pygame.time.Clock()


#variables
objects = []
nonPhysicsObjects = []
fixedObjects = []
slingshot = []
beanbags = []
xOffset = 0
yOffset = -75

#grab related variables
ballGrabbed = False
ballLaunched = False
bagFlying = False
coeff_of_friction = 0.3
grabbedObj = null
mousePosCur = Vector2(pygame.mouse.get_pos())
mousePosPre = Vector2(pygame.mouse.get_pos())
mouseVel = Vector2(0,0)
sideOfSlingshot = 0 #0 means it was released on the left, 1 means the right

#create boards
#left board
leftBoardTop = Polygon(window,local_points=[[0,0],[80,28],[96,0],[32/2,-28]],pos=Vector2(210 +xOffset,727 - yOffset),mass=math.inf,color=Vector3(255,0,0))
objects.append(leftBoardTop)
leftBoardBottom = Polygon(window,local_points=[[0,0],[150,53],[165,28],[32/2,-28]],pos=Vector2(360 +xOffset,782 - yOffset),mass=math.inf,color=Vector3(255,0,0))
objects.append(leftBoardBottom)

#left board scoring zones
#left3PointZone = Polygon(window,local_points=[[0,0],])

#right board
rightBoardTop = Polygon(window,local_points=[[0,0],[32/2,28],[96,0],[80,-28]],pos=Vector2(1610 -xOffset,722 - yOffset),mass=math.inf,color=Vector3(255,0,0))
objects.append(rightBoardTop)
fixedObjects.append(True)
rightBoardBottom = Polygon(window,local_points=[[0,0],[32/2,28],[165,-28],[150,-53]],pos=Vector2(1380 - xOffset,807 - yOffset),mass=math.inf,color=Vector3(255,0,0))
objects.append(rightBoardBottom)
fixedObjects.append(True)

#create floor
floor = Wall(window, start_point=Vector2(1920,910),end_point=Vector2(0,910),color=Vector3(0,255,0), reverse=True)
objects.append(floor)
fixedObjects.append(True)

#create sticks
leftStick = Polygon(window,local_points=[[0,0], [10,0],[10,105],[0,105]],color=(0,0,0),pos=Vector2(215 + xOffset,730 - yOffset),mass=math.inf)
nonPhysicsObjects.append(leftStick)
fixedObjects.append(True)
rightStick = Polygon(window,local_points=[[0,0], [10,0],[10,110],[0,110]],color=(0,0,0),pos=Vector2(1690 + xOffset,725 - yOffset),mass=math.inf)
nonPhysicsObjects.append(rightStick)
fixedObjects.append(True)

#slingshot creation
topCircle = Circle(window, mass=10, pos=Vector2(leftBoardBottom.pos.x - 50, leftBoardBottom.pos.y - 200), radius=10, vel=Vector2(0,0), color=Vector3(100,100,100), width=2) 

#beanbag creation
beanbag1 = Beanbag(color=Vector3(255,0,0), pos=Vector2(window.get_width()/2 - 100, 400), launchOrigin=topCircle)

beanbags.append(beanbag1)
beanbag1.AddSecsToList(objects)



fixedObjects.append(False)
fixedObjects.append(False)
fixedObjects.append(False)
fixedObjects.append(False)

#more slingshot creation
objects.append(topCircle)
fixedObjects.append(True)
slingshot.append(topCircle)

# SETUP FORCES
gravity = Gravity(objects_list=objects, acc=(0, 980))
bonds = SpringForce(window, pairs_list=slingshot, strength=40)
drag = AirDrag(objects_list=objects)
#repulsion = SpringRepulsion(objects_list=bag)
windVector = Vector2(0,0)
pygame.key.set_repeat(1,1)

#game loop
running = True
while running:
    click = pygame.mouse.get_pressed()
    # update the display
    pygame.display.update()
    # delay for correct timing
    clock.tick(fps)
    # clear the screen
    window.fill([255,255,255])

    mousePosCur = Vector2(pygame.mouse.get_pos())
    mouseVel = Vector2(mousePosCur - mousePosPre)

    #get pressed key
    key = pygame.key.get_pressed()

    # EVENT loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False



    if click[0]:
        for obj in objects:
            if fixedObjects[objects.index(obj)] == False:
                if (((obj.pos - Vector2(pygame.mouse.get_pos())).magnitude() <= obj.radius)) and grabbedObj == null and obj.isBeanbag:
                    grabbedObj = objects.index(obj)
                    if not ballGrabbed:
                        ballGrabbed = True
                    break
                

        if grabbedObj != null:
            objects[grabbedObj].pos = pygame.mouse.get_pos()
            objects[grabbedObj].vel = Vector2(0,0)


    if not click[0]:
        if ballGrabbed:
            ballGrabbed = False
            ballLaunched = True
            if grabbedObj != null:
                if objects[grabbedObj].pos.x < topCircle.pos.x:
                    sideOfSlingshot = 0
                else:
                    sideOfSlingshot = 1

        if grabbedObj == 0:
            objects[grabbedObj].vel = Vector2(0,0)
            grabbedObj = null

        if grabbedObj != null and grabbedObj > 0:
            objects[grabbedObj].vel = mouseVel
            grabbedObj = null
        

        mousePosPre = mousePosCur

    if beanbags[len(beanbags)-1].centralSec != null:
        if ballLaunched:
            if sideOfSlingshot == 0 and beanbags[len(beanbags)-1].centralSec.pos.x > topCircle.pos.x:
                ballLaunched = False
                bagFlying = True
                slingshot.pop(slingshot.index(beanbags[len(beanbags)-1].centralSec))
            elif sideOfSlingshot == 1 and beanbags[len(beanbags)-1].centralSec.pos.x < topCircle.pos.x:
                ballLaunched = False
                bagFlying =  True
                slingshot.pop(slingshot.index(beanbags[len(beanbags)-1].centralSec))

    if beanbags[len(beanbags)-1].vel.x < 1 and beanbags[len(beanbags)-1].vel.y < 1:
        if bagFlying:
            bagFlying = False
            beanbags.append(Beanbag(color=Vector3(0,0,255), pos=Vector2(window.get_width()/2 - 100, 400), launchOrigin=topCircle))
            beanbags[len(beanbags)-1].AddSecsToList(objects)

            fixedObjects.append(False)
            fixedObjects.append(False)
            fixedObjects.append(False)
            fixedObjects.append(False)



                


    # PHYSICS
    for o in objects:
        o.clear_force()

    # collisions
    for bag in beanbags:
        bag.UpdateCollisions()
    overlap = False
    contacts: list[Contact] = []

    # check for contact with any other objects
    for a, b in itertools.combinations(objects, 2):
        resolve = True

        if (a.isBeanbag and b == topCircle) or (a == topCircle and b.isBeanbag):
            resolve = False
            c: Contact = generate(a, b, resolve=resolve, friction=coeff_of_friction)
        else:
            c: Contact = generate(a, b, resolve=resolve, friction=coeff_of_friction)

        if c.overlap > 0:
            overlap = True
            contacts.append(c)



    ## apply all forces
    gravity.apply(grabbedObj)


    if len(slingshot) > 1:
        bonds.apply(grabbedObj)
    #drag.apply(grabbedObj)


    ## update all objects
    for obj in objects:
        if fixedObjects[objects.index(obj)] == False:
            if objects.index(obj) > 0 and objects.index(obj) != grabbedObj:
                obj.vel += windVector
            obj.update(dt)
    
    for bag in beanbags:
        bag.Update(grabbedObj=grabbedObj, objectsList=objects, slingshot=slingshot, ballGrabbed=ballGrabbed)
        

    # GRAPHICS
    # draw objects
    offset = 1200
    for d in nonPhysicsObjects:
        d.draw()
        pygame.draw.line(window, color=Vector3(0,0,0),start_pos=(225,772),end_pos=(525,884))
        #pygame.draw.line(window, color=Vector3(0,0,0),start_pos=(200,705),end_pos=(500,705))

    for o in objects:
        o.draw()