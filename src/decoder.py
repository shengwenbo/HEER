import torch as t
import numpy as np
import cPickle
import sys

def myfmt(r):
	return "%.6f" % (r,)

def decode(offset, out_mapping, address):
	offset = list(offset.iteritems())
	offset.sort(key=lambda x: x[1])
	for k, i in enumerate(offset):
		if address >= i[1] and address < offset[k+1][1]:
			return i[0]+':'+str(out_mapping[i[0]][address-i[1]])
			 

if __name__ == '__main__':
	t.cuda.set_device(int(sys.argv[2]))
	model = t.load('/shared/data/qiz3/data/model/subtype_' + sys.argv[1] +'.pt')
	emb = model.input_embeddings()
	offset = cPickle.load(open('/shared/data/qiz3/data/offset.p'))
	out_mapping = cPickle.load(open('/shared/data/qiz3/data/out_mapping.p'))
	with open('/shared/data/qiz3/data/hin_' + sys.argv[1] + '.emb', 'w') as IN:
		for i in xrange(emb.shape[0]):
			prefix = decode(offset, out_mapping, i)
			if 'cp' in prefix:
				break
			#IN.write(decode(offset, out_mapping, i) +' '+ np.array2string(emb[i,:], prefix='',separator=' ', precision=6)+'\n')
			vecfmt = np.vectorize(myfmt)
			IN.write(prefix +' '+ ' '.join(vecfmt(emb[i,:]).tolist())+'\n')
			#print(np.ndarray.tolist(np.around(emb[i,:], decimals=6)))
			if i % 100000 == 0:
				print(i)
			#break
