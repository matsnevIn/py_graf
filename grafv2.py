import pygame
import math

SX = 800
SY = 800

pygame.init()
screen = pygame.display.set_mode((SX, SY))
running = True

COUNT_CIRCLE = 100                      # Всего эллипсов.
STEP_RADIUS = 10                        # Шаг увеличения радиуса.
STEP_COLOR = (255-50) / COUNT_CIRCLE    # Шаг увеличения цвета.

Circles = []    # Список содержащий эллипсы, каждый из них
                # является списком с: X, Y, RADIUS, COLOR

X = 0       # Номер координаты X в списке единичного эллипса.
Y = 1       # Номер координаты Y в списке единичного эллипса.
RADIUS = 2  # Номер радиуса в списке единичного эллипса.
COLOR = 3   # Номер цвета в списке единичного эллипса.

rot = 0.05  # Угол смещения центра туннеля.

# ---------------------------------------------------------------------------------------------
# Отрисовка одного эллипса на экране.
# На вход поступает эллипс circle из списка Circles.
# ---------------------------------------------------------------------------------------------
def draw_circle(circle):
    alpha = 0                   # Угол перемещения по эллипсу, для отрисовки точки.
    step = math.pi * 2 / 100    # Шаг, с которым рисуются точки эллипса.
    while alpha < math.pi * 2:
        s_x = round(circle[X] + math.sin(alpha) * circle[RADIUS])
        s_y = round(circle[Y] + math.cos(alpha) * circle[RADIUS] / 1.5)
        color = round(circle[COLOR])
        if 0 < s_x < SX and 0 < s_y < SY:
            pygame.draw.circle(screen, (color, color, color), (s_x, s_y), 2)
        alpha += step

# ---------------------------------------------------------------------------------------------
for i in range(0, COUNT_CIRCLE):
    Circles.append([SX // 2, SY // 2, 100, 50])       # Заполняем список с эллипсами, инициализируя их

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for i in range(len(Circles) - 2, -1, -1):
        c = Circles[i]
        c[RADIUS] += STEP_RADIUS
        c[COLOR] += STEP_COLOR
        Circles[i + 1] = c

        draw_circle(c)

    sx = SX // 2 + math.sin(rot) * 50.0        # Вычисление координаты X,Y для нового эллипса
    sy = SY // 2 + math.sin(rot) * 50.0

    Circles[0] = [sx, sy, 100, 50]
    rot += 0.05

    pygame.display.flip()

pygame.quit()