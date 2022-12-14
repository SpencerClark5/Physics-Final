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
from functions import *

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
LeftScoringZone3Points = [Vector2(200,807), Vector2(200,907), Vector2(500,907)]
LeftScoringZone1Point = [Vector2(255,725),Vector2(255,772),Vector2(525,825),Vector2(525,884)]
RightScoringZone3Points = [Vector2(1400,907),Vector2(1400,807),Vector2(1700,907)]
RightScoringZone1Point = [Vector2(1375,832),Vector2(1700,713),Vector2(1375,882),Vector2(1700,736)]
redPoints = 0
bluePoints = 0
round = 1


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
leftBoardTop = Polygon(window,local_points=[[0,0],[80,28],[96,0],[16,-28]],pos=Vector2(210 + xOffset, 727 - yOffset), mass=math.inf, color=Vector3(255,0,0))
objects.append(leftBoardTop )
leftBoardBottom = Polygon(window,local_points=[[0,0],[150,53],[165,28],[16,-28]],pos=Vector2(360 + xOffset, 782 - yOffset), mass=math.inf, color=Vector3(255,0,0))
objects.append(leftBoardBottom)

#right board
rightBoardTop = Polygon(window,local_points=[[0,0],[16,28],[96,0],[80,-28]], pos=Vector2(1610 - xOffset, 722 - yOffset), mass=math.inf, color=Vector3(255,0,0))
objects.append(rightBoardTop)
fixedObjects.append(True)
rightBoardBottom = Polygon(window,local_points=[[0,0],[16,28],[165,-28],[150,-53]], pos=Vector2(1380 - xOffset, 807 - yOffset), mass=math.inf, color=Vector3(255,0,0))
objects.append(rightBoardBottom)
fixedObjects.append(True)

#create floor
floor = Wall(window, start_point=Vector2(1920,910),end_point=Vector2(0,910),color=Vector3(0,255,0), reverse=True)
objects.append(floor)
fixedObjects.append(True)

#create sticks
leftStick = Polygon(window,local_points=[[0,0], [10,0],[10,105],[0,105]], color=(0,0,0), pos=Vector2(215 + xOffset, 730 - yOffset), mass=math.inf)
nonPhysicsObjects.append(leftStick)
fixedObjects.append(True)
rightStick = Polygon(window,local_points=[[0,0], [10,0],[10,110],[0,110]], color=(0,0,0), pos=Vector2(1690 + xOffset, 725 - yOffset), mass=math.inf)
nonPhysicsObjects.append(rightStick)
fixedObjects.append(True)

#slingshot creation
topCircle = Circle(window, mass=10, pos=Vector2(leftBoardBottom.pos.x + 10, leftBoardBottom.pos.y - 200), radius=10, vel=Vector2(0,0), color=Vector3(100,100,100), width=2) 
objects.append(topCircle)
fixedObjects.append(True)
slingshot.append(topCircle)

#beanbag creation
beanbags.append(Beanbag(color=Vector3(255,0,0), pos=Vector2(window.get_width()/2 - 100, 400), launchOrigin=topCircle))
beanbags[len(beanbags)-1].AddSecsToList(objects)



