import pygame as py
import pygame.gfxdraw
import pygame.locals
import pygame.font
import random
from math import pi, sin, cos

randomReal = random.uniform
randomInt = random.randint

def vecSum(v1, v2):
    '''
    Возвращает сумму двух векторов
    v1, v2 - вектора вида [vx, vy]
    Результат:
    [v1x + v2x, v1y + v2y]
    '''
    return v1[0]+v2[0], v1[1]+v2[1]

def vecMul(v, k):
    '''
    Возвращает произведение вектора на число
    v - вектор вида [vx, vy]
    k - число
    Результат:
    [vx * k, vy * k]
    '''
    return v[0]*k, v[1]*k

def randomColor(colors):
    '''
    Возвращает случайный цвет из массива colors
    '''
    return colors[randomInt(0, len(colors) - 1)]
    #return (randomInt(0, 255), randomInt(0, 255), randomInt(0, 255))

def randomVelocity(vel_diap=None, ang_diap=None):
    '''
    Возвращает случайную скорость:
        Модуль скорости из диапазона vel_diap (по умолчанию [V_MIN, V_MAX])
        Направление скорости из диапазона ang_diap (по умолчанию [0, 2*PI])
    '''
    if vel_diap == None:
        vel_diap = V_MIN, V_MAX
    if ang_diap == None:
        ang_diap = 0, 2*pi

    ang_min, ang_max = ang_diap
    vel_min, vel_max = vel_diap
    ang = randomReal(ang_min, ang_max)
    vel = randomReal(vel_min, vel_max)
    vx = vel * cos(ang)
    vy = vel * sin(ang)
    return vx, vy

def randomBallState():
    '''
    Возвращает шарик со случайным состоянием
    '''
    _type = "particle" if randomReal(0,1) < particleProbability else "ball"
    rad = randomReal(R_MIN, R_MAX)
    x = randomReal(rad, SIZE_X - rad)
    y = randomReal(rad, SIZE_Y - rad)
    ang = randomReal(0, 2*pi)
    if _type != "particle":
        vx, vy = randomVelocity()
    else:
        vx, vy = randomReal(VPART_MIN,VPART_MAX), randomReal(VPART_MIN,VPART_MAX)
    color = randomColor(BALLCOLORS if _type=="ball" else PARTICLECOLORS)
    ltm = randomReal(0, LTM_MAX)
    return {
            "pos": (x, y), 
            "vel": (vx, vy),
            "rad": rad, 
            "ltm": ltm,
            "col": color,
            "type": _type
        }

def drawBall(ball):
    '''
    Рисует шарик
    '''
    x, y = ball["pos"]
    x, y = round(x), round(y)
    rad = ball["rad"]
    col = ball["col"]
    _type = ball["type"]
    if _type == "ball":
        pygame.draw.circle(screen, col, (x, y), round(rad))
    else:
        pygame.draw.polygon(screen, col, [(x-rad, y), (x, y+rad), (x+rad, y), (x, y-rad)])

def drawBalls():
    '''
    Рисует все шарики из массива balls
    '''
    f = pygame.font.Font(None, 30)
    sur = f.render(str(int(score)), True, SCORECOLOR)
    screen.blit(sur, (SIZE_X -  sur.get_size()[0], 0))
 
    for ball in balls:
        drawBall(ball)

