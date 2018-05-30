import scipy.spatial.distance as distance
import numpy as np
import cPickle as pkl
import os
import sys

data_root_dir = sys.argv[3] #'home_directory/VIC/VeRi'
test_pkl = os.path.join(data_root_dir, sys.argv[1] + '.pkl')
query_pkl = os.path.join(data_root_dir, sys.argv[2] + '.pkl')
save_file = os.path.join(data_root_dir, sys.argv[1] + '_' + sys.argv[2] + '_cos_sim_mar.txt')

with open(test_pkl, 'r') as f:
    test = pkl.load(f)
with open(query_pkl, 'r') as f:
    query = pkl.load(f)

# print test[0]
# print test[0].shape

with open(save_file, 'w') as f:
    cnt = 0
    for t in test:
        u = t[0]
        res = ''
        for q in query:
            v = q[0]
            sim = distance.cosine(u, v) #euclidean(u, v) #
            res += str(sim) + ' '
        f.write(res.strip() + '\n')
        cnt += 1
        print cnt , '/', len(test), 'finished'

print 'done'
