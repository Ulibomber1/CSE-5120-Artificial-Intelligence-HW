from GameStatus_5120 import GameStatus


"""
YOUR CODE HERE TO FIRST CHECK WHICH PLAYER HAS CALLED THIS FUNCTION (MAXIMIZING OR MINIMIZING PLAYER)
YOU SHOULD THEN IMPLEMENT MINIMAX WITH ALPHA-BETA PRUNING AND RETURN THE FOLLOWING TWO ITEMS
1. VALUE
2. BEST_MOVE
    
THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
"""
def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
	terminal = game_state.is_terminal()
	if (depth==0) or (terminal):
		newScores = game_state.get_scores(terminal)
		return newScores, None
	moves: list = game_state.get_moves()
	best_move = None

	if maximizingPlayer:
		value = float('-inf')
		for move in moves:
			newGameStatus = game_state.get_new_state(move)
			minimaxReturn, next_best_move = minimax(newGameStatus, depth - 1, False, alpha, beta)

			if minimaxReturn > value:
				value = minimaxReturn
				best_move = move
			if value > beta:
				break
			alpha = max(alpha, value)
	else:
		value = float('inf')
		for move in moves:
			newGameStatus = game_state.get_new_state(move)
			minimaxReturn, next_best_move = minimax(newGameStatus, depth - 1, True, alpha, beta)

			if minimaxReturn < value:
				value = minimaxReturn
				best_move = move
			if value < alpha:
				break
			beta = min(beta, value)

	return value, best_move


"""
YOUR CODE HERE TO CALL NEGAMAX FUNCTION. REMEMBER THE RETURN OF THE NEGAMAX SHOULD BE THE OPPOSITE OF THE CALLING
PLAYER WHICH CAN BE DONE USING -NEGAMAX(). THE REST OF YOUR CODE SHOULD BE THE SAME AS MINIMAX FUNCTION.
YOU ALSO DO NOT NEED TO TRACK WHICH PLAYER HAS CALLED THE FUNCTION AND SHOULD NOT CHECK IF THE CURRENT MOVE
IS FOR MINIMAX PLAYER OR NEGAMAX PLAYER
RETURN THE FOLLOWING TWO ITEMS
1. VALUE
2. BEST_MOVE
    
THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    
"""
def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
	terminal = game_status.is_terminal()
	if (depth==0) or (terminal):
		scores = turn_multiplier * game_status.get_negamax_scores(terminal)
		return (scores, None)

	moves: list = game_status.get_moves()

	value = alpha
	best_move = None
	for move in moves:
		newGameStatus = game_status.get_new_state(move)
		negaMaxReturn, next_best_move = negamax(newGameStatus, depth - 1, -turn_multiplier, -beta, -alpha)

		if -negaMaxReturn > value: # if negamax returns a greater value, set it as the new value
			value = -negaMaxReturn
			best_move = move
		alpha = max(alpha, value) # if the value is greater than alpha, the alpha becomes equal to the value
		if alpha >= beta:
			break # prune the branch that will never be considered

	return value, best_move

boardState = [[-1,-1, 1,-1], 
			  [ 1,-1,-1,-1],
			  [ 1,-1, 1,-1],
			  [ 1, 1, 1, 1]]

gameStatus = GameStatus(boardState, False)
gameStatus.oldScores = gameStatus.get_scores(True)
print("Score:" + str(gameStatus.oldScores))

value , move = minimax(gameStatus, 2, False)
print("Value:" + str(value))
print("Best Move:" + str(move))

value , move = minimax(gameStatus, 3, False)
print("Value:" + str(value))
print("Best Move:" + str(move))

value , move = minimax(gameStatus, 4, False)
print("Value:" + str(value))
print("Best Move:" + str(move))

value , move = minimax(gameStatus, 5, False)
print("Value:" + str(value))
print("Best Move:" + str(move))

value , move = minimax(gameStatus, 6, False)
print("Value:" + str(value))
print("Best Move:" + str(move))