import sys
from tkinter import *
import random
from PIL import Image, ImageTk

BOARD_WIDTH = 400

BOARD_HEIGHT = 600

CELL_SIZE = 20

doodleX = 200
doodleY = 500

ANCHOR_Gravity_Down = True
JUMP_HIGHT = 9
Spec_Iter = 0


IN_GAME = True



def loadImages():
    global doodle, plat
    idoodle = Image.open("img/doodle_main.png")
    doodle = ImageTk.PhotoImage(idoodle)
    iplatform = Image.open("img/platform_main.png")
    plat = ImageTk.PhotoImage(iplatform)


class Score(object):

    # функция отображения очков на экране
    def __init__(self):
        self.score = 0
        c.create_text(
            30, 10, text="Счет: {0}".format(self.score),
            fill="white", tags="score"
        )

    def increment(self):
        c.delete("score")
        self.score += 1
        c.create_text(
            30, 10, text="Счет: {0}".format(self.score),
            fill="white", tags="score"
        )

    def reset(self):
        c.delete("score")
        self.score = 0

class Doodle(object):

    def __init__(self, x, y):
        self.instance = c.create_rectangle(x - CELL_SIZE / 2, y - CELL_SIZE / 2,
                                           x + CELL_SIZE / 2, y + CELL_SIZE / 2,
                                           )
        self.mapping = {"d": (2, 0), "a": (-2, 0), "no": (0, 0)}

        # инициируем направление движения
        self.vector = self.mapping["no"]

    def move(self, upOrDown):
        x1, y1, x2, y2 = c.coords(self.instance)
        if x2 > BOARD_WIDTH:
            x2 -= BOARD_WIDTH
            x1 -= BOARD_WIDTH
            c.coords(self.instance,
                     x1 + self.vector[0] * CELL_SIZE, y1 + (1 if upOrDown else -1) * CELL_SIZE,
                     x2 + self.vector[0] * CELL_SIZE, y2 + (1 if upOrDown else -1) * CELL_SIZE)

            c.move(img_doodl,
                   self.vector[0] * CELL_SIZE - BOARD_WIDTH,
                   (1 if upOrDown else -1) * CELL_SIZE)

            self.vector = self.mapping["no"]
        elif x1 < 0:
            x2 += BOARD_WIDTH
            x1 += BOARD_WIDTH
            c.coords(self.instance,
                     x1 + self.vector[0] * CELL_SIZE, y1 + (1 if upOrDown else -1) * CELL_SIZE,
                     x2 + self.vector[0] * CELL_SIZE, y2 + (1 if upOrDown else -1) * CELL_SIZE)

            c.move(img_doodl,
                   self.vector[0] * CELL_SIZE + BOARD_WIDTH,
                   (1 if upOrDown else -1) * CELL_SIZE)

            self.vector = self.mapping["no"]

        else:
            c.coords(self.instance,
                     x1 + self.vector[0] * CELL_SIZE, y1 + (1 if upOrDown else -1) * CELL_SIZE,
                     x2 + self.vector[0] * CELL_SIZE, y2 + (1 if upOrDown else -1) * CELL_SIZE)

            c.move(img_doodl,
                   self.vector[0] * CELL_SIZE,
                   (1 if upOrDown else -1) * CELL_SIZE)

            self.vector = self.mapping["no"]




    def change_direction(self, event):
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_doodle(self):
        c.delete(self.instance)


class Platform:
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x - CELL_SIZE, y - CELL_SIZE / 8,
                                           x + CELL_SIZE, y + CELL_SIZE / 8,
                                           )

    @staticmethod
    def reset_Platforms():
        for plat in platforms:
            c.delete(plat.instance)


    @staticmethod
    def move(platforms, plat_imgs):
        for i in range(0, len(platforms)):
            x1, y1, x2, y2 = c.coords(platforms[i].instance)

            if y1 > BOARD_HEIGHT:
                y1 -= BOARD_HEIGHT
                y2 -= BOARD_HEIGHT
                y = (y1 + y2)/2
                y1 = y - CELL_SIZE / 8
                y2 = y + CELL_SIZE / 8
                tmp_x1 = x1
                tmp_x2 = x2
                tmp_x = (tmp_x1 + tmp_x2)/2
                x = random.randint(CELL_SIZE, BOARD_WIDTH - CELL_SIZE)
                x1 = x - CELL_SIZE
                x2 = x + CELL_SIZE

                c.coords(platforms[i].instance,
                         x1, y1,
                         x2, y2)
                c.move(plat_imgs[i], x - tmp_x, -BOARD_HEIGHT)
            else:
                c.coords(platforms[i].instance,
                         x1, y1 + 1.5 * CELL_SIZE,
                         x2, y2 + 1.5 * CELL_SIZE)
                c.move(plat_imgs[i], 0, 1.5 * CELL_SIZE)







