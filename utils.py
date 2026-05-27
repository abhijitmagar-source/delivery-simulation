from math import sqrt


def calculate_distance(point1, point2):

    return sqrt(
        (point2[0] - point1[0]) ** 2 +
        (point2[1] - point1[1]) ** 2
    )