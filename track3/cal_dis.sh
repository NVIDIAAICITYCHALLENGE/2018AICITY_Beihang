

GPU_NUM=1
for i in {0..2}; do
    srun  --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-36 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {3..5}; do
    srun  --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-37 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {6..8}; do
    srun  --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-38 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {9..11}; do
    srun  --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-39 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {12..14}; do
    srun  --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-40 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {15..17}; do
    srun  --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-41 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {18..20}; do
    srun  --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-42 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {21..23}; do
    srun  --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-43 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {24..26}; do
    srun  --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-44 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {27..29}; do
    srun  --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-45 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {30..32}; do
    srun  --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-46 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {33..38}; do
    srun  --partition=VIBackEnd2 -w BJ-IDC1-10-10-15-52 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {39..44}; do
    srun  --partition=VIFrontEnd -w BJ-IDC1-10-10-15-58 python2 -u ./src/track3_cal_dis.py ${i} &
done
for i in {45..49}; do
    srun  --partition=VIFrontEnd -w BJ-IDC1-10-10-15-58 python2 -u ./src/track3_cal_dis.py ${i} &
done


wait
echo 'all done!'