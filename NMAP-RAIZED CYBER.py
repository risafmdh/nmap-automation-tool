#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
from datetime import datetime

try:
    from colorama import init, Fore, Back, Style

    init(autoreset=True)

except ImportError:

    class Dummy:

        def __getattr__(self, name):
            return ""

    Fore = Back = Style = Dummy()


# ============================================================
# BLUENZ NMAP AUTOMATION
# Colorful Terminal Edition
# ============================================================

VERSION = "3.0"

SCANS = {

    # ================= SIMPLE =================

    1: ("Basic Scan", "SIMPLE", []),
    2: ("Host Discovery", "SIMPLE", ["-sn"]),
    3: ("Ping Scan", "SIMPLE", ["-PE"]),
    4: ("TCP Connect Scan", "SIMPLE", ["-sT"]),
    5: ("SYN Scan", "SIMPLE", ["-sS"]),
    6: ("Fast Scan", "SIMPLE", ["-F"]),
    7: ("Top 10 Ports", "SIMPLE", ["--top-ports", "10"]),
    8: ("Top 20 Ports", "SIMPLE", ["--top-ports", "20"]),
    9: ("Top 50 Ports", "SIMPLE", ["--top-ports", "50"]),
    10: ("Top 100 Ports", "SIMPLE", ["--top-ports", "100"]),
    11: ("Top 200 Ports", "SIMPLE", ["--top-ports", "200"]),
    12: ("Common Web Ports", "SIMPLE",
         ["-p", "80,443,8080,8443"]),
    13: ("SSH Port", "SIMPLE", ["-p", "22"]),
    14: ("FTP Port", "SIMPLE", ["-p", "21"]),
    15: ("DNS Port", "SIMPLE", ["-p", "53"]),
    16: ("SMTP Ports", "SIMPLE",
         ["-p", "25,465,587"]),
    17: ("Database Ports", "SIMPLE",
         ["-p", "1433,1521,3306,5432,6379,27017"]),
    18: ("Remote Access Ports", "SIMPLE",
         ["-p", "22,23,3389"]),
    19: ("Web Service Detection", "SIMPLE",
         ["-p", "80,443", "-sV"]),
    20: ("SSH Service Detection", "SIMPLE",
         ["-p", "22", "-sV"]),
    21: ("FTP Service Detection", "SIMPLE",
         ["-p", "21", "-sV"]),
    22: ("HTTP Service Detection", "SIMPLE",
         ["-p", "80,443", "-sV"]),
    23: ("HTTPS Detection", "SIMPLE",
         ["-p", "443", "-sV"]),
    24: ("Common Services", "SIMPLE",
         ["-sV", "--top-ports", "50"]),
    25: ("Service Version Scan", "SIMPLE",
         ["-sV"]),
    26: ("OS Detection", "SIMPLE",
         ["-O"]),
    27: ("OS Detection Limited", "SIMPLE",
         ["-O", "--osscan-limit"]),
    28: ("Default NSE Scripts", "SIMPLE",
         ["-sC"]),
    29: ("HTTP Title", "SIMPLE",
         ["-p", "80,443", "--script", "http-title"]),
    30: ("HTTP Headers", "SIMPLE",
         ["-p", "80,443", "--script", "http-headers"]),
    31: ("HTTP Methods", "SIMPLE",
         ["-p", "80,443", "--script", "http-methods"]),
    32: ("DNS Discovery", "SIMPLE",
         ["-p", "53", "--script", "dns-service-discovery"]),
    33: ("SSL Certificate", "SIMPLE",
         ["-p", "443", "--script", "ssl-cert"]),
    34: ("Traceroute", "SIMPLE",
         ["--traceroute"]),
    35: ("Service + Scripts", "SIMPLE",
         ["-sV", "-sC"]),

    # ================= MEDIUM =================

    36: ("Full TCP Connect", "MEDIUM",
         ["-sT", "-p-"]),
    37: ("Full TCP SYN", "MEDIUM",
         ["-sS", "-p-"]),
    38: ("Full TCP + Version", "MEDIUM",
         ["-sS", "-sV", "-p-"]),
    39: ("Full TCP + Scripts", "MEDIUM",
         ["-sS", "-sC", "-p-"]),
    40: ("Full TCP + OS", "MEDIUM",
         ["-sS", "-O", "-p-"]),
    41: ("TCP Version Detection", "MEDIUM",
         ["-sV", "--top-ports", "1000"]),
    42: ("TCP Default Scripts", "MEDIUM",
         ["-sC", "--top-ports", "1000"]),
    43: ("TCP OS + Version", "MEDIUM",
         ["-O", "-sV", "--top-ports", "1000"]),
    44: ("TCP Scripts + Version", "MEDIUM",
         ["-sC", "-sV", "--top-ports", "1000"]),
    45: ("TCP Enumeration", "MEDIUM",
         ["-sS", "-sV", "-sC", "--top-ports", "1000"]),
    46: ("UDP Top 10", "MEDIUM",
         ["-sU", "--top-ports", "10"]),
    47: ("UDP Top 20", "MEDIUM",
         ["-sU", "--top-ports", "20"]),
    48: ("UDP Top 50", "MEDIUM",
         ["-sU", "--top-ports", "50"]),
    49: ("UDP Top 100", "MEDIUM",
         ["-sU", "--top-ports", "100"]),
    50: ("UDP DNS", "MEDIUM",
         ["-sU", "-p", "53"]),
    51: ("UDP DHCP", "MEDIUM",
         ["-sU", "-p", "67,68"]),
    52: ("UDP SNMP", "MEDIUM",
         ["-sU", "-p", "161"]),
    53: ("UDP NTP", "MEDIUM",
         ["-sU", "-p", "123"]),
    54: ("UDP TFTP", "MEDIUM",
         ["-sU", "-p", "69"]),
    55: ("UDP Version Detection", "MEDIUM",
         ["-sU", "-sV", "--top-ports", "50"]),
    56: ("OS Detection", "MEDIUM",
         ["-O"]),
    57: ("OS + Version", "MEDIUM",
         ["-O", "-sV"]),
    58: ("OS + Scripts", "MEDIUM",
         ["-O", "-sC"]),
    59: ("OS + Version + Scripts", "MEDIUM",
         ["-O", "-sV", "-sC"]),
    60: ("Service Enumeration", "MEDIUM",
         ["-sV", "-sC", "--top-ports", "1000"]),
    61: ("HTTP Enumeration", "MEDIUM",
         ["-p", "80,443,8080,8443", "-sV", "-sC"]),
    62: ("SSH Enumeration", "MEDIUM",
         ["-p", "22", "-sV", "-sC"]),
    63: ("FTP Enumeration", "MEDIUM",
         ["-p", "21", "-sV", "-sC"]),
    64: ("SMTP Enumeration", "MEDIUM",
         ["-p", "25,465,587", "-sV", "-sC"]),
    65: ("DNS Enumeration", "MEDIUM",
         ["-p", "53", "-sV", "-sC"]),
    66: ("Database Enumeration", "MEDIUM",
         ["-p", "1433,1521,3306,5432,6379,27017",
          "-sV", "-sC"]),
    67: ("Remote Service Enumeration", "MEDIUM",
         ["-p", "22,23,3389", "-sV", "-sC"]),
    68: ("Web + SSH Enumeration", "MEDIUM",
         ["-p", "22,80,443,8080,8443", "-sV", "-sC"]),
    69: ("Infrastructure Scan", "MEDIUM",
         ["-sS", "-sV", "-sC", "--top-ports", "1000"]),
    70: ("Complete Medium Scan", "MEDIUM",
         ["-sS", "-sV", "-sC", "-O",
          "--top-ports", "1000"]),

    # ================= AGGRESSIVE =================

    71: ("Aggressive Scan", "AGGRESSIVE",
         ["-A"]),
    72: ("Aggressive TCP", "AGGRESSIVE",
         ["-A", "-sS"]),
    73: ("Aggressive Top 100", "AGGRESSIVE",
         ["-A", "--top-ports", "100"]),
    74: ("Aggressive Top 1000", "AGGRESSIVE",
         ["-A", "--top-ports", "1000"]),
    75: ("Aggressive Full TCP", "AGGRESSIVE",
         ["-A", "-p-"]),
    76: ("Aggressive Fast", "AGGRESSIVE",
         ["-A", "-T4"]),
    77: ("Aggressive Timing", "AGGRESSIVE",
         ["-A", "-T5"]),
    78: ("Aggressive Service", "AGGRESSIVE",
         ["-A", "-sV"]),
    79: ("Aggressive NSE", "AGGRESSIVE",
         ["-A", "-sC"]),
    80: ("Aggressive OS", "AGGRESSIVE",
         ["-A", "-O"]),
    81: ("Deep TCP Enumeration", "AGGRESSIVE",
         ["-sS", "-sV", "-sC", "-O",
          "-p-", "-T4"]),
    82: ("Deep TCP Top 1000", "AGGRESSIVE",
         ["-sS", "-sV", "-sC", "-O",
          "--top-ports", "1000", "-T4"]),
    83: ("Comprehensive Web", "AGGRESSIVE",
         ["-sS", "-sV", "-sC",
          "-p", "80,443,8080,8443", "-T4"]),
    84: ("Comprehensive SSH", "AGGRESSIVE",
         ["-sS", "-sV", "-sC",
          "-p", "22", "-T4"]),
    85: ("Comprehensive FTP", "AGGRESSIVE",
         ["-sS", "-sV", "-sC",
          "-p", "21", "-T4"]),
    86: ("Comprehensive DNS", "AGGRESSIVE",
         ["-sS", "-sV", "-sC",
          "-p", "53", "-T4"]),
    87: ("Comprehensive SMTP", "AGGRESSIVE",
         ["-sS", "-sV", "-sC",
          "-p", "25,465,587", "-T4"]),
    88: ("Comprehensive Database", "AGGRESSIVE",
         ["-sS", "-sV", "-sC",
          "-p", "1433,1521,3306,5432,6379,27017",
          "-T4"]),
    89: ("Comprehensive Remote Services", "AGGRESSIVE",
         ["-sS", "-sV", "-sC",
          "-p", "22,23,3389", "-T4"]),
    90: ("Full TCP Aggressive", "AGGRESSIVE",
         ["-A", "-p-", "-T4"]),
    91: ("Aggressive Top 100", "AGGRESSIVE",
         ["-A", "--top-ports", "100", "-T4"]),
    92: ("Aggressive Top 1000", "AGGRESSIVE",
         ["-A", "--top-ports", "1000", "-T4"]),
    93: ("Aggressive Web", "AGGRESSIVE",
         ["-A", "-p", "80,443,8080,8443", "-T4"]),
    94: ("Aggressive Infrastructure", "AGGRESSIVE",
         ["-A", "--top-ports", "1000", "-T4"]),
    95: ("Version Intensity 9", "AGGRESSIVE",
         ["-sS", "-sV", "--version-intensity", "9",
          "--top-ports", "1000"]),
    96: ("Aggressive NSE Enumeration", "AGGRESSIVE",
         ["-sS", "-sV", "-sC",
          "--top-ports", "1000", "-T4"]),
    97: ("Authorized Vulnerability Discovery", "AGGRESSIVE",
         ["-sV", "--script", "vuln",
          "--top-ports", "1000"]),
    98: ("Authorized Vulnerability Services", "AGGRESSIVE",
         ["-sS", "-sV", "--script", "vuln",
          "--top-ports", "1000"]),
    99: ("Authorized Comprehensive", "AGGRESSIVE",
         ["-A", "--script", "vuln",
          "--top-ports", "1000", "-T4"]),
    100: ("Full Authorized Assessment", "AGGRESSIVE",
         ["-A", "--script", "vuln", "-p-", "-T4"]),
}


