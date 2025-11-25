# network-perf-tool

Small network performance benchmarking tool using iperf3 and Python. This program runs the server from your local machine and the client from a virtual machine.

## configuration

This repo is designed to run the server on the local machine and the client on an ssh. I set it
up to work with my server Macbook/client Ubuntu linux virtual machine (via Parallels), and have yet
to test it on another device setup.

If you want to clone + run the repo, create a `.env` file with the following fields:  
`VM_IP="<your-vm-ip-addr>"`  
`VM_USERNAME="<your-vm-username>"`  
`VM_PASSWORD="<your-vm-password>"`

Please note that it is much more secure to forego the VM password being hardcoded, and that an ssh
key should really be used. I am planning on switching this, I'm just focusing on finishing the tool first.

Additionally, create a `.logs/` folder for all of the server/client output.

# references

- For learning about subprocesses: https://docs.python.org/3/library/subprocess.html
- For learning how to ssh into my linux VM using python: https://www.paramiko.org
- Great examples of using paramiko for an SSH: https://www.linode.com/docs/guides/use-paramiko-python-to-ssh-into-a-server/
