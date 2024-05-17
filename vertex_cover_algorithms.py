# Vertex cover problem algorithms 2024, github.com/RokNikolic

import time
import os
import numpy as np
from scipy.optimize import linprog
from scipy import sparse
from tabulate import tabulate


def read_file(name):
    with open(rf'{name}', 'r') as f:
        return f.read()


def naive_algorithm(puzzle_input):
    lines = puzzle_input.split("\n")
    cover_vertices = set()
    for edge in lines:
        if not edge:
            continue
        vertices = edge.split(" ")
        if vertices[0] not in cover_vertices and vertices[1] not in cover_vertices:
            cover_vertices.add(vertices[0])

    return cover_vertices


def natural_greedy_algorithm(puzzle_input):
    lines = puzzle_input.split("\n")
    vertex_dict = {}
    for edge in lines:
        if not edge:
            continue
        vertices = edge.split(" ")
        if vertices[0] not in vertex_dict:
            vertex_dict[vertices[0]] = []
        if vertices[1] not in vertex_dict:
            vertex_dict[vertices[1]] = []
        vertex_dict[vertices[0]].append(vertices[1])
        vertex_dict[vertices[1]].append(vertices[0])

    sorted_dict = sorted(vertex_dict.items(), key=lambda item: len(item[1]), reverse=True)

    cover_vertices = set()
    for vertex, edges in sorted_dict:
        if vertex not in cover_vertices and not all(ver in cover_vertices for ver in edges):
            cover_vertices.add(vertex)

    return cover_vertices


def greedy_apx2_algorithm(puzzle_input):
    lines = puzzle_input.split("\n")
    cover_vertices = set()
    for edge in lines:
        if not edge:
            continue
        vertices = edge.split(" ")
        if vertices[0] not in cover_vertices and vertices[1] not in cover_vertices:
            cover_vertices.add(vertices[0])
            cover_vertices.add(vertices[1])

    return cover_vertices


def linear_programing_algorithm(puzzle_input):
    lines = puzzle_input.split("\n")

    vertex_set = set()
    for edge in lines:
        if not edge:
            continue
        edge_vertex1, edge_vertex2 = map(int, edge.split(" "))
        vertex_set.add(edge_vertex1)
        vertex_set.add(edge_vertex2)

    num_of_vertices = max(vertex_set)
    num_of_edges = len([edge for edge in lines if edge])

    objective = np.ones(num_of_vertices)
    ineq_right = -np.ones(num_of_edges)

    row_indices = []
    col_indices = []
    data = []
    for i, edge in enumerate(lines):
        if not edge:
            continue
        edge_vertex1, edge_vertex2 = map(int, edge.split(" "))
        row_indices.extend([i, i])
        col_indices.extend([edge_vertex1-1, edge_vertex2-1])
        data.extend([-1, -1])

    sparce_ineq_left = sparse.csr_matrix((data, (row_indices, col_indices)), shape=(num_of_edges, num_of_vertices))
    bounds = [(0, 1) for _ in range(num_of_vertices)]

    result = linprog(c=objective, A_ub=sparce_ineq_left, b_ub=ineq_right, bounds=bounds, method='highs')
    vertex_cover = [1 if xi >= 0.5 else 0 for xi in result.x]

    return [vertex for vertex in vertex_cover if vertex != 0], result.fun


def run_all_algorithms(graph_path):
    graph_read = read_file(f'./graphs/{graph_path}')

    result1 = naive_algorithm(graph_read)
    result2 = natural_greedy_algorithm(graph_read)
    result3 = greedy_apx2_algorithm(graph_read)
    result4, low_bound = linear_programing_algorithm(graph_read)
    return [graph_path, len(result1), len(result2), len(result3), len(result4), int(low_bound)]


if __name__ == "__main__":
    graph_list = os.listdir(r'./graphs')
    graph_list.sort()

    start = time.perf_counter()
    result_data = []
    for graph in graph_list:
        print(f"Running algorithms on graph {graph}")
        result_data.append(run_all_algorithms(graph))
    end = time.perf_counter()

    col_names = ["Graph name", "Naive", "Greedy natural", "2APX Greedy", "2APX Linear prog", "Lower bound"]
    print(tabulate(result_data, headers=col_names))
    print(f"All algorithms on all graphs computed in: {end - start :.3} seconds")
