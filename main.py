# Read the standby status of HDDs using hdparm.

import subprocess
import sys


def get_drive_status(drive_path):
    result = subprocess.run(["hdparm", "-C", drive_path], capture_output=True)
    if result.returncode != 0:
        print(f'Status: {result.returncode}, stdout: {result.stdout}, stderr: {result.stderr}')
        sys.exit(1)
    stdout = result.stdout.decode("utf-8")
    if "active/idle" in stdout:
        return 1
    if "standby" in stdout:
        return 0
    print(f'Unexpected stdout: {stdout}')
    sys.exit(1)


def check_arguments():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py </dev/disk>")
        sys.exit(1)


if __name__ == '__main__':
    check_arguments()
    returnCode = get_drive_status(sys.argv[1])
    sys.exit(returnCode)
