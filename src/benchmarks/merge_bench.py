import os
from utils import jobs_slurm
from utils.logger import setup_log

class PopMergeTestParam(object):
    def __init__(self):
        self.snf_list = None
        self.dir_out = None
        self.output = None
        self.reference = None
        self.threads = None
        self.memory = None
        self.snf2_old = None
        self.snf2_new = None
        self.snf2_old_ver = None
        self.snf2_new_ver = None
        self.snf2_param = None
        self.snf2_param_string = None
        self.skip_old = None
        self.skip_new = None

    def set_parameters_from_json(self, json_dict, base_dir, data_dir):
        self.snf_list = json_dict["snf_list"]
        self.dir_out = json_dict["directory"]
        self.output = json_dict["output"]
        self.reference = json_dict["reference"]
        self.threads = json_dict["threads"]
        self.memory = json_dict["memory"]
        self.snf2_old = json_dict["snf_current"]
        self.snf2_new = json_dict["snf_new"]
        self.snf2_old_ver = json_dict["snf_current_ver"]
        self.snf2_new_ver = json_dict["snf_new_ver"]
        self.snf2_param = json_dict["extra_param"]
        self.extra_param_string()
        self.skip_old = bool(json_dict["skip_old"])
        self.skip_new = bool(json_dict["skip_new"])

    def extra_param_string(self):
        if len(self.snf2_param) > 0:
            self.snf2_param_string = " ".join("  ".join(self.snf2_param.split(",")).split(":"))
        else:
            self.snf2_param_string = self.snf2_param 


