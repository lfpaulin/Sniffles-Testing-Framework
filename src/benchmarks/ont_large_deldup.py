import os
import json
from utils import jobs_slurm
from utils.logger import setup_log


class ONTLargeDelDupParams(object):
    def __init__(self):
        self.base_dir = None
        self.data_dir = None
        self.bam_files = None
        self.dir_out = None
        self.output = None
        self.reference = None
        self.tandem_rep = ""
        self.snf2_old = None
        self.snf2_new = None
        self.snf2_old_ver = None
        self.snf2_new_ver = None
        self.snf2_param = ""
        self.snf2_param_string = None
        self.skip_old = None
        self.skip_new = None

    def set_parameters_from_json(self, json_dict, base_dir, data_dir, snf2_pub, snf2_dev):
        self.base_dir = base_dir
        self.data_dir = data_dir
        self.reference = f'{data_dir}/{json_dict["reference"]}'
        self.bam_files = [ f'{data_dir}/{b}' for b in json_dict["bam_file"] ]
        self.dir_out = f'{base_dir}/{json_dict["directory"]}'
        self.output = json_dict["output"]
        self.snf2_old = snf2_pub
        self.snf2_new = snf2_dev
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


class ONTLargeDelDup(object):
    def __init__(self, bench_args, bench_id, src_path):
        self.args = bench_args
        self.id = bench_id
        self.src_path = src_path
        self.logger = setup_log(__name__, True)
    
    def sniffles_run(self, version: str, bam_path: str):
        use_ver, use_bin = "", ""
        if "old" == version:
            use_ver = self.args.snf2_old_ver
            use_bin = self.args.snf2_old
        elif "new" == version:
            use_ver = self.args.snf2_new_ver
            use_bin = self.args.snf2_new
        else:
            self.logger.error(f"Not a known version: {version}, exiting with error")
            assert version not in {"old", "new"}, version
        self.logger.info(f"Sniffles2 {version} version")
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_deldup_{use_ver}.out')
        job.set_error(f'log_{self.id}_snf2_deldup_{use_ver}.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_jname(f'ont_{use_ver}')
        cmd = " ".join([
            f'{self.src_path}/scripts/sniffles.sh',  use_bin,
            f'{bam_path}/altered_coverages.cram',
            f'{self.args.output}_{use_ver}',
            self.args.reference, 
            self.args.tandem_rep,
            f'"{self.args.snf2_param_string}"'
        ])
        job.make(cmd)
        job.submit()
        return job

    def compare(self, old, new, bench_name, bench_log, vcf, bed, bench, statify = "0"):
        self.logger.info(f'Sniffles2 bench compare: {bench_name}')
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_{bench_log}.out')
        job.set_error(f'log_{self.id}_snf2_{bench_log}.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_jname(f'trv{bench_name}')
        if self.args.skip_old and self.args.skip_new:
            self.logger.error(f'Both analysis have the "skip" option on... none has run.')
        elif self.args.skip_old:
            self.logger.info(f'Only using new version of Sniffles2.')
            job.set_dependencies(f'afterok:{new.job_id}')
        elif self.args.skip_new:
            self.logger.info(f'Only using current version of Sniffles2.')
            job.set_dependencies(f'afterok:{old.job_id}')
        else:
            self.logger.info(f'Using both versions of Sniffles2.')
            job.set_dependencies(f'afterok:{old.job_id},{new.job_id}')
        # truvari command
        self.logger.info(f'Running GIAB SV-bench {bench_name}.')
        cmd = " ".join([
            f'{self.src_path}/scripts/truvari.sh', 
            f'{self.args.output}_{self.args.snf2_old_ver}.vcf.gz',
            f'{self.args.output}_{self.args.snf2_old_ver}_bench',
            f'{self.args.output}_{self.args.snf2_new_ver}.vcf.gz',
            f'{self.args.output}_{self.args.snf2_new_ver}_bench',
            vcf, bed, self.args.reference, bench, statify
        ])
        job.make(cmd)
        job.submit()

    def bench(self):
        sniffles_current = None
        sniffles_new = None
        for bam in self.args.bam_files:
            if not self.args.skip_old:
                sniffles_current = self.sniffles_run("old", bam)
            if not self.args.skip_new:
                sniffles_new = self.sniffles_run("new", bam)
            if sniffles_new is not None or sniffles_new is not None:
                pass
                # ALL_CNVs.bed
                # self.compare(sniffles_current, sniffles_new, "GIAB Q100", "bench_giab",
                    # self.args.truvari["vcf"], self.args.truvari["bed"], self.args.truvari["bench"], "1")
