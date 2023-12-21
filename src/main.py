#!/usr/bin/env python3
import sys 
import json 
import config
from benchmarks.merge_bench import PopMergeTestParam
from benchmarks.merge_bench import MergeXLBench
from benchmarks.giab_bench import GIABBenchParam
from benchmarks.giab_bench import GIABBench
from benchmarks.mendelian import TrioBenchParam
from benchmarks.mendelian import TrioBench
from scripts import generate_id


FRAMEWORK_SRC_PATH = "/".join(__file__.split("/")[:-1])


def giab_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    giab_params = GIABBenchParam()
    params_json = json.load(open(user_args.json, "r"))
    giab_params.set_parameters_from_json(params_json)
    # becnhmark
    giab_bench = GIABBench(giab_params, bench_id, FRAMEWORK_SRC_PATH)
    giab_bench.bench()

def cmrg_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    cmrg_params = GIABBenchParam()
    params_json = json.load(open(user_args.json, "r"))
    cmrg_params.set_parameters_from_json(params_json)
    # becnhmark
    cmrg_bench = GIABBench(cmrg_params, bench_id, FRAMEWORK_SRC_PATH)
    cmrg_bench.bench()

def trio_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    trio_params = TrioBenchParam()
    params_json = json.load(open(user_args.json, "r"))
    trio_params.set_parameters_from_json(params_json)
    # becnhmark
    trio_bench = TrioBench(trio_params, bench_id, FRAMEWORK_SRC_PATH)
    trio_bench.bench()

def merge_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    # TODO:

def population_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    merge_params = PopMergeTestParam()
    params_json = json.load(open(user_args.json, "r"))
    merge_params.set_parameters_from_json(params_json)
    # becnhmark
    merge_bench = MergeXLBench(merge_params, bench_id, FRAMEWORK_SRC_PATH)
    merge_bench.bench()


def full_bench(user_args):
    print(f'{FRAMEWORK_SRC_PATH}')
    bench_id = generate_id.make_id()
    params_json = json.load(open(user_args.json, "r"))
    # NOTE: GIAB
    giab_params = GIABBenchParam()
    giab_params.set_parameters_from_json(params_json["giab"])
    giab_bench = GIABBench(giab_params, bench_id, FRAMEWORK_SRC_PATH)
    giab_bench.bench()
    # NOTE: CMRG
    cmrg_params = GIABBenchParam()
    cmrg_params.set_parameters_from_json(params_json["cmrg"])
    cmrg_bench = GIABBench(cmrg_params, bench_id, FRAMEWORK_SRC_PATH)
    cmrg_bench.bench()
    # NOTE: Mendelian
    trio_params = TrioBenchParam()
    trio_params.set_parameters_from_json(params_json["mendelian"])
    trio_bench = TrioBench(trio_params, bench_id, FRAMEWORK_SRC_PATH)
    trio_bench.bench()


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
        merge_bench(user_args)
    elif command == "population":
        population_bench(user_args)
    elif command == "bench":
        full_bench(user_args)
    else:
        print(main_help)
        sys.exit(1)

""" Sam giab and medelian for later
    # Read contents of input JSON file with all the paths 
    with open(sys.argv[1], 'r') as file:
        json_data = json.load(file)

    # Set the working directory 
    os.chdir(json_data["directory"])

    # Check if the truvari benchmark needs to be tested 
    if len(json_data["truvari_versions"]) > 0: 

        snfjob_ids = []

        # Test the version of truvari on all the given test data sets
        # First run all sniffles jobs first so those jobs can run concurrenlty 
        for data_set in range(0, len(json_data["truvari_data"])): 
            alignment = json_data["truvari_data"][data_set][0]

            # Run sniffles jobs 
            snf_job = sniffles(alignment, json_data["current_snf"], json_data["new_snf"], data_set)
            snfjob_ids.append(snf_job.run())

        # Make sure to test all the different truvari versions
        for truv_type in range(0, len(json_data["truvari_versions"])): 

            # Now run all truvari jobs and collect results to compare the snf versions' performances 
            for id in range(0, len(snfjob_ids)): 
                bench_vcf = json_data["truvari_data"][id][1]
                bench_bed = json_data["truvari_data"][id][2]

                truvari_job = truvari(truv_type, json_data["truvari_versions"][truv_type], bench_vcf, bench_bed, snfjob_ids[id], id)
                truvari_job.run() 

    # Check if the mendelian benchmark needs to be tested 
    if len(json_data["mendelian_data"]) > 0: 
        mendelian_snf_ids = []

        # Make sure to test mendelian on all the given test data sets 
        for data_set in range(0, len(json_data["mendelian_data"])):
            alignment1 = json_data["mendelian_data"][data_set][0]
            alignment2 = json_data["mendelian_data"][data_set][1]
            alignment3 = json_data["mendelian_data"][data_set][2]

            # Run both verisons of sniffles on the given data set
            mendelian_sniffles = sniffles_trio(json_data["current_snf"], json_data["new_snf"], data_set, alignment1, alignment2, alignment3)
            job_ids = mendelian_sniffles.run()
            mendelian_snf_ids.append(job_ids)
            
        # Run mendelian jobs with correct respective snf job dependencies 
        for id_trio in range(0, len(mendelian_snf_ids)): 
            mendelian_job = mendelian(json_data["bcftools_plugin"], json_data["current_snf"], \
                          json_data["new_snf"], id_trio, mendelian_snf_ids[id_trio])
            mendelian_job.run()

    # Check if sniffles needs to be tested with extra parameters 
    if len(json_data["extra_param"]) != "": 

        # Run sniffles jobs with extra parameters on the alignment data provided 
        for data_set in range(0, len(json_data["truvari_data"])): 
            alignment = json_data["truvari_data"][data_set][0]

            snf_extra_job = sniffles_extra(alignment, json_data["current_snf"], json_data["new_snf"], data_set, json_data["extra_param"])
            snf_extra_job.run()

    return 0
    """

if __name__ == "__main__": 
    main()