
import generator
import numpy

# 加载数据集
def load_data_set():
    """
    加载样本数据集（摘自“数据挖掘：概念与技术”，第3版）
    Returns：
        数据集：交易清单。 每笔交易包含几个项目。
    """
    # data_set = [['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],
    #         ['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],
    #         ['l1', 'l3'], ['l1', 'l2', 'l3', 'l5'], ['l1', 'l2', 'l3']]
    data_set = generator.load_data('TASKNEW2', 24)
    return data_set

# 创建 C1
def create_C1(data_set):
    """
    通过扫描数据集创建频繁的候选 1-itemset C1。
    Args：
        data_set：事务列表。 每笔交易包含几个项目。
    Returns：
        C1：包含所有频繁的候选 1-itemset 的集合
    """
    C1 = set()
    for t in data_set:
        for item in t:
            item_set = frozenset([item])
            C1.add(item_set)
    return C1

# 一个数据集的子集是非频繁的，则该数据集也是非频繁的
def is_apriori(Ck_item, Lksub1):
    """
    判断频繁的候选 k-itemset 是否满足 Apriori 属性。
    Args：
        Ck_item：Ck中的一个频繁候选 k-itemset ，其中包含所有频繁候选 k-itemset 。
        Lksub1：Lk-1，一个包含所有频繁候选 (k-1)-itemset 的集合。
    Returns：
        True：满足 Apriori 属性。
        False：不满足 Apriori 属性。
    """
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True

# 通过 Lk-1 创建 Ck
def create_Ck(Lksub1, k):
    """
    创建 Ck ，这是一个包含所有频繁出现的候选 k-itemset 的集合通过 Lk-1 自己的连接操作。
    Args：
         Lksub1：Lk-1，一个包含所有频繁候选（k-1）个项目集的集合。
         k：频繁项目集的项目编号。
    Returns：
         Ck：包含所有常见候选 k-itemset 的集合。
    """
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


def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):
    """
    通过从 Ck 执行删除策略来生成 Lk 。
    Args：
         data_set：事务列表。 每笔交易包含几个项目。
         Ck：包含所有常见候选 k-itemset 的集合。
         min_support：最低支持。
         support_data：字典。 关键是频繁项集，值是支持。
    Returns：
         Lk：包含所有频繁出现的 k-itemset 的集合。
    """
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


def generate_L(data_set, k, min_support):
    """
    生成所有频繁项集。
    Args：
         data_set：事务列表。 每笔交易包含几个项目。
         k：所有频繁项目集的最大项目数。
         min_support：最低支持。
    Returns：
         L：Lk 的列表。
         support_data：字典。 关键是频繁项集，值是支持。
    """
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


def generate_big_rules(L, support_data, min_conf):
    """
    从频繁的项目集生成大规则。
    Args：
         L：Lk 的列表。
         support_data：字典。 关键是频繁项集，值是支持。
         min_conf：最小置信度。
    Returns：
         big_rule_list：包含所有大规则的列表。 每个大规则都代表作为一个三元组。
    """
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


if __name__ == "__main__":
    """
    Test
    """
    data_set = load_data_set()
    L, support_data = generate_L(data_set, k=3, min_support=0.5)
    big_rules_list = generate_big_rules(L, support_data, min_conf=0.6)
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
