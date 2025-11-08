from FPGrowth import FPTree, FPGrowth, load_data, print_frequent_items

transactions = [
        ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],   # TID 100
        ['a', 'b', 'c', 'f', 'l', 'm', 'o'],        # TID 200
        ['b', 'f', 'h', 'j', 'o'],                  # TID 300
        ['b', 'c', 'k', 's', 'p'],                  # TID 400
        ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']    # TID 500
    ]

min_support = 3

fptree = FPTree(transactions,min_support)
print(f"频繁1项集:{fptree.frequent_items}")

print("头表header_table:")
for item, (support, head_node) in fptree.header_table.items():
    print(f"项 {item} - 支持度: {support}:",end=' ')
    # 打印该 item 的 node_link 链表
    node_chain = []
    current_node = head_node
    while current_node:
        node_chain.append(f"{current_node.item}:{current_node.count}")
        current_node = current_node.node_link
    print(f"{' -> '.join(node_chain)}")

print("FP-tree前序遍历：")
fptree.root.show()

fpg = FPGrowth(min_support)
items = fpg.mine(transactions)

print(f"\n发现 {len(items)} 个频繁项集")
print_frequent_items(items,'length')