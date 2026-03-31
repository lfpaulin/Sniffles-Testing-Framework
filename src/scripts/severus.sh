#!/bin/bash
#SBATCH --ntasks=8
#SBATCH --mem=32Gb
#SBATCH --time=3-00:00:00
#SBATCH --partition=medium
#SBATCH --account=proj-fs0007

. /stornext/snfs130/fritz/luis/miniconda3_py310_24_3/etc/profile.d/conda.sh
conda activate severus_env

# self.args_ont.tandem_rep,
# pon_file,
# self.args_ont.bam,
# self.args_pb.bam

TANDEM_REP=$1
BAM_ONT=$2
BAM_PB=$3
NTASKS=8

# ont
gnu-time --verbose --output time_ont.log severus \
    --target-bam ${BAM_ONT} \
    --out-dir ont \
    --vntr-bed  ${TANDEM_REP} \
    --threads ${NTASKS}  \
    --phasing-vcf phased.vcf \

# pb
gnu-time --verbose --output time_pb.log severus \
    --target-bam ${BAM_PB} \
    --out-dir pb \
    --vntr-bed  ${TANDEM_REP} \
    --threads ${NTASKS}  \
    --phasing-vcf phased.vcf \
