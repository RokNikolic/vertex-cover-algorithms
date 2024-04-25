# Vertex cover problem algorithms

import time
import os


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


def run_all_algorithms(graph_path):
    graph_read = read_file(graph_path)

    start = time.perf_counter()
    result = naive_algorithm(graph_read)
    end = time.perf_counter()
    print(f"Naive algorithm result of length: {len(result)} computed in: {end - start :.3} seconds.")

    start = time.perf_counter()
    result = natural_greedy_algorithm(graph_read)
    end = time.perf_counter()
    print(f"Natural greedy algorithm result of length: {len(result)} computed in: {end - start :.3} seconds.")

    start = time.perf_counter()
    result = greedy_apx2_algorithm(graph_read)
    end = time.perf_counter()
    print(f"Greedy apx2 algorithm result of length: {len(result)} computed in: {end - start :.3} seconds.")


if __name__ == "__main__":
    graph_list = os.listdir(r'./graphs')
    graph_list.sort()
    for graph in graph_list:
        print(f"Running algorihtms on graph {graph}!")
        run_all_algorithms(f'./graphs/{graph}')
    