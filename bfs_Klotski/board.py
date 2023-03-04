import copy
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import colors


# PIECES_TYPE = {
#     "1x1": {"size": (1, 1), "value": 1}, 
#     "1x2": {"size": (1, 2), "value": 2},
#     "2x1": {"size": (2, 1), "value": 3}, 
#     "2x2": {"size": (2, 2), "value": 4}, 
# } 

PIECES_TYPE = {
    (1, 1): 1, 
    (1, 2): 2,
    (2, 1): 3, 
    (2, 2): 4, 
} 

DIRECTION = {'UP': (-1, 0), 'RIGHT': (0, 1), 'DOWN': (1, 0), 'LEFT': (0, -1)}
REDIRECTION = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}

class Piece:
    def __init__(self, piece_size, top_left_pos, piece_id: int):
        self.size = piece_size 
        self.id = piece_id
        self.pos = [[top_left_pos[0] + i, top_left_pos[1] + j] for i in range(self.size[0]) for j in range(self.size[1])]

    def __str__(self):
        return str(self.id)


class Board:
    def __init__(self, board, exit_pos=[(4,1), (4,2)], caocao=1):
        self.original_board = board

        self.board = self.original_board
        self.board_size = self.board.shape
        
        self.pieces = self.get_pieces()
        self.pos2pid = {}

        self.update_board()
        self.pid2color = None

        # define exit and 曹操
        self.exit_pos = exit_pos
        self.caocao = caocao

    def get_pieces(self):
        # check empty pos number is 2
        self.get_empties()
        mark = copy.deepcopy(self.original_board)
        
        # find all pieces
        pieces = [
            self._get_pieces(mark, (i,j)) 
            for i in range(self.board_size[0]) for j in range(self.board_size[1]) 
            if mark[i,j] != 0
        ]
        return {piece.id: piece for piece in pieces}


    def _get_pieces(self, mark, pos):
        # type list must be this order
        for piece_size in [(2, 2), (2, 1), (1, 2), (1, 1)]:
            val = mark[pos]
            ismatch = [
                pos[0]+i < self.board_size[0] and pos[1]+j < self.board_size[1] and mark[pos] == mark[pos[0]+i,pos[1]+j]
                for i in range(piece_size[0]) for j in range(piece_size[1])
            ]
            if all(ismatch):
                count = np.sum(mark == val)
                assert count == piece_size[0] * piece_size[1], "piece size not in [2x2, 2x1, 1x2, 1x1] or piece id is not unique"
                mark[mark == val] = 0
                return Piece(piece_size,  top_left_pos=pos, piece_id=val)
        
        # should not be go here
        return None


    def get_empties(self):
        empties = [(i, j) for i in range(self.board_size[0]) for j in range(self.board_size[1]) if self.board[i, j] == 0]
        assert len(empties) == 2, "empty pos number is not 2"
        return empties

    def update_board(self):
        self.board = np.zeros(self.board_size, dtype=int)
        self.pos2pid = {}

        for piece in self.pieces.values():
            for pos in piece.pos:
                pos = tuple(pos)
                self.board[pos] = PIECES_TYPE[piece.size]
                self.pos2pid[pos] = piece.id

    def show_board(self, mode="draw", save_dir="./result/", step=0):
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        
        if mode == "draw":
            self._draw_board(save_path = save_dir + f"step_{step}.jpg", step=step)




    def _draw_board(self, save_path=None, step=None):
        # first draw： assign a color to each piece
        if self.pid2color is None:
            color_list = list(colors.CSS4_COLORS.values())
            assert len(self.pieces) <= len(color_list), "too many pieces, setting color is not enough"
            # random.shuffle(color_list)
            self.pid2color = {name: color_list[i*3] for i, name, in enumerate(self.pieces.keys())}
        
        fig, ax = plt.subplots()
        ax.set_xlim(0, max(self.board_size))
        ax.set_ylim(0, max(self.board_size))
        for pid, piece in self.pieces.items():
            pos = piece.pos[0]
            trans_pos = (pos[1], self.board_size[0] - pos[0]- piece.size[0])
            rect = patches.Rectangle(trans_pos , piece.size[1], piece.size[0], color=self.pid2color[pid], label=pid)
            ax.text(trans_pos[0] + piece.size[1]/2, trans_pos[1] + piece.size[0]/2, s=str(pid))
            ax.add_patch(rect)
        
        # ax.xaxis.set_visible(False)
        # ax.yaxis.set_visible(False)
        ax.text(max(self.board_size)-0.5, max(self.board_size)-1, s=f"step : {step}")
        plt.axis('off')
        plt.savefig(save_path, dpi=300)
        plt.clf()
        plt.close()
        
    def encode_board(self):
        '''
        Each line of the board is encoded as an integer according the piece type 
        '''
        lines_encode = []
        for i in range(self.board_size[0]):
            line = [format(self.board[i,j], "b") if self.board[i,j] != self.caocao else "111" for j in range(self.board_size[1])]
            line = [num.zfill(3) for num in line]
            lines_encode.append(int("0b" + "".join(line), 2))
        return tuple(lines_encode)
    
    def move(self, pid, direction):
        piece = self.pieces[pid]
        for pos in piece.pos:
            pos[0] += DIRECTION[direction][0]
            pos[1] += DIRECTION[direction][1]
        self.update_board()
    
    def get_actions(self):
        empties = self.get_empties()
        actions = []

        # one move fill two empties

        # 两个空位上下相连
        if empties[0][1] == empties[1][1] and abs(empties[0][0] - empties[1][0]) == 1:
            # 空位左边是 2*1 or 2*2 的棋子，将其向右移动
            if empties[0][1] > 0 and self.pos2pid[(empties[0][0], empties[0][1]-1)] == self.pos2pid[(empties[1][0], empties[1][1]-1)]:
                actions.append((self.pos2pid[(empties[0][0], empties[0][1]-1)], "RIGHT"))
            # 空位右边是 2*1 or 2*2 的棋子，将其向左移动
            if empties[0][1] < self.board_size[1] - 1 and self.pos2pid[(empties[0][0], empties[0][1]+1)] == self.pos2pid[(empties[1][0], empties[1][1]+1)]:
                actions.append((self.pos2pid[(empties[0][0], empties[0][1]+1)], "LEFT"))
        # 两个空位左右相连
        elif empties[0][0] == empties[1][0] and abs(empties[0][1] - empties[1][1]) == 1:
            # 空位上边是 1*2 or 2*2 的棋子，将其向下移动
            if empties[0][0] > 0 and self.pos2pid[(empties[0][0]-1, empties[0][1])] == self.pos2pid[(empties[1][0]-1, empties[1][1])]:
                actions.append((self.pos2pid[(empties[0][0]-1, empties[0][1])], 'DOWN'))
            # 空位下边是 1*2 or 2*2 的棋子，将其向上移动
            if empties[0][0] < self.board_size[0] - 1 and self.pos2pid[(empties[0][0]+1, empties[0][1])] == self.pos2pid[(empties[1][0]+1, empties[1][1])]:
                actions.append((self.pos2pid[(empties[0][0]+1, empties[0][1])], 'UP'))
        
        # one move fill one empty
        for empty in empties:
            for dir in DIRECTION.values():
                x = empty[0] + dir[0]
                y = empty[1] + dir[1]
                if 0 <= x < self.board_size[0] and 0 <= y < self.board_size[1] and (x, y) in self.pos2pid.keys():
                    # up or down
                    if abs(dir[0]) == 1 and self.pieces[self.pos2pid[(x, y)]].size[1] == 1:
                        actions.append((self.pos2pid[(x, y)], "UP" if dir[0] == 1 else "DOWN"))
                    # left or right
                    if abs(dir[1]) == 1 and self.pieces[self.pos2pid[(x, y)]].size[0] == 1:
                        actions.append((self.pos2pid[(x, y)], "LEFT" if dir[1] == 1 else "RIGHT"))
        
        return actions
            
    def ispass(self):
        # return all([self.pos2pid[pos] == self.caocao for pos in self.exit_pos])
        return all([self.pos2pid.get(pos, -1) == self.caocao for pos in self.exit_pos])
        

if __name__ == "__main__":
    board = np.array([
        [1, 1, 2, 2],
        [1, 1, 3, 4],
        [0, 5, 6, 0],
        [7, 8, 9, 10],
        [7, 8, 9, 10],
    ], dtype=np.int32)
    test_board = Board(board)
    print(test_board.encode_board())
    print(test_board.get_actions())
    test_board.show_board()
