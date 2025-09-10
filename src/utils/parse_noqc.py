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
    truvari compare
        -v/--vcf     no-qc output file
        -o/--out     output (default is stdout)

    """
    parser = argparse.ArgumentParser(
             description="Sniffles2 testing Framework: truvari compare",
             usage=main_help
    )
    parser.add_argument('-v', '--vcf', type=str, required=True, dest='vcf', default="", help='')
    parser.add_argument('-o', '--out', type=str, required=False, dest='out', default="", help='')

    args = parser.parse_args()
    return args, main_help


def main():
    params, _ = get_arguments()
    output: VCF
    vcf_read = VCF(params.vcf)
    if "" != params.out:
        output = VCF(params.out, "w", header=vcf_read.header)
    else:
        output = VCF('-', "w", header=vcf_read.header)
    parse_noqc(vcf_read, output)


def parse_noqc(vcf: VCF, out: VCF):
    # --include 'SUPPORT > 1 && (SVTYPE = 'INS' || SVTYPE = 'DEL') 
    # change FILTERL MOSAIC PASS to MOSAIC_VAF'
    sv: SV
    min_support = 2
    for sv in vcf.fetch():
        svtype = sv.info.get("SVTYPE")
        if svtype in ["DEL", "INS"] and sv.info.get("SUPPORT") >= min_support:
            is_mosaic = sv.info.get("MOSAIC")
            if is_mosaic:
                [filt_obj] = sv.filter.items()
                f, v = filt_obj
                if "PASS" == f:
                    sv.filter.add("MOSAIC_VAF")
            out.write(sv)


if __name__ == "__main__":
    main()