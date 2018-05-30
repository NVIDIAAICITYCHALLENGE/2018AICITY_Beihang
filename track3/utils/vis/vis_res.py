import numpy as np
import os 
import sys
import cv2

# tracks = np.loadtxt('home_directory/VIC/track3/filters_distance/track_res_idx.txt', dtype=str)
# print 'tracklets shape', tracks.shape

# thresh = sys.argv[1]

with open('home_directory/VIC/track3/new/tracklets/track_res_idx_v5_1_0.4_nodate.txt', 'r') as f:
# with open('home_directory/VIC/track3/tracklets/track_res_idx_v4_' + sys.argv[1] + '.txt', 'r') as f:
    lines = f.readlines()
tracks = []
for l in lines:
    lst = l.strip().split()
    tracks.append(lst)


video_dir = '/mnt/lustre/share/aicitychallenge/track3'
raw_dets_dir = os.path.join(video_dir, 'dets')
vis_dir = 'home_directory/VIC/track3/tracklets/vis/v4'
if not os.path.exists(vis_dir):
    os.makedirs(vis_dir)

def vis(im, x, y, w, h, im_write_name):
    im = im[y:y+h, x:x+w]
    cv2.imwrite(im_write_name, im)

# for i in range(tracks.shape[0]):
# 	for j in range(tracks.shape[1]):
# 		loc = tracks[i, j][:6]
# 		tid = int(tracks[i, j][7:])
for i in range(len(tracks)):
    for j in range(len(tracks[i])):
        loc = tracks[i][j][:6]
        tid = int(tracks[i][j][7:])
        raw_det_file = os.path.join(raw_dets_dir, loc + '.mp4-res.txt')
        assert os.path.isfile(raw_det_file)
        raw_dets = np.genfromtxt(raw_det_file, delimiter=',')
        raw_dets_t = raw_dets[np.where(raw_dets[:, 1] == tid)[0]][:, :-4]
        video_name = os.path.join(video_dir, loc + '.mp4')
        assert os.path.isfile(video_name)
        cap = cv2.VideoCapture(video_name)
        if not cap.isOpened():
            print video_name, 'cannot open!'
            exit(-1)
        # if raw_dets_t.shape[0] > 50:
        #     T = 50
        # else:
        T = raw_dets_t.shape[0]
        vis_cnt = 0
        for t in range(T): #raw_dets_t.shape[0]):
            # if t > 10:
            #     break
            x, y, w, h = raw_dets_t[t, 2:]
            x, y, w, h = int(x), int(y), int(w), int(h)
            if w * h < 6000:
                continue
            cap.set(1, int(raw_dets_t[t, 0]))
            flag, frame = cap.read()

            while not flag:
                print 'read', tracks[i][j], 'failed!'
                flag, frame = cap.read()

            dir_name = os.path.join(vis_dir, str(i))
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            sub_dir_name = os.path.join(dir_name, '%03d' % j)
            if not os.path.exists(sub_dir_name):
                os.makedirs(sub_dir_name)
            vis(frame, x, y, w, h, os.path.join(sub_dir_name, loc + '_%06d.jpg' % t))
            vis_cnt += 1
            if vis_cnt > 100:
                break

    print i, 'finished'

print 'done'






