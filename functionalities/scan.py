import nmap
import json
import socket
import ipaddress
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox

def ask_scan_choice():
    """
    Display a menu of scan options for the user to choose from.

    Returns:
        int: The user's choice (1-2).
    """
    print("\nSelect a scan type:")
    print("1 - Scan a single IP address")
    print("2 - Scan a subnet based on your current IP")
    
    # Ensure valid input (1-2)
    choice = input("Enter your choice (1-2): ").strip()
    while choice not in ['1', '2']:
        choice = input("Invalid choice. Please enter 1 or 2: ").strip()

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

def show_warning_popup(message):
    """
    Display a warning popup with the provided message.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showwarning("Scan Warning", message)
    root.quit()  # Close the root window after the message is shown

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

def scan_network(network_range, output_folder, progress_callback=None):
    """
    Perform a network scan using nmap on the provided network range.

    Args:
        network_range (str): The network range or single IP to scan.
        output_folder (str): The folder to save the scan results.
        progress_callback (function): Function to update progress (optional).

    Returns:
        dict: Scan results as a dictionary.
    """
    try:
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Initialize the nmap scanner
        nm = nmap.PortScanner()
        print(f"Scanning network: {network_range}...")

        # Scan all ports (1-65535)
        nm.scan(hosts=network_range, arguments='-T4 -p 1-65535 --open')

        # Check if no hosts are found
        if len(nm.all_hosts()) == 0:
            print(f"\n[WARNING] No hosts found in the scan for the range: {network_range}.")
            show_warning_popup(f"No hosts were found during the scan for the range: {network_range}.")
            return None

        # Generate a timestamp for the scan output filenames
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file_json = os.path.join(output_folder, f"{current_time}_scan_results.json")
        output_file_txt = os.path.join(output_folder, f"{current_time}_scan_results.txt")
        
        # Prepare results
        scan_results = {'scan_time': current_time, 'network_range': network_range, 'hosts': []}
        txt_output = []

        # Add a delimiter for the new scan in the text file
        delimiter = f"\n{'='*50}\nScan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*50}\n"
        txt_output.append(delimiter)

        # Scan each host in the range
        for idx, host in enumerate(nm.all_hosts()):
            if progress_callback:
                progress_callback((idx + 1) / len(nm.all_hosts()) * 100)

            host_info = {
                'host': host,
                'status': nm[host].state(),
                'hostname': nm[host].hostname(),
                'os': nm[host].get('osmatch', []),
                'ports': []
            }

            host_txt = f"Host: {host}\nStatus: {nm[host].state()}\n"

            # Handle OS information
            if 'osmatch' in nm[host] and isinstance(nm[host]['osmatch'], list):
                os_matches = ', '.join([str(item) for item in nm[host]['osmatch']])
                host_txt += f"OS: {os_matches}\n"
            
            # Handle port information
            for proto in nm[host].all_protocols():
                for port in nm[host][proto]:
                    port_info = {
                        'port': port,
                        'state': nm[host][proto][port]['state'],
                        'service': nm[host][proto][port].get('name', 'unknown')
                    }
                    host_info['ports'].append(port_info)
                    host_txt += f"Port: {port} - {nm[host][proto][port]['state']} ({nm[host][proto][port].get('name', 'unknown')})\n"
            
            # Add host information to scan results
            scan_results['hosts'].append(host_info)
            txt_output.append(host_txt)

        # Save results to JSON file
        with open(output_file_json, 'a') as json_file:
            json.dump(scan_results, json_file, indent=4)
            json_file.write("\n\n")

        # Save results to TXT file
        with open(output_file_txt, 'a') as txt_file:
            txt_file.write("\n".join(txt_output))

        print(f"Scan completed. Results saved to {output_file_json} and {output_file_txt}.")
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
            scan_network(ip_address, 'scans')  # Save to the 'scans' folder

        elif choice == 2:
            # Scan a subnet based on the current IP
            local_ip = get_local_ip()
            subnet = get_subnet_from_ip(local_ip)
            print(f"Detected subnet: {subnet}")
            scan_network(subnet, 'scans')  # Save to the 'scans' folder

# Run the program
if __name__ == "__main__":
    main()
