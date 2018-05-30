import caffe
import cv2
import google.protobuf as pb2
import google.protobuf.text_format
import numpy as np
import sys
import cPickle as pkl
import os

proto = 'xtnet192_deploy.prototxt'
weights = 'xt_veri+box+vid+compcars_bl_0.1_125kit+_iter_80000.caffemodel'
pic_root_dir = 'home_directory/VIC/VeRi' #'show/0/0002_c004_00084270_0.jpg'
data_file = os.path.join(pic_root_dir, 'name_' + sys.argv[1] + '.txt')
image_dir = os.path.join(pic_root_dir, 'image_' + sys.argv[1])

# change the features file path to your own
save_dir_path = sys.argv[2]
save_file = os.path.join(save_dir_path, sys.argv[1] + '.pkl')


caffe.mpi_init()
caffe.set_mode_gpu()
caffe.set_device(0)

net = caffe.Net(proto, weights, caffe.TEST)
print 'model loaded'

def im_preprocess(pic_file):
    if not os.path.isfile(pic_file):
        print pic_file, 'not exist!'
        exit(-1)
    im = cv2.imread(pic_file)
    im = cv2.resize(im, (192,192), interpolation=cv2.INTER_LINEAR)
    im = im - np.array([[[104, 117, 123]]])
    img_blob = np.array([im], dtype=np.float32)
    img_blob = img_blob.transpose((0, 3, 1, 2))
    return img_blob


with open(data_file, 'r') as f:
    lines = f.readlines()

res_lst = []
for i in range(len(lines)):
    img_blob = im_preprocess(os.path.join(image_dir, lines[i].strip()))
    net.blobs['data'].reshape(*(img_blob.shape))
    res = net.forward(data=img_blob)
    print 'forward success!'
    feature = net.blobs['fc7'].data.copy()
    res_lst.append(feature)
    print i, '/', len(lines), 'finished'
    # print 'feature: ', feature
    # print 'shape is', feature.shape

with open(save_file, 'wb', pkl.HIGHEST_PROTOCOL) as f:
    pkl.dump(res_lst, f)
    print sys.argv[1], 'cache saved'

caffe.mpi_fin()
print 'done'
