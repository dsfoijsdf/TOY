from parse_hand import parse_hand
from utils import *


class Solution:
    def __init__(self, player_hand, opponent_hand):
        self.player = parse_hand(player_hand)
        self.opponent = parse_hand(opponent_hand)
        self.player_hand_subsets = self.player.get_subsets()
        self.opponent_hand_subsets = self.opponent.get_subsets()

        self.states = {(encode_hand(ph), encode_hand(oh)): [] for ph in self.player_hand_subsets for oh in self.opponent_hand_subsets}
        
    def is_certainly_win(self, player_hand, opponent_action, opponent):
        opponent_left_hand = opponent.get_left(opponent_action)
        if sum(opponent_left_hand) == 0:
            return False
        available_actions = self.states[(encode_hand(player_hand), encode_hand(opponent_left_hand))]
        return any(action_cmp(action, opponent_action) for action in available_actions)

    def run(self):
        print("caculating...   ")
        self.get_ans()
        self.show()
        
    def get_ans(self):
        for player_hand in self.player_hand_subsets:
            player = parse_hand(player_hand)
            player_actions = [('PASS', )] + player.get_actions()
            
            for opponent_hand in self.opponent_hand_subsets:
                opponent = parse_hand(opponent_hand)
                
                cur_state = self.states[(encode_hand(player_hand), encode_hand(opponent_hand))]
                # player任意选择一个出牌动作
                for player_action in player_actions:
                    # player 手中剩下的牌
                    player_left_hand = player.get_left(player_action)
                    if sum(player_left_hand) == 0:
                        cur_state.append(player_action)
                        break
                    # 在player选择player_action的情况下，opppnent可选的出牌动作
                    opponent_actions = opponent.get_actions(player_action)
                    
                    certainly_win = [self.is_certainly_win(player_left_hand, opponent_action, opponent) for opponent_action in opponent_actions]
                    if all(certainly_win):
                        cur_state.append(player_action)
                    
                        
    
    # 反向输出一条获胜路径（通过与玩家交互）
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
                print("    ({0}) : {1};".format(i+1, action))
                    
            x = input("input your action id : ")
            player_action = available_actions[int(x)-1]
            player_left_hand = player.get_left(player_action)
            
            print(f"\nplayer hand : {hand2card(player_left_hand)}")
            print(f"opponent hand : {hand2card(opponent.hand)}\n")

            if sum(player_left_hand) == 0:
                print("YOU WIN")
                break
            
            opponent_actions = opponent.get_actions(player_action)
            print("opp action : ")
            for i, action in enumerate(opponent_actions):
                print("    ({0}) : {1};".format(i+1, action))
            
            x = input("input opponent action id : ")

            opponent_action = opponent_actions[int(x)-1]
            opponent_left_hand = opponent.get_left(opponent_action)

            player = parse_hand(player_left_hand)
            opponent = parse_hand(opponent_left_hand)

            cur_state = self.states[(encode_hand(player_left_hand), encode_hand(opponent_left_hand))]
            
            last_action = opponent_action


if __name__ == "__main__":
    
    shp = "2q999643"
    sho = "daaj43"

    s = Solution(card2hand(shp), card2hand(sho))
    s.get_ans()
    s.show()