fixedObjects.append(False)
fixedObjects.append(False)
fixedObjects.append(False)
fixedObjects.append(False)

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


    #if clicking
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

    #if not clicking
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

    #when you pick up a beanbag
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

    #if beanbags are not moving
    if abs(beanbags[len(beanbags)-1].vel.x) < 10 and abs(beanbags[len(beanbags)-1].vel.y) < 10:
        
        for beanbag in beanbags:
            numOfRedBagsIn3 = 0
            numOfRedBagsIn1 = 0
            numOfBlueBagsIn3 = 0
            numOfBlueBagsIn1 = 0
        #if left side
        #check 3 point zone
            if IsInsideThreePointArea(LeftScoringZone3Points[0].x, LeftScoringZone3Points[0].y,
                                    LeftScoringZone3Points[1].x, LeftScoringZone3Points[1].y,
                                    LeftScoringZone3Points[2].x, LeftScoringZone3Points[2].y,
                                    beanbag.pos.x, beanbag.pos.y):
                print("in")

                if beanbag.color == Vector3(255,0,0):
                    numOfRedBagsIn3 += 1
                if beanbag.color == Vector3(0,0,255):
                    numOfBlueBagsIn3 += 1

        #check 1 point zone
            if IsInsideOnePointArea(LeftScoringZone1Point[0].x, LeftScoringZone1Point[0].y,
                                    LeftScoringZone1Point[1].x, LeftScoringZone1Point[1].y,
                                    LeftScoringZone1Point[2].x, LeftScoringZone1Point[2].y,
                                    LeftScoringZone1Point[3].x, LeftScoringZone1Point[3].y,
                                    beanbag.pos.x,
                                    beanbag.pos.y):
                print("in")
                if beanbag.color == Vector3(255,0,0):
                    numOfRedBagsIn1 += 1
                if beanbag.color == Vector3(0,0,255):
                    numOfBlueBagsIn1 += 1


        #else right side
        #check 3 point zone
            if IsInsideThreePointArea(RightScoringZone3Points[0].x, RightScoringZone3Points[0].y,
                                    RightScoringZone3Points[1].x, RightScoringZone3Points[1].y,
                                    RightScoringZone3Points[2].x, RightScoringZone3Points[2].y,
                                    beanbag.pos.x, beanbag.pos.y):
                print("in")
                if beanbag.color == Vector3(255,0,0):
                    numOfRedBagsIn3 += 1
                if beanbag.color == Vector3(0,0,255):
                    numOfBlueBagsIn3 += 1


        #else 
        #check 1 point zone
            if IsInsideOnePointArea(RightScoringZone1Point[0].x, RightScoringZone1Point[0].y,
                                    RightScoringZone1Point[1].x, RightScoringZone1Point[1].y,
                                    RightScoringZone1Point[2].x, RightScoringZone1Point[2].y,
                                    RightScoringZone1Point[3].x, RightScoringZone1Point[3].y,
                                    beanbag.pos.x,
                                    beanbag.pos.y):
                print("in")
                if beanbag.color == Vector3(255,0,0):
                    numOfRedBagsIn1 += 1
                if beanbag.color == Vector3(0,0,255):
                    numOfBlueBagsIn1 += 1
        if bagFlying:
            bagFlying = False
            
            #use the array of beanbags to check if there are any
            #inside of the scoring zones opposite of slingshot

            if len(beanbags) < 4:
                if len(beanbags) % 2 == 0:
                    beanbags.append(Beanbag(color=Vector3(255,0,0), pos=Vector2(window.get_width()/2 - 100, 400), launchOrigin=topCircle))
                else:
                    beanbags.append(Beanbag(color=Vector3(0,0,255), pos=Vector2(window.get_width()/2 - 100, 400), launchOrigin=topCircle))
                beanbags[len(beanbags)-1].AddSecsToList(objects)

                fixedObjects.append(False)
                fixedObjects.append(False)
                fixedObjects.append(False)
                fixedObjects.append(False)



               
            else:
                i = 0
                while i < len(fixedObjects)-1:
                    if not (fixedObjects[i]):
                        fixedObjects.pop(i)
                        i -= 1
                    i += 1

                for bag in beanbags:
                    bag.RemoveSecsFromList(objects)
                
                i = 1
                end = len(beanbags)

                while i <= end:
                    beanbags.pop(0)
                    i += 1

                beanbags.append(Beanbag(color=Vector3(255,0,0), pos=Vector2(window.get_width()/2 - 100, 400), launchOrigin=topCircle))
                beanbags[len(beanbags)-1].AddSecsToList(objects)

                fixedObjects.append(False)
                fixedObjects.append(False)
                fixedObjects.append(False)
                fixedObjects.append(False)

                round += 1
                if round % 2 == 0:
                    topCircle.pos = Vector2(rightBoardBottom.pos.x + 20, rightBoardBottom.pos.y - 200)
                else:
                    topCircle.pos = Vector2(leftBoardBottom.pos.x + 10, leftBoardBottom.pos.y - 200)

                


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

    for o in objects:
        o.draw()