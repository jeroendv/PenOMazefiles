'''
File: Maze.py
Author: Jeroen De Vlieger
Description: 

Module for code related to maze files
'''

class MazeTile(object):
    """
    A MazeTile contains a .tiles.Tile object and bidirectional pointers to the
    MazeTile objects that respectively lie to the North, East, South
    and West of this MazeTile
    """
    
    """
    Pointer to a Tile object. 
    This is never None.
    """
    tile = None
   
   """
   a list of 4 MazeTiles that respectively lie to the North, East, South
   and West of this MazeTile.

   invar: A adjacent tile equal to None means that there is no adjacent
   tile.

   invar: if links are not None then they are bidirectional.
   if self.adjacentTiles[Tile.NORTH].adjacentTiles[Tile.SOUTH] is self
   self.adjacentTiles[Tile.EAST].adjacentTiles[Tile.WEST] is self
   self.adjacentTiles[Tile.SOUTH].adjacentTiles[Tile.NORTH] is self
   self.adjacentTiles[Tile.WEST].adjacentTiles[Tile.EAST] is self
   """
    adjacentTiles = None

    def __init__(self, tile):
        super(CoordinateTile, self).__init__()
        self.arg = arg
        
class Maze(object):
    """A Maze in a interlinked list of CoordinateTile objects """
    def __init__(self, arg):
        super(Maze, self).__init__()
        self.arg = arg
        


