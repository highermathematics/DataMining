"""
FP-tree:
 input: A transaction database DB and a minimum support threshold s.  数据库和最小支持度s
 Output: Its frequent pattern tree, FP-tree  频繁模式树，FP树
"""

# FP-tree节点
class TreeNode:
    def __init__(self,item,count,parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {} # {item:TreeNode}
        self.node_link = None # 指向下一个相同item的节点

    #增加节点计数
    def increase_count(self):
        self.count += 1

    #显示树的结构
    def show(self,gap=0):
        print('    '*gap+f"{self.item}:{self.count}")
        for child in self.children.values():
            child.show(gap+1)

# FP-tree
class FPTree:
    def __init__(self,transactions,min_support):
        self.min_support = min_support
        self.header_table = {} # {item:[count,Node]}

        # 获取频繁1项集
        self.get_header_table(transactions)
        # 降序排序头表
        self.frequent_items = {item:self.header_table[item][0] for item in
                               sorted(self.header_table,key=lambda x:self.header_table[x][0],reverse=True)}
        # 创建根节点
        self.root = TreeNode('null',0,None)
        # 创建树
        self.build_tree(transactions)


    # 获取频繁1项集
    def get_header_table(self,transactions):
        item_count = {} #{item:count}
        for transaction in transactions:
            for item in transaction:
                item_count[item] = item_count.get(item,0)+1

        for item,count in item_count.items():
            if count >= self.min_support:
                self.header_table[item] = [count, None]

    # 构建FP-tree
    def build_tree(self,transactions):
        for transaction in transactions:
            frequent_item = [item for item in self.frequent_items.keys() if item in transaction]

            if frequent_item:
                # print(frequent_item)
                self.insert_tree(frequent_item,self.root)

    #插入节点
    def insert_tree(self,items,node):
        # 获取当前事务的第一个数据
        item = items[0]
        # 插入树中：
        # 如果已存在，只更新节点的count
        if item in node.children:
            node.children[item].increase_count()
        # 如果不存在：新建节点插入
        else:
            new_node = TreeNode(item,1,node)
            node.children[item] = new_node
            self.update_header_table(item,new_node)
        # 如果当前事务中还剩超过1个元素，递归插入下一个数据
        if len(items) > 1:
            # print(items[1:])
            self.insert_tree(items[1:],node.children[item])

    # 更新header_table的node_link链表
    def update_header_table(self,item,node):
        if self.header_table[item][1] is None:
            self.header_table[item][1] = node
        else:
            idx = self.header_table[item][1]
            while idx.node_link is not None:
                idx=idx.node_link
            idx.node_link = node

    # 判断是否为单路径树
    def is_single_path(self):
        node = self.root
        while True:
            if len(node.children) > 1:
                return False
            elif len(node.children) == 0:
                return True
            else:
                node = list(node.children.values())[0]

    # 获取单路径上的所有项和支持度
    def get_single_path_items(self):
        items = []
        node = self.root
        while len(node.children) > 0:
            child = list(node.children.values())[0]
            items.append((child.item,child.count))
            node = child
        return items

    # 获取item的所有前缀路径
    def get_previous_path(self,item):
        paths = []
        node = self.header_table.get(item)[1]

        while node is not None:
            path = []
            count = node.count
            parent = node.parent

            while parent.parent is not None:
                path.append(parent.item)
                parent = parent.parent

            if path:
                paths.append((path[::-1],count))

            node = node.node_link

        return paths


