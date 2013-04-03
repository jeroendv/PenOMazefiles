import unittest
from .mazefileparser import *
import penomazefiles

class Test_MazeFileTokenizer(unittest.TestCase):
    
    def test_tokenizer(self):
        """
        Test the MazeFileTokenizer class
          + correct identification of tokens
          + removal of comments
        """
        # string list corresponding the lines of apossible mazefile
        linestream = ['2 3',
                  'token.1  token2 #comment',
                  'token.drie #multiword comment',
                  "4'th_token"]

        # the list of tokens in present in the linestream
        true_tokenlist = ['2',
                     '3',
                     'token.1',
                     'token2',
                     'token.drie',
                     "4'th_token"]


        # construct a tokenizer object on the linestream
        t = MazeFileTokenizer(linestream)

        # build a list of all generated tokens
        tokenlist = []
        t.addTokenConsumer(tokenlist.append)


        # start the tokenizing process
        t.start()


        self.assertEqual(tokenlist,true_tokenlist)




if __name__ == '__main__':
    unittest.main()
