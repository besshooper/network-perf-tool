import json
import os
from parser import load_file_json
import matplotlib.pyplot as plt # type: ignore

# Directory of relevant logs
LOG_DIR = "./.logs"

# TCP test output
TCP_FILE = os.path.join(LOG_DIR, "test_tcp_output.json")
# UDP test outputs
UDP_CLIENT_FILE = os.path.join(LOG_DIR, "test_udp_client_output.json")
UDP_SERVER_FILE = os.path.join(LOG_DIR, "test_udp_server_output.json")

# Plots TCP throughput over the time the test was run
def plot_tcp():
    data = load_file_json(TCP_FILE)
    if not data or "intervals" not in data:
        # no data exists to plot
        print("[!] No TCP data to plot.")
        return

    times = []
    throughput_mbps = []

    # plot each interval - get end timestamp
    # and compute the throughput
    for interval in data["intervals"]:
        summary = interval.get("sum", {})
        times.append(summary.get("end", 0))
        bps = summary.get("bits_per_second", 0)
        throughput_mbps.append(bps / 1e6)

    # simple line plot
    plt.figure()
    plt.plot(times, throughput_mbps)
    plt.xlabel("Time (s)")
    plt.ylabel("Throughput (Mbps)")
    plt.title("TCP Throughput Over Time")
    plt.grid(True)
    plt.show()

# Plot throughput and packet loss as a function
# of time for UDP tests
def plot_udp():
    data = load_file_json(UDP_CLIENT_FILE)
    if not data or "intervals" not in data:
        # no data was loaded to plot
        print("[!] No UDP client data to plot.")
        return

    times = []
    throughput_mbps = []
    loss_percent = []

    for interval in data["intervals"]:
        # for each interval, find the end timestamp
        # and compute throughput and loss.
        summary = interval.get("sum", {})
        times.append(summary.get("end", 0))
        throughput_mbps.append(summary.get("bits_per_second", 0) / 1e6)
        loss_percent.append(summary.get("lost_percent", 0))

    # Throughput plot
    plt.figure()
    plt.plot(times, throughput_mbps)
    plt.xlabel("Time (s)")
    plt.ylabel("Throughput (Mbps)")
    plt.title("UDP Throughput Over Time")
    plt.grid(True)
    plt.show()

    # Packet loss plot
    plt.figure()
    plt.plot(times, loss_percent)
    plt.xlabel("Time (s)")
    plt.ylabel("Packet Loss (%)")
    plt.title("UDP Packet Loss Over Time")
    plt.grid(True)
    plt.show()


def main():
    # Generate plots based on user input

    print('Would you like to plot (1) TCP test results, (2) UDP test results, or (3) both?')
    option = int(input())
    print("Generating plots...")

    if option == 1 or option == 3:
        if os.path.exists(TCP_FILE):
            plot_tcp()
        else:
            print("[i] No TCP log found.")
    if option == 2 or option == 3:
        if os.path.exists(UDP_CLIENT_FILE):
            plot_udp()
        else:
            print("[i] No UDP log found.")
    print('Done')


if __name__ == "__main__":
    main()