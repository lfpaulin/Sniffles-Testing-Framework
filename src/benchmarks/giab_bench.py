#!/usr/bin/env python
import os
import sys
import json
from utils import jobs_slurm
from utils.logger import setup_log


class GIABBenchParam(object):
    def __init__(self):
        self.base_dir = ""
        self.data_dir = ""
        self.bam = ""
        self.dir_out = ""
        self.output = ""
        self.reference = ""
        self.tandem_rep = ""
        self.snf2_old = ""
        self.snf2_new = ""
        self.snf2_old_ver = ""
        self.snf2_new_ver = ""
        self.snf2_param = ""
        self.snf2_param_string = ""
        self.truvari = ""
        self.truvari_version = ""
        self.skip_old = ""
        self.skip_new = ""
        self.truvari2 = ""

    def set_parameters_from_json(self, json_dict, base_dir, data_dir, reference, snf2_pub, snf2_dev):
        self.base_dir = base_dir
        self.data_dir = data_dir
        self.reference = reference
        self.snf2_old = snf2_pub
        self.snf2_new = snf2_dev
        self.bam = f'{self.data_dir}/{json_dict["bam_file"]}'
        self.dir_out = f'{self.base_dir}/{json_dict["directory"]}'
        self.output = json_dict["output"]
        self.tandem_rep = json_dict["tandem_repeat"]
        self.snf2_old_ver = json_dict["snf_current_ver"]
        self.snf2_new_ver = json_dict["snf_new_ver"]
        self.snf2_param = json_dict["extra_param"]
        self.extra_param_string()
        self.truvari = self.set_truvari(f'{self.data_dir}/{json_dict["truvari"]}')
        self.truvari_version = self.truvari["version"]
        self.skip_old = bool(json_dict["skip_old"])
        self.skip_new = bool(json_dict["skip_new"])
        self.truvari2 = self.set_truvari(f'{self.data_dir}/{json_dict["truvari2"]}') if json_dict["truvari2"] != "" else None

    def extra_param_string(self):
        if len(self.snf2_param) > 0:
            self.snf2_param_string = " ".join("  ".join(self.snf2_param.split(",")).split(":"))
        else:
            self.snf2_param_string = self.snf2_param

    @staticmethod
    def set_truvari(json_file):
        return json.load(open(json_file, "r"))


