import sys 
import math
import pickle

unigram_dict = {} 
bigram_dict = {}
reverse_bigram = {}
observe = {}
gamma = 0.99
totalN = 0
ST_TAG = "START"
END_TAG = "END"
def getFreq(trainf):
	global unigram_dict,bigram_dict, reverse_bigram, observe, gamma
	file = open(trainf, 'rU')
	N = 0
	for line in file:
		prev = ''
		line = ST_TAG + "/" + ST_TAG + " " + line + " " + END_TAG + "/" + END_TAG
		
		words = line.split()
		N = N + len(words)
		count = 0 
		for word in words: 
			# FOR UNIGRAM
			splits = word.split('/')
			word = splits[0]
			pos  = splits[1]	

			if pos not in unigram_dict:
				unigram_dict[pos] = 1
			else:
				unigram_dict[pos] = unigram_dict[pos] + 1

			# FOR BIGRAM 
			if count > 0:
				if pos not in bigram_dict:
					bigram_dict[pos] = {}

				if prev not in bigram_dict[pos]:
					bigram_dict[pos][prev] = 1
				else:
					bigram_dict[pos][prev] = bigram_dict[pos][prev] + 1

				if prev not in reverse_bigram:
					reverse_bigram[prev] = set([])
			
				reverse_bigram[prev].add(pos)

			# FOR OBSERVATION FREQ
			if pos not in observe:
				observe[pos] = {}
			if word not in observe[pos]:
				observe[pos][word] = 1
			else:
				observe[pos][word] = observe[pos][word] + 1

			count = count + 1
			prev = pos
	file.close()
	return N

pBigram = {} 
pUnigram = {} 
pObserve = {}
def calcProb(totalN):
	global pBigram,pUnigram,pObserve
	# UNIGRAM
	for w in unigram_dict:
		pUnigram[w] = unigram_dict[w] / totalN

	# BIGRAM with interpolation
	bigram_dict[ST_TAG] = {}
	bigram_dict[END_TAG] = {}
	for w in unigram_dict:
		pBigram[w] = {}
		if w in bigram_dict:     
			cnt = 0
			for h in unigram_dict:
				if h not in bigram_dict[w]:
					cnt = cnt + 1
			if cnt == len(unigram_dict):
				for h in unigram_dict:
					pBigram[w][h] = pUnigram[h]

			for h in unigram_dict:
				if h not in bigram_dict[w]: 
					pBigram[w][h] = pUnigram[h] * (1 - gamma)
					#pBigram[w][h] = 1
				else:
					pBigram[w][h] = (bigram_dict[w][h]/unigram_dict[h])*gamma + (1-gamma)*pUnigram[h]
					if pBigram[w][h] > 1.00:
						print("Error %s %s %3.5f" %(w,h,pBigram[w][h]))
			
	# OBSERVATIONAL
	for pos in observe:
		for word in observe[pos]:
			if word not in pObserve:
				pObserve[word] = {}
			pObserve[word][pos] = observe[pos][word]/unigram_dict[pos]

	s = 0
	for a in pBigram:
		s = s + len(pBigram[a])
	if(s < len(unigram_dict)*len(unigram_dict)):
		print(s,"ayyo")
		print(unigram_dict)
		print(pBigram)
		sys.exit(-1)
def printout():
	suni = sorted(unigram_dict.keys())
	print("ugram")
	for w in suni:
		print("%s %f" %(w,math.log(pUnigram[w],2)))
	print("bigram")
	for w in bigram_dict:
		for h in bigram_dict[w]:
			print( "%s %s %f" %(h,w,math.log(pBigram[w][h],2)))
	print("obser")	
	for w in pObserve:
		for pos in pObserve[w]:
			print("%s %s %f" %(w,pos,math.log(pObserve[w][pos],2)))
	

def printall(outf):
	file = open(outf,"wb")
	
	dic = {}
	dic['unigram'] = pUnigram
	dic['bigram']  = pBigram
	dic['observe'] = pObserve

	pickle.dump(dic,file)
	

	file.close()
	return dic

def getProbs(filestr):
	file = open(filestr, 'rb')
	obj = pickle.load(file)
	file.close()
	return obj

def main():
	if(len(sys.argv) < 5):
#		print("usage : ")
#		print("python bigram-train.py -text train_file -lm lm_file")
#		sys.exit(-1)
		inp_file = "small-train.txt"	
		out_file = "lm_file.txt"
	else:
		inp_file = sys.argv[2]
		out_file = sys.argv[4]
	
	

#	print(inp_file,out_file)
	global totalN
	totalN = getFreq(inp_file)
	calcProb(totalN)
	uniqN  = len(unigram_dict.keys())
		
	bg = 0
	for p1 in bigram_dict.keys():
		bg = len(bigram_dict[p1])
	
	print(pObserve["START"]["START"],pObserve["END"]["END"],unigram_dict["START"],unigram_dict["END"])
	dic = printall(out_file)
	if(len(sys.argv) > 5):
		printout()
'''	tagpairs = sum([ len(bigram_dict[w]) for w in bigram_dict])
	obspairs = sum([ len(observe[w]) for w in observe])
	print(len(unigram_dict),tagpairs,obspairs)
	obspairs = sum([ len(pObserve[w]) for w in pObserve])
	tagpairs = sum([ len(pBigram[w]) for w in pBigram])
	print(len(pUnigram),tagpairs,obspairs)
	print(uniqN, bg, totalN)
'''
main()

	
	