# ============================================================
# COLORS
# ============================================================

def category_color(category):

    if category == "SIMPLE":
        return Fore.GREEN

    if category == "MEDIUM":
        return Fore.YELLOW

    if category == "AGGRESSIVE":
        return Fore.RED

    return Fore.WHITE


# ============================================================
# BANNER
# ============================================================

def banner():

    os.system(
        "clear" if os.name != "nt" else "cls"
    )

    print(Fore.CYAN + Style.BRIGHT)

    print(r"""
  ███████╗██╗████████╗███████╗    ███████╗███████╗██████╗
  ██╔════╝██║╚══██╔══╝██╔════╝    ██╔════╝██╔════╝██╔
  ███████╗██║   ██║   █████╗      ███████╗█████╗  ██║ 
  ╚════██║██║   ██║   ██╔══╝      ╚════██║██╔══╝  ██║ 
  ███████║██║   ██║   ███████╗    ███████║███████╗██████╔╝
  ╚══════╝╚═╝   ╚═╝   ╚══════╝    ╚══════╝╚══════╝╚═════╝ 

              C Y B E R   S E C U R I T Y
             N M A P   A U T O M A T I O N
""")

    print(
        Fore.CYAN
        + "=" * 70
    )

    print(
        Fore.WHITE
        + Style.BRIGHT
        + "                 BLUENZ SECURITY TOOLKIT"
    )

    print(
        Fore.CYAN
        + f"                         v{VERSION}"
    )

    print(
        Fore.CYAN
        + "=" * 70
    )


