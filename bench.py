from dotenv import load_dotenv # type: ignore
import os
import pytest # type: ignore
from iperf.server import open_server
from iperf.client import exec_cmd
from util import get_mac_ip_addr
from parser import parse_tcp_results, parse_udp_results
import sys
import json

# Runs TCP, UDP, or both iperf3 tests.
# Prints a helpful analysis of tests
def main():
    # first, check network & ssh connections
    print('Running connectivity tests...')
    pytest.main(["tests/test_connection.py"])
    print('[✓] All devices connected.')
    print()
    print('Running network analysis...')

    # Check for command line argument provided with function call
    # that specifies which test to run. Also check for too many
    # args. If no args provided, prompt user to enter option.
    option = None
    if len(sys.argv) > 2:
        print('Too many arguments provided. Only one expected,', len(sys.argv), 'found.')
        return
    elif len(sys.argv) == 1:
        # need user to decide on tcp, udp, or both
        print('Would you like to test (1) TCP, (2) UDP, or (3) both?')
        option = input()
        while (option != '1' and option != '2' and option != '3'):
            if (option == 'quit' or option == 'q'):
                return
            # invalid input!
            print('Invalid input. Please try again, or enter [quit] to quit.')
            option = input()
    else:
        option =  sys.argv[1]

    # get correct ip address
    server_ip = get_mac_ip_addr()

    if option == '1' or option == '3':
        run_tcp_test(server_ip)
        print('[✓] Ran TCP test')
    if option == '2' or option =='3':
        run_udp_test(server_ip)
        print('[✓] Ran UDP test')

    print()
    if option == '1' or option == '3':
        parse_tcp_results()
    if option == '2' or option == '3':
        parse_udp_results()
    print()
    print('Finished running analysis.')

# run a TCP iperf test
def run_tcp_test(server_ip):
    # open output file
    foutput = open("./.logs/test_tcp_output.json", "w")

    # boot up server
    server = open_server()

    # query client
    # TODO: add more options for users to include as flags.
    cmd = f"iperf3 -c {server_ip} --json"
    kill_cmd = "pkill -f iperf3"
    try:
        client_output, client_err = exec_cmd(cmd, kill_cmd=kill_cmd)
        # write outputs
        foutput.write(client_output)
    except:
        foutput.write("err")
    
    
    shutdown(server, [foutput])

# run a UDP iperf test
def run_udp_test(server_ip):
    # open output file
    fclient = open("./.logs/test_udp_client_output.json", "w")
    fserver = open("./.logs/test_udp_server_output.json", "w")

    # boot up server with output file
    server = open_server(fserver)

    # query client
    # TODO: add more options for users to include as flags.
    cmd = f"iperf3 -c {server_ip} -u --json"
    kill_cmd = "pkill -f iperf3"
    try:
        client_output, client_err = exec_cmd(cmd, kill_cmd=kill_cmd)
        # write outputs
        fclient.write(client_output)
    except:
        err = {"error": client_err}
        json.dump(err, fclient)

    shutdown(server, [fclient, fserver])
    

def shutdown(server, foutputs):
    # Wait for the server to finish.
    server.wait(timeout=10)

    # Check if server is still running (it shouldn't be).
    # Kill if necessary.
    if server.poll() is None:
        print('Server still running; killing...')
        server.kill()

    # clean up!
    for output in foutputs:
        output.close()

if __name__ == "__main__":
    main()