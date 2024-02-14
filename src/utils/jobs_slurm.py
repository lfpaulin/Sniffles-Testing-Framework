import subprocess
from logger import setup_log


class SubmitJobsSlurm(object):
    # init
    def __init__(self):
        #
        self.output = ""
        self.error = ""
        self.chdir = ""
        self.params = ""
        self.log_job_id = ""
        self.job_id = None
        self.dependencies = ""
        self.job_starter = ""
        self.logger = setup_log(__name__, True)

    def set_output(self, this_output):
        self.output = this_output

    def set_error(self, this_error):
        self.error = this_error

    def set_chdir(self, this_chdir):
        self.chdir = this_chdir

    def set_params(self, this_params):
        self.params = this_params

    def set_job_id(self, this_job_id):
        self.job_id = this_job_id

    def set_dependencies(self, this_dependencies):
        self.dependencies = f'--dependency={this_dependencies}'

    def make(self, script):
        # with job id in file
        self.job_starter = f'sbatch {self.dependencies} --output {self.output} --error {self.error} ' \
                           f'--chdir {self.chdir}  {self.params}  {script}'
        self.logger.info(f'CMD: {self.job_starter}')

    def submit(self):
        run_cmd = subprocess.run(self.job_starter, shell=True, capture_output=True, text=True)
        if run_cmd.stderr != "":
            self.logger.error(run_cmd.stderr)
        else:
            self.logger.info(run_cmd.stdout)
            self.set_job_id(self.get_job_id_from_stdout(job_stdout=run_cmd.stdout.rstrip("\n")))

    @staticmethod
    def get_job_id_from_stdout(job_stdout=None):
        # SBATCH prints: Submitted batch job XXXX
        return job_stdout.split(" ")[-1] if job_stdout is not None else '0'

    # slurm based
    def check_job(self):
        os_call = subprocess.run(f'squeue --long | grep "{self.job_id}"', shell=True, capture_output=True, text=True)
        my_job_status = [info for info in os_call.stdout.split(" ") if info != ""]
        return ",".join(my_job_status)

    def is_job_running(self):
        return self.check_job != ""
