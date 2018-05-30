import numpy as np
import os
import sys
import cv2

# tracks = np.loadtxt('home_directory/VIC/track3/filters_distance/track_res_idx.txt', dtype=str)
# print 'tracklets shape', tracks.shape

# thresh = sys.argv[1]

#with open('home_directory/VIC/track3/tracklets/track_res_idx_' + thresh + '.txt', 'r') as f:
with open('home_directory/VIC/track3/tracklets/track_res_idx_v4_' + sys.argv[1] + '.txt', 'r') as f:
    lines = f.readlines()
tracks = []
for l in lines:
    lst = l.strip().split()
    tracks.append(lst)


video_dir = '/mnt/lustre/share/aicitychallenge/track3'
raw_dets_dir = os.path.join(video_dir, 'dets')
vis_dir = 'home_directory/VIC/track3/tracklets/vis/finetune_v2/'
if not os.path.exists(vis_dir):
    os.makedirs(vis_dir)

def vis(im, x, y, w, h, im_write_name):
    im = im[y:y+h, x:x+w]
    cv2.imwrite(im_write_name, im)

with open(os.path.join(vis_dir, track_res_finetune_v2.txt), 'r')  as f:
    lines = f.readlines()

tracks = [x.split().strip() for x in lines]

for i in range(len(tracks)):
    all_res = []
    max_h = 0
    max_w = 0
    for j in range(len(tracks[i])):
        loc = tracks[i][j][:6]
        tid = int(tracks[i][j][7:])
        raw_det_file = os.path.join(raw_dets_dir, loc + '.mp4-res.txt')
        assert os.path.isfile(raw_det_file)
        raw_dets = np.genfromtxt(raw_det_file, delimiter=',')
        raw_dets_t = raw_dets[np.where(raw_dets[:, 1] == tid)[0]][:, :-4]

        ws = raw_dets_t[:, -2]
        hs = raw_dets_t[:, -1]
        areas = ws * hs
        mid = np.argsort(areas)
        p1, p2, p3, p4 = mid - 2, mid, mid + 2, mid + 4
        if mid + 4 > len(areas) - 1:
            if mid + 2 > len(areas) - 1:
                p1, p2, p3, p4 = mid - 6, mid - 4, mid - 2
            else:
                p1, p2, p3, p4 = mid - 2, mid, mid + 2, mid + 4
        if mid - 4 < 0:
            if mid - 2 < 0:
                p1, p2, p3, p4 = mid, mid + 2, mid + 4, mid + 6
            else:
                p1, p2, p3, p4 = mid - 2, mid, mid + 2, mid + 4

        video_name = os.path.join(video_dir, loc + '.mp4')
        assert os.path.isfile(video_name)
        cap = cv2.VideoCapture(video_name)
        if not cap.isOpened():
            print video_name, 'cannot open!'
            exit(-1)

        res_im = []
        for t in [p1, p2, p3, p4]:
            x, y, w, h = raw_dets_t[t, 2:]
            x, y, w, h = int(x), int(y), int(w), int(h)
            cap.set(1, int(raw_dets_t[t, 0]))
            flag, frame = cap.read()

            while not flag:
                print 'read', tracks[i][j], 'failed!'
                cv2.waitKey(1000)
                flag, frame = cap.read()

            res_im.append(frame[y:y+h, x:x+w])

        h = max([x.shape[0] for x in res_im])
        if h > max_h:
            max_h = h
        w = max([x.shape[1] for x in res_im])
        if w > max_w:
            max_w = w
        # res_im = [cv2.resize(im, (h, w)) for im in res_im]
        # cat_im = res_im[0]
        # for im_i in range(1, len(res_im)):
        #     cat_im = np.concatenate((cat_im, res_im[im_i]), axis=1)
        #vis(frame, x, y, w, h, os.path.join(sub_dir_name, loc + '_%06d.jpg' % t))
        all_res.append(res_im)
    for im_i in range(len(all_res)):
        each_lst = [cv2.resize(im, (max_h, max_w)) for im in res_im[im_i]]



    print i, 'finished'

print 'done'






