#!/usr/bin/env python3
"""
build_figures.py
================
Generates publication-quality visual diagrams, flowcharts, architectures,
and empirical figures for the Parliamentary AI Research Training Manuals.

Lead Facilitator: Eng. Dr. Kadeghe Fue, PhD (SUA / AB Consult)
Institution: College of Economics and Business Studies (COEBS),
             Sokoine University of Agriculture (SUA), Morogoro, Tanzania.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Official Colors of Tanzania and SUA
TZ_BLUE = "#0066B2"       # Tanzanian Blue
TZ_GOLD = "#FCD116"       # Tanzanian Yellow / Gold
TZ_GREEN = "#00703C"      # SUA / Tanzanian Green
TZ_DARK = "#232323"       # Dark Charcoal
TZ_LIGHT = "#F4F7FA"      # Clean Light Grey
TZ_RED = "#D9534F"        # Alert Red
TZ_BORDER = "#D0D7DE"     # Subtle Border Grey
TZ_BG_CARD = "#FFFFFF"    # Crisp Card Background

# Configure Matplotlib rcParams for publication standard
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.size": 9.5,
    "axes.labelsize": 10.5,
    "axes.titlesize": 12,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})


def add_tanzania_strip(ax, x=0.03, y=0.965, width=0.94, height=0.012):
    """Draws the official Tanzanian strip of Blue, Yellow, and Green."""
    h_sub = height / 3.0
    # Top: Blue
    ax.add_patch(patches.Rectangle((x, y + 2 * h_sub), width, h_sub,
                                   transform=ax.transAxes, color=TZ_BLUE, zorder=10))
    # Middle: Yellow
    ax.add_patch(patches.Rectangle((x, y + h_sub), width, h_sub,
                                   transform=ax.transAxes, color=TZ_GOLD, zorder=10))
    # Bottom: Green
    ax.add_patch(patches.Rectangle((x, y), width, h_sub,
                                   transform=ax.transAxes, color=TZ_GREEN, zorder=10))


def add_card(ax, xy, width, height, title="", subtitle="", body="",
             bg_color="#FFFFFF", border_color=TZ_BORDER, header_color=TZ_BLUE,
             badge_text=None, badge_color=TZ_BLUE, icon=None, fontsize_body=8.5):
    """Draws a professional card with rounded rectangle, header bar, and structured text."""
    x, y = xy
    # Rounded card background
    box = patches.FancyBboxPatch((x, y), width, height,
                                 boxstyle="round,pad=0.01,rounding_size=0.025",
                                 facecolor=bg_color, edgecolor=border_color,
                                 linewidth=1.2, zorder=2)
    ax.add_patch(box)

    # Accent top border strip
    accent = patches.FancyBboxPatch((x, y + height - 0.035), width, 0.035,
                                    boxstyle="round,pad=0.005,rounding_size=0.01",
                                    facecolor=header_color, edgecolor=header_color,
                                    zorder=3)
    ax.add_patch(accent)

    # Header text
    ty = y + height - 0.022
    if badge_text:
        # Badge
        badge_box = patches.FancyBboxPatch((x + 0.02, ty - 0.012), 0.08, 0.024,
                                           boxstyle="round,pad=0.002,rounding_size=0.006",
                                           facecolor=badge_color, edgecolor="none", zorder=4)
        ax.add_patch(badge_box)
        ax.text(x + 0.06, ty, badge_text, color="white", fontsize=8,
                fontweight="bold", ha="center", va="center", zorder=5)
        title_x = x + 0.11
    else:
        title_x = x + 0.03

    if title:
        ax.text(title_x, ty, title, color="white", fontsize=9.5,
                fontweight="bold", va="center", zorder=5)

    # Subtitle
    curr_y = y + height - 0.065
    if subtitle:
        ax.text(x + 0.03, curr_y, subtitle, color=TZ_DARK, fontsize=9,
                fontweight="bold", style="italic", va="top", zorder=4)
        curr_y -= 0.04

    # Body
    if body:
        ax.text(x + 0.03, curr_y, body, color="#333333", fontsize=fontsize_body,
                va="top", linespacing=1.35, zorder=4)


def generate_day1_auto_ingestion_arch(out_dir: Path):
    """Figure 1: End-to-End Automated Ingestion and AI-Driven Analysis Workflow."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Header title
    ax.text(0.5, 0.94, "The AB Consult Automated Ingestion Architecture",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Zero-Manual-Copy Pipeline: From Native Desk Files to Executive Parliamentary PDF",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    # 5 Stages
    stages = [
        {
            "num": "STAGE 1",
            "title": "Native File Drop",
            "sub": "Drag & Drop",
            "body": "- Drop .pdf & .docx\n- Native gazettes/bills\n- Confidential & local\n- No manual copy-paste",
            "color": TZ_BLUE,
        },
        {
            "num": "STAGE 2",
            "title": "Context Grounding",
            "sub": "File Tagging",
            "body": "- Use @filename.pdf\n- Precise file lock\n- Zero hallucination\n- Multi-doc context",
            "color": TZ_GREEN,
        },
        {
            "num": "STAGE 3",
            "title": "AI Scrutiny",
            "sub": "CLEAR Prompts",
            "body": "- Extract budget tables\n- Compare amendments\n- Reconcile CAG audits\n- Calculate variances",
            "color": TZ_BLUE,
        },
        {
            "num": "STAGE 4",
            "title": "Output Writing",
            "sub": "Markdown Dossier",
            "body": "- 4-column matrices\n- Empirical findings\n- Committee questions\n- Auto-saved to reports/",
            "color": TZ_GREEN,
        },
        {
            "num": "STAGE 5",
            "title": "1-Click PDF",
            "sub": "Executive Export",
            "body": "- VS Code Shortcut\n- Formatted headers\n- Speaker-ready layout\n- Archived with audit trail",
            "color": TZ_DARK,
        },
    ]

    x_start = 0.03
    w = 0.165
    gap = 0.026
    y = 0.10
    h = 0.72

    for i, s in enumerate(stages):
        cx = x_start + i * (w + gap)
        add_card(ax, (cx, y), w, h,
                 title=s["title"], subtitle=s["sub"], body=s["body"],
                 header_color=s["color"], badge_text=s["num"], badge_color=s["color"],
                 fontsize_body=8.5)

        # Arrow to next stage
        if i < len(stages) - 1:
            ax.annotate("", xy=(cx + w + gap - 0.005, y + h * 0.55),
                        xytext=(cx + w + 0.005, y + h * 0.55),
                        arrowprops=dict(arrowstyle="-|>", color=TZ_GOLD, lw=2.5,
                                        mutation_scale=15))

    p = out_dir / "fig_day1_auto_ingestion_arch.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_day1_workspace_tree(out_dir: Path):
    """Figure 2: Hierarchical Structure of the Standard Parliamentary Workspace in VS Code."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "Standard Parliamentary Research Workspace Layout",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "VS Code Workspace Architecture for Direct Ingestion & Reproducible Scrutiny",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    # Root Box
    root_box = patches.FancyBboxPatch((0.04, 0.70), 0.92, 0.13,
                                      boxstyle="round,pad=0.01,rounding_size=0.02",
                                      facecolor="#EAF2F8", edgecolor=TZ_BLUE, lw=1.5)
    ax.add_patch(root_box)
    ax.text(0.07, 0.77, "ROOT FOLDER: Parliamentary_Research_2026/",
            fontsize=11, fontweight="bold", color=TZ_BLUE, va="center")
    ax.text(0.07, 0.73, "Confidential Local Working Environment (Zero Cloud Leakage / Committee Privilege Intact)",
            fontsize=8.5, color=TZ_DARK, va="center")

    # Three Sub-Folders
    folders = [
        {
            "name": "documents/",
            "title": "Raw Ingestion Folder",
            "body": "[Source Input Files]\n- parent_act_2015.pdf\n- amendment_bill_2026.docx\n- cag_audit_report_2025.pdf\n- nbs_abstract_2025.pdf\n\nRule: Trainees never alter or re-type\nthese native files directly.",
            "color": TZ_BLUE,
            "x": 0.04,
        },
        {
            "name": "briefs_and_reports/",
            "title": "Analytical Deliverables",
            "body": "[AI-Compiled Deliverables]\n- Day1_Baseline_Brief.md\n- Day2_Legislative_Scrutiny.md\n- Day3_Evidence_Dossier.md\n- Compiled Official PDFs\n\nRule: Generated directly from AI\nstructured commands.",
            "color": TZ_GREEN,
            "x": 0.36,
        },
        {
            "name": "templates/",
            "title": "Parliamentary Skeletons",
            "body": "[Reusable Oversight Blueprints]\n- 4_column_clause_matrix.md\n- fydp3_alignment_brief.md\n- executive_callout_spec.md\n- cag_audit_variance_sheet.md\n\nRule: Enforces institutional rigor\nacross committee clerks.",
            "color": TZ_GOLD,
            "x": 0.68,
        },
    ]

    for f in folders:
        add_card(ax, (f["x"], 0.10), 0.28, 0.54,
                 title=f["name"], subtitle=f["title"], body=f["body"],
                 header_color=f["color"], badge_text="DIR", badge_color=f["color"],
                 fontsize_body=8.5)

    p = out_dir / "fig_day1_workspace_tree.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_day2_clear_framework(out_dir: Path):
    """Figure 3: The CLEAR Legislative Scrutiny Prompting Architecture."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "The CLEAR Legislative Scrutiny Prompting Protocol",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "5-Stage Role-Grounded Scrutiny Framework for Committee Bill Analysis",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    pillars = [
        {
            "letter": "C",
            "name": "Context & Role",
            "desc": "Institutional Persona",
            "text": "- Assign legal identity:\n  'Senior Parliamentary Counsel'\n- Define committee mandate\n- Anchor institutional stance",
            "color": TZ_BLUE,
        },
        {
            "letter": "L",
            "name": "Legislative Scope",
            "desc": "File Boundary Lock",
            "text": "- Tag exact source files:\n  @parent_act_2015.pdf\n  @amendment_bill.docx\n- Exclude extraneous text",
            "color": TZ_GREEN,
        },
        {
            "letter": "E",
            "name": "Evidence Constraint",
            "desc": "Zero Speculation",
            "text": "- Rely ONLY on supplied clauses\n- State 'Unchanged' if identical\n- Prevent fabricated legal citations\n- Flag ambiguities explicitly",
            "color": TZ_GOLD,
        },
        {
            "letter": "A",
            "name": "Action Architecture",
            "desc": "Output Matrix",
            "text": "- Dictate 4-column structure:\n  1. Clause Element\n  2. Existing Statute\n  3. Proposed Amendment\n  4. Committee Oversight Risk",
            "color": TZ_BLUE,
        },
        {
            "letter": "R",
            "name": "Restraint & Tone",
            "desc": "Neutral Oversight",
            "text": "- Enforce parliamentary neutrality\n- Eliminate partisan rhetoric\n- Focus on operational & fiscal risk\n- Concrete summons directives",
            "color": TZ_GREEN,
        },
    ]

    x_start = 0.03
    w = 0.166
    gap = 0.024
    y = 0.10
    h = 0.72

    for i, p in enumerate(pillars):
        cx = x_start + i * (w + gap)
        add_card(ax, (cx, y), w, h,
                 title=p["name"], subtitle=p["desc"], body=p["text"],
                 header_color=p["color"], badge_text=f"[{p['letter']}]",
                 badge_color=p["color"], fontsize_body=8.2)

    path = out_dir / "fig_day2_clear_framework.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"Generated: {path.name}")


