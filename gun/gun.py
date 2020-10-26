from random import randrange as rnd, choice
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(master=root)
root.geometry('800x600')
canv = tk.Canvas(master=root, bg='white')
canv.pack(side='bottom', fill='both', expand=1)
label = tk.Label(master=root, text="")
label.pack(side='top', fill='x')
class Ball:
    def __init__(self, x=40, y=450):
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
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r, 
                self.y - self.r,
                self.x + self.r, 
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

    def set_coords(self):
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
        if self.y <= 500:
            self.vy -= 100*t
            self.y -= self.vy*t
            self.x += self.vx*t
            self.vx *= 1-0.01*t
            self.set_coords()
        else:
            if self.vx ** 2 + self.vy ** 2 > 10:
                self.vy = -self.vy / 2
                self.vx = self.vx / 2
                self.y = 499
            if self.live < 0:
                balls.pop(balls.index(self))
                canv.delete(self.id)
            else:
                self.live -= 1
        if self.x > 780:
            self.vx = -self.vx * 0.9
            self.x = 779

    def hittest(self, ob):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if abs(ob.x - self.x) <= self.r + ob.r and abs(ob.y - self.y) \
            <= self.r + ob.r:
            return True
        else:
            return False

    def delete(self):
        self.x = -1000
        self.set_coords()

class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7)

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
        self.an = math.atan((event.y - new_ball.y) / (event.x
                            - new_ball.x))
        new_ball.vx = 10*self.f2_power * math.cos(self.an)
        new_ball.vy = -10*self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450, 20 + max(self.f2_power, 20)
                    * math.cos(self.an), 450 + max(self.f2_power, 20)
                    * math.sin(self.an))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class Target:
    def __init__(self):
        self.points = 0
        self.id = canv.create_oval(0, 0, 0, 0)
        self.id_points = canv.create_text(30, 30, text=self.points,
                font='28')
        self.new_target()
        self.live = 1


    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        self.vx = rnd(-500, 500)
        self.vy = rnd(-500, 500)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points
        canv.itemconfig(self.id_points, text=self.points)
    def move(self, t):
        self.x += self.vx*t
        self.y += self.vy*t
        if self.x >= 750 and self.vx > 0:
            self.x = 750
            self.vx *= -1
        if self.x <= 300 and self.vx < 0:
            self.x = 300
            self.vx *= -1
        if self.y >= 550 and self.vy > 0:
            self.y = 550
            self.vy *= -1
        if self.y <= 300 and self.vy < 0:
            self.y = 300
            self.vy *= -1
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        canv.itemconfig(self.id, fill=self.color)


targets_cnt = 3
targets = [0] * targets_cnt
screen1 = canv.create_text(400, 300, text='', font='28')
g = Gun()
bullet = 0
balls = []


def new_game(event=''):
    global Gun, targets, screen1, balls, bullet
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
    z = 0.03

    while alive_cnt:
        for b in balls:
            b.move(z)
            for t in targets:
                if b.hittest(t) and t.live:
                    t.live = 0
                    t.hit()
                    alive_cnt -= 1
        for t in targets:
            if t.live:
                t.move(z)
        canv.update()
        time.sleep(z)
        g.targetting()
        g.power_up()

    canv.bind('<Button-1>', '')
    canv.bind('<ButtonRelease-1>', '')
    label.config(text='Вы уничтожили цели за '
            + str(bullet)
            + ' выстрелов'
    )
    canv.update()
    for b in balls:
        b.delete()
    canv.delete(Gun)
    
    root.after(5000, new_game)


new_game()
root.mainloop()
