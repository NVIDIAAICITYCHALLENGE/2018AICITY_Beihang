import numpy as np
import os
import sys

res_file = 'home_directory/VIC/track3/new/tracklets/track3_submit_v5_1_0.4_nodate_removed_impossible/all.txt'

res = np.genfromtxt(res_file)

xmin = res[:, 3]
ymin = res[:, 4]
xmax = res[:, 5]
ymax = res[:, 6]

ws = xmax - xmin + 1
hs = ymax - ymin + 1
areas = ws * hs
idxs = np.where(areas > 1000)[0]

res = res[idxs]

np.savetxt('home_directory/VIC/track3/new/tracklets/track3_submit_v5_1_0.4_nodate_removed_impossible/all_filtered.txt', res.astype(int), fmt='%d')


