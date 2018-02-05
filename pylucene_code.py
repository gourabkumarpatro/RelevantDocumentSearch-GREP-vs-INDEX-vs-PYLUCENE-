import os,sys,lucene
import timeit
from os import path,listdir
from java.io import File
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.util import Version
from org.apache.lucene.store import RAMDirectory, SimpleFSDirectory
from datetime import datetime

# Indexer imports:
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.index import IndexReader

# Retriever imports:
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser

reload(sys)
sys.setdefaultencoding('utf8')
#------------------------------------output.txt to dictionary--------------------------------------------------
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
#-----------------------------------query.txt to dictionary----------------------------------------------------
def Q_to_dict():
	fp=open('query.txt','rb')
	Q_dict=dict()
	for line in fp:
		#print(line)
		if len(line.split())!=0:
			line_array=line.strip().split()
			Q_dict[line_array[0]]=str()
			for i in range(1,len(line_array)):
				Q_dict[line_array[0]]+=line_array[i]+','

	fp.close()
	return Q_dict;


#-----------------------printing versions----------------------------------------------
print "Python version: %d.%d.%d" % (sys.version_info.major,
                                      sys.version_info.minor,
                                      sys.version_info.micro)
print 'Lucene version:', lucene.VERSION

#------------------------global constants----------------------------------------------
INPUT_DIR='alldocs/'
INDEX_DIR='lucene_index/'

#------------------------indexing------------------------------------------------------

#doc reading
def create_document(file_name):
    path = INPUT_DIR+file_name # assemble the file descriptor
    file = open(path) # open in read mode
    doc = Document() # create a new document
    # add the title field
    doc.add(StringField("title", input_file, Field.Store.YES))
    # add the whole book
    doc.add(TextField("text", file.read(), Field.Store.YES))
    file.close() # close the file pointer
    return doc

# Initializing lucene and the JVM
lucene.initVM()


#new directory for lucene indexing
directory = SimpleFSDirectory(File("lucene_index/"))
# Getting and configuring an IndexWriter
analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
analyzer = LimitTokenCountAnalyzer(analyzer, 1000000000)
config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
writer = IndexWriter(directory, config)

print "Number of indexed documents: %d\n" % writer.numDocs()
for input_file in listdir(INPUT_DIR): # iterate over all input files
	print "Current file:", input_file
	if 1:
	  	doc = create_document(input_file) # call the create_document function
	       	writer.addDocument(doc) # add the document to the IndexWriter

print "\nNumber of indexed documents: %d" % writer.numDocs()
writer.close()
print "Indexing done!\n"
print "------------------------------------------------------"



#--------------------retrieving doc names----------------------------------------------------
def search_loop(searcher, analyzer):
	Q_dict=Q_to_dict()
	OP_dict=OP_to_dict()
	total_recall=0
	total_elapsed=0
	sorted_keys=sorted(Q_dict.keys())	
     	for ky in sorted_keys:
		command=Q_dict[ky]
		query = QueryParser(Version.LUCENE_CURRENT, "text", analyzer).parse(command)
	        start = timeit.default_timer()
        	scoreDocs = searcher.search(query, 50).scoreDocs
        	duration = timeit.default_timer() - start
		total_elapsed+=duration
		doc_list=list()
		for scoreDoc in scoreDocs:
			doc=searcher.doc(scoreDoc.doc)
			doc_list+=[str(doc['title'])]
		#print(ky,doc_list)
		recall=float(len(list(set(doc_list).intersection(set(OP_dict[ky])))))/len(OP_dict[ky])
		total_recall+=recall
		
		print('Query_id = '+str(ky)+' , Recall = '+str(recall)+' , Time_elapsed = '+str(duration))
        	#print "%s total matching documents in %s:" % (len(scoreDocs), duration)
	print('average recall',total_recall/len(sorted_keys))
	print('average time elapsed',total_elapsed/len(sorted_keys))
	print "\n------------------------------------------------------"


# Creating a searcher for the above defined Directory
searcher = IndexSearcher(DirectoryReader.open(directory))

# Creating a new retrieving analyzer
analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

# calling searching block
search_loop(searcher, analyzer)
