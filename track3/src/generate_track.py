import scipy.spatial.distance as distance
import numpy as np
import cPickle as pkl
import os
import sys
import pdb


# load all idxs
with open('home_directory/VIC/track3/filtered_mot_mean_features/all_idx.pkl', 'r') as f:
    all_idxs = pkl.load(f)

with open('home_directory/VIC/track3/filtered_mot_mean_features/all_fea.pkl', 'r') as f:
    all_feats = pkl.load(f)

def is_all_camera(input):
    loc_ids = []
    for i in input:
        cid = int(all_idxs[int(i)][3])
        if cid not in loc_ids:
            loc_ids.append(cid)

    loc_ids.sort()
    if loc_ids == [1,2,3,4]:
        return True
    else:
        return False

datelist = [['Loc1_1','Loc1_2','Loc1_3','Loc2_1','Loc2_2','Loc2_3','Loc2_4'],['Loc1_4','Loc2_5','Loc2_6'],['Loc3_1','Loc3_2','Loc4_1','Loc4_2','Loc4_3']]

def is_all_date(input):
    # pdb.set_trace()
    date_ids = []
    for i in input:
        cid = all_idxs[int(i)][0:6]
        tmp = [tmp for tmp in datelist if cid in tmp][0]
        if datelist.index(tmp) not in date_ids:
        date_ids.append(datelist.index(tmp))
    date_ids.sort()
    if date_ids == [0,1,2]:
        return True
    else:
        return False


filtered_dis_dir = 'home_directory/VIC/track3/filtered_mot_final_distance/diss'

# concat all filterd cache
all_split_num = 50
all_res = []
for i in range(all_split_num):
    with open(os.path.join(filtered_dis_dir, 'filtered_dis_' + str(i) + '.pkl'), 'r') as f:
        split_cache = pkl.load(f)
    all_res += split_cache

HIT_dis = all_res
print 'HIT_dis loaded, len is', len(HIT_dis)


filtered_idx_dir = 'home_directory/VIC/track3/filtered_mot_final_distance/inds'
all_res = []
for i in range(all_split_num):
    with open(os.path.join(filtered_idx_dir, 'filtered_idx_' + str(i) + '.pkl'), 'r') as f:
        split_cache = pkl.load(f)
    all_res += split_cache
HIT_map = all_res
print 'HIT_map loaded, len is', len(HIT_map)


# root_dir = 'home_directory/VIC/track3/filters_distance/'
# with open(os.path.join(root_dir, 'inds/all_inx.pkl'), 'r') as f:
#     HIT_map = pkl.load(f)
#
#
# with open(os.path.join(root_dir, 'diss/all_dis.pkl'), 'r') as f:
#     HIT_dis = pkl.load(f)
# need the HIT_dis_cosine
print 'all data loaded'

trk_size = len(HIT_map) # 19W-by-14*4
video_num = 15
pair_dis_T = 0.3
trk_res = []

# for each row in HIT_map, calculate the conf score (smaller the better)
# conf score is the sum of reranking index * pair cosine dis of each top match pair
# each video select at most one track
HIT_map_filter = []
trajectory_conf = []
for i in range(trk_size):
    trajectory = []
    dis = 0
    for j in range(video_num - 1):
        pair_dis_min = 1000
        ind_min = -1
        pair_dis = 0.
        for k in range(4 * j, 4 * j + 4):

            if i in HIT_map[HIT_map[i][k]]:
                pair_dis = (k % 4 + 2 + HIT_map[HIT_map[i][k]].index(i) % 4) * HIT_dis[i][k]
            if pair_dis > 1e-8 and pair_dis < pair_dis_min:
                pair_dis_min = pair_dis
                ind_min = k

        if pair_dis_min < pair_dis_T:
            trajectory.append(HIT_map[i][ind_min])
            dis = dis + pair_dis_min
    if dis == 0 or len(trajectory) < 3:
        continue
    else:
        trajectory.append(i)
        if is_all_camera(trajectory) and is_all_date(trajectory):
            HIT_map_filter.append(trajectory) 
            #trajectory_conf.append(float(dis) / len(trajectory))
print len(HIT_map_filter)
#pdb.set_trace()

# within-group distance
for i in range(len(HIT_map_filter)):
    dis = 0
    for j in range(len(HIT_map_filter[i])):
        for k in range(len(HIT_map_filter[i])):
            ind1 = HIT_map_filter[i][j]
            ind2 = HIT_map_filter[i][k]
            dis = dis + distance.cosine(all_feats[ind1], all_feats[ind2])
    dis = dis/(len(HIT_map_filter[i])*(len(HIT_map_filter[i])-1))
    trajectory_conf.append(dis)

# sort the conf map, define the available track indicator to avoid
# the same track in different trajectories
trajectory_conf = np.array(trajectory_conf, dtype=np.float32)
HIT_dis_rank_ind = np.argsort(trajectory_conf)
trk_avaiable = [1]*trk_size
trk_cnt = 0

#pdb.set_trace()
# from the highest conf, find the trajectory. Two conditions: one is
# the avaiable ratio, another one is in different locations
for i in range(len(trajectory_conf)):
    ind = HIT_dis_rank_ind[i]
    cnt = 0
    for j in range(len(HIT_map_filter[ind])):
        if trk_avaiable[HIT_map_filter[ind][j]] == 1:
            cnt = cnt + 1
            #HIT_map[ind][j] = 0
    if (float(cnt))/len(HIT_map_filter[ind]) > 0.5: #0.5: #need another condition: trk in different videos
        trk_res.append(HIT_map_filter[ind])
        trk_cnt = trk_cnt + 1
        for k in range(len(HIT_map_filter[ind])):
            trk_avaiable[HIT_map_filter[ind][k]] = 0
    if trk_cnt >= 200:
        break
# print 'i is', i
# print 'track count is', len(trajectory_conf)

# # load idx
# with open('./all_idx.pkl', 'r') as f:
#     all_idxs = pkl.load(f)

with open('home_directory/VIC/track3/tracklets/track_res_idx_v5.txt', 'w') as f:
    for i in trk_res:
        for j in i:
            #f.write(str(j) + ' ')
            f.write(all_idxs[int(j)] + ' ')
        f.write('\n')

print 'done'
