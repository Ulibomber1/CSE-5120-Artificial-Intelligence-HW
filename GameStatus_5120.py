# -*- coding: utf-8 -*-


class GameStatus:


	def __init__(self, board_state, turn_O):

		self.board_state = board_state
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

		# Simply: self.board_state[row][column]

		# to iterate in a col, do self.board_state[0][j] to [n][j]
		# to iterate in a row, do self.board_state[i][0] to [i][n] 
		# to iterate in up-left to down-right diagonal, do self.board_state[0][0] to [n][n]
		# to iterate in up-right to down-left diagonal, do self.board_state[0][n] to [n][0]

		# therefore, adjacency formulas (diagonals are combinations):
		# left: self.board_state[i][j-1]
		# right: self.board_state[i][j + 1]
		# up: self.board_state[i - 1][j]
		# down: self.board_state[i + 1][j]

		

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
		moves = []
		"""
        YOUR CODE HERE TO ADD ALL THE NON EMPTY CELLS TO MOVES VARIABLES AND RETURN IT TO BE USE BY YOUR
        MINIMAX OR NEGAMAX FUNCTIONS
        """
		return moves


	def get_new_state(self, move):
		new_board_state = self.board_state.copy()
		x, y = move[0], move[1]
		new_board_state[x,y] = 1 if self.turn_O else -1
		return GameStatus(new_board_state, not self.turn_O)