# ============================================================
# MENU
# ============================================================

def menu_section(title, start, end, color):

    print()
    print(
        color
        + Style.BRIGHT
        + f"┌── {title} ─────────────────────────────┐"
    )

    for number in range(start, end + 1):

        name, category, arguments = SCANS[number]

        print(
            color
            + f"│ {number:03d} │ "
            + Fore.WHITE
            + f"{name:<47}"
            + color
            + "│"
        )

    print(
        color
        + "└──────────────────────────────────────────────────────┘"
    )


def print_menu():

    menu_section(
        "SIMPLE SCANS  [01-35]",
        1,
        35,
        Fore.GREEN
    )

    menu_section(
        "MEDIUM SCANS  [36-70]",
        36,
        70,
        Fore.YELLOW
    )

    menu_section(
        "  AGGRESSIVE SCANS   ",
        71,
        100,
        Fore.RED
    )

    print()
    print(
        Fore.CYAN
        + Style.BRIGHT
        + " [0] "
        + Fore.WHITE
        + "EXIT"
    )


# ============================================================
# GET SCAN
# ============================================================

def get_scan_number():

    while True:

        choice = input(
            Fore.CYAN
            + "\n┌─[ "
            + Fore.WHITE
            + "SELECT SCAN"
            + Fore.CYAN
            + " ]─> "
        ).strip()

        if not choice.isdigit():

            print(
                Fore.RED
                + "[!] Enter a number."
            )

            continue

        number = int(choice)

        if number == 0:

            return 0

        if number not in SCANS:

            print(
                Fore.RED
                + "[!] Invalid scan number."
            )

            continue

        return number


