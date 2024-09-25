import socket
import time
import requests
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

def print_banner():
    print(Fore.MAGENTA + r"""
    ╔══╗────╔══╗╔═╗╔═╗╔╗╔╗  
    ╚╗╗║╔══╗╚╗╔╝║╦╝║╔╝║╚╝║  
    ╔╩╝║╚══╝─║║─║╩╗║╚╗║╔╗║  
    ╚══╝─────╚╝─╚═╝╚═╝╚╝╚╝  
    ──────────────────────  
    ▄▄  █  ▄▄▄▄▄    ▄▄▄▄▄▄▄▄▄      ▄▄▄▄▄  ▄▄▄▄  ▄▄▄▄   ▄▄▄▄▄▄ 
    ████ █  █        █   ▄▄▄▄      █       █    █ █    █   █
    █ █ █ █  █  ▄    █   █ █ █     █       █    █ █    █   █
    █ █ █ █  █ █ █   █   █▄█▄█     █       █    █ █    █   █
    █▄█▄█▄█  █▄▄▄▄   █   ▄▄  █     ▀▀▀▀▀▀▀▀▀▀    █ █    █   █
                         D-TECH SNI Host Checker
    ==================================================
    """)

def test_tcp_connection(host):
    try:
        start_time = time.time()
        socket.setdefaulttimeout(5)  # Timeout for the socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, 443))  # Connect to port 443 for HTTPS
        tcp_time = round(time.time() - start_time, 2)
        print(Fore.GREEN + f"[✔] TCP connection successful in {tcp_time} seconds.")
        return True, tcp_time
    except Exception as e:
        print(Fore.RED + f"[✘] TCP connection failed: {str(e)}")
        return False, None

def test_https_request(host):
    try:
        start_time = time.time()
        response = requests.get(f'https://{host}', timeout=5)
        http_time = round(time.time() - start_time, 2)
        if response.status_code == 200:
            print(Fore.GREEN + f"[✔] HTTPS GET request successful in {http_time} seconds.")
            return True, http_time
        else:
            print(Fore.RED + f"[✘] HTTPS GET request failed with status code: {response.status_code}")
            return False, None
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[✘] HTTPS GET request failed: {str(e)}")
        return False, None

def test_sni_connection(sni_host):
    tcp_success, tcp_time = test_tcp_connection(sni_host)
    http_success, http_time = test_https_request(sni_host)

    # Set rating to 0% if either connection fails
    if not tcp_success or not http_success:
        print(Fore.RED + "[✘] Connection test failed. Overall rating: 0%")
        return

    # Calculate overall rating if both tests are successful
    total_time = round(tcp_time + http_time, 2)
    rating = 100 - total_time * 10  # Simplified rating calculation
    print(Fore.CYAN + f"[+] Overall rating: {max(0, rating)}%")

def main():
    print_banner()
    sni_host = input(Fore.CYAN + "[+] Enter the SNI host (URL without https://): ")
    print(Fore.YELLOW + "\n[~] Initiating connection test...\n")
    test_sni_connection(sni_host)

if __name__ == "__main__":
    main()
