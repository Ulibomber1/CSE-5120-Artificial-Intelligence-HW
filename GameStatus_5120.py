# -*- coding: utf-8 -*-
from enum import Enum
from copy import deepcopy

class SpaceState(Enum):
    EMPTY = 0
    CIRCLE = 1
    CROSS = -1

class BoardSpace:
    def __init__(self,x ,y):
        self.x = x
        self.y = y

        # acts as an Enumerator for possible Cell States.
        self.state = SpaceState.EMPTY

class GameStatus:
	def __init__(self, board_state, turn_O):

		self.board_state = board_state # should be a 2d list (matrix)
		self.turn_O = turn_O
		self.oldScores = 0
		self.winner = ""


	def is_terminal(self):
		"""
        YOUR CODE HERE TO CHECK IF ANY CELL IS EMPTY WITH THE VALUE 0. IF THERE IS NO EMPTY
        THEN YOU SHOULD ALSO RETURN THE WINNER OF THE GAME BY CHECKING THE SCORES FOR EACH PLAYER 
        """
		for row in range(len(self.board_state)):
			for column in range(len(self.board_state[row])):
				if self.board_state[row][column] == 0:
					return False

		if self.oldScores == 0:
			self.winner = "Draw"
		elif self.oldScores > 0:
			self.winner = "Human"
		else:
			self.winner = "AI"
		return True
		

	def get_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)
        
        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        """   
		
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		check_point = 3 if terminal else 2
		
		# directions are grouped according to opposing directions
		directionPairs = [((1,0),(-1,0)),
					  ((0,1),(0,-1)),
					  ((1,1),(-1,-1)),
					  ((-1,1),(1,-1))]

		scoring_sequences: dict = {} # triple tuples (x,y), w/ value

		# this feels like a code smell... so many tabs, really long statements
		for row in range(rows):
			for col in range(cols):

				origin_state = self.board_state[row][col]
				if origin_state == 0:
					break

				for directionPair in directionPairs:
					accumulatedSequence = [(col, row)]
					for direction in directionPair:
						if len(accumulatedSequence) >= 3:
							break
						try:
							if row + direction[1] < 0 or col + direction[0] < 0:
								continue
							if origin_state == self.board_state[row + direction[1]][col + direction[0]]:
								accumulatedSequence.append((col + direction[0], row + direction[1]))
								if row + (2 * direction[1]) < 0 or col + (2 * direction[0]) < 0:
									continue
								if len(accumulatedSequence) < 3 and origin_state == self.board_state[row + (2 *direction[1])][col + (2 * direction[0])]:
									accumulatedSequence.append((col + (2 * direction[0]), row + (2 * direction[1])))
									break
						except IndexError:
							pass

					if len(accumulatedSequence) != 3:
						continue
					tuple1 , tuple2, tuple3 = accumulatedSequence
					key= frozenset({tuple1, tuple2, tuple3})
					if scoring_sequences.get(key, False) == False:
						scoring_sequences[key] = origin_state
						scores += origin_state
		return scores


	"""
    YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
    YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                            FOR HUMAN PLAYER INSTEAD OF 
                                                                            SCORES = SCORES + 1)
    """
	def get_negamax_scores(self, terminal):

		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		check_point = 3 if terminal else 2
		
		# directions are grouped according to opposing directions
		directionPairs = [((1,0),(-1,0)),
					  ((0,1),(0,-1)),
					  ((1,1),(-1,-1)),
					  ((-1,1),(1,-1))]

		scoring_sequences: dict = {} # triple tuples (x,y), w/ value

		# this feels like a code smell... so many tabs, really long statements
		for row in range(rows):
			for col in range(cols):

				origin_state = self.board_state[row][col]
				if origin_state == 0:
					break

				for directionPair in directionPairs:
					accumulatedSequence = [(col, row)]
					for direction in directionPair:
						if len(accumulatedSequence) >= 3:
							break
						try:
							if row + direction[1] < 0 or col + direction[0] < 0:
								continue
							if origin_state == self.board_state[row + direction[1]][col + direction[0]]:
								accumulatedSequence.append((col + direction[0], row + direction[1]))
								if row + (2 * direction[1]) < 0 or col + (2 * direction[0]) < 0:
									continue
								if len(accumulatedSequence) < 3 and origin_state == self.board_state[row + (2 *direction[1])][col + (2 * direction[0])]:
									accumulatedSequence.append((col + (2 * direction[0]), row + (2 * direction[1])))
									break
						except IndexError:
							pass

					if len(accumulatedSequence) != 3:
						continue
					tuple1 , tuple2, tuple3 = accumulatedSequence
					key= frozenset({tuple1, tuple2, tuple3})
					if scoring_sequences.get(key, False) == False:
						scoring_sequences[key] = origin_state
						scores += 100 if origin_state == 1 else -1
		return scores

	def get_moves(self):
		moves: list = []
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		"""
        YOUR CODE HERE TO ADD ALL THE NON EMPTY CELLS TO MOVES VARIABLES AND RETURN IT TO BE USE BY YOUR
        MINIMAX OR NEGAMAX FUNCTIONS
        """
		for row in range(rows):
			for col in range(cols):
				value = self.board_state[row][col]
				if self.board_state[row][col] == 0:
					moves.append((col, row)) # like (x,y)
		return moves
	

	# for the nodes in tree searches
	def get_new_state(self, move):
		new_board_state = deepcopy(self.board_state) # deep copy to prevent mutation
		x, y = move[1], move[0]
		new_board_state[x][y] = 1 if self.turn_O else -1
		return GameStatus(new_board_state, not self.turn_O)

	# for setting this instance's state
	def set_new_state(self, move):
		x, y = move[1], move[0]
		self.board_state[x][y] = 1 if self.turn_O else -1
		
