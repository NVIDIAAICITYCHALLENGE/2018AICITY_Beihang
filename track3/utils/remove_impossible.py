import numpy as np
import os

res_file = 'home_directory/VIC/track3/new/tracklets/track_res_idx_v5_1_0.4_nodate.txt'

with open(res_file, 'r') as f:
    lines = f.readlines()

assert len(lines) == 100

remove_id = [11, 14, 18, 23, 48, 60, 69, 74, 79, 85, 89, 99, 33, 32,93, 66, 35, 43, 40, 52, 34, 87, 57, 45]
# remove_id = [14, 18, 60, 74, 85]

with open('home_directory/VIC/track3/new/tracklets/track_res_idx_v5_1_0.4_nodate_slightly_removed_impossible_less.txt', 'w') as f:
    for i in range(len(lines)):
        if i in remove_id:
            continue
        f.write(lines[i])
print 'done'
