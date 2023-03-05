from parse_hand import parse_hand
from utils import *


class Solution:
    def __init__(self, player_hand, opponent_hand):
        self.player = parse_hand(player_hand)
        self.opponent = parse_hand(opponent_hand)
        self.states = {}        
    
    def get_available_actions(self, player, opponent):
        player_actions = [('PASS', )] + player.get_actions()
        available_actions = [player_action for player_action in player_actions if self.is_certainly_win(player, opponent, player_action)]
        self.states[(encode_hand(player.hand), encode_hand(opponent.hand))] = available_actions

    def is_certainly_win(self, player, opponent, player_action):
        player_left_hand = player.get_left(player_action)
        if sum(player_left_hand) == 0:
            return True
        opponent_actions = opponent.get_actions(player_action)
        for opponent_action in opponent_actions:
            if not self._is_certainly_win(player_left_hand, opponent_action, opponent):
                return False
        return True
    

    def _is_certainly_win(self, player_hand, opponent_action, opponent):
        opponent_left_hand = opponent.get_left(opponent_action)
        if sum(opponent_left_hand) == 0:
            return False
        encode_states = (encode_hand(player_hand), encode_hand(opponent_left_hand))
        if encode_states not in self.states.keys():
            self.get_available_actions(parse_hand(player_hand), parse_hand(opponent_left_hand))
        
        available_actions = self.states[encode_states]
        return any(action_cmp(action, opponent_action) for action in available_actions)

    def run(self):
        print("caculating...   ")
        self.get_available_actions(self.player, self.opponent)
        self.show()
                    
    # 通过与玩家交互 反向输出一条获胜路径
    def show(self):
        player = self.player
        opponent = self.opponent
        cur_state = self.states[(encode_hand(player.hand), encode_hand(opponent.hand))]
        
        last_action = ("PASS", )
        while True:
            print(f"\nplayer hand : {hand2card(player.hand)}")
            print(f"opponent hand : {hand2card(opponent.hand)}\n")
            
            print("can win action : ")
            available_actions = [action for action in cur_state if action_cmp(action, last_action)]
            for i, action in enumerate(available_actions):
                print("    ({0}) : {1};".format(i+1, action2card(action)))
                    
            x = input("input your action id : ")
            player_action = available_actions[int(x)-1]
            player_left_hand = player.get_left(player_action)
            
            print(f"\nplayer hand : {hand2card(player_left_hand)}")
            print(f"opponent hand : {hand2card(opponent.hand)}\n")

            if sum(player_left_hand) == 0:
                print("YOU WIN")
                break
            
            opponent_actions = opponent.get_actions(player_action)
            print("opponent action : ")
            for i, action in enumerate(opponent_actions):
                print("    ({0}) : {1};".format(i+1, action2card(action)))
            
            x = input("input opponent action id : ")

            opponent_action = opponent_actions[int(x)-1]
            opponent_left_hand = opponent.get_left(opponent_action)

            player = parse_hand(player_left_hand)
            opponent = parse_hand(opponent_left_hand)

            cur_state = self.states[(encode_hand(player_left_hand), encode_hand(opponent_left_hand))]
            
            last_action = opponent_action


if __name__ == "__main__":
    
    shp = "aqqj9988653"
    sho = "2kqjj095433"

    s = Solution(card2hand(shp), card2hand(sho))
    s.run()