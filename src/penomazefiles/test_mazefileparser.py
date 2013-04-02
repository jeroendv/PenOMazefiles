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
                  'token.drie']

        # the list of tokens in present in the linestream
        true_tokenlist = ['2',
                     '3',
                     'token.1',
                     'token2',
                     'token.drie']


        # construct a tokenizer object on the linestream
        t = MazeFileTokenizer(linestream)

        #initialize TokenListBuilder object and register it with the tokenizer
        token_listbuilder = TokenListBuilder()
        t.addTokenConsumer(token_listbuilder.consume)


        # start the tokenizing process
        t.start()


        self.assertEqual(token_listbuilder.tokenlist,true_tokenlist)



class TokenListBuilder(penomazefiles.mazefileparser.TokenConsumer):
    """
    Token consumer that builds a list of all consumed tokens
    """
    tokenlist = []

    def consume(self, token):
        self.tokenlist.append(token)

if __name__ == '__main__':
    unittest.main()
