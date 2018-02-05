# RelevantDocumentSearch
## (Comparing GREP-vs-INDEX-vs-PYLUCENE)
Dataset_link=https://drive.google.com/open?id=1pogGFFrn_WjIKn5uTKQ_mw4N4CIhalQF <br>
The folder contains query.txt, output.txt, alldocs.rar.
1. query.txt contains total 82 queries, which has 2 columns query id and query.
2. alldocs.rar contains documents file named with doc id. Each document has set of sentences.
3. output.txt contains top 50 relevant documents (doc id) for each query.<br>
***DON'T FORGET TO EXTRACT THE RAR FILE BEFORE RUNNING THE CODES

The objective is to use three different methods to retrieve all the relevant document(with out ranking) out of more than 5800 documents based on the query terms and then to compare the results.The codes will print the time to retrieve and recall value. As we are retrieving with out ranking, so calculating Precision doesn't make any sense here in this task.

## COMPARISION TABLE 

Method                      GREP            INDEX-NLTK          PYLUCENE 

Mean Recall               0.6736            0.7578              0.7031 
  
Mean Exec Time (Sec)      0.8487            0.0019              0.0015 



















 
