#!/bin/bash
#SBATCH --ntasks=8
#SBATCH --mem=32Gb
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
NTASKS=8

${SNF2_PATH} \
    --input ${INPUT} \
    --vcf ${OUTPUT}.vcf.gz \
    --snf ${OUTPUT}.snf \
    --threads ${NTASKS} \
    --reference ${REFERENCE} \
    --minsvlen 50  \
    --output-rnames \
    --sample-id ${OUTPUT} \
    --dev-monitor-memory 30 \
    ${USE_TANDEM_REP}  ${EXTRA_PARAM}

${SNF2_PATH} \
    --input ${INPUT} \
    --vcf ${OUTPUT}_noqc.vcf.gz \
    --threads ${NTASKS} \
    --reference ${REFERENCE} \
    --minsvlen 50  \
    --output-rnames \
    --no-qc \
    --sample-id ${OUTPUT} \
    --dev-monitor-memory 30 \
    ${USE_TANDEM_REP}  ${EXTRA_PARAM}
