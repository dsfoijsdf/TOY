class Player:
    def __init__(self, player):
        self.player = player
        self.N = 16
        self.subsets = []
        self.subset2index = {}
        self._get_subset()

    def get_index(self, subset):
        return self.subset2index[subset]

    # 递归生成子集
    def _get_subset(self):
        cur = [0 for _ in range(self.N)]
        self._dfs(cur, 0)
        self.subsets = [tuple(subset) for subset in self.subsets]
        # 手牌数量从小到大排序
        self.subsets = sorted(self.subsets, key=lambda i: sum(i))
        # 删除空集
        self.subsets = self.subsets[1:]
        for i, subset in enumerate(self.subsets):
            self.subset2index[subset] = i

    def _dfs(self, cur, start):
        self.subsets.append(cur.copy())
        for i in range(start, self.N):
            for j in range(1, self.player[i] + 1):
                cur[i] = j
                self._dfs(cur, i + 1)
            cur[i] = 0

h1 = (0, 1, 0, 0, 4, 2, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0)
p1 = Player(h1)

ss = p1.subsets
print(len(ss))
print(len(set(ss)))