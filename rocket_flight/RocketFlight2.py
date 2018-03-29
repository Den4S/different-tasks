import math, timeit
# Константы из условия
r_mass = 2150  # кг
f_mass = 1000  # кг
f_mass0 = 1000
g = 1.62  # м/с^2
lim_ovrld = 29.43
f_speed = 3660  # м/с
lim_vx = 1  # м/с
lim_vy = 3  # м/с
v_x = 0; v_y = 0  # Начальные условия.
r_x = 0; r_y = 0
dt = 0.01; n_after_p = 3
f_spent = 0  # Потраченное топливо.
good_landing = False
answer = open('flight_output2.txt', 'w')
alpha0 = 45
angle = 0


def calculations_acceleration():  # Вычисляем значения v_x, v_y, r_x, r_y через dt. Ускорение.
    global v_x, v_y, r_x, r_y, g, f_mass, r_mass, f_speed, lim_ovrld, f_spent, dt, alpha0, angle
    afull_x = math.cos(math.pi * alpha0 / 180) * lim_ovrld
    afull_y = (lim_ovrld ** 2 - afull_x ** 2) ** 0.5
    angle = math.atan2((afull_y + g), afull_x) * 180 / math.pi
    f_dm = (r_mass + f_mass) * afull_x / (math.cos(math.pi * alpha0 / 180) * f_speed)  # Расчет расхода и угла для маневра.
    v_x = v_x + afull_x * dt  # v_y = 0
    v_y = v_y + afull_y * dt
    r_x = r_x + v_x * dt + afull_x * dt * dt / 2
    r_y = r_y + v_y * dt + afull_y * dt * dt / 2
    f_mass = f_mass - f_dm * dt
    f_spent = f_spent + f_dm * dt
    return f_dm


def calculations_braking():  # Вычисляем значения v_x, v_y, r_x, r_y через dt. Торможение.
    global v_x, v_y, r_x, r_y, g, f_mass, r_mass, f_speed, lim_ovrld, f_spent, dt, alpha0
    afull_x = - math.cos(math.pi * alpha0 / 180) * lim_ovrld
    afull_y = (lim_ovrld ** 2 - afull_x ** 2) ** 0.5
    f_dm = abs((r_mass + f_mass) * afull_x / (math.cos(math.pi * alpha0 / 180) * f_speed))  # Расчет расхода и угла для маневра.
    v_x = v_x + afull_x * dt  # v_y = 0
    v_y = v_y + afull_y * dt
    r_x = r_x + v_x * dt + afull_x * dt * dt / 2
    r_y = r_y + v_y * dt + afull_y * dt * dt / 2
    f_mass = f_mass - f_dm * dt
    f_spent = f_spent + f_dm * dt
    if r_y <= 0:  # Если аппарат "коснулся" земли.
        r_y = 0
    return f_dm


def fall():  # Вычисляем значения v_x, v_y, r_x, r_y через dt.
    global v_x, v_y, r_x, r_y, g, f_mass, f_speed, r_mass, dt
    afull_y = -g  # afull_x = 0
    v_y = v_y + afull_y * dt
    r_x = r_x + v_x * dt
    r_y = r_y + v_y * dt + afull_y * dt * dt / 2


def check_landing():  # Проверям скорости при нашей посадке и завершаем программу.
    global v_x, v_y, r_x, r_y, lim_vx, lim_vy, good_landing
    if (abs(v_x) <= lim_vx) and (abs(v_y) <= lim_vy):
        good_landing = True
    else:
        good_landing = False


def check_flight(f_mass_a):  # Проверяем возможность полета, если на разгон потратим f_mass_a топлива.
    global dt, f_spent, good_landing, v_y
    while f_spent < f_mass_a:
        calculations_acceleration()
    v_ynew = -v_y
    while v_y >= v_ynew:
        fall()
    while (f_spent < f_mass0) and (r_y > 0):
        calculations_braking()
    check_landing()
    return good_landing


def create_steps(f_mass_a):  # Записываем маневры в файл по найденному f_mass_a, для которого с посадеой все ОК.
    global v_x, v_y, r_x, r_y, dt, f_mass, f_mass0, f_spent, answer, n_after_p
    f_spent = 0; v_x = 0; v_y = 0; r_x = 0; r_y = 0; f_mass = f_mass0  # Возвращаем начальные условия.
    f_dm0 = 0; t_sum = dt
    while f_spent < f_mass_a:
        f_dm = calculations_acceleration()
        if round(f_dm * dt, 4) == round(f_dm0 * dt, 4):
            t_sum = t_sum + dt
        else:
            answer.write(str(round(angle, 2)) + '\t\t' + str(round(f_dm * t_sum, 4)) + '\t\t'
                         + str(round(t_sum, n_after_p)) + '\n')
            f_dm0 = f_dm
            t_sum = dt
    v_ynew = - v_y
    t_fall = 0
    while v_y > v_ynew:
        t_fall = t_fall + dt
        fall()
    answer.write(str(round(0, 2)) + '\t\t' + str(round(0, 4)) + '\t\t' + str(round(t_fall, n_after_p)) + '\n')
    f_dm0 = 0; t_sum = dt
    while (f_spent < f_mass0) and (r_y != 0):
        f_dm = calculations_braking()
        if round(f_dm * dt, 4) == round(f_dm0 * dt, 4):
            t_sum = t_sum + dt
        else:
            answer.write(str(round(180 - angle, 2)) + '\t\t' + str(round(f_dm * t_sum, 4)) + '\t\t'
                         + str(round(t_sum, n_after_p)) + '\n')
            f_dm0 = f_dm
            t_sum = dt
    answer.close()
    exit()


def calculations_flight():
    global f_mass, f_spent, good_landing, dt, answer, r_x, r_y, v_x, v_y, f_mass0
    f_mass_a = 700
    while (not check_flight(f_mass_a)) and (f_mass_a > 0):  # Ищем заветное количество топлива на разгон.
        f_mass_a = f_mass_a - 0.1
        r_x = 0; r_y = 0; v_x = 0; v_y = 0; f_spent = 0
        f_mass = f_mass0
    answer.write('f_mass_a = ' + str(round(f_mass_a, 2)) + ' кг;  ' + 'Vx_end = ' + str(round(v_x, 3)) + ' м/с;  ' + 'Lmax = '
                 + str(round(r_x, 3)) + ' м;' + '\n\n')
    create_steps(f_mass_a)


tim = timeit.default_timer()
calculations_flight()
print(timeit.default_timer() - tim)
