# coding:utf-8

import generator


# 加载数据集
def load_data_set():
    # data_set = generator.load_data('QUESDATA', 24)        # 单道题目分析
    data_set = generator.load_data('TASKDATA', 8)       # 专项分析
    return data_set


# 创建频繁候选集C1
def create_C1(data_set):
    C1 = set()
    for t in data_set:
        for item in t:
            item_set = frozenset([item])
            C1.add(item_set)
    return C1


# 一个数据集的子集是非频繁的，则该数据集也是非频繁的
def is_apriori(Ck_item, Lksub1):
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True


# 通过 Lk-1 创建 Ck
def create_Ck(Lksub1, k):
    Ck = set()
    len_Lksub1 = len(Lksub1)
    list_Lksub1 = list(Lksub1)
    for i in range(len_Lksub1):
        for j in range(i+1, len_Lksub1):
            l1 = list(list_Lksub1[i])
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k-2] == l2[0:k-2]:
                Ck_item = list_Lksub1[i] | list_Lksub1[j]
                # pruning
                if is_apriori(Ck_item, Lksub1):
                    Ck.add(Ck_item)
    return Ck


# 通过从 Ck 执行删除策略来生成 Lk
def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):
    Lk = set()
    item_count = {}
    for t in data_set:
        for item in Ck:
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    t_num = float(len(data_set))
    for item in item_count:
        if (item_count[item] / t_num) >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item] / t_num
    return Lk


# 生成所有频繁项集
def generate_L(data_set, k, min_support):
    support_data = {}
    C1 = create_C1(data_set)
    L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data)
    Lksub1 = L1.copy()
    L = []
    L.append(Lksub1)
    for i in range(2, k+1):
        Ci = create_Ck(Lksub1, i)
        Li = generate_Lk_by_Ck(data_set, Ci, min_support, support_data)
        Lksub1 = Li.copy()
        L.append(Lksub1)
    return L, support_data


# 从频繁项集生成强关联规则
def generate_big_rules(L, support_data, min_conf):
    big_rule_list = []
    sub_set_list = []
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = support_data[freq_set] / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_conf and big_rule not in big_rule_list:
                        # print (freq_set-sub_set, " => ", sub_set, "conf: ", conf)
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return big_rule_list


# 题目：0.5 0.7，专项：
if __name__ == "__main__":
    data_set = load_data_set()
    L, support_data = generate_L(data_set, k=3, min_support=0.2)
    big_rules_list = generate_big_rules(L, support_data, min_conf=0.7)
    for Lk in L:
        try:
            print("="*50)
            print("frequent " + str(len(list(Lk)[0])) + "-itemsets\t\tsupport")
            print("="*50)
            for freq_set in Lk:
                print(list(freq_set), support_data[freq_set])
        except:
            continue
    print("\nBig Rules")
    for item in big_rules_list:
        print(list(item[0]), "=>", list(item[1]), "conf: ", item[2])

    print("\n")
    print("=" * 50)
    fset = [list(freq_set), support_data]
    print(fset)
