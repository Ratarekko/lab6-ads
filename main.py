import random
import turtle
import keyboard
import math

SEED = 3223
NUM_VERTICES = 12
K = 0.915
drawn_edges = set()
def generate_matrix():
    random.seed(SEED)
    matrix = [[random.random() * 2 for _ in range(NUM_VERTICES)] for _ in range(NUM_VERTICES)]
    return matrix

def apply_threshold(matrix):
    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            matrix[i][j] = 1 if matrix[i][j] * K >= 1 else 0
    return matrix

def make_directed_matrix():
    matrix = generate_matrix()
    directed_matrix = apply_threshold(matrix)
    return directed_matrix

def make_undirected_matrix():
    directed_matrix = make_directed_matrix()
    undirected_matrix = [[0] * NUM_VERTICES for _ in range(NUM_VERTICES)]
    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            if directed_matrix[i][j] == 1:
                undirected_matrix[i][j] = 1
                undirected_matrix[j][i] = 1
    return undirected_matrix

def print_matrix():
    undirected = make_undirected_matrix()
    print("\nUndirected Matrix:")
    for row in undirected:
        print(row)


print_matrix()

def draw_vertex(x, y, number):
    turtle.penup()
    turtle.goto(x, y - 20)
    turtle.pendown()
    turtle.begin_fill()
    turtle.color("orange")
    turtle.circle(20)
    turtle.end_fill()
    turtle.penup()
    turtle.goto(x, y - 15)
    turtle.color("black")
    turtle.write(number, align="center", font=("Arial", 18, "bold"))

def loop(x1, y1):
    if x1 == 225:
        turtle.goto(x1 + 35, y1 + 15)
    if x1 == -225:
        turtle.goto(x1 - 35, y1 + 15)
    if y1 == -225:
        turtle.goto(x1, y1 - 20)
    if y1 == 225:
        turtle.goto(x1, y1 + 20)
    turtle.setheading(180)
    turtle.pendown()
    turtle.circle(15)
    turtle.penup()

def draw_bent_edge(x1, y1, x2, y2):
    turtle.goto(x1, y1)
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    angle = math.atan2(y2 - y1, x2 - x1)
    turtle.setheading(math.degrees(angle))
    turtle.forward(20)
    turtle.pendown()
    bent_x = mid_x * random.uniform(1.15, 1.35)
    bent_y = mid_y * random.uniform(1.15, 1.35)
    turtle.goto(bent_x, bent_y)
    distance = math.sqrt((x2 - bent_x) ** 2 + (y2 - bent_y) ** 2)
    angle = math.atan2(y2 - bent_y, x2 - bent_x)
    turtle.setheading(math.degrees(angle))
    turtle.forward(distance - 20)
    turtle.penup()

def diff_edge(x1, y1, x2, y2, i, j):
    if i - j == 1 or j - i == 1:
        draw_normal_edge(x1, y1, x2, y2)
    else:
        draw_bent_edge(x1, y1, x2, y2)

def draw_normal_edge(x1, y1, x2, y2):
    angle = math.atan2(y2 - y1, x2 - x1)
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    turtle.setheading(math.degrees(angle))
    turtle.forward(20)
    turtle.pendown()
    turtle.forward(distance - 40)
    turtle.penup()

def draw_edge(x1, y1, x2, y2, i, j, weight):
    if weight:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        turtle.penup()
        turtle.goto(mid_x+10, mid_y+10)
        turtle.color('Dark blue')
        turtle.write(weight, align="center", font=("Arial", 15, "normal"))
        turtle.penup()
        turtle.color('Magenta')

    if (i, j) in drawn_edges or (j, i) in drawn_edges:
        return

    drawn_edges.add((i, j))

    turtle.goto(x1, y1)

    if x1 == x2 == -225 or x1 == x2 == 225 or y1 == y2 == 225 or y1 == y2 == -225:
        if i == j:
            loop(x1, y1)
        else:
            diff_edge(x1, y1, x2, y2, i, j)
    else:
        draw_normal_edge(x1, y1, x2, y2)

