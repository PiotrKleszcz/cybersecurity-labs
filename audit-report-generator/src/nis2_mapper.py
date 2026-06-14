"""
nis2_mapper.py
Maps findings to NIS2 Article 21 controls and produces a compliance gap summary.
"""

import json
import os
from collections import defaultdict
from src.analyser import Finding


DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "nis2_controls.json")


def _load_controls() -> dict:
    with open(DB_PATH, "r") as f:
        return json.load(f)


def build_compliance_map(findings: list[Finding]) -> dict:
    """
    Returns a dict mapping each NIS2 article to the list of findings
    that violate it, plus the article title and description.
    """
    controls = _load_controls()
    control_defs = controls.get("controls", {})

    article_to_findings: dict[str, list[Finding]] = defaultdict(list)

    for finding in findings:
        for article in finding.nis2_articles:
            article_to_findings[article].append(finding)

    result = {}
    for article, article_findings in sorted(article_to_findings.items()):
        meta = control_defs.get(article, {})
        worst_severity = min(article_findings, key=lambda f: f.severity_rank).severity
        result[article] = {
            "title": meta.get("title", article),
            "description": meta.get("description", ""),
            "status": "Non-Compliant" if worst_severity in ("Critical", "High") else "Partially Compliant",
            "findings_count": len(article_findings),
            "findings": article_findings,
        }

    all_articles = set(control_defs.keys())
    covered = set(result.keys())
    for article in sorted(all_articles - covered):
        meta = control_defs[article]
        result[article] = {
            "title": meta.get("title", article),
            "description": meta.get("description", ""),
            "status": "No Issues Found",
            "findings_count": 0,
            "findings": [],
        }

    return result
