# Read the standby status of HDDs using hdparm.

from prometheus_client import start_http_server, Gauge

import subprocess
import sys
import time


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
    if len(sys.argv) < 2:
        print("Usage: python3 main.py </dev/disk1> </dev/disk2> ...")
        sys.exit(1)


if __name__ == '__main__':
    check_arguments()
    start_http_server(8000)
    gauge = Gauge('drive_status', 'standby status of the HDD. 0 means standby, 1 means active.', ['disk'])
    while True:
        for i in range(1, len(sys.argv)):
            gauge.labels(sys.argv[i]).set(get_drive_status(sys.argv[i]))
        time.sleep(10)
