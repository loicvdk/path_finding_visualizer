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
########## GRID ##########
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
        self.width = width
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
        pass
