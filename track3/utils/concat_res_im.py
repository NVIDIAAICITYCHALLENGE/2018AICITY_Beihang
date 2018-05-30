import numpy as np
import cv2
import sys
import os

version_num = 'v5_1_0.4_nodate' #sys.argv[1]
root_path = 'home_directory/VIC/track3/new/tracklets/vis/' + version_num
save_path = 'home_directory/VIC/track3/new/tracklets/vis/' + version_num + '_all'
if not os.path.exists(save_path):
    os.makedirs(save_path)

show_num = 10

for d in sorted(os.listdir(root_path), key=lambda x: (int(x), x)):
    # save_dir_path = os.path.join(save_path, d)
    # if not os.path.exists(save_dir_path):
    #     os.makedirs(save_dir_path)
    dir_path = os.path.join(root_path, d)
    all_ims = []
    max_h = 0
    max_w = 0
    for subd in sorted(os.listdir(dir_path), key=lambda x: (int(x), x)):
        # print subd,
        sub_dir_path = os.path.join(dir_path, subd)
        im_lst = sorted(os.listdir(sub_dir_path), key=lambda x: (int(x[7:-4]), x))
        # print im_lst, '\n'
        im_num = len(im_lst)
        each = im_num / show_num

        select_ims = []
        for i in range(show_num):
            im = cv2.imread(os.path.join(sub_dir_path, im_lst[each * i]))
            h, w = im.shape[:2]
            if h > max_h:
                max_h = h
            if w > max_w:
                max_w = w
            select_ims.append(im)

        all_ims.append(select_ims)

    for i in range(len(all_ims)):
        for j in range(len(all_ims[i])):
            all_ims[i][j] = cv2.resize(all_ims[i][j], (max_h, max_h))

    im_cols = []
    for i in range(len(all_ims)):
        im_row = all_ims[i][0]
        for j in range(1, len(all_ims[i])):
            im_row = np.concatenate((im_row, all_ims[i][j]), axis=1)
        im_cols.append(im_row)

    im_all = im_cols[0]
    for i in range(1, len(im_cols)):
        im_all = np.concatenate((im_all, im_cols[i]), axis=0)
    # cv2.imwrite(os.path.join(save_dir_path, 'all.jpg'), im_all)
    cv2.imwrite(os.path.join(save_path, d + '.jpg'), im_all)

    print d, 'done'

print 'all done'



