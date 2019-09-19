import random
import gym_tictactoe.envs.tictactoe_env as ttt
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



def play(max_episodes=300):
	episode=0
	player1_symbol,player2_symbol='X','O'
	env=ttt.TicTacToeEnv(player1_symbol,player2_symbol)
	player1,player2=RandomAgent(player1_symbol),RandomAgent(player2_symbol)

	while(episode<max_episodes):
		print("Episode:"+str(episode))
		current_player_symbol=player1_symbol
		board_state,current_player_symbol=env.reset(current_player_symbol)
		print(board_state)
		game_over=False
		while(not game_over):
			action=player1.choose_action(board_state)
			print(action)
			state,reward,game_over,info=env.step(action)
			board_state,current_player_symbol=state
			env.render()
			print(reward)
		episode=episode+1
	env.close()	
			
play()
	