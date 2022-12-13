#imports
import os
from pygame import *
from pygame.math import Vector2,Vector3
from pygame.locals import *
from forces import *
from physics_objects import *
from contact import *

#clear terminal before you run
os.system("cls||clear")

#initialize pygame and open window
pygame.init()
width, height = 1920, 1080
window = pygame.display.set_mode([width, height])

fontpath = pygame.font.match_font("arial")
font = pygame.font.SysFont('arial', round(window.get_width()/30))

#timing
fps = 60
dt = 1 / fps
clock = pygame.time.Clock()


#variables
objects = []
nonPhysicsObjects = []
xOffset = 0
yOffset = -75

#create boards
#left board
leftBoardTop = Polygon(window,local_points=[[0,0],[80,28],[96,0],[32/2,-28]],pos=Vector2(210 +xOffset,727 - yOffset),mass=math.inf,color=Vector3(255,0,0))
objects.append(leftBoardTop)
leftBoardBottom = Polygon(window,local_points=[[0,0],[150,53],[165,28],[32/2,-28]],pos=Vector2(360 +xOffset,782 - yOffset),mass=math.inf,color=Vector3(255,0,0))
objects.append(leftBoardBottom)

#left board scoring zones
#left3PointZone = Polygon(window,local_points=[[0,0],])

#right board
rightBoardTop = Polygon(window,local_points=[[0,0],[80,-28],[96,0],[32/2,28]],pos=Vector2(1610 -xOffset,722 - yOffset),mass=math.inf,color=Vector3(255,0,0))
objects.append(rightBoardTop)
rightBoardBottom = Polygon(window,local_points=[[0,0],[150,-53],[165,-28],[32/2,28]],pos=Vector2(1380 - xOffset,807 - yOffset),mass=math.inf,color=Vector3(255,0,0))
objects.append(rightBoardBottom)

#create floor
floor = Wall(window, start_point=Vector2(0,910),end_point=(1920,910),color=Vector3(0,255,0))
objects.append(floor)

#create sticks
leftStick = Polygon(window,local_points=[[0,0], [10,0],[10,105],[0,105]],color=(0,0,0),pos=Vector2(215 + xOffset,730 - yOffset),mass=math.inf)
nonPhysicsObjects.append(leftStick)
rightStick = Polygon(window,local_points=[[0,0], [10,0],[10,110],[0,110]],color=(0,0,0),pos=Vector2(1690 + xOffset,725 - yOffset),mass=math.inf)
nonPhysicsObjects.append(rightStick)

#game loop
running = True
while running:
    # update the display
    pygame.display.update()
    # delay for correct timing
    clock.tick(fps)
    # clear the screen
    window.fill([255,255,255])

    #get pressed key
    key = pygame.key.get_pressed()

    # EVENT loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    # PHYSICS
    for o in objects:
        o.clear_force()

    # collisions
    overlap = False
    contacts = []

    for a, b in itertools.combinations(objects, 2):
        pass

    # GRAPHICS
    # draw objects
    for d in nonPhysicsObjects:
        d.draw()
    for o in objects:
        o.draw()
