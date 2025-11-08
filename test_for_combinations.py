from itertools import combinations
dic1 = {'f':4, 'c': 4, 'a': 3, 'm': 3, 'p': 3, 'b': 3}
dic2 = [('f', 4), ('c', 4), ('a', 3), ('m', 3), ('p', 3), ('b', 3)]
dic3 = combinations(dic1,2) # 当combinations作用于一个字典时，它默认是对字典的键(keys)进行组合
dic4 = combinations(dic2,2) # combinations会对列表中的元素进行组合
print(f"对于字典{list(dic3)}")
print(f"对于数列{list(dic4)}")

# frequent_set = set([item for item, _ in dic4])
# print(frequent_set)
i = 2
for subset in combinations(dic2, i):
        pattern = set([item for item, _ in subset])
        print(subset,end=": ")
        print(pattern)