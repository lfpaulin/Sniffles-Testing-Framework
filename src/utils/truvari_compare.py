#!/usr/bin/python
import json
import argparse


# Version
version = 'v0.1'


# Arguments
def get_arguments():
    main_help = """
    truvari compare
        -p/--prev    JSON file result of truvari prev version
        -n/--new     JSON file result of truvari new version

    """
    parser = argparse.ArgumentParser(
             description="Sniffles2 testing Framework: truvari compare",
             usage=main_help
    )
    parser.add_argument('-p', '--prev', type=str, required=True, dest='json_prev', default="", help='')
    parser.add_argument('-n', '--new', type=str, required=True, dest='json_new', default="", help='')

    args = parser.parse_args()
    return args, main_help


info_needed_int = ("TP-comp", "FP", "FN")
info_needed_float = ("precision", "recall", "f1", "gt_concordance")

def main():
    params, _ = get_arguments()
    compare(params.json_prev, params.json_new)


def compare(snf_truvari_old, snf_truvari_new):
    snf2_old = open(snf_truvari_old)
    snf2_new = open(snf_truvari_new)
    snf2_old_dict = json.load(snf2_old)
    snf2_new_dict = json.load(snf2_new)
    for info in info_needed_int:
        if type(snf2_new_dict[info]) == type(0) and type(snf2_old_dict[info]) == type(0):
            int_val_diff = (snf2_new_dict[info]-snf2_old_dict[info])
        else:
            int_val_diff = f'{snf2_new_dict[info]}-{snf2_old_dict[info]}'
        print(f'{info}\t{snf2_old_dict[info]}\t{snf2_new_dict[info]}\t{int_val_diff}')
    for info in info_needed_float:
        if type(snf2_new_dict[info]) == type(0.0) and type(snf2_old_dict[info]) == type(0.0):
            float_val_diff = f'{(snf2_new_dict[info]-snf2_old_dict[info]):.4f}'
            print(f'{info}\t{snf2_old_dict[info]:.4f}\t{snf2_new_dict[info]:.4f}\t{float_val_diff}')
        else:
            float_val_diff = f'{snf2_new_dict[info]}-{snf2_old_dict[info]}'
            print(f'{info}\t{snf2_old_dict[info]}\t{snf2_new_dict[info]}\t{float_val_diff}')


if __name__ == "__main__":
    main()