# ============================================================
# TARGET
# ============================================================

def get_target():

    while True:

        target = input(
            Fore.CYAN
            + "┌─[ "
            + Fore.WHITE
            + "TARGET"
            + Fore.CYAN
            + " ]─> "
        ).strip()

        if not target:

            print(
                Fore.RED
                + "[!] Target cannot be empty."
            )

            continue

        forbidden = [
            ";",
            "&",
            "|",
            "`",
            "$",
            ">",
            "<",
            "\n",
            "\r"
        ]

        if any(
            char in target
            for char in forbidden
        ):

            print(
                Fore.RED
                + "[!] Invalid target."
            )

            continue

        return target


# ============================================================
# COMMAND PREVIEW
# ============================================================

def show_preview(scan_number, target):

    name, category, arguments = SCANS[scan_number]

    command = [
        "nmap"
    ] + arguments + [target]

    color = category_color(category)

    print()

    print(
        color
        + Style.BRIGHT
        + "══════════════════════════════════════════════════════════════"
    )

    print(
        color
        + "                         SCAN PREVIEW                          "
    )

    print(
        color
        + "══════════════════════════════════════════════════════════════"
    )

    print(
        Fore.WHITE
        + f" NUMBER : {scan_number:<50}"
    )

    print(
        Fore.WHITE
        + f" NAME   : {name:<50}"
    )

    print(
        color
        + f" TYPE   : {category:<50}"
    )

    print(
        Fore.WHITE
        + f" TARGET : {target:<50}"
    )

    print(
        color
        + "══════════════════════════════════════════════════════════════"
    )

    print(
        Fore.WHITE
        + " COMMAND:                                                     "
    )

    print(
        Fore.CYAN
        + " "
        + " ".join(command)[:60].ljust(60)
        + " "
    )

    print(
        color
        + "══════════════════════════════════════════════════════════════"
    )


# ============================================================
# OUTPUT DIRECTORY
# ============================================================

