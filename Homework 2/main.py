import random
import matplotlib.pyplot as plt
import math


class Point:
    def __init__(self, x, y, color='b', centroid=None):
        self.x = x
        self.y = y
        self.color = color
        self.centroid = centroid


def init_points(n):
    points = []
    for i in range(n):
        points.append(Point(random.randint(-50, 50), random.randint(-50, 50)))
    return points


def get_mass_center(points):
    return Point(sum([p.x for p in points]) / len(points), sum([p.y for p in points]) / len(points))


def get_centroids(points, centroids_count):
    mass_center = get_mass_center(points)
    if centroids_count == 1:
        return [mass_center]
    else:
        radius = max(count_euclidean_dist(point, mass_center) for point in points)
        return [Point(radius * math.cos(2 * math.pi * k / centroids_count) + mass_center.x,
                      radius * math.sin(2 * math.pi * k / centroids_count) + mass_center.y,
                      color="#%06x" % random.randint(0, 0xFFFFFF)) for k
                in range(1, centroids_count + 1)]


def count_euclidean_dist(point1, point2):
    return math.sqrt(math.pow(point1.x - point2.x, 2) + math.pow(point1.y - point2.y, 2))


def show_generated_points(points):
    plt.scatter([p.x for p in points], [p.y for p in points])
    plt.title('Generated points')
    plt.show()


def show_clustered_points(points, centroids, iteration_number):
    plt.scatter([p.x for p in points], [p.y for p in points], c = [p.color for p in points])
    plt.title('Clusterization. Step: ' + str(iteration_number) + ' Cluster count: ' + str(len(centroids)))
    plt.scatter([c.x for c in centroids], [c.y for c in centroids], c=[centroid.color for centroid in centroids],
                marker='x')
    plt.show()


def clust_points(points, centroids_count, show):
    centroids = get_centroids(points, centroids_count)
    iteration = 1
    while True:
        for point in points:
            minimal_distance = count_euclidean_dist(point, centroids[0])
            point.centroid = centroids[0]
            point.color = centroids[0].color
            for centroid in centroids:
                current_distance = count_euclidean_dist(centroid, point)
                if current_distance <= minimal_distance:
                    minimal_distance = current_distance
                    point.centroid = centroid
                    point.color = centroid.color
        if show:
            show_clustered_points(points, centroids, iteration)
        new_centroids = []
        for centroid in centroids:
            x_sum = 0
            y_sum = 0
            count_points_in_cluster = 0
            for point in points:
                if point.centroid == centroid:
                    x_sum += point.x
                    y_sum += point.y
                    count_points_in_cluster += 1

            if count_points_in_cluster == 0:
                new_centroids.append(centroid)
            else:
                new_centroids.append(
                Point(x_sum / count_points_in_cluster, y_sum / count_points_in_cluster, color=centroid.color))
        distance_between_centroids = 0
        for centroid_index in range(len(centroids)):
            distance_between_centroids += count_euclidean_dist(new_centroids[centroid_index],
                                                                   centroids[centroid_index])
        if distance_between_centroids == 0:
            return centroids, points
        else:
            centroids = new_centroids
            iteration += 1


def count_clusters(points):
    clusters_max = int(math.sqrt(len(points)))
    clusters_count = 1
    min_difference = math.inf
    differences_by_clusters_count = []
    for k in range(1, 2*clusters_max):
        difference = 0
        centroids, points = clust_points(points, k, False)
        for point in points:
            for centroid in centroids:
                if point.centroid == centroid:
                    difference += count_euclidean_dist(point, centroid)
                    break
        differences_by_clusters_count.append(difference)
    for k in range(1, len(differences_by_clusters_count)-1):
        current_difference = math.fabs(differences_by_clusters_count[k] - differences_by_clusters_count[k+1])\
                             / (math.fabs(differences_by_clusters_count[k-1] - differences_by_clusters_count[k]))
        if current_difference < min_difference:
            min_difference = current_difference
            clusters_count = k+1
    return clusters_count


inited_points = init_points(100)
show_generated_points(inited_points)
clusters_count = count_clusters(inited_points)
clust_points(inited_points, clusters_count, True)