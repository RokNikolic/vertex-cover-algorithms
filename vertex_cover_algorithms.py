# Vertex cover problem algorithms

import time


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
    cover_vertices = set()


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


if __name__ == "__main__":
    graph_read = read_file('g01.graph')

    start = time.perf_counter()
    result = naive_algorithm(graph_read)
    end = time.perf_counter()
    print(f"Naive algorithm result of length: {len(result)} computed in: {end - start :.3} seconds.")

    start = time.perf_counter()
    result = greedy_apx2_algorithm(graph_read)
    end = time.perf_counter()
    print(f"Greedy apx2 algorithm result of length: {len(result)} computed in: {end - start :.3} seconds.")
