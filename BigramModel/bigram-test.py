import sys
import math

def getProbs(file):
		
	boolIsBG = 0
	bgram = {}
	ugram = {}
	alpha = {}
	for line in file:
		words = line.split()
		if len(words) == 1:
			if(words[0] != 'unigrams:'):
				boolIsBG = 1 
			continue
		if len(words) != 3:
			print("Ayyo " + line)
			continue

		if(boolIsBG == 1):
			if words[2] not in bgram:
				bgram[words[2]] = {}
			bgram[words[2]][words[1]] = float(words[0])
		else:
			if(words[2] == 'None'):
				words[2] = "0"
			ugram[words[1]] = float(words[0])
			alpha[words[1]] = float(words[2])

	res = {}
	res['bgram'] = bgram
	res['ugram'] = ugram
	res['alpha'] = alpha
	
	return res	

def fcomp(a,b):
	if math.fabs(a-b) < 10e-10:
		return 0
	else:
		if a > b:
			return 1
		else:
			return -1

def getPerpex(strf, bgram, ugram, alpha):
	file = open(strf, 'rU')
	N = 0
	tot = 0
	for line in file:
		count = 0 
		prev = ''
		words = line.split()
		N = N + len(words)
		for word in words: 
			if count > 0:
				if word in ugram and prev in ugram:
					if word not in bgram or prev not in bgram[word]: 
						# KATZ
						tot = tot + ( alpha[prev] + ugram[word] )
						#print(prev,word,"back", alpha[prev], ugram[word])
					else:
						tot = tot + bgram[word][prev]
						#print(prev,word,bgram[word][prev])
				else:
					# UNKNOWN WORDS CASE
					#print("Unknown word",prev,word)
					tot = tot + 0
			count = count + 1
			prev = word

	print("Perplexity :" , math.pow(2, -tot/N))

def main():
	if(len(sys.argv) < 5):
		print("usage : ")
		print("python bigram-test.py -text test_file -lm lm_file")

	test_file = sys.argv[2]
	lm_file = sys.argv[4]

#	print(test_file,lm_file)
	
	mine = open(lm_file, 'rU')
	resm = getProbs(mine)
	mine.close()

	getPerpex(test_file, resm['bgram'],resm['ugram'],resm['alpha'])
	
main()
