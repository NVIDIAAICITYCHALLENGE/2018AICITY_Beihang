import numpy as np
import math
from math import *
import random
eps = 1e-7

def gauss(Mat, N, M):	# Mat: N*(M+1)
	for edone in Mat:
		print edone
	print '-'*10
	match = [-1] * N
	ans = [0] * N
	equation_idx = 0
	for var in range(M):
		t = equation_idx
		ma = 0

		# find the max coefficient, and move the equation to the current idx
		for i in range(equation_idx, N):
			if abs(Mat[i][var]) > ma:
				ma = abs(Mat[i][var])
				t = i
		if abs(Mat[t][var]) < eps:
			match[var] = -1
			continue
		tmp = Mat[equation_idx]
		Mat[equation_idx] = Mat[t]
		Mat[t] = tmp

		# make this coefficient to be 1
		for j in range(var + 1, M + 1):
			Mat[equation_idx][j] /= Mat[equation_idx][var]
		Mat[equation_idx][var] = 1.

		# subtract this equation from all others
		for i in range(0, N):
			if i == equation_idx:
				continue
			print i, ') -', Mat[i][var], ' * ', equation_idx, ')'
			if abs(Mat[i][var]) > eps:
				for j in range(var + 1, M + 1):
					Mat[i][j] -= Mat[i][var] * Mat[equation_idx][j]
				Mat[i][var] = 0.

		match[var] = equation_idx
		equation_idx += 1
		for edone in Mat:
			print edone
		print '-'*10
	for i in range(0, M):
		if (match[i] == -1):
			# ans[i] can be any number
			ans[i] = 0
		else:
			ans[i] = Mat[match[i]][M]
	for i in range(equation_idx, N):
		if abs(Mat[i][M]) > eps:
			# there's no solution
			raise
	return ans

def cam(M):
	return M[0][0] * M[1][1] - M[0][1] * M[1][0]

class Calibrator:

	def __init__(self, FourP):
		self.pts = FourP
		self.solve()

	def solve(self):
		FourP = self.pts
		if len(FourP)<4:
			raise Exception('impossible to calibra')
		Mat = []
		A = []
		B = []
		# for I, W in FourP:
		for one in FourP:
			I = one[:2]
			W = one[2:]
			u, v = I
			x, y = W
			u = float(u)
			v = float(v)
			x = float(x)
			y = float(y)
			if abs(x)<0.00000001:
				x = 0.00000001
			'''
			item = [y*u, u, -x, -y, -1, 0,0,0, -x*u]
			item = [float(i) for i in item]
			Mat.append(item)
			item = [y*v, v, 0,0,0, -x, -y, -1, -x*v]
			item = [float(i) for i in item]
			Mat.append(item)

		self.ans = gauss(Mat, 8, 8)
		'''
			# itemA = [y*u/x, u/x, -1, -y/x, -1/x, 0,0,0]
			# itemB = [-u]
			itemA = [y*u, u, -x, -y, -1, 0,0,0]
			itemB = [-x*u]
			itemA = [float(i) for i in itemA]
			itemB = [float(i) for i in itemB]
			A.append(itemA)
			B.append(itemB)
			# itemA = [y*v/x, v/x, 0,0,0, -1, -y/x, -1/x]
			# itemB = [-v]
			itemA = [y*v, v, 0,0,0, -x, -y, -1]
			itemB = [-x*v]
			itemA = [float(i) for i in itemA]
			itemB = [float(i) for i in itemB]
			A.append(itemA)
			B.append(itemB)
		A = np.mat(A)
		B = np.mat(B)
		AA = A.T * A
		BB = A.T * B
		ans = AA.I * BB
		ans = ans.tolist()
		# print (ans)
		self.ans = [ i[0] for i in ans]
		#'''		
	
	def infer(self, u, v):
		b, c, e, f, g, h, i, j = self.ans
		cx = cam([[c*u-g,c*v-j],[f-b*u,i-b*v]])
		cy = cam([[e-u,h-v],[c*u-g,c*v-j]])
		dd = cam([[e-u,h-v],[f-b*u,i-b*v]])
		x = cx/dd
		y = cy/dd
		return x, y

	def predict(self, pos):
		res = []
		for u, v in pos:
			x, y = self.infer(u, v)
			res.append((x,y))
		return res

	def predict2(self, pos):
		res = []
		for u1, v1, u2, v2, d in pos:
			x1, y1 = self.infer(u1, v1)
			x2, y2 = self.infer(u2, v2)
			dis = sqrt((x1 - x2)**2+(y1 - y2)**2)
			res.append(dis/d)
		return res

	def inversion(self, pos):
		b, c, e, f, g, h, i, j = self.ans
		res = []
		for x, y in pos:
			u = (e*x + f*y + g) / (x + b*y + c)
			v = (h*x + i*y + j) / (x + b*y + c)
			res.append((u,v))
		return res

	def test(self, X, dt, sz, Q):
		w, h = sz
		base, thres = Q
		pre = self.pts
		self.pts = X
		self.solve()
		err = 0.
		d = 5
		cnt = 0
		maxI = 5
		for one in dt:
			# if one[one.min_fr][0].id!=61: continue
			if one.max_fr - one.min_fr < 20 : continue
			kk = []
			for fr in xrange(one.min_fr + d, one.max_fr + 1 - d, d):
				if len(one[fr - d])>0 and len(one[fr + d])>0 \
					 and len(one[fr])>0 and one[fr][0].w()>34 and one[fr][0].y1 + one[fr][0].h() < h - 20:
					bef = one[fr - d][0].cx(), one[fr - d][0].cy()
					aft = one[fr + d][0].cx(), one[fr + d][0].cy()
					v = self.predict2([(bef[0], bef[1], aft[0], aft[1], d*2)])[0]
					# print one[fr + d][0].id, fr, v*base, one.min_fr, one.max_fr, thres*d
					# raw_input()
					kk.append(v)
				else:
					if len(kk):
						kk.append(kk[-1])
			if len(kk)<=0: continue
			tmpErr = 0.
			for i in xrange(len(kk)-1):
				diff = abs(kk[i] - kk[i+1])
				if diff * base > thres * d:
					tmpErr += (diff*base - thres * d)**2
			tmpErr = sqrt(tmpErr)
			tmpErr /= len(kk)
			err += tmpErr
			cnt += 1
			if cnt>maxI: break
		self.pts = pre
		return err / maxI

	def optim(self, dt, sz, Q):
		return self
		adjX = self.pts[0][2]
		delta = 0.05
		be = -0.
		en = 0.04
		i = be
		bestPts = self.pts
		error = self.test(self.pts, dt, sz, Q)
		def frange(be, en, d):
			res = []
			while be <= en:
				res.append(be)
				be += d
			return res
		while i <= en:
			for iix in frange(-2, 2.5, 0.5):
				for iiy in frange(-2, 2.5, 0.5):
					tryPts = []
					for j in self.pts:
						if abs(j[2] - adjX) < 0.0001:
							ix, iy, wx, wy = j
							tryPts.append((ix + iix, iy + iiy, wx, wy + i))
						else:
							ix, iy, wx, wy = j
							tryPts.append((ix, iy, wx, wy))
					tmp = self.test(tryPts, dt, sz, Q)
					# print tryPts, tmp
					if tmp < error:
						error = tmp
						bestPts = tryPts
			i += delta
		self.pts = bestPts
		print 'best optim', error
		print self.pts
		self.solve()
		return self
