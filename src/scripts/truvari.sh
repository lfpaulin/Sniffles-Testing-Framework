#!/bin/bash
#SBATCH --job-name=truvari
#SBATCH --ntasks-per-node=1
#SBATCH --mem=8gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0002

. /stornext/snfs4/next-gen/scratch/luis/hermann/conda3/etc/profile.d/conda.sh
conda activate sniffles

# from args
INVCF_OLD=$1
OUTPUT_OLD=$2
INVCF_NEW=$3
OUTPUT_NEW=$4

# from json
THUTHSET_VCF=$5
INCLUDE_BED=$6

# from args
REFERENCE=$7
# from json
BENCH=$8

truvari bench \
    --base ${THUTHSET_VCF} \
    --comp ${INVCF_OLD} \
    --output ${OUTPUT_OLD}_${BENCH} \
    --passonly \
    --includebed ${INCLUDE_BED} \
    --refdist 2000 \
    --reference ${REFERENCE} \
    --giabreport

truvari bench \
    --base ${THUTHSET_VCF} \
    --comp ${INVCF_NEW} \
    --output ${OUTPUT_NEW}_${BENCH} \
    --passonly \
    --includebed ${INCLUDE_BED} \
    --refdist 2000 \
    --reference ${REFERENCE} \
    --giabreport
