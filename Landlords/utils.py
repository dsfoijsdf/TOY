import numpy as np


def card_cmp(card1, card2):
    """
    扑克牌中的大小优先级
    card1的位置的牌是否大于card2的位置的牌
    """
    cards = [0, 14, 15, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17]
    return cards[card1] > cards[card2]


def action_cmp(action1, action2):
    '''
    扑克牌出牌规则
    如果上家的动作是action2,该玩家能否出动作action1
    '''
    if action1[0] == 'PASS' and action2[0] == 'PASS':
        return False
    if action1[0] == "PASS" or action2[0] == 'PASS':
        return True
    if action1[0] == "KING":
        return True
    if action2[0] == "KING":
        return False
    if action1[0] == 'FOUR' and (action2[0] != 'FOUR' or card_cmp(action1[1], action2[1])):
        return True
    if action1[0] == action2[0]:
        if action1[0] != "STRAIGHT" and action1[0] != "DOUBLE STRAIGHT":
            return card_cmp(action1[1], action2[1])
        else:
            return card_cmp(action1[1], action2[1]) and action1[2] - action1[1] == action2[2] - action2[1]
    return False


def encode_hand(hand):
    # 将16个数字转成 16个3位的二进制字符串
    line = [format(num, "b").zfill(3) for num in hand]
    # 将字符串拼在一起转化成一个数字
    return int("0b" + "".join(line), 2)


def card2hand(cards="2qq999643"):
    hand = [0 for i in range(16)]
    c2i = {c : i for i, c in enumerate(" a234567890jqkxd")}
    for c in cards:
       hand[c2i[c]] += 1
    return hand 


def hand2card(hand=[0, 0, 1, 1, 1, 0, 1, 0, 0, 3, 0, 0, 2, 0, 0, 0]):
    cards = [0, 14, 15, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17]
    names = " a234567890jqkxd"
    order = np.argsort(np.array(cards))[::-1]
    card = ""
    for idx in order:
        card += hand[idx] * names[idx]
    return card


def action2hand(action):
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


def action2card(action):
    if action[0] == "PASS":
        return action
    return hand2card(action2hand(action))

if __name__ == "__main__":
    print(card2hand())
    print(hand2card())
