# coding:utf-8

from math import log
import operator
import treePlotter
import generator


def read_dataset():
    """
    学习时长：A0 - A9 共十个等级；
    学习次数：B0 - B9 共十个等级；
    期末成绩：G0 - G9 共十个等级；
    """
    # labels=['学习时长', '学习次数', '与相关用户的学习时长', '与相关用户的期末成绩', '期末成绩']
    labels = ['t1', 't2', 't3', 't4', 't12', 't14', 't15', 't16', 't18', 't19', 't20', 't21', 't24', 't25', 't26', 't27', 't28', 't56', 't57', 't59', 't60', '机考成绩']
    dataset = generator.load_data('TASKNEW2', 24)
    return dataset, labels


def read_testset():
    """
    学习时长：A0 - A9 共十个等级；
    学习次数：B0 - B9 共十个等级；
    期末成绩：G0 - G9 共十个等级；
    """
    testset = generator.load_data('TASKNEW2_TEST', 23)
    return testset


# 计算信息熵
def jisuanEnt(dataset):
    numEntries = len(dataset)
    labelCounts = {}
    # 给所有可能分类创建字典
    for featVec in dataset:
        currentlabel = featVec[-1]
        if currentlabel not in labelCounts.keys():
            labelCounts[currentlabel] = 0
        labelCounts[currentlabel] += 1
    Ent = 0.0
    for key in labelCounts:
        p = float(labelCounts[key])/numEntries
        Ent = Ent-p*log(p,2)     # 以2为底求对数
    return Ent


# 划分数据集
def splitdataset(dataset, axis, value):
    retdataset = []     # 创建返回的数据集列表
    for featVec in dataset:     # 抽取符合划分特征的值
        if featVec[axis] == value:
            reducedfeatVec = featVec[:axis]     # 去掉axis特征
            reducedfeatVec.extend(featVec[axis+1:])     # 将符合条件的特征添加到返回的数据集列表
            retdataset.append(reducedfeatVec)
    return retdataset


'''
选择最好的数据集划分方式
ID3算法:以信息增益为准则选择划分属性
C4.5算法：使用“增益率”来选择划分属性
'''


def C45_chooseBestFeatureToSplit(dataset):
    numFeatures = len(dataset[0])-1
    baseEnt = jisuanEnt(dataset)
    bestInfoGain_ratio = 0.0
    bestFeature = -1
    for i in range(numFeatures):    # 遍历所有特征
        featList = [example[i]for example in dataset]  
        uniqueVals = set(featList)      # 将特征列表创建成为set集合，元素不可重复。创建唯一的分类标签列表
        newEnt = 0.0
        IV = 0.0
        for value in uniqueVals:     # 计算每种划分方式的信息熵
            subdataset = splitdataset(dataset, i, value)
            p = len(subdataset)/float(len(dataset))
            newEnt += p*jisuanEnt(subdataset)
            IV = IV-p*log(p, 2)
        infoGain = baseEnt-newEnt
        if (IV == 0):   # fix the overflow bug
            continue
        infoGain_ratio = infoGain / IV                   # 这个feature的infoGain_ratio
        print(u"C4.5中第%d个特征的信息增益率为：%.3f" % (i, infoGain_ratio))
        if (infoGain_ratio > bestInfoGain_ratio):          # 选择最大的gain ratio
            bestInfoGain_ratio = infoGain_ratio
            bestFeature = i                              # 选择最大的gain ratio对应的feature
    return bestFeature


def majorityCnt(classList):
    '''
    数据集已经处理了所有属性，但是类标签依然不是唯一的，
    此时我们需要决定如何定义该叶子节点，在这种情况下，我们通常会采用多数表决的方法决定该叶子节点的分类
    '''
    classCont = {}
    for vote in classList:
        if vote not in classCont.keys():
            classCont[vote] = 0
        classCont[vote] += 1
    sortedClassCont = sorted(classCont.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCont[0][0]


def C45_createTree(dataset, labels):
    classList = [example[-1] for example in dataset]
    if classList.count(classList[0]) == len(classList):
        # 类别完全相同，停止划分
        return classList[0]
    if len(dataset[0]) == 1:
        # 遍历完所有特征时返回出现次数最多的
        return majorityCnt(classList)
    bestFeat = C45_chooseBestFeatureToSplit(dataset)
    bestFeatLabel = labels[bestFeat]
    print(u"此时最优索引为：" + bestFeatLabel)
    C45Tree = {bestFeatLabel: {}}
    del(labels[bestFeat])
    # 得到列表包括节点所有的属性值
    featValues = [example[bestFeat] for example in dataset]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        C45Tree[bestFeatLabel][value] = C45_createTree(splitdataset(dataset, bestFeat, value), subLabels)
    return C45Tree


def classify(inputTree, featLabels, testVec):
    """
    输入：决策树，分类标签，测试数据
    输出：决策结果
    描述：跑决策树
    """
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    classLabel = '0'
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel


def classifytest(inputTree, featLabels, testDataSet):
    """
    输入：决策树，分类标签，测试数据集
    输出：决策结果
    描述：跑决策树
    """
    classLabelAll = []
    for testVec in testDataSet:
        classLabelAll.append(classify(inputTree, featLabels, testVec))
    return classLabelAll


if __name__ == '__main__':
    dataset, labels = read_dataset()
    print('dataset', dataset)
    print("---------------------------------------------")
    print(u"数据集长度", len(dataset))
    print(u"信息熵:", jisuanEnt(dataset))
    print("---------------------------------------------")

    print(u"以下为首次寻找最优索引:\n")
    print(u"C4.5算法的最优特征索引为:"+str(C45_chooseBestFeatureToSplit(dataset)))
    print(u"\n首次寻找最优索引结束！")
    print("---------------------------------------------")

    print(u"下面开始创建相应的决策树-------")
    # C4.5决策树
    labels_tmp = labels[:] # 拷贝，createTree会改变labels
    C45desicionTree = C45_createTree(dataset, labels_tmp)
    # print('C45desicionTree:\n', C45desicionTree)
    # treePlotter.C45_Tree(C45desicionTree)
    testSet = read_testset()
    result = classifytest(C45desicionTree, labels, testSet)
    # for i in range(0, len(result)):
    #     if result[i] == '0':
    #         result[i] = 'G0'
    # print('C4.5_TestSet_classifyResult:\n', classifytest(C45desicionTree, labels, testSet))
    # 计算准确率
    real_result = generator.load_data('TASKNEW2_TEST', 24)
    sum = 0
    print("实际值\t预测值")
    for i in range(0, len(real_result)):
        print(real_result[i][21]+'\t\t'+result[i])
        # print(result[i])
        if result[i] == real_result[i][21]:
            sum = sum + 1
    # print("下面为测试数据集的预测值：")
    print("\n与实际比较的预测准确率：")
    print(sum / len(result))
