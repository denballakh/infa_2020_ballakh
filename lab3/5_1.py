import pygame
from pygame.draw import *

pygame.init()

FPS = 100
size = [1000, 667]
[size_x, size_y] = [size[0], size[1]]
screen = pygame.display.set_mode(size)

#Произведение вектора на число
def vecmul(vec, k):
	return [vec[0] * k, vec[1] * k]
#Сумма векторов
def vecsum(vec1, vec2):
	return [vec1[0] + vec2[0], vec1[1] + vec2[1]]
#Факториал
def fact(n):
	res = 1
	for i in range(1, n + 1):
		res *= i
	return res
#Кривая Безье
def beziercurve(pointlist, stepcount=100):
	n = len(pointlist) - 1
	result = [[0, 0]] * stepcount
	for step in range(0, stepcount):
		t = step / (stepcount-1)
		vec = [0, 0]
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
	return round(k * size_x)
def fy(k):
	return round(k * size_y)
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
color = [254, 213, 162]
[x1, x2] = fxm([0.000, 1.000])
[y1, y2] = fym([0.000, 0.215])
rect(screen, color, [x1, y1, x2-x1, y2-y1])

#2 полоса
color = [254, 213, 196]
[x1, x2] = fxm([0.000, 1.000])
[y1, y2] = fym([0.215, 0.431])
rect(screen, color, [x1, y1, x2-x1, y2-y1])

#3 полоса
color = [254, 213, 148]
[x1, x2] = fxm([0.000, 1.000])
[y1, y2] = fym([0.431, 0.640])
rect(screen, color, [x1, y1, x2-x1, y2-y1])

#4 полоса
color = [179, 134, 148]
[x1, x2] = fxm([0.000, 1.000])
[y1, y2] = fym([0.640, 1.000])
rect(screen, color, [x1, y1, x2-x1, y2-y1])

#Солнце
color = [252, 238, 33]
[sun_x, sun_y] = fxy([0.500, 0.200])
sun_r = fx(0.060)
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
	[0.000, 0.570],
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
		])
	+ beziercurve([
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

#Темные нижние горы
color = [48,16,38]
poly = fxym([
	[0.000, 1.000],
	[0.000, 0.518],
	[0.120, 0.565],
	[0.215, 0.742],
	[0.300, 0.920],
	]+beziercurve([
		[0.300, 0.920],
		[0.350, 0.996],
		[0.470, 0.985],
		])+[
	[0.470, 0.985],
	[0.633, 0.850],
	[0.680, 0.880],
	]+beziercurve([
		[0.680, 0.880],
		[0.800, 1.100],
		[0.956, 0.620],
		[1.000, 0.605],
		])+[
	[1.000, 0.605],
	[1.000, 1.000],
	])
polygon(screen, color, poly)

#Рисование птиц
birdcolor = [66,33,11]
bird_original_relative_size = 0.05
bird =[
	]+beziercurve([
		[+0.00, +0.00],
		[+0.26, -0.38],
		[+0.90, -0.42],
		])+[
	]+beziercurve([
		[+0.90, -0.42],
		[-0.06, +0.36],
		])+[
	]+beziercurve([
		[-0.06, +0.36],
		[-0.96, -0.32],
		[-0.88, -0.42],
		])+[
	]+beziercurve([
		[-0.88, -0.42],
		[-0.64, -0.46],
		[+0.00, +0.00],
		])+[
	]

def bird_relative(relative_pos, relative_size=1.00):
	return fxym([vecsum(relative_pos, vecmul(pt, relative_size*bird_original_relative_size)) for pt in bird])

birds = [
	[[0.387, 0.352], 0.70],
	[[0.477, 0.364], 0.70],
	[[0.477, 0.415], 0.70],
	[[0.400, 0.457], 0.70],
	[[0.630, 0.666], 0.80],
	[[0.685, 0.741], 0.70],
	[[0.797, 0.715], 0.60],
	[[0.782, 0.785], 1.00],
]

for elem in birds:
	[pos, size] = elem
	polygon(screen, birdcolor, bird_relative(pos, size))



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True

pygame.quit()
