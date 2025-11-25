import json
import os
from stats import calculate_latency_threshold, calculate_average_rtt


# Parses statistics relevant to UDP transport in 
# relevant output files
def parse_udp_results():
    test_client_output = '.logs/test_udp_client_output.json'
    test_server_output = '.logs/test_udp_server_output.json'
    client_data = load_file_json(test_client_output)
    server_data = load_file_json(test_server_output)

    if (client_data is None or server_data is None):
        print('Output file could not be parsed. Ending analysis.')
        return
    print()
    print('-------- UDP Results --------')
    # check for error
    if ('error' in client_data):
        print('Error occured in UDP test:', client_data['error'])
        print('-------- End UDP Results --------') 
        return

    # measure throughput
    amount, unit = format_bps(client_data['end']['sum_received']['bits_per_second'])
    print(f'Measured throughput: {amount:.2f} {unit}')

    # measure jitter/latency
    # use accepted heuristics
    # P99 latency = time for which 99% of transmissions took less latency
    # P95 latency: same as above but for 95%
    print(f'Jitter (avg): {client_data['end']['sum_received']['jitter_ms']:.4f} ms')
    p95, p99 = calculate_latency_threshold(server_data)
    print(f"   P95 Jitter Threshold: {p95:.4f} ms")
    print(f"   P99 Jitter Threshold: {p99:.4f} ms")

    # print packet loss
    print(f'Packet loss: {client_data['end']['sum_received']['lost_percent']:.3f}% of packets sent were lost.')

    print('-------- End UDP Results --------')

# parses statistics relevant to TCP transport in 
# relevant output files
def parse_tcp_results():
    test_output = '.logs/test_tcp_output.json'
    test_data = load_file_json(test_output)

    if (test_data is None):
        print('Output file could not be parsed. Ending analysis.')
        return

    print('-------- TCP Results --------')
    # check for error
    if ('error' in test_data):
        print('Error occured in TCP test:', test_data['error'])
        print('-------- End TCP Results --------') 
        return


    # measure throughput
    # measure via the recieved bits, not the sent bits,
    # as that is the functional throughput of the system.
    amount, unit = format_bps(test_data['end']['sum_received']['bits_per_second'])
    print(f'Measured throughput: {amount:.2f} {unit}')

    # measure retransmit rate: retransmits / total packets sent * 100
    num_bytes_sent = test_data['end']['sum_sent']['bytes']
    num_bytes_retransmitted = test_data['end']['sum_sent']['retransmits']
    retransmit_rate = 0
    if num_bytes_retransmitted != 0: 
        retransmit_rate = (num_bytes_retransmitted / num_bytes_sent) * 100
    if (retransmit_rate > 2):
        print(f'[!] High retransmission rate: {retransmit_rate:.2f}%. Your network may be experiencing congestion.')
    else: print(f'[✓] Acceptable retransmission rate: {retransmit_rate:.2f}%')
    # measure average RTT
    average_rtt = calculate_average_rtt(test_data)
    print(f'Average RTT: {average_rtt:.2f} ms')

    # measure cpu utilization percent to check for bottleneck
    # host machine CPU stats
    cpu_stats = test_data['end']['cpu_utilization_percent']
    host_cpu_usage_pct = cpu_stats['host_total']
    host_cpu_system_pct = cpu_stats['host_system']/ host_cpu_usage_pct * 100
    host_cpu_user_pct = cpu_stats['host_user']/ host_cpu_usage_pct * 100
    if (host_cpu_usage_pct >= 50):
        print(f'[!] High host machine CPU usage: {host_cpu_usage_pct:.2f}%')
    elif (host_cpu_usage_pct < 50):
        print(f'[✓] Good host machine CPU usage: {host_cpu_usage_pct:.2f}%')
    print(f'   System funcs used {host_cpu_system_pct:.2f}% of total host CPU.')
    print(f'   User funcs used {host_cpu_user_pct:.2f}% of total host CPU.')
    if (host_cpu_system_pct > 75):
        print('   [!] Your host machine may be bottlenecking your network.')

    # remote machine CPU stats
    remote_cpu_usage_pct = cpu_stats['remote_total']
    remote_cpu_system_pct = cpu_stats['remote_system']/ remote_cpu_usage_pct * 100
    remote_cpu_user_pct = cpu_stats['remote_user']/ remote_cpu_usage_pct * 100
    if (remote_cpu_usage_pct >= 50):
        print(f'[!] High remote machine CPU usage: {remote_cpu_usage_pct:.2f}%')
    elif (remote_cpu_usage_pct < 50):
        print(f'[✓] Good remote machine CPU usage: {remote_cpu_usage_pct:.2f}%')
    print(f'   System funcs used {remote_cpu_system_pct:.2f}% of total remote CPU.')
    print(f'   User funcs used {remote_cpu_user_pct:.2f}% of total remote CPU.')
    if (remote_cpu_system_pct > 75):
        print('   [!] Your remote machine may be bottlenecking your network.')
    
    print('-------- End TCP Results --------')


# loads json data from the inputted file path
def load_file_json(file_path):
    data = None
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Check the path.")
        return None
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from the file.")
        return None

    # close file and return data
    f.close()
    return data

# Formats a size in bits per second into the correct
# bps/kilobits ps/megabits ps/gigabits ps/terrabits ps.
# returns a (size, unit) tuple.
def format_bps(size):
    power = 1000
    n = 0
    power_labels = {0 : '', 1: 'k', 2: 'M', 3: 'G', 4: 'T'}
    while size >= power and n < 4:
        size /= power
        n += 1
    return size, power_labels[n]+'bps'