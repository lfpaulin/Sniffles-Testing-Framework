#!/bin/bash
#SBATCH --job-name=snf2merge
#SBATCH --ntasks=8
#SBATCH --mem=16gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0002

. /stornext/snfs4/next-gen/scratch/luis/hermann/conda3/etc/profile.d/conda.sh
conda activate sniffles

# sniffles2
SNF2_PATH=$1
# data
SAMPLE1=$2
SAMPLE2=$3
# output
OUTPUT=$4
# ref
REFERENCE=$5
TANDEM=$6
# other
EXTRA_PARAM=$7
NTASKS=8

# sniffles2 call
merge_names=()
for bam in ${SAMPLE1} ${SAMPLE2};
do
    # get name
    bamid=$(basename $bam | cut -d "." -f 1) \
    # save name
    merge_names+=(${bamid})
    printf "%s\t%s\n" ${OUTPUT}_${bamid}.snf ${bamid} >> ${OUTPUT}.tsv
    /usr/bin/time -v -o log_snf2_time_${OUTPUT}_${bamid}.txt  ${SNF2_PATH} \
        --input ${bam} \
        --vcf ${OUTPUT}_${bamid}.vcf.gz \
        --threads ${NTASKS} \
        --reference ${REFERENCE} \
        --minsvlen 50  \
        --sample-id ${bamid} \
        --snf ${OUTPUT}_${bamid}.snf \
        ${USE_TANDEM_REP}  ${EXTRA_PARAM}
done

# sniffles2 merge
/usr/bin/time -v -o log_snf2_time_merge.txt  ${SNF2_PATH} \
    --input ${OUTPUT}.tsv \
    --vcf ${OUTPUT}.vcf.gz \
    --minsvlen 50 \
    --reference ${REFERENCE} \
    --threads ${NTASKS}