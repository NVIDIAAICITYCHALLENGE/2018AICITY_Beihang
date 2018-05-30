import numpy as np
import  os
import cPickle as pkl

fea_dir = 'home_directory/VIC/track3/features'

for file in os.listdir(fea_dir):
    if 'ave' in file:
        with open(os.path.join(fea_dir, file), 'r') as f:
            cache = pkl.load(f)
        print file, 'has', len(cache.keys()), 'trackids'

print 'done'





