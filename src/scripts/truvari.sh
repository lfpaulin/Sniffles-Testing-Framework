#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --mem=4Gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0002

. /stornext/snfs130/fritz/luis/miniconda3_py310_24_3/etc/profile.d/conda.sh
conda activate truvari

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
    --refdist 1000 \
    --reference ${REFERENCE}

if [[ "${INVCF_NEW}" != "none" ]]
then
    truvari bench \
        --base ${THUTHSET_VCF} \
        --comp ${INVCF_NEW} \
        --output ${OUTPUT_NEW}_${BENCH} \
        --passonly \
        --includebed ${INCLUDE_BED} \
        --refdist 1000 \
        --reference ${REFERENCE}
fi