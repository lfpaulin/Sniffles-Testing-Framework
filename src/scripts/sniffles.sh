#!/bin/bash
#SBATCH --ntasks=8
#SBATCH --mem=16Gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0002

. /stornext/snfs4/next-gen/scratch/luis/hermann/conda3/etc/profile.d/conda.sh
conda activate sniffles

SNF2_PATH=$1
INPUT=$2
OUTPUT=$3
REFERENCE=$4
USE_TANDEM_REP=$5
EXTRA_PARAM=$6
NTASKS=8

/usr/bin/time -v -o log_snf2_time${OUTPUT}.txt ${SNF2_PATH} \
    --input ${INPUT} \
    --vcf ${OUTPUT}.vcf.gz \
    --snf ${OUTPUT}.snf \
    --threads ${NTASKS} \
    --reference ${REFERENCE} \
    --minsvlen 50  \
    --sample-id ${OUTPUT} \
    ${USE_TANDEM_REP}  ${EXTRA_PARAM}
