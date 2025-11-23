from dotenv import load_dotenv # type: ignore
import os
from iperf.server import open_server, close_server
from iperf.client import exec_cmd

SERVER_IP = os.getenv("SERVER_IP")

def main():
    print('Running network analysis...')

    # open output files
    fserver = open("./.logs/server_output.txt", "w")
    fclient = open("./.logs/client_output.txt", "w")

    # boot up server with relevant output file
    server = open_server(fserver)

    # query client
    # TODO: add more options for users to include as flags.
    cmd = f"iperf3 -c {SERVER_IP} --json"
    try:
        client_output, client_err = exec_cmd(cmd)
        # write outputs
        fclient.write(client_output)
    except:
        fclient.write("err")

    # clean up!
    fclient.close()
    fserver.close()
    close_server(server)
    print('Finished running analysis.')



if __name__ == "__main__":
    main()