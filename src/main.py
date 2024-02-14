#!/usr/bin/env python3
import sys 
import json 
import config
from benchmarks.merge_bench import PopMergeTestParam
from benchmarks.merge_bench import MergeTestParam
from benchmarks.merge_bench import MergeXLBench
from benchmarks.merge_bench import MergeBench
from benchmarks.giab_bench import GIABBenchParam
from benchmarks.giab_bench import GIABBench
from benchmarks.mendelian import TrioBenchParam
from benchmarks.mendelian import TrioBench
from utils import generate_id


FRAMEWORK_SRC_PATH = "/".join(__file__.split("/")[:-1])


# ONT or HiFi
def giab_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    giab_params = GIABBenchParam()
    params_json = json.load(open(user_args.json, "r"))
    giab_params.set_parameters_from_json(params_json)
    # becnhmark
    giabsv_bench = GIABBench(giab_params, bench_id, FRAMEWORK_SRC_PATH)
    giabsv_bench.bench()


# ONT or HiFi
def cmrg_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    cmrg_params = GIABBenchParam()
    params_json = json.load(open(user_args.json, "r"))
    cmrg_params.set_parameters_from_json(params_json)
    # becnhmark
    cmrgsv_bench = GIABBench(cmrg_params, bench_id, FRAMEWORK_SRC_PATH)
    cmrgsv_bench.bench()


# ONT or HiFi
def trio_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    trio_params = TrioBenchParam()
    params_json = json.load(open(user_args.json, "r"))
    trio_params.set_parameters_from_json(params_json)
    # becnhmark
    triosv_bench = TrioBench(trio_params, bench_id, FRAMEWORK_SRC_PATH)
    triosv_bench.bench()


# ONT (truvari)
def combine_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    merge_params = MergeTestParam()
    params_json = json.load(open(user_args.json, "r"))
    merge_params.set_parameters_from_json(params_json)
    # becnhmark
    merge_bench = MergeBench(merge_params, bench_id, FRAMEWORK_SRC_PATH)
    merge_bench.bench()


# ONT (Mike)
def population_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    pop_merge_params = PopMergeTestParam()
    params_json = json.load(open(user_args.json, "r"))
    pop_merge_params.set_parameters_from_json(params_json)
    # becnhmark
    pop_bench = MergeXLBench(pop_merge_params, bench_id, FRAMEWORK_SRC_PATH)
    pop_bench.bench()


# ONT
def mosaic_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    mosaic_params = GIABBenchParam()
    params_json = json.load(open(user_args.json, "r"))
    mosaic_params.set_parameters_from_json(params_json)
    # becnhmark
    mosaicsv_bench = GIABBench(mosaic_params, bench_id, FRAMEWORK_SRC_PATH)
    mosaicsv_bench.bench()


# ONT and HiFi
def full_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    params_json = json.load(open(user_args.json, "r"))
    # NOTE: GIAB ONT
    giab_params = GIABBenchParam()
    giab_params.set_parameters_from_json(params_json["giab"])
    giabsv_bench = GIABBench(giab_params, bench_id, FRAMEWORK_SRC_PATH)
    giabsv_bench.bench()
    # NOTE: CMRG ONT
    cmrg_params = GIABBenchParam()
    cmrg_params.set_parameters_from_json(params_json["cmrg"])
    cmrgsv_bench = GIABBench(cmrg_params, bench_id, FRAMEWORK_SRC_PATH)
    cmrgsv_bench.bench()
    # NOTE: GIAB HiFI
    giab_hifi_params = GIABBenchParam()
    giab_hifi_params.set_parameters_from_json(params_json["giab_hifi"])
    giabsv_hifi_bench = GIABBench(giab_hifi_params, bench_id, FRAMEWORK_SRC_PATH)
    giabsv_hifi_bench.bench()
    # NOTE: CMRG HiFi
    cmrg_hifi_params = GIABBenchParam()
    cmrg_hifi_params.set_parameters_from_json(params_json["cmrg_hifi"])
    cmrgsv_hifi_bench = GIABBench(cmrg_hifi_params, bench_id, FRAMEWORK_SRC_PATH)
    cmrgsv_hifi_bench.bench()
    # NOTE: Mendelian
    trio_params = TrioBenchParam()
    trio_params.set_parameters_from_json(params_json["mendelian"])
    triosv_bench = TrioBench(trio_params, bench_id, FRAMEWORK_SRC_PATH)
    triosv_bench.bench()
    # NOTE: Mendelian HiFi
    trio_hifi_params = TrioBenchParam()
    trio_hifi_params.set_parameters_from_json(params_json["mendelian_hifi"])
    triosv_hifi_bench = TrioBench(trio_hifi_params, bench_id, FRAMEWORK_SRC_PATH)
    triosv_hifi_bench.bench()
    # NOTE: Merge
    merge_params = MergeTestParam()
    merge_params.set_parameters_from_json(params_json["merge"])
    merge_bench = MergeBench(merge_params, bench_id, FRAMEWORK_SRC_PATH)
    merge_bench.bench()
    # NOTE: Mosaic
    mosaic_params = GIABBenchParam()
    mosaic_params.set_parameters_from_json(params_json["mosaic"])
    # TODO: finish BAM
    """
      we have the unique SVs for HG002 now we need the read names +
      the coverage for HG00733 and the specific regions we are 
      interested in
    """
    # mosaicsv_bench = GIABBench(mosaic_params, bench_id, FRAMEWORK_SRC_PATH)
    # mosaicsv_bench.bench()


def main():
    # Get arguments
    user_args, main_help = config.get_arguments()
    command = user_args.command

    if command == "giab":
        giab_bench(user_args)
    elif command == "cmrg":
        cmrg_bench(user_args)
    elif command == "mendelian":
        trio_bench(user_args)
    elif command == "merge":
        combine_bench(user_args)
    elif command == "mosaic":
        mosaic_bench(user_args)
    elif command == "population":
        population_bench(user_args)
    elif command == "bench":
        full_bench(user_args)
    else:
        print(main_help)
        sys.exit(1)

if __name__ == "__main__": 
    main()