def updateBallState(ball):
    pos = ball["pos"]
    vel = ball["vel"]
    rad = ball["rad"]
    ltm = ball["ltm"]
    col = ball["col"]
    _type = ball["type"]

    if ltm>LTM_MAX:
        return randomBallState()

    if _type == "ball":
        pos = vecSum(pos, vecMul(vel, DT))
        x, y = pos
        vx, vy = vel
        v = (vx**2 + vy**2)**.5
        if x>=SIZE_X-rad and vx>0:
            x = SIZE_X-rad
            da = pi/2 if vy<0 else 0
            vx, vy = randomVelocity([v,v], [pi/2+da, pi+da])

        if x<=rad and vx<0:
            x = rad
            da = pi/2 if vy>0 else 0
            vx, vy = randomVelocity([v,v], [-pi/2+da, 0+da])

        if y>=SIZE_Y-rad and vy>0:
            y = SIZE_Y-rad
            da = pi/2 if vx>0 else 0
            vx, vy = randomVelocity([v,v], [pi+da,3/2*pi+da])

        if y<=rad and vy<0:
            y = rad
            da = pi/2 if vx<0 else 0
            vx, vy = randomVelocity([v,v], [0+da,pi/2+da])

        pos = x, y
        vel = vx, vy
    else:
        x, y = pos
        vx, vy = vel
        v = (vx**2 + vy**2)**.5
        oldvel = vel
        vel = vx + vy * DT * MAGNETICFIELD * randomReal(.5, 1), vy - vx * DT * MAGNETICFIELD * randomReal(.5, 1)
        pos = vecSum(pos, vecMul(vecMul(vecSum(oldvel, vel), 0.5), DT))
        x, y = pos
        vx, vy = vel
        vx, vy = vecMul((vx, vy), 1 - DT * v/1000)
        if x>=SIZE_X-rad and vx>0:
            x = SIZE_X-rad
            vx *= -1

        if x<=rad and vx<0:
            x = rad
            vx *= -1

        if y>=SIZE_Y-rad and vy>0:
            y = SIZE_Y-rad
            vy *= -1

        if y<=rad and vy<0:
            y = rad
            vy *= -1

        pos = x, y
        vel = vx, vy
    return {
        "type": _type,
        "pos": pos, 
        "vel": vel,
        "rad": rad, 
        "ltm": ltm + DT,
        "col": col,
    }

def updateBallStates():
    '''
    Обновляет все состояние шариков
    '''
    for i, ball in enumerate(balls):
        balls[i] = updateBallState(balls[i])

def mouseButtonDown(event):
    '''
    Обрабатывает событие нажатия кнопки мыши
    '''
    x0, y0 = event.pos
    flag = False
    for i, ball in enumerate(balls):
        x, y = ball["pos"]
        r = ball["rad"]
        _type = ball["type"]
        if (x - x0)**2 + (y - y0)**2 <= r**2:
            updateScore(score + dScore(r, _type))
            print(dScore(r, _type))
            balls[i] = randomBallState()
            flag = True
    if not flag:
        updateScore(score - MISCLICK_FINE)
    pass

def dScore(r, _type):
    '''
    Приращение количества очков за нажатие на шарик
    r - радиус шарика
    '''
    if _type == "ball":
        return SIZE_X/NUMBER_OF_BALLS*V_MAX / (r+1)
    else:
        return SIZE_X/NUMBER_OF_BALLS*VPART_MAX / (r+1)

def updateScore(newScore):
    '''
    Обновляет количество очков
    '''
    global score
    score = newScore

def showScore():
    '''
    Выводит в консоль колчество очков
    '''
    print(score)

pygame.init()
SIZE_X, SIZE_Y = 500, 500

FPS = 100
DT = 1/FPS
time = 0

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (63, 63, 63)
BALLCOLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]
SCORECOLOR = (0, 255, 0)
PARTICLECOLORS = [WHITE, DARKGRAY]

score = 0
MISCLICK_FINE = 50
MAGNETICFIELD = 10
particleProbability = .2
R_MIN, R_MAX = 20, 50
V_MIN, V_MAX = 100, 300
LTM_MAX = 1000
VPART_MIN, VPART_MAX = 100, 300

NUMBER_OF_BALLS = 10
balls = []

for i in range(0, NUMBER_OF_BALLS):
    balls.append(randomBallState())

screen = pygame.display.set_mode((SIZE_X, SIZE_Y))
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseButtonDown(event)
    time += DT
    title = "Score: " + str(round(score)) + "  Score per second: " + str(round(score / time, 1))
    pygame.display.set_caption(str(title))
    updateBallStates()
    drawBalls()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()

