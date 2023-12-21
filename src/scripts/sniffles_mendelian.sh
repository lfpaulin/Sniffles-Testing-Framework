#!/bin/bash
#SBATCH --job-name=snf2mend
#SBATCH --ntasks-per-node=8
#SBATCH --mem=16gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0002

. /stornext/snfs4/next-gen/scratch/luis/hermann/conda3/etc/profile.d/conda.sh
conda activate sniffles

# sniffles2
SNF2_PATH=$1
# data
PROBAND=$2
FATHER=$3
MOTHER=$4
# output
OUTPUT=$5
# ref
REFERENCE=$6
TANDEM=$7
# other
EXTRA_PARAM=$8
NTASKS=8

[[ -f ${OUTPUT}.tsv]]  && rm ${OUTPUT}.tsv
touch ${OUTPUT}.tsv

trio_names=()
for bam in ${MOTHER} ${FATHER} ${PROBAND};
do
    # get name
    bamid=$(basename $bam | cut -d "." -f 1 | sed -e "s/[.]/_/g") \
    # save name
    trio_names+=(${bamid})
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

# trio order for mendelian
trio_names_string=$(echo ${trio_names[*]} | sed -e "s/ /,/g")

# sniffles2 merge
/usr/bin/time -v -o log_snf2_time${OUTPUT}_trio.txt  ${SNF2_PATH} \
    --input ${OUTPUT}.tsv \
    --vcf ${OUTPUT}.vcf.gz \
    --minsvlen 50 \
    --reference ${REFERENCE} \
    --threads ${NTASKS}

# bcftools mendelian
bcftools +mendelian --trio ${trio_names_string}  --mode c  ${OUTPUT}.vcf.gz >  ${OUTPUT}.mendelian
