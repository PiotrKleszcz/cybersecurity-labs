"""
pdf_builder.py
Generates a professional PDF security audit report using ReportLab.
Layout: Cover → Executive Summary → Host Inventory → Findings → NIS2 Map → Remediation
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable,
)
from reportlab.platypus.flowables import KeepTogether
from src.analyser import Finding, summarise


# ── Palette ──────────────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#0a1628")
CYAN    = colors.HexColor("#00d8ff")
CRITICAL = colors.HexColor("#dc2626")
HIGH    = colors.HexColor("#ea580c")
MEDIUM  = colors.HexColor("#d97706")
LOW     = colors.HexColor("#059669")
INFO    = colors.HexColor("#0284c7")
LIGHT   = colors.HexColor("#f1f5f9")
BORDER  = colors.HexColor("#cbd5e1")
WHITE   = colors.white
BLACK   = colors.HexColor("#0f172a")

SEVERITY_COLOUR = {
    "Critical": CRITICAL,
    "High":     HIGH,
    "Medium":   MEDIUM,
    "Low":      LOW,
    "Info":     INFO,
}

# ── Styles ────────────────────────────────────────────────────────────────────
def _build_styles():
    base = getSampleStyleSheet()
    custom = {}

    def s(name, **kwargs):
        custom[name] = ParagraphStyle(name, **kwargs)

    s("cover_title",   fontSize=28, fontName="Helvetica-Bold", textColor=WHITE,  alignment=TA_CENTER, leading=34, spaceAfter=8)
    s("cover_sub",     fontSize=14, fontName="Helvetica",      textColor=CYAN,   alignment=TA_CENTER, leading=20, spaceAfter=4)
    s("cover_meta",    fontSize=10, fontName="Helvetica",      textColor=WHITE,  alignment=TA_CENTER, leading=14, spaceAfter=2)
    s("cover_conf",    fontSize=9,  fontName="Helvetica-Bold", textColor=CYAN,   alignment=TA_CENTER, leading=12, spaceBefore=20)

    s("section_h1",    fontSize=18, fontName="Helvetica-Bold", textColor=NAVY,   leading=22, spaceBefore=18, spaceAfter=10)
    s("section_h2",    fontSize=13, fontName="Helvetica-Bold", textColor=NAVY,   leading=17, spaceBefore=14, spaceAfter=6)
    s("body",          fontSize=9,  fontName="Helvetica",      textColor=BLACK,  leading=14, spaceAfter=6)
    s("body_bold",     fontSize=9,  fontName="Helvetica-Bold", textColor=BLACK,  leading=14, spaceAfter=4)
    s("caption",       fontSize=8,  fontName="Helvetica",      textColor=colors.HexColor("#64748b"), leading=11, spaceAfter=4)
    s("finding_title", fontSize=10, fontName="Helvetica-Bold", textColor=NAVY,   leading=14, spaceBefore=10, spaceAfter=4)
    s("code",          fontSize=8,  fontName="Courier",        textColor=BLACK,  leading=12, spaceAfter=4, backColor=LIGHT)
    s("toc_entry",     fontSize=9,  fontName="Helvetica",      textColor=NAVY,   leading=14, spaceAfter=2)
    s("footer_text",   fontSize=8,  fontName="Helvetica",      textColor=colors.HexColor("#94a3b8"), leading=10)

    return custom


# ── Page template ─────────────────────────────────────────────────────────────
def _on_page(canvas, doc, target: str, date_str: str):
    if doc.page == 1:
        return
    canvas.saveState()
    w, h = A4

    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 1.2 * cm, w, 1.2 * cm, fill=True, stroke=False)
    canvas.setFillColor(CYAN)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(1.5 * cm, h - 0.8 * cm, "Fifth Ace — Confidential Security Audit Report")
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(w - 1.5 * cm, h - 0.8 * cm, f"Target: {target}  |  {date_str}")

    canvas.setFillColor(colors.HexColor("#e2e8f0"))
    canvas.rect(0, 0, w, 0.9 * cm, fill=True, stroke=False)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.5 * cm, 0.32 * cm, "This report is confidential. Do not distribute without authorisation.")
    canvas.drawRightString(w - 1.5 * cm, 0.32 * cm, f"Page {doc.page}")

    canvas.restoreState()


# ── Helpers ───────────────────────────────────────────────────────────────────
def _severity_pill(severity: str, styles: dict) -> Paragraph:
    colour = SEVERITY_COLOUR.get(severity, BORDER).hexval().replace("0x", "#")
    return Paragraph(
        f'<font color="{colour}"><b>{severity}</b></font>',
        styles["body"],
    )


def _table_style(header_bg=NAVY) -> TableStyle:
    return TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  header_bg),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0),  9),
        ("ALIGN",       (0, 0), (-1, 0),  "LEFT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 1), (-1, -1), 8),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("GRID",        (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",(0, 0), (-1, -1), 7),
    ])


# ── Section builders ──────────────────────────────────────────────────────────
def _cover_page(target: str, date_str: str, styles: dict) -> list:
    w, h = A4
    story = []

    cover_table = Table(
        [[Paragraph(".", ParagraphStyle("dummy", textColor=NAVY))]],
        colWidths=[w - 4 * cm],
        rowHeights=[h * 0.55],
    )
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), NAVY),
        ("VALIGN",     (0, 0), (0, 0), "MIDDLE"),
    ]))

    def _cover_content():
        elems = [
            Spacer(1, 3 * cm),
            Paragraph("Fifth Ace", styles["cover_sub"]),
            Paragraph("Security Audit Report", styles["cover_title"]),
            HRFlowable(width="60%", thickness=1, color=CYAN, spaceAfter=18),
            Paragraph(f"Target: {target}", styles["cover_meta"]),
            Paragraph(f"Date: {date_str}", styles["cover_meta"]),
            Paragraph("Prepared by: Fifth Ace Cybersecurity", styles["cover_meta"]),
            Spacer(1, 1 * cm),
            Paragraph("CONFIDENTIAL", styles["cover_conf"]),
        ]
        return elems

    story.extend(_cover_content())
    story.append(PageBreak())
    return story


def _exec_summary(hosts: list[dict], findings: list[Finding], styles: dict) -> list:
    counts = summarise(findings)
    story = [Paragraph("Executive Summary", styles["section_h1"])]

    story.append(Paragraph(
        f"This report presents the findings of a network security audit conducted against "
        f"<b>{len(hosts)} hosts</b> in the target environment. The assessment was performed "
        f"using automated port scanning and service enumeration tools, with findings mapped to "
        f"NIS2 Directive Article 21 cybersecurity risk-management controls.",
        styles["body"],
    ))
    story.append(Spacer(1, 0.3 * cm))

    severity_data = [["Severity", "Count", "Action Required"]]
    actions = {
        "Critical": "Immediate remediation — within 24–48 hours",
        "High":     "Urgent remediation — within 7 days",
        "Medium":   "Scheduled remediation — within 30 days",
        "Low":      "Planned remediation — within 90 days",
        "Info":     "Review and document",
    }
    for sev, count in counts.items():
        severity_data.append([sev, str(count), actions[sev]])

    t = Table(severity_data, colWidths=[3.5 * cm, 2.5 * cm, 10 * cm])
    ts = _table_style()

    for i, sev in enumerate(["Critical", "High", "Medium", "Low", "Info"], 1):
        c = SEVERITY_COLOUR[sev]
        ts.add("TEXTCOLOR", (0, i), (0, i), c)
        ts.add("FONTNAME",  (0, i), (0, i), "Helvetica-Bold")

    t.setStyle(ts)
    story.append(t)
    story.append(Spacer(1, 0.4 * cm))

    if counts["Critical"] > 0 or counts["High"] > 0:
        story.append(Paragraph(
            f"⚠ The audit identified <b>{counts['Critical']} Critical</b> and "
            f"<b>{counts['High']} High</b> severity findings that require immediate attention. "
            f"These findings represent significant risk to business continuity and data integrity, "
            f"and indicate non-compliance with NIS2 Article 21 security requirements.",
            styles["body"],
        ))

    story.append(PageBreak())
    return story


def _host_inventory(hosts: list[dict], styles: dict) -> list:
    story = [Paragraph("Host Inventory", styles["section_h1"])]
    story.append(Paragraph(
        f"The following {len(hosts)} hosts were identified as active during the scan.",
        styles["body"],
    ))
    story.append(Spacer(1, 0.2 * cm))

    data = [["IP Address", "Hostname", "Operating System", "Open Ports", "Port List"]]
    for h in hosts:
        ports = h.get("ports", [])
        port_str = ", ".join(str(p["port"]) for p in ports)
        data.append([
            h["ip"],
            h.get("hostname") or "—",
            h.get("os") or "Unknown",
            str(len(ports)),
            Paragraph(port_str or "—", ParagraphStyle("ps", fontSize=8, leading=10)),
        ])

    t = Table(data, colWidths=[3 * cm, 3.5 * cm, 4 * cm, 2.5 * cm, 4.5 * cm])
    t.setStyle(_table_style())
    story.append(t)
    story.append(PageBreak())
    return story


def _findings_overview(findings: list[Finding], styles: dict) -> list:
    story = [Paragraph("Findings Overview", styles["section_h1"])]
    story.append(Paragraph(
        f"The table below lists all {len(findings)} findings identified, sorted by severity. "
        f"Detailed remediation guidance is provided in the following sections.",
        styles["body"],
    ))
    story.append(Spacer(1, 0.2 * cm))

    data = [["#", "Severity", "CVSS", "Host", "Port", "Finding Title"]]
    for i, f in enumerate(findings, 1):
        host = f.host_ip + (f"\n{f.hostname}" if f.hostname else "")
        port = f"{f.port}/{f.protocol}" if f.port else "N/A"
        cvss = f"{f.cvss:.1f}" if f.cvss > 0 else "—"
        data.append([
            str(i),
            Paragraph(f'<b>{f.severity}</b>', ParagraphStyle("sev", fontSize=8, textColor=SEVERITY_COLOUR.get(f.severity, BLACK))),
            cvss,
            Paragraph(host, ParagraphStyle("h", fontSize=8, leading=11)),
            port,
            Paragraph(f.title, ParagraphStyle("ft", fontSize=8, leading=11)),
        ])

    t = Table(data, colWidths=[0.7 * cm, 2 * cm, 1.3 * cm, 3.5 * cm, 1.8 * cm, 8.2 * cm])
    t.setStyle(_table_style())
    story.append(t)
    story.append(PageBreak())
    return story


def _detailed_findings(findings: list[Finding], styles: dict) -> list:
    story = [Paragraph("Detailed Findings", styles["section_h1"])]

    for i, f in enumerate(findings, 1):
        sev_colour = SEVERITY_COLOUR.get(f.severity, BORDER)

        header_data = [[
            Paragraph(f"Finding {i:02d}", ParagraphStyle("fn", fontSize=9, textColor=WHITE, fontName="Helvetica-Bold")),
            Paragraph(f.severity, ParagraphStyle("fs", fontSize=9, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_RIGHT)),
        ]]
        header_t = Table(header_data, colWidths=[8 * cm, 9.5 * cm])
        header_t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), sev_colour),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))

        host_display = f.host_ip + (f" ({f.hostname})" if f.hostname else "")
        cvss_display = f"{f.cvss:.1f}" if f.cvss > 0 else "N/A"
        port_display = f"{f.port}/{f.protocol}" if f.port else "N/A"
        cve_display  = ", ".join(f.cve_refs) if f.cve_refs else "None"
        nis2_display = ", ".join(f.nis2_articles) if f.nis2_articles else "None"

        meta_data = [
            ["Title",    Paragraph(f.title, ParagraphStyle("mt", fontSize=9, fontName="Helvetica-Bold"))],
            ["Host",     host_display],
            ["Port",     port_display],
            ["CVSS",     cvss_display],
            ["CVE Refs", cve_display],
            ["NIS2",     nis2_display],
            ["Evidence", Paragraph(f.evidence, ParagraphStyle("ev", fontSize=8, fontName="Courier"))],
        ]
        meta_t = Table(meta_data, colWidths=[2.5 * cm, 15 * cm])
        meta_t.setStyle(TableStyle([
            ("FONTNAME",      (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, -1), 8),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 7),
            ("BACKGROUND",    (0, 0), (0, -1), LIGHT),
            ("GRID",          (0, 0), (-1, -1), 0.3, BORDER),
        ]))

        desc_t = Table(
            [["Description", Paragraph(f.description, ParagraphStyle("d", fontSize=8, leading=12))]],
            colWidths=[2.5 * cm, 15 * cm],
        )
        desc_t.setStyle(TableStyle([
            ("FONTNAME",      (0, 0), (0, 0), "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, -1), 8),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 7),
            ("BACKGROUND",    (0, 0), (0, 0), LIGHT),
            ("GRID",          (0, 0), (-1, -1), 0.3, BORDER),
        ]))

        rem_t = Table(
            [["Remediation", Paragraph(f.remediation, ParagraphStyle("r", fontSize=8, leading=12))]],
            colWidths=[2.5 * cm, 15 * cm],
        )
        rem_t.setStyle(TableStyle([
            ("FONTNAME",      (0, 0), (0, 0), "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, -1), 8),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 7),
            ("BACKGROUND",    (0, 0), (0, 0), colors.HexColor("#ecfdf5")),
            ("GRID",          (0, 0), (-1, -1), 0.3, BORDER),
        ]))

        story.append(KeepTogether([
            header_t,
            meta_t,
            desc_t,
            rem_t,
            Spacer(1, 0.5 * cm),
        ]))

    story.append(PageBreak())
    return story


def _nis2_section(compliance_map: dict, styles: dict) -> list:
    story = [Paragraph("NIS2 Compliance Mapping", styles["section_h1"])]
    story.append(Paragraph(
        "The table below maps identified findings to Directive (EU) 2022/2555 (NIS2) "
        "Article 21 cybersecurity risk-management controls.",
        styles["body"],
    ))
    story.append(Spacer(1, 0.3 * cm))

    data = [["Article", "Control Title", "Status", "Findings"]]
    for article, meta in sorted(compliance_map.items()):
        status = meta["status"]
        if status == "Non-Compliant":
            status_para = Paragraph(f'<b>{status}</b>', ParagraphStyle("nc", fontSize=8, textColor=CRITICAL))
        elif status == "Partially Compliant":
            status_para = Paragraph(f'<b>{status}</b>', ParagraphStyle("pc", fontSize=8, textColor=MEDIUM))
        else:
            status_para = Paragraph(status, ParagraphStyle("ok", fontSize=8, textColor=LOW))

        data.append([
            Paragraph(article, ParagraphStyle("art", fontSize=8, fontName="Helvetica-Bold")),
            Paragraph(meta["title"], ParagraphStyle("ct", fontSize=8, leading=11)),
            status_para,
            str(meta["findings_count"]) if meta["findings_count"] else "—",
        ])

    t = Table(data, colWidths=[3.5 * cm, 7.5 * cm, 4 * cm, 2.5 * cm])
    t.setStyle(_table_style())
    story.append(t)
    story.append(PageBreak())
    return story


def _appendix(findings: list[Finding], styles: dict) -> list:
    story = [Paragraph("Appendix: Remediation Priority List", styles["section_h1"])]
    story.append(Paragraph(
        "Prioritised remediation actions sorted by CVSS score. Address Critical and High "
        "findings first to achieve maximum risk reduction.",
        styles["body"],
    ))
    story.append(Spacer(1, 0.3 * cm))

    data = [["Priority", "Host", "Finding", "CVSS", "NIS2 Article"]]
    for i, f in enumerate(findings, 1):
        nis2 = f.nis2_articles[0] if f.nis2_articles else "—"
        data.append([
            str(i),
            f"{f.host_ip}" + (f"\n({f.hostname})" if f.hostname else ""),
            Paragraph(f.title, ParagraphStyle("rt", fontSize=8, leading=11)),
            f"{f.cvss:.1f}" if f.cvss > 0 else "—",
            nis2,
        ])

    t = Table(data, colWidths=[1.5 * cm, 3.5 * cm, 7.5 * cm, 1.5 * cm, 3.5 * cm])
    t.setStyle(_table_style())
    story.append(t)
    return story


# ── Main builder ──────────────────────────────────────────────────────────────
def build(
    hosts: list[dict],
    findings: list[Finding],
    compliance_map: dict,
    target: str,
    output_path: str = "",
) -> str:
    os.makedirs("reports", exist_ok=True)
    if not output_path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_target = target.replace("/", "_").replace(".", "-")
        output_path = os.path.join("reports", f"audit_{safe_target}_{ts}.pdf")

    date_str = datetime.now().strftime("%d %B %Y")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = _build_styles()

    def on_page(canvas, doc):
        _on_page(canvas, doc, target, date_str)

    story = []
    story += _cover_page(target, date_str, styles)
    story += _exec_summary(hosts, findings, styles)
    story += _host_inventory(hosts, styles)
    story += _findings_overview(findings, styles)
    story += _detailed_findings(findings, styles)
    story += _nis2_section(compliance_map, styles)
    story += _appendix(findings, styles)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"[+] PDF report saved: {output_path}")
    return output_path
