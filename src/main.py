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
    snf2_pub, snf2_dev = params_json["snf2_pub"], params_json["snf2_dev"]
    giab_params.set_parameters_from_json(params_json["hg002_ont_hg38_5khz"], bdir, data_dir, ref, snf2_pub, snf2_dev)
    # benchmark
    giabsv_bench = GIABBench(giab_params, bench_id, FRAMEWORK_SRC_PATH)
    giabsv_bench.bench()


# ONT or HiFi
def trio_bench(user_args):
    my_logger.info(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    trio_params = TrioBenchParam()
    params_json = json.load(open(user_args.json, "r"))
    bdir, data_dir, ref = params_json["base_dir"], params_json["data_dir"], params_json["reference"]
    snf2_pub, snf2_dev = params_json["snf2_pub"], params_json["snf2_dev"]
    trio_params.set_parameters_from_json(params_json["mendelian_ont"], bdir, data_dir, ref, snf2_pub, snf2_dev)
    # benchmark
    triosv_bench = TrioBench(trio_params, bench_id, FRAMEWORK_SRC_PATH)
    triosv_bench.bench()


# ONT (truvari)
def combine_bench(user_args):
    my_logger.info(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    merge_params = MergeTestParam()
    params_json = json.load(open(user_args.json, "r"))
    bdir, data_dir, ref = params_json["base_dir"], params_json["data_dir"], params_json["reference"]
    snf2_pub, snf2_dev = params_json["snf2_pub"], params_json["snf2_dev"]
    merge_params.set_parameters_from_json(params_json["merge"], bdir, data_dir, ref, snf2_pub, snf2_dev)
    # benchmark
    merge_bench = MergeBench(merge_params, bench_id, FRAMEWORK_SRC_PATH)
    merge_bench.bench()


# ONT
def mosaic_bench(user_args):
    my_logger.info(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    mosaic_params = GIABBenchParam()
    params_json = json.load(open(user_args.json, "r"))
    bdir, data_dir, ref = params_json["base_dir"], params_json["data_dir"], params_json["reference"]
    snf2_pub, snf2_dev = params_json["snf2_pub"], params_json["snf2_dev"]
    mosaic_params.set_parameters_from_json(params_json["mosaic"], bdir, data_dir, ref, snf2_pub, snf2_dev)
    # benchmark
    mosaicsv_bench = GIABBench(mosaic_params, bench_id, FRAMEWORK_SRC_PATH)
    mosaicsv_bench.bench()


# ONT
def population_bench(user_args):
    my_logger.info(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    pop_merge_params = PopMergeTestParam()
    params_json = json.load(open(user_args.json, "r"))
    bdir, data_dir, ref = params_json["base_dir"], params_json["data_dir"], params_json["reference"]
    snf2_pub, snf2_dev = params_json["snf2_pub"], params_json["snf2_dev"]
    pop_merge_params.set_parameters_from_json(params_json, "", "")
    # benchmark
    pop_bench = MergeXLBench(pop_merge_params, bench_id, FRAMEWORK_SRC_PATH)
    pop_bench.bench()


# ONT and HiFi
def full_bench(user_args):
    my_logger.info(f'Framework path: {FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    params_json = json.load(open(user_args.json, "r"))
    base_dir, data_dir, ref = params_json["base_dir"], params_json["data_dir"], params_json["reference"]
    snf2_pub, snf2_dev = params_json["snf2_pub"], params_json["snf2_dev"]
    # NOTE: GIAB ONT hg38
    my_logger.info("GIAB ONT hg38")
    giab_params = GIABBenchParam()
    giab_params.set_parameters_from_json(params_json["hg002_ont_hg38"], base_dir, data_dir, ref, snf2_pub, snf2_dev)
    giabsv_bench = GIABBench(giab_params, bench_id, FRAMEWORK_SRC_PATH)
    giabsv_bench.bench()
    time.sleep(2)
    # NOTE: GIAB ONT hg38 low
    my_logger.info("GIAB ONT hg38 low coverage")
    giab_params = GIABBenchParam()
    giab_params.set_parameters_from_json(params_json["hg002_ont_hg38_low"], base_dir, data_dir, ref, snf2_pub, snf2_dev)
    giabsv_bench = GIABBench(giab_params, bench_id, FRAMEWORK_SRC_PATH)
    giabsv_bench.bench()
    time.sleep(2)
    # NOTE: GIAB HiFi hg38
    my_logger.info("GIAB HiFI hg38")
    giab_hifi_params = GIABBenchParam()
    giab_hifi_params.set_parameters_from_json(params_json["hg002_hifi_hg38"], base_dir, data_dir, ref, snf2_pub, snf2_dev)
    giabsv_hifi_bench = GIABBench(giab_hifi_params, bench_id, FRAMEWORK_SRC_PATH)
    giabsv_hifi_bench.bench()
    time.sleep(2)
    # NOTE: GIAB HiFi hg38 low
    my_logger.info("GIAB HiFI hg38 low coverage")
    giab_hifi_params = GIABBenchParam()
    giab_hifi_params.set_parameters_from_json(params_json["hg002_hifi_hg38_low"], base_dir, data_dir, ref, snf2_pub, snf2_dev)
    giabsv_hifi_bench = GIABBench(giab_hifi_params, bench_id, FRAMEWORK_SRC_PATH)
    giabsv_hifi_bench.bench()
    time.sleep(2)
    # NOTE: Mendelian
    my_logger.info("Mendelian")
    trio_params = TrioBenchParam()
    trio_params.set_parameters_from_json(params_json["mendelian_ont"], base_dir, data_dir, ref, snf2_pub, snf2_dev)
    triosv_bench = TrioBench(trio_params, bench_id, FRAMEWORK_SRC_PATH)
    triosv_bench.bench()
    time.sleep(2)
    # NOTE: Mendelian HiFi
    my_logger.info("Mendelian HiFi")
    trio_hifi_params = TrioBenchParam()
    trio_hifi_params.set_parameters_from_json(params_json["mendelian_hifi"], base_dir, data_dir, ref, snf2_pub, snf2_dev)
    triosv_hifi_bench = TrioBench(trio_hifi_params, bench_id, FRAMEWORK_SRC_PATH)
    triosv_hifi_bench.bench()
    time.sleep(2)
    # NOTE: Merge
    my_logger.info("Merge")
    merge_params = MergeTestParam()
    merge_params.set_parameters_from_json(params_json["merge"], base_dir, data_dir, ref, snf2_pub, snf2_dev)
    merge_bench = MergeBench(merge_params, bench_id, FRAMEWORK_SRC_PATH)
    merge_bench.bench()
    time.sleep(2)
    # NOTE: Mosaic => use HapMap
    my_logger.info("Mosaic => use HapMap")
    mosaic_params = GIABBenchParam()
    mosaic_params.set_parameters_from_json(params_json["mosaic"], base_dir, data_dir, ref, snf2_pub, snf2_dev)
    mosaicsv_bench = HapMapMosaic(mosaic_params, bench_id, FRAMEWORK_SRC_PATH)
    mosaicsv_bench.bench()
    # NOTE: Mosaic => use HG002, chjeck how many are reported
    my_logger.info("Mosaic => use HG002")
    mosaic_params = GIABBenchParam()
    mosaic_params.set_parameters_from_json(params_json["mosaic_hg002"], base_dir, data_dir, ref, snf2_pub, snf2_dev)
    mosaicsv_bench = HapMapMosaic(mosaic_params, bench_id, FRAMEWORK_SRC_PATH)
    mosaicsv_bench.bench()
    # NOTE: BNDs => we use HG008
    # my_logger.info("BNDs => we sue HG008")
    # bnds_params = GIABBenchParam()
    # bnds_params.set_parameters_from_json(params_json["bnds"], base_dir, data_dir, ref, snf2_pub, snf2_dev)
    # bnds_bench = GIABBND(mosaic_params, bench_id, FRAMEWORK_SRC_PATH)
    # bnds_bench.bench()
    # NOTE: Severus
    my_logger.info("Severus in HG002 (ONT + PB)")
    my_logger.info("Severus => use HG002")
    severus_params = SeverusParam()
    severus_params.set_parameters_from_json(params_json["severus"], base_dir, data_dir, ref)
    severus_bench = SeverusBench(severus_params, bench_id, FRAMEWORK_SRC_PATH)
    severus_bench.bench()
    # TODO: implement HapMap
    # my_logger.info("Severus in HG002 (ONT + PB) and HapMap")
    # # TODO: update
    # my_logger.warning("large events missing")
    # ont_large_deldup_params = ONTLargeDelDupParams()
    # ont_large_deldup_params.set_parameters_from_json(params_json["large_deldup_ont_colo"], base_dir, data_dir, ref, snf2_pub, snf2_dev)
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
