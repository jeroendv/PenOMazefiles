'''
File: Maze.py
Author: Jeroen De Vlieger
Description: 

Module for code related to maze files
'''
from .tiles import Tile

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
        (coordinate,tile) = next(tile_iterator)
        assert(tile is not None)
        min_x = coordinate[0]
        max_x = min_x + 1
        min_y = coordinate[1]
        max_y = min_y + 1

        for (coordinate,tile) in tile_iterator:
            if coordinate[0] < min_x:
                min_x = coordinate[0]
            if coordinate[0]+1> max_x:
                max_x = coordinate[0] +1
            if coordinate[1] < min_y:
                min_y = coordinate[1]
            if coordinate[1]+1> max_y:
                max_y = coordinate[1] +1

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



def are_walls_consistent(maze):
    """
    when two tiles touch then they should both have a wall or both be open.
    If this is not the case then maze is inconsistent.

    Return False if any two touching tiles are inconsistent. Return True otherwise
    """

    for ((x,y), current_tile) in iter(maze):
        # check to the north of the current tile
        bordering_tile = maze.get_tile((x,y-1))
        if bordering_tile is None:
            # if there is no bordering tile then there can't be any consistency
            # problems :-)
            pass
        else:
            if bordering_tile.has_wall(Tile.SOUTH) != current_tile.has_wall(Tile.NORTH):
                return False

        # check to the South of the current tile
        bordering_tile = maze.get_tile((x,y+1))
        if bordering_tile is None:
            # if there is no bordering tile then there can't be any consistency
            # problems :-)
            pass
        else:
            if bordering_tile.has_wall(Tile.NORTH) != current_tile.has_wall(Tile.SOUTH):
                return False

        # check to the East of the current tile
        bordering_tile = maze.get_tile((x+1,y))
        if bordering_tile is None:
            # if there is no bordering tile then there can't be any consistency
            # problems :-)
            pass
        else:
            if bordering_tile.has_wall(Tile.WEST) != current_tile.has_wall(Tile.EAST):
                return False

        # check to the West of the current tile
        bordering_tile = maze.get_tile((x-1,y))
        if bordering_tile is None:
            # if there is no bordering tile then there can't be any consistency
            # problems :-)
            pass
        else:
            if bordering_tile.has_wall(Tile.EAST) != current_tile.has_wall(Tile.WEST):
                return False

    # all tiles are consistent
    return True
