from collections import defaultdict
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

Q_dict=Q_to_dict()
OP_dict=OP_to_dict()

total_recall=0
total_elapsed=0

sorted_keys=sorted(Q_dict.keys())

for ky in sorted_keys:
	words=Q_dict[ky]
	results=list()
	start=timeit.default_timer()
	for word in words:
		results+=[i[8:] for i in (os.popen('grep -HFLr \'alldocs/\' -e '+word).read()).split()]
	elapsed=timeit.default_timer()-start
	recall=float(len(list(set(results).intersection(set(OP_dict[ky])))))/len(OP_dict[ky])
	total_elapsed+=elapsed
	total_recall+=recall
	print('Query_id = '+str(ky)+' , Recall = '+str(recall)+' , Time_elapsed = '+str(elapsed))
print('average recall',total_recall/len(sorted_keys))
print('average time elapsed',total_elapsed/len(sorted_keys))
