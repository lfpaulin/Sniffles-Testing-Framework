#!/usr/bin/env python
import json
import argparse
import pysam


# Version
version = 'v0.1.250310'


# Arguments ######################################
def get_arguments():
    main_help = ""
    parser = argparse.ArgumentParser(
             description="Sniffles2 testing Framework: sniffles bench",
             usage=main_help
    )
    subparsers = parser.add_subparsers(help=main_help, dest="command")
    #
    subparser = subparsers.add_parser("missed", help="Evaluate FN or TP")
    subparser.add_argument('-v', '--vcf1', type=str, required=True, dest='vcf1', default="", 
                        help='VCF file result of truvari FN/TP for the previous version of Sniffles')
    subparser.add_argument('-w', '--vcf2', type=str, required=True, dest='vcf2', default="", 
                        help='VCF file result of truvari FN/TP for the new version of Sniffles')
    subparser.add_argument('-n', '--noqc1', type=str, required=False, dest='noqc1', default="", 
                        help='VCF noqc for the previous version of Sniffles')
    subparser.add_argument('-m', '--noqc2', type=str, required=False, dest='noqc2', default="", 
                        help='VCF noqc for the new version of Sniffles')
    #
    subparser = subparsers.add_parser("errors", help="Evaluate FP")
    subparser.add_argument('-v', '--vcf1', type=str, required=True, dest='vcf1', default="", 
                        help='VCF file result of truvari FN/TP for the previous version of Sniffles')
    subparser.add_argument('-w', '--vcf2', type=str, required=True, dest='vcf2', default="", 
                        help='VCF file result of truvari FN/TP for the new version of Sniffles')

    # GT difference
    subparser = subparsers.add_parser("gt_comp", help="Compare GT")
    subparser.add_argument('-b', '--vcfb1', type=str, required=True, dest='vcfb1', default="", 
                           help='TP base from truvari from previous Sniffles2 version')
    subparser.add_argument('-B', '--vcfb2', type=str, required=True, dest='vcfb2', default="", 
                           help='TP base from truvari from new Sniffles2 version')
    subparser.add_argument('-c', '--vcfc1', type=str, required=False, dest='vcfc1', default="", 
                           help='TP base from truvari from previous Sniffles2 version')
    subparser.add_argument('-C', '--vcfc2', type=str, required=False, dest='vcfc2', default="", 
                           help='TP base from truvari from new Sniffles2 version')

    # SUPPORT v DV
    subparser = subparsers.add_parser("supp_dv", help="SUPPORT v DV counts")
    subparser.add_argument('-v', '--vcf', type=str, required=True, dest='vcf', default="", 
                           help='Compare SUPPORT and SV values, output non match SVs')


    args = parser.parse_args()
    return args
# ################################################


# MISC ###########################################
# gt translate
def gt_translate(gt: tuple) -> str:
    gts = {
        (0,0): "0/0",
        (0,1): "0/1",
        (1,0): "0/1",
        (1,1): "1/1",
        (None,1): "0/1",
        (1,None): "0/1",
    }
    return gts[gt]


# long INS
def sv_long_ins(sv: pysam.VariantRecord, long_ins: int = 2500) -> bool:
    if "INS" == sv.info.get("SVTYPE"):
        if long_ins <= sv.info.get("SVLEN"):
            return True
    return False
# ################################################


# Missing ########################################
def test_missing(user_args):
    if "" == user_args.noqc1 or "" == user_args.noqc2:
        test_missing_simple(user_args)
    else:
        test_missing_full(user_args)


def test_missing_simple(user_args):
    fn_current = pysam.VariantFile(user_args.vcf1)
    fn_dev = pysam.VariantFile(user_args.vcf2)
    # old
    current_missed = []
    for sv in fn_current.fetch():
        current_missed.append(sv.id)
    fn_current.close()
    # new
    dev_missed = []
    dev_missed_x2 = []
    for sv in fn_dev.fetch():
        dev_missed.append(sv.id)
        if sv.id not in dev_missed:
            dev_missed_x2.append(sv.id)
    fn_dev.close()
    print(len(current_missed), len(dev_missed), len(dev_missed_x2))
    print(dev_missed_x2) if len(dev_missed_x2) > 0 else None


