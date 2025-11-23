import subprocess

# Starts an iperf3 server on the local machine. Returns the
# reference to the Popen object. Must be closed later!
# Prints all output in JSON format to fout.
def open_server(fout):
    server = subprocess.Popen(["iperf3", "-s", "--json"], stdout=fout)
    return server

# closes the server opened with Popen by open_server().
def close_server(server):
    if (server.poll() is not None):
        # only close if object has not already terminated
        server.terminate()



    