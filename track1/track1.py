# -*- coding: utf8 -*-
from math import *
import random
import sys
import os
import numpy as np
import cv2
from Calibra import *
import json
import copy

class Det:
	CLASS_CNT = 3
	OBJECT_PEDESTRIAN = 1
	OBJECT_VEHICLE = 2
	OBJECT_OTHER = 3

	def __init__(self, x1=0., y1=0., x2=50., y2=50., cls=OBJECT_OTHER, conf=0.0):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.cls = cls
		self.conf = conf
		self.label = 0
	
	def __str__(self):
		return '[(%.2f,%.2f) (%.2f,%.2f)::%d(%.2f)]'%(self.x1,self.y1,self.x2,self.y2,self.cls,self.conf)

	def cx(self):
		return (self.x1+self.x2)/2

	def cy(self):
		return (self.y1+self.y2)/2

	def w(self):
		return self.x2-self.x1

	def h(self):
		return self.y2-self.y1

	def area(self):
		if (self.x2>self.x1) and (self.y2>self.y1):
			return (self.x2-self.x1)*(self.y2-self.y1)
		else: return 0.0

	def chk(self, sz):
		w, h = sz
		x1 = self.x1
		x2 = self.x2
		y1 = self.y1
		y2 = self.y2
		x1 = max(0., x1)
		x2 = min(w-1, x2)
		y1 = max(0., y1)
		y2 = min(h-1, y2)
		x1 = int(x1)
		x2 = int(x2)
		y1 = int(y1)
		y2 = int(y2)
		return x1+5<x2 and y1+5<y2

	def trim(self, sz, toInt = True):
		w, h = sz
		x1 = self.x1
		x2 = self.x2
		y1 = self.y1
		y2 = self.y2
		x1 = max(0., x1)
		x2 = min(w-1, x2)
		y1 = max(0., y1)
		y2 = min(h-1, y2)
		if toInt:
			x1 = int(x1)
			x2 = int(x2)
			y1 = int(y1)
			y2 = int(y2)
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		return self

	def __mul__(self, y):
		if isinstance(y, float) or isinstance(y, int):
			w = self.w()*y
			h = self.h()*y
			self.x1, self.x2 = self.cx() - w/2., self.cx() + w/2.
			self.y1, self.y2 = self.cy() - h/2., self.cy() + h/2.
		return self

	def __div__(self, y):
		return self.__mul__(1./y)

class VidDet(object): #tagged format

	min_fr = 100000
	max_fr = -1

	#@staticmethod
	def readline(self, row):
		row = row[:-1].split(',')
		fr = int(row[0])
		la = int(row[1])
		x1 = int(row[2])
		y1 = int(row[3])
		w = int(row[4])
		h = int(row[5])
		f = int(row[8])
		cl = int(row[7])
		conf = float(row[6])
		# if f!=1: return None
		if cl!=3: return None
		res = Det(x1,y1,x1+w,y1+h,cl,conf)
		res.fr = fr
		res.id = la
		# res.ign = cl not in [1,2,7,12]
		return res

	def __init__(self, fn = None):
		self.frd = {}
		self.idmap = {}
		if fn is not None:
			f = open(fn)
			rows = f.readlines()
			for row in rows:
				D = self.readline(row)
				if D is None: continue
				# print type(D)
				if isinstance(D, Det)==False:
					# print D
					fr, x1, y1, w, h, label, conf = D
					D = Det(x1,y1,w,h,label,conf)
				else:
					fr = D.fr
				if fr not in self.frd:
					self.frd[fr] = []
				self.frd[fr].append(D)
				if 'id' in D.__dict__:
					self.idmap[D.id] = True
				self.min_fr = min(self.min_fr, fr)
				self.max_fr = max(self.max_fr, fr)
			f.close()
		self.p_map = {}

	def __getitem__(self, index):
		if index in self.frd:
			return self.frd[index]
		else:
			return []

	def frameRange(self):
		return xrange(self.min_fr, self.max_fr+1)

	def append_data(self, fr, det, tag):
		if fr not in self.frd:
			self.frd[fr] = []
		det.label = tag
		self.frd[fr].append(det)
		self.min_fr = min(self.min_fr, fr)
		self.max_fr = max(self.max_fr, fr)

	def Person(self, ind):
		if ind in self.p_map:
			return self.p_map[ind]
		res = VidDet()
		for i in self.frameRange():
			for j in self[i]:
				if j.id==ind:
					res.append_data(i, j, j.label)
					break
		self.p_map[ind] = res
		return res

