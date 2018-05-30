import numpy as np
import os
import sys
import cv2
import cPickle as pkl
import caffe
import google.protobuf as pb2
import google.protobuf.text_format
import cPickle as pkl

src_root_dir = '/mnt/lustre/share/aicitychallenge/track3/'
src_dets_root_dir = 'home_directory/VIC/track3/new_20000/filtered_mot_res/15000'
save_root_dir = 'home_directory/VIC/track3/new_20000/filtered_mot_features'
camera_id = int(sys.argv[1])
split_id = int(sys.argv[2])

video_name = 'Loc' + str(camera_id) + '_' + str(split_id)


proto = 'xtnet192_deploy.prototxt'
weights = 'xt_veri+box+vid+compcars_bl_0.1_125kit+_iter_80000.caffemodel'

caffe.mpi_init()
caffe.set_mode_gpu()
caffe.set_device(0)

net = caffe.Net(proto, weights, caffe.TEST)
print 'model loaded'

def deploy(im_lst):
    im_num = len(im_lst)
    net.blobs['data'].reshape(im_num, 3, 192, 192)
    for i in range(im_num):
        im = im_lst[i]
        im = cv2.resize(im, (192, 192), interpolation=cv2.INTER_LINEAR)
        im = im.astype(np.float32)
        im = im - np.array([[[104, 117, 123]]])  # + np.finfo(float).eps

        net.blobs['data'].data[i] = im.transpose((2, 0, 1))
    # img_blob = np.array([im], dtype=np.float32)
    # img_blob = img_blob.transpose((0, 3, 1, 2))
    # net.blobs['data'].reshape(*(img_blob.shape))

    net.forward() # data=img_blob)
    features = net.blobs['fc7'].data.copy()
    return features



file_name = video_name + 'filtered_mot_res.txt'
file_path = os.path.join(src_dets_root_dir, file_name)
if not os.path.isfile(file_path):
    print file_path, 'not exist!'
    exit(-1)
dets = np.genfromtxt(file_path) #, delimiter=',')
# dets = dets[np.where(dets[:, -3] == 3.0)[0]]
# dets = dets[:, :6]

video_path = os.path.join(src_root_dir, video_name + '.mp4')
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print video_path, 'cannot open!'
    exit(-1)

save_file = os.path.join(save_root_dir, video_name + '.pkl')

tids = np.unique(dets[:, 1])
print video_name, 'has', len(tids), 'track ids'
res = {}
for t in tids:
    res[int(t)] = [0, 0, []]

frame_num = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
for fid in range(1, frame_num + 1):
    flag, frame = cap.read()
    # while not flag:
    #     print 'read', fid, 'frame failed!, retrying...'
    #     #exit(-1)
    #     #flag, frame = cap.read()
    #     #break
    if not flag:
        break

    fid_idx = np.where(dets[:, 0]==fid)[0]
    if len(fid_idx) == 0:
        continue
    dets_fid = dets[fid_idx]

    im_lst = []
    for i in range(dets_fid.shape[0]):
        t, x, y, w, h = dets_fid[i, 1:]
        t, x, y, w, h = int(t), int(x), int(y), int(w), int(h)

        im = frame[y:y+h, x:x+w]

        # cv2.imwrite('ttt/' + str(fid) + '.jpg', frame)
        im_lst.append(im)
    assert len(im_lst) > 0
    feas = deploy(im_lst)
    #print 'features got, shape is', feas.shape
    for i in range(dets_fid.shape[0]):
        t = int(dets_fid[i, 1])
        # cv2.imwrite('tmp/' + str(fid) + '.jpg', im)

        if res[t][0] == 0:
            res[t][0] = fid
        if res[t][1] < fid:
            res[t][1] = fid
        res[t][2].append(feas[i])
        # print feas[i]

    print fid, '/', frame_num, 'finished'

with open(save_file, 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(res, f)
    print video_name, 'all features saved'

print 'deploy finished, starting to average feature'



cache_file = os.path.join(save_root_dir, video_name+'.pkl')
assert os.path.isfile(cache_file)
with open(cache_file, 'r') as f:
    res = pkl.load(f)
print 'cache loaded'
keys = res.keys()
cnt = 0
for t in keys: #tids:
    fea_arr = np.array(res[int(t)][2])
    ave_fea = np.sum(fea_arr, axis=0)
    print t
    ave_fea /= float(len(ave_fea))

    '''
    num_fea = fea_arr.shape[0]
    each = int(num_fea / 4)
    ave_fea = []
    for i in range(4):
        sid = each * i
        eid = each * (i + 1)
        if i == 3:
            eid = num_fea - 1
        tmp = np.sum(fea_arr[sid:eid], axis=0)
        tmp /= float(len(tmp))
        ave_fea.append(tmp)
    '''
    res[t][2] = ave_fea
    cnt += 1
    print cnt, '/', len(keys), 'finished'

mean_feature_dir = 'home_directory/VIC/track3/new_20000/filtered_mot_mean_features'
if not os.path.exists(mean_feature_dir):
    os.makedirs(mean_feature_dir)
ave_save_file = os.path.join(mean_feature_dir, 'Loc' + str(camera_id) + '_' + str(split_id) + '_ave_1.pkl')
with open(ave_save_file, 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(res, f)

# caffe.mpi_fin()
print 'done'













