#!/bin/bash
#SBATCH --ntasks=8
#SBATCH --mem=16Gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0002

. /stornext/snfs130/fritz/luis/miniconda3_py310_24_3/etc/profile.d/conda.sh
conda activate snf2dev

SNF2_PATH=$1
INPUT=$2
OUTPUT=$3
REFERENCE=$4
USE_TANDEM_REP=$5
EXTRA_PARAM=$6

NTASKS=4
${SNF2_PATH} \
    --input ${INPUT} \
    --vcf ${OUTPUT}_threads_${NTASKS}.vcf.gz \
    --snf ${OUTPUT}_threads_${NTASKS}.snf \
    --threads ${NTASKS} \
    --reference ${REFERENCE} \
    --minsvlen 50  \
    --sample-id ${OUTPUT} \
    ${USE_TANDEM_REP}  ${EXTRA_PARAM}

md5sum ${OUTPUT}_threads_${NTASKS}.vcf.gz


NTASKS=6
${SNF2_PATH} \
    --input ${INPUT} \
    --vcf ${OUTPUT}_threads_${NTASKS}.vcf.gz \
    --snf ${OUTPUT}_threads_${NTASKS}.snf \
    --threads ${NTASKS} \
    --reference ${REFERENCE} \
    --minsvlen 50  \
    --sample-id ${OUTPUT} \
    ${USE_TANDEM_REP}  ${EXTRA_PARAM}

md5sum ${OUTPUT}_threads_${NTASKS}.vcf.gz



NTASKS=8
${SNF2_PATH} \
    --input ${INPUT} \
    --vcf ${OUTPUT}_threads_${NTASKS}.vcf.gz \
    --snf ${OUTPUT}_threads_${NTASKS}.snf \
    --threads ${NTASKS} \
    --reference ${REFERENCE} \
    --minsvlen 50  \
    --sample-id ${OUTPUT} \
    ${USE_TANDEM_REP}  ${EXTRA_PARAM}

md5sum ${OUTPUT}_threads_${NTASKS}.vcf.gz


