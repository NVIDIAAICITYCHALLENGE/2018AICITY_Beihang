This repository contains our source code of Track 3 in the NVIDIA AI City Challenge Workshop at CVPR 2018.

The source code of Track 3 is developed in Python and C++. 

Track 3 has been tested on Linux. Dependencies include CUDA, cuDNN and OpenCV library.

## Code structure

### Track 3

Since the computation cost of all the data is huge, we divide this task into 4 steps in the `./Track3/` folder:

1. Run the script  `download_mot_raw.sh` to download our precaculated multiple object tracking (single camera) raw data.
2. Based on the MOT raw data, run the script  `get_feature.sh` to calculate re-identification feature of all the cropped vehicle images and store them in the disk.
3. After getting all the features, script  `cal_dis.sh` will compute all the pair distances between two vehicles.
4. Fianlly, run script  `run_generate_track.sh` , which process the data to group vehicles crossing the cameras. The vehicles to be found are the ones that have shown in all the four different camera locations. 

Besides of the track3 task, we include some experimental results of VeRi776 dataset in the folder  `./veri776/` . It is a purely vehicle re-identification problem and we achieve the state-of-the-art mAP and CMC1 scores.

## Reference

W. Feng, D. Ji, Y. Wang, S. Chang, H. Ren and W. Gan, "Challenges on Large Scale Surveillance Video Analysis," in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recogn. Workshops (CVPRW), Jun. 2018. (to appear)

## Disclaimer

For any question you can contact .