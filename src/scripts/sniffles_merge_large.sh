#!/bin/bash
#SBATCH --job-name=snfPopXL
#SBATCH --time=21-00:00:00
#SBATCH --partition=long
#SBATCH --account=proj-fs0007

. /stornext/snfs210/fritz/luis/miniconda3_py313_26_322/etc/profile.d/conda.sh
conda activate snf2dev


SNF2_PATH="/stornext/snfs170/next-gen/scratch/luis/hermann/bin/Sniffles_dev/src/sniffles2"
INPUT_FILE_TSV=$1
OUTPUT=$2
REFERENCE="/stornext/snfs170/next-gen/scratch/zhengxc/workspace/reference/1KG_ONT_VIENNA_hg38.fa"
NTASKS=24

ulimit -n 32768

python ${SNF2_PATH} \
    --input "${INPUT_FILE_TSV}" \
    --vcf ${OUTPUT}.vcf \
    --minsvlen 50 \
    --phase \
    --reference ${REFERENCE} \
    --threads ${NTASKS} \
    --no-sort
