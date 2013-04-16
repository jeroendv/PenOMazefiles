'''
File: Maze.py
Author: Jeroen De Vlieger
Description: 

Module for code related to maze files
'''

class Maze(object):
    """A Maze is a collection of 'Tile' objects

    Each tile has a unique coordinate assciated with it and together they form
    a maze.

    The coordinates (x,y) are integers, where y increases downward and x
    increases from left ot right as illustrated below

      0       1      2      3      4   x
       +------+------+------+------+----> 
       |(0,0)  (1,0)  (2,0)  (3,0)
       | 
      1+      +      +      +      +
       |(0,1)  (1,1)  (2,1)  (3,1)
       |
      2+      +      +      +      +
       |(0,2)  (1,2)  (2,2)  (3,2)
      y|
       V


    Tiles have a dimension of 1 by 1 and its associated coordinate denotes the
    left upper corner of the tile.


    todo: type checking of the methods
    todo: robustify for None arguments
    """

   
    """
    The maze is stored as a dictionary of Tile objects with the tile
    coordinates a its key.
            { (x,y) -> Tile } 
    This ensures that each coordinate can only be
    associated with one tile.

    """
    def __init__(self):
        super(Maze, self).__init__()
        self._maze = {}

    def add_tile(self, coordinate, tile):
        """Add a tile to this maze on a specific coordinate

        'coordinate' is a 2 dimensional tuple of integers (int, int) denoting
        the position if the maze where 'tile' should be added.
        If a tile is already present on that coordinate then it gets replaced.
        """
        self._maze[coordinate] = tile

    def get_tile(self, coordinate):
        """
        Return the tile at a given coordinate.

        Return None if there is no tile at the given coordinate
        """
        
        fallback_value = None
        return self._maze.get(coordinate,fallback_value)

    def get_boundingbox(self):
        """
        compute a bounding box of the current maze.

        Returns  a tuple of coordinates (lu, rl). lu is the coordinate of the
        left upper point of the bounding box while rl is the coordinate of the
        right lower point of the bounding box
        """
        tile_iterator = iter(self)
        value = next(tile_iterator)
        if value[1] is not None:
            min_x = value[0][0]
            max_x = min_x + 1
            min_y = value[0][1]
            max_y = min_y + 1

        for value in tile_iterator:
            if value[1] is not None:
                if value[0][0] < min_x:
                    min_x = value[0][0]
                if value[0][0]+1> max_x:
                    max_x = value[0][0] +1
                if value[0][1] < min_y:
                    min_y = value[0][1]
                if value[0][1]+1> max_y:
                    max_y = value[0][1] +1

        return ((min_x, min_y), (max_x, max_y))

    def __eq__(self,other):
        if isinstance(other,self.__class__):
            return other._maze == self._maze
        else:
            return False

    def __ne__(self,other):
        return not self.__eq__(other)

    def __iter__(self):
        """return an Iterator for a maze object
        
        The iterator traverses the maze object returning all (coordinate, tile) tuples.
        """
        return iter(self._maze.items())

class AsciiArtRenderer(object):
    """docstring for AsciiArtMaze"""

    def render(self,maze,stream):
        """Render an ascii art representation of a maze to the given text stream"""
        ((min_x,min_y),(max_x,max_y)) = maze.get_boundingbox()

        # each tile in 8 by 5 character
        for major_row_index in range(min_y, max_y):
            for minor_row_index in range(0,5):
                # print a line
                for major_column_index in  range(min_x,max_x):
                    tile = maze.get_tile((major_column_index,major_row_index))
                    if tile is not None:
                        stream.write(tile.ascii_art()[minor_row_index])
                    else:
                        stream.write(' '*9)
                # end the line with a newline
                stream.write('\n')


