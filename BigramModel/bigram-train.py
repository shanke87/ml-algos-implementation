import sys 
import math
unigram_dict = {} 
bigram_dict = {}
reverse_bigram = {}
gamma = 0.99
def getFreq(trainf):
	file = open(trainf, 'rU')
#	file = open('train_small.txt', 'rU')
#	file = open('hw2_test.txt', 'rU')
	N = 0
	for line in file:
		count = 0 
		prev = ''
		words = line.split()
		N = N + len(words)
		for word in words: 
			# FOR UNIGRAM
			if word not in unigram_dict:
				unigram_dict[word] = 1
			else:
				unigram_dict[word] = unigram_dict[word] + 1

			# FOR BIGRAM 
			if count > 0:
				if word not in bigram_dict:
					bigram_dict[word] = {}

				if prev not in bigram_dict[word]:
					bigram_dict[word][prev] = 1
				else:
					bigram_dict[word][prev] = bigram_dict[word][prev] + 1

				if prev not in reverse_bigram:
					reverse_bigram[prev] = set([])
			
				reverse_bigram[prev].add(word)

			count = count + 1
			prev = word
			
	file.close()
	return N

def getInverseCount(count):
	N = 0
	for w in bigram_dict:
		for h in bigram_dict[w]:
#			print(w + " " + h + " " + bigram_dict[w][h])
			if bigram_dict[w][h] == count:
				N = N + 1
	return N

def fcomp(a,b):
	if math.fabs(a-b) < 10e-8:
		return 0
	else:
		if a > b:
			return 1
		else:
			return -1

pBigram = {} 
pUnigram = {} 
alpha = {}

def calcProb(N, N1, N2):
	for w in unigram_dict:
		pUnigram[w] = unigram_dict[w] / N
	
	for w in bigram_dict:
		pBigram[w] = {}
		for h in bigram_dict[w]:
			if bigram_dict[w][h] == 1: 
				pBigram[w][h] = 2 * N2 / ( N1 * unigram_dict[h] )
			elif bigram_dict[w][h] > 1:
				pBigram[w][h] = bigram_dict[w][h] / unigram_dict[h]
				if pBigram[w][h] > 1.00:
					print("Error %s %s %3.5f" %(w,h,pBigram))
					
	for h in reverse_bigram:
		pnum = 0.0
		pden = 0.0
		pnumml = 0.0
		pnumgt = 0.0
		hasGT = 0
		for w in reverse_bigram[h]:
			pnum = pnum + pBigram[w][h] 
			pden = pden + pUnigram[w]
			if(bigram_dict[w][h] == 1):
				pnumgt = pnumgt + pBigram[w][h]
				hasGT = 1
			else:
				pnumml = pnumml + pBigram[w][h]
			

		if(hasGT == 0):
			#print("haha",pnumml,pnumgt,h)
			for w in reverse_bigram[h]:
				if(bigram_dict[w][h] > 1):
					pBigram[w][h] = pBigram[w][h] * gamma

			alpha[h] = (1 - gamma) / (1 - pden)
		else:
			if(fcomp(pnumml+pnumgt,1.0) == 1):
				print(h,pnumml,pnumgt,hasGT,pnum)
				sys.exit(-1)

			alpha[h] = (1 - pnum)  / (1-pden)

def printall(outf):
	file = open(outf,"w")
	file.write("unigrams:\n")
	suni = sorted(unigram_dict.keys())
	alpha['</s>'] = 1
	for w in suni:
#		if(w in alpha and alpha[w] != 0):
#			try:
				file.write("%3.15f %s %3.15f\n" %(math.log(pUnigram[w],2), w, math.log(alpha[w],2)))
#			except ValueError:
#				file.write("Ayyo problem" + str(pUnigram[w]) + " " + str(alpha[w]))
#				sys.exit(-1)
#		else:
#			file.write(str(math.log(pUnigram[w],2)) + " " + w + " zeroo")
	file.write("bigrams:\n")
	for w in bigram_dict:
		for h in bigram_dict[w]:
			file.write( "%3.10f %s %s\n" %(math.log(pBigram[w][h],2),h,w))
	file.close()

def main():
	

	if(len(sys.argv) < 5):
		print("usage : ")
		print("python bigram-train.py -text train_file -lm lm_file")
		sys.exit(-1)

	inp_file = sys.argv[2]
	out_file = sys.argv[4]

	print(inp_file,out_file)

	N = getFreq(inp_file)

	uniqN  = len(unigram_dict.keys())
	N1 = getInverseCount(1)
	N2 = getInverseCount(2) 

	calcProb(N,N1,N2)

	printall(out_file)

main()

	
	
