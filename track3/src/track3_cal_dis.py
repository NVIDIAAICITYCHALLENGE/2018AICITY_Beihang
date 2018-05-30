import scipy.spatial.distance as distance
import numpy as np
import cPickle as pkl
import os
import sys

root_dir = 'home_directory/VIC/track3/new_15000'
fea_dir = os.path.join(root_dir, 'filtered_mot_mean_features')
dis_dir = os.path.join(root_dir, 'filtered_mot_distances')
# if not os.path.exists(fea_dir):
#     os.makedirs(fea_dir)
# if not os.path.exists(dis_dir):
#     os.makedirs(dis_dir)

'''
cache_files = ['Loc1_1_ave_1.pkl',
               'Loc1_2_ave_1.pkl',
               'Loc1_3_ave_1.pkl',
               'Loc1_4_ave_1.pkl',
               'Loc2_1_ave_1.pkl',
               'Loc2_2_ave_1.pkl',
               'Loc2_3_ave_1.pkl',
               'Loc2_4_ave_1.pkl',
               'Loc2_5_ave_1.pkl',
               'Loc2_6_ave_1.pkl',
               'Loc3_1_ave_1.pkl',
               'Loc3_2_ave_1.pkl',
               'Loc4_1_ave_1.pkl',
               'Loc4_3_ave_1.pkl',
               'Loc4_2_ave_1.pkl']

# concat all cache
all_fea_lst = []
all_idx_lst = []
for i in cache_files:
    cache_f = os.path.join(fea_dir, i)
    with open(cache_f, 'r') as f:
        cache = pkl.load(f)

    for k, v in cache.iteritems():
        all_idx_lst.append(i[:7] + str(k))
        all_fea_lst.append(v[2])
    print i, 'concat finished'
print 'concat done!'

# all_lst = [all_idx_lst, np.array(all_fea_lst)]

with open(os.path.join(fea_dir, 'all_fea.pkl'), 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(all_fea_lst, f)
with open(os.path.join(fea_dir, 'all_idx.pkl'), 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(all_idx_lst, f)

print 'all ave fea dump finished!'


# with open(os.path.join(fea_dir, 'all_ave.pkl'), 'r') as f:
#     all_lst = pkl.load(f)
#
# print 'cache loaded'
#
#
# # split cache
# all_fea_arr = all_lst[1]


# with open('home_directory/VIC/track3/filtered_mot_mean_features/all_fea.pkl', 'r') as f:
#     all_fea_lst = pkl.load(f)
#
all_fea_arr = np.array(all_fea_lst)

num = len(all_fea_arr)
split_num = 50
each = num / split_num
for i in range(split_num):
    sid = each * i
    eid = each * (i + 1)
    if i == split_num - 1:
        eid = num

    fea_arr_each = all_fea_arr[sid:eid]
    all_ave_split_path = os.path.join(fea_dir, 'all_ave_split')
    if not os.path.exists(all_ave_split_path):
        os.makedirs(all_ave_split_path)
    with open(os.path.join(all_ave_split_path, str(i)+'.pkl'), 'wb', pkl.HIGHEST_PROTOCOL) as f:
        pkl.dump(fea_arr_each, f)
    print i, 'split finished'
print 'all split finished'
exit(0)
'''

'''
with open(os.path.join(fea_dir, 'all_fea.pkl'), 'r') as f:
    all_fea_lst = pkl.load(f)

all_fea_arr = np.array(all_fea_lst)

# calcualte distance
all_ave_split_path = os.path.join(fea_dir, 'all_ave_split')
if not os.path.exists(all_ave_split_path):
    os.makedirs(all_ave_split_path)
with open(os.path.join(all_ave_split_path, sys.argv[1]+'.pkl'), 'r') as f:
    split_arr = pkl.load(f)
all_res = distance.cdist(split_arr, all_fea_arr, 'cosine')

with open(os.path.join(dis_dir, 'dis_' + sys.argv[1] + '.pkl'), 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(all_res, f)

print 'split', sys.argv[1], 'done!'
exit(0)
'''

'''
# concat all splited distance
split_num = 50
with open(os.path.join(dis_dir, 'dis_0.pkl'), 'r') as f:
    res = pkl.load(f)
print '0 /', split_num, 'cancat finished'

for i in range(1, split_num):
    with open(os.path.join(dis_dir, 'dis_' + str(i) + '.pkl'), 'r') as f:
        split_cache = pkl.load(f)
    res = np.concatenate((res, split_cache), axis=0)
    print i, '/', split_num, 'cancat finished'

print 'all concat finished, shape is', res.shape

with open(os.path.join(dis_dir, 'dis_all.pkl'), 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(res, f)

print 'concat done!'
'''

