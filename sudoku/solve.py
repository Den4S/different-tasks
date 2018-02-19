import timeit


def reading():  # Процедура считывающая условие из файла в список given[].
    field = open('sudoku.txt', 'r').read()
    given = field.split()
    for i in range(len(given)):
        given[i] = int(given[i])
    return given


def empty_pos(task_now):  # Процедура, возвращающая номер первого 0-ого элемента или -1, если такого нет.
    for i in range(len(task_now)):
        if task_now[i] == 0:
            return i
    return -1


def possible_val(k, task_now):  # Процедура, возвращающая список can_use[] цифр, которые мы можем поставить в ячейку k.
    line_i = int(k / 9)
    column_i = k - line_i * 9
    can_use = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):  # Проверяем что уже нельзя использовать, т.к. использовано в столбце и строке.
        if (task_now[column_i + 9 * i] != 0) and (task_now[column_i + 9 * i] in can_use):
            can_use.remove(task_now[column_i + 9 * i])
        if (task_now[line_i * 9 + i] != 0) and (task_now[line_i * 9 + i] in can_use):
            can_use.remove(task_now[line_i * 9 + i])
    cell_x = int(column_i / 3)
    cell_y = int(line_i / 3)
    cell_0 = cell_x * 3 + cell_y * 27
    for i in range(3):  # Проверяем что уже нельзя использовать, т.к. использовано в клетке 3*3.
        for j in range(3):
            if (task_now[cell_0 + j + 9 * i] != 0) and (task_now[cell_0 + j + 9 * i] in can_use):
                can_use.remove(task_now[cell_0 + j + 9 * i])
    return can_use


def solving(task):  # Рекурсивная функция, решающая задачу. True - решаема, False - нет.
    k = empty_pos(task)
    if k == -1:
        return True
    can_use = possible_val(k, task)
    for t in can_use:
        task[k] = t
        if solving(task):
            return True
        task[k] = 0
    return False


def check(answer):  # Проверка корректности ответа по правилам.
    for column_i in range(9):
        nine = []
        for i in range(9):
            num = answer[column_i + 9 * i]
            if num != 0:
                if num in nine:
                    return False
                else:
                    nine.append(num)
    for line_i in range(9):
        nine = []
        for i in range(9):
            num = answer[line_i * 9 + i]
            if num != 0:
                if num in nine:
                    return False
                else:
                    nine.append(num)
    for cell0 in range(0, 3, 81):
        nine = []
        if cell0 > 80:
            break
        for i in range(3):
            for j in range(3):
                num = answer[cell0 + j + 9 * i]
                if num != 0:
                    if num in nine:
                        return False
                    else:
                        nine.append(num)
    return True


def start():  # Процедура, которая вызывается в теле программы.
    task = reading()
    for k in range(int(len(task) / 81)):
        print('Sudoku', k, ':')
        task_i = task[k * 81:(k+1) * 81]
        solvable = solving(task_i)
        if solvable and check(task_i):
            for i in range(len(task_i)):
                if (i + 1) % 9 == 0:
                    print(task_i[i])
                    if (i + 1) % 27 == 0:
                        print()
                else:
                    if (i + 1) % 3 == 0:
                        print(task_i[i], end='   ')
                    else:
                        print(task_i[i], end=' ')
        else:
            print('The task condition is incorrect!')
    if len(task) / 81 != int(len(task) / 81):
        print('The task condition is incorrect!')


tim = timeit.default_timer()
start()  # Тело программы.
print(timeit.default_timer() - tim)