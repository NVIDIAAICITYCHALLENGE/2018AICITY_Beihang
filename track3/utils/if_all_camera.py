
# load all idxs 
with open('home_directory/VIC/track3/mean_features/all_idx.pkl', 'r') as f:
    all_idxs = pkl.load(f)

def if_all_camera(input):
	loc_ids = []
	for i in input:
		cid = int(all_idxs[int(i)][3])
		if cid not in loc_ids:
			loc_ids.append(cid)

	loc_ids.sort()
	if loc_ids == [1,2,3,4]:
		return True
	else:
		return False


