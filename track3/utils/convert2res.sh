for i in {0..9}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-36 python2 -u convert2res.py ${i} &
done

for i in {10..19}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-37 python2 -u convert2res.py ${i} &
done

for i in {20..29}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-38 python2 -u convert2res.py ${i} &
done

for i in {30..39}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-39 python2 -u convert2res.py ${i} &
done

for i in {40..49}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-40 python2 -u convert2res.py ${i} &
done

for i in {50..59}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-41 python2 -u convert2res.py ${i} &
done

for i in {60..69}; do
    srun --partition=VIBackEnd1 -w BJ-IDC1-10-10-15-42 python2 -u convert2res.py ${i} &
done

for i in {70..79}; do
    srun --partition=VIBackEnd2 -w BJ-IDC1-10-10-15-50 python2 -u convert2res.py ${i} &
done

for i in {80..89}; do
    srun --partition=VIBackEnd2 -w BJ-IDC1-10-10-15-51 python2 -u convert2res.py ${i} &
done

#for i in {90..94}; do
#    srun --partition=VIBackEnd2 -w BJ-IDC1-10-10-15-52 python2 -u convert2res.py ${i} &
#done

wait

echo "all done"