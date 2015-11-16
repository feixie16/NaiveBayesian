#!/usr/bin/python 
# -*- coding: utf-8 -*- 
from numpy import *


#根据输入数据生成单词列表
def createWordList(dataSet):
	wordSet=set()
	for line in dataSet:
		wordSet=wordSet | set(line)
	
	return list(wordSet)

#把输入的单词列表转换为bool列表(词集模型)
def set_of_words(wordList,inputList):
	boolList=[0]*len(wordList)
	for word in inputList:
		if word in wordList:
			boolList[wordList.index(word)]=1
	
	return boolList

#把输入的单词列表转换为数字列表(词袋模型)
def bag_of_words(wordList,inputList):
	bagList=[0]*len(wordList)
	for word in inputList:
		if word in wordList:
			bagList[wordList.index(word)]+=1
	return bagList

#训练朴素贝叶斯，输出为p(c=0),p(c=1),p(xi|c=0),p(xi|c=1)
def trainNaiveBayes(trainData,classList):
	sampleNum=len(trainData)
	wordNum=len(trainData[0])

	class0Num=2
	class1Num=2
	wordList_0=ones(wordNum)
	wordList_1=ones(wordNum)

	for i in range(sampleNum):
		if classList[i]==1:
			wordList_1 +=trainData[i]
			class1Num +=1
		else:
			wordList_0 +=trainData[i]
			class0Num +=1

	prob_0=float(class0Num)/sampleNum
	prob_1=float(class1Num)/sampleNum
	probList_0=wordList_0/float(class0Num)
	probList_1=wordList_1/float(class1Num)

	return prob_0, prob_1, probList_0, probList_1

#利用朴素贝叶斯模型进行分类
def calssfy(boolList,prob_0, prob_1, probList_0, probList_1):
	p_0=sum(log(probList_0)*boolList)+log(prob_0)
	p_1=sum(log(probList_1)*boolList)+log(prob_1)

	if p_0 > p_1:
		return 0
	else:
		return 1

#-----------------------test--------------------------

def loadDataSet():
	dataSet=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
	              ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
		      ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
		      ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
	              ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                      ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]

	classVector = [0,1,0,1,0,1]   # 0代表正常言论  1代表侮辱性言论
	return dataSet , classVector

dataSet , classVector=loadDataSet()	
wordList=createWordList(dataSet)
length = len(dataSet)
mat=[]
for i in range(length-1):
	boolList=set_of_words(wordList,dataSet[i])
	mat.append(boolList)

#prob_0, prob_1, probList_0, probList_1=trainNaiveBayes(mat,classVector)
#for i in range(length):
#	cla=calssfy(set_of_words(wordList,dataSet[i]),prob_0, prob_1, probList_0, probList_1)
#	print cla



#-------------------------过滤垃圾邮件-----------------------	
