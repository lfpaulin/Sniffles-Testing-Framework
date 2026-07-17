#!/usr/bin/env python3
import json
from utils import generate_id
from utils.logger import setup_log

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
