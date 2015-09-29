W0 = 0
eta = 0.1
lamb = 1.4
ITERATION = 20

import sys
import os
import re
import math
import operator
import random

SPAM_DIR = "spam"
HAM_DIR  = "ham"
bad = 0
stop = set([ 'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can\'t', 'cannot', 'could', 'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t', 'having', 'he', 'he\'d', 'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'how\'s', 'i', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it', 'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most', 'mustn\'t', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours	ourselves', 'out', 'over', 'own', 'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s', 'should', 'shouldn\'t', 'so', 'some', 'such', 'than', 'that', 'that\'s', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll', 'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'when', 'when\'s', 'where', 'where\'s', 'which', 'while', 'who', 'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t', 'you', 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours', 'yourself', 'yourselves'])
yesstop = 0
def llg(val):
	return math.log(val,10)
def apply(val):
	return llg(val)

def join(val1,val2):
	return val1 + val2
def initialize():
	return 0

def getFilesInDir(parDir, childDir):
	mypath = os.path.join(parDir,childDir)
	return [ os.path.join(mypath,f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f)) ]

def updateVocab(files):
	patt = re.compile("^\\s+$")
	vocabmap = {}
	cnt = 0
	for fstr in files:
		file = open(fstr,'rU',encoding='latin-1')
		for line in file:
			if patt.match(line):
				continue
			words = line.split()
			for word in words:
				if(word not in vocabmap):
					vocabmap[word] = cnt
					cnt = cnt + 1
		file.close()
	return vocabmap	

def getFreq(doc, dic):
	file = open(doc,'rU',encoding='latin-1')
	#print("Doc", doc)
	first = 1
	patt = re.compile("^\\s+$")
	for line in file:
		if patt.match(line):
			continue
		words = line.split()
		for i in range(0,len(words)):
			if words[i] not in dic:
				dic[words[i]] = 1
			else:
				dic[words[i]] = dic[words[i]] + 1
	file.close()

globpatt = re.compile("^\\s+$")
outofvocab = set()

def getXvector(doc,vocabmap):
	V = len(vocabmap)
	x = [0]*V
	file = open(doc,'rU',encoding='latin-1')
	tot = 0
	for line in file:
		if globpatt.match(line):
			continue
		words = line.split()
		tot = tot + len(words)
		for word in words:
			if word in vocabmap:
				ind = vocabmap[word]
				x[ind] = x[ind] + 1
			else:
				if (yesstop == 1 and word not in stop) or yesstop == 0:
					outofvocab.add(word)

	for i in range(V):
		x[i] = x[i]
	
	file.close()
	return x

def dotProd(x,w):
	s = 0 
	for i in range(len(x)):
		s = s + x[i]*w[i]
	return s

def getOneSigmoid(x,w):
	
	term = 1 + math.exp(-( dotProd(x,w) + W0 ))
	return 1/term

def getWithDPOneSigmoid(dp):
	if(-dp > 700):
		return  1
	if(dp > 700) : 
		return 0

	term = 1 + math.exp(-(dp + W0))
	return 1/term


def trainRegression(trainDocs,vocabmap):
	V = len(vocabmap)
	w = [1]*V
	random.seed(15485683)
	for i in range(1,V):
		w[i] = random.randrange(30,100)
	W0 = 1
	lx = [None]*(len(trainDocs[0]) + len(trainDocs[1]))
	y  = [None]*(len(trainDocs[0]) + len(trainDocs[1]))

	l = 0
	for c in range(len(trainDocs)):
		for doc in trainDocs[c]:
			lx[l] = getXvector(doc,vocabmap)
			y[l] = c
			l = l + 1
			
	#print(lx)
	#print(y)
	yp = [0]*l
	tmpw = [0]*V
	changw = [None]*V

	dtp = [0]*(l)	
	change = w[V-1]

	for ex in range(l):
		dtp[ex] = dotProd(lx[ex],w) - lx[ex][V-1]*w[V-1]
	
	for iter in range(ITERATION):
		maxwi  = -1 
		maxchange = 0
		
		for i in range(V):
			tmpw[i] = 0
			
			prevind = i-1
			if(prevind < 0):
				prevind = V-1
				
			for ex in range(0,l):
				dtp[ex] = dtp[ex] + change*lx[ex][prevind]
				#print(iter,i,ex,dtp[ex],dotProd(lx[ex],w))
				yp[ex] = y[ex] - getWithDPOneSigmoid(dtp[ex])
			
			for ex in range(l):
				tmpw[i] = tmpw[i] + lx[ex][i]*yp[ex]
			
			change = eta * tmpw[i] - eta*lamb*w[i]
			if(changw[i] != None) :
				chch = (changw[i] - change)
			#	print(changw[i],change)
				if(change != 0 and math.fabs(chch / change) < 0.3 ):
					if(chch != 0):
						change = change/chch * change
					else:
						change = change*change
				changw[i] = None
			else:
				changw[i] = change

			w[i] = w[i] + change
			if(maxwi == -1 or maxchange < change):
				maxwi = i
				maxchange = change
			#print("iter",iter,i,w[i],change)
		print("iter",iter,maxwi,w[maxwi],maxchange)
		if(maxchange < 1e-05):
			break
#		print("W",w)
	#print("W",w)	
	ret = {}
	ret['w'] = w
	return ret

def applyRegression(w,d,vocabmap):
	x = getXvector(d,vocabmap)
	dp = dotProd(x,w) + W0	
	if(-dp  > 700):
		oneP = 1
		zeroP = 0
	elif(dp >700) : 
		zeroP = 1
		oneP = 0
	else:
		exp = math.exp( -(dotProd(x,w) + W0 ) )
		oneP = 1/(1 + exp)
		zeroP = exp/(1+exp)
	
#	print(d,"X",x,oneP,zeroP, math.exp(oneP) + math.exp(zeroP))
	
	if zeroP - oneP > 0:
		return 0
	else:
		return 1

def main(train_dir,test_dir):
	train_classified_docs = [ getFilesInDir(train_dir, SPAM_DIR),getFilesInDir(train_dir,HAM_DIR) ]
	
	vocabmap = updateVocab(train_classified_docs[0] + train_classified_docs[1])
	ret = trainRegression(train_classified_docs,vocabmap)
	w = ret["w"]
	V = len(vocabmap.keys())
	print(V,"Vocab size")
#	print(vocabmap)


	test_classified_docs = [ getFilesInDir(test_dir,SPAM_DIR),getFilesInDir(test_dir,HAM_DIR) ]

	for c in range(len(test_classified_docs)):
		correct = 0
		for d in test_classified_docs[c]:
			k = applyRegression(w,d,vocabmap)
			#print("Actual value", c , "Observed value", k, "doc",d)
			if(k == c):
				correct = correct + 1
		Nc = len(test_classified_docs[c])
		print("Accurracy " + str(c) + " : " , correct/Nc)
 
if(len(sys.argv) < 3):
	print("Give command line arguments: test_directory_path train_directory_path")
	sys.exit(-1)
else:
	train_dir = sys.argv[1]
	test_dir  = sys.argv[2]
	
	if(sys.argv == 3):
		yesstop = 1

main(train_dir,test_dir)
