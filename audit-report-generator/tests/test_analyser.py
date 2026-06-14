"""
test_analyser.py
Unit tests for the analyser module — finding detection and severity scoring.
Run with: python3 -m pytest tests/ -v
     or:  python3 tests/test_analyser.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analyser import analyse, summarise, Finding


DEMO_HOSTS = [
    {
        "ip": "192.168.1.10",
        "hostname": "test-host",
        "os": "Linux",
        "ports": [
            {"port": 21,   "protocol": "tcp", "service": "ftp",    "version": "vsftpd 3.0.3"},
            {"port": 22,   "protocol": "tcp", "service": "ssh",    "version": "OpenSSH 8.2"},
            {"port": 23,   "protocol": "tcp", "service": "telnet", "version": ""},
            {"port": 3306, "protocol": "tcp", "service": "mysql",  "version": "MySQL 8.0"},
        ],
    }
]


def test_findings_detected():
    findings = analyse(DEMO_HOSTS)
    assert len(findings) > 0, "Expected findings from demo host"
    print(f"[+] test_findings_detected passed — {len(findings)} findings found")


def test_telnet_is_critical():
    findings = analyse(DEMO_HOSTS)
    telnet = [f for f in findings if f.port == 23]
    assert len(telnet) == 1, "Expected exactly one Telnet finding"
    assert telnet[0].severity == "Critical", f"Expected Critical, got {telnet[0].severity}"
    print(f"[+] test_telnet_is_critical passed — severity: {telnet[0].severity}")


def test_ftp_is_high():
    findings = analyse(DEMO_HOSTS)
    ftp = [f for f in findings if f.port == 21]
    assert len(ftp) == 1, "Expected exactly one FTP finding"
    assert ftp[0].severity == "High", f"Expected High, got {ftp[0].severity}"
    print(f"[+] test_ftp_is_high passed — severity: {ftp[0].severity}")


def test_findings_sorted_by_severity():
    findings = analyse(DEMO_HOSTS)
    ranks = [f.severity_rank for f in findings]
    assert ranks == sorted(ranks), "Findings should be sorted by severity (Critical first)"
    print("[+] test_findings_sorted_by_severity passed")


def test_findings_include_nis2_articles():
    findings = analyse(DEMO_HOSTS)
    for f in findings:
        if f.severity in ("Critical", "High"):
            assert len(f.nis2_articles) > 0, f"High/Critical finding '{f.title}' missing NIS2 articles"
    print("[+] test_findings_include_nis2_articles passed")


def test_summarise_counts_correctly():
    findings = analyse(DEMO_HOSTS)
    counts = summarise(findings)
    total = sum(counts.values())
    assert total == len(findings), f"Summary count {total} != findings count {len(findings)}"
    assert counts["Critical"] >= 1, "Expected at least one Critical finding (Telnet)"
    assert counts["High"] >= 2, "Expected at least two High findings (FTP + MySQL)"
    print(f"[+] test_summarise_counts_correctly passed — {counts}")


def test_unknown_port_ignored():
    hosts_with_unknown = [
        {
            "ip": "192.168.1.20",
            "hostname": "",
            "os": "",
            "ports": [
                {"port": 9999, "protocol": "tcp", "service": "unknown", "version": ""},
            ],
        }
    ]
    findings = analyse(hosts_with_unknown)
    assert len(findings) == 0, f"Expected 0 findings for unknown port, got {len(findings)}"
    print("[+] test_unknown_port_ignored passed")


def test_evidence_string():
    findings = analyse(DEMO_HOSTS)
    ftp = [f for f in findings if f.port == 21][0]
    assert "21/tcp" in ftp.evidence
    assert "ftp" in ftp.evidence.lower() or "vsftpd" in ftp.evidence.lower() or "21" in ftp.evidence
    print(f"[+] test_evidence_string passed — '{ftp.evidence}'")


if __name__ == "__main__":
    tests = [
        test_findings_detected,
        test_telnet_is_critical,
        test_ftp_is_high,
        test_findings_sorted_by_severity,
        test_findings_include_nis2_articles,
        test_summarise_counts_correctly,
        test_unknown_port_ignored,
        test_evidence_string,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__}: {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"  Results: {passed} passed, {failed} failed")
    print(f"{'='*40}\n")
    sys.exit(0 if failed == 0 else 1)
