#!/bin/bash
#SBATCH --ntasks=8
#SBATCH --mem=32Gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0007

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
    --phase \
    --output-rnames \
    --sample-id ${OUTPUT} \
    --dev-monitor-memory 1 \
    ${USE_TANDEM_REP}  ${EXTRA_PARAM}

${SNF2_PATH} \
    --input ${INPUT} \
    --vcf ${OUTPUT}_noqc.vcf.gz \
    --threads ${NTASKS} \
    --reference ${REFERENCE} \
    --minsvlen 50  \
    --output-rnames \
    --mosaic-include-germline \
    --phase \
    --no-qc \
    --sample-id ${OUTPUT} \
    --dev-monitor-memory 1 \
    ${USE_TANDEM_REP}  ${EXTRA_PARAM}

if [[ -f "${OUTPUT}_noqc.vcf.gz" ]]
then
    bcftools view --include "SUPPORT > 1 && (SVTYPE = 'INS' || SVTYPE = 'DEL') && (SVLEN <= 50000 && SVLEN >= -50000)" \
    ${OUTPUT}_noqc.vcf.gz | bgzip -c > ${OUTPUT}_noqc_FILT.vcf.gz
    bcftools view --include "FILTER != 'PASS'" ${OUTPUT}_noqc_FILT.vcf.gz | bgzip -c > ${OUTPUT}_noqc_USE.vcf.gz
fi
