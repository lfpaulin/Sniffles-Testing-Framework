#!/usr/bin/env python
import os
import sys
import json
import argparse


# Version
version = 'v0.2'


# Arguments
def get_arguments():
    main_help = """
    truvari compare
        -p/--prev    Direcorty of the benchamrk (truvari) from prev version
        -n/--new     Direcorty of the benchamrk (truvari) from new version
        -r/--refine  Flag that states use refine output

    """
    parser = argparse.ArgumentParser(
             description="Sniffles2 testing Framework: truvari compare",
             usage=main_help
    )
    parser.add_argument('-p', '--prev', type=str, required=True, dest='bench_prev', default="", help='')
    parser.add_argument('-n', '--new', type=str, required=True, dest='bench_new', default="", help='')
    parser.add_argument('-r', '--refine', action="store_true", required=False, dest='refine', help='')

    args = parser.parse_args()
    return args, main_help


def main():
    params, _ = get_arguments()
    prev_file = get_bench(params.bench_prev, params.refine)
    new_file = get_bench(params.bench_new, params.refine)
    compare(prev_file, new_file, params.refine)


def get_bench(bench_dir: str, use_refine: bool = False):
    refine_bench = "refine.variant_summary.json"
    default_bench = "summary.json"
    if use_refine:
        if refine_bench in os.listdir(bench_dir):
            return f'{os.path.abspath(bench_dir)}/{refine_bench}'
        else:
            sys.stderr.write(f'[ERROR] required file {refine_bench} not found for "refine" benchmark comparison')
            sys.exit(1)
    if default_bench in os.listdir(bench_dir):
        return f'{os.path.abspath(bench_dir)}/{default_bench}'
    else:
        sys.stderr.write(f'[ERROR] required file {default_bench} not found needed for benchmark comparison')
        sys.exit(1)


def compare(snf_truvari_old: str, snf_truvari_new: str, use_refine: bool = False):
    # uses summary.json or refine.variant_summary.json
    info_needed_int = ("TP-comp", "FP")
    info_needed_float = ("precision", "recall", "f1", "gt_concordance")
    if use_refine:
        info_needed_float = info_needed_float[:-1]
    snf2_old = open(snf_truvari_old)
    snf2_new = open(snf_truvari_new)
    snf2_old_dict = json.load(snf2_old)
    snf2_new_dict = json.load(snf2_new)
    print(f'STAT\tvPrevious\tvNew\tDifference')
    for info in info_needed_int:
        if type(snf2_new_dict[info]) is int and type(snf2_old_dict[info]) is int:
            int_val_diff = (snf2_new_dict[info]-snf2_old_dict[info])
        else:
            int_val_diff = f'{snf2_new_dict[info]}-{snf2_old_dict[info]}'
        print(f'{info}\t{snf2_old_dict[info]}\t{snf2_new_dict[info]}\t{int_val_diff}')
    for info in info_needed_float:
        if type(snf2_new_dict[info]) is float and type(snf2_old_dict[info]) is float:
            float_val_diff = f'{(snf2_new_dict[info]-snf2_old_dict[info]):.4f}'
            print(f'{info}\t{snf2_old_dict[info]:.4f}\t{snf2_new_dict[info]:.4f}\t{float_val_diff}')
        else:
            float_val_diff = f'{snf2_new_dict[info]}-{snf2_old_dict[info]}'
            print(f'{info}\t{snf2_old_dict[info]}\t{snf2_new_dict[info]}\t{float_val_diff}')


if __name__ == "__main__":
    main()