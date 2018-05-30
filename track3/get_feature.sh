
[[ $# -eq 0 ]] && echo "$0 test/query your_save_directory" && exit 0

export PYTHONUNBUFFERED="True"
export PYTHONPATH=home_directory/codes/VIC/core/python:$PYTHONPATH

GPU_NUM=1
MV2_USE_CUDA=1 MV2_ENABLE_AFFINITY=0 MV2_SMP_USE_CMA=0 srun \
--mpi=pmi2 --gres=gpu:${GPU_NUM} -n1 --ntasks-per-node=1  --partition=VIBackEnd1 \
python2 -u ./src/deploy_model.py $1 $2