import random
import gym_tictactoe.envs.tictactoe_env as ttt
import copy
import itertools
import numpy as np

class QLearningAgent:

	def __init__(self,player_symbol,alpha=0.9,gamma=0.95,q_init=0.6):
		self.player_symbol=player_symbol
		self.alpha=alpha # Learning rate
		self.gamma=gamma # Discounting factor
		self.q_init_val = q_init
		self.move_history = []
		self.q_table={}
		self.moves={0:[0,0],1:[0,1],2:[0,2],3:[1,0],4:[1,1],5:[1,2],6:[2,0],7:[2,1],8:[2,2]}

	def _choose_random_action(self,board_state):
		legal_moves=self.lookForLegalMoves(board_state)
		action=random.choice(legal_moves)
		return(action)

	def _is_legal_move(self,board_state,move):
		''' Returns a list of legal moves for a given board state.'''
		if(board_state[move[0]][move[1]]==' '):					
			return(True)
		else:
			return(False)	

	def _encrypt_board_state(self,board_state):
		bs=list(itertools.chain(*board_state))
		board_hash_val=''.join(bs)
		return(board_hash_val)

	def _decrypt_board_hash_val(self,board_hash_val):
		bs=list(board_hash_val)
		return(bs)
			
	def _get_q_vals(self,board_state):
		board_hash_val=self._encrypt_board_state(board_state)
		if board_hash_val in self.q_table:
			q_vals=self.q_table[board_hash_val]
		else:
			q_vals=np.full(9,self.q_init_val)
			self.q_table[board_hash_val]=q_vals
		return(q_vals)		

	def _update_q_table(self,game_history,action_history,rewards):			
		move_history=[self._encrypt_board_state(i) for i in game_history]
		action_history=[list(self.moves.keys())[list(self.moves.values()).index(i)] for i in action_history]
		move_history.reverse()
		action_history.reverse()
		rewards.reverse()
		next_max=-1.0
		for move in range(len(move_history)):
			q_vals=self._get_q_vals(move_history[move])
			if(next_max<0):
				q_vals[action_history[move]]=rewards[move]
			else:
				q_vals[action_history[move]]=q_vals[action_history[move]]*((
					(1-self.alpha)*q_vals[action_history[move]])+(
					self.alpha*(rewards[move]+self.gamma*next_max)))
			self.q_table[move_history[move]]=q_vals
			next_max=max(q_vals)
			
	def choose_action(self,board_state):
		board_hash_val=self._encrypt_board_state(board_state)
		q_vals=self._get_q_vals(board_hash_val)
		while True:
			m=np.argmax(q_vals)
			next_move=self.moves[m]
			if(self._is_legal_move(board_state,next_move)):
				action=[next_move[0],next_move[1]]
				return(action)
			else:
				q_vals[m]=-1

