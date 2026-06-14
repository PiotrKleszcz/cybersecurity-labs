"""
analyser.py
Maps open ports/services to findings from vulnerability_db.json.
Assigns CVSS scores and severity levels. Returns a sorted finding list.
"""

import json
import os
from dataclasses import dataclass, field


SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "vulnerability_db.json")


@dataclass
class Finding:
    host_ip: str
    hostname: str
    port: int
    protocol: str
    service: str
    service_version: str
    title: str
    severity: str
    cvss: float
    description: str
    remediation: str
    nis2_articles: list[str] = field(default_factory=list)
    cve_refs: list[str] = field(default_factory=list)

    @property
    def evidence(self) -> str:
        version = f" ({self.service_version})" if self.service_version else ""
        return f"Port {self.port}/{self.protocol} open — {self.service}{version}"

    @property
    def severity_rank(self) -> int:
        return SEVERITY_ORDER.get(self.severity, 99)


def _load_db() -> dict:
    with open(DB_PATH, "r") as f:
        return json.load(f)


def analyse(hosts: list[dict]) -> list[Finding]:
    """Analyse scan results and return findings sorted by severity."""
    db = _load_db()
    port_db = db.get("ports", {})
    general_db = db.get("general", {})
    findings = []

    for host in hosts:
        ip = host["ip"]
        hostname = host.get("hostname", "")
        open_ports = host.get("ports", [])

        for port_info in open_ports:
            port_num = str(port_info["port"])
            entry = port_db.get(port_num)
            if entry is None:
                continue

            findings.append(Finding(
                host_ip=ip,
                hostname=hostname,
                port=port_info["port"],
                protocol=port_info.get("protocol", "tcp"),
                service=port_info.get("service", entry.get("service", "")),
                service_version=port_info.get("version", ""),
                title=entry["title"],
                severity=entry["severity"],
                cvss=entry["cvss"],
                description=entry["description"],
                remediation=entry["remediation"],
                nis2_articles=entry.get("nis2_articles", []),
                cve_refs=entry.get("cve_refs", []),
            ))

        threshold = general_db.get("many_open_ports", {}).get("threshold", 10)
        if len(open_ports) > threshold:
            entry = general_db["many_open_ports"]
            findings.append(Finding(
                host_ip=ip,
                hostname=hostname,
                port=0,
                protocol="",
                service="multiple",
                service_version="",
                title=entry["title"],
                severity=entry["severity"],
                cvss=entry["cvss"],
                description=entry["description"],
                remediation=entry["remediation"],
                nis2_articles=entry.get("nis2_articles", []),
            ))

    findings.sort(key=lambda f: (f.severity_rank, -f.cvss))
    return findings


def summarise(findings: list[Finding]) -> dict:
    """Return count of findings per severity level."""
    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Info": 0}
    for f in findings:
        if f.severity in counts:
            counts[f.severity] += 1
    return counts