def paint(im, dt, sp, base, fd = None):
	margin = 20
	w = im.shape[1]
	h = im.shape[0]
	if dt.cls==3 and dt.w()>34 and sp>=-0.0000000001:
		sp*=base
		sp = abs(sp)
		l = int(dt.x1)
		r = int(dt.x2)
		t = int(dt.y1)
		b = int(dt.y2)
		if l < margin or r > w - margin or t < margin or b > h - margin*2:
			return
		color = (255,199,199)
		cv2.rectangle(im, (l,t), (r,b), color, 1)
		cv2.putText(im, 'id %d'%dt.id, (r+3,t+0), cv2.FONT_HERSHEY_DUPLEX, 0.5, color)
		cv2.putText(im, 'km %.2f'%sp, (r+3,t+16), cv2.FONT_HERSHEY_DUPLEX, 0.5, color)
		cv2.putText(im, 'mi %.2f'%(sp*0.6213711), (r+3,t+32), cv2.FONT_HERSHEY_DUPLEX, 0.5, color)
		cv2.putText(im, 'W_ %.1f %.1f'%(one.wx, one.wy), (r+3,t+64), cv2.FONT_HERSHEY_DUPLEX, 0.5, color)
		if fd is not None:
			fd, seq, fr = fd
			if sp > 145: sp = 145
			fd.write('%d %d -1 %d %d %d %d %.3f %.2f\n'%(seq, fr, l,t,r,b, sp*0.6213711, 1.0))

def estiP(im, Ps):
	for cx, cy, wx, wy in Ps:
		cx = int(cx)
		cy = int(cy)
		color = (0,255,255)
		cv2.rectangle(im, (cx-2, cy-2), (cx+2, cy+2), color, 1)
		cv2.putText(im, 'e %.2f %.2f'%(wx, wy), (cx+5,cy-5), cv2.FONT_HERSHEY_DUPLEX, 0.5, color)

def judge(P, Q):
	A, B = Q
	x, y = P
	dx = B[0] - A[0]
	dy = B[1] - A[1]
	x -= A[0]
	y -= A[1]
	if x*dy - y*dx<0: return 0
	else: return 1

def dis_p2l(P, Q):
	A, B = Q
	x, y = P
	dx = B[0] - A[0]
	dy = B[1] - A[1]
	x -= A[0]
	y -= A[1]
	return abs(dy*x+dx*y)/sqrt(dx**2+dy**2)

def ffloat(x):
	return tuple([int(i) for i in x])

def kf_pred(x,p,a,q):
	return [a*x, a*p*a.T+q]

def kf_upda(x,p,y,h,r):
	IM = h*x
	IS = r+h*p*h.T
	K = p*h.T*IS.I
	D = K*(y-IM)
	# D[1,0] = D.take(1) * 0.2
	# D[3,0] = D.take(3) * 0.2
	# return [x+K*(y-IM),p-K*IS*K.T]
	return [x+D,p-K*IS*K.T]

def kf_loop(x,p,h,r,y,a,q):
	tmp = kf_pred(x,p,a,q)
	return kf_upda(tmp[0],tmp[1],y,h,r)

def km_esti(x, p, y):
	h = np.zeros((1,2),dtype='float32').reshape(2)
	h[0] = 1
	R = np.eye(1,1,dtype='float32')*0.1
	A = np.eye(2,2,dtype='float32').reshape(4)
	A[1] = 1
	Q = np.eye(2,2,dtype='float32').reshape(4)
	Q[1] = 1
	Q[2] = 1
	Q = Q*0.0000025
	h = np.mat(h.reshape(1,2))
	A = np.mat(A.reshape(2,2))
	Q = np.mat(Q.reshape(2,2))
	if y is None:
		return kf_pred(x,p,A,Q)
	else:
		return kf_loop(x,p,h,R,y,A,Q)

