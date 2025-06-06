from concurrent.futures import ThreadPoolExecutor
import socket
import multiprocessing



def generate_port_chunks(port_range,MAX_WORKERS):
    port_ranges = port_range.split('-')
    port_chunks= []

    chunk_size= int((int(port_ranges[1]) - int(port_ranges[0])) / MAX_WORKERS)

    for i in range(MAX_WORKERS):
        start= int(port_ranges[0]) + (chunk_size*i)
        end= start + chunk_size 
        port_chunks.append((start, end))
    return port_chunks    



def scan(ip_address, port_chunk,timeout):
   # print(f"Scanning ports {port_chunk[0]}-{port_chunk[1]} on {ip_address}")
    print(f"Using timeout: {timeout}")
    for port in range(int(port_chunk[0]), int(port_chunk[1])):
        
        try:
            scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scan_socket.settimeout(timeout)  # Set a timeout for the socket connection
            scan_socket.connect((ip_address, port))
            print(f"Port {port} is open")

        except:
            None    



def Workers(port,ports_per_worker):
    port_ranges = port.split('-')
    start_port = int(port_ranges[0])
    end_port = int(port_ranges[1])

    cpu_cores = multiprocessing.cpu_count()
    ideal_cap = cpu_cores * 50  # e.g., 8 cores * 50 = 400

    # Number of ports each worker will handle

    port_range= end_port - start_port
    max_workers = min(ideal_cap, max(10,port_range // ports_per_worker))

    return max_workers if max_workers > 0 else 1
   