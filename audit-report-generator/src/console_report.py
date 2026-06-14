"""
console_report.py
Prints a colour-coded terminal summary after scanning — mirrors netsniff reporter style.
"""

from colorama import Fore, Style, init
from tabulate import tabulate
from src.analyser import Finding, summarise

init(autoreset=True)

SEVERITY_COLOURS = {
    "Critical": Fore.RED,
    "High":     Fore.YELLOW,
    "Medium":   Fore.CYAN,
    "Low":      Fore.GREEN,
    "Info":     Fore.WHITE,
}


def _colour(severity: str, text: str) -> str:
    return f"{SEVERITY_COLOURS.get(severity, '')}{text}{Style.RESET_ALL}"


def print_host_table(hosts: list[dict]) -> None:
    rows = []
    for h in hosts:
        port_list = ", ".join(str(p["port"]) for p in h.get("ports", []))
        rows.append([
            h["ip"],
            h.get("hostname") or "—",
            h.get("os") or "Unknown",
            str(len(h.get("ports", []))),
            port_list or "—",
        ])

    print("\n" + "=" * 70)
    print("  HOST INVENTORY")
    print("=" * 70)
    print(tabulate(rows, headers=["IP Address", "Hostname", "OS", "Open Ports", "Port List"], tablefmt="simple"))


def print_findings_summary(findings: list[Finding]) -> None:
    counts = summarise(findings)

    print("\n" + "=" * 70)
    print("  FINDINGS SUMMARY")
    print("=" * 70)

    severity_rows = [
        [_colour(sev, sev), _colour(sev, str(count))]
        for sev, count in counts.items()
    ]
    print(tabulate(severity_rows, headers=["Severity", "Count"], tablefmt="simple"))
    print(f"\n  Total findings: {len(findings)}")


def print_findings_table(findings: list[Finding]) -> None:
    print("\n" + "=" * 70)
    print("  DETAILED FINDINGS")
    print("=" * 70)

    rows = []
    for i, f in enumerate(findings, 1):
        host = f"{f.host_ip}" + (f" ({f.hostname})" if f.hostname else "")
        port = f"{f.port}/{f.protocol}" if f.port else "N/A"
        rows.append([
            str(i),
            _colour(f.severity, f.severity),
            f"{f.cvss:.1f}" if f.cvss > 0 else "—",
            host,
            port,
            f.title[:52] + "…" if len(f.title) > 52 else f.title,
        ])

    print(tabulate(rows, headers=["#", "Severity", "CVSS", "Host", "Port", "Finding"], tablefmt="simple"))


def print_nis2_summary(compliance_map: dict) -> None:
    print("\n" + "=" * 70)
    print("  NIS2 COMPLIANCE OVERVIEW")
    print("=" * 70)

    rows = []
    for article, data in sorted(compliance_map.items()):
        status = data["status"]
        if status == "Non-Compliant":
            status_str = _colour("Critical", status)
        elif status == "Partially Compliant":
            status_str = _colour("Medium", status)
        else:
            status_str = _colour("Info", status)

        rows.append([
            article,
            data["title"][:42] + "…" if len(data["title"]) > 42 else data["title"],
            status_str,
            str(data["findings_count"]) if data["findings_count"] else "—",
        ])

    print(tabulate(rows, headers=["Article", "Control", "Status", "Findings"], tablefmt="simple"))


def print_report(hosts: list[dict], findings: list[Finding], compliance_map: dict) -> None:
    print_host_table(hosts)
    print_findings_summary(findings)
    print_findings_table(findings)
    print_nis2_summary(compliance_map)
    print("\n" + "=" * 70 + "\n")
