import subprocess

def get_mac_ip_addr():
    result = subprocess.run(["ipconfig", "getifaddr", "en0"], capture_output=True, text=True)
    # strip newline character
    return result.stdout.strip()

def get_ubuntu_ip_addr():
    result = subprocess.run(["hostname", "-I"], capture_output=True, text=True)
    # strip newline character
    return result.stdout.strip()