def generate_day2_workspace(out_dir: Path):
    """Figure 4: Day 2 Document-Driven Directory Structure."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "Day 2 Ingestion Repository & Comparative Scrutiny Flow",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Dual-Document Ingestion: Linking Parent Acts, Bills & CAG Audits in VS Code",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    # Ingestion Card
    add_card(ax, (0.04, 0.12), 0.38, 0.70,
             title="documents/ (Input Corpus)",
             subtitle="Native Legislative & Audit Files",
             body="[1] parent_act_2015.pdf\n    - Gazetted Principal Act of Parliament\n    - Statutory mandates & penalty clauses\n\n[2] amendment_bill_2026.docx\n    - Native executive draft amending bill\n    - Proposed deletions and insertions\n\n[3] cag_audit_report_2025.pdf\n    - Controller & Auditor General audit\n    - Historical compliance infractions",
             header_color=TZ_BLUE, badge_text="INPUT", badge_color=TZ_BLUE)

    # Center arrow with AI process
    ax.annotate("", xy=(0.58, 0.47), xytext=(0.43, 0.47),
                arrowprops=dict(arrowstyle="-|>", color=TZ_GOLD, lw=3, mutation_scale=20))
    ax.text(0.505, 0.52, "CLEAR Protocol\nClause Reconciliation",
            ha="center", va="center", fontsize=8.5, fontweight="bold", color=TZ_DARK)

    # Output Card
    add_card(ax, (0.59, 0.12), 0.37, 0.70,
             title="briefs_and_reports/ (Deliverable)",
             subtitle="Day2_Legislative_Scrutiny_Brief",
             body="[Deliverable 2 Key Sections]\n\n1. Executive Summary & Fiduciary Risk\n2. 4-Column Statutory Scrutiny Matrix\n   - Identifies ministerial discretion risks\n   - Pinpoints unbudgeted fiscal outlays\n3. Empirical CAG Audit Cross-Check\n   - Historical leakage correlation\n4. Three (3) Actionable Questions (PQs)\n   - Targeted summons directives for MPs",
             header_color=TZ_GREEN, badge_text="OUTPUT", badge_color=TZ_GREEN)

    p = out_dir / "fig_day2_workspace.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_day3_evidence_hierarchy(out_dir: Path):
    """Figure 5: The 5-Tier Parliamentary Hierarchy of Statistical Credibility."""
    fig, ax = plt.subplots(figsize=(10.5, 5.0), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "The 5-Tier Parliamentary Hierarchy of Evidence",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Statutory and Empirical Weight Protocol for Legislative Scrutiny",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    tiers = [
        {
            "rank": "TIER 1",
            "weight": "DECISIVE LEGAL AUTHORITY",
            "title": "Statutory & Constitutional Enactments",
            "examples": "Acts of Parliament, National Gazettes, Hansard Official Records, Subsidiary Regulations",
            "color": TZ_BLUE,
            "y": 0.70,
        },
        {
            "rank": "TIER 2",
            "weight": "HIGHEST OVERSIGHT WEIGHT",
            "title": "Independent Constitutional Oversight Reports",
            "examples": "CAG Annual & Performance Audits, PPRA Procurement Audits, Law Reform Commission Reports",
            "color": TZ_GREEN,
            "y": 0.55,
        },
        {
            "rank": "TIER 3",
            "weight": "BENCHMARK EMPIRICAL DATA",
            "title": "Official National Statistical Repositories",
            "examples": "National Bureau of Statistics (NBS) Surveys, Population Census, Central Bank Economic Bulletins",
            "color": TZ_GOLD,
            "y": 0.40,
        },
        {
            "rank": "TIER 4",
            "weight": "SUBJECT TO ADVERSARIAL SCRUTINY",
            "title": "Executive Agency Self-Submissions",
            "examples": "Ministerial Budget Speeches, Sector Implementation Plans, Agency Annual Progress Books",
            "color": "#E67E22",
            "y": 0.25,
        },
        {
            "rank": "TIER 5",
            "weight": "CORROBORATIVE EVIDENCE ONLY",
            "title": "External Stakeholder Submissions",
            "examples": "Academic Research, Think Tank Policy Briefs, CSO Memoranda, Commercial Lobby Submissions",
            "color": "#7F8C8D",
            "y": 0.10,
        },
    ]

    for t in tiers:
        # Tier card
        y = t["y"]
        card = patches.FancyBboxPatch((0.05, y), 0.90, 0.125,
                                      boxstyle="round,pad=0.01,rounding_size=0.015",
                                      facecolor="#FFFFFF", edgecolor=t["color"], lw=1.3)
        ax.add_patch(card)

        # Left pill
        pill = patches.FancyBboxPatch((0.06, y + 0.02), 0.12, 0.085,
                                      boxstyle="round,pad=0.005,rounding_size=0.01",
                                      facecolor=t["color"], edgecolor="none")
        ax.add_patch(pill)
        ax.text(0.12, y + 0.062, t["rank"], color="white", fontsize=9,
                fontweight="bold", ha="center", va="center")

        # Titles
        ax.text(0.20, y + 0.085, t["title"], color=TZ_DARK, fontsize=10, fontweight="bold", va="center")
        ax.text(0.20, y + 0.040, f"Scope: {t['examples']}", color="#444444", fontsize=8.2, va="center")

        # Right badge
        ax.text(0.93, y + 0.062, t["weight"], color=t["color"], fontsize=8,
                fontweight="bold", ha="right", va="center")

    p = out_dir / "fig_day3_evidence_hierarchy.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_day3_policy_architecture(out_dir: Path):
    """Figure 6: The 4-Tier Structural Architecture of an Executive Policy Brief."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "The 4-Tier Parliamentary Briefing Architecture",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Structural Format for Evidence-Backed Policy Briefs in Legislative Chambers",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    tiers = [
        {
            "num": "TIER I",
            "name": "Executive Callout",
            "sub": "The Decision Anchor",
            "body": "- Length: <= 150 words\n- Core fiduciary finding\n- Urgent committee summons\n- Zero bureaucratic fluff\n- Framed for Speaker/Chairs",
            "color": TZ_BLUE,
        },
        {
            "num": "TIER II",
            "name": "Strategic Context",
            "sub": "Policy Alignment",
            "body": "- Statutory parent act\n- FYDP III 5-year targets\n- Tanzania Vision 2025/50\n- Target regional beneficiaries\n- Governance objectives",
            "color": TZ_GREEN,
        },
        {
            "num": "TIER III",
            "name": "Empirical Tables",
            "sub": "Data Cross-Tabulation",
            "body": "- Clean Markdown tables\n- Budget target vs. Actual\n- CAG audited discrepancy\n- NBS field service metrics\n- Regional ranking index",
            "color": TZ_GOLD,
        },
        {
            "num": "TIER IV",
            "name": "Policy Options",
            "sub": "Actionable Directives",
            "body": "- 3 Legislative Options\n- Fiscal & legal trade-offs\n- Concrete amendments\n- Three (3) targeted PQs\n- Next committee action",
            "color": TZ_DARK,
        },
    ]

    x_start = 0.04
    w = 0.208
    gap = 0.028
    y = 0.10
    h = 0.72

    for i, t in enumerate(tiers):
        cx = x_start + i * (w + gap)
        add_card(ax, (cx, y), w, h,
                 title=t["name"], subtitle=t["sub"], body=t["body"],
                 header_color=t["color"], badge_text=t["num"], badge_color=t["color"],
                 fontsize_body=8.5)

    p = out_dir / "fig_day3_policy_architecture.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_day3_workspace(out_dir: Path):
    """Figure 7: Day 3 Document-Driven Directory Structure."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "Day 3 Statistical Ingestion & Cross-Tabulation Flow",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Direct Ingestion of Statistical Abstracts & Ministerial Budget Books in VS Code",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    # Ingestion Card
    add_card(ax, (0.04, 0.12), 0.38, 0.70,
             title="documents/ (Input Data)",
             subtitle="Statistical & Financial Gazettes",
             body="[1] statistical_abstract_2025.pdf\n    - NBS Official Statistics\n    - Regional water access, health clinics,\n      and agricultural output data\n\n[2] ministerial_budget_performance.pdf\n    - Ministry self-reported expenditures\n    - Treasury allocations vs disbursement",
             header_color=TZ_BLUE, badge_text="INPUT", badge_color=TZ_BLUE)

    # Center arrow
    ax.annotate("", xy=(0.58, 0.47), xytext=(0.43, 0.47),
                arrowprops=dict(arrowstyle="-|>", color=TZ_GOLD, lw=3, mutation_scale=20))
    ax.text(0.505, 0.52, "Direct AI Ingestion\nVariance Extraction",
            ha="center", va="center", fontsize=8.5, fontweight="bold", color=TZ_DARK)

    # Output Card
    add_card(ax, (0.59, 0.12), 0.37, 0.70,
             title="briefs_and_reports/ (Dossier)",
             subtitle="Day3_Sector_Evidence_Dossier",
             body="[Deliverable 3 Output Highlights]\n\n1. Executive Callout (< 150 words)\n2. Sector Funding Discrepancy Matrix\n   - Identifies TZS 14.8B unspent capital\n   - Correlates with 42% completion lag\n3. Regional Disparity Ranking Index\n4. Dual-Pane Verified Citation Log",
             header_color=TZ_GREEN, badge_text="OUTPUT", badge_color=TZ_GREEN)

    p = out_dir / "fig_day3_workspace.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_day3_fact_checking_panes(out_dir: Path):
    """Figure 8: VS Code Dual-Pane Fact-Checking Interface."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "VS Code Dual-Pane Fact-Checking Configuration",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Adversarial Verification Workspace: Side-by-Side Source Audit in Parliamentary Research",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    # Left Pane (Source PDF)
    add_card(ax, (0.04, 0.10), 0.33, 0.72,
             title="LEFT PANE: Source PDF",
             subtitle="@statistical_abstract.pdf",
             body="[Native Evidence Source Document]\n\nTable 4.12: Rural Water Coverage\n- Dodoma Region: 61.4%\n- Morogoro Region: 68.2%\n- Shinyanga Region: 52.8%\n\nFootnote 3: Excludes seasonal boreholes\ndecommissioned before FY24.",
             header_color=TZ_BLUE, badge_text="EVIDENCE", badge_color=TZ_BLUE)

    # Right Pane (Draft Brief)
    add_card(ax, (0.39, 0.10), 0.33, 0.72,
             title="RIGHT PANE: Draft Brief",
             subtitle="Day3_Sector_Evidence_Dossier.md",
             body="[Parliamentary Brief Draft]\n\n| Region | NBS Metric | Ministry Claim |\n| Dodoma | 61.4% | 84.0%* |\n| Morogoro| 68.2% | 79.5% |\n\n*Critical Discrepancy Note:\nMinistry overstated coverage by 22.6%\nthrough unverified borehole counts.",
             header_color=TZ_GREEN, badge_text="DRAFT", badge_color=TZ_GREEN)

    # Far Right (AI Assistant Sidebar)
    add_card(ax, (0.74, 0.10), 0.22, 0.72,
             title="AI AUDITOR",
             subtitle="VS Code Sidebar",
             body="[Prompt Command]\n'Cross-check Table\n4.12 footnote 3 against\nMinistry claims. Flag\nunsupported variances.'\n\nResult:\n'Discrepancy confirmed\nin Table 4.12; 22.6%\ninflation verified.'",
             header_color=TZ_GOLD, badge_text="AI", badge_color=TZ_GOLD,
             fontsize_body=8.0)

    p = out_dir / "fig_day3_fact_checking_panes.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_day4_analytical_transition(out_dir: Path):
    """Figure 9: Transforming Executive Advocacy into Disciplined Parliamentary Options Scrutiny."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "The Parliamentary Analytical Transition",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Transforming Executive Single-Choice Advocacy into Rigorous Multi-Option Scrutiny",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    # Left: Executive Advocacy
    add_card(ax, (0.04, 0.10), 0.42, 0.72,
             title="TRADITIONAL EXECUTIVE ADVOCACY",
             subtitle="Single-Solution Executive Stance",
             body="'We strongly recommend Option A because it directly solves\nthe sector challenge.'\n\n[Typical Pitfalls for Oversight]\n- Suppresses alternative policy designs\n- Obscures long-term recurrent fiscal liabilities\n- Downplays LGA administrative implementation bottlenecks\n- Assumes 100% compliance without risk contingency",
             header_color=TZ_RED, badge_text="ADVOCACY", badge_color=TZ_RED)

    # Middle Arrow
    ax.annotate("", xy=(0.54, 0.46), xytext=(0.47, 0.46),
                arrowprops=dict(arrowstyle="-|>", color=TZ_GOLD, lw=3, mutation_scale=20))
    ax.text(0.505, 0.52, "Parliamentary\nScrutiny Shift",
            ha="center", va="center", fontsize=8.5, fontweight="bold", color=TZ_DARK)

    # Right: Parliamentary Scrutiny
    add_card(ax, (0.55, 0.10), 0.41, 0.72,
             title="PARLIAMENTARY OPTIONS SCRUTINY",
             subtitle="Multi-Criteria Trade-off Evaluation",
             body="- Option A (Capital Subsidy):\n  Rapid impact but High Treasury Burden & Leakage Risk.\n- Option B (LGA Decentralized Grants):\n  Moderate Fiscal Outlay but Demands Council Capacity.\n- Option C (Regulatory Tariff Reform):\n  Minimal Treasury Burden but Demands Primary Act Amendment.\n\nResult: Empowers Committee to debate genuine policy trade-offs.",
             header_color=TZ_GREEN, badge_text="SCRUTINY", badge_color=TZ_GREEN)

    p = out_dir / "fig_day4_analytical_transition.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_day4_mcpa_pillars(out_dir: Path):
    """Figure 10: The 4 Pillars of Parliamentary Multi-Criteria Policy Analysis (MCPA)."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "The 4 Pillars of Parliamentary Multi-Criteria Policy Analysis",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Comprehensive Analytical Framework for Committee Legislative & Policy Review",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    pillars = [
        {
            "num": "PILLAR 1",
            "name": "Fiscal & Budgetary",
            "sub": "Treasury Viability",
            "body": "- Direct Consolidated Fund burden\n- Multi-year recurrent costs\n- Deficit & debt ceiling impact\n- Revenue leakage & tax risks\n- Contingent state liabilities",
            "color": TZ_BLUE,
        },
        {
            "num": "PILLAR 2",
            "name": "Administrative",
            "sub": "Implementation Capacity",
            "body": "- LGA staffing & competence\n- Inter-ministerial coordination\n- Digital infrastructure readiness\n- Procurement timeline feasibility\n- Compliance monitoring load",
            "color": TZ_GREEN,
        },
        {
            "num": "PILLAR 3",
            "name": "Socio-Economic",
            "sub": "Equity & Distribution",
            "body": "- Smallholder income protection\n- Regional & gender equality\n- Household service tariffs\n- Private investment crowding\n- Environmental sustainability",
            "color": TZ_GOLD,
        },
        {
            "num": "PILLAR 4",
            "name": "Statutory Alignment",
            "sub": "Constitutional Compliance",
            "body": "- Alignment with Parent Acts\n- Subordinate regulation limits\n- Constitutional fundamental rights\n- EAC & SADC treaty conformity\n- Judicial review vulnerabilities",
            "color": TZ_DARK,
        },
    ]

    x_start = 0.04
    w = 0.208
    gap = 0.028
    y = 0.10
    h = 0.72

    for i, p in enumerate(pillars):
        cx = x_start + i * (w + gap)
        add_card(ax, (cx, y), w, h,
                 title=p["name"], subtitle=p["sub"], body=p["body"],
                 header_color=p["color"], badge_text=p["num"], badge_color=p["color"],
                 fontsize_body=8.5)

    path = out_dir / "fig_day4_mcpa_pillars.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"Generated: {path.name}")


