import pygame
import pygame as pg
import sys
import sklearn.svm
import math

sc = pg.display.set_mode((600, 600))
sc.fill('white')
pg.display.update()

class Point:
    def __init__(self, x, y, point_class, color='black'):
        self.x = x
        self.y = y
        self.point_class = point_class
        self.color = color


def display_point(point):
    pg.draw.circle(sc, point.color, (math.fabs(point.x), math.fabs(point.y)), 5)
    pg.display.update()


def fit_svm(points):
    X = [(point.x, point.y) for point in points]
    y = [point.point_class for point in points]
    svc = sklearn.svm.LinearSVC(random_state=42, tol=1e-5, max_iter=100000000)
    svc.fit(X, y)
    return svc.coef_[0][0], svc.coef_[0][1], svc.intercept_[0], svc


points = []
line_data = (0, 0, 0)


def count_x_for_line(line_data, y):
    return (-line_data[2] - line_data[1] * y) / line_data[0]


while True:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()

        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                point = Point(i.pos[0], -i.pos[1], 0, 'red')
                points.append(point)
                display_point(point)
            elif i.button == 3:
                point = Point(i.pos[0], -i.pos[1], 1, 'blue')
                points.append(point)
                display_point(point)
            elif i.button == 2:
                color = 'black'
                if line_data[1]*-i.pos[1] + line_data[0]*i.pos[0] + line_data[2] > 0:
                    point = Point(i.pos[0], -i.pos[1], 1, 'blue')
                    points.append(point)
                    display_point(point)
                else:
                    point = Point(i.pos[0], -i.pos[1], 0, 'red')
                    points.append(point)
                    display_point(point)

        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_RETURN:
                line_data = fit_svm(points)
                x1 = count_x_for_line(line_data, -599)
                x2 = count_x_for_line(line_data, 0)
                pg.draw.line(sc, 'black', (x1, 599), (x2, 0))
                pg.display.update()
    pg.time.delay(100)