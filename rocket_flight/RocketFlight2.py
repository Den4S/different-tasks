import math
# Константы из условия
r_mass = 2000  # кг
f_mass = 1000  # кг
f_mass0 = 1000
g = 1.62  # м/с^2
lim_ovrld = 3
f_speed = 3660  # м/с
lim_vx = 1  # м/с
lim_vy = 3  # м/с
v_x = 0; v_y = 0  # Начальные условия.
r_x = 0; r_y = 0
dt = 0.01; n_after_p = 2
f_spent = 0  # Потраченное топливо.
good_landing = False
answer = open('flight_output.txt', 'w')
a_check = 0


# Поймем, что максимальное перемещение вдоль оси x аппарат совершит, если перемещений вдоль оси y
# почти не будет. Т.е. считаем, что на протяжении всего полета v_y = 0, afull_y = 0, r_y = 0.
# Сила тяги должна немножко отрывать корабль от земли,
def calculations_acceleration():  # Вычисляем значения v_x, v_y, r_x, r_y через dt. Ускорение.
    global v_x, v_y, r_x, r_y, g, f_mass, r_mass, f_speed, lim_ovrld, f_spent, a_check
    # Какие ускорения хотим.
    afull_x = lim_ovrld * g  # afull_y = 0
    alpha = math.atan2(1, lim_ovrld)
    f_dm = (r_mass + f_mass) * lim_ovrld * g / (math.cos(alpha) * f_speed)  # Расчет расхода и угла для маневра.
    a_check = (math.cos(alpha) * f_dm * f_speed) / (g * (r_mass + f_mass))
    v_x = v_x + afull_x * dt  # v_y = 0
    r_x = r_x + v_x * dt + afull_x * dt * dt / 2  # r_y = 0
    f_mass = f_mass - f_dm * dt
    f_spent = f_spent + f_dm * dt
    return alpha, f_dm


def calculations_braking():  # Вычисляем значения v_x, v_y, r_x, r_y через dt. Торможение.
    global v_x, v_y, r_x, r_y, g, f_mass, r_mass, f_speed, lim_ovrld, f_spent, a_check
    # Какие ускорения хотим.
    afull_x = -lim_ovrld * g  # afull_y = 0
    alpha = math.pi - math.atan2(1, lim_ovrld)
    f_dm = abs((r_mass + f_mass) * lim_ovrld * g / (math.cos(alpha) * f_speed)) # Расчет расхода и угла для маневра.
    a_check = (math.cos(alpha) * f_dm * f_speed) / (g * (r_mass + f_mass))
    v_x = v_x + afull_x * dt  # v_y = 0
    r_x = r_x + v_x * dt + afull_x * dt * dt / 2  # r_y = 0
    f_mass = f_mass - f_dm * dt
    f_spent = f_spent + f_dm * dt
    return alpha, f_dm


def check_landing():  # Проверям скорости при нашей посадке и завершаем программу.
    global v_x, v_y, r_x, r_y, lim_vx, lim_vy, good_landing
    if abs(v_x) > lim_vx:
        good_landing = False
    else:
        good_landing = True


def check_flight(f_mass_a):  # Проверяем возможность полета, если на разгон потратим f_mass_a топлива.
    global dt, f_spent, good_landing
    while f_spent < f_mass_a:
        calculations_acceleration()
    while f_spent < f_mass:
        calculations_braking()
    check_landing()
    # answer.write(str(good_landing) + '\t' + str(f_mass_a) + '\t' + str(v_x) + '\n')
    return good_landing


def create_steps(f_mass_a):  # Записываем маневры в файл по найденному f_mass_a, для которого с посадеой все ОК.
    global v_x, v_y, r_x, r_y, dt, f_mass, f_mass0, f_spent, answer, a_check, n_after_p
    f_spent = 0; v_x = 0; v_y = 0; r_x = 0; r_y = 0; f_mass = f_mass0  # Возвращаем начальные условия.
    f_dm0 = 0; t_sum = dt
    while f_spent < f_mass_a:
        alpha, f_dm = calculations_acceleration()
        if round(f_dm * dt, 4) == round(f_dm0 * dt, 4):
            t_sum = t_sum + dt
        else:
            answer.write(str(round(180 * alpha / math.pi, 2)) + '\t\t' + str(round(f_dm * t_sum, 4)) + '\t\t'
                         + str(round(t_sum, n_after_p)) + '\n')
            f_dm0 = f_dm
            t_sum = dt
    f_dm0 = 0; t_sum = dt
    while f_spent < f_mass0:
        alpha, f_dm = calculations_braking()
        if round(f_dm * dt, 4) == round(f_dm0 * dt, 4):
            t_sum = t_sum + dt
        else:
            answer.write(str(round(180 * alpha / math.pi, 2)) + '\t\t' + str(round(f_dm * t_sum, 4)) + '\t\t'
                         + str(round(t_sum, n_after_p)) + '\n')
            f_dm0 = f_dm
            t_sum = dt
    answer.close()
    exit()


def calculations_flight():
    global f_mass, f_spent, good_landing, dt, answer, r_x, v_x, f_mass0
    f_mass_a = f_mass0
    while (not check_flight(f_mass_a)) and (f_mass_a > 0):  # Ищем заветное количество топлива на разгон.
        f_mass_a = f_mass_a - 1
        r_x = 0
        v_x = 0
        f_spent = 0
        f_mass = f_mass0
    answer.write('f_mass_a = ' + str(f_mass_a) + ' кг;  ' + 'Vx_end = ' + str(v_x) + ' м/с;  ' + 'Lmax = '
                 + str(round(r_x, 3)) + ' м;' + '\n\n')
    create_steps(f_mass_a)


calculations_flight()