class GIABBench(object):
    def __init__(self, bench_args: GIABBenchParam, bench_id, src_path):
        self.args = bench_args
        self.id = bench_id
        self.src_path = src_path
        self.logger = setup_log(__name__, True)
    
    def sniffles_run(self, version: str):
        if "old" == version:
            use_ver = self.args.snf2_old_ver
            use_bin = self.args.snf2_old
        elif "new" == version:
            use_ver = self.args.snf2_new_ver
            use_bin = self.args.snf2_new
        else:
            self.logger.error(f"Not a known version: {version}, exiting with error")
            sys.exit(0)
        self.logger.info(f"Sniffles2 {version} version")
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_call_{use_ver}.out')
        job.set_error(f'log_{self.id}_snf2_call_{use_ver}.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_jname(f'call{use_ver}')
        cmd = " ".join([
            f'{self.src_path}/scripts/sniffles.sh',
            use_bin,
            self.args.bam,
            f'{self.args.output}_{use_ver}',
            self.args.reference, 
            self.args.tandem_rep,
            f'"{self.args.snf2_param_string}"'
        ])
        job.make(cmd)
        job.submit()
        return job

    def compare(self, old, new, bench_name=""):
        self.logger.info(f'Sniffles2 bench compare: {bench_name}')
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_bench_giab.out')
        job.set_error(f'log_{self.id}_snf2_bench_giab.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_jname(f'trvGIAB')
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
        self.logger.info(f'Running GIAB SV-bench v1.')
        cmd = " ".join([
            f'{self.src_path}/scripts/truvari.sh', 
            f'{self.args.output}_{self.args.snf2_old_ver}.vcf.gz',
            f'{self.args.output}_{self.args.snf2_old_ver}_bench',
            f'{self.args.output}_{self.args.snf2_new_ver}.vcf.gz',
            f'{self.args.output}_{self.args.snf2_new_ver}_bench',
            self.args.truvari["vcf"],
            self.args.truvari["bed"],
            self.args.reference,
            self.args.truvari["bench"], "1"
        ])
        job.make(cmd)
        job.submit()
        if self.args.truvari2 is not None:
            job2 = jobs_slurm.SubmitJobsSlurm()
            job2.set_output(f'log_{self.id}_snf2_bench_cmrg2.out')
            job2.set_error(f'log_{self.id}_snf2_bench_cmrg2.err')
            job2.set_chdir(f'{self.args.dir_out}')
            job2.set_jname(f'trvCMRG')
            if self.args.skip_old and self.args.skip_new:
                self.logger.error(f'Both analysis have the "skip" option on... none has run.')
            elif self.args.skip_old:
                self.logger.info(f'Only using new version of Sniffles2.')
                job2.set_dependencies(f'afterok:{new.job_id}')
            elif self.args.skip_new:
                self.logger.info(f'Only using current version of Sniffles2.')
                job2.set_dependencies(f'afterok:{old.job_id}')
            else:
                self.logger.info(f'Using both versions of Sniffles2.')
                job2.set_dependencies(f'afterok:{old.job_id},{new.job_id}')
            # truvari command
            self.logger.info(f'Running GIAB SV-bench CMRG.')
            cmd = " ".join([
                f'{self.src_path}/scripts/truvari.sh',
                f'{self.args.output}_{self.args.snf2_old_ver}.vcf.gz',
                f'{self.args.output}_{self.args.snf2_old_ver}_bench',
                f'{self.args.output}_{self.args.snf2_new_ver}.vcf.gz',
                f'{self.args.output}_{self.args.snf2_new_ver}_bench',
                self.args.truvari2["vcf"],
                self.args.truvari2["bed"],
                self.args.reference,
                self.args.truvari2["bench"], "0"
            ])
            job2.make(cmd)
            job2.submit()

    def bench(self):
        sniffles_current = None
        sniffles_new = None
        if not self.args.skip_old:
            sniffles_current = self.sniffles_run("old")
        if not self.args.skip_new:
            sniffles_new = self.sniffles_run("new")
        if sniffles_new is not None or sniffles_new is not None:
            self.compare(sniffles_current, sniffles_new, "GIAB")


class GIABBND(object):
    def __init__(self, bench_args: GIABBenchParam, bench_id, src_path):
        self.args = bench_args
        self.id = bench_id
        self.src_path = src_path
        self.logger = setup_log(__name__, True)
    
    def sniffles_run(self, version: str):
        if "old" == version:
            use_ver = self.args.snf2_old_ver
            use_bin = self.args.snf2_old
        elif "new" == version:
            use_ver = self.args.snf2_new_ver
            use_bin = self.args.snf2_new
        else:
            self.logger.error(f"Not a known version: {version}, exiting with error")
            sys.exit(0)
        self.logger.info(f"Sniffles2 {version} version")
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_call_{use_ver}.out')
        job.set_error(f'log_{self.id}_snf2_call_{use_ver}.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_jname(f'call{use_ver}')
        cmd = " ".join([
            f'{self.src_path}/scripts/sniffles.sh',
            use_bin,
            self.args.bam,
            f'{self.args.output}_{use_ver}',
            self.args.reference, 
            self.args.tandem_rep,
            f'"{self.args.snf2_param_string}"'
        ])
        job.make(cmd)
        job.submit()
        return job

    def compare(self, old, new, bench_name=""):
        self.logger.info(f'Sniffles2 bench compare: {bench_name}')
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_bench_bnds.out')
        job.set_error(f'log_{self.id}_snf2_bench_bnds.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_jname(f'snf2BND')
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
        self.logger.info(f'Running GIAB HG008')
        cmd = " ".join([
            f'{self.src_path}/scripts/truvari.sh', 
            f'{self.args.output}_{self.args.snf2_old_ver}.vcf.gz',
            f'{self.args.output}_{self.args.snf2_old_ver}_bench',
            f'{self.args.output}_{self.args.snf2_new_ver}.vcf.gz',
            f'{self.args.output}_{self.args.snf2_new_ver}_bench',
            self.args.truvari["vcf"],
            self.args.truvari["bed"],
            self.args.reference,
            self.args.truvari["bench"], "1"
        ])
        job.make(cmd)
        job.submit()

    def bench(self):
        sniffles_current = None
        sniffles_new = None
        if not self.args.skip_old:
            sniffles_current = self.sniffles_run("old")
        if not self.args.skip_new:
            sniffles_new = self.sniffles_run("new")
        if sniffles_new is not None or sniffles_new is not None:
            self.logger.warning("WiP: BNDs")
            # self.compare(sniffles_current, sniffles_new, "BNDs")


class HapMapMosaic(object):
    def __init__(self, bench_args: GIABBenchParam, bench_id, src_path):
        self.args = bench_args
        self.id = bench_id
        self.src_path = src_path
        self.logger = setup_log(__name__, True)
    
    def sniffles_run(self, version: str):
        if "old" == version:
            use_ver = self.args.snf2_old_ver
            use_bin = self.args.snf2_old
        elif "new" == version:
            use_ver = self.args.snf2_new_ver
            use_bin = self.args.snf2_new
        else:
            self.logger.error(f"Not a known version: {version}, exiting with error")
            sys.exit(0)
        self.logger.info(f"Sniffles2 {version} version")
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_call_{use_ver}.out')
        job.set_error(f'log_{self.id}_snf2_call_{use_ver}.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_jname(f'call{use_ver}')
        cmd = " ".join([
            f'{self.src_path}/scripts/sniffles_mosaic.sh',
            use_bin,
            self.args.bam,
            f'{self.args.output}_{use_ver}',
            self.args.reference, 
            self.args.tandem_rep,
            f'"{self.args.snf2_param_string}"'
        ])
        job.make(cmd)
        job.submit()
        return job

    def compare(self, old, new, bench_name=""):
        self.logger.info(f'Sniffles2 bench compare: {bench_name}')
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_bench_mosaic.out')
        job.set_error(f'log_{self.id}_snf2_bench_mosaic.err')
        job.set_chdir(f'{self.args.dir_out}')
        if not os.path.exists(f'{self.args.dir_out}'):
            os.mkdir(f'{self.args.dir_out}')
        job.set_jname(f'trvMIMS')
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
        self.logger.info(f'Running SMaHT HapMap (mosaic)')
        cmd = " ".join([
            f'{self.src_path}/scripts/truvari_mosaic.sh',
            f'{self.args.output}_{self.args.snf2_old_ver}.vcf.gz',
            f'{self.args.output}_{self.args.snf2_old_ver}_bench',
            f'{self.args.output}_{self.args.snf2_new_ver}.vcf.gz',
            f'{self.args.output}_{self.args.snf2_new_ver}_bench',
            self.args.truvari["vcf"],
            self.args.truvari["bed"],
            self.args.reference,
            self.args.truvari["bench"], "1"
        ])
        job.make(cmd)
        job.submit()

    def bench(self):
        sniffles_current = None
        sniffles_new = None
        if not self.args.skip_old:
            sniffles_current = self.sniffles_run("old")
        if not self.args.skip_new:
            sniffles_new = self.sniffles_run("new")
        if sniffles_new is not None or sniffles_new is not None:
            self.compare(sniffles_current, sniffles_new, "Mosaic")


class SeverusParam(object):
    def __init__(self):
        self.bam_ont = ""
        self.bam_pb = ""
        self.directory = ""
        self.tandem_repeat = ""
        self.truvari = ""
        self.skip_step = ""
        self.version = ""

    def set_parameters_from_json(self, json_dict, base_dir, data_dir, reference):
        self.base_dir = base_dir
        self.data_dir = data_dir
        self.reference = reference        
        self.bam_ont = f'{self.data_dir}/{json_dict["bam_ont"]}'
        self.bam_pb = f'{self.data_dir}/{json_dict["bam_pb"]}'
        self.directory = f'{self.base_dir}/{json_dict["directory"]}'
        self.tandem_repeat = json_dict["tandem_repeat"]
        self.truvari = self.set_truvari(f'{self.data_dir}/{json_dict["truvari"]}')
        self.truvari["bench"] = "giabsv_hg38_v1"
        self.skip_step = bool(json_dict["skip_step"])
        self.version = json_dict["version"]

    @staticmethod
    def set_truvari(json_file):
        return json.load(open(json_file, "r"))



class SeverusBench(object):
    def __init__(self, bench_args: SeverusParam, bench_id, src_path):
        self.args = bench_args
        self.id = bench_id
        self.src_path = src_path
        self.logger = setup_log(__name__, True)
    
    def severus_run(self, version: str):
        self.logger.info(f"Severus, assumed to be in $PATH")
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_sev.out')
        job.set_error(f'log_{self.id}_sev.err')
        job.set_chdir(f'{self.args.directory}')
        job.set_chdir(f'{self.args.directory}')
        if not os.path.exists(f'{self.args.directory}'):
            os.mkdir(f'{self.args.directory}')
        job.set_jname(f'callSev')
        cmd = " ".join([
            f'{self.src_path}/scripts/severus.sh',
            self.args.tandem_repeat,
            self.args.bam_ont,
            self.args.bam_pb
        ])
        job.make(cmd)
        job.submit()
        return job

    def compare(self, severus_sv_run, bench_name=""):
        self.logger.info(f'Severus bench: {bench_name}')
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_severus_bench_giab.out')
        job.set_error(f'log_{self.id}_severus_bench_giab.err')
        job.set_chdir(f'{self.args.directory}')
        job.set_dependencies(f'afterok:{severus_sv_run.job_id}')
        job.set_jname(f'trvGIAB')
        # truvari command
        self.logger.info(f'Running GIAB SV-bench Q100')
        cmd = " ".join([
            f'{self.src_path}/scripts/truvari.sh', 
            f'{self.args.directory}/ont/all_SVs/severus_all.vcf.gz',
            f'severus_bench_ont',
            f'{self.args.directory}/pb/all_SVs/severus_all.vcf.gz',
            f'severus_bench_pb',
            self.args.truvari["vcf"],
            self.args.truvari["bed"],
            self.args.reference,
            self.args.truvari["bench"], "1"
        ])
        job.make(cmd)
        job.submit()

    def bench(self):
        if self.args.skip_step:
            return None
        severus_sv = self.severus_run(self.args.version)
        if severus_sv is not None:
            self.compare(severus_sv, "GIAB")
