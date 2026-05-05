#!/bin/bash
#SBATCH --ntasks=8
#SBATCH --mem=16Gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0007

. /stornext/snfs210/fritz/luis/miniconda3_py313_26_322/etc/profile.d/conda.sh
conda activate snf2dev

SNF2_PATH=$1
INPUT=$2
VCF_IN=$3
OUTPUT=$4
REFERENCE=$5
NTASKS=8

${SNF2_PATH} \
    --input ${INPUT} \
    --genotype-vcf ${VCF_IN} \
    --vcf ${OUTPUT}.vcf.gz \
    --threads ${NTASKS} \
    --phase \
    --reference ${REFERENCE} \
    --minsvlen 50  \
    --sample-id ${OUTPUT}
