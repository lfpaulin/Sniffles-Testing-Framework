#!/usr/bin/env python
import os
import argparse
from pysam import VariantFile as VCF
from pysam import VariantRecord as SV


# Version
version = 'v0.1'
HETS = {(1,0), (0,1)}

# Arguments
def get_arguments():
    main_help = """
    phasing QC
        -v/--vcf     Sniffles single sample call, phased/unphased

    """
    parser = argparse.ArgumentParser(
             description="Sniffles2 testing Framework: SV position QC",
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
    curr: SV
    got_current= False
    for sv in vcf.fetch():
        # skip BND if contig == contig2
        svtype = sv.info.get("SVTYPE")
        # if svtype == "BND":
        #     if sv.contig == sv.info.get("CHR2"):
        #         continue
        # skip large(r) INS
        # if svtype == "INS":
        #     if sv.info.get("SVLEN") > 10000:
        #         continue

        if not got_current:
            curr = sv
            got_current = True
        else:
            csvtype = curr.info.get("SVTYPE")
            # svtype = sv.info.get("SVTYPE")
            if sv.contig == curr.contig and sv.pos == curr.pos:
                # overall
                contig = curr.contig
                pos = curr.pos

                # current
                cchr2 = curr.info.get("CHR2") if "BND" == csvtype else None
                csvlen = curr.info.get("SVLEN") if csvtype != "BND" else cchr2
                _, tmpgt = curr.samples.items().pop()
                cgt = tmpgt.get("GT")
                chp, _, _, _, chpf, _ = curr.info.get("PHASE")

                # next
                schr2 = sv.info.get("CHR2") if "BND" == svtype else None
                svlen = sv.info.get("SVLEN") if svtype != "BND" else schr2
                _, tmpgt = sv.samples.items().pop()
                sgt = tmpgt.get("GT")
                shp, _, _, _, shpf, _ = sv.info.get("PHASE")

                # skip hets different hap
                if sgt in HETS and cgt in HETS:
                    # HAP1 v HAP2
                    if cgt != sgt and shp != chp:
                        continue
                    # HAP1/2 v HAP0
                    if cgt == sgt and shp != chp:
                        continue
                    # HAP0 v HAP0
                    if cgt == sgt and shp == chp and "0" == chp:
                        continue
                    # BNDs anchoring to different contigs
                    if "BND" == csvtype and cchr2 != schr2:
                        continue

                    if chp != shp and "FAIL" in {chpf, shpf}:
                        continue
                
                collision_type = "SAME" if svtype == csvtype else "DIFF"
                print(f'{collision_type}:', f'{contig}:{pos}', (curr.id, cgt, csvlen, chp, chpf), (sv.id, sgt, svlen, shp, shpf))
            curr = sv

    vcf.close()
    # print("No position inconsitencies detected")


if __name__ == "__main__":
    main()
