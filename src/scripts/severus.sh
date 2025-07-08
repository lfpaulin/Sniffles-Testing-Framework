#!/bin/bash
#SBATCH --ntasks=8
#SBATCH --mem=32Gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0002

. /stornext/snfs130/fritz/luis/miniconda3_py310_24_3/etc/profile.d/conda.sh
conda activate severus_env

# self.args_ont.tandem_rep,
# pon_file,
# self.args_ont.bam,
# self.args_pb.bam

TANDEM_REP=$1
PON_FILE=$2
BAM_ONT=$3
BAM_PB=$4
NTASKS=8

# ont
severus \
    --target-bam ${BAM_ONT} \
    --out-dir ont \
    --vntr-bed  ${TANDEM_REP} \
    --threads ${NTASKS}  \
    --PON ${PON_FILE}
    # --phasing-vcf phased.vcf \

# pb
severus \
    --target-bam ${BAM_PB} \
    --out-dir pb \
    --vntr-bed  ${TANDEM_REP} \
    --threads ${NTASKS}  \
    --PON ${PON_FILE}
    # --phasing-vcf phased.vcf \
