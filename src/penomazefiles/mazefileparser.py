
'''
File: 2012_2013_parser.py
Author: Jeroen De Vlieger
Description: 

P&O 2012-2013 maze file parser
it returns a maze object correcponding to the maze specified in a mazefile

see Toledo for specifications of mazefiles
'''



def MazeFileTokenizer(filename,consumer):
    """
    Filter out comments from the maze file and then split it in tokens.
    These tokens are then given to a consumer for further processing

    mazefile tokens are single words seperated by a newline or white space
    """

    f = open(filename, w)
    for line in f:
        # remove comments
        comment_start_index = line.index('#')
        if(comment_start_index != -1)
            line = line[0,comment_start_index]

        # remove leading and trailing white space
        line = line.strip()

        # skip empty lines
        if len(line) == 0:
            continue

        # split line in tokens
        tokens = line.split()
        for token in tokens:
            consumer.consumer(token)



class MazeBuilder(object):
    """The MazeBuilder builds a maze file by consuming makefile tokens """
    def __init__(self, arg):
        super(MazeBuilder, self).__init__()
        self.arg = arg
        

