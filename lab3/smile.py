import pygame
from pygame.draw import *
import pygame.gfxdraw

pygame.init()

FPS = 100
screen = pygame.display.set_mode((400, 400))




bacgroundColor = (200,200,200)

faceCenter = (200,200)
faceRaduis = 100
#faceWidth = 1
faceColor = (255,255,0)

leftEyeCenter = (150,180)
leftEyeRadius = 20
leftEyeColor = (255,0,0)

rightEyeCenter = (250,180)
rightEyeRadius = 15
rightEyeColor = (255,0,0)



screen.fill(bacgroundColor)

circle(screen, faceColor, faceCenter, faceRaduis)
#circle(screen, (0,0,0), faceCenter, faceRaduis+faceWidth, faceWidth)

circle(screen, leftEyeColor, leftEyeCenter, leftEyeRadius)
circle(screen, (0,0,0), leftEyeCenter, leftEyeRadius//2)
circle(screen, rightEyeColor, rightEyeCenter, rightEyeRadius)
circle(screen, (0,0,0), rightEyeCenter, rightEyeRadius//2)

line(screen, (0,0,0), [170,160],  [110,130], 15)

line(screen, (0,0,0), [400-170,160], [400-110,130], 10)

line(screen, (0,0,0), [150,250], [250,250], 20)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()