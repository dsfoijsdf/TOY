import numpy as np
from board import Board
from solution import Solution


# 初始状态游戏 ： 每个数字代表一个棋子，0代表空位
# 经典华容道关卡 ： 横刀立马
b = np.array([
    [2, 1, 1, 3,],
    [2, 1, 1, 3,],
    [4, 5, 5, 6,],
    [4, 7, 8, 6,],
    [0, 9, 10, 0],
])

board = Board(board=b)
s = Solution(board)
s.run()