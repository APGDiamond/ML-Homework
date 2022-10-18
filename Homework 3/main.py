import math
import random
import pygame
import sys


class Point:
    def __init__(self, x ,y, point_type=0, color='black', is_visited = False):
        self.x = x
        self.y = y
        self.point_type = point_type
        self.color = color
        self.is_visited = is_visited


sc = pygame.display.set_mode((800, 600))
sc.fill('white')
pygame.display.update()

list_of_points = []


def is_point_exist(points, new_point):
    for point in points:
        if point.x == new_point.x and point.y == new_point.y:
            return True
    return False


def get_points_neighbours(point, points, max_distance):
    neighbours = []
    for current_point in points:
        if point == current_point:
            continue
        else:
            distance = get_distance(current_point, point)
            if distance <= max_distance:
                neighbours.append(current_point)

    return neighbours


def get_groups(points, max_distance, min_neighbours):
    groups = []

    for point in points:
        if point.is_visited:
            continue
        else:
            neighbours = get_points_neighbours(point, points, max_distance)
            if len(neighbours) >= min_neighbours:
                point.is_visited = True
                point.point_type = 1
                groups.append([point])
                while len(neighbours) > 0:
                    current_neighbour = neighbours.pop(0)
                    if current_neighbour.is_visited:
                        continue
                    sub_neighbours = get_points_neighbours(current_neighbour, points, max_distance)
                    if len(sub_neighbours) < min_neighbours or current_neighbour.point_type == 3:
                        current_neighbour.is_visited = True
                        current_neighbour.point_type = 2
                        groups[len(groups)-1].append(current_neighbour)
                    else:
                        current_neighbour.is_visited = True
                        current_neighbour.point_type = 1
                        groups[len(groups) - 1].append(current_neighbour)
                        neighbours.extend(sub_neighbours)
            else:
                point.point_type = 3

    return groups


def get_distance(first_point, second_point):
    return math.sqrt(math.pow(first_point.x - second_point.x, 2) + math.pow(first_point.y - second_point.y, 2))


def refresh_points(points):
    for point in points:
        point.is_visited = False
        point.point_type = 0


def flag_colorize_points(points):
    sc.fill('white')
    pygame.display.update()

    for point in points:
        color = 'black'
        if point.point_type == 3:
            color = 'red'
        elif point.point_type == 2:
            color = 'yellow'
        elif point.point_type == 1:
            color = 'green'
        else:
            color = 'black'
        pygame.draw.circle(sc, color, (point.x, point.y), 5)
        pygame.display.update()


def group_colorize_points(groups, points):
    sc.fill('white')
    pygame.display.update()
    for list in groups:
        random_color = "#%06x" % random.randint(0, 0xFFFFFF)
        for item in list:
            pygame.draw.circle(sc, random_color, (item.x, item.y), 5)
            pygame.display.update()

    for point in points:
        if point.point_type == 3:
            pygame.draw.circle(sc, 'red', (point.x, point.y), 5)
            pygame.display.update()


while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_RETURN:
                refresh_points(list_of_points)
                groups = get_groups(list_of_points, 20, 3)
                flag_colorize_points(list_of_points)
            if i.key == pygame.K_ESCAPE:
                refresh_points(list_of_points)
                groups = get_groups(list_of_points, 20, 3)
                group_colorize_points(groups, list_of_points)

    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if pressed[0]:
        point = Point(pos[0], pos[1])
        if not is_point_exist(list_of_points, point):
            list_of_points.append(point)
            pygame.draw.circle(sc, point.color, pos, 5)
            pygame.display.update()

    pygame.time.delay(50)
