import itertools
import gym_tictactoe.envs.tictactoe_env as ttt
from agents.base_agents import RandomAgent

def play(max_episodes=2):
	episode=0
	player1_symbol,player2_symbol='X','O'
	env=ttt.TicTacToeEnv(player1_symbol,player2_symbol)
	player1=RandomAgent(player1_symbol)
	player2=RandomAgent(player2_symbol)
	current_player_symbol=player1_symbol
	
	while(episode<max_episodes):
		print("Episode:"+str(episode))
		board_state,current_player_symbol=env.reset(current_player_symbol)
		game_over=False
		game_history=[]
		while(not game_over):
			if(current_player_symbol==player1_symbol):
				action=player1.choose_action(board_state)
			else:
				action=player2.choose_action(board_state)
			state,reward,game_over,info=env.step(action)
			board_state,current_player_symbol=state
			game_history.append(list(itertools.chain(*board_state)))
			env.render()
			print(reward)
		print(game_history)	
		episode=episode+1
	env.close()	
			
play()
