import unittest

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
