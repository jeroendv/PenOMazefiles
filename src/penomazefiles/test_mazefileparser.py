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
        linestream = ['2 3',
                  'token.1  token2 #comment',
                  'token.drie']


        t = MazeFileTokenizer(linestream)
        token_list = TokenListBuilder()

        t.addTokenConsumer(token_list)
        t.start()

        self.assertEqual(token_list.tokenlist,
            ['2',
             '3',
             'token.1',
             'token2',
             'token.drie'])



class TokenListBuilder(penomazefiles.mazefileparser.TokenConsumer):
    """
    Token consumer that builds a list of received tokens
    """
    tokenlist = []

    def consume(self, token):
        self.tokenlist.append(token)

if __name__ == '__main__':
    unittest.main()
