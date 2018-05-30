import numpy as np
from random import shuffle
import os

root_dir = 'home_directory/VIC/track3/new'

with open(os.path.join(root_dir, 'tracklets/track_res_idx_v5_1_0.4.txt'), 'r') as f:
    lines = f.readlines()

# shuffle(lines)
lines = lines[:100]

with open(os.path.join(root_dir, 'tracklets/track_res_idx_v5_1_0.4_ran-100.txt'), 'w') as f:
    f.writelines(lines)

print 'done'
