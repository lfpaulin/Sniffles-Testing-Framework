from scripts import jobs_slurm

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
        self.snf2_param = None
        self.snf2_param_string = None
        self.skip_old = None

    def set_parameters_from_json(self, json_dict):
        self.snf_list = json_dict["snf_list"]
        self.dir_out = json_dict["directory"]
        self.output = json_dict["output"]
        self.reference = json_dict["reference"]
        self.threads = json_dict["threads"]
        self.memory = json_dict["memory"]
        self.snf2_old = json_dict["snf_current"]
        self.snf2_new = json_dict["snf_new"]
        self.snf2_param = json_dict["extra_param"]
        self.extra_param_string()
        self.skip_old = bool(json_dict["skip_old"])

    def extra_param_string(self):
        if len(self.extra_param) > 0:
            self.snf2_param_string = " ".join("  ".join(self.extra_param.split(",")).split(":"))
        else:
            self.snf2_param_string = self.extra_param 


class MergeXLBench(object):
    def __init__(self, bench_args, bench_id, src_path):
        self.args = bench_args
        self.id = bench_id
        self.src_path = src_path
    
    def sniffles_current(self):
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_old_mergeXL.out')
        job.set_error(f'log_{self.id}_snf2_old_mergeXL.err')
        job.set_chdir(f'{self.args.dir_out}')
        job.set_params(f'--tasks-per-node={self.args.threads}  --mem={self.args.memory}')
        cmd = f'{self.src_path}/scripts/sniffles_merge_large.sh  {self.args.snf2_old}  {self.args.snf_list}  {self.args.output}_old ' \
              f'  {self.args.reference}  {self.args.threads}  {self.args.snf2_param_string}'
        job.make(cmd)
        job.submit()

    def sniffles_new(self):
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_new_mergeXL.out')
        job.set_error(f'log_{self.id}_snf2_new_mergeXL.err')
        job.set_chdir(f'{self.args.dir_out}')
        job.set_params(f'--tasks-per-node={self.args.threads}  --mem={self.args.memory}')
        cmd = f'{self.src_path}/scripts/sniffles_merge_large.sh  {self.args.snf2_new}  {self.args.snf_list}  {self.args.output}_new ' \
              f'  {self.args.reference}  {self.args.threads}  {self.args.snf2_param_string}'
        job.make(cmd)
        job.submit()

    def compare(self):
        pass  # TODO:

    def bench(self):
        self.sniffles_current() if not self.args.skip_old else None
        self.sniffles_new()
        self.compare()
