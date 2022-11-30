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
leftBoardTop = Polygon(window,local_points=[[0,0],[25,-25],[50,0],[25,25]],pos=Vector2(300,720),mass=math.inf,color=Vector3(255,0,0))
objects.append(leftBoardTop)

#right board
leftBoardBottom = leftBoardTop = Polygon(window,local_points=[[0,0],[250,-250],[275,-225],[25,25]],pos=Vector2(400,500),mass=math.inf,color=Vector3(255,0,0))
objects.append(leftBoardBottom)


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
