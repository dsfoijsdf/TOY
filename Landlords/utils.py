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

if __name__ == "__main__":
    print(card2hand())
    print(hand2card())
