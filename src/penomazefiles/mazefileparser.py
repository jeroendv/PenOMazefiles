'''
File: 2012_2013_parser.py
Author: Jeroen De Vlieger
Description: 

P&O 2012-2013 maze file parser

This module can build a maze object correcponding to the maze specified in a mazefile.

The maze file describes a rectangular maze. It first list the width and
height of the maze followed by a list of tiles. Each tile has type and
orientation. A tile can also boast a barcode, player start position or
the presence of an object.

see Toledo for specifications of mazefiles
'''

def MazeFileBuilder(stream):
    """
    Parse a stream of lines to build a Maze object

    Return a Maze 
    """
    # step 1: tokenizing the stream
    token_stream = MazeFileTokenizer(stream)

    # step 2: extend tiles with coordinate information
    mazefile_parser = MazeFileParser()
    token_stream.addTokenConsumer(mazefile_parser.consumeToken)

    # step 3; build a Maze object
    mazetoken_parser = MazeTokenParser()
    mazefile_parser.add_token_parser(mazetoken_parser.consume)

    token_stream.start()
    return mazetoken_parser.getMaze()



class MazeFileTokenizer(object):
    """
    Filter out comments from a sequence of text lines and split it in tokens.
    These tokens are then passed to a consumer function for further processing.

    Each strings represents a single line from a mazefile. Comments start with
    a '#' character and run till the end of the line.

    mazefile tokens are single words seperated by a newline or white space.
    """

    # todo: possibly turn the start method into a simple module function
    # def tokenize(stream, consumer)
    #
    # con:
    #  - it forces a bottum up construction of the parser blocks. because the
    # consumer function must be defined before the top level tokenizer can be invoked.
    #
    # pro:
    #  + shorter more compact code, I.e. a single function instead of a whole
    #  class with several methods
    #  + avoid unwanted behaviour, where the user could invoke start() twice.
    #  Either this must be caught and raise an error or document that this
    #  should simply not be done. Or ..  make the stream an argument of the
    #  start() method.

    # a token consumer function wich should accept a token as the single
    # argument
    token_consumer = None

    stream = None

    def __init__(self,stream):
        """
        Create a new MazeFileTokenizer object to tokenize a stream of text 
        lines.
        """
        self.stream = stream

    def addTokenConsumer(self,token_consumer):
        """subscribe a token consumer that will process all the tokens 
        generated from the stream of text lines when start() is invoked.

        token_consumer should be a fuction which accepts a single token as
        argument.
        """
        self.token_consumer = token_consumer

    def start(self):
        """
        Process the stream of text lines producing a sequence of tokens that 
        are to be processed by the consumer.
        """
        if self.token_consumer is None:
            return

        for line in self.stream:
            # remove comments
            comment_start_index = line.find('#')
            if(comment_start_index != -1):
                line = line[0:comment_start_index]

            # remove leading and trailing white space
            line = line.strip()

            # skip empty lines
            if len(line) == 0:
                continue

            # split line in tokens
            tokens = line.split()
            for token in tokens:
                self.token_consumer(token)

class TokenConsumer(object):
    """
    Abstract Consumer object for maze file Tokens
    """
    #todo: elliminate this class. It serves as an java like 'abstract class'
    #which is nonsensical in python which doens't really have such a language
    #construct
        
    def consume(self, token):
        """Consume mazefile tokens"""
        raise NotImplementedError()

class SpecificationViolationError(Exception):
    """Raised in case of mazefile syntax violations. 

    It useually means that some part of the maze file could not be interpreted.

    The args attribute may contain some extra info.
    """
        

class MazeFileParser(TokenConsumer):
    """
    A mazefile describes a rectangular maze with implicitly defined tile
    coordinates. A MazeFileParser object enriches the tile tokens from such a
    mazefile with explicit coordinates for the construction of a freeform Maze
    object.
    
    The first two tokens of should be numbers defining the width and height of
    the rectangular maze, as defined by the maze file spec. A
    SpecificationViolationError is raised if this is not the case.
    
    This is followed by a sequence of tokens representing tiles. Listing the
    tiles in each row from left to right starting with the top row. These tile
    tokens are complemented with an explicit coordinate based on the dimensions
    of the maze.
    
    The very first tile token will have coordinate (0,0), while
    the very last tile token will have coordinate (width -1, height -1) in
    accordance with the coordinate structure of penomazefiles.Maze.Maze object

    Each constructed tuple (coordinate, token) is passed to a consumer
    function for further processing.
    """

    width = None
    height = None

    # coordinate of the next tile token
    currentX = 0
    currentY = 0

    maze_token_parser = None

    def add_token_parser(self, token_parser):
        """
        Set a (coordinate, token) tuple to the consumer function.
        """
        self.maze_token_parser = token_parser
    

    def consumeToken(self, token):
        """Consume mazefile tokens"""
        if(self.width is None):
            try:
                self.width = int(token)
            except ValueError:
                raise SpecificationViolationError(
                    'The first token must be an integer')

        elif(self.height is None):
            try:
                self.height = int(token)
            except ValueError:
                raise SpecificationViolationError(
                    'The second token must be an integer')
        else:
            
            if self.currentX > self.width-1:
                raise SpecificationViolationError(
                        'To many tiles')

            if self.currentY > self.height-1:
                raise SpecificationViolationError(
                        'To many tiles')

            self.produce(((self.currentX,self.currentY),token))

            #update the coordinate
            if(self.currentX < self.width-1):
                self.currentX += 1
            else:
                self.currentX = 0
                self.currentY += 1



    def produce(self, coordinate_token):
        """
        pass a given (coordinate, token) tuple to the consumer function.
        """
        if(self.maze_token_parser is not None):
            self.maze_token_parser(coordinate_token)


class MazeTokenParser(object):
    """Class to parse Tokens (coordinate, token) tuples produced by the MazeFileParser object
    it turns token into proper Tile Objects and builds a Maze Object
    """

    from .Maze import Maze
    _maze = Maze()

    # dictionary of valid tile tokens mapped to actual tiles
    from .tiles import Tile
    _TILES = {'Straight': Tile.Straight(),
              'Corner': Tile.Corner(),
              'T': Tile.T(),
              'DeadEnd':Tile.DeadEnd(),
              'Cross':Tile.Cross(),
              'Closed':Tile.Closed(),
              'Seesaw':Tile.Seesaw()}


    # dictionary of valid orientation tokens mapped to the required number or
    # rotations.
    _ROTATIONS = {'N': 0,
                  'E': 1,
                  'S': 2,
                  'W': 3}


    def getMaze(self):
        """
        Return the maze object
        """
        return self._maze

    def consume(self,token):
        coordinate = token[0]
        token = token[1]

        tokenparts = token.split('.')

        if len(tokenparts) <2 :
            raise SpecificationViolationError(
                'Each tile token must consist of at least a tile and an orientation seperated by a point')
    
        try:
            tile = self._TILES[tokenparts[0]]
        except KeyError:
            raise SpecificationViolationError(
                    "Invalid tile token '{:s}'".format(tokenparts[0]))

        try:
            rotations = self._ROTATIONS[tokenparts[1]]
        except KeyError:
            raise SpecificationViolationError(
                    "Invalid Orientation Token '{:s}'".format(tokenparts[1]))

        self._maze.add_tile(coordinate,tile.rotate(rotations))

