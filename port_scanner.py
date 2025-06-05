from concurrent.futures import ThreadPoolExecutor
import socket
import time
import argparse


MAX_WORKERS = 100



def generate_port_chunks(port_range):
    port_ranges = port_range.split('-')
    port_chunks= []

    chunk_size= int((int(port_ranges[1]) - int(port_ranges[0])) / MAX_WORKERS)

    for i in range(MAX_WORKERS):
        start= int(port_ranges[0]) + (chunk_size*i)
        end= start + chunk_size 
        port_chunks.append((start, end))
    return port_chunks    



def scan(ip_address, port_chunk):
    print(f"Scanning ports {port_chunk[0]}-{port_chunk[1]} on {ip_address}")

    for port in range(int(port_chunk[0]), int(port_chunk[1])):
        
        try:
            scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scan_socket.settimeout(1)
            scan_socket.connect((ip_address, port))
            print(f"Port {port} is open")

        except:
            None    



def Workers(port_range):
    port_ranges = port_range.split('-')
    start_port = int(port_ranges[0])
    end_port = int(port_ranges[1])

    

    

def main():
    parser = argparse.ArgumentParser(description="Fast Python Port Scanner")
    parser.add_argument("-ip", "--ip_address", required=True, help="Target IP address to scan")
    parser.add_argument("-p", "--port_range", required=True, help="Port range to scan (e.g., 20-80)")
    args = parser.parse_args()

    ip_address = args.ip_address
    port_range = args.port_range

    if (ip_address.count('.') != 3 or not all(part.isdigit() and 0 <= int(part) < 256 for part in ip_address.split('.'))):
        print("Invalid IP address format. Please provide a valid IPv4 address.")
        return
    
    if not (port_range.count('-') == 1 and all(part.isdigit() and 0 <= int(part) <= 65535 for part in port_range.split('-'))):
        print("Invalid port range format. Please provide a valid range (e.g., 20-80).")
        return



    port_chunks = generate_port_chunks(port_range)

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(scan, [ip_address] * len(port_chunks), port_chunks)

    end_time = time.time()
    print(f"Scanning completed in {end_time - start_time:.2f} seconds")          
      

def Workers(port)



if __name__ == "__main__":
    main()      