def calculate_positions(num_vertices, distance):
    positions = []
    x, y = -225, 225
    for i in range(4):
        for _ in range(num_vertices // 4):
            positions.append((x, y))
            if i % 2 == 0:
                x += distance if i == 0 else -distance
            else:
                y += -distance if i == 1 else distance
    return positions

def draw_graph(matrix):
    positions = calculate_positions(NUM_VERTICES, 150)

    for i, (x, y) in enumerate(positions):
        draw_vertex(x, y, i + 1)

    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            if matrix[i][j] == 1:
                draw_edge(positions[i][0], positions[i][1], positions[j][0], positions[j][1], i, j, False)

def make_weight_matrix():
    undirected_matrix = make_undirected_matrix()
    b = [[random.random() * 2 for _ in range(NUM_VERTICES)] for _ in range(NUM_VERTICES)]
    c = [[math.ceil(b[i][j] * 100 * undirected_matrix[i][j]) for j in range(NUM_VERTICES)] for i in range(NUM_VERTICES)]
    d = [[1 if c[i][j] > 0 else 0 for j in range(NUM_VERTICES)] for i in range(NUM_VERTICES)]
    h = [[1 if d[i][j] != d[j][i] else 0 for j in range(NUM_VERTICES)] for i in range(NUM_VERTICES)]
    tr = [[1 if i < j else 0 for j in range(NUM_VERTICES)] for i in range(NUM_VERTICES)]

    w_matrix = [[0] * NUM_VERTICES for _ in range(NUM_VERTICES)]
    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            w_matrix[i][j] = (d[i][j] + (h[i][j] * tr[i][j])) * c[i][j]
            w_matrix[j][i] = w_matrix[i][j]

    print("\nMatrix W:")
    for row in w_matrix:
        print(row)
    return w_matrix

def calculate_min_spanning_tree_weight(min_spanning_tree, weight_matrix):
    total_weight = 0
    for edge in min_spanning_tree:
        i, j = edge
        total_weight += weight_matrix[i][j]
    return total_weight

def prim_algorithm(weight_matrix):
    num_vertices = len(weight_matrix)
    visited = [False] * num_vertices
    min_spanning_tree = []

    start_vertex = 0
    visited[start_vertex] = True

    while len(min_spanning_tree) < num_vertices - 1:
        min_weight = float('inf')
        min_edge = None
        positions = calculate_positions(NUM_VERTICES, 150)

        for i in range(num_vertices):
            if visited[i]:
                for j in range(num_vertices):
                    if not visited[j] and 0 < weight_matrix[i][j] < min_weight:
                        min_weight = weight_matrix[i][j]
                        min_edge = (i, j)

        if min_edge:
            min_spanning_tree.append(min_edge)
            visited[min_edge[1]] = True
            turtle.width(5)
            drawn_edges.clear()
            keyboard.wait('space')
            draw_edge(positions[min_edge[0]][0], positions[min_edge[0]][1], positions[min_edge[1]][0], positions[min_edge[1]][1], min_edge[0], min_edge[1], weight_matrix[min_edge[0]][min_edge[1]])

    return min_spanning_tree

def main():
    wn = turtle.Screen()
    wn.title("Graphs")
    wn.bgcolor("white")
    wn.setup(width=800, height=600)
    turtle.speed("fastest")

    undirected_matrix = make_undirected_matrix()

    weight_matrix = make_weight_matrix()

    draw_graph(undirected_matrix)

    min_spanning_tree = prim_algorithm(weight_matrix)
    min_spanning_tree_weight = calculate_min_spanning_tree_weight(min_spanning_tree, weight_matrix)

    print("Minimum Spanning Tree:")
    print(min_spanning_tree)
    print("Total weight of the minimum spanning tree:", min_spanning_tree_weight)
    turtle.hideturtle()
    turtle.done()


main()
