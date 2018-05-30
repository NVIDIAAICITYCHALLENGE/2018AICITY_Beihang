import numpy as np
import os
import sys

root_dir = 'home_directory/VIC/track3/new_15000/tracklets'
raw_dir = '/mnt/lustre/share/aicitychallenge/track3/dets'

submits_dir = os.path.join(root_dir, 'submit_v5_1_0.4_nodate')
if not os.path.exists(submits_dir):
    os.makedirs(submits_dir)

track3_submit_dir = os.path.join(root_dir, 'track3_submit_v5_1_0.4_nodate')
if not os.path.exists(track3_submit_dir):
    os.makedirs(track3_submit_dir)  


with open(os.path.join(root_dir, 'track_res_idx_v5_1_0.4_nodate_improved.txt'), 'r') as f:
    lines = f.readlines()

res_num = len(lines)

'''

# split res
# roi_num = 100
# total_num = len(lines)
# if roi_num < total_num:
#     lines = lines[:100]



for i in range(len(lines)):#roi_num):
    with open(os.path.join(submits_dir, str(i)+'.txt'), 'w') as f:
        f.write(lines[i])

print 'split done'
exit(0)
'''

'''
obj_id = int(sys.argv[1])

with open(os.path.join(submits_dir, str(obj_id)+'.txt'), 'r') as f:
    lines = f.readlines()

track_res = [x.strip().split() for x in lines]

print 'track res loaded'

all_locs = ['Loc1_1', 'Loc1_2', 'Loc1_3', 'Loc1_4', 'Loc2_1', 'Loc2_2', 'Loc2_3', 'Loc2_4',
            'Loc2_5', 'Loc2_6', 'Loc3_1', 'Loc3_2', 'Loc4_1', 'Loc4_2', 'Loc4_3']
loc_to_idx = dict(zip((all_locs), xrange(len(all_locs))))




speed = -1
conf = 1
with open(os.path.join(track3_submit_dir, str(obj_id)+'.txt'), 'w') as f:
    for i in range(len(track_res)):
        # obj_id =  #i + 1
        for j in range(len(track_res[i])):
            flag = 0
            if track_res[i][j][0] == 'd':
                loc = track_res[i][j][2:8]
                tid = int(track_res[i][j][9:])
                flag = 1
            else:
                loc = track_res[i][j][:6]
                tid = int(track_res[i][j][7:])
            video_id = loc_to_idx[loc] + 1
            # tid = int(track_res[i][j][7:])
            raw_dets_file = os.path.join(raw_dir, loc + '.mp4-res.txt')
            raw_dets = np.genfromtxt(raw_dets_file, delimiter=',')
            idxs = np.where(raw_dets[:,1]==tid)[0]
            dets = raw_dets[idxs]
            for ii in range(len(idxs)):
                frame_id = int(dets[ii, 0])
                xmin = int(dets[ii, 2])
                ymin = int(dets[ii, 3])
                w = int(dets[ii, 4])
                h = int(dets[ii, 5])
                if w * h < 1000:
                    continue
                xmax = int(xmin + dets[ii, 4] - 1)
                ymax = int(ymin + dets[ii, 5] - 1)
                wrt_str = ' '.join((str(video_id), str(frame_id), str(obj_id+1), str(xmin), str(ymin), str(xmax), str(ymax), str(speed), str(conf)))
                f.write(wrt_str+'\n')
                f.flush()
                if flag == 1:
                    break
        print i, 'finished'
        # if i >= 99:
        #     break

print 'done'

exit(0)
'''


# merge res 'r

all_res = []
for i in range(res_num):
    with open(os.path.join(track3_submit_dir, str(i)+'.txt'), 'r') as f:
        lines = f.readlines()
    all_res += lines

with open(os.path.join(track3_submit_dir, 'all.txt'), 'w') as f:
    f.writelines(all_res)
print 'done'


'''
org = np.loadtxt(os.path.join(root_dir, 'track3_submit_splits', 'all.txt'), dtype=int)
org[:, 2] += 1
np.savetxt(os.path.join(root_dir, 'track3_submit_splits', 'all_final.txt'), org.astype(int), fmt='%d')

print 'done'
'''

