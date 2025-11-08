# 工具函数，提供从文件加载事务数据、格式化打印频繁项集

# 从文件加载事务数据
def load_data(file_path):
    transactions = []
    with open(file_path,'r') as f:
        for line in f:
            items = line.strip().split()
            transaction = set(int(item) for item in items)
            transactions.append(transaction)
    return transactions

# 格式化打印频繁项集
def print_frequent_items(items,sort_by='support',top=None):
    """
    格式化打印频繁项集
    :param items: {frozenset: support}
    :param sort_by:'support'（按支持度）或 'length'（按长度）
    :param top:只显示前N个（None表示全部）
    :return:None
    """
    # 转换为列表
    l = [(set(i), s) for i, s in items.items()]

    # 排序
    if sort_by == 'support':
        l.sort(key=lambda x:x[1],reverse=True)
    elif sort_by == 'length':
        l.sort(key=lambda x:len(x[0]))

    # 限制显示数量
    if top:
        l = l[:top]

    # 打印
    for i,s in l:
        ans =  '{' + ', '.join(str(item) for item in sorted(i)) + '}'
        print(f"{ans:<40} {s:>10}")
