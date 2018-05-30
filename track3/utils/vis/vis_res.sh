export PYTHONPATH=/mnt/lustre/share/opencv-2.4.13-ffmpeg/lib/python2.7/site-packages:$PYTHONPATH
srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-45 python2 -u vis_res.py $1