'''
# # calcute distance marix
# with open('home_directory/VIC/track3/filtered_mot_mean_features/all_fea.pkl', 'r') as f:
#     all_fea = pkl.load(f)
# with open('home_directory/VIC/track3/filtered_mot_mean_features/all_idx.pkl', 'r') as f:
#     all_idx = pkl.load(f)
# 
# all_dis = distance.cdist(all_fea, all_fea, 'cosine')
# with open('home_directory/VIC/track3/filtered_mot_distances/dis_all.pkl', 'wb', pkl.HIGHEST_PROTOCOL) as f:
#     pkl.dump(all_dis, f)
# print 'all dis calculate finished'
# split_cache = all_dis
'''

# filter the distance matrix with max_num=15 and threshould sys.argv[1]
split_num = int(sys.argv[1])
# # thresh = 0.3 # int(sys.argv[1])
#
res = []
cache_name = 'dis_' + str(split_num) + '.pkl'
# load each split cache
with open(os.path.join(dis_dir, cache_name), 'r') as f:
    split_cache = pkl.load(f)

# load index cache
with open(os.path.join(fea_dir, 'all_idx.pkl'), 'r') as f:
    all_idx = pkl.load(f)

print split_num, 'loaded cache'

all_locs = ['Loc1_1', 'Loc1_2', 'Loc1_3', 'Loc1_4', 'Loc2_1', 'Loc2_2', 'Loc2_3', 'Loc2_4',
            'Loc2_5', 'Loc2_6', 'Loc3_1', 'Loc3_2', 'Loc4_1', 'Loc4_2', 'Loc4_3']
loc_to_idx = dict(zip((all_locs), xrange(len(all_locs))))

res_inds = []
res_diss = []

each_split_num = len(all_idx) / 50

for idx in range(split_cache.shape[0]):
    each = split_cache[idx]
    this_loc = all_idx[idx + split_num * each_split_num][:6]
    # this_loc_idxs = [t_i for t_i in range(len(all_idx)) if all_idx[t_i][:6] == this_loc]
    # other_loc_idx = list(set(range(len(all_idx))) - set(this_loc_idxs))
    # each = each[other_loc_idx]

    each_ind = []
    each_dis = []
    for loc in all_locs:
        if loc == this_loc:
            continue

        loc_idxs = [t_i for t_i in range(len(all_idx)) if all_idx[t_i][:6] == loc]
        ii = np.argsort(each[loc_idxs])[:4]
        each_ind += list(np.array(loc_idxs)[ii])
        # each_ind += list(np.argsort(each[loc_idxs])[:4] + loc_idxs[0])
        each_dis += list(np.sort(each[loc_idxs])[:4])# list(each[np.array(loc_idxs)[ii]]) # list(np.sort(each[loc_idxs])[:4])
        # print list(each[np.array(loc_idxs)[ii]])
        # print list(np.sort(each[loc_idxs])[:4])
    res_inds.append(each_ind)
    res_diss.append(each_dis)

filtered_dis_dir = os.path.join(root_dir, 'filtered_mot_final_distance')

# with open(os.path.join(filtered_dis_dir, 'diss.pkl'), 'wb', pkl.HIGHEST_PROTOCOL) as f:
#     pkl.dump(res_diss, f)
# with open(os.path.join(filtered_dis_dir, 'inds.pkl'), 'wb', pkl.HIGHEST_PROTOCOL) as f:
#     pkl.dump(res_inds, f)

with open(os.path.join(filtered_dis_dir, 'diss/filtered_' + cache_name), 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(res_diss, f)
with open(os.path.join(filtered_dis_dir, 'inds/filtered_idx_' + str(split_num) + '.pkl'), 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(res_inds, f)

print split_num, 'done'




'''
filtered_dis_dir = os.path.join(root_dir, 'filtered_mot_final_distance/diss')

# concat all filterd cache
all_split_num = 50
all_res = []
for i in range(all_split_num):
    with open(os.path.join(filtered_dis_dir, 'filtered_dis_' + str(i) + '.pkl'), 'r') as f:
        split_cache = pkl.load(f)
    all_res += split_cache
    print i, 'loaded'

with open(os.path.join(filtered_dis_dir, 'all_dis.pkl'), 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(all_res, f)

print 'dis done'

filtered_idx_dir = os.path.join(root_dir, 'filtered_mot_final_distance/inds')
all_res = []
for i in range(all_split_num):
    with open(os.path.join(filtered_idx_dir, 'filtered_idx_' + str(i) + '.pkl'), 'r') as f:
        split_cache = pkl.load(f)
    all_res += split_cache
    print i, 'loaded'

with open(os.path.join(filtered_idx_dir, 'all_inx.pkl'), 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(all_res, f)

print 'done'
'''





