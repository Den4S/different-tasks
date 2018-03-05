from tkinter import Tk, Canvas
import time
import timeit
dict_cells_xy = {}  # Словарь: номер ячейки --> координата
window = Tk()
cell = 40
d = int(cell/10)
tim = 0


def reading():  # Считывает условие из файла в двумерный список board[]
    field = open('board.txt', 'r').read()
    given = field.split()
    for i in range(len(given)):
        given[i] = int(given[i])
    board = []
    for i in range(given[0]):
        board.append(given[(1 + i * given[0]):(1 + (i + 1) * given[0])])
    return board


def start_position(field):  # Возвращает поз. последней заполн. клетки, номер хода и кол-во 0-ей
    last_move = 0
    b_size = len(field)
    n_0 = 0
    start_x, start_y = 0, 0
    for i in range(b_size):
        for j in range(b_size):
            if field[i][j] > last_move:
                last_move = field[i][j]
                start_x = j
                start_y = i
    for i in range(b_size):
        n_0 = n_0 + field[i].count(0)
    return start_y, start_x, last_move, n_0


def possible_moves(field, y, x): # Возвращает возможные ходы
    pos_moves = []
    b_size = len(field)
    for move_y in [2, -2]:
        for move_x in [1, -1]:
            if ((y + move_y) >= 0) and ((y + move_y) <= (b_size - 1)):
                if ((x + move_x) >= 0) and ((x + move_x) <= (b_size - 1)):
                    if field[y + move_y][x + move_x] == 0:
                        pos_moves.append([move_y, move_x])
    for move_y in [1, -1]:
        for move_x in [2, -2]:
            if ((y + move_y) >= 0) and ((y + move_y) <= (b_size - 1)):
                if ((x + move_x) >= 0) and ((x + move_x) <= (b_size - 1)):
                    if field[y + move_y][x + move_x] == 0:
                        pos_moves.append([move_y, move_x])
    return pos_moves


def solving(field):  # Рекурсивная функция, решающая задачу. True - решаема, False - нет.
    y, x, n_move, n_0 = start_position(field)
    n_move = n_move + 1
    if n_0 == 0:
        return True
    pos_moves = possible_moves(field, y, x)
    for move in pos_moves:
        field[y + move[0]][x + move[1]] = n_move
        if solving(field):
            return True
        field[y + move[0]][x + move[1]] = 0
    return False


def show_move (from_xy, to_xy, canvas):
    canvas.create_oval((to_xy[0] + 1) * cell + int(cell / 2) - d, (to_xy[1] + 1) * cell + int(cell/2) - d,
                       (to_xy[0] + 1) * cell + int(cell / 2) + d, (to_xy[1] + 1) * cell + int(cell/2) + d,
                       fill='blue', width=0)
    canvas.create_line((from_xy[0] + 1) * cell + int(cell/2), (from_xy[1] + 1) * cell + int(cell/2),
                       (to_xy[0] + 1) * cell + int(cell / 2), (to_xy[1] + 1) * cell + int(cell/2),
                       width=2, arrow='last')
    window.update()
    time.sleep(0.3)


def print_answer(field, canvas):
    b_size = len(field)
    for i in range(b_size):
        for j in range(b_size):
            if field[i][j] == 1:
                canvas.create_rectangle((j + 1) * cell, (i + 1) * cell, (j + 1) * cell + cell, (i + 1) * cell + cell,
                                        fill='white', width=1)
                canvas.create_oval((j + 1) * cell + int(cell / 2) - d, (i + 1) * cell + int(cell / 2) - d,
                                   (j + 1) * cell + int(cell / 2) + d, (i + 1) * cell + int(cell / 2) + d,
                                   fill='red', width=0)
            else:
                canvas.create_rectangle((j + 1) * cell, (i + 1) * cell, (j + 1) * cell + cell, (i + 1) * cell + cell,
                                        fill='white', width=1)
    window.update()
    for i in range(b_size**2 - 1):
        show_move(dict_cells_xy[i+1], dict_cells_xy[i+2], canvas)



def play():
    given_board = reading()
    size = len(given_board)
    canvas = Canvas(window, width=cell * (size + 2), height=cell * (size + 2))
    canvas.pack()
    if solving(given_board):
        print(timeit.default_timer() - tim)
        for i in range(size):
            for j in range(size):
                dict_cells_xy[given_board[i][j]] = [j, i]
        print_answer(given_board, canvas)
        window.mainloop()
    else:
        print(timeit.default_timer() - tim)
        print("It's impossible!")


tim = timeit.default_timer()
play()  # Тело программы.
