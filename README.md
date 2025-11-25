# network-perf-tool

This is a small network performance benchmarking tool created using iperf3 and Python. This program runs the server from your local machine and the client from a virtual machine.

This tool can be run with `python bench.py <o>`, where `<o>` can be 1 (run TCP test), 2 (run UDP test), or 3 (run both). If not entered on the command line, the user will be prompted for their choice of tests.

Side note: this is not a true test of network speed in its current form, but instead a test of the host's CPU/VM processing speed. It will stay this way until I get a second device or Raspberry Pi that I can use as an actual secondary device!

### TCP Test

The program can run a simple TCP test with no artificial stress. It reports on:

- Measured throughput
- Average RTT, excluding first interval
- Host machine CPU usage
- Remote machine CPU usage
- Likely sources of bottleneck in the network

### UDP Test

The program can run a simple UDP test with no artificial stress. It reports on:

- Measured throughput
- Average jitter
- P95 jitter threshold
- P99 jitter threshold
- Packet loss rate

## Configuration

This repo is designed to run the server on the local machine (Mac) and the client on a virtual machine (Ubuntu Linux) via SSH. I have yet to test it on another device setup.

If you want to clone + run the repo, create a `.env` file with the following fields:  
`VM_IP="<your-vm-ip-addr>"`  
`VM_USERNAME="<your-vm-username>"`  
`VM_PASSWORD="<your-vm-password>"`

Please note that it is much more secure to forego the VM password being hardcoded, and that an ssh
key should really be used. I am planning on switching this, I'm just focusing on finishing the tool first.

Additionally, create a `.logs/` folder for all of the server/client output.

# References

Thanks to the below sources for helping me teach myself this process!

- For learning about subprocesses: https://docs.python.org/3/library/subprocess.html
- For learning how to ssh into my linux VM using python: https://www.paramiko.org
- Great examples of using paramiko for an SSH: https://www.linode.com/docs/guides/use-paramiko-python-to-ssh-into-a-server/
- For understanding output: https://thelinuxcode.com/iperf3-commands/
- And for a great foundation on network topics: https://book.systemsapproach.org/foundation.html
