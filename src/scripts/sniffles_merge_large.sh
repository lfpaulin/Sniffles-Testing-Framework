#!/bin/bash
#SBATCH --job-name=snfPopXL
#SBATCH --time=21-00:00:00
#SBATCH --partition=long
#SBATCH --account=proj-fs0002

. /stornext/snfs4/next-gen/scratch/luis/hermann/conda3/etc/profile.d/conda.sh
conda activate sniffles


SNF2_PATH=$1
INPUT_FILE_TSV=$2
OUTPUT=$3
REFERENCE=$4
NTASKS=$5
EXTRA_PARAM=$6

let MAX_FILES=$(wc -l ${SNF2_PATH} | cut -d " " -f 1)+100

ulimit -n ${MAX_FILES}

python ${SNF2_PATH} \
    --input "${INPUT_FILE_TSV}" \
    --vcf ${OUTPUT}.vcf.gz \
    --minsvlen 50 \
    --reference ${REFERENCE} \
    --threads ${NTASKS} \
    ${EXTRA_PARAM}