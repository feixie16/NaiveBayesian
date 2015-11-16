#!/usr/bin/python 
# -*- coding: utf-8 -*- 

from naiveBayes import *
import re

#把文本分解为单词列表
def textParse(bigString):
	listOfWords=re.split(r'\W*',bigString)
	return [ word.lower() for word in listOfWords if len(word)>2 ]

#读取文件
def loadFile():
	dataSet=[]
	classList=[]
	for i in range(1,26):    
		wordList=textParse(open("email/spam/%d.txt" % i).read())
		dataSet.append(wordList)
		classList.append(1)
		wordList=textParse(open("email/ham/%d.txt" % i).read())
		dataSet.append(wordList)
		classList.append(0)
	return dataSet , classList

#留存交叉验证得到训练集和测试集
def  hold_out_cross_validation(dataSet,classList):
	trainSet=[]
	trainClassList=[]
	testSet=[]
	testClassList=[]

	wordList=createWordList(dataSet)
	for i in range(10):
		index=int(random.uniform(0,len(dataSet)))
		testSet.append(bag_of_words(wordList,dataSet[index]))
		testClassList.append(classList[index])
		del(dataSet[index])
		del(classList[index])

	for i in range(len(dataSet)):
		trainSet.append(bag_of_words(wordList,dataSet[i]))
		trainClassList.append(classList[i])

	return trainSet, trainClassList , testSet,  testClassList

#训练并测试贝叶斯，返回分类的错误率
def trainNB(trainSet, trainClassList , testSet,  testClassList):
	prob_0, prob_1, probList_0, probList_1=trainNaiveBayes(trainSet ,trainClassList)
	classList=[]
	testLength=len(testSet)
	errorCount=0
	for i in range(testLength):
		classList.append(calssfy(testSet[i],prob_0, prob_1, probList_0, probList_1))
	
	for i in range(testLength):
		if classList[i]!=testClassList[i]:
			errorCount+=1
	errorRate=float(errorCount)/testLength

	return  errorRate

#多次交叉验证得到的平均错误率
def naiveBayes():
	dataSet , classList=loadFile()
	totalTimes=10
	errorRateSum=0.0
	for i in range(totalTimes):
		dataSet , classList=loadFile()
		trainSet, trainClassList , testSet,  testClassList=hold_out_cross_validation(dataSet,classList)
		errorRateSum+=trainNB(trainSet, trainClassList , testSet,  testClassList)

	averageErrorRate=float(errorRateSum)/totalTimes
	return averageErrorRate 

#----------------------------test----------------------------------
averageErrorRate=naiveBayes()
print averageErrorRate
