import paramiko # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

VM_IP = os.getenv("VM_IP")
VM_USERNAME = os.getenv("VM_USERNAME")
VM_PASSWORD = os.getenv("VM_PASSWORD")

    

# Run command on ssh
def exec_cmd(cmd, kill_cmd=None):
    # open ssh
    vm = paramiko.client.SSHClient()
    vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    vm.connect(VM_IP, username=VM_USERNAME, password=VM_PASSWORD)

    # execute command, decode output
    _, stdout, stderr = vm.exec_command(cmd)
    stdout.channel.recv_exit_status() 
    output = stdout.read().decode()
    error = stderr.read().decode()
    if error is not '':
        print('Client error:', error)

    if kill_cmd is not None:
        # ensure no remote processes are left hanging
        vm.exec_command(kill_cmd)

    # close connection
    vm.close()
    return output, error