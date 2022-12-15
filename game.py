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

Font = pygame.font.SysFont('comicsansms', round(window.get_width()/20))

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
redPoints = 0
bluePoints = 0
round = 1 
scoring = False

#scoring zones
rightscorezone3 = Polygon(window,local_points=[[0,0],[300,0],[300,-100]],pos=Vector2(1400,907), mass=math.inf, color=Vector3(255,255,255), isScoring=True)
objects.append(rightscorezone3)
fixedObjects.append(True)

leftscorezone3 = Polygon(window,local_points=[[0,0],[300,0],[0,-100]],pos=Vector2(200,907), mass=math.inf, color=Vector3(255,255,255), isScoring=True)
objects.append(leftscorezone3)
fixedObjects.append(True)

rightscorezone1 = Polygon(window,local_points=[[0,0],[325,-120],[325,-143],[0,-50]],pos=Vector2(1375,882), mass=math.inf, color=Vector3(255,255,255), isScoring=True)
objects.append(rightscorezone1)
fixedObjects.append(True)

leftscorezone1 = Polygon(window,local_points=[[0,0],[300,112],[300,53],[0,-47]],pos=Vector2(225,772), mass=math.inf, color=Vector3(255,255,255), isScoring=True)
objects.append(leftscorezone1)
fixedObjects.append(True)


#grab related variables
ballGrabbed = False
ballLaunched = False
bagFlying = False
coeff_of_friction = 0.6
grabbedObj = null
mousePosCur = Vector2(pygame.mouse.get_pos())
mousePosPre = Vector2(pygame.mouse.get_pos())
mouseVel = Vector2(0,0)
sideOfSlingshot = 0 #0 means it was released on the left, 1 means the right

#create boards
#left board
leftBoardTop = Polygon(window,local_points=[[0,0],[80,28],[96,0],[16,-28]],pos=Vector2(210 + xOffset, 727 - yOffset), mass=math.inf, color=Vector3(255,0,0))
objects.append(leftBoardTop)
fixedObjects.append(True)
leftBoardBottom = Polygon(window,local_points=[[0,0],[150,53],[165,28],[16,-28]],pos=Vector2(360 + xOffset, 782 - yOffset), mass=math.inf, color=Vector3(255,0,0))
objects.append(leftBoardBottom)
fixedObjects.append(True)

#right board
rightBoardTop = Polygon(window,local_points=[[0,0],[16,28],[96,0],[80,-28]], pos=Vector2(1610 - xOffset, 722 - yOffset), mass=math.inf, color=Vector3(255,0,0))
objects.append(rightBoardTop)
fixedObjects.append(True)
rightBoardBottom = Polygon(window,local_points=[[0,0],[16,28],[165,-28],[150,-53]], pos=Vector2(1380 - xOffset, 807 - yOffset), mass=math.inf, color=Vector3(255,0,0))
objects.append(rightBoardBottom)
fixedObjects.append(True)

#create sticks
leftStick = Polygon(window,local_points=[[0,0], [0,105],[10,105],[10,0]], color=(0,0,0), pos=Vector2(215 + xOffset, 730 - yOffset), mass=math.inf)
objects.append(leftStick)
fixedObjects.append(True)
rightStick = Polygon(window,local_points=[[0,0], [0,110],[10,110],[10,0]], color=(0,0,0), pos=Vector2(1690 + xOffset, 725 - yOffset), mass=math.inf)
objects.append(rightStick)
fixedObjects.append(True)

#create floor
floor = Wall(window, start_point=Vector2(1920,910),end_point=Vector2(0,910),color=Vector3(0,255,0), reverse=True)
objects.append(floor)
fixedObjects.append(True)



#slingshot creation
topCircle = Circle(window, mass=10, pos=Vector2(leftBoardBottom.pos.x + 30, leftBoardBottom.pos.y - 200), radius=10, vel=Vector2(0,0), color=Vector3(100,100,100), width=2) 
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
        if bagFlying:
            bagFlying = False

            
            #     #use the array of beanbags to check if there are any
            #     #inside of the scoring zones opposite of slingshot

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
                scoring = True

                if scoring:

                    overlap = False
                    contacts: list[Contact] = []

                    for a, b in itertools.combinations(objects, 2):
                        resolve = False

                        if a.isScoring or b.isScoring:
                            c: Contact = generate(a, b, resolve=resolve, friction=coeff_of_friction)

                        if c.overlap > 0:
                            overlap = True
                            contacts.append(c)

                            if (a.isScoring and b.isBeanbag) or (a.isBeanbag and b.isScoring):
                                if a.isBeanbag:
                                    for bag in beanbags:
                                        if a == bag.sec1:
                                            if b == leftscorezone3 or b == rightscorezone3:
                                                if bag.color == Vector3(255,0,0):
                                                    redPoints += 3
                                                else:
                                                    bluePoints += 3
                                            if b == leftscorezone1 or b == rightscorezone1:
                                                if bag.color == Vector3(255,0,0):
                                                    redPoints += 1
                                                else:
                                                    bluePoints += 1

                                elif b.isBeanbag:
                                    for bag in beanbags:
                                        if b == bag.sec1:
                                            if a == leftscorezone3 or a == rightscorezone3:
                                                if bag.color == Vector3(255,0,0):
                                                    redPoints += 3
                                                else:
                                                    bluePoints += 3
                                            elif a == leftscorezone1 or a == rightscorezone1:
                                                if bag.color == Vector3(255,0,0):
                                                    redPoints += 1
                                                else:
                                                    bluePoints += 1

                    
                if scoring:
                    scoring = False
                    print ("red: "+str(redPoints))
                    print ("blue: "+str(bluePoints))

                


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
                    topCircle.pos = Vector2(leftBoardBottom.pos.x + 30, leftBoardBottom.pos.y - 200)
                    

                    


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
        elif a.isScoring or b.isScoring:
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
    
    #UI
    currentTurn = len(beanbags) % 2
    curPlayer = 0
    if currentTurn == 1:
        curPlayer = "Reds "
    else:
        curPlayer = "Blues "
    text = Font.render(f"{curPlayer} turn", True, (0,255,0))
    RedText = Font.render(f"{redPoints}", True, (255,0,0))
    BlueText = Font.render(f"{bluePoints}", True, (0,0,255))


    window.blit(text, (((window.get_width()) - text.get_width()) / 2, 200))
    window.blit(RedText, (((window.get_width()) - RedText.get_width()) / 4, 200))
    window.blit(BlueText, ((((window.get_width()) - BlueText.get_width()) / 4) * 3, 200))

    if redPoints > 11 :
        redPoints = 6
    if bluePoints > 11:
        bluePoints = 6

    Redwins = Font.render(f"Red wins!", True, (255,0,0))
    Bluewins = Font.render(f"Blue wins!", True, (0,0,255))

    
    if redPoints == 11:
        window.blit(Redwins, (((window.get_width()) - Redwins.get_width()) / 2, (window.get_height() - Redwins.get_height())/2 ))

    if bluePoints == 11:
        window.blit(Bluewins, (((window.get_width()) - Bluewins.get_width()) / 2, (window.get_height() - Bluewins.get_height())/2 ))
 

