# -*- coding: utf-8 -*-

from numpy import *
import operator
import matplotlib

# 2-1
# k近邻核心算法
def classify0(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]               #获取dataSet第一维长度
    diffMat=tile(inX,(dataSetSize,1))-dataSet  #tile复制数组
    sqDiffMat=diffMat**2                       #连续两个*表示平方
    sqDistances=sqDiffMat.sum(axis=1)          #axis=0表示列求和；axis=1表示行求和。
    distances=sqDistances**0.5
    sortedDistIndicies=distances.argsort()     #argsort()升序，返回数组的索引即序号。
    classCount={}                              #建立空字典classCount
    for i in range(k):
        voteIlabel=labels[sortedDistIndicies[i]]                 #获取第i近的标签
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1    #建立类标签字典并计数
          #classCount[voteIlabel]=k，表示创建一个键voteIlabel；并且键voteIlabel的值为k。
          #classCount.get(voteIlabel,0)，查询是否有voteIlabel键，如果有则返回键值，如果没有则返回0                                                                                                            
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
          #对classCount{}进行排序，关键字为第一维，降序
    return sortedClassCount[0][0]

# 2-2
# 读取原始数据文件，创建数据集returnMat和标签向量classLabelVector
def file2matrix(filename):
    fr=open(filename)               #打开文件
    arrayOLines=fr.readlines()      #读取整个文件，并存储为一个只有一行的列表
    numberOfLines=len(arrayOLines)  #len读取列表、字符串、数组等的长度
    returnMat=zeros((numberOfLines,3)) #zeros（（a，b））创建a行b列的数组，b并初始化为0
    classLabelVector=[]                #创建空列表
    index=0
    for line in arrayOLines:
        line=line.strip()             #strip()用来删除回车、空格或指定字符
        listFromLine=line.split('\t') #split()通过指定分隔符对字符串进行切片
        returnMat[index,:]=listFromLine[0:3]          #为 returnMat[]赋值
        classLabelVector.append(int(listFromLine[-1]))#类别标签向量赋值
        index+=1
    return returnMat,classLabelVector

# 2-3
# 数据归一化处理得到归一化后的数据集normDataSet
def autoNorm(dataSet):
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    normDataSet=zeros(shape(dataSet))        #normDataSet初始化为与dataSet相同形状的矩阵
    m=dataSet.shape[0]                       #读取dataSet第一维的长度
    normDataSet=dataSet-tile(minVals,(m,1))  #tile复制数组
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals


#2-4
# 测试
'''def datingClassTest():
    hoRatio=0.10
    datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],4)
        print "the classifier came back with:%d,the real answer is:%d" % (classifierResult,datingLabels[i])
        if(classifierResult != datingLabels[i]):
            errorCount += 1.0
    print errorCount
    print numTestVecs
    print "the total error rate is:%f" % (errorCount/float(numTestVecs))
datingClassTest()
'''

# 2-5
# 调用上面各函数，实现约会网站预测功能
def classifyPerson():
    resultList=['not at all','in small doses','in large doses']
    percentTats=float(raw_input("percentage of time spent playing video games?"))
    ffMiles=float(raw_input("frquent flier miles earned per years?"))
    iceCream=float(raw_input("liters of ice cream consumed per years?"))
    datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResult=classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print "you will probably like this person:",resultList[classifierResult-1]

# 测试算法
classifyPerson()




