def mk_cal(G, w, h):
	mi = 100000000
	res = None
	S = copy.copy(G)
	W = [(i[2], i[3]) for i in G]
	I = [(i[0], i[1]) for i in G]
	for case in xrange(10000):
		random.shuffle(S)
		n = random.randint(4, 4)
		K = S[:n]
		try:
			tmpC = Calibrator(K)
			tmp = tmpC.inversion(W + [(K[0][2], 1000000)])
		except:
			continue
		if tmp[-1][1]>h/2 or tmp[-1][1]<-100: continue# or tmp[-1][0]<300 or tmp[-1][0]>1600: continue
		d = 0.
		for i, (cx, cy) in enumerate(tmp[:-1]):
			d += ((cx - I[i][0])**2 + (cy - I[i][1])**2)**1
		if d < mi:
			mi = d
			res = K
	if res is None:
		print 'error, using first 4'
		res = G[:4]
	print 'rand dis', mi
	return res	

def choosing(G, w, h, dt, Q):
	#-----------start choosing points--------------------
	# K = [random.choice(PS[seq]) for ii in xrange(4)]
	# K = PS[seq]
	# K = [i for i in K if (i[2]==-3.6576  and i[3]!=3.048 or i[2]==22.0456)] + [(1095, 22, -3.6576, 1000000)]
	res = mk_cal(G, w, h)
	posCal = Calibrator(res)
	disP = posCal.inversion([(res[0][2],10000000)])[0]
	be = w
	en = -1
	for i in G:
		be = min(be, int(i[0]))
		en = max(en, int(i[0]))
	Y = G[0][1]
	maxi = 180.
	mmin = w
	endP = None
	for i in xrange(be, en+1, 2):
		stP = (i, Y)
		mini = [w, w]
		for j in G:
			clu = judge(j[:2], (stP, disP))
			tmp = dis_p2l(j[:2], (stP, disP))
			mini[clu] = min(mini[clu], tmp)
		if mini[0]==w or mini[1]==w: continue
		if abs(mini[0] - mini[1]) < 10 and mini[0] + mini[1]>maxi:
			maxi = mini[0] + mini[1]
			mmin = abs(mini[0] - mini[1])
			endP = stP
	sumA = ([], [])
	if endP is not None:
		for i in G:
			sumA[judge(i[:2], (endP, disP))].append(i)
	print len(sumA[0]), len(sumA[1])
	if len(sumA[0])<4 or len(sumA[1])<4:
		tmp = [dt.Person(i) for i in dt.idmap]
		posCal.optim(dt, (w, h), Q)
		calA = posCal, res
		calB = posCal, res
		return (calA, calB), (disP, disP)
	else:
		def classi(x, Q):
			for i in x.frameRange():
				if len(x[i]):
					return judge((x[i][0].cx(), x[i][0].cy()), Q)
			return 0
		dtA = [dt.Person(i) for i in dt.idmap if classi(dt.Person(i), (endP, disP))==0]
		dtB = [dt.Person(i) for i in dt.idmap if classi(dt.Person(i), (endP, disP))==1]
		calA = mk_cal(sumA[0], w, h)
		calB = mk_cal(sumA[1], w, h)
		return ((Calibrator(calA).optim(dtA, (w, h), Q), calA), (Calibrator(calB).optim(dtB, (w, h), Q), calB)), (endP, disP)
	# for D in xrange(-10, 10):
	# 	K = []
	# 	Gi = 0
	# 	D  = 2
	# 	pos = D
	# 	neg = D
	# 	while len(K)<4:
	# 		if G[Gi][2]<D:
	# 			if neg==D:
	# 				# neg = G[Gi][2:]
	# 				neg = G[Gi][2]
	# 				K.append(G[Gi])
	# 			elif G[Gi][2]==neg:
	# 			# elif isinstance(neg, list) and G[Gi][2]!=neg[0] and G[Gi][3]!=neg[1]:
	# 				neg = D+10000000
	# 				K.append(G[Gi])
	# 		if G[Gi][2]>D:
	# 			if pos==D:
	# 				pos = G[Gi][2]
	# 				# pos = G[Gi][2:]
	# 				K.append(G[Gi])
	# 			elif G[Gi][2]==pos:
	# 			# elif isinstance(pos, list) and G[Gi][2]!=pos[0] and G[Gi][3]!=pos[1]:
	# 				pos = D-10000000
	# 				K.append(G[Gi])
	# 		Gi += 1
	# 		if Gi>=len(G):
	# 			break
	# K = G
	#-----------end choosing points--------------------
	return res

