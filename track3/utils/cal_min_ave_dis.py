import scipy.spatial.distance as distance
import numpy as np
import cPickle as pkl
import os
import sys
import pdb

root_dir = 'home_directory/VIC/track3/new'


filtered_dis_dir = os.path.join(root_dir, 'filtered_mot_final_distance/diss')

# concat all filtered cache
all_split_num = 50
all_res = []
for i in range(all_split_num):
    with open(os.path.join(filtered_dis_dir, 'filtered_dis_' + str(i) + '.pkl'), 'r') as f:
        split_cache = pkl.load(f)
    all_res += split_cache


total_sum = 0
total_cnt = len(all_res) * 14

for each in all_res:
    for i in range(14):
        total_sum += each[i * 4]

ave = total_sum / float(total_cnt)

print ave
