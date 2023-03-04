from utils import *


class parse_hand:
    def __init__(self, hand):
        self.ACTIONS = ["SINGLE", 'DOUBLE', "THREE", "THREE ONE", "THREE TWO", "FOUR", "FOUR ONE", "FOUR TWO",
                        "AIR", "AIR ONE", "AIR TWO", "STRAIGHT", "DOUBLE STRAIGHT", "KING"]
        self.hand = hand
        self.N = len(hand)

    # 通过上家动作获得目前可行动作
    def get_actions(self, last=('PASS',)):
        actions = self._get_actions()
        ans = []
        for action in actions:
            if action_cmp(action, last):
                ans.append(action)
        return ans

    # 行动过action后，手中剩余的牌
    def get_left(self, action):
        card = self._action2card(action)
        left = [self.hand[i] - card[i] for i in range(16)]
        left = tuple(left)
        return left

    def get_subsets(self):
        subsets = []
        cur_hand = [0 for _ in range(self.N)]
        self._dfs(subsets, cur_hand, 0)
        # 手牌数量从小到大排序
        subsets = sorted(subsets, key=lambda i : sum(i))
        # 删除空集
        return subsets[1:]
    
    def _dfs(self, subsets, cur_hand, start):
        subsets.append(tuple(cur_hand))
        for i in range(start, self.N):
            for j in range(1, self.hand[i]+1):
                cur_hand[i] = j
                self._dfs(subsets, cur_hand, i+1)
            cur_hand[i] = 0
        
        



    def _get_actions(self):
        ans = []
        for card in range(1, 16):
            if self.hand[card] >= 1:
                ans.append(['SINGLE', card])
            if self.hand[card] >= 2:
                ans.append(['DOUBLE', card])
            if self.hand[card] >= 3:
                ans.append(['THREE', card])
                # 三带一
                for card_ in range(1, 16):
                    if card_ == card:
                        continue
                    if self.hand[card_] >= 1:
                        ans.append(["THREE ONE", card, card_])
                    if self.hand[card_] >= 2:
                        ans.append(["THREE TWO", card, card_])
            if self.hand[card] >= 4:
                # 炸弹
                ans.append(["FOUR", card])
                # 四带二
                for card_, card__ in [(i, j) for i in range(1, 16) for j in range(i+1, 16)]:
                    if card_ == card or card__ == card:
                        continue
                    if self.hand[card_] >= 1 and self.hand[card__] >= 1:
                        ans.append(["FOUR ONE", card, card_, card__])
                    if self.hand[card_] >= 2 and self.hand[card__] >= 2:
                        ans.append(["FOUR TWO", card, card_, card__])
            # 飞机
            if 3 <= card <= 13:
                next_card = 1 if card == 13 else card + 1
                if self.hand[card] >= 3 and self.hand[next_card] >= 3:
                    ans.append(["AIR", card, next_card])
                    for card_, card__ in [(i, j) for i in range(1, 16) for j in range(i + 1, 16)]:
                        if card_ == card or card__ == card or card_ == next_card or card__ == next_card:
                            continue
                        if self.hand[card_] >= 1 and self.hand[card__] >= 1:
                            ans.append(["AIR ONE", card, next_card, card_, card__])
                        if self.hand[card_] >= 2 and self.hand[card__] >= 2:
                            ans.append(["AIR TWO", card, next_card, card_, card__])

        # 顺子
        straights = [[k if k != 14 else 1 for k in range(i, j)] for i in range(3, 14) for j in range(i+5, 16)]
        for straight in straights:
            if 0 not in [self.hand[index] for index in straight]:
                ans.append(["STRAIGHT", straight[0], straight[-1]])
        # 连对
        double_straights = [[k if k != 14 else 1 for k in range(i, j)] for i in range(3, 14) for j in range(i+3, 16)]
        for straight in double_straights:
            target = [self.hand[index] for index in straight]
            if 0 not in target and 1 not in target:
                ans.append(["DOUBLE STRAIGHT", straight[0], straight[-1]])
        # 王炸
        if self.hand[14] == 1 and self.hand[15] == 1:
            ans.append(["KING"])

        ans = [tuple(i) for i in ans + [["PASS"]]]
        return ans

    def _action2card(self, action):
        if action[0] == "PASS":
            return tuple([0 for _ in range(16)])
        ans = [0 for _ in range(16)]
        if action[0] == 'SINGLE':
            ans[action[1]] += 1
        elif action[0] == 'DOUBLE':
            ans[action[1]] += 2
        elif action[0] == 'THREE':
            ans[action[1]] += 3
        elif action[0] == 'FOUR':
            ans[action[1]] += 4
        elif action[0] == 'THREE ONE':
            ans[action[1]] += 3
            ans[action[2]] += 1
        elif action[0] == 'THREE TWO':
            ans[action[1]] += 3
            ans[action[2]] += 2
        elif action[0] == 'FOUR ONE':
            ans[action[1]] += 4
            ans[action[2]] += 1
            ans[action[3]] += 1
        elif action[0] == 'FOUR TWO':
            ans[action[1]] += 4
            ans[action[2]] += 2
            ans[action[3]] += 2
        elif action[0] == 'AIR':
            ans[action[1]] += 3
            ans[action[2]] += 3
        elif action[0] == 'AIR ONE':
            ans[action[1]] += 3
            ans[action[2]] += 3
            ans[action[3]] += 1
            ans[action[4]] += 1
        elif action[0] == 'AIR TWO':
            ans[action[1]] += 3
            ans[action[2]] += 3
            ans[action[3]] += 2
            ans[action[4]] += 2
        elif action[0] == 'STRAIGHT':
            end = -1
            if action[2] == 1:
                end = 14
                ans[1] += 1
            else:
                end = action[2] + 1
            for i in range(action[1], end):
                ans[i] += 1
        elif action[0] == 'DOUBLE STRAIGHT':
            end = -1
            if action[2] == 1:
                end = 14
                ans[1] += 1
            else:
                end = action[2] + 1
            for i in range(action[1], end):
                ans[i] += 2
        elif action[0] == "KING":
            ans[14] += 1
            ans[15] += 1
        return tuple(ans)

