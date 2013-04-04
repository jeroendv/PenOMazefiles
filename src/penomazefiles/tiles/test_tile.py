'''
File: test_tile.py
Author: Me
Description: 

unit test for the tile module
#todo Tile.py should be a module named tiles.py in the project root, instead of
a module in the tiles package
'''


import unittest
from .Tile import *


class Test_Tile(unittest.TestCase):

    tile = None

    def setUp(self):
        self.tile = Tile([True, 0, 1, 0])

    def tearDown(self):
        self.tile = None

    def test_has_wall(self):
        self.assertEqual(self.tile.has_wall(Tile.NORTH), True)
        self.assertEqual(self.tile.has_wall(Tile.EAST), False)
        self.assertEqual(self.tile.has_wall(Tile.SOUTH), True)
        self.assertEqual(self.tile.has_wall(Tile.WEST), False)
    def test_is_open(self):

        tile = Tile([True, 0, 1, 0])
        self.assertEqual(tile.is_open(Tile.NORTH), False)
        self.assertEqual(tile.is_open(Tile.EAST), True)
        self.assertEqual(tile.is_open(Tile.SOUTH), False)
        self.assertEqual(tile.is_open(Tile.WEST), True)

    def test_rotate_once(self):
        self.tile.rotate(0)
        self.assertListEqual(self.tile.walls,[1,0,1,0])
        self.tile.rotate(1)
        self.assertListEqual(self.tile.walls,[0,1,0,1])
        self.tile.rotate(1)
        self.assertListEqual(self.tile.walls,[1,0,1,0])
        self.tile.rotate(1)
        self.assertListEqual(self.tile.walls,[0,1,0,1])
        self.tile.rotate(1)
        self.assertListEqual(self.tile.walls,[1,0,1,0])

    def test_rotate_twice(self):
        self.tile.rotate(0)
        self.assertListEqual(self.tile.walls,[1,0,1,0])
        self.tile.rotate(2)
        self.assertListEqual(self.tile.walls,[1,0,1,0])
        self.tile.rotate(2)
        self.assertListEqual(self.tile.walls,[1,0,1,0])

    def test_rotate_three(self):
        self.tile.rotate(0)
        self.assertListEqual(self.tile.walls,[1,0,1,0])
        self.tile.rotate(3)
        self.assertListEqual(self.tile.walls,[0,1,0,1])
        self.tile.rotate(3)
        self.assertListEqual(self.tile.walls,[1,0,1,0])

    def test_rotate_four(self):
        self.tile.rotate(4)
        self.assertListEqual(self.tile.walls,[1,0,1,0])

    def test_ascii_art(self):
        """
        Test asci art of unittest Tile
        """
        self.assertListEqual(self.tile.ascii_art(),
                ['+-------+',
                 '         ',
                 '         ',
                 '         ',
                 '+-------+']
            )

    def test_tile_equality(self):
        self.assertEqual(Straight(), Straight())
        self.assertEqual(Straight(), Straight(4))
        self.assertEqual(Straight(), Straight(2))

        self.assertNotEqual(Straight(),Straight(1))
        self.assertNotEqual(Straight(),Corner())
        self.assertNotEqual(Straight(),Seesaw())

    def test_CornerRotate(self):
        self.assertEqual(Corner(1), Corner(0).rotate(1))
        self.assertEqual(Corner(1).walls, [1,1,0,0])




class Test_Tile_Types(unittest.TestCase):
    """Test of different Tile types
    """
        
    def test_t(self):
        t = T()
        self.assertEqual(t.has_wall(Tile.NORTH),True)
        self.assertEqual(t.has_wall(Tile.EAST),False)
        self.assertEqual(t.has_wall(Tile.SOUTH),False)
        self.assertEqual(t.has_wall(Tile.WEST),False)

    def test_closed(self):
        t = Closed()
        self.assertEqual(t.has_wall(Tile.NORTH),True)
        self.assertEqual(t.has_wall(Tile.EAST), True)
        self.assertEqual(t.has_wall(Tile.SOUTH),True)
        self.assertEqual(t.has_wall(Tile.WEST), True)

    def test_corner(self):
        t = Corner()
        self.assertEqual(t.has_wall(Tile.NORTH),True)
        self.assertEqual(t.has_wall(Tile.EAST), False)
        self.assertEqual(t.has_wall(Tile.SOUTH),False)
        self.assertEqual(t.has_wall(Tile.WEST), True)

    def test_cross(self):
        t = Cross()
        self.assertEqual(t.has_wall(Tile.NORTH),False)
        self.assertEqual(t.has_wall(Tile.EAST), False)
        self.assertEqual(t.has_wall(Tile.SOUTH),False)
        self.assertEqual(t.has_wall(Tile.WEST), False)


    def test_deadend(self):
        t = DeadEnd()
        self.assertEqual(t.has_wall(Tile.NORTH),True)
        self.assertEqual(t.has_wall(Tile.EAST), True)
        self.assertEqual(t.has_wall(Tile.SOUTH),False)
        self.assertEqual(t.has_wall(Tile.WEST), True)

    def test_seesaw(self):
        t = Seesaw()
        self.assertEqual(t.has_wall(Tile.NORTH),False)
        self.assertEqual(t.has_wall(Tile.EAST), True)
        self.assertEqual(t.has_wall(Tile.SOUTH),False)
        self.assertEqual(t.has_wall(Tile.WEST), True)

    def test_straight(self):
        t = Straight()
        self.assertEqual(t.has_wall(Tile.NORTH),False)
        self.assertEqual(t.has_wall(Tile.EAST), True)
        self.assertEqual(t.has_wall(Tile.SOUTH),False)
        self.assertEqual(t.has_wall(Tile.WEST), True)





if __name__ == '__main__':
    unittest.main()


