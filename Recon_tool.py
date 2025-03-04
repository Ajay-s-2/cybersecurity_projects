#!/usr/bin/env python3

import os
import sys
import subprocess
import json
from time import sleep
from pathlib import Path

# Colors for CLI
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
MAGENTA = "\033[1;35m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ASCII Art Header
def show_header():
    print(f"{CYAN}")
    print("██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗")
    print("██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║")
    print("██║  ██║█████╗  ██║     ██║   ██║██╔██╗ ██║")
    print("██║  ██║██╔══╝  ██║     ██║   ██║██║╚██╗██║")
    print("██████╔╝██║     ╚██████╗╚██████╔╝██║ ╚████║")
    print("╚═════╝ ╚═╝      ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝")
    print(f"{RESET}")
    print(f"{DIM}Interactive Reconnaissance Toolkit v2.1{RESET}\n")

# Tool paths (update these if needed)
TOOLS = {
    "subfinder": "subfinder",
    "nmap": "nmap",
    "httpx": "httpx",
    "gowitness": "gowitness",
    "nuclei": "nuclei",
    "ffuf": "ffuf",
    "theHarvester": "theHarvester",
    "jq": "jq",
}

# Check if all tools are installed
def check_dependencies():
    print(f"{YELLOW}[*] Checking dependencies...{RESET}")
    missing = []
    for tool, command in TOOLS.items():
        if not shutil.which(command):
            missing.append(tool)
    if missing:
        print(f"{RED}[!] Missing tools: {', '.join(missing)}{RESET}")
        print(f"{YELLOW}[*] Install them and try again.{RESET}")
        sys.exit(1)
    print(f"{GREEN}[+] All dependencies are installed!{RESET}")

# Create output directories
def setup_directories(domain):
    Path(f"{domain}/subdomains").mkdir(parents=True, exist_ok=True)
    Path(f"{domain}/screenshots").mkdir(parents=True, exist_ok=True)
    Path(f"{domain}/scans").mkdir(parents=True, exist_ok=True)
    Path(f"{domain}/reports").mkdir(parents=True, exist_ok=True)

# Subdomain enumeration
def subdomain_enum(domain):
    print(f"{YELLOW}[*] Running Subfinder...{RESET}")
    subfinder_cmd = f"{TOOLS['subfinder']} -d {domain} -o {domain}/subdomains/subfinder.txt"
    subprocess.run(subfinder_cmd, shell=True)
    print(f"{GREEN}[+] Subdomain enumeration complete!{RESET}")

# Port scanning
def port_scan(domain):
    print(f"{YELLOW}[*] Running Nmap...{RESET}")
    nmap_cmd = f"{TOOLS['nmap']} -iL {domain}/subdomains/subfinder.txt -oA {domain}/scans/nmap_scan"
    subprocess.run(nmap_cmd, shell=True)
    print(f"{GREEN}[+] Port scanning complete!{RESET}")

# Web application discovery
def web_discovery(domain):
    print(f"{YELLOW}[*] Running httpx...{RESET}")
    httpx_cmd = f"cat {domain}/subdomains/subfinder.txt | {TOOLS['httpx']} -o {domain}/subdomains/live_subdomains.txt"
    subprocess.run(httpx_cmd, shell=True)
    print(f"{GREEN}[+] Web application discovery complete!{RESET}")

# Screenshotting
def take_screenshots(domain):
    print(f"{YELLOW}[*] Running gowitness...{RESET}")
    gowitness_cmd = f"{TOOLS['gowitness']} file -f {domain}/subdomains/live_subdomains.txt -P {domain}/screenshots"
    subprocess.run(gowitness_cmd, shell=True)
    print(f"{GREEN}[+] Screenshots captured!{RESET}")

# Vulnerability scanning
def vuln_scan(domain):
    print(f"{YELLOW}[*] Running Nuclei...{RESET}")
    nuclei_cmd = f"{TOOLS['nuclei']} -l {domain}/subdomains/live_subdomains.txt -o {domain}/scans/nuclei_results.txt"
    subprocess.run(nuclei_cmd, shell=True)
    print(f"{GREEN}[+] Vulnerability scanning complete!{RESET}")

# Content discovery
def content_discovery(domain):
    print(f"{YELLOW}[*] Running ffuf...{RESET}")
    ffuf_cmd = f"{TOOLS['ffuf']} -w /path/to/wordlist.txt -u https://{domain}/FUZZ -o {domain}/scans/ffuf_results.json"
    subprocess.run(ffuf_cmd, shell=True)
    print(f"{GREEN}[+] Content discovery complete!{RESET}")

# OSINT gathering
def osint_gathering(domain):
    print(f"{YELLOW}[*] Running theHarvester...{RESET}")
    theharvester_cmd = f"{TOOLS['theHarvester']} -d {domain} -b all -f {domain}/reports/osint_results.json"
    subprocess.run(theharvester_cmd, shell=True)
    print(f"{GREEN}[+] OSINT gathering complete!{RESET}")

# Data aggregation
def aggregate_data(domain):
    print(f"{YELLOW}[*] Aggregating data...{RESET}")
    # Example: Parse Nuclei results with jq
    nuclei_results = f"{domain}/scans/nuclei_results.txt"
    if os.path.exists(nuclei_results):
        jq_cmd = f"cat {nuclei_results} | {TOOLS['jq']} '.'"
        subprocess.run(jq_cmd, shell=True)
    print(f"{GREEN}[+] Data aggregation complete!{RESET}")

# Main menu
def main_menu(domain):
    while True:
        show_header()
        print(f"{BOLD}Target: {GREEN}{domain}{RESET}\n")
        print(f"{CYAN}1. Full Automated Recon")
        print("2. Subdomain Enumeration")
        print("3. Port Scanning")
        print("4. Web Application Discovery")
        print("5. Screenshotting")
        print("6. Vulnerability Scanning")
        print("7. Content Discovery")
        print("8. OSINT Gathering")
        print("9. View Reports")
        print("10. Exit{RESET}")

        choice = input(f"\n{GREEN}[?] Select an option [1-10]: {RESET}")

        if choice == "1":
            subdomain_enum(domain)
            port_scan(domain)
            web_discovery(domain)
            take_screenshots(domain)
            vuln_scan(domain)
            content_discovery(domain)
            osint_gathering(domain)
            aggregate_data(domain)
        elif choice == "2":
            subdomain_enum(domain)
        elif choice == "3":
            port_scan(domain)
        elif choice == "4":
            web_discovery(domain)
        elif choice == "5":
            take_screenshots(domain)
        elif choice == "6":
            vuln_scan(domain)
        elif choice == "7":
            content_discovery(domain)
        elif choice == "8":
            osint_gathering(domain)
        elif choice == "9":
            aggregate_data(domain)
        elif choice == "10":
            print(f"{YELLOW}[*] Exiting...{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[!] Invalid choice!{RESET}")

# Main function
def main():
    if len(sys.argv) != 2:
        print(f"{RED}[!] Usage: {sys.argv[0]} <domain>{RESET}")
        sys.exit(1)

    domain = sys.argv[1]
    check_dependencies()
    setup_directories(domain)
    main_menu(domain)

if __name__ == "__main__":
    main()
