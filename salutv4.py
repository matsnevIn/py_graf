import pygame
import random
import math
import copy

MX = MY = 128		# Размер массива для взрыва

scale = 5               # Масштаб точек для вывода на экран

SX = MX * scale         # Размер экрана исходя из размера плазмы и ее масштаба
SY = MX * scale

scr = []                # Промежуточный список для хранения экрана
line = [0] * MX         # Создаем список из нулей длиной MX
scr = []                # Создаем список списков из нулей длиной MY, в итоге получится квадратная таблица из нулей.
for y in range(0, MY):
    scr.append(copy.deepcopy(line))

pygame.init()
screen = pygame.display.set_mode((SX, SY))
running = True

pal = []                # Палитра для графического эффекта
                        # Палитра почти как для пламени, но немного больше.
for i in range(0, 64):
    pal.append([i*4, 0, 0])
for i in range(64, 128):
    pal.append([255, i*4 - 255, 0])
for i in range(128, 255):
    pal.append([255, 255, round((i*4-128)/4)])

numParticle = 500       # Общее количество частиц

gravity = 0.08          # Коэффициент гравитации

particles = []                          # Список с частицами
for i in range(0, numParticle):         # Инициализируем список пустыми значениями
    particles.append([0, 0, 0, 0, 0])

# Для простоты ориентации в списке частиц, сделаем отдельные переменные для номеров ячеек отдельной частицы:
_x = 0              # номер координаты X
_y = 1              # номер координаты Y
_dirx = 2           # номер направления по X
_diry = 3           # номер направления по Y
_color = 4          # номер цвета

time = 0            # Счетчик времени существования взрыва на экране

# -------------------------------------------------------------------------------------------------------
# Генерация нового взрыва в указанных координатах.
# -------------------------------------------------------------------------------------------------------
def Boom(x, y):
    for i in range(0, numParticle):
        particles[i][_x] = x                # Задаем точку, откуда взорветса салют
        particles[i][_y] = y
                                            # Генерируем случайные скорости разлета частицы в диапазоне от -3.0 до 3.0
        particles[i][_dirx] = random.randint(-30, 30)/10.0
        particles[i][_diry] = random.randint(-30, 30)/10.0
                                            # Генерируем случайное число внутри радиуса от 0 до 5.0, для придания сферической формы взрыву
        dist = random.randint(0, 50)/10.0
                                            # Вычисляем диагональ треугольника верктора скорости до увеличения.
        mlen = math.sqrt(particles[i][_dirx]**2 + particles[i][_diry]**2)
        if mlen != 0:
            mlen = 1.0 / mlen
                                            # Используя теорему подобия вычисляем новые значения скоростей.
        particles[i][_dirx] *= mlen * dist
        particles[i][_diry] *= mlen * dist
                                            # Задаем начальный цвет точки - он самый яркий, т.к. это только начало взрыва
        particles[i][_color] = 254

# -------------------------------------------------------------------------------------------------------
#  Отрисовка закрашенного квадрата в нужных координатах, определенного размера.
# -------------------------------------------------------------------------------------------------------
def drawBox(x, y, size, color):
    pygame.draw.rect(screen, pal[color], (x, y, size, size))

# -------------------------------------------------------------------------------------------------------

Boom(MX/2, MY/2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(0, numParticle):             # Перебираем все частицы
        x = round(particles[i][_x])
        y = round(particles[i][_y])
                                                # Если координаты входят в экран - выводим
        if (x in range(1, MX-1)) and (y in range(1, MY-1)):
            scr[y][x] = particles[i][_color]
                                                # Изменяем координаты частицы в зависимости от скорости
        particles[i][_x] += particles[i][_dirx]
        particles[i][_y] += particles[i][_diry]

                                                # Реализуем отскок от земли
        if particles[i][_y] > MY:
            particles[i][_y] = MY
            particles[i][_diry] = -particles[i][_diry] / 2.0
        else:
            particles[i][_diry] += gravity      # Применяем к скрости частицы - гравитацию

    # Осуществляем размытие экрана по 4 соседним точкам
    for y in range(1, MY-1):
        for x in range(1, MX-1):
            color = round(((scr[y][x+1] + scr[y][x-1] + scr[y+1][x] + scr[y-1][x]) / 4.0) - 2)
            if color < 0:
                color = 0
            scr[y][x] = color
            drawBox(x*scale, y*scale, scale, color)

    # Для генерации нового взрыва используем счетчик, как только он превышен, новый взрыв и
    # перестартуем счетчик
    time += 1
    if time > 70:
        time = 0
        Boom(random.randint(1, MX), random.randint(1, MY))

    pygame.display.flip()

pygame.quit()