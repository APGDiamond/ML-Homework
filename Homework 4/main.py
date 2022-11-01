import math
import random
import networkx as nx
import matplotlib.pyplot as plt


def init_weight(count_of_nodes):
    matrix = [[0 for x in range(count_of_nodes)] for x in range(count_of_nodes)]
    for i in range(count_of_nodes):
        for j in range(i, count_of_nodes):
            if j != i:
                radom_weight = random.randint(0, 50)
                matrix[i][j] = radom_weight
                matrix[j][i] = radom_weight

    return matrix


def build_graph(matrix):
    graph = nx.Graph()
    for i in range(len(matrix)):
        graph.add_node(i)

    for i in range(len(matrix)):
        for j in range(i, len(matrix[i])):
            if matrix[i][j] != 0:
                graph.add_edge(i, j, weight=matrix[i][j])

    return graph


def draw_graph(graph):
    pos = nx.spring_layout(graph, k=10)
    nx.draw(graph, with_labels=True, pos=pos, font_weight='bold')
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()

def get_min_tree(matrix):
    isolated_nodes = [node for node in range(len(matrix))]

    min_distance = math.inf
    new_edges = []
    new_edge = (0, 0, 0)
    for i in range(len(matrix)):
        for j in range(i, len(matrix[i])):
            if matrix[i][j] != 0 and matrix[i][j] < min_distance:
                min_distance = matrix[i][j]
                new_edge = (i, j, matrix[i][j])

    new_edges.append(new_edge)
    isolated_nodes.remove(new_edge[0])
    isolated_nodes.remove(new_edge[1])

    while len(isolated_nodes) > 0:
        min_distance = math.inf

        for i in range(len(matrix)):
            if i in isolated_nodes:
                continue
            for j in range(len(matrix[i])):
                if matrix[i][j] != 0 and matrix[i][j] < min_distance and j in isolated_nodes:
                    min_distance = matrix[i][j]
                    new_edge = (i, j, matrix[i][j])

        new_edges.append(new_edge)
        isolated_nodes.remove(new_edge[1])

    new_matrix = [[0 for x in range(len(matrix))] for x in range(len(matrix))]

    for edge in new_edges:
        new_matrix[edge[0]][edge[1]] = edge[2]
        new_matrix[edge[1]][edge[0]] = edge[2]

    return new_matrix


def get_clusterized_matrix(matrix, number_of_clusters):
    matrix_copy = []

    for line in matrix:
        matrix_copy.append(line.copy())

    for k in range(number_of_clusters-1):
        max_edge = (0, 0, 0)
        for i in range(len(matrix_copy)):
            for j in range(i, len(matrix_copy)):
                if matrix_copy[i][j] > max_edge[2]:
                    max_edge = (i, j, matrix_copy[i][j])

        matrix_copy[max_edge[0]][max_edge[1]] = 0
        matrix_copy[max_edge[1]][max_edge[0]] = 0

    return matrix_copy


matrix = init_weight(5)
graph = build_graph(matrix)
draw_graph(graph)
min_tree_matrix = get_min_tree(matrix)
min_graph = build_graph(min_tree_matrix)
draw_graph(min_graph)
clusterized_matrix = get_clusterized_matrix(min_tree_matrix, 3)
clusterized_graph = build_graph(clusterized_matrix)
draw_graph(clusterized_graph)