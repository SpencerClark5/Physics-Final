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

#create boards

#left board
#draws clock wise
leftBoardTop = Polygon(window,local_points=[[0,0],[80,28],[96,0],[32/2,-28]],pos=Vector2(210,725),mass=math.inf,color=Vector3(255,0,0))
objects.append(leftBoardTop)

leftBoardBottom = Polygon(window,local_points=[[0,0],[150,53],[165,28],[32/2,-28]],pos=Vector2(360,780),mass=math.inf,color=Vector3(255,0,0))
objects.append(leftBoardBottom)


#
#right board
rightBoardTop = Polygon(window,local_points=[[0,0],[80,28],[96,0],[16,-28]],pos=Vector2(500,725),mass=math.inf,color=Vector3(255,0,0))
objects.append(rightBoardTop)


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
    for o in objects:
        o.draw()
