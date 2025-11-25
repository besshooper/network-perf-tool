import subprocess

# Starts an iperf3 server on the local machine. Returns the
# reference to the Popen object. Must be closed later!
# Prints all output in JSON format to fout.
def open_server(fout):
    server = subprocess.Popen(["iperf3", "-s", "--json", "--one-off"], stdout=fout)
    return server




    