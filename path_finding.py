"""
This is a PATH FINDING ALGORITHMS visualiser, I decided to create this project
because I wanted to learn more about Algorithms and Data Structures. In this file 
you will find the code that display the grid and handle the special nodes (start, end, walls).

At the moment, the grid is based on a YouTube video of TechWithTim. However, I decided to develop 
all the algorithm by myself as it will help allow me to learn more about those algos.
"""
############################
########## IMPORT ##########
############################
import pygame
import math
from queue import PriorityQueue

###############################
########## CONSTANTS ##########
###############################

WIDTH = 800  # in pixels, in our case width will equal height
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))  # Create the window
# Set the title of the window
pygame.display.set_caption("Path Finding Algorithms")

# A bunch of colors' RGA code
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

##########################
########## NODE ##########
##########################


class Node:
    """
    This class will allow us to create all the nodes of our Grid, a node is a square 
    i.e. a path we can take or not take. 
    The main part of this class is composed of two types of functions:
    - is_XXX(): will return if True if the node is in the XXX state
    - make_XXX(): will change the color of the node to change the state of it to XXX
    """

    def __init__(self, row, col, width, total_row):
        self.row = row
        self.col = col
        self.x = row * width    # x position in pixels
        self.y = col * width    # y position in pixels
        self.color = WHITE      # default color
        self.neighbors = []     # neighbors, useful for the algorithm
        self.width = width      # node width, not the window width
        self.total_row = total_row

    def get_pos(self):
        return self.row, self.col   # return (Y, X) format!!

    def is_closed(self):
        """
        Verification function: will return True or False based on the state
        of the node. True if the node is in the closed set.
        """
        return self.color == RED

    def is_open(self):
        """
        Verification function: will return True if the node is in the open set.
        """
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        """
        This is note a verification function. This one will actually change the color 
        of the node, and set it to white (i.e. reset the state of the node to a neutral one)
        """
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(
            window,
            self.color,
            # The pygame draw rectange function take 3 arguments: the windows it is drawned on, the color and a set with the (x,y) coordinate and the rectangle side size
            (self.x, self.y, self.width, self.width)
        )

    def update_neighbors(self, grid):
        """
        This method will keep track of the neighbors of the node, but in order to do that
        we will first have to check if the neighbor is valid.
        """
        self.neighbors = []
        if self.row < self.total_row - 1 and not grid[self.row + 1][self.col].is_barrier():
            # Check if I am not on the bottom edge and append neighbor BELOW
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            # Check if I am not on the upper edge and append neighbor ABOVE
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_row - 1 and not grid[self.row][self.col + 1].is_barrier():
            # Check if I am not on the right edge and append neighbor on the RIGH
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            # Check if I am not on the left edge and append neighbor on the LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        def __lt__(self, other):
            """
            Dunder method that allow us to use < (less than).
            """
            return False


##########################
########## GRID ##########
##########################

def make_grid(nbr_rows, win_width):
    """
    This function will create (populate) a 2D list that will represent our grid. It takes two
    arguments: the number of rows and the width of the pygame window that we want to 
    display.
    """
    grid = []
    # Compute the nodes' width based on the size of the window and the number of row that we want to have
    node_width = win_width // rows
    for row in range(rows):
        grid.append([])
        # Remember that we have a square here so #rows = #columns
        for column in range(rows):
            node = Node(row, column, node_width, rows)
            grid[row].append(node)

    return grid


def draw_grid(window, rows, win_width):
    node_width = win_width // rows
    for row in range(rows):
        # Draw an horizontal line for every row and space them every node_width = node_height
        pygame.draw.line(window, GREY, (0, row * node_width),
                         (win_width, row * node_width))
        for column in range(rows):
            # Draw vertical line for every column and space them every node_width
            pygame.draw.line(window, GREY, (column * node_width,
                             0), (column * node_width, win_width))


def draw(window, grid, rows, win_width):
    """
    This function will actually make the changes on our pygame window.
    """
    win.fill(WHITE)  # every frame we show, we will fill it in white

    for row in grid:
        for node in row:
            # Call the draw method in the Spot class and draw itself on the window
            node.draw(window)

    draw_grid(window, rows, win_width)
    pygame.display.update()     # append all the changes to our pygame window


def get_clicked_position(position, nbr_rows, win_width):
    """
    Based on a (y, x) position return by pygame, this function will figure out in which
    node we clicked.
    """
    node_width = win_width // nbr_rows
    y, x = position

    clicked_row = y // node_width
    clicked_col = x // node_width

    return clicked_row, clicked_col


###############################
########## ALGORITHM ##########
###############################


def heuristic(p1, p2):
    """
    This is the heuristic that we will use in the A* algorithm. This one will compute
    the _Manhattan Distance_ between a point (p1) and an other point (p2)
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
