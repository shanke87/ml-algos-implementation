import sys
import math
import pickle
import pprint 

ST_TAG = "START"
END_TAG = "END"
def getProbs(filestr):
	file = open(filestr, 'rb')
	obj = pickle.load(file)
	file.close()
	return obj

prob = [ {} for i in range(50)]
prev = [ {} for i in range(50)]

def vertibi(taglist, trans,observe,words):
	Nt = len(words)
	global prob, prev
	if Nt > len(prob):
		prob = [ {} for i in range(Nt)]
		prev = [ {} for i in range(Nt)]

	for i in range(Nt):
		prob[i].clear()
		prev[i].clear()

	for tag in taglist:
		prob[0][tag] = 0
		prev[0][tag] = "NULL"

	prob[0][ST_TAG] = 1.0	
	wc = 0
	for word in words:
		if wc == 0:
			wc = 1
			continue
		#print(wc,word)
		for tag in taglist:
			maxv = 0
			maxtag = -1
			pobs = 0
			if(tag in observe[word]):
				pobs = observe[word][tag]
			for prevtag in taglist:
				try:
					
					vp = prob[wc-1][prevtag]*trans[tag][prevtag]*pobs
			
					if vp > maxv or maxtag == -1:
						maxv = vp
						maxtag = prevtag


				except :
					print(prevtag,wc-1, "HERE")
					print(prob[wc-1][prevtag])
					print(tag,prevtag, "NEXT")
					print(trans[tag][prevtag])
					raise NameError("test")

			
			prob[wc][tag] = maxv
			prev[wc][tag] = maxtag

		#print(observe[word])
		#print(prob[wc])
		#print(prev[wc])
		wc = wc + 1

	guessTags = [0]*Nt
	st = END_TAG
	for wc in range(Nt-1, -1, -1):
		guessTags[wc] = st
		st = prev[wc][st]

	'''
	wc = 0
	for w in words:
		if(wc == 0):
			wc = 1
			continue
		print(w,": ",end="")
		for tag in taglist:
			pobs = 0
			if tag in observe[w]:
				pobs = observe[w][tag]
			print("%s,%f,%f " %(tag,prob[wc][tag],pobs), end="")

		wc = wc + 1	
		print("")
	'''
	return guessTags


def getUnknownWordDist(word,observe,unigram,index):
	dis = {}
	alphas = 0
	digits = 0
	for i in range(len(word)):
		if word[i] >= '0' and word[i] <= '9':
			digits = digits + 1
		elif (word[i] >= 'A' and word[i] <= 'Z') or (word[i] >= 'A' and word[i] <= 'Z'):
			alphas = alphas + 1
		
	if alphas == 0 and digits > 0: 
		for tag in unigram:
			dis[tag] = 0
		dis['CD'] = 1.0
	else: 
		if digits == 0 and alphas > 0 and word[0] >= 'A' and word[0] <= 'Z':
			if index != 0:
				for tag in unigram:
					dis[tag] = 0
				dis['NNP'] = 1.0
			else: 
				su = 0
				for tag in unigram:
					if tag != 'NNP':
						dis[tag] = unigram[tag] * 0.7
						su = su + unigram[tag] * 0.3
				dis['NNP'] = su + unigram['NNP']

		else:
			for tag in unigram:
				dis[tag] = unigram[tag]
			
	return dis


def guessTags(taglist, unigram, trans,observe,test_file,out_file):
	inpfile = open(test_file,"rU")
	outfile = open(out_file, "w")
	try:
		x = 0
		for line in inpfile:
			line = ST_TAG + " " + line + " " + END_TAG
			words = line.split()
			index = 0 
			for word in words:
				if(word not in observe):
					observe[word] = getUnknownWordDist(word,observe,unigram,index)
				index = index + 1

			tags = vertibi(taglist,trans,observe,words)
			x = x + 1
			for i in range(1,len(words)-1):
				outfile.write(words[i]+ "/" + tags[i] + " ")
			outfile.write("\n")
	except Exception as ex:
		print(ex.args)
		raise ex
	finally:
		outfile.close()
		inpfile.close()

def main():
	if(len(sys.argv) < 7):
	#	print("usage : ")
	#	print("python bigram-test.py -text test_file -lm lm_file")
		test_file = "small-test.txt"
		lm_file = "lm_file.txt"
		out_file = "output.txt"
	else:
		test_file = sys.argv[2]
		lm_file = sys.argv[4]
		out_file = sys.argv[6]
	
	resm = getProbs(lm_file)
	taglist = [ w for w in resm['unigram']]
	#taglist.append('<s>')
	
	#print(taglist)
	guessTags(taglist, resm['unigram'],resm['bigram'],resm['observe'],test_file,out_file)
	
main()