def test_missing_full(user_args):
    fn_current = pysam.VariantFile(user_args.vcf1)
    fn_dev = pysam.VariantFile(user_args.vcf2)
    # old
    current_missed = {}
    for sv in fn_current.fetch():
        current_missed[sv.id] = [sv.contig, sv.pos, sv.info.get("SVTYPE"), sv.info.get("SVLEN")]
    fn_current.close()
    # new
    dev_missed = {}
    dev_missed_list = []
    dev_missed_x2 = []
    for sv in fn_dev.fetch():
        dev_missed[sv.id] = [sv.contig, sv.pos, sv.info.get("SVTYPE"), sv.info.get("SVLEN")]
        dev_missed_list.append(sv.id)
        if sv.id not in dev_missed_list:
            dev_missed_x2.append(sv.id)
    fn_dev.close()
    print(len(current_missed.keys()), len(dev_missed_list), len(dev_missed_x2))
    print(dev_missed_x2) if len(dev_missed_x2) > 0 else None
    # NO-QC
    padding = 1000
    svlen_diff = 100
    add_svlen = ["DEL", "DUP", "INV"]
    print(dev_missed_list[:10])
    for x in dev_missed_list[:10]:
        dev_missed_x2.append(x) 
    
    if len(dev_missed_x2) > 0:
        noqc_dev = pysam.VariantFile(user_args.noqc2)
        for miss_id in dev_missed_x2:
            [contig, pos, svtype, svlen] = dev_missed[miss_id]
            end = pos + svlen if svtype in add_svlen else pos + 1
            region = f'{contig}:{pos-padding}-{end-padding}'
            print(region)
            noqc_dev.seek(0)
            for svnoqc in noqc_dev.fetch(region=region):
                if svnoqc.info.get("SVTYPE") == svtype and abs(svnoqc.info.get("SVLEN") - svlen) <= svlen_diff:
                    print(svnoqc)
        noqc_dev.close()
# ################################################


# Errors #########################################
def test_errors(user_args):
    print(1)
# ################################################


# SUPP v DV ######################################
def test_supp_dv(user_args):
    # currently long INS have different way to compute SUPPORT, thus will not match SV
    vcf = pysam.VariantFile(user_args.vcf)
    sample_name = ""
    for sv in vcf.fetch():
        sample_name = sv.samples.keys()[0]
        break
    vcf.seek(0)
    count_match = 0
    count_nomatch = 0
    count_long_ins = 0
    for sv in vcf.fetch():
        supp = sv.info.get("SUPPORT")
        dv = sv.samples.get(sample_name).get("DV")
        is_long_ins = sv_long_ins(sv)
        if dv != supp and not is_long_ins:
            count_nomatch += 1
            print(f'{sv.contig}:{sv.pos}\t{sv.id}\t{supp}\t{dv}')
        else:
            if is_long_ins:
                count_long_ins += 1
            else:
                count_match += 1
    print(f'SUPPORT == DV: {count_match}\nSUPPORT =/= DV: {count_nomatch}\nlong INS: {count_long_ins}')
    vcf.close()
# ################################################


