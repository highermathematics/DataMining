# Apriori算法：
from itertools import combinations
from collections import OrderedDict


# 加载数据库
def load_data(file_path):
    transactions = []
    with open(file_path,'r') as f:
        for line in f:
            items = line.strip().split()
            transaction = set(int(item) for item in items)
            transactions.append(transaction)
    return transactions

# 获取频繁1-项集
def get_L1(transactions,min_support):
    L1 = set()
    L1_count = OrderedDict()
    C1 = {}
    # 获取C1
    for transaction in transactions:
        for item in transaction:
            C1[item] = C1.get(item,0)+1

    # print(f"C1:{C1}")

    # 获取L1
    for item,count in C1.items():
        if count >= min_support:
            L1.add(frozenset([item]))
            L1_count[item]=count

    ordered_L1 = sorted(L1, key=lambda x: sorted(list(x)))
    # print(f"L1:{L1_count}")

    return ordered_L1

# 连接: 用 L(k)自连接得到C(k+1)
def link(L,k):
    C_next = set()

    # 将L(k)转化为列表，方便后续操作
    L_list = [list(item) for item in L]
    L_list.sort()
    # print(L_list)

    # 自链接
    n = len(L_list)
    for i in range(n):
        for j in range(i+1,n):
            p = L_list[i]
            q = L_list[j]
            # print(f"p:{p}",end=',')
            # print(f"q:{q}")

            if p[:-1] == q[:-1]:
                new_candidate = frozenset(p+q)
                # print(f"new_candidate:{new_candidate}")
                C_next.add(new_candidate)
                # print(f"C_next:{C_next}")
    ordered_C_next = sorted(C_next, key=lambda x: sorted(list(x)))
    return ordered_C_next

# 修剪: 对于一个k-项集，如果它的一个k-1项集(它的子集)不是频繁的，那它本身也不可能是频繁的
# 获取项集所有的k-1项集
def get_subset(item):
    k = len(item)
    items = list(item)

    subsets = [frozenset(subset) for subset in combinations(items,k-1)]
    return subsets

# 剪枝
def cut(Ck,L_pre):
    C_next=set()

    for candidate in Ck:
        # 获取项集所有的k-1项集
        subsets = get_subset(candidate)

        # 检查是否所有子集都在Ck中
        is_In = True
        for subset in subsets:
            if subset not in L_pre:
                is_In = False

        # 如果都在就保留，不在就剪掉
        if is_In:
            C_next.add(candidate)
    ordered_C_next = sorted(C_next, key=lambda x: sorted(list(x)))
    return ordered_C_next

# 筛选频繁项集
def get_Lk(Ck,transactions,min_support):
    Lk=set()
    Lk_count = OrderedDict()
    for item in Ck:
        count = 0
        for transaction in transactions:
            if item.issubset(transaction):
                count += 1
        if count >= min_support:
            Lk.add(frozenset(item))
            Lk_count[item]=count

    ordered_Lk = sorted(Lk, key=lambda x: sorted(list(x)))
    # print(f"L2:{Lk_count}")
    return ordered_Lk

def apriori(transactions,min_support):
    print(f"交易总数: {len(transactions)}")
    print(f"最小支持度: {min_support}")

    # 存储所有频繁项集和支持度
    all_frequent_itemsets = []

    # all_support_count = []
    # 生成频繁1项集
    L1 = get_L1(transactions, min_support)
    all_frequent_itemsets.append(set(L1))
    #迭代生成L2,L3...
    k = 1
    Lk_pre = L1

    while Lk_pre:
        # 自链接
        Ck = link(Lk_pre,k)
        # 剪枝
        Ck_next = cut(Ck,Lk_pre)
        # 筛选频繁项集
        Lk = get_Lk(Ck_next,transactions, min_support)
        # 如果没有频繁项集了，终止
        if not Lk:
            break
        # 保存结果
        all_frequent_itemsets.append(set(Lk))
        # 准备下一轮迭代
        Lk_pre = Lk
        k += 1
    return all_frequent_itemsets

def print_results(all_frequent_itemsets):
    total_count = 0
    frequent_itemsets = []
    for i, Lk in enumerate(all_frequent_itemsets, 1):
        itemsets = []
        for itemset in sorted(Lk, key=lambda x: sorted(list(x))):
            itemsets.append(set(itemset))
            frequent_itemsets.append(set(itemset))
        print(f"频繁{i}项集（共 {len(Lk)} 个）:{itemsets}")
        total_count += len(Lk)

    print(f"共{total_count}个频繁项集")
    print(frequent_itemsets)

if __name__ == '__main__':
    # 加载数据
    transactions = load_data('data.dat')
    # 最小支持度
    min_support = 2

    all_frequent_itemsets = apriori(transactions, min_support)

    print_results(all_frequent_itemsets)
    # print(f"交易总数: {len(transactions)}")
    # print(f"交易: {transactions}")
    # ans = get_L1(transactions, min_support)
    # print(f"L1:{ans}")
    # ans2 = link(ans,k)
    # print(f"C2未剪枝：{ans2}")
    # ans3 = cut(ans2,ans)
    # print(f"C2剪枝后：{ans3}")
    # ans4 = get_Lk(ans3,transactions, min_support)
    # print(f"L2:{ans4}")
