export PYTHONPATH=/mnt/lustre/share/opencv-2.4.13-ffmpeg/lib/python2.7/site-packages:$PYTHONPATH

for i in {0..4}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-44 python2 -u vis_split.py ${i} &
done
for i in {5..9}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-45 python2 -u vis_split.py ${i} &
done
for i in {10..14}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-46 python2 -u vis_split.py ${i} &
done
for i in {15..19}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-37 python2 -u vis_split.py ${i} &
done
for i in {20..24}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-38 python2 -u vis_split.py ${i} &
done
for i in {25..29}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-39 python2 -u vis_split.py ${i} &
done
for i in {30..34}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-40 python2 -u vis_split.py ${i} &
done
for i in {35..39}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-41 python2 -u vis_split.py ${i} &
done
for i in {40..44}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-42 python2 -u vis_split.py ${i} &
done
for i in {45..49}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-43 python2 -u vis_split.py ${i} &
done

wait
srun --partition=VIBackEnd1 python2 -u concat_res_im.py
echo "all done"