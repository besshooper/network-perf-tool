import json
import os

client_output_file = '.logs/client_output.json'
server_output_file = '.logs/server_output.json'


def main():
    print('Loading files....')
    client_data = load_file_json(client_output_file)
    print('[✓] Client output data loaded')

    server_data  = load_file_json(server_output_file)
    print('[✓] Server output data loaded')

    if (client_data is None or server_data is None):
        print('Ending analysis.')
        return
    print()

    # now analyze the json data!
    client_sent = client_data['end']['sum_sent']
    print_sr_data(client_sent, 'Client', 'sent')
    server_sent = server_data['end']['sum_sent']
    print_sr_data(server_sent, 'Server', 'sent')
    print()

    # now received data
    client_received = client_data['end']['sum_received']
    print_sr_data(client_received, 'Client', 'received')
    server_received = server_data['end']['sum_received']
    print_sr_data(server_received, 'Server', 'received')

    

def print_sr_data(data, agent, action):
    print(f'{agent} {action}:')
    print('  -', data['bits_per_second'], 'bits per second')
    print('  - in', data['seconds'], 'seconds')
    if ('retransmits' in data):
        print('  - with', data['retransmits'], 'retransmissions')
    

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


if __name__ == "__main__":
    main()