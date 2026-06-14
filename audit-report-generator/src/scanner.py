"""
scanner.py
Runs Nmap and parses XML output into a normalised host list.
Supports: live scan (requires nmap + root), XML file input, demo data.
"""

import subprocess
import xml.etree.ElementTree as ET
import os
from datetime import datetime


def run_nmap(target: str, ports: str = "1-65535", output_dir: str = "scans") -> str:
    """Run Nmap against target and save XML to scans/. Returns path to XML file."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    xml_path = os.path.join(output_dir, f"scan_{timestamp}.xml")

    cmd = [
        "nmap",
        "-sV",          # service/version detection
        "-sC",          # default scripts
        "--open",       # only open ports
        "-p", ports,
        "-oX", xml_path,
        target,
    ]

    print(f"[*] Running: {' '.join(cmd)}")
    print(f"[*] Target: {target}  |  Ports: {ports}")
    print(f"[*] Output: {xml_path}\n")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            raise RuntimeError(f"Nmap error: {result.stderr.strip()}")
    except FileNotFoundError:
        raise RuntimeError("nmap not found. Install with: sudo apt install nmap")
    except subprocess.TimeoutExpired:
        raise RuntimeError("Nmap scan timed out after 10 minutes.")

    return xml_path


def parse_xml(xml_path: str) -> list[dict]:
    """Parse an Nmap XML file and return a list of host dicts."""
    if not os.path.exists(xml_path):
        raise FileNotFoundError(f"XML file not found: {xml_path}")

    tree = ET.parse(xml_path)
    root = tree.getroot()
    hosts = []

    for host_elem in root.findall("host"):
        if host_elem.find("status").get("state") != "up":
            continue

        ip = ""
        hostname = ""

        for addr in host_elem.findall("address"):
            if addr.get("addrtype") == "ipv4":
                ip = addr.get("addr", "")

        hostnames_elem = host_elem.find("hostnames")
        if hostnames_elem is not None:
            hn = hostnames_elem.find("hostname")
            if hn is not None:
                hostname = hn.get("name", "")

        os_name = ""
        os_elem = host_elem.find("os")
        if os_elem is not None:
            match = os_elem.find("osmatch")
            if match is not None:
                os_name = match.get("name", "")

        ports = []
        ports_elem = host_elem.find("ports")
        if ports_elem is not None:
            for port_elem in ports_elem.findall("port"):
                state = port_elem.find("state")
                if state is None or state.get("state") != "open":
                    continue

                service_elem = port_elem.find("service")
                service_name = ""
                service_version = ""
                if service_elem is not None:
                    service_name = service_elem.get("name", "")
                    product = service_elem.get("product", "")
                    version = service_elem.get("version", "")
                    service_version = f"{product} {version}".strip()

                ports.append({
                    "port": int(port_elem.get("portid", 0)),
                    "protocol": port_elem.get("protocol", "tcp"),
                    "service": service_name,
                    "version": service_version,
                })

        if ip:
            hosts.append({
                "ip": ip,
                "hostname": hostname,
                "os": os_name,
                "ports": ports,
            })

    return hosts


def load_demo_data() -> list[dict]:
    """Return hardcoded scan results representing a typical SMB network audit."""
    return [
        {
            "ip": "192.168.1.1",
            "hostname": "router.local",
            "os": "Linux 3.x",
            "ports": [
                {"port": 22,   "protocol": "tcp", "service": "ssh",   "version": "OpenSSH 7.2p2"},
                {"port": 80,   "protocol": "tcp", "service": "http",  "version": "lighttpd 1.4.35"},
                {"port": 443,  "protocol": "tcp", "service": "https", "version": ""},
                {"port": 8080, "protocol": "tcp", "service": "http",  "version": "MiniHTTPServer 1.0"},
            ],
        },
        {
            "ip": "192.168.1.100",
            "hostname": "WINSERVER01",
            "os": "Windows Server 2016",
            "ports": [
                {"port": 80,   "protocol": "tcp", "service": "http",  "version": "Microsoft IIS 10.0"},
                {"port": 135,  "protocol": "tcp", "service": "msrpc", "version": ""},
                {"port": 139,  "protocol": "tcp", "service": "netbios-ssn", "version": ""},
                {"port": 443,  "protocol": "tcp", "service": "https", "version": "Microsoft IIS 10.0"},
                {"port": 445,  "protocol": "tcp", "service": "microsoft-ds", "version": ""},
                {"port": 3389, "protocol": "tcp", "service": "ms-wbt-server", "version": ""},
            ],
        },
        {
            "ip": "192.168.1.101",
            "hostname": "webserver",
            "os": "Ubuntu 20.04",
            "ports": [
                {"port": 21,  "protocol": "tcp", "service": "ftp",  "version": "vsftpd 3.0.3"},
                {"port": 22,  "protocol": "tcp", "service": "ssh",  "version": "OpenSSH 8.2p1"},
                {"port": 80,  "protocol": "tcp", "service": "http", "version": "Apache 2.4.41"},
                {"port": 443, "protocol": "tcp", "service": "https","version": "Apache 2.4.41"},
            ],
        },
        {
            "ip": "192.168.1.105",
            "hostname": "db-server",
            "os": "Ubuntu 22.04",
            "ports": [
                {"port": 22,   "protocol": "tcp", "service": "ssh",        "version": "OpenSSH 8.9p1"},
                {"port": 3306, "protocol": "tcp", "service": "mysql",      "version": "MySQL 8.0.32"},
                {"port": 5432, "protocol": "tcp", "service": "postgresql", "version": "PostgreSQL 14.5"},
                {"port": 6379, "protocol": "tcp", "service": "redis",      "version": "Redis 7.0.5"},
            ],
        },
        {
            "ip": "192.168.1.110",
            "hostname": "old-server",
            "os": "Windows Server 2008 R2",
            "ports": [
                {"port": 23,   "protocol": "tcp", "service": "telnet",         "version": ""},
                {"port": 161,  "protocol": "udp", "service": "snmp",           "version": ""},
                {"port": 445,  "protocol": "tcp", "service": "microsoft-ds",   "version": ""},
                {"port": 1433, "protocol": "tcp", "service": "ms-sql-s",       "version": "Microsoft SQL Server 2012"},
                {"port": 5900, "protocol": "tcp", "service": "vnc",            "version": "VNC protocol 3.8"},
            ],
        },
    ]
