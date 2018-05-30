import numpy as np
import os
import  sys

root_dir = 'home_directory/VIC/track3/new_15000/tracklets'

good_res_file = os.path.join(root_dir, 'track_res_idx_v5_1_0.4_nodate.txt')
bad_res_file = []
bad_res_file.append(os.path.join('home_directory/VIC/track3/new/tracklets', 'track_res_idx_v5_1_0.4_nodate.txt'))

with open(good_res_file, 'r') as f:
    lines = f.readlines()

assert len(lines) == 100
good_res = [x.strip().split() for x in lines]


bad_res = []
for i in range(1):

    with open(bad_res_file[i], 'r') as f:
        lines = f.readlines()

    assert len(lines) == 100

    remove_id = [11, 14, 18, 23, 48, 60, 69, 74, 79, 85, 89, 99]
    lines_d = []
    for id in remove_id:
        lines_d.append(lines[id])

    lines = lines_d

    for l in lines:
        bad_res += l.strip().split()

with open(os.path.join(root_dir, 'track_res_idx_v5_1_0.4_nodate_improved.txt'), 'w') as f:
    for i in range(len(good_res)):
        flag = 0
        for j in range(len(good_res[i])):
            if good_res[i][j] in bad_res:
                #good_res[i][j] = 'd_' + good_res[i][j]
                flag = 1
                break
        if flag == 0:
            for j in range(len(good_res[i])):
                f.write(good_res[i][j] + ' ')
            f.write('\n')

print 'done'









