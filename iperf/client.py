import paramiko # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

VM_IP = os.getenv("VM_IP")
VM_USERNAME = os.getenv("VM_USERNAME")
VM_PASSWORD = os.getenv("VM_PASSWORD")

def main():
    print('Connecting to client...')
    # pings google server 5 times, outputs results.
    # can be used to test that ssh connection is succesful
    try: 
        output, err = exec_cmd("ping -c 5 8.8.8.8")
        print(output)
        if err != '':
            print('err:', err)
    except: 
        print('Error executing cmd. Are you connected to the internet?')
    

# Run command on ssh
def exec_cmd(cmd):
    # open ssh
    vm = paramiko.client.SSHClient()
    vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    vm.connect(VM_IP, username=VM_USERNAME, password=VM_PASSWORD)

    # execute command, decode output
    _, stdout, stderr = vm.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()

    # close connection
    vm.close()
    return output, error


    

if __name__ == "__main__":
    main()