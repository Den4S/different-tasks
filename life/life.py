import copy
from tkinter import Tk, Canvas
import time
neighbors = []
cell = 20


def reading():  # Считывает условие из файла в двумерный список field[]
    field = open('life.txt', 'r').read()
    given = field.split()
    for i in range(len(given)):
        given[i] = int(given[i])
    f_width = given[1]
    f_height = given[0]
    field = []
    for i in range(f_height):
        field.append(given[(2 + i * f_width):(2 + (i + 1) * f_width)])
    return field


def neighbors_step(field, f_height, f_width):  # Возвращает матрицу: в каждой клетке количество её соседей
    for i in range(f_height):
        for j in range(f_width):
            for k_h in [-1, 0, 1]:
                for k_w in [-1, 0, 1]:
                    if ((i + k_h) >= 0) and ((i + k_h) <= (f_height - 1)):
                        if ((j + k_w) >= 0) and ((j + k_w) <= (f_width - 1)):
                            if field[i + k_h][j + k_w] == 1:
                                if (k_h != 0) or (k_w != 0):
                                    neighbors[i][j] = neighbors[i][j] + 1


def step(field, f_height, f_width):  # Переделывает поле в соответствии с правилами
    neighbors_step(field, f_height, f_width)
    for i in range(f_height):
        for j in range(f_width):
            if (field[i][j] == 0) and (neighbors[i][j] == 3):
                field[i][j] = 1
            if (field[i][j] == 1) and ((neighbors[i][j] < 2) or (neighbors[i][j] > 3)):
                field[i][j] = 0
            if (field[i][j] == 1) and ((neighbors[i][j] == 2) or (neighbors[i][j] == 3)):
                field[i][j] = 1
    return field


def print_field(field, window, canvas, f_height, f_width):  # Вывод поля
    # for i in range(f_height):
    #     for j in range(f_width):
    #         print(field[i][j], end=' ')
    #     print()
    canvas.delete("all")
    for i in range(f_height):
        for j in range(f_width):
            if field[i][j] == 1:
                canvas.create_rectangle((j + 1) * cell, (i + 1) * cell, (j + 1) * cell + cell, (i + 1) * cell + cell, fill='black', width=1)
            else:
                canvas.create_rectangle((j + 1) * cell, (i + 1) * cell, (j + 1) * cell + cell, (i + 1) * cell + cell, fill='white', width=1)
    window.update()
    time.sleep(0.1)


def life():  # Всё вместе
    field = reading()  # Чтение
    f_width = len(field[0])
    f_height = len(field)
    for i in range(f_height):
        neighbors.append([0] * f_width)
    window = Tk()
    canvas = Canvas(window, width=cell * (f_width + 2), height=cell * (f_height + 2))
    canvas.pack()
    print_field(field, window, canvas, f_height, f_width)
    flag_end = False
    while not flag_end:  # Запускаем "ЖИЗНЬ"!
        for i in range(f_height):
            for j in range(f_width):
                neighbors[i][j] = 0
        print()
        field_old = copy.deepcopy(field)
        field = step(field, f_height, f_width)
        if field_old == field:
            flag_end = True
        else:
            print_field(field, window, canvas, f_height, f_width)
    window.mainloop()


life()
