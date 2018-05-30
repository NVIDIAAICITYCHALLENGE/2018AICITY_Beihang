import numpy as np

res_file = 'home_directory/VIC/track3/tracklets/track3_submit_splits_v5_1_0.3/all.txt'

res = np.genfromtxt(res_file)
obj_ids = np.unique(res[:, 2])

# print 'all_id', obj_ids
#
# for id in obj_ids:
#     ii = np.where(res[:, 2] == id)[0]
#     # print 'ii', ii
#     res_id = res[ii]
#     res_id = res_id[:, :2]
#
#     # print 'shape: ', res_id.shape[0]
#     #
#     # for i in range(res_id.shape[0]):
#     #     for j in range(i+1, res_id.shape[0]):
#     #         if res_id[i,0] == res_id[j,0] and res_id[i, 1] == res_id[j, 1]:
#     #             print id, i, j, 'dup!'
#     #
#     # print id, 'finished'
#
#     res_id_uni = np.unique(res_id, axis=0)
#     if len(res_id) > len(res_id_uni):
#         print id, 'duplicate!'
res_id = res
for i in range(res.shape[0]):
    for j in range(i+1, res.shape[0]):
        if res_id[i,0] == res_id[j,0] and res_id[i, 1] == res_id[j, 1] and res_id[i,6] == res_id[j,6] and res_id[i,3] == res_id[j,3] and res_id[i,4] == res_id[j,4] and res_id[i,5] == res_id[j,5]:
            print id, i, j, 'dup!'

print 'done'


