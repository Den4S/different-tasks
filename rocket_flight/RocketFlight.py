import math
# Константы из условия
r_mass = 2000  # кг
f_mass = 1000  # кг
g = 9.81  # м/с^2
lim_ovrld = 2.943
f_speed = 3660  # м/с
lim_vx = 1  # м/с
lim_vy = 3  # м/с
v_x = 0; v_y = 0  # Начальные условия.
r_x = 0; r_y = 0
dt = 0.1
answer = open('maneuvers_output.txt', 'w')


def reading():  # Считывает условие из файла в двумерный список maneuvers[][].
    given = (open('maneuvers_input.txt', 'r').read()).split()
    for i in range(len(given)):
        given[i] = float(given[i])
    maneuvers = []
    for i in range(int(len(given)/3)):
        maneuvers.append(given[(i * 3):((i + 1) * 3)])
    return maneuvers


# Считаем, что в пределах промежуточка dt, движение равноускоренное.
def calculations(alpha, f_dm, d_t):  # Вычисляем значения v_x, v_y, r_x, r_y через dt.
    global v_x, v_y, r_x, r_y, g, f_mass, f_speed, r_mass
    afull_x = (math.cos(math.pi * alpha / 180) * f_dm * f_speed) / (r_mass + f_mass)  # Проекции полного ускорения согласно ур-ю Мещерского
    afull_y = (math.sin(math.pi * alpha / 180) * f_dm * f_speed) / (r_mass + f_mass) - g
    v_x = v_x + afull_x * d_t
    v_y = v_y + afull_y * d_t
    r_x = r_x + v_x * d_t + afull_x * d_t * d_t / 2
    r_y = r_y + v_y * d_t + afull_y * d_t * d_t / 2
    f_mass = f_mass - f_dm * dt
    if r_y < 0:  # Если аппарат "коснулся" земли.
        r_y = 0
        check_landing()  # Проверяем скорости посадки.
    # answer.write(str(afull_y) + '\t' + str(alpha) + '\n')
    # alpha = 180 * math.atan2(v_y, v_x) / math.pi
    return alpha


def check_landing():  # Проверям скорости при нашей посадке и завершаем программу.
    global v_x, v_y, r_x, r_y, lim_vx, lim_vy, answer
    if (abs(v_x) > lim_vx) or (-v_y > lim_vy):
        answer.write(str(round(v_x)) + '\t\t' + str(round(v_y)) + '\t\t' + str(round(r_x)) + '\t\t'
                     + str(round(r_y)) + '\n')
        answer.write("Landing failed!")
    else:
        answer.write(str(round(v_x)) + '\t\t' + str(round(v_y)) + '\t\t' + str(round(r_x)) + '\t\t'
                     + str(round(r_y)) + '\n')
        answer.close()
        answer.write("Landing succeeded!")
    exit()


def make_step(angle, f_consumption, m_time):  # Совершаем маневр.
    global dt, r_x, r_y
    for i in range(int(m_time / dt)):
        calculations(angle, f_consumption, dt)
        # angle = calculations(angle, f_consumption, dt)
        # print(round(v_x), round(v_y), round(r_x), round(r_y), sep="\t\t")
    tau = m_time - int(m_time / dt) * dt
    calculations(angle, f_consumption, tau)


def fall():  # Падение.
    global v_x, v_y, r_x, r_y, dt, answer
    angle = 180 * math.atan2(v_y, v_x) / math.pi
    answer.write("FALL: ")
    while r_y > 0:
        angle = calculations(angle, 0, dt)
        # print(round(v_x), round(v_y), round(r_x), round(r_y), sep="\t\t")


def flight(maneuvers):  # Пробегаем по maneuvers[][] и последовательно выполняем все маневры.
    global v_x, v_y, r_x, r_y, dt, answer
    for i in range(len(maneuvers)):  # Выполняем все маневры.
        make_step(maneuvers[i][0], maneuvers[i][1], maneuvers[i][2])
        answer.write(str(round(v_x)) + '\t\t' + str(round(v_y)) + '\t\t' + str(round(r_x)) + '\t\t'
                     + str(round(r_y)) + '\n')
    fall()
    answer.close()


flight(reading())
