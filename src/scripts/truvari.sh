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

WORKDIR=$PWD
echo "INFO: ${WORKDIR}"
# OLD
truvari bench \
    --base ${THUTHSET_VCF} \
    --comp ${WORKDIR}/${INVCF_OLD} \
    --output ${OUTPUT_OLD}_${BENCH} \
    --passonly \
    --includebed ${INCLUDE_BED} \
    --refdist 1000 \
    --reference ${REFERENCE}


# Stratification
DO_STRAT=$9
if [[ "${DO_STRAT}" == "1" ]];
then
    if [[ -d "${OUTPUT_OLD}_${BENCH}" ]];
    then
        cd ${OUTPUT_OLD}_${BENCH}
        mkdir strat
        cd strat
        # SVTYPE
        ## DEL
        bcftools view --include 'SVTYPE = "DEL"' ${THUTHSET_VCF} | bgzip -c > ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_DEL.vcf.gz
        tabix --preset vcf ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_DEL.vcf.gz
        bcftools view --include 'SVTYPE = "DEL"' ${WORKDIR}/${INVCF_OLD} | bgzip -c > ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_DEL.vcf.gz
        tabix --preset vcf ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_DEL.vcf.gz
        truvari bench \
            --base ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_DEL.vcf.gz \
            --comp ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_DEL.vcf.gz \
            --output strat_old_del \
            --passonly \
            --includebed ${INCLUDE_BED} \
            --refdist 1000 \
            --reference ${REFERENCE}
        ## DEL < 10kb
        bcftools view --include 'SVTYPE = "DEL" && SVLEN > -10000' ${THUTHSET_VCF} | bgzip -c > ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_DEL_small.vcf.gz
        tabix --preset vcf ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_DEL_small.vcf.gz
        bcftools view --include 'SVTYPE = "DEL" && SVLEN > -10000' ${WORKDIR}/${INVCF_OLD} | bgzip -c > ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_DEL_small.vcf.gz
        tabix --preset vcf ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_DEL_small.vcf.gz
        truvari bench \
            --base ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_DEL_small.vcf.gz \
            --comp ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_DEL_small.vcf.gz \
            --output strat_old_del_small \
            --passonly \
            --includebed ${INCLUDE_BED} \
            --refdist 1000 \
            --reference ${REFERENCE}
        ## DEL >= 10kb
        bcftools view --include 'SVTYPE = "DEL" && SVLEN <= -10000' ${THUTHSET_VCF} | bgzip -c > ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_DEL_large.vcf.gz
        tabix --preset vcf ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_DEL_large.vcf.gz
        bcftools view --include 'SVTYPE = "DEL" && SVLEN <= -10000' ${WORKDIR}/${INVCF_OLD} | bgzip -c > ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_DEL_large.vcf.gz
        tabix --preset vcf ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_DEL_large.vcf.gz
        truvari bench \
            --base ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_DEL_large.vcf.gz \
            --comp ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_DEL_large.vcf.gz \
            --output strat_old_del_large \
            --passonly \
            --includebed ${INCLUDE_BED} \
            --refdist 1000 \
            --reference ${REFERENCE}
        ## INS
        bcftools view --include 'SVTYPE = "INS"' ${THUTHSET_VCF} | bgzip -c > ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_INS.vcf.gz
        tabix --preset vcf ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_INS.vcf.gz
        bcftools view --include 'SVTYPE = "INS"' ${WORKDIR}/${INVCF_OLD} | bgzip -c > ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_INS.vcf.gz
        tabix --preset vcf ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_INS.vcf.gz
        truvari bench \
            --base ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_INS.vcf.gz \
            --comp ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_INS.vcf.gz \
            --output strat_old_ins \
            --passonly \
            --includebed ${INCLUDE_BED} \
            --refdist 1000 \
            --reference ${REFERENCE}
        ## INS < 10000
        bcftools view --include 'SVTYPE = "INS" && SVLEN < 10000' ${THUTHSET_VCF} | bgzip -c > ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_INS_small.vcf.gz
        tabix --preset vcf ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_INS_small.vcf.gz
        bcftools view --include 'SVTYPE = "INS" && SVLEN < 10000' ${WORKDIR}/${INVCF_OLD} | bgzip -c > ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_INS_small.vcf.gz
        tabix --preset vcf ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_INS_small.vcf.gz
        truvari bench \
            --base ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_INS_small.vcf.gz \
            --comp ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_INS_small.vcf.gz \
            --output strat_old_ins_small \
            --passonly \
            --includebed ${INCLUDE_BED} \
            --refdist 1000 \
            --reference ${REFERENCE}
        ## INS >= 10000
        bcftools view --include 'SVTYPE = "INS" && SVLEN >= 10000' ${THUTHSET_VCF} | bgzip -c > ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_INS_large.vcf.gz
        tabix --preset vcf ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_INS_large.vcf.gz
        bcftools view --include 'SVTYPE = "INS" && SVLEN >= 10000' ${WORKDIR}/${INVCF_OLD} | bgzip -c > ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_INS_large.vcf.gz
        tabix --preset vcf ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_INS_large.vcf.gz
        truvari bench \
            --base ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_truthset_INS_large.vcf.gz \
            --comp ${WORKDIR}/${OUTPUT_OLD}_${BENCH}/strat/strat_2bench_OLD_INS_large.vcf.gz \
            --output strat_old_ins_large \
            --passonly \
            --includebed ${INCLUDE_BED} \
            --refdist 1000 \
            --reference ${REFERENCE}
    fi

    cd ${WORKDIR}/
    if [[ "${INVCF_NEW}" != "none" ]]
    then
        # NEW
        truvari bench \
            --base ${THUTHSET_VCF} \
            --comp ${WORKDIR}/${INVCF_NEW} \
            --output ${OUTPUT_NEW}_${BENCH} \
            --passonly \
            --includebed ${INCLUDE_BED} \
            --refdist 1000 \
            --reference ${REFERENCE}
        # Stratification
        if [[ -d "${OUTPUT_NEW}_${BENCH}" ]];
        then
            cd ${OUTPUT_NEW}_${BENCH}
            if [[ ! -d "strat" ]];
            then
                mkdir strat
            fi
            cd strat
            # SVTYPE
            ## DEL
            bcftools view --include 'SVTYPE = "DEL"' ${THUTHSET_VCF} | bgzip -c > ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_DEL.vcf.gz
            tabix --preset vcf ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_DEL.vcf.gz
            bcftools view --include 'SVTYPE = "DEL"' ${WORKDIR}/${INVCF_NEW} | bgzip -c > ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_DEL.vcf.gz
            tabix --preset vcf ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_DEL.vcf.gz
            truvari bench \
                --base ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_DEL.vcf.gz \
                --comp ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_DEL.vcf.gz \
                --output strat_new_del \
                --passonly \
                --includebed ${INCLUDE_BED} \
                --refdist 1000 \
                --reference ${REFERENCE}
            ## DEL < 10kb
            bcftools view --include 'SVTYPE = "DEL" && SVLEN > -10000' ${THUTHSET_VCF} | bgzip -c > ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_DEL_small.vcf.gz
            tabix --preset vcf ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_DEL_small.vcf.gz
            bcftools view --include 'SVTYPE = "DEL" && SVLEN > -10000' ${WORKDIR}/${INVCF_NEW} | bgzip -c > ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_DEL_small.vcf.gz
            tabix --preset vcf ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_DEL_small.vcf.gz
            truvari bench \
                --base ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_DEL_small.vcf.gz \
                --comp ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_DEL_small.vcf.gz \
                --output strat_new_del_small \
                --passonly \
                --includebed ${INCLUDE_BED} \
                --refdist 1000 \
                --reference ${REFERENCE}
            ## DEL >= 10kb
            bcftools view --include 'SVTYPE = "DEL" && SVLEN <= -10000' ${THUTHSET_VCF} | bgzip -c > ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_DEL_large.vcf.gz
            tabix --preset vcf ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_DEL_large.vcf.gz
            bcftools view --include 'SVTYPE = "DEL" && SVLEN <= -10000' ${WORKDIR}/${INVCF_NEW} | bgzip -c > ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_DEL_large.vcf.gz
            tabix --preset vcf ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_DEL_large.vcf.gz
            truvari bench \
                --base ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_DEL_large.vcf.gz \
                --comp ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_DEL_large.vcf.gz \
                --output strat_new_del_large \
                --passonly \
                --includebed ${INCLUDE_BED} \
                --refdist 1000 \
                --reference ${REFERENCE}
            ## INS
            bcftools view --include 'SVTYPE = "INS"' ${THUTHSET_VCF} | bgzip -c > ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_INS.vcf.gz
            tabix --preset vcf ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_INS.vcf.gz
            bcftools view --include 'SVTYPE = "INS"' ${WORKDIR}/${INVCF_NEW} | bgzip -c > ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_INS.vcf.gz
            tabix --preset vcf ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_INS.vcf.gz
            truvari bench \
                --base ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_INS.vcf.gz \
                --comp ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_INS.vcf.gz \
                --output strat_new_ins \
                --passonly \
                --includebed ${INCLUDE_BED} \
                --refdist 1000 \
                --reference ${REFERENCE}
            ## INS < 10000
            bcftools view --include 'SVTYPE = "INS" && SVLEN < 10000' ${THUTHSET_VCF} | bgzip -c > ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_INS_small.vcf.gz
            tabix --preset vcf ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_INS_small.vcf.gz
            bcftools view --include 'SVTYPE = "INS" && SVLEN < 10000' ${WORKDIR}/${INVCF_NEW} | bgzip -c > ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_INS_small.vcf.gz
            tabix --preset vcf ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_INS_small.vcf.gz
            truvari bench \
                --base ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_INS_small.vcf.gz \
                --comp ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_INS_small.vcf.gz \
                --output strat_new_ins_small \
                --passonly \
                --includebed ${INCLUDE_BED} \
                --refdist 1000 \
                --reference ${REFERENCE}
            ## INS >= 10000
            bcftools view --include 'SVTYPE = "INS" && SVLEN >= 10000' ${THUTHSET_VCF} | bgzip -c > ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_INS_large.vcf.gz
            tabix --preset vcf ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_INS_large.vcf.gz
            bcftools view --include 'SVTYPE = "INS" && SVLEN >= 10000' ${WORKDIR}/${INVCF_NEW} | bgzip -c > ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_INS_large.vcf.gz
            tabix --preset vcf ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_INS_large.vcf.gz
            truvari bench \
                --base ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_truthset_INS_large.vcf.gz \
                --comp ${WORKDIR}/${OUTPUT_NEW}_${BENCH}/strat/strat_2bench_NEW_INS_large.vcf.gz \
                --output strat_new_ins_large \
                --passonly \
                --includebed ${INCLUDE_BED} \
                --refdist 1000 \
                --reference ${REFERENCE}
        fi
    fi
fi
