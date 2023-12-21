from scripts import jobs_slurm

class TrioBenchParam(object):
    def __init__(self):
        self.proband = None
        self.father = None
        self.mother = None
        self.use_snf = None
        self.snf_list = None
        self.dir_out = None
        self.output = None
        self.reference = None
        self.tandem_rep = None
        self.snf2_old = None
        self.snf2_new = None
        self.snf2_param = None
        self.snf2_param_string = None
        self.bcftools_version = None

    def set_parameters_from_json(self, json_dict):
        self.proband = json_dict["proband"]
        self.father = json_dict["father"]
        self.mother = json_dict["mother"]
        self.use_snf = json_dict["use_snf"]
        self.snf_list = json_dict["snf_list"]
        self.dir_out = json_dict["directory"]
        self.output = json_dict["output"]
        self.reference = json_dict["reference"]
        self.tandem_rep = json_dict["tandem_repeat"]
        self.snf2_old = json_dict["snf_current"]
        self.snf2_new = json_dict["snf_new"]
        self.snf2_param = json_dict["extra_param"]
        self.extra_param_string()
        self.bcftools_version = json_dict["bcftools_version"]

    def extra_param_string(self):
        if len(self.snf2_param) > 0:
            self.snf2_param_string = " ".join("  ".join(self.snf2_param.split(",")).split(":"))
        else:
            self.snf2_param_string = self.snf2_param


class TrioBench(object):
    def __init__(self, bench_args, bench_id, src_path):
        self.args = bench_args
        self.id = bench_id
        self.src_path = src_path
    
    def sniffles_current(self):
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_old_trio.out')
        job.set_error(f'log_{self.id}_snf2_old_trio.err')
        job.set_chdir(f'{self.args.dir_out}')
        if bool(self.args.use_snf):
            cmd = f'{self.src_path}/scripts/sniffles_mendelian_snf.sh  {self.args.snf2_old} '\
                  f'{self.args.proband}  {self.args.father}  {self.args.mother}  {self.args.output}_old  ' \
                  f'{self.args.reference}  {self.args.tandem_rep}  "{self.args.snf2_param_string}" '
        else:
            cmd = f'{self.src_path}/scripts/sniffles_mendelian_snf.sh  {self.args.snf2_old} '\
                  f'{self.args.snf_list}  {self.args.output}_old  ' \
                  f'{self.args.reference}  {self.args.tandem_rep}  "{self.args.snf2_param_string}" '
        job.make(cmd)
        job.submit()
        return job

    def sniffles_new(self):
        job = jobs_slurm.SubmitJobsSlurm()
        job.set_output(f'log_{self.id}_snf2_new_trio.out')
        job.set_error(f'log_{self.id}_snf2_new_trio.err')
        job.set_chdir(f'{self.args.dir_out}')
        if bool(self.args.use_snf):
            cmd = f'{self.src_path}/scripts/sniffles_mendelian_snf.sh  {self.args.snf2_new} '\
                  f'{self.args.proband}  {self.args.father}  {self.args.mother}  {self.args.output}_new  ' \
                  f'{self.args.reference}  {self.args.tandem_rep}  "{self.args.snf2_param_string}" '
        else:
            cmd = f'{self.src_path}/scripts/sniffles_mendelian_snf.sh  {self.args.snf2_new} '\
                  f'{self.args.snf_list}  {self.args.output}_new  ' \
                  f'{self.args.reference}  {self.args.tandem_rep}  "{self.args.snf2_param_string}" '
        job.make(cmd)
        job.submit()
        return job

    def compare(self, old, new):
        pass  # TODO:
        # job = jobs_slurm.SubmitJobsSlurm()
        # job.set_output(f'log_{self.id}_snf2_trio_compare.out')
        # job.set_error(f'log_{self.id}_snf2_trio_compare.err')
        # job.set_chdir(f'{self.args.dir_out}')
        # job.set_dependencies(f'afterok:{old.job_id},{new.job_id}')
        # cmd = f''
        # job.make(cmd)
        # job.submit()

    def bench(self):
        sniffles_current = self.sniffles_current()
        sniffles_new = self.sniffles_new()
        self.compare(sniffles_current, sniffles_new)
