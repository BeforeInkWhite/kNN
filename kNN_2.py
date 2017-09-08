# -*- coding: utf-8 -*-
"""
Created on Fri May 19 17:11:27 2017

@author: Administrator
"""
# 2.3手写识别系统
from numpy import *
import operator
import os
from imp import reload 

# 防止超出编码范围



import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

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

# 2.3.1
# 将图像转换成"向量returnVector"
def img2vector(filename):
    returnVector=zeros((1,1024))  #先定义向量的形式：1行1024列
    fr=open(filename)         #打开原始文件
    for i in range(32):       #原始文件第i行
        lineStr=fr.readline() #读取第i行
        for j in range(32):      #将原始第i行数据赋值给向量
            returnVector[0,32*i+j]=int(lineStr[j])
    return returnVector

# 2-6
# 手写识别系统测试代码
def handwritingClassTest():
    hwLabels=[] 
    trainingFileList = os.listdir('trainingDigits') #获取路径中的所有文件名，以列表形式返回
    m = len(trainingFileList)                       #m为文件数量
    trainingMat=zeros((m,1024))                     #初始化训练数组
    for i in range(m):
        fileNameStr=trainingFileList[i]          #获取第i个文件名
        fileStr=fileNameStr.split('.')[0]        
         #以“.”为分隔符进行文件名的分割，并用fileStr返回第0个元素
         #在本例中实际就是去掉后缀TXT，只保留文件名
        classNumstr=int(fileStr.split('_')[0])
         #以“_”为分隔符对变量fileStr进行分割，并用classNumstr返回第0个元素
         #在本例中实际就是获取实际对应的“数字”
        hwLabels.append(classNumstr)   #标签集添加对应标签
        trainingMat[i,:]=img2vector('trainingDigits/%s' % fileNameStr)
        #调用img2vector（filename）函数
        #('trainingDigits/%s' % fileNameStr)实际上就是文件的路径
        #例如:trainingDigits/0_0.txt
    testFileList=os.listdir('testDigits')  #获取测试集中的所有文件名
    errorCount=0.0                         #错误量初始化
    mTest=len(testFileList)                #获取测试集文件数量
    for i in range(mTest):
        fileNameStr=testFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumstr=int(fileStr.split('_')[0])
        vectorUnderTest=img2vector('testDigits/%s' % fileNameStr)
        classifierResult=classify0(vectorUnderTest,trainingMat,hwLabels,3)
        #调用classify0（）进行k近邻分类
        print "the classifier came back with:%d,the real answer is:%d" % (classifierResult,classNumstr)
        if(classifierResult != classNumstr):
            errorCount += 1.0
    print "\n the total number of error is: %d" % errorCount
    print "\n the total error rate is: %f" % (errorCount/float(mTest))

handwritingClassTest()