def create_platforms():
    global plat_imgs, platforms
    r1 = random.randint(CELL_SIZE, BOARD_WIDTH - CELL_SIZE)
    r2 = random.randint(CELL_SIZE, BOARD_WIDTH - CELL_SIZE)
    r3 = random.randint(CELL_SIZE, BOARD_WIDTH - CELL_SIZE)
    r4 = random.randint(int(BOARD_HEIGHT*0.6), int(BOARD_HEIGHT*0.8))
    r5 = random.randint(int(BOARD_HEIGHT*0.4), int(BOARD_HEIGHT*0.6))
    r6 = random.randint(int(BOARD_HEIGHT*0.2), int(BOARD_HEIGHT*0.4))
    plat_imgs = [c.create_image(doodleX, doodleY, image=plat, tag="plt0"),
                 c.create_image(r1, r4, image=plat, tag="plt1"),
                 c.create_image(r2, r5, image=plat, tag="plt2"),
                 c.create_image(r3, r6, image=plat, tag="plt3")]

    platforms =[Platform(doodleX, doodleY),
                Platform(r1, r4),
                Platform(r2, r5),
                Platform(r3, r6)]



def main():
    """ Моделируем игровой процесс """
    global IN_GAME, Spec_Iter, ANCHOR_Gravity_Down, JUMP_HIGHT
    if IN_GAME:
        if ANCHOR_Gravity_Down:
            dood.move(True)
        elif ANCHOR_Gravity_Down == False and Spec_Iter < JUMP_HIGHT:
            dood.move(False)
            Spec_Iter += 1
            if Spec_Iter == JUMP_HIGHT:
                ANCHOR_Gravity_Down = True
                Spec_Iter = 0
        else:
            ANCHOR_Gravity_Down = True
            Spec_Iter = 0

        if not ANCHOR_Gravity_Down:
            Platform.move(platforms, plat_imgs)

        # Определяем координаты doodle
        x1, y1, x2, y2 = c.coords(dood.instance)
        for i in range(0, len(platforms)):
            x3, y3, x4, y4 = c.coords(platforms[i].instance)
            left = max(x1, x3)
            top = min(y2, y4)
            right = min(x2, x4)
            bottom = max(y1, y3)
            width = right - left
            height = top - bottom
            if (width >= 0 and height >= 0):
                ANCHOR_Gravity_Down = False
                score.increment()

        # столкновение с низом
        if y1 > BOARD_HEIGHT and ANCHOR_Gravity_Down:
            IN_GAME = False




        root.after(100, main)
    # Не IN_GAME -> останавливаем игру и выводим сообщения
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')
        set_state(close_but, 'normal')


def set_state(item, state):
    c.itemconfigure(item, state=state)

# Функция для старта игры
def start_game():
    global dood, platforms, img_doodl, plat_imgs
    loadImages()

    dood = Doodle(doodleX, doodleY-200)
    img_doodl = c.create_image(doodleX, doodleY - 200, image=doodle, tag="doodle")
    create_platforms()

    # Реагируем на нажатие клавиш
    c.bind("<KeyPress>", dood.change_direction)
    main()

def clicked(event):
    global IN_GAME
    dood.reset_doodle()
    Platform.reset_Platforms()
    IN_GAME = True
    score.reset()
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    c.itemconfigure(close_but, state='hidden')
    start_game()


def close_win(root):
    exit()

# Настройка главного окна
root = Tk()
root.resizable(width=False, height=False)
root.title("Doodle Jump")

# Создаем экземпляр класса Canvas
c = Canvas(root, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg="blue")
c.grid()

# Захватываем фокус для отлавливания нажатий клавиш
c.focus_set()

# Текст результата игры
game_over_text = c.create_text(BOARD_WIDTH / 2, BOARD_HEIGHT / 2, text="Game Over!",
                               font='Arial 20', fill='red',
                               state='hidden')

# Текст начала новой игры после проигрыша
restart_text = c.create_text(BOARD_WIDTH / 2, BOARD_HEIGHT - BOARD_HEIGHT / 3,
                             font='Arial 25',
                             fill='green',
                             text="New Game",
                             state='hidden')

# Текст выхода из программы после проигрыша
close_but = c.create_text(BOARD_WIDTH / 2, BOARD_HEIGHT - BOARD_HEIGHT / 5, font='Arial 25',
                          fill='green',
                          text="Exit",
                          state='hidden')

# Отработка событий при нажимания кнопок
c.tag_bind(restart_text, "<Button-1>", clicked)
c.tag_bind(close_but, "<Button-1>", close_win)

# Считаем очки
score = Score()

# Запускаем игру
start_game()

root.mainloop()
