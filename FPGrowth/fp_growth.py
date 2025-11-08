"""
FP-growth
 Input: FP-tree constructed based on Algorithm 1,using DB and a minimum support threshold s.基于算法1构建的FP树，使用DB和最小支持度s
 Output: The complete set of frequent patterns. 所有频繁模式
"""
from itertools import combinations
from .fp_tree import FPTree

class FPGrowth:
    def __init__(self,min_support):
        self.min_support = min_support
        self.frequent_items = {}

    # 数据挖掘入口函数
    def mine(self,transactions):
        a = set()
        tree = FPTree(transactions,self.min_support)
        self.fp_growth(tree,a)
        return self.frequent_items

    # FP-Growth递归算法
    def fp_growth(self,tree,a):
        """
        (1) if Tree包含单路径P:
        (2)     for P中节点的每个组合β:
        (3)         生成模式 β∪α，支持度=β中最小支持度
        (4) else:
        (5)     for header_table中的每个项ai（从底部开始）:
        (6)         生成模式 β = {ai}∪α，支持度=ai.support
        (7)         构建ai的条件模式基
        (8)         构建ai的条件FP-Tree
        (9)         if 条件Tree非空:
        (10)            递归: fp_growth(条件Tree, β)
        :param tree: FPTree
        :param a: 当前后缀模式（set）
        :return:
        """
        # 单路径
        if tree.is_single_path():
            items = tree.get_single_path_items()
            self.mine_single_path(items,a)
        # 多路径
        else:
            items = sorted(tree.header_table.items(),key=lambda x:x[1][0])
            # for header_table中的每个项ai（从底部开始）:
            for item,(count,node) in items:
                # 生成模式 β = {ai}∪α，支持度=ai.support
                b = a | {item}
                self.frequent_items[frozenset(b)] = count
                # 构建ai的条件模式基
                previous_paths = tree.get_previous_path(item)
                # 构建ai的条件FP-Tree
                new_tree = self.build_conditional_tree(previous_paths,self.min_support)
                #if 条件Tree非空:
                if new_tree is not None:
                    # 递归: fp_growth(条件Tree, β)
                    self.fp_growth(new_tree,b)

    """
    处理单路径情况:
    for P中节点的每个组合β:
    生成模式 β∪α，支持度=β中最小支持度
    """
    def mine_single_path(self,items,a):
        for i in range(1,len(items)+1):
            for subset in combinations(items,i):
                frequent_set = set([item for item, _ in subset]) | a
                support = min([count for _, count in subset])
                self.frequent_items[frozenset(frequent_set)] = support

    # 根据条件模式基构建条件FP - Tree
    def build_conditional_tree(self,previous_paths,min_support):
        transactions = []
        for path, count in previous_paths:
            for i in range (count):
                transactions.append(path)

        new_tree = FPTree(transactions,min_support)

        return new_tree