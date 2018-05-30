import numpy as np
import cPickle as pkl
import os
import sys

root_dir = '/mnt/lustre/share/aicitychallenge/track3/dets'
save_root_dir = 'home_directory/VIC/track3/new_25000/filtered_mot_res'

thresh = [15000]

all_locs = ['Loc1_1', 'Loc1_2', 'Loc1_3', 'Loc1_4', 'Loc2_1', 'Loc2_2', 'Loc2_3', 'Loc2_4',
            'Loc2_5', 'Loc2_6', 'Loc3_1', 'Loc3_2', 'Loc4_1', 'Loc4_2', 'Loc4_3']
loc_to_idx = dict(zip((all_locs), xrange(len(all_locs))))


for i in range(len(all_locs)):
    mot_raw_res = np.genfromtxt(os.path.join(root_dir, all_locs[i] + '.mp4-res.txt'), delimiter=',')
    mot_raw_res = mot_raw_res[np.where(mot_raw_res[:, -3]==3)[0]][:, :-4]
    area = mot_raw_res[:, -1] * mot_raw_res[:, -2]

    for t in thresh:
        mot_filtered_res = mot_raw_res[np.where(area > int(t))[0]]
        dir_path = os.path.join(save_root_dir, str(t))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        np.savetxt(os.path.join(dir_path, all_locs[i] + 'filtered_mot_res.txt'), mot_filtered_res.astype(int), fmt='%d')
        print all_locs[i], t, 'filtered, before:', mot_raw_res.shape, 'now:', mot_filtered_res.shape

print 'all done'

