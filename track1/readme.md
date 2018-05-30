## Track1

### Input
- trk1vids: folder contains all videos, e.g., Loc1_1.mp4
- trk1out/out: folder contains all output of MOT system, e.g. Loc1_1.mp4-res.txt
- LOC-modL2: file contains labels of lanelines

### Output
track1.txt: the result file

### Steps
- run refine.py

> python refine.py

- run track1

> python track1.py

### Files Description
- track1.py is the entrance script
- Calibra.py is a helper library
- refine.py is to get more precise label
- verify.py is a tool to analyse the speed distribution
- LOCF2.txt is the middle file of refined label

### Depends
- Numpy
- cv2
- matplotlib


