#!/usr/bin/env python
import os
import sys
import argparse
from pysam import VariantFile as VCF
from pysam import VariantRecord as SV


# Version
version = 'v0.1'


# Arguments
def get_arguments():
    main_help = """
    phasing QC
        -v/--vcf     Sniffles single sample call, phased

    """
    parser = argparse.ArgumentParser(
             description="Sniffles2 testing Framework: phasing QC",
             usage=main_help
    )
    parser.add_argument('-v', '--vcf', type=str, required=True, dest='vcf', default="", help='')

    args = parser.parse_args()
    return args, main_help


def main():
    params, _ = get_arguments()
    assert os.path.exists(params.vcf), f'File "{params.vcf}" does not exisit'
    vcf = VCF(params.vcf)
    sv: SV
    vcf.seek(0)
    for sv in vcf.fetch():
        svtype = sv.info.get("SVTYPE")
        phase_info = sv.info.get("PHASE")
        hp, ps, hp_supp, ps_supp, hp_filt, ps_filt = phase_info
        sample_name, sample_gt = sv.samples.items().pop()
        gt = sample_gt.get("GT")
        if gt in {(0,1), (1,0)} and hp_filt == "PASS" and "BND" != svtype:
            assert (hp == "1" and gt == (1,0) or hp == "2" and gt == (0,1)), f'{sv.id} has incorrect phasing (HP): {hp} {gt}'
        gt_ps = sample_gt.get("PS")
        if ps_filt == "PASS" and hp_filt == "PASS" and "BND" != svtype: 
            assert(str(ps) == str(gt_ps)), f'{sv.id} has incorrect PS, {ps} | {gt_ps}'
    vcf.close()
    print("No phasing inconsitencies detected")


if __name__ == "__main__":
    main()
