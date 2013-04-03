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
    
    """ Wall list of this Tile

    A list with 4 booleans indication the presence of a wall in the north, 
    east, south and west direction of the tile respectively
    """
    walls = None



    """North direction Identifier"""
    NORTH = 0
    """East direction Identifier"""
    EAST  = 1
    """South direction Identifier"""
    SOUTH = 2
    """West direction Identifier"""
    WEST  = 3

    def __init__(self, walls = [0,0,0,0], rotations=0):
        """ Create a new Tile object

        Input is a list with 4 booleans values indicating the presence of a 
        wall in the north, east, south and west direction respectively.
        """

        if len(walls) != 4 :
            raise ValueError('The walls argument must contain 4 booleans, not {:d}'.format(len(walls)))

        super(Tile, self).__init__()
        self.walls = [bool(x) for x in walls]
        self.rotate(rotations)

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

    def rotate(self, number=1):
        """Rotate this Tile <number> times 90 degrees counter clockwise"""
        for rotationNumber in range(0,number):
            tmp= self.walls[3]
            for i in range(3,0,-1):
                self.walls[i] = self.walls[i-1]
            self.walls[0] = tmp

        return self

    def __str__(self):
        str_= 'Tile('
        str_ = str_ + ','.join(map(lambda x : str(x), self.walls))
        str_ = str_ + ')'
        return str_


    def ascii_art(self):
        """
        return a list of 5 strings each of which 9 characters long. 

        these 5 strings form a 5 by 9 ascii art representation of this Tile 
        which is approximately square.
        """
        ascii_art = []
        if self.has_wall(Tile.NORTH) :
            ascii_art.append('+-------+')
        else:
            ascii_art.append('+       +')
        
        if self.has_wall(Tile.WEST) :
            ascii_art.append('|    ')
            ascii_art.append('|    ')
            ascii_art.append('|    ')
        else:
            ascii_art.append('     ')
            ascii_art.append('     ')
            ascii_art.append('     ')

        if self.has_wall(Tile.EAST) :
            ascii_art[1] = ascii_art[1] + '   |'
            ascii_art[2] = ascii_art[2] + '   |'
            ascii_art[3] = ascii_art[3] + '   |'
        else:
            ascii_art[1] = ascii_art[1] + '    '
            ascii_art[2] = ascii_art[2] + '    '
            ascii_art[3] = ascii_art[3] + '    '

        if self.has_wall(Tile.SOUTH) :
            ascii_art.append('+-------+')
        else:
            ascii_art.append('+       +')

        return ascii_art

    def print_ascii_art(self):
        for line in self.ascii_art():
            print(line)

    def __eq__(self,other):
        return (isinstance(other,self.__class__)) and (self.walls == other.walls)

    def __ne__(self,other):
        return not self.__eq__(other)



class Straight(Tile):
    """Create a Straight tile.

    A straight Tile is  tile with walls in the West and East direction, and 
    is open  in the North and South direction
    """

    def __init__(self,rotations=0):
        super().__init__([False, True, False, True], rotations)

class Corner(Tile):
    """Create a Corner tile.

    A Corner Tile is  tile with walls in the West and North direction, and 
    is open  in the East and South direction
    """

    def __init__(self,rotations=0):
        super().__init__([True, False, False, True],rotations)

class T(Tile):
    """Create a T tile.

    A T Tile is  tile a wall in the North direction and is open elsewhere
    """

    def __init__(self,rotations=0):
        super().__init__([True, False, False, False],rotations)

class DeadEnd(Tile):
    """Create a DeadEnd tile.

    A DeadEnd Tile is  tile which is open in the south and has walls in all 
    other directions.
    """

    def __init__(self,rotations=0):
        super().__init__([True, True, False, True],rotations)

class Cross(Tile):
    """Create a Cross tile.

    A Cross Tile is  tile which is open in all directions.
    """

    def __init__(self,rotations=0):
        super().__init__([False, False, False, False],rotations)

class Closed(Tile):
    """Create a Closed tile.

    A Closed Tile is  has walls in all directions.
    """

    def __init__(self,rotations=0):
        super().__init__([True, True, True, True],rotations)

class Seesaw(Tile):
    """Create a Seasaw tile.

    A Seesaw Tile is  has walls in East and west and in open in the north and south direction.
    """

    def __init__(self,rotations=0):
        super().__init__([False, True, False,True],rotations)


if __name__ == '__main__':
    import unittest
    unittest.main()
