import unittest
from .Maze  import *
import penomazefiles.tiles.Tile
from penomazefiles.tiles import Tile
import io

class Test_Maze(unittest.TestCase):
    """
    Test of the Maze class
    """
    

    def test_str_strip(self):
        """
        linux style line endings, i.e. '\n' are stripped away using str.strip()
        """
        str_ = "blabla\n"
        self.assertEqual(len(str_),7)
        self.assertTrue(str_.endswith('\n'))
        self.assertFalse(str_.strip().endswith('\n'))
        self.assertEqual(len(str_.strip()),6)

    def test_str_strip2(self):
        """
        windows style line endings, i.e. '\r\n' are stripped away using str.strip()
        """
        str_ = "blabla\r\n"
        self.assertEqual(len(str_),8)
        self.assertTrue(str_.endswith('\r\n'))
        self.assertFalse(str_.strip().endswith('\r\n'))
        self.assertEqual(len(str_.strip()),6)


    def test_equality(self):
        maze1 = Maze()
        maze1.add_tile((0,0), penomazefiles.tiles.Tile.Straight(0))
        maze1.add_tile((1,0), penomazefiles.tiles.Tile.Corner(1))
        maze1.add_tile((0,1), penomazefiles.tiles.Tile.T(2))
        maze1.add_tile((1,1), penomazefiles.tiles.Tile.Closed())

        maze2 = Maze()
        maze2.add_tile((0,0), penomazefiles.tiles.Tile.Straight(0))
        maze2.add_tile((1,0), penomazefiles.tiles.Tile.Corner(1))
        maze2.add_tile((0,1), penomazefiles.tiles.Tile.T(2))
        maze2.add_tile((1,1), penomazefiles.tiles.Tile.Closed())

        self.assertEqual(maze1,maze2)
        self.assertTrue(maze1 == maze2)
        self.assertFalse(maze1 != maze2)

    def test_inequality(self):
        maze1 = Maze()
        maze1.add_tile((0,0), penomazefiles.tiles.Tile.Straight(0))
        maze1.add_tile((1,0), penomazefiles.tiles.Tile.Corner(1))
        maze1.add_tile((0,1), penomazefiles.tiles.Tile.T(2))
        maze1.add_tile((1,1), penomazefiles.tiles.Tile.Closed())

        maze2 = Maze()
        maze2.add_tile((0,0), penomazefiles.tiles.Tile.Straight(0))
        maze2.add_tile((1,0), penomazefiles.tiles.Tile.Corner(1))
        maze2.add_tile((0,1), penomazefiles.tiles.Tile.T(3))
        maze2.add_tile((1,1), penomazefiles.tiles.Tile.Closed())

        self.assertTrue(maze1 != maze2)
        self.assertNotEqual(maze1, maze2)
        self.assertFalse(maze1 == maze2)

    def test_get_boundingbox(self):
        maze1 = Maze()
        maze1.add_tile((0,0), penomazefiles.tiles.Tile.Straight(0))
        maze1.add_tile((1,0), penomazefiles.tiles.Tile.Corner(1))
        maze1.add_tile((0,1), penomazefiles.tiles.Tile.T(2))
        maze1.add_tile((1,1), penomazefiles.tiles.Tile.Closed())

        self.assertEqual(maze1.get_boundingbox(), ((0,0),(2,2)))

class Test_AsciiArtRenderer(unittest.TestCase):
    
    def test_description(self):
        maze = Maze()
        maze.add_tile((1,1), Tile.Corner())
        maze.add_tile((2,1), Tile.Corner(1))

        true_stream = """+-------++-------+
|                |
|                |
|                |
+       ++       +
"""

        stream = io.StringIO()
        AsciiArtRenderer().render(maze,stream)

        self.assertEqual(stream.getvalue(),true_stream)

        stream.close()
        
