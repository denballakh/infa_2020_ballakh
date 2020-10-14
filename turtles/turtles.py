import turtle
import numpy as np
from random import *

#Количество черепах
number_of_turtles = 100

#Параметры времени (при маленьких расстояниях шаг времени следует уменьшить)
time_max = 1e100			#Всего пройдет времени (бесконечность, т.е. бесконечная симуляция)
dt_max = 0.03				#Шаг при больщих расстояниях
dt_min = 0.003				#Шаг при мин. расстоянии dist0
dt = dt_max					#Действительное значение шага времени (пересчитывается на каждом шаге)
dist0 = 5					#Мин. расст., при котором шаг будет равен dt_min
dt_min_min = dt_min/5		#dt не опустится ниже этого значения (это доп. слагаемое)

#Коэффициент силы взаимодействия ("+" - притяжение, "- - оттлакивание)
k_grav = +100000

#Минимальная рассчитываемая дистанция, на расстояниях меньше нее кулоновская сила не учитывается
dist_grav = 2 

#При расстоянии менее dist_repul появляется сила отталкивания, растущая со скоростью k_repul на пиксель
dist_repul = 30
k_repul = 3 * np.abs(k_grav)/(dist_repul*(0.5))**2/(dist_repul*(1-0.5)) #Удвоенная(удесятеренная) сила притяжения на расстоянии dist_repul/2, поделенная на dist_repul/2

#Вязкое трение f = k * v + k_2 * v^2
k_visc = 0.5
k_visc_2 = 0.0

#Упругость столкновения со стенами
k_elast = 0.7

#Размеры поля
x1, x2 = -300, 300
y1, y2 = -300, 300

#Максимальный модуль начальной скорости
vmax = 50

#Добавочное константное ускорение
[a0x,a0y] = [0, -0]

#Рисовать ли линии
draw_bool = False

def f_grav(dist):
	f = 0
	if dist>dist_grav:
		f +=  k_grav / dist ** 2	#Формула силы взаимодействия
	else:
		f +=  0

	if dist<dist_repul:
		f -= (dist_repul - dist) * k_repul	#Упругое отталкивание

	return f


def f_visc(vel):
	f = k_visc*vel + k_visc_2 * vel**2
	return -f

#Рисование квадрата поля
turtle.tracer(1, 0)
t = turtle.Turtle()
t.hideturtle()
t.penup()
t.goto(x1,y1)
t.pendown()
t.goto(x2,y1)
t.goto(x2,y2)
t.goto(x1,y2)
t.goto(x1,y1)

turtle.tracer(10, 0)

#Создание черепашек со случайными позициями и скоростями
turtles = [] #список словарей с состояниями черепашек
for i in range(number_of_turtles):
	pos = [randint(x1, x2), randint(y1, y2)]
	ang = random() * 2 * np.pi
	v = vmax * random()
	vel = [v * np.cos(ang), v * np.sin(ang)]
	acc = [0,0]

	t = turtle.Turtle(shape='classic')

	if i==0:
		color = "red"
	elif i==1:
		color = "green"
	elif i==2:
		color = "blue"
	else:
		color = "#c0c0c0"
	t.pencolor(color)
	#t.hideturtle()
	t.penup()
	t.goto(pos[0], pos[1])
	t.pendown()
	if not draw_bool:
		t.penup()

	turtles.append({
		"t": t,
		"pos": pos,
		"vel": vel,
		"acc": acc,
		"drawing_time": 0
	})


time = 0
while time < time_max:
	time += dt

	mindist = x2 - x1
	for unit in turtles:
		[x, y] = unit["pos"]
		[ax, ay] = [a0x,a0y]
		#Суммирование сил от остальных черепашек
		for unit_sec in turtles:
			if unit_sec != unit:
				[x_, y_] = unit_sec["pos"]
				dist = ((x_ - x)**2 + (y_ - y)**2)**0.5
				
				f = f_grav(dist)

				dax = f * (x_ - x)/dist
				day = f * (y_ - y)/dist
				[ax, ay] = [ax+dax, ay+day]

				if dist<mindist and dist>dist_grav: #Нахождение минимального расстояния
					mindist = dist
				elif dist<mindist and mindist>dist_grav:
					mindist = dist_grav
		unit["acc"] = [ax, ay]

	#Формулы изменения шага (они очень похожи)
	#dt = dt_max * 2/np.pi * np.arctan(np.tan(np.pi/2 * dt_min/dt_max) * mindist/dist0 * 0.5) + dt_min_min
	dt = dt_max * (1 - 1/(1 + mindist/dist0 * dt_min/dt_max)) + dt_min_min

	#Изменение состояния черепах
	for unit in turtles:
		[x, y] = unit["pos"]
		[vx, vy] = unit["vel"]
		[ax, ay] = unit["acc"]

		v = (vx**2 + vy**2)**.5
		[ax, ay] = [ax + f_visc(v) * vx/v, ay + f_visc(v) * vy/v]

		#Расчет сдвигов с учетом ускорений и трения
		x += vx*dt + ax*dt**2/2
		y += vy*dt + ay*dt**2/2
		vx += ax*dt
		vy += ay*dt

		#Проверка на столкновения со стенами
		if x<x1 and vx<0:
			vx *= -k_elast
			x = x1
		if x>x2 and vx>0:
			vx *= -k_elast
			x = x2
		if y<y1 and vy<0:
			vy *= -k_elast
			y = y1
		if y>y2 and vy>0:
			vy *= -k_elast
			y = y2
		if (vx**2+vy**2)**.5>2:
			unit["t"].setheading(180/np.pi * np.arctan2(vy, vx))

		unit["drawing_time"] += 1 #Когда нарисовано много длинных линий программа начинает тормозить, поэтому будем их иногда очищать
		if unit["drawing_time"]>100:
			unit["drawing_time"] = 0
			unit["t"].clear()
		unit["t"].goto(x,y)
		unit["pos"] = [x, y]
		unit["vel"] = [vx, vy]
		unit["acc"] = [ax, ay]

