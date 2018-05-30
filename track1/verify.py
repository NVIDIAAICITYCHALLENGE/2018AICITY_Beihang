import cv2
import os
import sys
from track1 import Det

intT = lambda x: [int(i) for i in x]

def IOU(x, y):
    rx1 = max(x.x1, y.x1)
    rx2 = min(x.x2, y.x2)
    ry1 = max(x.y1, y.y1)
    ry2 = min(x.y2, y.y2)
    if ry2>ry1 and rx2>rx1:
        i = (ry2-ry1)*(rx2-rx1)
        u = x.area()+y.area()-i
        return float(i)/u
    else: return 0.0

def loadAns(txt, ind):
    res = {}
    with open(txt+'/'+'track1.txt') as fd:
        rows = fd.readlines()
        for row in rows:
            row = row.split(' ')
            if int(row[0])!=ind: continue
            fr = int(row[1])
            x1, y1, x2, y2 = intT(row[3:7])
            sp = float(row[7])
            if fr not in res:
                res[fr] = []
            D = Det(x1, y1, x2, y2)
            D.sp = sp
            res[fr].append(D)
    return res

def paint(im, dts, base, typ):
    for dt in dts:
        sp = dt.sp
        sp = abs(sp)
        l = int(dt.x1)
        r = int(dt.x2)
        t = int(dt.y1)
        b = int(dt.y2)
        color = (255,199,199)
        cv2.rectangle(im, (l,t), (r,b), color, 1)
        d = 0
        if typ!='one':
            d = 40
            color = (255,199,0)
        cv2.putText(im, 'km %.2f'%(sp/0.6213711), (r+3,t+d), cv2.FONT_HERSHEY_DUPLEX, 0.5, color)
        cv2.putText(im, '%s %.2f'%(typ, sp), (r+3,t+d+16), cv2.FONT_HERSHEY_DUPLEX, 0.5, color)

if __name__=='__main__':
    root = './trk1vids'
    # psfile = './LOCF2.txt'
    # trkroot = './trk1out/out'
    vids = sorted(os.listdir(root))
    ind = int(sys.argv[1])-1
    seq = vids[ind]
    one = loadAns(sys.argv[2], ind+1)
    two = loadAns(sys.argv[3], ind+1)
    print len(one), len(two)
    vi = cv2.VideoCapture(root+'/'+seq)

    fps = vi.get(cv2.cv.CV_CAP_PROP_FPS)
    base = 3.6 * fps
    cnt = int(vi.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    w, h = int(vi.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(vi.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    print 'fps', fps, 'w', w, 'h', h, 'cnt', cnt
    vi.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
    data = {}
    d1 = {}
    d2 = {}
    P = [[], []]
    Q = [[], []]
    for fi in xrange(cnt):
        s, im = vi.read()
        if not s or im is None: break
        # if fi+1 in one: paint(im, one[fi+1], base, 'one')
        # if fi+1 in two: paint(im, two[fi+1], base, sys.argv[3])

        # cv2.imshow('demo', im)
        # cv2.waitKey(0)
        if fi+1 in one and fi+1 in two:
            for it in one[fi+1]:
                diff = float('%.1f'%(it.sp))
                if diff not in d1:
                    d1[diff] = 0
                d1[diff] += 1
            for it in two[fi+1]:
                diff = float('%.1f'%(it.sp))
                if diff not in d2:
                    d2[diff] = 0
                d2[diff] += 1
        if fi+1 in one and fi+1 in two:
            for it in one[fi+1]:
                mx = 0.
                diff = None
                for o in two[fi+1]:
                    iou = IOU(it, o)
                    if iou>mx:
                        mx = iou
                        diff = float('%.1f'%(it.sp - o.sp))
                if mx>0.:
                    if diff not in data:
                        data[diff] = 0
                    data[diff] += 1
    X = []
    Y = []
    for i in xrange(-500, 501):
        d = float('%.1f'%(float(i)/10))
        X.append(d)
        if d not in data:
            Y.append(0)
        else:
            Y.append(data[d])
    for i in xrange(0, 1501):
        d = float('%.1f'%(float(i)/10))
        P[0].append(d)
        if d not in d1:
            Q[0].append(0)
        else:
            Q[0].append(d1[d])
        P[1].append(d)
        if d not in d2:
            Q[1].append(0)
        else:
            Q[1].append(d2[d])
    from matplotlib import pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(X,Y)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(P[0],Q[0], color='red')
    ax.plot(P[1],Q[1], color='blue')
    plt.show()
    vi.release()
