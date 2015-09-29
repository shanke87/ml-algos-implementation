import sys
import os
import re
import math

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

def updateVocab(files,vocab):
	
	for fstr in files:
		file = open(doc,'rU',encoding='latin-1')
		for line in file:
			if patt.match(line):
				continue
			words = line.split()
			for word in word:
				if (yesstop == 1 and word not in stop) or yesstop == 0:
					vocab.add(word)

		file.close()
	return	

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
				if (yesstop == 1 and word not in stop) or yesstop == 0:
					dic[words[i]] = 1
			else:
				dic[words[i]] = dic[words[i]] + 1
	file.close()

def trainMultinomial(train_classified_docs):

	allClassFreq = []
	C = len(train_classified_docs)
	for c in range(C):
		classFreq = {}
		for d in train_classified_docs[c]:
			getFreq(d,classFreq)
		allClassFreq.append(classFreq)

	vocabset = set()
	Tcall = [0]*C
	for c in range(C):
		for key in allClassFreq[c].keys():
			vocabset.add(key)
			Tcall[c] = Tcall[c] + allClassFreq[c][key]

	V = len(vocabset)
	N = sum( [len(el) for el in train_classified_docs] )
#	print("Start",N,V,"Tcall",Tcall)
#	print("Vocab", vocabset)
	condProb = {} 
	for word in vocabset:
		condProb[word] = [0]*C

	priors = [None]*C

	for c in range(C):
		Nc = len(train_classified_docs[c])
#		priors[c] = math.log(2,Nc/N)
		priors[c] = apply(Nc/N)
		print("Priors",c,Nc/N,"TCall", Tcall)
		classFreq = allClassFreq[c]
		for word in vocabset:
			freq = 0
			if word in classFreq:
				freq = classFreq[word]
			
			condProb[word][c] = (freq+1)/(Tcall[c] + V)
			condProb[word][c] = apply(condProb[word][c])
			
		#print("Class freq",c, classFreq)
	#print("Condi", condProb)
			
	ret = {}
	ret["vocabset"] = vocabset
	ret["condProb"] = condProb
	ret["priors"] = priors
	return ret

def applyMultinomial(C,doc,vocabset,condProb,priors):
	freq = {}
	getFreq(doc,freq)
	#print("Freq",freq)
	maxc = -1 
	maxscore = 0
	
	bad = 0
	for c in range(C):
		score = initialize()
		for word in freq.keys():
			if(word in condProb):
				score = join(score,condProb[word][c])
				if freq[word] > 1: 
					score = join(score,freq[word])
			else:
				bad = bad + 1
		score = join(score,priors[c])
#		print("scores",doc,c,score,"prior",priors[c])
		if score > maxscore or maxc == -1:
			maxscore = score
			maxc = c
#	print("MAX", maxc, maxscore,"BAD",bad)
	return maxc

def main(train_dir,test_dir):
	train_classified_docs = [ getFilesInDir(train_dir, SPAM_DIR),getFilesInDir(train_dir,HAM_DIR) ]
	
	ret = trainMultinomial(train_classified_docs)
	vocabset = ret["vocabset"]
	condProb = ret["condProb"]
	priors = ret["priors"]

	V = len(vocabset)
	print(V,"Vocab size")

	test_classified_docs = [ getFilesInDir(test_dir,SPAM_DIR),getFilesInDir(test_dir,HAM_DIR) ]

	for c in range(len(test_classified_docs)):
		correct = 0
		for d in test_classified_docs[c]:
			k = applyMultinomial(len(train_classified_docs),d,vocabset,condProb,priors)
			
#			print("Actual value", c , "Observed value", k, "doc",d)
			if(k == c):
				correct = correct + 1
		Nc = len(test_classified_docs[c])
		print("Accurracy " + str(c) + " : " , correct/Nc)


if(len(sys.argv) < 3):
	print("Give command line arguments: test_directory_path train_directory_path")
	sys.exit(-1)
	train_dir = "small-train"
	test_dir  = "small-test"
else:
	train_dir = sys.argv[1]
	test_dir  = sys.argv[2]
	if(sys.argv == 4):
		yesstop = 1

main(train_dir,test_dir)
