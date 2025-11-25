import os
from iperf.client import exec_cmd
from util import get_mac_ip_addr


class TestConnection:
    ping_server = '8.8.8.8'

    def test_server_connection(self):
        # tests that the server device (local machine) is connected to 
        # internet by pinging google server
        response = os.system("ping -c 1 " + self.ping_server)
        # and then check the response...
        assert response == 0

    def test_client_reachable(self):
        # test that the client (ssh) can be reachable from this machine
        out, err = exec_cmd("echo hello")

        # If SSH is working, stdout should contain "hello"
        assert "hello" in out, f"Bad SSH connection. stderr={err}"

    def test_client_connection(self):
        # tests that the client device (vm) is connected to 
        # internet by pinging google server
        output, err = exec_cmd("ping -c 1 " + self.ping_server)
        # and then check the response...
        assert "1 packets transmitted" in output or "1 received" in output, f"Ping failed: {output} {err}"

    def test_client_connection_to_server(self):
        # tests that the client device (vm) can connect to the 
        # server device (local). Essentially test that the local device's
        # IP is as expected.
        local_ip = get_mac_ip_addr()
        output, err = exec_cmd("ping -c 1 " + local_ip)
        # and then check the response...
        assert "1 packets transmitted" in output or "1 received" in output, f"Ping failed: {output} {err}"