# GT comp ########################################
def test_gt_compare(user_args):
    wrong_both = []
    wrong_old = []
    wrong_new = []
    wrong_both_mid = []
    wrong_old_mid = []
    wrong_new_mid = []
    truv_old = pysam.VariantFile(user_args.vcfb1)
    sampleb1 = ""
    truv_new = pysam.VariantFile(user_args.vcfb2)
    sampleb2 = ""
    for sv in truv_old.fetch():
        if sampleb1 == "":
            sampleb1 = sv.samples.keys()[0]
        if sv.info.get("GTMatch") > 0:
            print_1st = 0
            wrong_old.append(sv.id)
            wrong_old_mid.append(sv.info.get("MatchId"))
    for sv in truv_new.fetch():
        if sampleb2 == "":
            sampleb2 = sv.samples.keys()[0]
        if sv.info.get("GTMatch") > 0:
            print_1st = 0
            wrong_new.append(sv.id)
            wrong_new_mid.append(sv.info.get("MatchId"))
            if sv.id in wrong_old:
                wrong_both.append(sv.id)
                wrong_both_mid.append(sv.info.get("MatchId"))
    wrong_old_only_mid = []
    wrong_old_only_svid = []
    wrong_new_only_mid = []
    wrong_new_only_svid = []
    for svid1, mid1 in zip(wrong_old, wrong_old_mid):
        if svid1 not in wrong_both:
            wrong_old_only_mid.append(mid1)
            wrong_old_only_svid.append(svid1)
    for svid2, mid2 in zip(wrong_new, wrong_new_mid):
        if svid2 not in wrong_both:
            wrong_new_only_mid.append(mid2)
            wrong_new_only_svid.append(svid2)
    # output 1
    print(f'both: {len(wrong_both)}\nold only: {len(wrong_old_only_svid)}\nnew only: {len(wrong_new_only_svid)}\n'
          f'old: {len(wrong_old)}\nnew: {len(wrong_new)}')
    truv_old.close()
    truv_new.close()
    # output 2
    do_comp1 = False if "" == user_args.vcfc1 else True
    do_comp2 = False if "" == user_args.vcfc2 else True
    samplen = ""
    if do_comp1 and not do_comp2:
        print("#")
        truv_old = pysam.VariantFile(user_args.vcfb1)
        snf2_old = pysam.VariantFile(user_args.vcfc1)
        for sv in snf2_old.fetch():
            samplen = sv.samples.keys()[0]
        snf2_old.seek(0)
        for sv, bn in zip(snf2_old.fetch(), truv_old.fetch()):
            mid = sv.info.get("MatchId")
            if mid in wrong_old_only_mid:
                gt = gt_translate(sv.samples.get(samplen).get("GT"))
                dr = sv.samples.get(samplen).get("DR")
                dv = sv.samples.get(samplen).get("DV")
                svlen = sv.info.get("SVLEN")
                gtb = gt_translate(bn.samples.get(sampleb1).get("GT"))
                midstr = ",".join(mid)
                supp = sv.info.get("SUPPORT")
                print(f'{sv.contig}\t{sv.pos}\t{sv.id}|{svlen}\t{supp}\t{gt}|{dr}|{dv}\t{gtb}\t{midstr}')
        snf2_old.close()
        truv_old.close()
    elif do_comp2 and not do_comp1:
        print("#")
        truv_new = pysam.VariantFile(user_args.vcfb2)
        snf2_new = pysam.VariantFile(user_args.vcfc2)
        for sv in snf2_new.fetch():
            samplen = sv.samples.keys()[0]
        snf2_new.seek(0)
        for sv, bn in zip(snf2_new.fetch(), truv_new.fetch()):
            mid = sv.info.get("MatchId")
            if mid in wrong_new_only_mid:
                gt = gt_translate(sv.samples.get(samplen).get("GT"))
                dr = sv.samples.get(samplen).get("DR")
                dv = sv.samples.get(samplen).get("DV")
                svlen = sv.info.get("SVLEN")
                gtb = gt_translate(bn.samples.get(sampleb2).get("GT"))
                midstr = ",".join(mid)
                supp = sv.info.get("SUPPORT")
                print(f'{sv.contig}\t{sv.pos}\t{sv.id}|{svlen}\t{supp}\t{gt}|{dr}|{dv}\t{gtb}\t{midstr}')
        snf2_new.close()
        truv_new.close()
    elif do_comp2 and do_comp1:
        snf2_old = pysam.VariantFile(user_args.vcfc1)
        snf2_new = pysam.VariantFile(user_args.vcfc2)
        sampleno, samplenn = "", ""
        for sv in snf2_old.fetch():
            sampleno = sv.samples.keys()[0]
        snf2_old.seek(0)
        for sv in snf2_new.fetch():
            samplenn = sv.samples.keys()[0]
        snf2_new.seek(0)
        truv_old = pysam.VariantFile(user_args.vcfb1)
        truv_new = pysam.VariantFile(user_args.vcfb2)
        print("# good GT in new bad GT in old")
        print("Region\tSVTYPE\tSVLEN\tSUPPo\tGTo\tGTbench\ttSUPPn\tGTn")
        for sv, bn in zip(snf2_old.fetch(), truv_old.fetch()):
            mid = sv.info.get("MatchId")
            if mid in wrong_old_only_mid:
                svtype = sv.info.get("SVTYPE")
                svlen = sv.info.get("SVLEN")
                supp = sv.info.get("SUPPORT")
                vaf = round(sv.info.get("VAF"), 3)
                dr = sv.samples.get(sampleno).get("DR")
                dv = sv.samples.get(sampleno).get("DV")
                gt = gt_translate(sv.samples.get(sampleno).get("GT"))
                gtb = gt_translate(bn.samples.get(sampleb1).get("GT"))
                # check other version
                reg = f'{sv.contig}:{sv.pos}-{sv.pos+1}' if "INS" == svtype else f'{sv.contig}:{sv.pos}-{sv.pos+abs(svlen)}'
                truv_new.seek(0)
                sv2, bn2 = "", ""
                for bn2 in truv_new.fetch():
                    if bn2.id == bn.id:
                        break
                snf2_new.seek(0)
                for sv2 in snf2_new.fetch(region=reg):
                    if sv2.info.get("MatchId") == bn2.info.get("MatchId"):
                        svlen2 = sv2.info.get("SVLEN")
                        supp2 = sv2.info.get("SUPPORT")
                        dr2 = sv2.samples.get(samplenn).get("DR")
                        dv2 = sv2.samples.get(samplenn).get("DV")
                        gt2 = gt_translate(sv2.samples.get(samplenn).get("GT"))
                        vaf2 = round(sv2.info.get("VAF"), 3)
                        print(f'{reg}\t{svtype}\t{svlen}|{svlen2}\t{supp}\t{gt}|{dr}|{dv}|{vaf}\t{gtb}\t'
                                f'{supp2}\t{gt2}|{dr2}|{dv2}|{vaf2}\t{round(vaf-vaf2, 3)}|{supp-supp2}')
                        break
        print("# good GT in old bad GT in new")
        print("Region\tSVTYPE\tSVLEN\tSUPPn\tGTn\tGTbench\ttSUPPo\tGTo")
        for sv, bn in zip(snf2_new.fetch(), truv_new.fetch()):
            mid = sv.info.get("MatchId")
            if mid in wrong_new_only_mid:
                svtype = sv.info.get("SVTYPE")
                svlen = sv.info.get("SVLEN")
                supp = sv.info.get("SUPPORT")
                vaf = round(sv.info.get("VAF"), 3)
                dr = sv.samples.get(samplenn).get("DR")
                dv = sv.samples.get(samplenn).get("DV")
                gt = gt_translate(sv.samples.get(samplenn).get("GT"))
                gtb = gt_translate(bn.samples.get(sampleb2).get("GT"))
                # check other version
                reg = f'{sv.contig}:{sv.pos}-{sv.pos+1}' if "INS" == svtype else f'{sv.contig}:{sv.pos}-{sv.pos+abs(svlen)}'
                truv_old.seek(0)
                sv2, bn2 = "", ""
                for bn2 in truv_old.fetch():
                    if bn2.id == bn.id:
                        break
                snf2_old.seek(0)
                for sv2 in snf2_old.fetch(region=reg):
                    if sv2.info.get("MatchId") == bn2.info.get("MatchId"):
                        svlen2 = sv2.info.get("SVLEN")
                        supp2 = sv2.info.get("SUPPORT")
                        dr2 = sv2.samples.get(sampleno).get("DR")
                        dv2 = sv2.samples.get(sampleno).get("DV")
                        gt2 = gt_translate(sv2.samples.get(sampleno).get("GT"))
                        vaf2 = round(sv2.info.get("VAF"), 3)
                        print(f'{reg}\t{svtype}\t{svlen}|{svlen2}\t{supp}\t{gt}|{dr}|{dv}|{vaf}\t{gtb}\t'
                                f'{supp2}\t{gt2}|{dr2}|{dv2}|{vaf2}\t{round(vaf-vaf2, 3)}|{supp-supp2}')
                        break
        

    else:
        pass
# ################################################
    

def main():
    params = get_arguments()
    if "missed" == params.command:
        test_missing(params)
    elif "errors" == params.command:
        test_errors(params)
    elif "supp_dv" == params.command:
        test_supp_dv(params)
    elif "gt_comp" == params.command:
        test_gt_compare(params)
    else:
        pass


if __name__ == "__main__":
    main()