# Vertex cover problem algorithms
import time
import numpy as np
import os
from scipy.optimize import linprog


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

    num_of_vertices = len(vertex_set)
    num_of_edges = len([edge for edge in lines if edge])

    objective = np.ones(num_of_vertices)
    ineq_left = np.zeros((num_of_edges, num_of_vertices))
    ineq_right = np.ones(num_of_edges)

    for i, edge in enumerate(lines):
        if not edge:
            continue
        edge_vertex1, edge_vertex2 = map(int, edge.split(" "))
        ineq_left[i, edge_vertex1 - 1] = 1
        ineq_left[i, edge_vertex2 - 1] = 1

    bounds = [(0, 1) for _ in range(num_of_vertices)]

    result = linprog(c=objective, A_ub=ineq_left, b_ub=ineq_right, bounds=bounds, method='highs')
    print(result)


def run_all_algorithms(graph_path):
    graph_read = read_file(graph_path)

    start = time.perf_counter()
    result = naive_algorithm(graph_read)
    end = time.perf_counter()
    print(f"Naive algorithm result length: {len(result)} computed in: {end - start :.3} seconds.")

    start = time.perf_counter()
    result = natural_greedy_algorithm(graph_read)
    end = time.perf_counter()
    print(f"Natural greedy algorithm result length: {len(result)} computed in: {end - start :.3} seconds.")

    start = time.perf_counter()
    result = greedy_apx2_algorithm(graph_read)
    end = time.perf_counter()
    print(f"Greedy apx2 algorithm result length: {len(result)} computed in: {end - start :.3} seconds.")

    start = time.perf_counter()
    result = linear_programing_algorithm(graph_read)
    end = time.perf_counter()
    print(f"Linear programming algorithm result length: {result} computed in: {end - start :.3} seconds.")


if __name__ == "__main__":
    graph_list = os.listdir(r'./graphs')
    graph_list.sort()
    print(linear_programing_algorithm(read_file(f'./graphs/small_graph.graph')))
    #for graph in graph_list:
    #    print(f"Running algorithms on graph {graph}.")
    #    run_all_algorithms(f'./graphs/{graph}')
    