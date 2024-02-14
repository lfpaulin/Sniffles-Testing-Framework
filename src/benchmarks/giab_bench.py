import json
from utils import jobs_slurm
from utils.logger import setup_log


class GIABBenchParam(object):
    def __init__(self):
        self.bam = None
        self.dir_out = None
        self.output = None
        self.reference = None
        self.tandem_rep = None
        self.snf2_old = None
        self.snf2_new = None
        self.snf2_param = None
        self.snf2_param_string = None
        self.truvari = None
        self.truvari_version = None
        self.skip_old = None
        self.skip_new = None

    def set_parameters_from_json(self, json_dict):
        self.bam = json_dict["bam_file"]
        self.dir_out = json_dict["directory"]
        self.output = json_dict["output"]
        self.reference = json_dict["reference"]
        self.tandem_rep = json_dict["tandem_repeat"]
        self.snf2_old = json_dict["snf_current"]
        self.snf2_new = json_dict["snf_new"]
        self.snf2_param = json_dict["extra_param"]
        self.extra_param_string()
        self.truvari = self.set_truvari(json_dict["truvari"])
        self.truvari_version = self.truvari["version"]
        self.skip_old = json_dict["skip_old"]
        self.skip_old = json_dict["skip_new"]

    def extra_param_string(self):
        if len(self.snf2_param) > 0:
            self.snf2_param_string = " ".join("  ".join(self.snf2_param.split(",")).split(":"))
        else:
            self.snf2_param_string = self.snf2_param

    @staticmethod
    def set_truvari(json_file):
        return json.load(open(json_file, "r"))


class GIABBench(object):
    def __init__(self, bench_args, bench_id, src_path):
        self.args = bench_args
        self.id = bench_id
        self.src_path = src_path
        self.logger = setup_log(__name__, True)
    
    def sniffles_current(self):
        self.logger.info("Sniffles2 current version")
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_old_call.out')
        job.set_error(f'log_{self.id}_snf2_old_call.err')
        job.set_chdir(f'{self.args.dir_out}')
        cmd = f'{self.src_path}/scripts/sniffles.sh  {self.args.snf2_old}  {self.args.bam}  {self.args.output}_old ' \
              f'  {self.args.reference}  {self.args.tandem_rep}  "{self.args.snf2_param_string}" '
        job.make(cmd)
        job.submit()
        return job

    def sniffles_new(self):
        self.logger.info("Sniffles2 new version")
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_new_call.out')
        job.set_error(f'log_{self.id}_snf2_new_call.err')
        job.set_chdir(f'{self.args.dir_out}')
        cmd = f'{self.src_path}/scripts/sniffles.sh  {self.args.snf2_new}  {self.args.bam}  {self.args.output}_new ' \
              f'  {self.args.reference}  {self.args.tandem_rep}  "{self.args.snf2_param_string}" '
        job.make(cmd)
        job.submit()
        return job

    def compare(self, old=None, new=None, bench_name=""):
        self.logger.info(f'Sniffles2 bench compare: {bench_name}')
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_call_bench.out')
        job.set_error(f'log_{self.id}_snf2_call_bench.err')
        job.set_chdir(f'{self.args.dir_out}')
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
        # truvari command
        cmd = f'{self.src_path}/scripts/truvari.sh  {self.args.output}_old.vcf.gz  {self.args.output}_old_bench  ' \
              f'{self.args.output}_new.vcf.gz  {self.args.output}_new_bench  {self.args.truvari["vcf"]}  ' \
              f'{self.args.truvari["bed"]}  {self.args.reference}  {self.args.truvari["bench"]}'
        job.make(cmd)
        job.submit()

    def bench(self):
        sniffles_current = self.sniffles_current() if not self.args.skip_old else None
        sniffles_new = self.sniffles_new() if not self.args.skip_new else None
        self.compare(sniffles_current, sniffles_new)
