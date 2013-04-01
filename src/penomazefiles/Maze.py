'''
File: Maze.py
Author: Jeroen De Vlieger
Description: 

Module for code related to maze files
'''

class Maze(object):
    """A Maze is a collection of 'Tile' objects


    Each tile has a unique integer coordinate assciated with it and
    together they form a maze.

    Tiles have a dimension of 1 by 1 and the its coordinate denotes 
    its left upper corner.

    todo: type checking of the methods
    todo: robustify for None arguments
    """

   
    """
    The maze is stored as a dictionary of Tile objects with the tile
    coordinates a its key.
    """
    _maze = {};

    def __init__(self):
        super(Maze, self).__init__()

    def add_tile(self, coordinate, tile):
        """Add a tile to this maze on a specific coordinate

        'coordinate' is a 2 dimensional tuple of integers (int, int) denoting
        the position if the maze where 'tile' should be added.
        If a tile is already present on that coordinate then it gets replaced.
        """
        self._maze[coordinate] = tile


