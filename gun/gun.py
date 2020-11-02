from random import randrange as rnd, choice
import tkinter as tk
import math
import time

accX = 0
accY = 30
visc = 1
canvasSize = 1000, 500
canvasX, canvasY = canvasSize

root = tk.Tk()

canv = tk.Canvas(master=root, bg='white', width=canvasX, height=canvasY)
canv.pack(side='bottom', fill='both', expand=1)

label = tk.Label(master=root, text="")
label.pack(side='top', fill='x', expand=0)

class Ball:
    def __init__(self, x=10, y=canvasY-10):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'magenta', 'yellow', 'lime'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

    def draw(self):
        canv.coords(
                self.id, 
                self.x - self.r, 
                self.y - self.r, 
                self.x + self.r, 
                self.y + self.r
        )

    def move(self, t):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        self.vx += accX * t
        self.vy += accY * t

        self.vx *= 1 - visc * t
        self.vy *= 1 - visc * t

        self.x += self.vx*t - accX * t**2 / 2
        self.y += self.vy*t - accY * t**2 / 2
        
        if self.y >= canvasY - self.r and self.vy > 0:
            self.y = canvasY - self.r
            self.vy *= -1
            self.live -= 1

        if self.y <= self.r and self.vy < 0:
            self.y = self.r
            self.vy *= -1
            self.live -= 1

        if self.x >= canvasX - self.r and self.vx > 0:
            self.x = canvasX - self.r
            self.vx *= -1
            self.live -= 1

        if self.x <= self.r and self.vx < 0:
            self.x = self.r
            self.vx *= -1
            self.live -= 1


        if self.live < 0:
            balls.pop(balls.index(self))
            canv.delete(self.id)



    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return (obj.x - self.x)**2 + (obj.y - self.y)**2 <= (obj.r + self.r)**2

    def delete(self):
        self.x = -1000
        self.y = -1000
        self.draw()

class Gun:
    def __init__(self):
        self.f2_power = 0.1
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(10, canvasY-10, 50, canvasY-10, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball()
        new_ball.r += 5
        self.an = math.atan2(event.y - new_ball.y, event.x - new_ball.x)
        new_ball.vx = 1000 * self.f2_power * math.cos(self.an)
        new_ball.vy = 1000 * self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 0.1

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - canvasY+10) / (event.x - 10))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 
                10, 
                canvasY-10, 
                10 + 50 * max(self.f2_power, 0.5) * math.cos(self.an), 
                canvasY-10 + 50 * max(self.f2_power, 0.5) * math.sin(self.an)
        )

    def power_up(self, t):
        if self.f2_on:
            if self.f2_power < 1:
                self.f2_power += t
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class Target:
    def __init__(self):
        self.id = canv.create_oval(0, 0, 0, 0)
        self.new_target()
        self.live = 1

    def new_target(self):
        """ Инициализация новой цели. """
        r = self.r = rnd(2, 50)
        x = self.x = rnd(r, canvasX - r)
        y = self.y = rnd(r, canvasY - r)
        vx = self.vx = rnd(-500, 500)
        vy = self.vy = rnd(-500, 500)
        
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def delete(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)

    def move(self, t):
        self.vx += accX * t
        self.vy += accY * t

        # self.vx *= 1 - visc * t
        # self.vy *= 1 - visc * t

        self.x += self.vx*t - accX * t**2 / 2
        self.y += self.vy*t - accY * t**2 / 2
        
        if self.y >= canvasY - self.r and self.vy > 0:
            self.y = canvasY - self.r
            self.vy *= -1

        if self.y <= self.r and self.vy < 0:
            self.y = self.r
            self.vy *= -1

        if self.x >= canvasX - self.r and self.vx > 0:
            self.x = canvasX - self.r
            self.vx *= -1

        if self.x <= self.r and self.vx < 0:
            self.x = self.r
            self.vx *= -1

    def draw(self):
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        canv.itemconfig(self.id, fill=self.color)


targets_cnt = 20
targets = [0] * targets_cnt
# screen1 = canv.create_text(400, 300, text='', font='28')
g = Gun()
bullet = 0
balls = []


def new_game(event=''):
    global Gun, targets, balls, bullet
    label.config(text='')
    alive_cnt = targets_cnt
    targets = [0] * targets_cnt
    for i in range(targets_cnt):
        targets[i] = Target()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g.fire2_start)
    canv.bind('<ButtonRelease-1>', g.fire2_end)
    canv.bind('<Motion>', g.targetting)
    z = 0.01
    points = 0
    while alive_cnt:
        for b in balls:
            b.move(z)
            b.draw()
            for t in targets:
                if b.hittest(t) and t.live:
                    t.live = 0
                    t.delete()
                    points += 1
                    alive_cnt -= 1
        for t in targets:
            if t.live:
                t.move(z)
                t.draw()
        label.config(text=f'Вы уничтожили {points} целей за {bullet} выстрелов')
        canv.update()
        time.sleep(z)
        g.targetting()
        g.power_up(z)

    canv.bind('<Button-1>', '')
    canv.bind('<ButtonRelease-1>', '')
    label.config(text=f'Вы уничтожили все цели за {bullet} выстрелов')
    canv.update()
    for t in targets:
        t.delete()
    for b in balls:
        b.delete()
    canv.delete(Gun)
    
    root.after(2000, new_game)


new_game()
root.mainloop()
