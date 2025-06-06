from concurrent.futures import ThreadPoolExecutor
from port_scanner import generate_port_chunks, scan, Workers
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description="Fast Python Port Scanner")
    parser.add_argument("-ip", "--ip_address", required=True, help="Target IP address to scan")
    parser.add_argument("-p", "--port_range", required=True, help="Port range to scan (e.g., 20-80)")
    parser.add_argument("-w", "--workers", type=int, default=10, help="Number of worker threads (default: 10)")
    parser.add_argument("-t", "--timeout", type=float, default=1, help="Socket timeout in seconds (default: 1)")
    parser.add_argument("-s", "--stealth", help="Run in stealth mode (no output)")
    args = parser.parse_args()

    ip_address = args.ip_address
    port_range = args.port_range
    timeout = args.timeout
    workers= args.workers

    port_ranges = port_range.split('-')
    ports_per_worker = (int(port_ranges[1])-int(port_ranges[0]))//workers  # Number of ports each worker will handle


    if (ip_address.count('.') != 3 or not all(part.isdigit() and 0 <= int(part) < 256 for part in ip_address.split('.'))):
        print("Invalid IP address format. Please provide a valid IPv4 address.")
        return
    
    if not (port_range.count('-') == 1 and all(part.isdigit() and 0 <= int(part) <= 65535 for part in port_range.split('-'))):
        print("Invalid port range format. Please provide a valid range (e.g., 20-80).")
        return

    MAX_WORKERS = Workers(port_range, ports_per_worker)


    port_chunks = generate_port_chunks(port_range, MAX_WORKERS)

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(scan, [ip_address] * len(port_chunks), port_chunks, [timeout] * len(port_chunks))

    end_time = time.time()
    print(f"Scanning completed in {end_time - start_time:.2f} seconds")          
      


if __name__ == "__main__":
    main()      

