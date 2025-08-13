#!/usr/bin/env python3
import sys 
import json 
import config
import time
from benchmarks.merge_bench import PopMergeTestParam
from benchmarks.merge_bench import MergeTestParam
from benchmarks.merge_bench import MergeXLBench
from benchmarks.merge_bench import MergeBench
from benchmarks.giab_bench import *
from benchmarks.mendelian import TrioBenchParam
from benchmarks.mendelian import TrioBench
from benchmarks.genotyper import GenotyperParam
from benchmarks.genotyper import GenotyperBench
from benchmarks.snf_threads import SNFThreads, SNFThreadsParams
from benchmarks.ont_large_deldup import ONTLargeDelDup, ONTLargeDelDupParams
from utils import generate_id
from utils.logger import setup_log

my_logger = setup_log(__name__, True)
FRAMEWORK_SRC_PATH = "/".join(__file__.split("/")[:-1])


# ONT or HiFi
def giab_bench(user_args):
    my_logger.info(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    giab_params = GIABBenchParam()
    params_json = json.load(open(user_args.json, "r"))
    bdir, data_dir, ref = params_json["base_dir"], params_json["data_dir"], params_json["reference"]
    giab_params.set_parameters_from_json(params_json["hg002_ont_hg38_5khz"], bdir, data_dir, ref)
    # becnhmark
    giabsv_bench = GIABBench(giab_params, bench_id, FRAMEWORK_SRC_PATH)
    giabsv_bench.bench()


# ONT or HiFi
def trio_bench(user_args):
    my_logger.info(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    trio_params = TrioBenchParam()
    params_json = json.load(open(user_args.json, "r"))
    bdir, data_dir, ref = params_json["base_dir"], params_json["data_dir"], params_json["reference"]
    trio_params.set_parameters_from_json(params_json["mendelian_ont"], bdir, data_dir, ref)
    # becnhmark
    triosv_bench = TrioBench(trio_params, bench_id, FRAMEWORK_SRC_PATH)
    triosv_bench.bench()


# ONT (truvari)
def combine_bench(user_args):
    my_logger.info(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    merge_params = MergeTestParam()
    params_json = json.load(open(user_args.json, "r"))
    bdir, data_dir, ref = params_json["base_dir"], params_json["data_dir"], params_json["reference"]
    merge_params.set_parameters_from_json(params_json["merge"], bdir, data_dir, ref)
    # becnhmark
    merge_bench = MergeBench(merge_params, bench_id, FRAMEWORK_SRC_PATH)
    merge_bench.bench()


# ONT
def mosaic_bench(user_args):
    my_logger.info(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    mosaic_params = GIABBenchParam()
    params_json = json.load(open(user_args.json, "r"))
    bdir, data_dir, ref = params_json["base_dir"], params_json["data_dir"], params_json["reference"]
    mosaic_params.set_parameters_from_json(params_json["mosaic"], bdir, data_dir, ref)
    # becnhmark
    mosaicsv_bench = GIABBench(mosaic_params, bench_id, FRAMEWORK_SRC_PATH)
    mosaicsv_bench.bench()


# ONT
def population_bench(user_args):
    my_logger.info(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    pop_merge_params = PopMergeTestParam()
    params_json = json.load(open(user_args.json, "r"))
    bdir, data_dir, ref = params_json["base_dir"], params_json["data_dir"], params_json["reference"]
    pop_merge_params.set_parameters_from_json(params_json)
    # becnhmark
    pop_bench = MergeXLBench(pop_merge_params, bench_id, FRAMEWORK_SRC_PATH)
    pop_bench.bench()


# ONT and HiFi
def full_bench(user_args):
    my_logger.info(f'Framework path: {FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    params_json = json.load(open(user_args.json, "r"))
    bdir, data_dir, ref = params_json["base_dir"], params_json["data_dir"], params_json["reference"]
    # NOTE: GIAB ONT hg38 5khz
    my_logger.info("GIAB ONT hg38 5khz")
    giab_params = GIABBenchParam()
    giab_params.set_parameters_from_json(params_json["hg002_ont_hg38_5khz"], bdir, data_dir, ref)
    giabsv_bench = GIABBench(giab_params, bench_id, FRAMEWORK_SRC_PATH)
    giabsv_bench.bench()
    time.sleep(2)
    # NOTE: GIAB ONT hg38
    my_logger.info("GIAB ONT hg38")
    giab_params = GIABBenchParam()
    giab_params.set_parameters_from_json(params_json["hg002_ont_hg38"], bdir, data_dir, ref)
    giabsv_bench = GIABBench(giab_params, bench_id, FRAMEWORK_SRC_PATH)
    giabsv_bench.bench()
    time.sleep(2)
    # NOTE: GIAB HiFI hg38
    my_logger.info("GIAB HiFI hg38")
    giab_hifi_params = GIABBenchParam()
    giab_hifi_params.set_parameters_from_json(params_json["hg002_hifi_hg38"], bdir, data_dir, ref)
    giabsv_hifi_bench = GIABBench(giab_hifi_params, bench_id, FRAMEWORK_SRC_PATH)
    giabsv_hifi_bench.bench()
    time.sleep(2)
    # NOTE: Mendelian
    my_logger.info("Mendelian")
    trio_params = TrioBenchParam()
    trio_params.set_parameters_from_json(params_json["mendelian_ont"], bdir, data_dir, ref)
    triosv_bench = TrioBench(trio_params, bench_id, FRAMEWORK_SRC_PATH)
    triosv_bench.bench()
    time.sleep(2)
    # NOTE: Mendelian HiFi
    my_logger.info("Mendelian HiFi")
    trio_hifi_params = TrioBenchParam()
    trio_hifi_params.set_parameters_from_json(params_json["mendelian_hifi"], bdir, data_dir, ref)
    triosv_hifi_bench = TrioBench(trio_hifi_params, bench_id, FRAMEWORK_SRC_PATH)
    triosv_hifi_bench.bench()
    time.sleep(2)
    # NOTE: Merge
    my_logger.info("Merge")
    merge_params = MergeTestParam()
    merge_params.set_parameters_from_json(params_json["merge"], bdir, data_dir, ref)
    merge_bench = MergeBench(merge_params, bench_id, FRAMEWORK_SRC_PATH)
    merge_bench.bench()
    time.sleep(2)
    # NOTE: Mosaic => use HapMap
    my_logger.info("Mosaic => use HapMap")
    mosaic_params = GIABBenchParam()
    mosaic_params.set_parameters_from_json(params_json["mosaic"], bdir, data_dir, ref)
    mosaicsv_bench = HapMapMosaic(mosaic_params, bench_id, FRAMEWORK_SRC_PATH)
    mosaicsv_bench.bench()
    # NOTE: BNDs => we sue HG008
    my_logger.info("BNDs => we sue HG008")
    bnds_params = GIABBenchParam()
    bnds_params.set_parameters_from_json(params_json["bnds"], bdir, data_dir, ref)
    bnds_bench = GIABBND(mosaic_params, bench_id, FRAMEWORK_SRC_PATH)
    bnds_bench.bench()
    # NOTE: ONT specific
    # TODO: update
    my_logger.warning("large events missing")
    # ont_large_deldup_params = ONTLargeDelDupParams()
    # ont_large_deldup_params.set_parameters_from_json(params_json["large_deldup_ont_colo"], bdir, data_dir, ref)
    # ont_large_deldup_bench = ONTLargeDelDup(ont_large_deldup_params, bench_id, FRAMEWORK_SRC_PATH)
    # ont_large_deldup_bench.bench()
    # NOTE: Genotyper # TODO: update BAM
    # genotyper_params = GenotyperParam()
    # genotyper_params.set_parameters_from_json(params_json["genotyper"], params_json["base_dir"], params_json["data_dir"])
    # genotyper_bench = GenotyperBench(genotyper_params, bench_id, FRAMEWORK_SRC_PATH)
    # genotyper_bench.bench()
    # time.sleep(2)


def main():
    # Get arguments
    user_args, main_help = config.get_arguments()
    command = user_args.command

    if command == "bench":
        full_bench(user_args)
    elif command == "giab":
        giab_bench(user_args)
    elif command == "mendelian":
        trio_bench(user_args)
    elif command == "merge":
        combine_bench(user_args)
    elif command == "mosaic":
        mosaic_bench(user_args)
    elif command == "population":
        population_bench(user_args)
    else:
        my_logger.info(main_help)
        sys.exit(1)


if __name__ == "__main__": 
    main()
