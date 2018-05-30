import numpy as np
import os
import sys
import cPickle as pkl

src_ave_features_file = 'home_directory/VIC/track3/filtered_mot_mean_features/all_fea.pkl'
with open(src_ave_features_file, 'r') as f:
    src_ave_features = pkl.load(f)

src_ave_idx_file = 'home_directory/VIC/track3/filtered_mot_mean_features/all_idx.pkl'
with open(src_ave_idx_file, 'r') as f:
    src_ave_idx = pkl.load(f)

print 'all data loaded'

save_root_dir = 'home_directory/VIC/track3/tracklets/features'

trk_res_file = 'home_directory/VIC/track3/tracklets/track_res_v4_idx_505.txt'
with open(trk_res_file, 'r') as f:
    lines =f.readlines()

trk_res = [x.strip().split() for x in lines]

# with open(trk_res_file, 'r') as f:
#     trk_res = pkl.load(f)


all_res = []
for i in range(len(trk_res)):
    res = []
    for j in range(len(trk_res[i])):
        ii = int(trk_res[i][j])
        res.append(src_ave_features[ii])
    all_res.append(res)
    print i, 'finished'

with open(os.path.join(save_root_dir, 'track_res_fea_v4_505.pkl'), 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(all_res, f)

with open(os.path.join(save_root_dir, 'track_res_idx_v4_505.pkl'), 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(trk_res, f)

print 'done'


