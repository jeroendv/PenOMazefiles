import unittest
from penomazefiles.mazefileparser import MazeFileBuilder
from penomazefiles.mazefileparser import SpecificationViolationError

class TestMazeFiles(unittest.TestCase):
    """
    Unit test Case class for testing maze files
    """

    def test_demo2_orig(self):
        """
        Check that the original maze file for demo 2 is indeed faulty. The
        MazeFileBuilder should raise an error when trying to parse it.

        The file  can be found at

            src/testmazes/demo2.orig.maze
        """
        with self.assertRaises(SpecificationViolationError):
            MazeFileBuilder(open('testmazes/demo2.orig.maze','r'))

    def test_demo2_fixed(self):
        """
        Check that the fixed version of the original maze file for demo 2 is
        indeed fixed. I.e. the MazeFileBuilder should *not* raise an error when
        trying to parse it.

        The file can be found at

            src/testmazes/demo2.fixed.maze
        """
        try:
            MazeFileBuilder(open('testmazes/demo2.fixed.maze','r'))
        except SpecificationViolationError:
            self.fail('Valid mazefile, yet a SpecificationViolationError is still raised')

    def test_demo2_bronze(self):
        """
        Check that the version of the original maze file for demo 2 as provided
        by team bronze  is also incorrect.  I.e. the MazeFileBuilder should
        raise an error when trying to parse it.

        The file can be found at

            src/testmazes/demo2.bronz.maze
        """
        with self.assertRaises(SpecificationViolationError):
            MazeFileBuilder(open('testmazes/demo2.brons.maze','r'))







