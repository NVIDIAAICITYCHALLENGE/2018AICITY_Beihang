
[[ $# -eq 0 ]] && echo "$0 camera_id split_id" && exit 0

export PYTHONUNBUFFERED="True"
export PYTHONPATH=/home_directory/opencv-2.4.13-ffmpeg/lib/python2.7/site-packages:home_directory/codes/VIC/core/python:$PYTHONPATH

GPU_NUM=1
MV2_USE_CUDA=1 MV2_ENABLE_AFFINITY=0 MV2_SMP_USE_CMA=0 srun \
--mpi=pmi2 --gres=gpu:${GPU_NUM} -n1 --ntasks-per-node=1  --partition=VIBackEnd1 \
python2 -u ./src/generate_track.py
