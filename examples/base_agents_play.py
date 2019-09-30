import itertools
import gym_tictactoe.envs.tictactoe_env as ttt
from agents.base_agents import RandomAgent,HumanAgent

def play(max_episodes=2):
	episode=0
	player1_symbol,player2_symbol='X','O'
	env=ttt.TicTacToeEnv(player1_symbol,player2_symbol)
	player1=RandomAgent(player1_symbol)
	player2=RandomAgent(player2_symbol)
	#player2=HumanAgent(player2_symbol)
	
	while(episode<max_episodes):
		print("Episode:"+str(episode))
		board_state=env.reset()
		game_over=False
		game_history=[]
		if(episode%2==0):
			current_player_symbol=player1_symbol
			init_player_symbol=player1_symbol
		else:
			current_player_symbol=player2_symbol
			init_player_symbol=player2_symbol
			
		while(not game_over):
			if(current_player_symbol==player1_symbol):
				action=player1.choose_action(board_state)
			else:
				action=player2.choose_action(board_state)
			board_state,reward,game_over,info=env.step(action,init_player_symbol,current_player_symbol)
			current_player_symbol= player2_symbol if current_player_symbol==player1_symbol else player1_symbol
			game_history.append(list(itertools.chain(*board_state)))
			env.render()
			print(reward)
		episode=episode+1
	env.close()	
			
play()