if __name__=='__main__':
	root = './trk1vids'
	psfile = './LOCF2.txt'
	trkroot = './trk1out/out'
	vids = sorted(os.listdir(root))
	# vids = ['Loc3_5.mp4']
	# vids = [i for i in vids if 'Loc3' in i or 'Loc4' in i]
	seqs = [i[:-4] for i in vids]
	fd = open('track1.txt', 'w')
	testSet = zip(seqs, vids)
	with open(psfile) as f:
		PS = json.load(f)
	print len(PS), 'Loc'
	for ccnt, (seq, vid) in enumerate(testSet):
		# if 'Loc3' not in vid and 'Loc4' not in vid: continue
		print seq, vid
		vn = root+'/'+vid
		tn = trkroot+'/'+vid+'-res.txt'
		vi = cv2.VideoCapture(vn)
		dt = VidDet(tn)
		fps = vi.get(cv2.cv.CV_CAP_PROP_FPS)
		base = 3.6 * fps
		cnt = int(vi.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
		w, h = int(vi.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(vi.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
		print 'fps', fps, 'w', w, 'h', h, 'cnt', cnt
		print 'LOC points', len(PS[seq])
		vi.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
		fr = 0
		mo = {}
		# PS[seq] = [i for i in PS[seq] if not (i[2]>10 and i[3]>13 and i[3] <14)]
		K, Q = choosing(PS[seq], w, h, dt, (base, 0.6))

		# print K
		# K += [(1191, 104, K[0][2], 5000000)]
		# Calib = Calibrator(K)
		for fi in xrange(cnt):
			fi = fi + 1
			for one in dt[fi]:
				uid = one.id
				cx, cy = one.cx(), one.cy()
				Calib = K[judge((cx, cy), Q)][0]
				d = 5
				lefti = fi - d
				righi = fi + d
				while lefti>fi - d*3 and len(dt.Person(uid)[lefti])<=0: lefti -= 1
				while righi<fi + d*3 and len(dt.Person(uid)[righi])<=0: righi += 1
				if lefti>fi-d*3 and righi<fi+d*3:
					bef = dt.Person(uid)[lefti][0]
					aft = dt.Person(uid)[righi][0]
					tmp = [(bef.cx(), bef.cy()+bef.h()/2., aft.cx(), aft.cy()+aft.h()/2., righi - lefti)]
					sp = Calib.predict2(tmp)[0]
					if sp>0 and sp*base<6. and len(dt.Person(uid)[fi-5]) and sp < dt.Person(uid)[fi-5][0].sp+5/base and dt.Person(uid)[fi-5][0].sp>=0.:
						d = 5 * int(6. - sp*base) * 2
						lefti = fi - d
						righi = fi + d
						while lefti>fi - d*3 and len(dt.Person(uid)[lefti])<=0: lefti -= 1
						if lefti<=fi-d*3:
							lefti = fi - d
							while lefti<fi and len(dt.Person(uid)[lefti])<=0: lefti += 1
							if lefti>=fi: lefti = fi - d*3
						while righi<fi + d*3 and len(dt.Person(uid)[righi])<=0: righi += 1
						if righi>=fi + d*3:
							righi = fi + d
							while righi>fi and len(dt.Person(uid)[righi])<=0: righi -= 1
							if righi<=fi: righi = fi + d*3
						if lefti>fi-d*3 and righi<fi+d*3:
							d = min(fi - lefti, righi - fi)
							lefti = fi - d
							righi = fi + d
							# print fi, lefti, righi, d
							sp2 = 100000
							try:
								bef = dt.Person(uid)[lefti][0]
								aft = dt.Person(uid)[righi][0]
								tmp = [(bef.cx(), bef.cy()+bef.h()/2., aft.cx(), aft.cy()+aft.h()/2., righi - lefti)]
								sp2 = Calib.predict2(tmp)[0]
							except Exception:
								pass
							if sp2<sp:
								sp = sp2
								if sp<1:
									sp /= 10.
							# raw_input()
				else:
					sp = -1
				if sp>-1 and uid not in mo:
					Y_ = np.mat(np.array([sp], dtype='float32').reshape(1,1))
					X_ = np.mat(np.array([sp, 0], dtype='float32').reshape(2,1))
					P_ = np.mat(np.eye(2,2, dtype='float32'))*5
					mo[uid] = km_esti(X_,P_,Y_)
				else:
					if sp>-1:
						Y_ = np.mat(np.array([sp], dtype='float32').reshape(1,1))
						X_ = mo[uid][0]
						P_ = mo[uid][1]
						mo[uid] = km_esti(X_,P_,Y_)
						sp = mo[uid][0].take(0)
					elif uid in mo:
						X_ = mo[uid][0]
						P_ = mo[uid][1]
						mo[uid] = km_esti(X_,P_,None)
						sp = mo[uid][0].take(0)
				one.sp = sp
				if one.sp>-0.3 and one.sp<0:
					one.sp = 0.
				# if one.sp>0 and one.sp<0.5/base: one.sp = 0.
				one.wx, one.wy = Calib.predict([(one.cx(), one.cy()+one.h()/2.)])[0]
		# thr = 0.1
		# for uid in mo:
		# 	one = dt.Person(uid)
		# 	flag = h+1
		# 	fli = None
		# 	for fi in one.frameRange():
		# 		it = one[fi][0]
		# 		if it.cy()>h*0.7 and it.cy()<h*0.8:
		# 			if it.cy() < flag:
		# 				flag = min(flag, it.cy())
		# 				fli = fi
		# 	if flag>h:
		# 		pass
		# 	else:
		# 		for fi in xrange(fli, one.min_fr, -1):
		# 			fi -= 1
		# 			pre = one[fi + 1][0]
		# 			it = one[fi][0]
		# 			if it.sp - pre.sp<-thr: it.sp = pre.sp - thr
		# 			elif it.sp - pre.sp>thr: it.sp = pre.sp + thr
		# 		for fi in one.frameRange(fli, one.max_fr):
		# 			fi += 1
		# 			pre = one[fi - 1][0]
		# 			it = one[fi][0]
		# 			if it.sp - pre.sp<-thr: it.sp = pre.sp - thr
		# 			elif it.sp - pre.sp>thr: it.sp = pre.sp + thr
		for fi in xrange(cnt):
			fi = fi + 1
			s, im = vi.read()
			if not s or im is None:
				break
			fr += 1
			for one in dt[fi]:
				paint(im, one, one.sp, base, (fd, ccnt+1, fr))
			continue
			estiP(im, K[0][0].pts + K[1][0].pts)
			# estiP(im, K[0][1] + K[1][1])
			cv2.line(im, ffloat(Q[0]), ffloat(Q[1]), (0,0,255), 1)
			# estiP(im, PS[seq])
			W = [(i[2], i[3]) for i in PS[seq]] + [(0, 10000000)]
			te = K[0][0].inversion(W)
			for ti, po in enumerate(te):
				cx, cy = po
				cx = int(cx)
				cy = int(cy)
				color = (0,255,100)
				cv2.rectangle(im, (cx-2, cy-2), (cx+2, cy+2), color, 1)
				wx, wy = W[ti]
				cv2.putText(im, 's1 %.2f %.2f'%(wx, wy), (cx+5,cy-5), cv2.FONT_HERSHEY_DUPLEX, 0.5, color)
			te = K[1][0].inversion(W)
			for ti, po in enumerate(te):
				cx, cy = po
				cx = int(cx)
				cy = int(cy)
				color = (100,255,0)
				cv2.rectangle(im, (cx-2, cy-2), (cx+2, cy+2), color, 1)
				wx, wy = W[ti]
				cv2.putText(im, 's2 %.2f %.2f'%(wx, wy), (cx+5,cy+5), cv2.FONT_HERSHEY_DUPLEX, 0.5, color)
			cv2.imshow(seq, im)
			cv2.waitKey(0)

			# if fr > 50: break
		print 'iter', fr
		vi.release()
	fd.close()
	