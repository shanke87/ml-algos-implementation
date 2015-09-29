import sys 
import math
import pickle

def getProbs(filestr):
	file = open(filestr, 'rb')
	obj = pickle.load(file)
	file.close()

	return obj

def compwords(w1,w2):
	w1s = w1.split('/')
	w2s = w2.split('/')
	if(w1s[1] == w2s[1]):
		return 1
	else:
		return 0

def compare(ref_file,out_file,observe):
	ref = open(ref_file,"rU")
	out = open(out_file,"rU")

	tot = 0
	acc = 0
	totKn = 0
	accKn = 0
	totUn = 0
	accUn = 0
	for rline in ref:
		oline = out.readline()
		rwords = rline.split()
		owords = oline.split()
		owords[-1] = owords[-1].split('\n')[0]
		if len(rwords) != len(owords):
			print("ayyo",rwords)
			print(owords)
			sys.exit(-1)
		
		for i in range(len(rwords)):
			compres = compwords(rwords[i],owords[i])
			word = owords[i].split("/")[0]
			if word in observe:
				totKn = totKn + 1
				accKn = accKn + compres
			else:
				totUn = totUn + 1
				accUn = accUn + compres
			
			tot = tot + 1
			acc = acc + compres
	print("Accuracy % :", acc/tot*100)
	print("Accuracy Unknown % :", accUn/totUn*100)
	print("Accuracy Known % :", accKn/totKn*100)
	

def main():
	if(len(sys.argv) < 5):
#		print("usage : ")
#		print("python bigram-train.py -text train_file -lm lm_file")
#		sys.exit(-1)
		ref_file = "small-train.txt"	
		out_file = "output.txt"
		lm_file = "lm_file.txt"
	else:
		ref_file = sys.argv[2]
		out_file = sys.argv[4]
		lm_file  = sys.argv[6]

	dic = getProbs(lm_file)
	compare(ref_file,out_file,dic['observe'])

main()
