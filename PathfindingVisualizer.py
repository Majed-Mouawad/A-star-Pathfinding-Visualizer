from os import path
import pygame
from queue import PriorityQueue

window = pygame.display.set_mode((600,600))
pygame.display.set_caption("Path finding using the A* algorithm")

print("1- Left-click a square to select the start node")
print("2- Left-click another square to select the end node")
print("3- Hold the left-click and drag your mouse while holding to select the barriers")
print("4- Press SPACE to run")
class Node:
    def __init__(self, row, column, width, rows ):
        self.row = row
        self.column = column
        self.color = (255,255,255)
        self.width = width
        self.rows = rows
        self.x = row*width
        self.y = column*width
        self.nodes_around = []

    def get_position(self):
        return (self.row, self.column)

    def is_checked(self):
        return self.color == (255,0,0)

    def is_barrier(self):
        return self.color == (0,0,0)

    def is_start(self):
        return self.color == (255,165,0)

    def is_end(self):
        return self.color == (128,0,128)

    def make_path(self):
        self.color =(64, 224, 208)

    def make_normal(self):
        self.color = (255, 255, 255)

    def make_checked(self):
        self.color = (255,0,0)

    def make_open(self):
        self.color = (0,255,0)

    def make_barrier(self):
        self.color = (0,0,0)

    def make_start(self):
        self.color = (255,165,0)

    def make_end(self):
        self.color = (128,0,128)

    def draw_cube(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        return False

    def check_surroundings(self, grid):
        if self.row >0 and grid[self.row -1][self.column].is_barrier() == False: #Checks row above
            self.nodes_around.append(grid[self.row -1][self.column])

        if self.row < self.rows - 1 and grid[self.row +1][self.column].is_barrier() == False: #Checks row below
            self.nodes_around.append(grid[self.row +1][self.column])

        if self.column < self.rows - 1 and grid[self.row ][self.column + 1].is_barrier() == False: #Checks column to the right
            self.nodes_around.append(grid[self.row ][self.column+1])

        if self.column > 0 and grid[self.row][self.column -1].is_barrier() == False: #Checks column to the left
            self.nodes_around.append(grid[self.row ][self.column-1])

def draw_path(last, current_node, visualize):
    while current_node in last:
        current_node = last[current_node]
        current_node.make_path()
        visualize()


def heuristic_function(start, end):
    x_start = start[0]
    x_end = end[0]
    y_start = start[1]
    y_end = end[1]
    return abs(x_start-y_start) + abs(x_end-y_end)

def algorithm(visualize,grid, start_node, end_node):
    open_set = PriorityQueue()
    count = 0
    open_set.put((0, count, start_node))
    last ={} # Keeps track of last node before current
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start_node] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start_node] = heuristic_function(start_node.get_position(), end_node.get_position())

    open_set_tracker = {start_node}

    while open_set.empty() == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current_node = open_set.get()[2]
        open_set_tracker.remove(current_node)

        if current_node == end_node:
            draw_path(last, end_node, visualize)
            start_node.make_start()
            end_node.make_end()
            return True
        
        for node_arround in current_node.nodes_around:
            tmp_g_score = g_score[current_node] + 1

            if tmp_g_score < g_score[node_arround]:
                last[node_arround ] = current_node
                g_score[node_arround] = tmp_g_score
                f_score[node_arround] = g_score[node_arround] + heuristic_function(node_arround.get_position(), end_node.get_position())
                if node_arround not in open_set_tracker:
                    count+=1
                    open_set.put((f_score[node_arround], count, node_arround))
                    open_set_tracker.add(node_arround)
                    node_arround.make_open()

        visualize()
        if current_node != start_node:
            current_node.make_checked()

    return False



def sketch_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,gap,rows)
            grid[i].append(node)
    return grid

def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, (128,128,128), (0,i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(window, (128,128,128), (j*gap,0), (j*gap, width))

def visualize(window, grid, rows, width):
    window.fill((255,255,255))
    for row in grid:
        for node in row:
            node.draw_cube(window)
    draw_grid(window, rows, width)
    pygame.display.update()


def get_cursor_position(cursor, rows, width):
    gap = width // rows
    (y, x) = cursor
    row = y//gap
    column = x//gap
    return (row, column)

def main(window, width):
    rows = 50
    grid = sketch_grid(rows, width)
    run = True
    running = False
    starting_pos = None
    ending_pos = None
    while run:
        visualize(window, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if running:
                continue
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                (row, column) = get_cursor_position(position, rows, width)
                current_node = grid[row][column]
                if starting_pos ==None and current_node != ending_pos:
                    starting_pos = current_node
                    starting_pos.make_start()
                
                elif ending_pos == None and current_node != starting_pos:
                    ending_pos = current_node
                    ending_pos.make_end()

                elif current_node != starting_pos or current_node != ending_pos:
                    current_node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                (row, column) = get_cursor_position(position, rows, width)
                current_node = grid[row][column]
                current_node.make_normal()
                if current_node == starting_pos :
                    starting_pos = None
                if current_node == ending_pos:
                    ending_pos = None 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and running == False:
                    for row in grid:
                        for node in row:
                            node.check_surroundings(grid)

                    algorithm(lambda: visualize(window, grid, rows, width), grid, starting_pos, ending_pos)
            
                if event.key == pygame.K_DELETE:
                    starting_pos = None
                    ending_pos = None
                    grid = sketch_grid(rows, width)

    pygame.quit()

main(window, 600)