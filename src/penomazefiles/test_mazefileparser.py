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
                  '', # empty line
                  ' # some comment line',
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




class Test_MazeFileParser(unittest.TestCase):
    """Test of the MazeFileParser class"""

    def setUp(self):
        # string list corresponding the lines of apossible mazefile
        self.input_linelist = ['2 3',
                  '', # empty line
                  ' # some comment line',
                  'token.1    token.2 #line 1',
                  'token.3    token.4 # example comment',
                  'token.5    token.6']
        self.input_tokenlist= ['2','3',
                  'token.1', 'token.2',
                  'token.3', 'token.4',
                  'token.5', 'token.6']

        # the list of tokens in present in the linestream
        self.true_outputlist = [
                  ((0,0),'token.1'), ((1,0),'token.2'),
                  ((0,1),'token.3'), ((1,1),'token.4'),
                  ((0,2),'token.5'), ((1,2),'token.6')]

    def test_valid_tokenstream(self):
        """parse a valid 2x3 mazefile token stream"""
        
        # create MazeFileParser and subscribe a consumer to build list of
        # produced tokens which can then be compared with the true output list
        parser = MazeFileParser()
        outputlist = []
        parser.add_token_parser(outputlist.append)

        for token in self.input_tokenlist:
            parser.consumeToken(token)

        self.assertEqual(outputlist, self.true_outputlist)

    @unittest.expectedFailure
    def test_incomplete_tokenstream(self):
        """
        test an incomplete 2x3 mazefile token stream

        fixme: introduce a start and end token to identify the start of
        mazefile token stream and the end of one. This is the only way to
        detect that tiles are missing. instead of still on the way.
        """
        
        del self.input_tokenlist[-1]

        parser = MazeFileParser()
        with self.assertRaises(SpecificationViolationError):
            for  token in self.input_tokenlist:
                parser.consumeToken(token)
            
    def test_tobig_tokenstream(self):
        """
        test an 2x3 mazefile token stream which contains one tile token to much
        """
        
        self.input_tokenlist.append(((10,10),'token'))

        parser = MazeFileParser()
        with self.assertRaises(SpecificationViolationError):
            for  token in self.input_tokenlist:
                parser.consumeToken(token)


    def test_withTokenizer(self):
        """docstring for # string list corresponding the lines of apossible m"""

        tokenizer = MazeFileTokenizer(self.input_linelist)

        parser = MazeFileParser()
        tokenizer.addTokenConsumer(parser.consumeToken)

        outputlist = []
        parser.add_token_parser(outputlist.append)

        tokenizer.start()
        self.assertListEqual(outputlist, self.true_outputlist)


    def test_missingdimnsion_tokenstream(self):
        """
        chech that a SpecificationViolationError is raised when procosessing
        a 2x3 mazefile token stream which which does not start with 2 integers
        to specify maze dimentions
        """
        
        # delete the first token specifying maze width
        del self.input_tokenlist[0]

        # check whether an SpecificationViolationError is raised
        parser = MazeFileParser()
        with self.assertRaises(SpecificationViolationError):
            for  token in self.input_tokenlist:
                parser.consumeToken(token)




if __name__ == '__main__':
    unittest.main()
