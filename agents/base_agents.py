import random

import copy

class RandomAgent:

	def __init__(self,player_symbol):
		self.player_symbol=player_symbol

	def lookForLegalMoves(self,boardState):
		''' Returns a list of legal moves for a given board state.'''

		legalMoves = []
		for i in range(len(boardState[0])):
			for j in range(len(boardState[0])):
				if(boardState[i][j] == ' '):
					tempBoard = copy.deepcopy(boardState)
					tempBoard[i][j]=self.player_symbol
					legalMoves.append([i,j])					
		return(legalMoves)	
			
	def choose_action(self,board_state):
		legal_moves=self.lookForLegalMoves(board_state)
		action=random.choice(legal_moves)
		return(action)


class HumanAgent:
	def __init__(self,player_symbol):
		self.player_symbol=player_symbol

	def lookForLegalMoves(self,boardState):
		''' Returns a list of legal moves for a given board state.'''

		legalMoves = []
		for i in range(len(boardState[0])):
			for j in range(len(boardState[0])):
				if(boardState[i][j] == ' '):
					tempBoard = copy.deepcopy(boardState)
					tempBoard[i][j]=self.player_symbol
					legalMoves.append([i,j])					
		return(legalMoves)

	def choose_action(self,board_state):
		legal_moves=self.lookForLegalMoves(board_state)
		x=int(input("Enter x(0,2) board Coordinate:"))
		y=int(input("Enter y(0,2) board Coordinate:"))
		action=[x,y]
		legal_moves=self.lookForLegalMoves(board_state)
		if(action in legal_moves):
			return(action)		
		return(-1)	#indicates invalid move


