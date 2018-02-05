import nltk
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer
import os,sys
import timeit

reload(sys)
sys.setdefaultencoding('utf8')

def OP_to_dict():
	fp=open('output.txt','rb')
	OP_dict=dict()
	for line in fp:
		#print(line)
		if len(line.split())!=0:
			line_array=line.strip().split()
			if line_array[0] in OP_dict:
				OP_dict[line_array[0]]+=[line_array[1]]
			else:
				OP_dict[line_array[0]]=[line_array[1]]
	fp.close()
	return OP_dict;
def Q_to_dict():
	fp=open('query.txt','rb')
	Q_dict=dict()
	for line in fp:
		#print(line)
		if len(line.split())!=0:
			line_array=line.strip().split()
			Q_dict[line_array[0]]=list()
			for i in range(1,len(line_array)):
				Q_dict[line_array[0]]+=[line_array[i]]

	fp.close()
	return Q_dict;

class Index:
    """ Inverted index datastructure """
 
    def __init__(self, tokenizer, stemmer=None, stopwords=None):
        """
        tokenizer   -- NLTK compatible tokenizer function
        stemmer     -- NLTK compatible stemmer 
        stopwords   -- list of ignored words
        """
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.inverse_index = defaultdict(list)

        if not stopwords:
            self.stopwords = set()
        else:
            self.stopwords = set(stopwords)
 
    def lookup(self, words):
        """
        to lookup a word in the index
        """
	doc_list=list()
	for word in words:
	        word = word.lower()
		temp=self.inverse_index[word]
		if len(doc_list)==0:
	 		doc_list=temp
		else:
			doc_list=list(set(doc_list).union(set(temp)))
		#print(word,temp)
        return doc_list;
 
    def add(self, document,doc_name):
        """
        to add a document string to the index
        """
        for token in [t.lower() for t in nltk.wordpunct_tokenize(document)]:
	        if token in self.stopwords:
	                continue
 
	        if self.stemmer:
			token = self.stemmer.stem(token)
 
        	if doc not in self.inverse_index[token]:
                	self.inverse_index[token].append(doc)
		#print(token,self.inverse_index[token])
 
 
 
index = Index(nltk.word_tokenize, 
              None, 
              nltk.corpus.stopwords.words('english'))

alldocs=os.listdir('alldocs')
k=0
for doc in alldocs:
	k+=1
	fp=open('alldocs/'+doc,'rb')
	txt=fp.read()
	index.add(txt,doc)
	print(k,doc,'loaded')
	fp.close()

Q_dict=Q_to_dict()
OP_dict=OP_to_dict()
sorted_keys=sorted(Q_dict.keys())

total_recall=0
total_elapsed=0

for ky in sorted_keys:
	start=timeit.default_timer()
	search_res=index.lookup(Q_dict[ky])
	elapsed=timeit.default_timer()-start
	recall=float(len(list(set(search_res).intersection(set(OP_dict[ky])))))/len(OP_dict[ky])
	total_elapsed+=elapsed
	total_recall+=recall
	print('Query_id = '+str(ky)+' , Recall = '+str(recall)+' , Time_elapsed = '+str(elapsed))
print('average recall',total_recall/len(sorted_keys))
print('average time elapsed',total_elapsed/len(sorted_keys))
