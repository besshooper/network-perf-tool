from dotenv import load_dotenv # type: ignore
import os
import pytest # type: ignore
from iperf.server import open_server
from iperf.client import exec_cmd
from util import get_mac_ip_addr

def main():
    # first, check network & ssh connections
    print('Running connectivity tests...')
    pytest.main(["tests/test_connection.py"])
    print('[✓] All devices connected.')
    print()
    print('Running network analysis...')

    # open output files
    fserver = open("./.logs/server_output.json", "w")
    fclient = open("./.logs/client_output.json", "w")

    # boot up server with relevant output file
    server = open_server(fserver)

    # get correct ip address
    server_ip = get_mac_ip_addr()

    # query client
    # TODO: add more options for users to include as flags.
    cmd = f"iperf3 -c {server_ip} --json"
    kill_cmd = "pkill -f iperf3"
    try:
        client_output, client_err = exec_cmd(cmd, kill_cmd=kill_cmd)
        # write outputs
        fclient.write(client_output)
    except:
        fclient.write("err")
    
    # Wait for the server to finish.
    server.wait(timeout=10)

    # Check if server is still running (it shouldn't be).
    # Kill if necessary.
    if server.poll() is None:
        print('Server still running; killing...')
        server.kill()

    # clean up!
    fclient.close()
    fserver.close()
    print('Finished running analysis.')


if __name__ == "__main__":
    main()