class MergeXLBench(object):
    def __init__(self, bench_args, bench_id, src_path):
        self.args = bench_args
        self.id = bench_id
        self.src_path = src_path
        self.logger = setup_log(__name__, True)

    def sniffles_current(self):
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_old_mergeXL.out')
        job.set_error(f'log_{self.id}_snf2_old_mergeXL.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_params(f'--ntasks={self.args.threads}  --mem={self.args.memory}')
        cmd = f'{self.src_path}/scripts/sniffles_merge_large.sh  {self.args.snf2_old}  {self.args.snf_list}  {self.args.output}_old ' \
              f'  {self.args.reference}  {self.args.threads}  {self.args.snf2_param_string}'
        job.make(cmd)
        job.submit()
        return job

    def sniffles_new(self):
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_new_mergeXL.out')
        job.set_error(f'log_{self.id}_snf2_new_mergeXL.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_params(f'--ntasks={self.args.threads}  --mem={self.args.memory}')
        cmd = f'{self.src_path}/scripts/sniffles_merge_large.sh  {self.args.snf2_new}  {self.args.snf_list}  {self.args.output}_new ' \
              f'  {self.args.reference}  {self.args.threads}  {self.args.snf2_param_string}'
        job.make(cmd)
        job.submit()
        return job

    def compare(self, old, new):
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_merge_bench.out')
        job.set_error(f'log_{self.id}_snf2_merge_bench.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        if self.args.skip_old and self.args.skip_new:
            self.logger.error(f'Both analysis have the "skip" option on... none has run.')
        elif self.args.skip_old:
            self.logger.info(f'Only running new version of Sniffles2.')
            job.set_dependencies(f'afterok:{new.job_id}')
        elif self.args.skip_old:
            self.logger.info(f'Only running current version of Sniffles2.')
            job.set_dependencies(f'afterok:{old.job_id}')
        else:
            self.logger.info(f'Running both versions of Sniffles2.')
            job.set_dependencies(f'afterok:{old.job_id},{new.job_id}')
        pass  # TODO:
        # cmd = f''
        # job.make(cmd)
        # job.submit()

    def bench(self):
        sniffles_current = None
        sniffles_new = None
        if not self.args.skip_old:
            sniffles_current = self.sniffles_current() 
        if not self.args.skip_new:
            sniffles_new = self.sniffles_new()
        # self.compare(sniffles_current, sniffles_new)


class MergeTestParam(object):
    def __init__(self):
        self.base_dir = None
        self.data_dir = None
        self.sample1 = None
        self.sample2 = None
        self.dir_out = None
        self.output = None
        self.reference = None
        self.tandem_rep = None
        self.snf2_old = None
        self.snf2_new = None
        self.snf2_old_ver = None
        self.snf2_new_ver = None
        self.snf2_param = None
        self.snf2_param_string = None
        self.skip_old = None
        self.skip_new = None

    def set_parameters_from_json(self, json_dict, base_dir, data_dir, reference):
        self.base_dir = base_dir
        self.data_dir = data_dir
        self.reference = reference
        self.sample1 = f'{data_dir}/{json_dict["sample1"]}'
        self.sample2 = f'{data_dir}/{json_dict["sample2"]}'
        self.dir_out = f'{base_dir}/{json_dict["directory"]}'
        self.output = json_dict["output"]
        self.tandem_rep = json_dict["tandem_repeat"]
        self.snf2_old = json_dict["snf_current"]
        self.snf2_new = json_dict["snf_new"]
        self.snf2_old_ver = json_dict["snf_current_ver"]
        self.snf2_new_ver = json_dict["snf_new_ver"]
        self.snf2_param = json_dict["extra_param"]
        self.extra_param_string()
        self.skip_old = bool(json_dict["skip_old"])
        self.skip_new = bool(json_dict["skip_new"])

    def extra_param_string(self):
        if len(self.snf2_param) > 0:
            self.snf2_param_string = " ".join("  ".join(self.snf2_param.split(",")).split(":"))
        else:
            self.snf2_param_string = self.snf2_param 


class MergeBench(object):
    def __init__(self, bench_args, bench_id, src_path):
        self.args = bench_args
        self.id = bench_id
        self.src_path = src_path
        self.logger = setup_log(__name__, True)

    def sniffles_current(self):
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_merge_{self.args.snf2_old_ver}.out')
        job.set_error(f'log_{self.id}_snf2_merge_{self.args.snf2_old_ver}.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_jname(f'mrg{self.args.snf2_old_ver}')
        cmd = " ".join([
            f'{self.src_path}/scripts/sniffles_merge.sh',
            self.args.snf2_old,
            self.args.sample1,
            self.args.sample2,
            f'{self.args.output}_{self.args.snf2_old_ver}',
            self.args.reference,
            self.args.tandem_rep,
            f'"{self.args.snf2_param_string}"'
        ])
        job.make(cmd)
        job.submit()
        return job

    def sniffles_new(self):
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_merge_{self.args.snf2_new_ver}.out')
        job.set_error(f'log_{self.id}_snf2_merge_{self.args.snf2_new_ver}.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_jname(f'mrg{self.args.snf2_new_ver}')
        cmd = " ".join([
            f'{self.src_path}/scripts/sniffles_merge.sh',
            self.args.snf2_new,
            self.args.sample1,
            self.args.sample2,
            f'{self.args.output}_{self.args.snf2_new_ver}',
            self.args.reference,
            self.args.tandem_rep,
            f'"{self.args.snf2_param_string}"'
        ])
        job.make(cmd)
        job.submit()
        return job

    def compare(self, old, new):
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_merge_bench.out')
        job.set_error(f'log_{self.id}_snf2_merge_bench.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        if self.args.skip_old and self.args.skip_new:
            self.logger.error(f'Both analysis have the "skip" option on... none has run.')
        elif self.args.skip_old:
            self.logger.info(f'Only running new version of Sniffles2.')
            job.set_dependencies(f'afterok:{new.job_id}')
        elif self.args.skip_old:
            self.logger.info(f'Only running current version of Sniffles2.')
            job.set_dependencies(f'afterok:{old.job_id}')
        else:
            self.logger.info(f'Running both versions of Sniffles2.')
            job.set_dependencies(f'afterok:{old.job_id},{new.job_id}')
        pass  # TODO:
        # cmd = f''
        # job.make(cmd)
        # job.submit()

    def bench(self):
        sniffles_current = None
        sniffles_new = None
        if not self.args.skip_old:
            sniffles_current = self.sniffles_current()
        if not self.args.skip_new:
            sniffles_new = self.sniffles_new()
        # self.compare(sniffles_current, sniffles_new)
