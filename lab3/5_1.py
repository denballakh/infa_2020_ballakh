import pygame
from pygame.draw import *
import pygame.gfxdraw

pygame.init()

FPS = 100
size = [2500, 1667]
[size_x, size_y] = [size[0], size[1]]
screen = pygame.display.set_mode(size)


#1 полоса
color = [254,213,162]
[y1, y2] = [0,360]
rect(screen, color, [0,y1,size_x,y2-y1])

#2 полоса
color = [254,213,196]
[y1, y2] = [360,720]
rect(screen, color, [0,y1,size_x,y2-y1])

#3 полоса
color = [254,213,148]
[y1, y2] = [720,1080]
rect(screen, color, [0,y1,size_x,y2-y1])

#4 полоса
color = [179,134,148]
[y1, y2] = [1080,size_y]
rect(screen, color, [0,y1,size_x,y2-y1])

#Солнце
color = [255,255,0]
[sun_x, sun_y] = [1180, 340]
sun_r = 120
circle(screen, color, [sun_x, sun_y], sun_r)

#Верхние горы
color = [255,84,0]
poly = [[100,0],[200,100],[0,500]]
polygon(screen, color, poly)

#Нижние горы
color = [255,50,0]
poly = [[0,0],[0,0],[0,0]]
polygon(screen, color, poly)



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True

pygame.quit()
