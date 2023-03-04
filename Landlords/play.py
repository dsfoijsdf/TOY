from solution import Solution
from utils import *

# d : 大王； x:小王  0：10
# player_card = "2q999643"
# opponent_card = "daaj43"

print("'x' means 大王; 'd' means 小王; '0' means 10")
print("You can use characters to represent the hand, for example '2q999643'")


player_card = input("please input the player hand : ")
opponent_card = input("please input the opponent hand : ")

s = Solution(card2hand(player_card), card2hand(opponent_card))
s.run()