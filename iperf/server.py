import subprocess

# Starts an iperf3 server on the local machine. Returns the
# reference to the Popen object. Must be closed later!
def open_server(output_file=subprocess.DEVNULL):
    server = subprocess.Popen(["iperf3", "-s", "--json", "--one-off"],stdout=output_file,
    stderr=subprocess.STDOUT)
    return server




    