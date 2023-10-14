# -*- coding: utf-8 -*-
from enum import Enum

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
		for row in self.board_state:
			for column in self.board_state[row]:
				if column == 0:
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

		scoring_sequences: dict = [] # triple tuples (x,y), w/ value

		# this feels like a code smell... so many tabs, really long statements
		for row in range(rows):
			for col in range(cols):
				origin_state = self.board_state[row][column]

				if origin_state == 0:
					break

				accumulatedSequence = [(col, row)]

				for directionPair in directionPairs:
					for direction in directionPair:
						try:
							if len(accumulatedSequence) < 3 and origin_state == self.board_state[row + direction[1]][col + direction[0]]:
								accumulatedSequence.append((row + direction[1], col + direction[0]))
								if len(accumulatedSequence) < 3 and origin_state == self.board_state[row + (2 *direction[1])][col + (2 * direction[0])]:
									accumulatedSequence.append((row + (2 * direction[1]), col + (2 * direction[0])))
						except:
							pass
				if len(accumulatedSequence) == 3 and scoring_sequences.get(accumulatedSequence, false) == false:
					scoring_sequences[accumulated_sequence] = origin_state
					scores += 1 if origin_state == 1 else -1

		return scores

		

	def get_negamax_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1)
        """
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		check_point = 3 if terminal else 2


	def get_moves(self):
		moves: dict = [] # dictionary for iterability and constant lookup time; no ordering property is necessary
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
					break
				moves.update({(col, row): value}) # like (x,y): (int between -1 to 1)
		return moves

	# Changed to mutating function since copies may cause unintended behavior 
	# and use more memory than necessary (based on OOP principles)
	def get_new_state(self, move):
		new_board_state = self.board_state.copy()
		x, y = move[0], move[1]
		new_board_state[x][y] = 1 if self.turn_O else -1
		self.board_state = new_board_state 
		self.turn_O = not turn_O 