def create_output_directory():

    date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    directory = os.path.join(
        "nmap_results",
        date
    )

    os.makedirs(
        directory,
        exist_ok=True
    )

    return directory


# ============================================================
# SAFE FILE NAME
# ============================================================

def safe_filename(value):

    return "".join(
        char
        if char.isalnum() or char in "._-"
        else "_"
        for char in value
    )


# ============================================================
# RUN
# ============================================================

def run_scan(scan_number, target):

    name, category, arguments = SCANS[scan_number]

    show_preview(
        scan_number,
        target
    )

    print()

    print(
        Fore.YELLOW
        + Style.BRIGHT
        + "⚠ AUTHORIZATION CHECK"
    )

    print(
        Fore.WHITE
        + "Only scan systems you own or are authorized to test."
    )

    confirm = input(
        Fore.CYAN
        + "\n┌─[ "
        + Fore.WHITE
        + "RUN SCAN"
        + Fore.CYAN
        + " ]─> "
    ).strip().lower()

    if confirm not in (
        "y",
        "yes"
    ):

        print(
            Fore.YELLOW
            + "\n[!] Scan cancelled."
        )

        return

    output_directory = (
        create_output_directory()
    )

    timestamp = datetime.now().strftime(
        "%H-%M-%S"
    )

    clean_target = safe_filename(
        target
    )

    base = (
        f"scan_{scan_number:03d}_"
        f"{clean_target}_"
        f"{timestamp}"
    )

    txt_file = os.path.join(
        output_directory,
        base + ".txt"
    )

    xml_file = os.path.join(
        output_directory,
        base + ".xml"
    )

    command = (
        ["nmap"]
        + arguments
        + [target]
        + [
            "-oN",
            txt_file,
            "-oX",
            xml_file
        ]
    )

    print()

    print(
        Fore.CYAN
        + "══════════════════════════════════════════════════════════════"
    )

    print(
        Fore.CYAN
        + "                    SCAN STARTING                           "
    )

    print(
        Fore.CYAN
        + "══════════════════════════════════════════════════════════════"
    )

    print()

    print(
        Fore.GREEN
        + "[+] "
        + Fore.WHITE
        + f"Profile : {name}"
    )

    print(
        Fore.GREEN
        + "[+] "
        + Fore.WHITE
        + f"Target  : {target}"
    )

    print(
        Fore.GREEN
        + "[+] "
        + Fore.WHITE
        + f"Output  : {txt_file}"
    )

    print()

    try:

        result = subprocess.run(
            command,
            check=False
        )

        print()

        if result.returncode == 0:

            print(
                Fore.GREEN
                + Style.BRIGHT
                + "══════════════════════════════════════════════════════════════"
            )

            print(
                Fore.GREEN
                + "                  ✓ SCAN COMPLETED                          "
            )

            print(
                Fore.GREEN
                + "══════════════════════════════════════════════════════════════"
            )

        else:

            print(
                Fore.RED
                + f"[!] Nmap exited with code: {result.returncode}"
            )

        print()

        print(
            Fore.CYAN
            + "[+] TXT: "
            + Fore.WHITE
            + txt_file
        )

        print(
            Fore.CYAN
            + "[+] XML: "
            + Fore.WHITE
            + xml_file
        )

    except KeyboardInterrupt:

        print()

        print(
            Fore.YELLOW
            + "\n[!] Scan interrupted by user."
        )

    except FileNotFoundError:

        print(
            Fore.RED
            + "\n[!] Nmap executable not found."
        )

    except PermissionError:

        print(
            Fore.RED
            + "\n[!] Permission denied."
        )

    except Exception as error:

        print(
            Fore.RED
            + f"\n[!] Error: {error}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    check = shutil.which("nmap")

    if check is None:

        print(
            Fore.RED
            + Style.BRIGHT
            + "\n[!] Nmap is not installed or not in PATH."
        )

        print(
            Fore.YELLOW
            + "Try: nmap --version"
        )

        sys.exit(1)

    while True:

        banner()

        print_menu()

        scan_number = get_scan_number()

        if scan_number == 0:

            print(
                Fore.CYAN
                + "\n[+] BLUENZ Nmap Automation stopped."
            )

            break

        target = get_target()

        run_scan(
            scan_number,
            target
        )

        input(
            Fore.CYAN
            + "\nPress ENTER to return to menu..."
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()
