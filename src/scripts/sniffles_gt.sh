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
VCF_IN=$3
OUTPUT=$4
REFERENCE=$5
NTASKS=8

/usr/bin/time -v -o log_snf2_time${OUTPUT}.txt ${SNF2_PATH} \
    --input ${INPUT} \
    --genotype-vcf ${VCF_IN} \
    --vcf ${OUTPUT}.vcf.gz \
    --threads ${NTASKS} \
    --reference ${REFERENCE} \
    --minsvlen 50  \
    --sample-id ${OUTPUT}
