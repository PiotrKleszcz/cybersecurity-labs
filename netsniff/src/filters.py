PRESET_FILTERS = {
    "http":  "tcp port 80",
    "https": "tcp port 443",
    "dns":   "udp port 53",
    "ftp":   "tcp port 21",
    "ssh":   "tcp port 22",
    "icmp":  "icmp",
    "arp":   "arp",
    "tcp":   "tcp",
    "udp":   "udp",
}

def get_filter(name: str) -> str:
    return PRESET_FILTERS.get(name.lower(), name)
