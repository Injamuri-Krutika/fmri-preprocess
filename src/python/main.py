from make_FSL_timings import Make_FSL_Timings
from create_design_file import Create_Design
import subprocess


def remove_run_folders():
    subprocess.call(["./remove.sh"])


def main():
    # Make_FSL_Timings().run()
    Create_Design().run()


if __name__ == "__main__":
    # remove_run_folders()
    main()
