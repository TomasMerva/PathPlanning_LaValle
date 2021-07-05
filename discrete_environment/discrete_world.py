#!/usr/bin/python3
import math
import pygame


class Colors:
    def __init__(self):
        self.RED = (255, 0, 0)
        self.GREEN = (0,128,0)          # alive node
        self.BLUE = (0, 0, 255)
        self.WHITE = (255, 255, 255)    # default
        self.BLACK = (0, 0, 0)          # obstacle and grid
        self.GREY = (128, 128, 128)
        self.SLATEGREY = (47, 79, 79)   # dead
        self.PURPLE = (128, 0, 128)     # path
        self.YELLOW = (255, 255, 0)     # start
        self.ORANGE = (255, 102, 0)     # goal


class Node:
    def __init__(self, index_row, index_col, grid_size, total_rows):
        # Discrete position
        self.index_row = index_row
        self.index_col = index_col
        # Continous position that is required for pygame
        self.position_x = index_col * grid_size
        self.position_y = index_row * grid_size
        self.grid_size = grid_size
        self.neighbors = []
        self.total_rows = total_rows

        # Graphics properties
        self.colors_list = Colors()
        self.color = self.colors_list.WHITE


    def get_index_pos(self):
        return self.index_row, self.index_col

    def reset(self):
        self.color = self.colors_list.WHITE

    def is_dead(self):
        return self.color == self.colors_list.SLATEGREY

    def is_alive(self):
        return self.color == self.colors_list.GREEN

    def is_obstacle(self):
        return self.color == self.colors_list.BLACK

    def make_dead(self):
        self.color = self.colors_list.SLATEGREY

    def make_alive(self):
        self.color = self.colors_list.GREEN

    def make_obstacle(self):
        self.color = self.colors_list.BLACK

    def make_path(self):
        self.color = self.colors_list.PURPLE

    def make_start(self):
        self.color = self.colors_list.YELLOW

    def make_goal(self):
        self.color = self.colors_list.ORANGE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.position_x, self.position_y, self.grid_size, self.grid_size))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Neighbor on right
        if self.index_col < self.total_rows-1 and not grid[self.index_row][self.index_col + 1].is_obstacle():
            self.neighbors.append(grid[self.index_row][self.index_col + 1])
        # Neighbor on left
        if self.index_col > 0 and not grid[self.index_row][self.index_col - 1].is_obstacle():
            self.neighbors.append(grid[self.index_row][self.index_col - 1])
        # Neighbor up
        if self.index_row > 0 and not grid[self.index_row-1][self.index_col].is_obstacle():
            self.neighbors.append(grid[self.index_row-1][self.index_col])
        # Neighbor down
        if self.index_row < self.total_rows-1 and not grid[self.index_row + 1][self.index_col].is_obstacle():
            self.neighbors.append(grid[self.index_row+1][self.index_col])

    def __lt__(self, other):
        return False


class DiscreteWorld:
    def __init__(self, width, rows):
        # Physical properties
        self.WIDTH = width
        self.ROWS = rows
        self.GRID_SIZE = self.WIDTH // self.ROWS # integer grid size
        self.grid = []
        # Graphics properties
        self.window = pygame.display.set_mode((self.WIDTH, self.WIDTH))
        self.colors_list = Colors()

    # Function for generating the grid containing nodes
    def make_grid(self):
        self.grid = []
        # 2D list representing grid with dimension ROWS * ROWS
        for row in range(self.ROWS):
            self.grid.append([])     # append a new row
            for col in range(self.ROWS):
                # Create new node at grid[row][col]
                node = Node(index_row=row,
                            index_col=col,
                            grid_size=self.GRID_SIZE,
                            total_rows=self.ROWS)
                self.grid[row].append(node)

    # Function for drawing lines to represent grid
    def draw_grid_lines(self):
        for row in range(self.ROWS):
            pygame.draw.line(self.window, self.colors_list.GREY, (0, row * self.GRID_SIZE), (self.WIDTH, row * self.GRID_SIZE))
            for col in range(self.ROWS):
                pygame.draw.line(self.window, self.colors_list.GREY, (col * self.GRID_SIZE, 0), (col * self.GRID_SIZE, self.WIDTH))

    # Function for drawing whole grid
    def draw(self):
        self.window.fill(self.colors_list.WHITE)    # Reset pygame window
        # Draw nodes and grid_lines
        for row in self.grid:
            for node in row:
                node.draw(self.window)
        self.draw_grid_lines()
        pygame.display.update()

    def get_mouse_clicked_node(self):
        x, y = pygame.mouse.get_pos()
        row = y // self.GRID_SIZE
        col = x // self.GRID_SIZE
        node = self.grid[row][col]
        return node

    def create_obstacle_map(self, grid, obstacles_list):
        pass

    def update_neighbors(self):
        for row in self.grid:
            for node in row:
                node.update_neighbors(self.grid)


