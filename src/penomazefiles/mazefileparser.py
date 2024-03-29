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
from .maze import Maze
import copy

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

        lineNb = 0
        for line in self.stream:
            lineNb +=1

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
            tokenNb =0
            for token in tokens:
                tokenNb +=1
                try:
                    self.token_consumer(token)
                except SpecificationViolationError as e:
                    #Todo:reraise the exception but some how augment it with the
                    # following information instead of printing it directly to
                    # sys.stdout
                    e.line_nb = lineNb
                    e.token_nb = tokenNb
                    e.token_value = token
                    print('line number: {:d}'.format(lineNb))
                    print('line value: {!r}'.format(line))
                    print('token number: {:d}'.format(tokenNb))
                    print('{!s}'.format(e.args))
                    raise


class SpecificationViolationError(Exception):
    """Raised in case of mazefile syntax violations. 

    It useually means that some part of the maze file could not be interpreted.

    The args attribute may contain some extra info.
    """
    def __init__(self,args):
        super().__init__(args)
        print('SpecificationViolationError: {!s}'.format(str(args)))


class MazeFileParser(object):
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

    def __init__(self):
        self.width = None
        self.height = None


        # coordinate of the next tile token
        self.currentX = 0
        self.currentY = 0

        self.maze_token_parser = None

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
                print('token value: {:s}'.format(token))
                raise SpecificationViolationError(
                    'The first token must be an integer')

        elif(self.height is None):
            try:
                self.height = int(token)
            except ValueError:
                print('token value: {:s}'.format(token))
                raise SpecificationViolationError(
                    'The second token must be an integer')
        else:
            
            if self.currentX > self.width-1:
                print('token value: {:s}'.format(token))
                raise SpecificationViolationError(
                        'To many tiles')

            if self.currentY > self.height-1:
                print('token value: {:s}'.format(token))
                raise SpecificationViolationError(
                        'To many tiles')
            try:
                self.produce(((self.currentX,self.currentY),token))
            except SpecificationViolationError as e:
                print('coordinate: ({:d},{:d})'.format(self.currentX,self.currentY))
                print('Skip this coordinate.')
                raise
            finally:
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

    _maze = None

    # dictionary of valid tile tokens mapped to actual tiles
    from . import tiles
    _TILES = {'Straight': tiles.Straight(),
              'Corner': tiles.Corner(),
              'T': tiles.T(),
              'DeadEnd':tiles.DeadEnd(),
              'Cross':tiles.Cross(),
              'Closed':tiles.Closed(),
              'Seesaw':tiles.Seesaw()}


    # dictionary of valid orientation tokens mapped to the required number or
    # rotations.
    _ROTATIONS = {'N': 0,
                  'E': 1,
                  'S': 2,
                  'W': 3}

    def __init__(self):
        """docstring for # TODO: write """
        self._maze= Maze()


    def getMaze(self):
        """
        Return the maze object
        """
        return self._maze

    def consume(self,token):
        coordinate = token[0]
        token = token[1]

        tokenparts = token.split('.')

        try: 
            if len(tokenparts) <2 :
                raise SpecificationViolationError(
                    'Each tile token must consist of at least a tile and an orientation seperated by a point')

            try:
                tile = self._TILES[tokenparts[0]]
            except KeyError:
                raise SpecificationViolationError(
                        "Invalid tile token '{:s}'".format(tokenparts[0]))
            else:
                #todo: replace with a proper Tile specific deepcopy routine
                tile = copy.deepcopy(tile)

            try:
                rotations = self._ROTATIONS[tokenparts[1]]
            except KeyError as e:
                raise SpecificationViolationError(
                        "Invalid Orientation Token '{:s}'".format(tokenparts[1])) from e

        except SpecificationViolationError:
            print('token value: {:s}'.format(token))
            raise

        self._maze.add_tile(coordinate,tile.rotate(rotations))

