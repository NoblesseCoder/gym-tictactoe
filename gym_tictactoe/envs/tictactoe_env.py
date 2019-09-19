import gym
import itertools
import copy

INIT_BOARD_STATE=[[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
PLAYER1_WIN_REWARD = 1 
PLAYER2_WIN_REWARD = -1
DRAW_REWARD = 0
NO_REWARD = 0

class TicTacToeEnv(gym.Env):
	'''Tic-Tac-Toe board environment for openai gym '''
	metadata={'render.modes':['human']}

	def __init__(self,player1_symbol,player2_symbol):
		self.board_state=INIT_BOARD_STATE
		self.game_over=False
		self.player1_symbol=player1_symbol
		self.player2_symbol=player2_symbol

	def _board_state_print(self):
		''' Displays board in proper format'''
		
		print('\n')
		print(self.board_state[0][0] + '|' + self.board_state[0][1] + '|' + self.board_state[0][2])
		print("-----")
		print(self.board_state[1][0] + '|' + self.board_state[1][1] + '|' + self.board_state[1][2])
		print("-----")
		print(self.board_state[2][0] + '|' + self.board_state[2][1] + '|' + self.board_state[2][2])
		print('\n')	

	def _get_obs(self):
		return(self.board_state,self.current_player_symbol)	

	def _next_player_symbol(self):
	    return self.player1_symbol if  self.current_player_symbol== self.player2_symbol else self.player2_symbol
	
	def _check_game_status(self):
		if((self.board_state[0][0] == self.board_state[0][1] == self.board_state[0][2] == self.player1_symbol)  or 
			(self.board_state[1][0] == self.board_state[1][1] == self.board_state[1][2] == self.player1_symbol) or
			(self.board_state[2][0] == self.board_state[2][1] == self.board_state[2][2] == self.player1_symbol) or
			(self.board_state[0][0] == self.board_state[1][0] == self.board_state[2][0] == self.player1_symbol) or
			(self.board_state[0][1] == self.board_state[1][1] == self.board_state[2][1] == self.player1_symbol) or
			(self.board_state[0][2] == self.board_state[1][2] == self.board_state[2][2] == self.player1_symbol) or
			(self.board_state[0][0] == self.board_state[1][1] == self.board_state[2][2] == self.player1_symbol) or
			(self.board_state[0][2] == self.board_state[1][1] == self.board_state[2][0] == self.player1_symbol) ): 
				return(1)
		elif((self.board_state[0][0] == self.board_state[0][1] == self.board_state[0][2] == self.player2_symbol)  or 
			(self.board_state[1][0] == self.board_state[1][1] == self.board_state[1][2] == self.player2_symbol) or
			(self.board_state[2][0] == self.board_state[2][1] == self.board_state[2][2] == self.player2_symbol) or
			(self.board_state[0][0] == self.board_state[1][0] == self.board_state[2][0] == self.player2_symbol) or
			(self.board_state[0][1] == self.board_state[1][1] == self.board_state[2][1] == self.player2_symbol) or
			(self.board_state[0][2] == self.board_state[1][2] == self.board_state[2][2] == self.player2_symbol) or
			(self.board_state[0][0] == self.board_state[1][1] == self.board_state[2][2] == self.player2_symbol) or
			(self.board_state[0][2] == self.board_state[1][1] == self.board_state[2][0] == self.player2_symbol) ): 
				return(2)					
		elif(' ' in list(itertools.chain.from_iterable(self.board_state))):
			return(-1)
		else:
			return(0)	
					
	def step(self,action):
		'''Execute one time step within the environment'''
		if self.game_over:
			return(self._get_obs(),0,True,None)
		
		self.board_state[action[0]][action[1]]=self.current_player_symbol
		reward=NO_REWARD
		status=self._check_game_status()
		
		if(status>=0):
			self.game_over=True
			reward= PLAYER1_WIN_REWARD if status==1 else PLAYER2_WIN_REWARD if status==2 else DRAW_REWARD
		
		self.current_player_symbol=self._next_player_symbol()
		return(self._get_obs(),reward,self.game_over,None)	


	def reset(self,player_symbol):
		'''Reset the state of the environment to an initial state'''
		self.board_state=copy.deepcopy(INIT_BOARD_STATE)
		self.game_over=False
		self.current_player_symbol=player_symbol
		return(self._get_obs())

	def render(self):
		'''Render the environment to the screen'''
		self._board_state_print()			
