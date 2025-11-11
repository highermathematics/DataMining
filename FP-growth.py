from FPGrowth import FPTree, FPGrowth, load_data, print_frequent_items

if __name__ == '__main__':
    # 加载数据
    transactions = load_data('retail.dat')
    print(f"交易总数: {len(transactions)}")
    min_support = 0.01
    if min_support < 1:
        min_support = len(transactions) * min_support

    print(f"最小支持度: {min_support}")

    fpg = FPGrowth(min_support)
    frequent_items = fpg.mine(transactions)

    print(f"共{len(frequent_items)}个频繁项集")
    print_frequent_items(frequent_items,'length')
    print(f"共{len(frequent_items)}个频繁项集")
