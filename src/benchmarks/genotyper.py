import os
from utils import jobs_slurm
from utils.logger import setup_log


class GenotyperParam(object):
    def __init__(self):
        self.base_dir = None
        self.data_dir = None
        self.bam = None
        self.dir_out = None
        self.output = None
        self.reference = None
        self.vcf_input = None
        self.snf2_old = None
        self.snf2_new = None
        self.snf2_old_ver = None
        self.snf2_new_ver = None
        self.snf2_param = ""
        self.snf2_param_string = None
        self.skip_old = None
        self.skip_new = None

    def set_parameters_from_json(self, json_dict):
        self.base_dir = json_dict["base_dir"]
        self.data_dir = json_dict["data_dir"]
        self.bam = f'{json_dict["data_dir"]}/{json_dict["bam_file"]}'
        self.dir_out = f'{json_dict["base_dir"]}/{json_dict["directory"]}'
        self.output = json_dict["output"]
        self.reference = json_dict["reference"]
        self.vcf_input = f'{json_dict["data_dir"]}/{json_dict["vcf_input"]}'
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


class GenotyperBench(object):
    def __init__(self, bench_args, bench_id, src_path):
        self.args = bench_args
        self.id = bench_id
        self.src_path = src_path
        self.logger = setup_log(__name__, True)
    
    def sniffles_current(self):
        self.logger.info("Sniffles2 current version")
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_gter_{self.args.snf2_old_ver}.out')
        job.set_error(f'log_{self.id}_snf2_gter_{self.args.snf2_old_ver}.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_jname(f'gter{self.args.snf2_old_ver}')
        cmd = " ".join([
            f'{self.src_path}/scripts/sniffles_gt.sh',
            self.args.snf2_old,
            self.args.bam,
            self.args.vcf_input,
            f'{self.args.output}_{self.args.snf2_old_ver}',
            self.args.reference
        ])
        job.make(cmd)
        job.submit()
        return job

    def sniffles_new(self):
        self.logger.info("Sniffles2 new version")
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_gter_{self.args.snf2_new_ver}.out')
        job.set_error(f'log_{self.id}_snf2_gter_{self.args.snf2_new_ver}.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_jname(f'gter{self.args.snf2_new_ver}')
        cmd = " ".join([
            f'{self.src_path}/scripts/sniffles_gt.sh',
            self.args.snf2_new,
            self.args.bam,
            self.args.vcf_input,
            f'{self.args.output}_{self.args.snf2_new_ver}',
            self.args.reference
        ])
        job.make(cmd)
        job.submit()
        return job

    def compare(self, old, new, bench_name=""):
        pass


    def bench(self):
        sniffles_current = None
        sniffles_new = None
        if not self.args.skip_old:
            sniffles_current = self.sniffles_current()
        if not self.args.skip_new:
            sniffles_new = self.sniffles_new()
        #self.compare(sniffles_current, sniffles_new)
