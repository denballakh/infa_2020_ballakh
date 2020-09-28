import pygame
from pygame.draw import *
import pygame.gfxdraw

pygame.init()

FPS = 100
size = [1000, 667]
[size_x, size_y] = [size[0], size[1]]
screen = pygame.display.set_mode(size)

def vecmul(vec, k):
	return [vec[0]*k, vec[1]*k]

def vecsum(vec1, vec2):
	return [vec1[0]+vec2[0],vec1[1]+vec2[1]]

def fact(n):
	res = 1
	for i in range(1, n+1):
		res *= i
	return res

def beziercurve(pointlist, stepcount=100):
	n = len(pointlist) - 1
	result = [[0,0]] * stepcount
	for step in range(0, stepcount):
		t = step / (stepcount-1)
		vec = [0,0]
		for j, pt in enumerate(pointlist):
			vec = vecsum(vec, 
				vecmul(pt,
					fact(n)/(fact(j)*fact(n-j)) * t**j * (1-t)**(n-j)
					)
				)
		result[step] = vec
	return result

#Относительную координату превращают в абсолютную
def fx(k): 
	return round(k*size_x)
def fy(k):
	return round(k*size_y)
#Относительную позицию превращает в абсолютную
def fxy(pos):
	return [fx(pos[0]), fy(pos[1])]
#Применяют fx, fy, fxy к списку значений
def fxm(array):
	return [fx(i) for i in array]
def fym(array):
	return [fy(i) for i in array]
def fxym(array):
	return [fxy(i) for i in array]

#1 полоса
color = [254,213,162]
[x1, x2] = fxm([0.000, 1.000])
[y1, y2] = fym([0.000, 0.215])
rect(screen, color, [x1,y1,x2-x1,y2-y1])

#2 полоса
color = [254,213,196]
[x1, x2] = fxm([0.000, 1.000])
[y1, y2] = fym([0.215, 0.431])
rect(screen, color, [x1,y1,x2-x1,y2-y1])

#3 полоса
color = [254,213,148]
[x1, x2] = fxm([0.000, 1.000])
[y1, y2] = fym([0.431, 0.640])
rect(screen, color, [x1,y1,x2-x1,y2-y1])

#4 полоса
color = [179,134,148]
[x1, x2] = fxm([0.000, 1.000])
[y1, y2] = fym([0.640, 1.000])
rect(screen, color, [x1,y1,x2-x1,y2-y1])

#Солнце
color = [252,238,33]
[sun_x, sun_y] = fxy([0.500, 0.200])
sun_r = fx(0.050)
circle(screen, color, [sun_x, sun_y], sun_r)

#Верхние горы
color = [252,152,49]
poly = fxym([
	[0.006, 0.470],
	[0.013, 0.406],
	]+beziercurve([
		[0.013, 0.406],
		[0.097, 0.401],
		[0.207, 0.198],
		])+[
	[0.207, 0.198],
	[0.245, 0.215],
	[0.263, 0.255],
	[0.385, 0.378],
	[0.452, 0.363],
	[0.486, 0.390],
	[0.535, 0.319],
	[0.577, 0.333],
	[0.602, 0.301],
	]+beziercurve([
		[0.602, 0.301],
		[0.671, 0.307],
		[0.717, 0.106],
		[0.750, 0.185],
		])+[
	[0.750, 0.185],
	[0.795, 0.250],
	[0.831, 0.236],
	]+beziercurve([
		[0.831, 0.236],
		[0.850, 0.236],
		[0.897, 0.286],
		])+[
	[0.897, 0.286],
	[0.932, 0.259],
	[1.000, 0.311],
	[1.000, 0.314],
	])
polygon(screen, color, poly)

#Нижние горы
color = [172,67,52]
poly = fxym([
	[0.000, 0.500],
	[0.025, 0.520],
	]+beziercurve([
		[0.025, 0.520],
		[0.087, 0.321],
		[0.136, 0.355],
		[0.175, 0.640],
		])+[
	[0.175, 0.640],
	[0.220, 0.530],
	[0.290, 0.585],
	[0.320, 0.450],
	[0.410, 0.480],
	[0.480, 0.560],
	[0.575, 0.530],
	]+beziercurve([
		[0.575, 0.530],
		[0.673, 0.365],
		[0.726, 0.445],
		])+[
	]+beziercurve([
		[0.726, 0.445],
		[0.777, 0.512],
		[0.820, 0.530],
		])+[
	[0.820, 0.530],
	[0.860, 0.450],
	[0.900, 0.500],
	[0.920, 0.445],
	[0.960, 0.450],
	[1.000, 0.360],
	[1.000, 0.645],
	[0.000, 0.680],	
	])
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
