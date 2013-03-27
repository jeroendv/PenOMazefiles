'''
File: Tile.py
Author: Jeroen De Vlieger
Description: 

This module contains a Tile object
'''



class Tile(object):
    """A tile object

    A tile represents a square object with either a wall or no wall on either side
    """
    
    # a list with 4 bools indication the presence of a wall in the north, east,
    # south and west direction of the tile respectively
    walls = None

    """North direction Identifier"""
    NORTH = 0
    """East direction Identifier"""
    EAST  = 1
    """South direction Identifier"""
    SOUTH = 2
    """West direction Identifier"""
    WEST  = 3

    def __init__(self, walls = [0,0,0,0]):
        """ Create a new Tile object

        Input is a list with 4 booleans values indicating the presence of a 
        wall in the north, east, south and west direction respectively.
        """

        if len(walls) != 4 :
            raise ValueError('The walls argument must contain 4 booleans, not {:d}'.format(len(walls)))

        super(Tile, self).__init__()
        self.walls = [bool(x) for x in walls]

    def has_wall(self, direction):
        """
        Check whether this Tile object has a wall in the given direction

        Returns True if there is a wall or False other wise
        """
        if not isinstance(direction, int): 
            raise ValueError('direction must be an integer, not {:s}'.format(type(direction)))

        if direction >3 or direction < 0:
            raise ValueError('direction must be 0, 1, 2 or 3, not {:d}'.format(direction))

        return self.walls[direction];

    def is_open(self, direction):
        """
        Check whether this Tile object is open in the given direction, i.e. has no wall

        Returns False if there is a wall or True other wise
        """
        if not isinstance(direction, int): 
            raise ValueError('direction must be an integer, not {:s}'.format(type(direction)))

        if direction >3 or direction < 0:
            raise ValueError('direction must be 0, 1, 2 or 3, not {:d}'.format(direction))

        return not self.walls[direction];


    def __str__(self):
        str_= 'Tile('
        str_ = str_ + ','.join(map(lambda x : str(x), self.walls))
        str_ = str_ + ')'
        return str_
        

class Straight(Tile):
    """Create a Straight tile.

    A straight Tile is  tile with walls in the West and East direction, and 
    is open  in the North and South direction
    """

    def __init__(self):
        super().__init__([False, True, False, True])

class Corner(Tile):
    """Create a Corner tile.

    A Corner Tile is  tile with walls in the West and North direction, and 
    is open  in the East and South direction
    """

    def __init__(self):
        super().__init__([True, False, False, True])

class T(Tile):
    """Create a T tile.

    A T Tile is  tile a wall in the North direction and is open elsewhere
    """

    def __init__(self):
        super().__init__([True, False, False, False])

class DeadEnd(Tile):
    """Create a DeadEnd tile.

    A DeadEnd Tile is  tile which is open in the south and has walls in all 
    other directions.
    """

    def __init__(self):
        super().__init__([True, True, False, True])

class Cross(Tile):
    """Create a Cross tile.

    A Cross Tile is  tile which is open in all directions.
    """

    def __init__(self):
        super().__init__([False, False, False, False])

class Closed(Tile):
    """Create a Closed tile.

    A Closed Tile is  has walls in all directions.
    """

    def __init__(self):
        super().__init__([True, True, True, True])

class Seesaw(Tile):
    """Create a Seasaw tile.

    A Seesaw Tile is  has walls in East and west and in open in the north and south direction.
    """

    def __init__(self):
        super().__init__([False, True, False,True])


def main():
    """docstring for main"""
    print(Straight())
    print(Corner())
    print(T())
    print(DeadEnd())
    print(Cross())
    print(Closed())
    print(Seesaw())


if __name__ == '__main__':
    main()
