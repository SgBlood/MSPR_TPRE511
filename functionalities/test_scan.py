import nmap
import json
import socket
import ipaddress
from datetime import datetime

def ask_scan_choice():
    """
    Display a menu of scan options for the user to choose from.

    Returns:
        int: The user's choice (1-3).
    """
    print("\nSelect a scan type:")
    print("1 - Scan a single IP address")
    print("2 - Scan a subnet based on your current IP")
    print("3 - Exit the program")
    
    # Ensure valid input (1-3)
    choice = input("Enter your choice (1-3): ").strip()
    while choice not in ['1', '2', '3']:
        choice = input("Invalid choice. Please enter 1, 2, or 3: ").strip()

    return int(choice)

def get_local_ip():
    """
    Get the local IP address of the machine.
    
    Returns:
        str: The local IP address.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # Connect to an external host to determine the local IP
        s.connect(('10.254.254.254', 1))  # This won't actually connect but will determine the local IP
        local_ip = s.getsockname()[0]
    except:
        local_ip = '127.0.0.1'  # Fallback to localhost if unable to detect the local IP
    finally:
        s.close()
    
    return local_ip

def get_subnet_from_ip(local_ip):
    """
    Given a local IP address, calculate the subnet to scan (assuming /24 mask).
    
    Args:
        local_ip (str): The local IP address of the machine.
        
    Returns:
        str: The subnet to scan (e.g., '192.168.1.0/24').
    """
    network = ipaddress.IPv4Network(local_ip + '/24', strict=False)
    return str(network.network_address) + '/24'

def format_scan_results_for_txt(scan_results):
    """
    Format the scan results for a clear, human-readable text file.
    
    Args:
        scan_results (dict): The dictionary containing the scan results.
    
    Returns:
        str: A formatted string to be saved as a text file.
    """
    output = f"Network Scan Results ({scan_results['scan_time']})\n"
    output += f"Network Range: {scan_results['network_range']}\n\n"
    
    for host_info in scan_results["hosts"]:
        output += f"Host: {host_info['host']}\n"
        output += f"  Status: {host_info['status']}\n"
        output += f"  Hostname: {host_info['hostname']}\n"
        output += f"  OS: {host_info['os']}\n"
        
        if host_info['ports']:
            output += f"  Ports:\n"
            for port_info in host_info['ports']:
                output += f"    - Port: {port_info['port']}\n"
                output += f"      State: {port_info['state']}\n"
                output += f"      Service: {port_info['service']}\n"
        else:
            output += "  No open ports detected.\n"
        
        output += "\n"  # Add a newline for separation between hosts

    return output

def scan_network(network_range, output_file_json="network_scan_results.json", output_file_txt="network_scan_results.txt"):
    """
    Perform a network scan using nmap and save the results to both JSON and TXT files.

    Args:
        network_range (str): The network range to scan (e.g., '192.168.1.0/24').
        output_file_json (str): The file where scan results will be stored in JSON format.
        output_file_txt (str): The file where scan results will be stored in text format.
    
    Returns:
        dict: The scan results for the given network.
    """
    try:
        # Initialize the nmap scanner
        nm = nmap.PortScanner()
        print(f"\nScanning network: {network_range}...")

        # Perform the scan using nmap with detailed options
        nm.scan(hosts=network_range, arguments='-A -O')

        # Prepare the results in a dictionary
        scan_results = {
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Include timestamp of scan
            "network_range": network_range,
            "hosts": []
        }

        # Loop over each host in the scan result
        for host in nm.all_hosts():
            host_info = {
                'host': host,
                'status': nm[host].state(),
                'hostname': nm[host].hostname(),
                'os': nm[host].get('osmatch', 'Unknown OS'),
                'ports': []
            }

            # Scan ports and services
            for proto in nm[host].all_protocols():
                for port in nm[host][proto]:
                    port_info = {
                        'port': port,
                        'state': nm[host][proto][port]['state'],
                        'service': nm[host][proto][port].get('name', 'Unknown service')
                    }
                    host_info['ports'].append(port_info)

            scan_results["hosts"].append(host_info)

        # Append the scan results to the JSON file
        try:
            with open(output_file_json, 'r') as file_json:
                all_data = json.load(file_json)
        except (FileNotFoundError, json.JSONDecodeError):
            all_data = {}

        if 'scans' not in all_data:
            all_data['scans'] = []

        all_data['scans'].append(scan_results)

        with open(output_file_json, 'w') as file_json:
            json.dump(all_data, file_json, indent=4, separators=(',', ': '))

        # Format the results for a clear text output
        text_output = format_scan_results_for_txt(scan_results)

        # Append the formatted results to a text file
        with open(output_file_txt, 'a') as file_txt:
            file_txt.write(text_output)

        print(f"\nScan completed. Results saved to {output_file_json} and {output_file_txt}.")
        return scan_results

    except Exception as e:
        print(f"An error occurred during the scan: {e}")
        return None

def main():
    """
    Main function to drive the program, allowing the user to choose scan options and initiate the scan.
    """
    while True:
        # Display the menu and get the user's choice
        choice = ask_scan_choice()

        if choice == 1:
            # Scan a single IP address
            ip_address = input("\nEnter the IP address to scan: ").strip()
            scan_network(ip_address)

        elif choice == 2:
            # Scan a subnet based on the current IP
            local_ip = get_local_ip()
            subnet = get_subnet_from_ip(local_ip)
            print(f"Detected subnet: {subnet}")
            scan_network(subnet)

        elif choice == 3:
            # Exit the program
            print("Exiting the program. Goodbye!")
            break

# Run the program
if __name__ == "__main__":
    main()
