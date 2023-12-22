#!/bin/bash
#SBATCH --job-name=snf2mend
#SBATCH --ntasks-per-node=8
#SBATCH --mem=16gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0002

. /stornext/snfs4/next-gen/scratch/luis/hermann/conda3/etc/profile.d/conda.sh
conda activate sniffles

SNF2_PATH=$1
INPUT_FILE_TSV=$2
OUTPUT=$3
REFERENCE=$4
EXTRA_PARAM=$5
NTASKS=8

/usr/bin/time -v -o log_snf2_time${OUTPUT}.txt  ${SNF2_PATH} \
    --input "${INPUT_FILE_TSV}" \
    --vcf ${OUTPUT}.vcf.gz \
    --minsvlen 50 \
    --reference ${REFERENCE} \
    --threads ${NTASKS} \
    ${EXTRA_PARAM}