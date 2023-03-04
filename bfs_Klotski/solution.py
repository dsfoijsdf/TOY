from board import Board
import queue
import copy
import imageio
import os

REDIRECTION = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}


class Solution:
    def __init__(self, board: Board):
        self.board = board
        self.histories = {}

    def run(self):
        print("find solution ...")
        result = self.bfs()
        print(f"total steps is {self.histories[result.encode_board()]}")
        if result is None:
            print("NO SOLUTION")
            return
        print("generate the shortest path ...")
        self.back(result)
        print("generate final result ...")
        self.get_gif()

    def bfs(self):

        q = queue.Queue()
        q.put_nowait(self.board)
        # self.histories.add(board.encode_board())
        self.histories[self.board.encode_board()] = 0
        while not q.empty():
            cur_board = q.get_nowait()
            actions = cur_board.get_actions()
            for (pid, direction) in actions:
                new_board = copy.deepcopy(cur_board)
                new_board.move(pid, direction)
                if new_board.encode_board() in self.histories.keys():
                    continue
                self.histories[new_board.encode_board()] = self.histories[cur_board.encode_board()] + 1
                if new_board.ispass():
                    return new_board

                q.put_nowait(new_board)

    def back(self, board):
        steps = self.histories[board.encode_board()]
        
        for step in range(steps, -1, -1):
            board.show_board(step=step)
            actions = board.get_actions()
            for (pid, direction) in actions:
                board.move(pid, direction)
                if board.encode_board() in self.histories.keys() and self.histories[board.encode_board()] == steps - 1:
                    steps -= 1
                    break
                board.move(pid, REDIRECTION[direction])
    
    def get_gif(self, img_dir='./result/'):
        img_list = sorted(os.listdir(img_dir), key=lambda x : int(x.split('.')[0][5:]))
        images = [imageio.imread(img_dir + img_name) for img_name in img_list]
        imageio.mimwrite("result.gif", images, duration=0.5)
    
        