def generate_day4_workspace(out_dir: Path):
    """Figure 11: Day 4 Document-Driven Directory Structure."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "Day 4 Document-Driven Strategic Policy Repository",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Direct Ingestion of Sector White Papers and Strategic Blueprints in VS Code",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    add_card(ax, (0.04, 0.12), 0.38, 0.70,
             title="documents/ (Input Strategy)",
             subtitle="Native White Papers & Plans",
             body="[1] policy_whitepaper_2025.pdf\n    - Strategic ministerial white paper\n    - Subsidized input distribution targets\n\n[2] sector_strategic_plan.docx\n    - 5-year ministerial operational strategy\n    - LGA capital deployment schedule",
             header_color=TZ_BLUE, badge_text="INPUT", badge_color=TZ_BLUE)

    ax.annotate("", xy=(0.58, 0.47), xytext=(0.43, 0.47),
                arrowprops=dict(arrowstyle="-|>", color=TZ_GOLD, lw=3, mutation_scale=20))
    ax.text(0.505, 0.52, "4-Pillar MCPA\nOptions Scrutiny",
            ha="center", va="center", fontsize=8.5, fontweight="bold", color=TZ_DARK)

    add_card(ax, (0.59, 0.12), 0.37, 0.70,
             title="briefs_and_reports/ (Options)",
             subtitle="Day4_Strategic_Policy_Options",
             body="[Deliverable 4 Outputs]\n\n1. Executive Summary & Policy Anchors\n2. 4-Pillar Multi-Criteria Analysis Matrix\n3. 4-Way Adversarial Stakeholder Profiles\n4. 3 Evidence-Backed Legislative Options\n5. Three (3) Targeted Ministerial Questions",
             header_color=TZ_GREEN, badge_text="OUTPUT", badge_color=TZ_GREEN)

    p = out_dir / "fig_day4_workspace.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_day4_stakeholder_simulation(out_dir: Path):
    """Figure 12: The 4-Way Adversarial Stakeholder Simulation Architecture."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "The 4-Way Adversarial Stakeholder Simulation Architecture",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Stress-Testing Policy Proposals Against Conflicting Institutional Priorities",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    actors = [
        {
            "num": "ACTOR 1",
            "name": "Ministry of Finance",
            "sub": "Fiscal Ceiling Guardian",
            "body": "- Focus: Cash ceiling limits\n- Debt-to-GDP sustainability\n- Rejects open-ended subsidies\n- Demands cost-recovery tariffs",
            "color": TZ_BLUE,
        },
        {
            "num": "ACTOR 2",
            "name": "LGAs / Councils",
            "sub": "Operational Implementer",
            "body": "- Focus: Field staff deficits\n- Enforcement capacity lag\n- Protects own-source revenues\n- Cautions against unfunded mandates",
            "color": TZ_GREEN,
        },
        {
            "num": "ACTOR 3",
            "name": "Private Investors",
            "sub": "Commercial Capital",
            "body": "- Focus: Tariff predictability\n- Contract enforcement reliability\n- Fair competition safeguards\n- Foreign exchange repatriation",
            "color": TZ_GOLD,
        },
        {
            "num": "ACTOR 4",
            "name": "Citizens & Farmers",
            "sub": "Public Beneficiaries",
            "body": "- Focus: Household affordability\n- Transparent service delivery\n- Universal rural access\n- Relief from predatory pricing",
            "color": TZ_DARK,
        },
    ]

    x_start = 0.04
    w = 0.208
    gap = 0.028
    y = 0.10
    h = 0.72

    for i, a in enumerate(actors):
        cx = x_start + i * (w + gap)
        add_card(ax, (cx, y), w, h,
                 title=a["name"], subtitle=a["sub"], body=a["body"],
                 header_color=a["color"], badge_text=a["num"], badge_color=a["color"],
                 fontsize_body=8.5)

    p = out_dir / "fig_day4_stakeholder_simulation.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_day5_ethical_pillars(out_dir: Path):
    """Figure 13: The 4 Ethical Pillars of Parliamentary AI Research."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "The 4 Ethical Pillars of Artificial Intelligence in Parliamentary Research",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Standards of Integrity, Democratic Accountability, and Institutional Rigor",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    pillars = [
        {
            "num": "PILLAR 1",
            "name": "Confidentiality",
            "sub": "Parliamentary Privilege",
            "body": "- Zero data-leakage policy\n- Offline & local model protocols\n- Un-tabled bills remain secret\n- In-camera evidence protection",
            "color": TZ_BLUE,
        },
        {
            "num": "PILLAR 2",
            "name": "Verification",
            "sub": "Zero Hallucination",
            "body": "- Mandatory statutory lookup\n- Every section cross-verified\n- Primary Act date validation\n- Footnote and gazette checks",
            "color": TZ_GREEN,
        },
        {
            "num": "PILLAR 3",
            "name": "Neutrality",
            "sub": "Non-Partisan Stance",
            "body": "- Objective framing of options\n- Zero partisan rhetoric/bias\n- Focus on empirical evidence\n- Equal scrutiny of all policies",
            "color": TZ_GOLD,
        },
        {
            "num": "PILLAR 4",
            "name": "Transparency",
            "sub": "Disclosure Standards",
            "body": "- Standard AI methodology notice\n- Clear indexing declaration\n- Human verification sign-off\n- Transparent audit trail",
            "color": TZ_DARK,
        },
    ]

    x_start = 0.04
    w = 0.208
    gap = 0.028
    y = 0.10
    h = 0.72

    for i, p in enumerate(pillars):
        cx = x_start + i * (w + gap)
        add_card(ax, (cx, y), w, h,
                 title=p["name"], subtitle=p["sub"], body=p["body"],
                 header_color=p["color"], badge_text=p["num"], badge_color=p["color"],
                 fontsize_body=8.5)

    path = out_dir / "fig_day5_ethical_pillars.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"Generated: {path.name}")


def generate_day5_workspace(out_dir: Path):
    """Figure 14: Day 5 Multi-Document Corpus Workspace Layout."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "Day 5 Multi-Document Corpus Ingestion Repository",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Comprehensive Triangulation: Reconciling Budget, Audit & Field Survey Data",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    add_card(ax, (0.04, 0.12), 0.38, 0.70,
             title="documents/corpus/ (Inputs)",
             subtitle="Tripartite Evidence Corpus",
             body="[1] DocA_Ministerial_Budget_2025.pdf\n    - Executive expenditure claims\n\n[2] DocB_CAG_Audit_Report_2025.pdf\n    - Independent oversight audit\n    - Fiduciary queries & compliance leaks\n\n[3] DocC_NBS_Survey_Report_2025.pdf\n    - Empirical citizen household survey",
             header_color=TZ_BLUE, badge_text="CORPUS", badge_color=TZ_BLUE)

    ax.annotate("", xy=(0.58, 0.47), xytext=(0.43, 0.47),
                arrowprops=dict(arrowstyle="-|>", color=TZ_GOLD, lw=3, mutation_scale=20))
    ax.text(0.505, 0.52, "Tripartite AI\nSynthesis",
            ha="center", va="center", fontsize=8.5, fontweight="bold", color=TZ_DARK)

    add_card(ax, (0.59, 0.12), 0.37, 0.70,
             title="briefs_and_reports/ (Outputs)",
             subtitle="Three Targeted Deliverables",
             body="[Deliverable 5A] Executive Report (1-2 pp)\n    - For Speaker & Committee Chairs\n\n[Deliverable 5B] Policy Brief (2-3 pp)\n    - For Floor Debate by MPs\n\n[Deliverable 5C] Scientific Dossier (6-10 pp)\n    - Full empirical & econometric tables\n    - Institutional archive record",
             header_color=TZ_GREEN, badge_text="REPORTS", badge_color=TZ_GREEN)

    p = out_dir / "fig_day5_workspace.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_day5_tripartite_architecture(out_dir: Path):
    """Figure 15: The Tripartite Parliamentary Research Architecture."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "The Tripartite Parliamentary Output Architecture",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "Transforming a Single Evidentiary Corpus into Three Distinct Institutional Deliverables",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    deliverables = [
        {
            "num": "OUTPUT 1",
            "name": "Executive Report",
            "target": "Speaker & Chairs",
            "pages": "1 -- 2 Pages",
            "body": "- Focus: Urgent Fiduciary Risk\n- Core variance summaries\n- Immediate legal non-compliance\n- Formal committee summons directives\n- Maximum brevity for rapid leadership decisions",
            "color": TZ_BLUE,
        },
        {
            "num": "OUTPUT 2",
            "name": "Policy Brief",
            "target": "Floor MPs & Debaters",
            "pages": "2 -- 3 Pages",
            "body": "- Focus: Plenary Floor Debate\n- 120-word executive callout anchor\n- Regional performance contrast tables\n- Concrete constituency impact statistics\n- Three (3) evidence-backed Questions (PQs)",
            "color": TZ_GREEN,
        },
        {
            "num": "OUTPUT 3",
            "name": "Scientific Report",
            "target": "Clerks & Researchers",
            "pages": "6 -- 10 Pages",
            "body": "- Focus: Institutional Evidence Archive\n- Exhaustive methodology disclosure\n- Primary statutory & gazette citations\n- Complete econometric regression tables\n- Audited CAG variance appendices",
            "color": TZ_DARK,
        },
    ]

    x_start = 0.04
    w = 0.28
    gap = 0.04
    y = 0.10
    h = 0.72

    for i, d in enumerate(deliverables):
        cx = x_start + i * (w + gap)
        add_card(ax, (cx, y), w, h,
                 title=d["name"], subtitle=f"Target: {d['target']} ({d['pages']})",
                 body=d["body"], header_color=d["color"],
                 badge_text=d["num"], badge_color=d["color"], fontsize_body=8.5)

    p = out_dir / "fig_day5_tripartite_architecture.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_master_auto_ingestion_arch(out_dir: Path):
    """Figure 16: Master Ingestion & Analytical Workflow."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.94, "Master Parliamentary AI Direct Ingestion Architecture",
            ha="center", va="center", fontsize=13, fontweight="bold", color=TZ_DARK)
    ax.text(0.5, 0.895, "5-Stage Unified Curriculum: Direct Ingestion, Dual-Pane Verification, and Tripartite Reporting",
            ha="center", va="center", fontsize=9.5, color=TZ_BLUE, style="italic")
    add_tanzania_strip(ax, 0.04, 0.865, 0.92, 0.010)

    stages = [
        {"num": "DAY 1", "title": "VS Code Desk", "sub": "Native Ingestion", "body": "- Setup workspace\n- Drop Word & PDF\n- Zero copy-paste\n- Export PDF", "color": TZ_BLUE},
        {"num": "DAY 2", "title": "Bill Scrutiny", "sub": "CLEAR Prompts", "body": "- Parent Act vs Bill\n- CAG audit queries\n- 4-column matrix\n- Draft 3 PQs", "color": TZ_GREEN},
        {"num": "DAY 3", "title": "Evidence Lab", "sub": "Statistical NBS", "body": "- Budget vs Actual\n- Discrepancy tables\n- Split fact-check\n- Sector dossier", "color": TZ_GOLD},
        {"num": "DAY 4", "title": "Policy Options", "sub": "MCPA 4 Pillars", "body": "- Strategy white paper\n- 4-way simulation\n- Options matrix\n- Trade-off review", "color": TZ_BLUE},
        {"num": "DAY 5", "title": "Ethics & Tripartite", "sub": "Full Synthesis", "body": "- 3-doc corpus\n- Executive brief\n- Policy brief (MPs)\n- Archive dossier", "color": TZ_DARK},
    ]

    x_start = 0.03
    w = 0.165
    gap = 0.026
    y = 0.10
    h = 0.72

    for i, s in enumerate(stages):
        cx = x_start + i * (w + gap)
        add_card(ax, (cx, y), w, h,
                 title=s["title"], subtitle=s["sub"], body=s["body"],
                 header_color=s["color"], badge_text=s["num"], badge_color=s["color"],
                 fontsize_body=8.5)
        if i < len(stages) - 1:
            ax.annotate("", xy=(cx + w + gap - 0.005, y + h * 0.55),
                        xytext=(cx + w + 0.005, y + h * 0.55),
                        arrowprops=dict(arrowstyle="-|>", color=TZ_GOLD, lw=2.5, mutation_scale=15))

    p = out_dir / "fig_master_auto_ingestion_arch.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def generate_empirical_budget_variance(out_dir: Path):
    """Bonus Figure: Empirical Budget Discrepancy & Service Delivery Variance Across Tanzanian Regions."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.6), dpi=300)

    regions = ["Dodoma", "Morogoro", "Mwanza", "Arusha", "Mbeya", "Tanga", "Kagera", "Kigoma"]
    budget_alloc = np.array([45.2, 38.6, 52.1, 41.0, 36.4, 33.8, 29.5, 31.2]) # Billion TZS
    cag_audited  = np.array([32.4, 36.8, 38.5, 39.2, 28.1, 26.5, 21.0, 19.8]) # Billion TZS
    variance = budget_alloc - cag_audited

    x = np.arange(len(regions))
    width = 0.38

    ax1.bar(x - width/2, budget_alloc, width, label="Ministerial Claim (Budget)", color=TZ_BLUE, alpha=0.88)
    ax1.bar(x + width/2, cag_audited, width, label="CAG Audited Expenditure", color=TZ_GREEN, alpha=0.88)
    ax1.set_ylabel("Expenditure (Billion TZS)", fontweight="bold")
    ax1.set_title("A. Ministerial Allocation vs. CAG Audited Actuals", fontweight="bold", fontsize=10.5)
    ax1.set_xticks(x)
    ax1.set_xticklabels(regions, rotation=35, ha="right", fontsize=8.5)
    ax1.legend(loc="upper left", frameon=True, facecolor="white", fontsize=8)
    ax1.grid(True, linestyle="--", alpha=0.5, axis="y")

    # Panel B: Variance & Delivery lag
    colors = [TZ_RED if v > 8.0 else TZ_GOLD if v > 4.0 else TZ_GREEN for v in variance]
    ax2.barh(regions, variance, color=colors, alpha=0.85, edgecolor=TZ_DARK, lw=0.8)
    ax2.set_xlabel("Unaccounted / Unspent Discrepancy (Billion TZS)", fontweight="bold")
    ax2.set_title("B. Audit Discrepancy Flagged for Committee Action", fontweight="bold", fontsize=10.5)
    ax2.grid(True, linestyle="--", alpha=0.5, axis="x")

    for i, v in enumerate(variance):
        ax2.text(v + 0.3, i, f"+{v:.1f}B", va="center", fontsize=8, fontweight="bold", color=TZ_DARK)

    plt.tight_layout()
    p = out_dir / "fig_empirical_budget_variance.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"Generated: {p.name}")


def build_all_figures(output_dir: str | Path = "figures"):
    """Generates all figures and saves them into the specified output directory."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n========================================================")
    print(f"Generating Publication-Ready Figures in: {out_dir.resolve()}")
    print(f"========================================================")

    generate_day1_auto_ingestion_arch(out_dir)
    generate_day1_workspace_tree(out_dir)
    generate_day2_clear_framework(out_dir)
    generate_day2_workspace(out_dir)
    generate_day3_evidence_hierarchy(out_dir)
    generate_day3_policy_architecture(out_dir)
    generate_day3_workspace(out_dir)
    generate_day3_fact_checking_panes(out_dir)
    generate_day4_analytical_transition(out_dir)
    generate_day4_mcpa_pillars(out_dir)
    generate_day4_workspace(out_dir)
    generate_day4_stakeholder_simulation(out_dir)
    generate_day5_ethical_pillars(out_dir)
    generate_day5_workspace(out_dir)
    generate_day5_tripartite_architecture(out_dir)
    generate_master_auto_ingestion_arch(out_dir)
    generate_empirical_budget_variance(out_dir)

    print(f"\nSuccessfully generated 17 publication-grade figures in {out_dir}!\n")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "figures"
    build_all_figures(target)
