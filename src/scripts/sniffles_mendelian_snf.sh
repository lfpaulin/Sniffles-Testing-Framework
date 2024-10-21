#!/bin/bash
#SBATCH --ntasks=8
#SBATCH --mem=16gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0002

. /stornext/snfs130/fritz/luis/miniconda3_py310_24_3/etc/profile.d/conda.sh
conda activate snf2dev

# sniffles2
SNF2_PATH=$1
# data
SNF_TSV_LIST=$2
# output
OUTPUT=$3
# ref
REFERENCE=$4
TANDEM=$5
# other
EXTRA_PARAM=$6
NTASKS=8

M=$(cat ${SNF_LIST} | head -n 1 | cut -f 2)               # first  elem of three
F=$(cat ${SNF_LIST} | head -n 2 | tail -n 1 | cut -f 2)   # second elem of three
P=$(cat ${SNF_LIST} | tail -n 1 | cut -f 2)               # third  elem of three
# trio order for mendelian
trio_names_string="${M},${F},${P}"

# sniffles2 merge
${SNF2_PATH} \
    --input ${SNF_TSV_LIST} \
    --vcf ${OUTPUT}.vcf.gz \
    --minsvlen 50 \
    --reference ${REFERENCE} \
    --threads ${NTASKS}

# bcftools mendelian
bcftools +mendelian2 --pfm 1X:hg002,hg003,hg004  --mode c ${OUTPUT}.vcf.gz |  grep "^n" >  ${OUTPUT}.mendelian
