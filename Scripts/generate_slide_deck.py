#!/usr/bin/env python3
"""
generate_slide_deck.py
======================
Generates high-quality, executive-grade 16:9 presentation slide decks as PDFs
for the Parliamentary AI Research Training Program and stores them in:
  Training_Materials/Training_Presentations/

Features:
- Official Tanzanian Government & Sokoine University of Agriculture (SUA) Branding
- Touching-close National Color Strips (Tanzanian Blue, Gold/Yellow, SUA Green)
- Official SUA Crest & Tanzanian Coat of Arms in running header
- Guaranteed Layout Containment (zero text running out of boxes)
- High-Resolution Figure Integration from build_figures.py
- Clean LaTeX typography with zero Markdown asterisks or hashes
- Dual-pass LuaLaTeX compilation for accurate slide numbering

Decks Generated:
1. executive_overview_presentation.pdf      (5-Day Executive Curriculum Synopsis)
2. day_1_presentation.pdf                   (Native File Ingestion & VS Code Desk)
3. day_2_presentation.pdf                   (Statutory Scrutiny & CAG Audit Ingestion)
4. day_3_presentation.pdf                   (Statistical NBS Data & Evidence Lab)
5. day_4_presentation.pdf                   (MCPA Framework & Stakeholder Simulation)
6. day_5_presentation.pdf                   (Ethical AI Guardrails & Tripartite Reporting)
7. master_parliamentary_ai_presentation.pdf (Comprehensive 5-Day Master Curriculum Deck)

Lead Facilitator: Eng. Dr. Kadeghe Fue, PhD (SUA / AB Consult)
Institution: College of Economics and Business Studies (COEBS),
             Sokoine University of Agriculture (SUA), Morogoro, Tanzania.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "Scripts"
LOGO_DIR = REPO_ROOT / "Logo"
FIGURES_DIR = REPO_ROOT / "Training_Materials" / "figures"
OUTPUT_DIR = REPO_ROOT / "Training_Materials" / "Training_Presentations"


def get_lualatex_cmd() -> str:
    """Finds the path to lualatex executable."""
    texbin = Path("/Library/TeX/texbin/lualatex")
    if texbin.exists():
        return str(texbin)
    found = shutil.which("lualatex")
    if found:
        return found
    raise FileNotFoundError("lualatex executable not found on system.")


def ensure_symlinks():
    """Ensures Logo and figures are accessible from OUTPUT_DIR."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logo_link = OUTPUT_DIR / "Logo"
    if not logo_link.exists():
        logo_link.symlink_to(Path("../../Logo"), target_is_directory=True)
    figs_link = OUTPUT_DIR / "figures"
    if not figs_link.exists():
        figs_link.symlink_to(Path("../figures"), target_is_directory=True)


def get_beamer_preamble(short_title: str) -> str:
    """Returns the standardized official Beamer LaTeX preamble."""
    return rf"""\documentclass[aspectratio=169, 10pt]{{beamer}}
\usepackage{{fontspec}}
\usepackage[english]{{babel}}
\babelfont{{rm}}{{Noto Sans}}
\usepackage{{xcolor}}
\usepackage{{graphicx}}
\usepackage{{tabularx}}
\usepackage{{booktabs}}
\usepackage{{tcolorbox}}
\tcbuselibrary{{skins,breakable}}

% Official Colors of Tanzania & SUA
\definecolor{{tanzaniablue}}{{RGB}}{{0, 102, 178}}
\definecolor{{tanzaniayellow}}{{RGB}}{{252, 209, 22}}
\definecolor{{suagreen}}{{RGB}}{{0, 112, 60}}
\definecolor{{darkcharcoal}}{{RGB}}{{30, 41, 59}}
\definecolor{{lightgrey}}{{RGB}}{{248, 250, 252}}
\definecolor{{cardborder}}{{RGB}}{{203, 213, 225}}
\definecolor{{calloutbg}}{{RGB}}{{241, 245, 249}}

% Beamer Theme Settings
\setbeamertemplate{{navigation symbols}}{{}}
\setbeamersize{{text margin left=0.6cm, text margin right=0.6cm}}

% Native Beamer Title Styling
\setbeamercolor{{frametitle}}{{fg=tanzaniablue}}
\setbeamercolor{{framesubtitle}}{{fg=suagreen}}
\setbeamerfont{{frametitle}}{{size=\Large,series=\bfseries}}
\setbeamerfont{{framesubtitle}}{{size=\footnotesize,series=\bfseries}}

% Official Touching-Close Strips Macro
\newcommand{{\tzstrip}}[1][\paperwidth]{{%
  \parbox[t]{{#1}}{{%
    \setlength{{\parskip}}{{0pt}}\setlength{{\lineskip}}{{0pt}}\setlength{{\baselineskip}}{{0pt}}%
    {{\color{{tanzaniablue}}\rule{{#1}}{{2.0pt}}}}\par\vspace{{-0.2pt}}%
    {{\color{{tanzaniayellow}}\rule{{#1}}{{1.4pt}}}}\par\vspace{{-0.2pt}}%
    {{\color{{suagreen}}\rule{{#1}}{{2.0pt}}}}\par%
  }}%
}}

% Official Running Header
\setbeamertemplate{{headline}}{{%
  \leavevmode%
  \begin{{beamercolorbox}}[wd=\paperwidth,ht=0.98cm,dp=0.20cm]{{white}}%
    \vskip2pt%
    \hskip0.03\paperwidth%
    \parbox[c]{{0.10\paperwidth}}{{\includegraphics[height=0.62cm,keepaspectratio]{{Logo/SUA.png}}}}%
    \hfill%
    \parbox[c]{{0.72\paperwidth}}{{\centering%
      {{\fontsize{{7pt}}{{8pt}}\selectfont\textbf{{\textcolor{{darkcharcoal}}{{THE UNITED REPUBLIC OF TANZANIA \textbullet\ SOKOINE UNIVERSITY OF AGRICULTURE}}}}}}\par\vspace{{2pt}}%
      {{\fontsize{{5.5pt}}{{6.5pt}}\selectfont\textbf{{\textcolor{{suagreen}}{{{short_title} \textbar\ AB CONSULT}}}}}}%
    }}%
    \hfill%
    \parbox[c]{{0.10\paperwidth}}{{\raggedleft\includegraphics[height=0.62cm,keepaspectratio]{{Logo/Coat_of_arms_of_Tanzania.png}}}}%
    \hskip0.03\paperwidth%
    \par\vspace{{2pt}}%
    \tzstrip[\paperwidth]%
  \end{{beamercolorbox}}%
}}

% Official Running Footer
\setbeamertemplate{{footline}}{{%
  \leavevmode%
  \tzstrip[\paperwidth]%
  \begin{{beamercolorbox}}[wd=\paperwidth,ht=0.40cm,dp=0pt]{{white}}%
    \vskip2pt%
    \hskip0.03\paperwidth%
    \parbox[c]{{0.68\paperwidth}}{{%
      {{\fontsize{{5.8pt}}{{6.8pt}}\selectfont\textcolor{{darkcharcoal}}{{\textbf{{Lead Facilitator:}} Eng. Dr. Kadeghe Fue, PhD (SUA) \textbar\ National Assembly of Tanzania}}}}%
    }}%
    \hfill%
    \parbox[c]{{0.22\paperwidth}}{{\raggedleft%
      {{\fontsize{{5.8pt}}{{6.8pt}}\selectfont\textcolor{{darkcharcoal}}{{\textbf{{Slide \insertframenumber{{}} / \inserttotalframenumber}}}}}}%
    }}%
    \hskip0.03\paperwidth%
    \vskip2pt%
  \end{{beamercolorbox}}%
}}
"""


def sanitize_slide_tex(content: str) -> str:
    """Escapes literal & characters that are not part of table alignment."""
    lines = content.split("\n")
    in_tabular = False
    cleaned_lines = []
    for line in lines:
        if r"\begin{tabular" in line:
            in_tabular = True
            cleaned_lines.append(line)
        elif r"\end{tabular" in line:
            in_tabular = False
            cleaned_lines.append(line)
        elif in_tabular:
            cleaned_lines.append(line)
        else:
            clean_l = re.sub(r"(?<!\\)&", r"\&", line)
            cleaned_lines.append(clean_l)
    return "\n".join(cleaned_lines)


def render_title_slide(day_title: str, day_subtitle: str, doc_id: str, dates: str) -> str:
    """Renders the official government title slide."""
    t_clean = day_title.replace("&", r"\&")
    s_clean = day_subtitle.replace("&", r"\&")
    d_clean = dates.replace("&", r"\&")
    id_clean = doc_id.replace("&", r"\&")

    return rf"""
\begin{{frame}}[plain]
  \centering
  \vspace*{{-0.3cm}}
  \hbox to \textwidth{{%
    \parbox[c]{{0.15\textwidth}}{{\includegraphics[height=1.3cm,keepaspectratio]{{Logo/SUA.png}}}}%
    \hfill%
    \parbox[c]{{0.68\textwidth}}{{\centering%
      {{\fontsize{{8pt}}{{9pt}}\selectfont\textbf{{\textcolor{{darkcharcoal}}{{THE UNITED REPUBLIC OF TANZANIA}}}}}}\par\vspace{{1.5pt}}%
      {{\fontsize{{7.2pt}}{{8.2pt}}\selectfont\textbf{{\textcolor{{suagreen}}{{SOKOINE UNIVERSITY OF AGRICULTURE}}}}}}\par\vspace{{1.2pt}}%
      {{\fontsize{{6.2pt}}{{7.2pt}}\selectfont\textbf{{\textcolor{{tanzaniablue}}{{COLLEGE OF ECONOMICS AND BUSINESS STUDIES (COEBS)}}}}}}\par\vspace{{1.0pt}}%
      {{\fontsize{{5.2pt}}{{6.2pt}}\selectfont\textbf{{AB CONSULT \textbullet\ PARLIAMENTARY CAPACITY BUILDING INITIATIVE}}}}%
    }}%
    \hfill%
    \parbox[c]{{0.15\textwidth}}{{\raggedleft\includegraphics[height=1.3cm,keepaspectratio]{{Logo/Coat_of_arms_of_Tanzania.png}}}}%
  }}
  \par\vspace{{4pt}}
  \tzstrip[\textwidth]
  \par\vspace{{6pt}}
  {{\fontsize{{11.5pt}}{{13.5pt}}\selectfont\textbf{{\textcolor{{suagreen}}{{APPLICATION OF ARTIFICIAL INTELLIGENCE IN PARLIAMENTARY RESEARCH}}}}}}\par\vspace{{3pt}}
  {{\fontsize{{15pt}}{{17pt}}\selectfont\textbf{{\textcolor{{tanzaniablue}}{{{t_clean}}}}}}}\par\vspace{{2pt}}
  {{\fontsize{{8.5pt}}{{10pt}}\selectfont\textit{{{s_clean}}}}}\par\vspace{{6pt}}
  
  \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.7pt, width=0.96\textwidth, top=3pt, bottom=3pt, left=6pt, right=6pt]
    \fontsize{{6.8pt}}{{8.2pt}}\selectfont
    \begin{{tabularx}}{{\linewidth}}{{@{{}}>{{}}p{{2.6cm}}X>{{}}p{{2.0cm}}X@{{}}}}
      \textbf{{Lead Facilitator:}} & Eng. Dr. Kadeghe Fue, PhD & \textbf{{Document Ref:}} & {id_clean} \\
      \textbf{{Target Cohort:}} & Parliamentary Researchers \& Clerks & \textbf{{Program Dates:}} & {d_clean} \\
    \end{{tabularx}}
  \end{{tcolorbox}}
  
  \vfill
  \tzstrip[\textwidth]
  \par\vspace{{2pt}}
  {{\fontsize{{5.2pt}}{{6.2pt}}\selectfont\textbf{{AB Consult \textbullet\ COEBS, Sokoine University of Agriculture \textbullet\ Morogoro, Tanzania}}}}
  \vspace*{{-0.2cm}}
\end{{frame}}
"""


# ==============================================================================
# SLIDE DECK BUILDERS
# ==============================================================================

def build_executive_deck() -> str:
    """Builds the 5-Day Executive Training Outline presentation."""
    title = render_title_slide(
        day_title="Executive Training Outline",
        day_subtitle="5-Day Executive Hands-On Program Outline (Zero-Copy Desktop Ingestion)",
        doc_id="SUA/COEBS/PARL-AI/EXEC-00",
        dates="9--13 November 2026"
    )

    body = rf"""
\begin{{frame}}{{Executive Summary \& Pedagogical Philosophy}}{{The Zero-Manual-Copy Mandate ("Drop the File, Ask the AI")}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Core Executive Problem}}]
        \small
        \begin{{itemize}}
          \item Parliamentary clerks and researchers handle \textcolor{{suagreen}}{{\textbf{{hundreds of pages}}}} of bills, audit reports, and estimates weekly.
          \item Traditional copy-pasting is \textcolor{{tanzaniablue}}{{\textbf{{error-prone}}}}, causes formatting chaos, and loses evidentiary context.
          \item Legislative scrutiny requires \textcolor{{suagreen}}{{\textbf{{rapid cross-referencing}}}} without programming knowledge.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=calloutbg, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{The Applied Solution}}]
        \small
        \begin{{itemize}}
          \item \textcolor{{tanzaniablue}}{{\textbf{{Zero-Copy Ingestion:}}}} Trainees drop native \texttt{{.docx}} and \texttt{{.pdf}} gazettes directly into workspace folders.
          \item \textcolor{{suagreen}}{{\textbf{{Role-Grounded AI:}}}} Specialized prompts query whole files (\texttt{{@filename}}) inside Visual Studio Code.
          \item \textcolor{{darkcharcoal}}{{\textbf{{Split Dual-Pane Verification:}}}} Raw law is always open side-by-side with AI-synthesized outputs.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Master Ingestion Architecture}}{{5-Stage Unified Curriculum: Direct Ingestion, Verification, and Reporting}}
  \begin{{center}}
    \includegraphics[width=0.96\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_master_auto_ingestion_arch.png}}
  \end{{center}}
\end{{frame}}

\begin{{frame}}{{5-Day Applied Training Roadmap}}{{Step-by-Step Transition from Document Drop to Legislative Brief}}
  \begin{{columns}}[t]
    \begin{{column}}{{0.32\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Days 1 \& 2: Foundations}}]
        \scriptsize
        \textbf{{\textcolor{{tanzaniablue}}{{Day 1: VS Code Desk}}}}
        \begin{{itemize}}
          \item Native docx \& pdf workspace drop
          \item Extensions \& 1-click PDF build
          \item File-grounded indexing
        \end{{itemize}}
        \vspace{{2pt}}
        \textbf{{\textcolor{{suagreen}}{{Day 2: Bill Scrutiny}}}}
        \begin{{itemize}}
          \item CLEAR prompting framework
          \item Parent Act vs Amendment bill
          \item 3 Actionable PQs formulation
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.32\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=suagreen, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Days 3 \& 4: Empirical \& Policy}}]
        \scriptsize
        \textbf{{\textcolor{{suagreen}}{{Day 3: Evidence Lab}}}}
        \begin{{itemize}}
          \item NBS \& statistical report ingestion
          \item Budget variance reconciliation
          \item Dual-pane empirical audit
        \end{{itemize}}
        \vspace{{2pt}}
        \textbf{{\textcolor{{tanzaniablue}}{{Day 4: Policy Options}}}}
        \begin{{itemize}}
          \item MCPA 4-pillar evaluation
          \item 4-way stakeholder simulation
          \item Options trade-off matrices
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.32\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=darkcharcoal, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Day 5: Synthesis \& Ethics}}]
        \scriptsize
        \textbf{{\textcolor{{darkcharcoal}}{{Day 5: Tripartite Deliverables}}}}
        \begin{{itemize}}
          \item Ethical AI guardrails \& NDA
          \item 20--30 page committee report
          \item 2-page MP executive brief
          \item Complete archival audit dossier
        \end{{itemize}}
        \vspace{{2pt}}
        \textbf{{\textcolor{{suagreen}}{{Institutionalization:}}}}
        \begin{{itemize}}
          \item Bunge research standard
          \item Zero data leakage protocols
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Participant Profile \& Environment Stack}}{{Zero-Programming Threshold Designed for Parliamentary Practitioners}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Target Trainee Cohort}}]
        \small
        \begin{{itemize}}
          \item Parliamentary Researchers \& Analysts
          \item Standing Committee Clerks (PAC, LAAC, Budget)
          \item Elected Legislators \& Parliamentary Leaders
          \item Social, Legal \& Governance Practitioners
          \item \textcolor{{suagreen}}{{\textbf{{No prior coding or scripting required}}}}
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Approved Technology Stack}}]
        \small
        \begin{{itemize}}
          \item \textbf{{\textcolor{{tanzaniablue}}{{Core IDE:}}}} Visual Studio Code (Free/Open)
          \item \textbf{{\textcolor{{suagreen}}{{Extension 1:}}}} Markdown All in One
          \item \textbf{{\textcolor{{suagreen}}{{Extension 2:}}}} Markdown PDF (1-Click builds)
          \item \textbf{{\textcolor{{tanzaniablue}}{{AI Layer:}}}} GitHub Copilot / Continue.dev
          \item \textbf{{\textcolor{{darkcharcoal}}{{OS Support:}}}} Windows 10/11, macOS, Linux
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Daily Operational Schedule}}{{Rigorous Hands-On Structure Balanced with Executive Peer Reviews}}
  \begin{{center}}
    \small
    \begin{{tabularx}}{{0.94\textwidth}}{{@{{}}>{{}}p{{2.8cm}}X>{{}}p{{3.5cm}}@{{}}}}
      \toprule
      \textbf{{\textcolor{{tanzaniablue}}{{Timeframe}}}} & \textbf{{\textcolor{{tanzaniablue}}{{Session Content \& Activity}}}} & \textbf{{\textcolor{{tanzaniablue}}{{Pedagogical Format}}}} \\
      \midrule
      08:30 -- 10:00 & Morning Masterclass: Conceptual Grounding & Interactive Lecture \& Demo \\
      \textbf{{\textcolor{{suagreen}}{{10:00 -- 11:00}}}} & \textbf{{\textcolor{{suagreen}}{{Health Break \& Executive Networking Tea}}}} & \textit{{Faculty Refreshment}} \\
      11:00 -- 13:00 & Practical Hands-On Lab: Ingestion \& Prompting & Individual Laptop Work \\
      \textbf{{\textcolor{{suagreen}}{{13:00 -- 14:00}}}} & \textbf{{\textcolor{{suagreen}}{{Executive Networking Lunch}}}} & \textit{{Executive Dining}} \\
      14:00 -- 15:30 & Applied Simulation: Drafting Committee Briefs & Paired Peer Collaboration \\
      15:30 -- 16:00 & Debrief, Quality Audit \& Verification Checklist & Faculty Q\&A \& Adjournment \\
      \bottomrule
    \end{{tabularx}}
  \end{{center}}
\end{{frame}}

\begin{{frame}}{{Institutional Governance \& Sustainability}}{{Strategic Integration in Bunge Research Operations}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Immediate Institutional Impact}}]
        \small
        \begin{{itemize}}
          \item \textbf{{\textcolor{{tanzaniablue}}{{10x Faster Analysis:}}}} 100-page bills scrutinized in 15 minutes instead of 3 days.
          \item \textbf{{\textcolor{{suagreen}}{{Evidentiary Depth:}}}} CAG financial audit tables cross-referenced with zero copy errors.
          \item \textbf{{\textcolor{{darkcharcoal}}{{Uniform Output:}}}} Publication-grade PDF dossiers ready for committee distribution.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=calloutbg, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Long-Term Institutionalization}}]
        \small
        \begin{{itemize}}
          \item \textbf{{\textcolor{{suagreen}}{{Trained Cohort:}}}} Self-sufficient research clerks across all standing committees.
          \item \textbf{{\textcolor{{tanzaniablue}}{{Security Architecture:}}}} Zero document leakage; all data remains in sovereign desks.
          \item \textbf{{\textcolor{{darkcharcoal}}{{Academic Partnership:}}}} Continuous capacity building via COEBS, SUA \& AB Consult.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}
"""
    return title + body


def build_day1_deck() -> str:
    """Builds the Day 1 presentation deck."""
    title = render_title_slide(
        day_title="Day 1 Practical Presentation",
        day_subtitle="Automated Native File Ingestion & Direct AI Querying in Visual Studio Code",
        doc_id="SUA/COEBS/PARL-AI/DOC-01",
        dates="Monday, 9th November 2026"
    )

    body = rf"""
\begin{{frame}}{{The Legislative Document Bottleneck}}{{Why Traditional Manual Copy-Pasting Fails Parliamentary Research}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{The Manual Reality}}]
        \small
        \begin{{itemize}}
          \item Clerks spend \textcolor{{tanzaniablue}}{{\textbf{{80\% of their time}}}} copying, pasting, and reformatting statutory clauses.
          \item Highlighting scanned PDFs creates broken line wraps, unreadable tables, and missed amendments.
          \item Critical committee deadlines force superficial reading of major legislative bills.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=calloutbg, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{The Zero-Copy Paradigm}}]
        \small
        \begin{{itemize}}
          \item \textcolor{{suagreen}}{{\textbf{{Never copy-paste:}}}} Drop original \texttt{{.docx}} and \texttt{{.pdf}} files straight into VS Code folders.
          \item Direct AI indexing reads documents \textcolor{{tanzaniablue}}{{\textbf{{natively in memory}}}}.
          \item Researchers maintain full structural context, schedules, clauses, and tabular footnotes.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{VS Code Desktop Workspace Architecture}}{{Structured Folder Hierarchy for Legislative Documents}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day1_workspace_tree.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Workspace Rules}}]
        \scriptsize
        \begin{{itemize}}
          \item \texttt{{raw\_bills/}}: Store native government gazettes and draft bills.
          \item \texttt{{parent\_acts/}}: Principal Acts for comparative scrutiny.
          \item \texttt{{audit\_data/}}: Official CAG reports and NBS statistical tables.
          \item \texttt{{briefs/}}: Output Markdown files compiled into PDFs.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Automated Ingestion Pipeline}}{{End-to-End Workflow: Native Document to Verified Legislative Brief}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.58\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day1_auto_ingestion_arch.png}}
    \end{{column}}
    \begin{{column}}{{0.39\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=suagreen, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Pipeline Stages}}]
        \scriptsize
        \textbf{{\textcolor{{tanzaniablue}}{{1. Document Drop:}}}} Native Word/PDF drop into workspace folder.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{suagreen}}{{2. AI Indexing:}}}} Reference directly via \texttt{{@filename}} token.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{darkcharcoal}}{{3. Dual-Pane Check:}}}} Side-by-side audit of AI claims against source text.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{tanzaniablue}}{{4. 1-Click Export:}}}} Export to publication PDF in 1 second.
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Role-Grounded Document Interrogation}}{{Direct Querying via @filename Indexing in VS Code}}
  \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Exemplary Parliamentary AI Command}}]
    \small
    \texttt{{@raw\_bills/Mining\_Amendment\_Bill\_2026.docx @parent\_acts/Mining\_Act\_Cap123.pdf}}\\
    \vspace{{3pt}}
    \textcolor{{suagreen}}{{\textbf{{Role:}}}} Senior Parliamentary Research Fellow for the Energy \& Minerals Committee.\\
    \textcolor{{tanzaniablue}}{{\textbf{{Task:}}}} Cross-examine Section 14 of the Bill against Section 42 of the Principal Act.\\
    \textbf{{Output:}} Generate a 3-column comparative table detailing: (1) Existing Provision, (2) Proposed Amendment, and (3) Strategic Legal Impact on Artisanal Miners.
  \end{{tcolorbox}}
  \vspace{{4pt}}
  \begin{{center}}
    \scriptsize \textbf{{\textcolor{{suagreen}}{{Result:}}}} Instantaneous tabular breakdown with exact statutory citations and zero hallucination risk.
  \end{{center}}
\end{{frame}}

\begin{{frame}}{{Dual-Pane Verification Architecture}}{{Guaranteeing Evidentiary Truth in Committee Briefings}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Left Pane: Raw Statutory Source}}]
        \small
        \begin{{itemize}}
          \item Scanned National Gazette or PDF Act open in VS Code built-in viewer.
          \item Exact line and clause numbers visible to researcher.
          \item Unaltered official government authority.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=calloutbg, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Right Pane: Synthesized Analysis}}]
        \small
        \begin{{itemize}}
          \item Active Markdown analysis brief with synthesized matrix.
          \item Researcher verifies each quote and statistic against Left Pane.
          \item Zero unverified assertions leave the research desk.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{1-Click Markdown PDF Publishing}}{{Publishing Committee Briefs to Official Standards}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Markdown Formatting Hygiene}}]
        \small
        \begin{{itemize}}
          \item \textbf{{\textcolor{{tanzaniablue}}{{Never use hashes or asterisks in titles:}}}} Use semantic styling and colors.
          \item Structure tables with standard GitHub Markdown pipes (\texttt{{|}}).
          \item Use callout blockquotes (\texttt{{> [!IMPORTANT]}}) for high-impact legislative alerts.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{1-Click PDF Generation}}]
        \small
        \begin{{itemize}}
          \item Right-click active document $\rightarrow$ \textcolor{{suagreen}}{{\textbf{{Markdown PDF: Export (pdf)}}}}.
          \item Automatically styles typography, tables, and page headers.
          \item Produces distribution-ready PDF in $<2$ seconds.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Day 1 Hands-On Lab \& Deliverables}}{{Practical Trainee Assessment Checklist}}
  \begin{{tcolorbox}}[colback=lightgrey, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Individual Lab Exercise (90 Minutes)}}]
    \small
    \begin{{enumerate}}
      \item Initialize your assigned workspace folder on your laptop desk.
      \item Ingest the \texttt{{Finance\_Bill\_2026.docx}} and \texttt{{Income\_Tax\_Act\_Cap332.pdf}}.
      \item Execute a role-grounded query identifying all proposed tax threshold shifts.
      \item Reconcile the proposed shifts in a dual-pane verification layout.
      \item Export your completed analysis to \texttt{{briefs/Tax\_Threshold\_Brief.pdf}}.
    \end{{enumerate}}
  \end{{tcolorbox}}
  \vspace{{4pt}}
  \begin{{center}}
    \textbf{{\textcolor{{tanzaniablue}}{{Day 1 Milestone:}}}} Every trainee exports their first zero-copy verified legislative brief!
  \end{{center}}
\end{{frame}}
"""
    return title + body


def build_day2_deck() -> str:
    """Builds the Day 2 presentation deck."""
    title = render_title_slide(
        day_title="Day 2 Practical Presentation",
        day_subtitle="Statutory Scrutiny, CAG Audit Ingestion & Parliamentary Questions",
        doc_id="SUA/COEBS/PARL-AI/DOC-02",
        dates="Tuesday, 10th November 2026"
    )

    body = rf"""
\begin{{frame}}{{The Legislative Scrutiny Challenge}}{{Unpacking Complex Amendments Under Tight Committee Deadlines}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{The Committee Scrutiny Trap}}]
        \small
        \begin{{itemize}}
          \item Government bills often amend \textcolor{{tanzaniablue}}{{\textbf{{multiple parent acts}}}} simultaneously.
          \item Minor clauses (e.g., "delete word 'may' and substitute 'shall'") carry massive legal ramifications.
          \item Committee members receive bills days before scheduled plenary debate.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=calloutbg, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{The AI-Powered Solution}}]
        \small
        \begin{{itemize}}
          \item Ingest both the \textcolor{{suagreen}}{{\textbf{{Parent Act}}}} and the \textcolor{{tanzaniablue}}{{\textbf{{Amendment Bill}}}} simultaneously.
          \item Apply the structured \textcolor{{darkcharcoal}}{{\textbf{{CLEAR Prompting Framework}}}} to identify concealed legal shifts.
          \item Extract actionable audit evidence from the Controller and Auditor General (CAG).
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{The CLEAR Prompting Framework}}{{Guaranteed Clarity, Constraint, and Evidentiary Precision}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day2_clear_framework.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.2mm, boxrule=0.7pt, title=\textbf{{The 5 CLEAR Pillars}}]
        \scriptsize
        \textbf{{\textcolor{{tanzaniablue}}{{C -- Context:}}}} Legislative background \& mandate.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{suagreen}}{{L -- Legislation:}}}} Specific section \& clause boundaries.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{tanzaniablue}}{{E -- Evidence:}}}} Ground claims strictly in CAG/NBS text.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{suagreen}}{{A -- Actionable:}}}} Produce tangible questions for MPs.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{darkcharcoal}}{{R -- Red Lines:}}}} Zero speculation or policy hallucination.
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Statutory Scrutiny Workspace Tree}}{{Dual Document Comparative Workspace Setup}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day2_workspace.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=suagreen, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Workspace Organization}}]
        \scriptsize
        \begin{{itemize}}
          \item \texttt{{parent\_acts/}}: Official consolidated laws of Tanzania.
          \item \texttt{{bills/}}: New legislative bills gazetted for first reading.
          \item \texttt{{cag\_reports/}}: Annual CAG audit reports for ministries.
          \item \texttt{{matrices/}}: 4-column statutory comparative matrices.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{CAG Audit Ingestion \& Discrepancy Tracking}}{{Bridging Statutory Authority with Public Spending Realities}}
  \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{CAG Audit Prompting Strategy}}]
    \small
    \texttt{{@cag\_reports/CAG\_Report\_Central\_Gov\_2025.pdf @bills/Appropriation\_Bill\_2026.docx}}\\
    \vspace{{3pt}}
    \textcolor{{suagreen}}{{\textbf{{Context:}}}} Standing Committee on Public Accounts (PAC).\\
    \textcolor{{tanzaniablue}}{{\textbf{{Task:}}}} Reconcile Vote 48 development expenditure allocations with CAG-reported non-performing procurement contracts.\\
    \textbf{{Output:}} Table of unresolved audit queries exceeding TZS 500 million, citing the exact CAG page numbers and contract reference IDs.
  \end{{tcolorbox}}
  \vspace{{4pt}}
  \begin{{center}}
    \scriptsize \textbf{{\textcolor{{suagreen}}{{Benefit:}}}} Committee clerks discover hidden fiscal discrepancies in seconds rather than days.
  \end{{center}}
\end{{frame}}

\begin{{frame}}{{The 4-Column Statutory Scrutiny Matrix}}{{Standardized Legislative Comparison for Standing Committees}}
  \begin{{center}}
    \small
    \begin{{tabularx}}{{0.94\textwidth}}{{@{{}}>{{}}p{{2.6cm}}>{{}}p{{3.4cm}}>{{}}p{{3.8cm}}X@{{}}}}
      \toprule
      \textbf{{\textcolor{{tanzaniablue}}{{Parent Act Clause}}}} & \textbf{{\textcolor{{tanzaniablue}}{{Proposed Amendment}}}} & \textbf{{\textcolor{{tanzaniablue}}{{Substantive Legal Shift}}}} & \textbf{{\textcolor{{tanzaniablue}}{{Actionable Scrutiny Note}}}} \\
      \midrule
      Sec 24(1): "Minister may consult Council" & "Minister shall act on binding advice of Board" & Executive discretion curtailed; board veto introduced & Verify board composition and appointment mandate in Schedule 2. \\
      \addlinespace
      Sec 88(2): "Fine not exceeding 5m TZS" & "Fine not exceeding 50m TZS or 5 yrs jail" & Ten-fold sanction increase; mandatory minimum jail & Scrutinize proportionality against economic offences thresholds. \\
      \bottomrule
    \end{{tabularx}}
  \end{{center}}
\end{{frame}}

\begin{{frame}}{{Formulating Actionable Parliamentary Questions (PQs)}}{{Converting Analytical Scrutiny into Piercing Committee Questions}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Weak PQ (Vague / Opinion)}}]
        \small
        \textit{{"Why is the government increasing mining penalties when our artisanal miners in Geita are already poor and struggling?"}}\\[4pt]
        \textcolor{{tanzaniablue}}{{\textbf{{Flaw:}}}} Allows Minister to give evasive, political answer without addressing legal technicalities.
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=calloutbg, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Actionable PQ (Evidence-Grounded)}}]
        \small
        \textit{{"In light of Clause 14 raising fines tenfold while CAG Report 2025 (p. 84) shows 68\% of mineral disputes remain unadjudicated, what specific appellate recourse is guaranteed to smallholder miners before forfeiture?"}}\\[4pt]
        \textcolor{{suagreen}}{{\textbf{{Strength:}}}} Cites exact clause and CAG audit facts.
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}
"""
    return title + body


def build_day3_deck() -> str:
    """Builds the Day 3 presentation deck."""
    title = render_title_slide(
        day_title="Day 3 Practical Presentation",
        day_subtitle="Empirical Evidence Ingestion, Statistical NBS Fact-Checking & Sectoral Dossiers",
        doc_id="SUA/COEBS/PARL-AI/DOC-03",
        dates="Wednesday, 11th November 2026"
    )

    body = rf"""
\begin{{frame}}{{The Empirical Deficit in Parliamentary Debate}}{{Replacing Rhetorical Assertion with Verified Macro-Economic Data}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{The Rhetoric Trap}}]
        \small
        \begin{{itemize}}
          \item Debates often hinge on \textcolor{{tanzaniablue}}{{\textbf{{unverified assertions}}}} and anecdotal claims.
          \item Budget allocations are passed without cross-checking against actual disbursements.
          \item Regional inequalities and sectoral service delivery deficits remain obscured.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=calloutbg, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{The Empirical Mandate}}]
        \small
        \begin{{itemize}}
          \item Ground every legislative argument in \textcolor{{suagreen}}{{\textbf{{authoritative data}}}}: NBS, MoFP, and CAG.
          \item Automate statistical extraction from dense statistical tables.
          \item Equip committee chairs with \textcolor{{darkcharcoal}}{{\textbf{{fact-checking ammunition}}}} during ministerial cross-examination.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Hierarchy of Evidence in Parliamentary Research}}{{Establishing Document Authority and Evidentiary Weight}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day3_evidence_hierarchy.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Evidence Hierarchy}}]
        \scriptsize
        \textbf{{\textcolor{{suagreen}}{{Tier 1: Legal \& Audit Authority}}}}
        \begin{{itemize}}
          \item Acts of Parliament, National Gazettes
          \item CAG Audited Public Accounts
        \end{{itemize}}
        \vspace{{2pt}}
        \textbf{{\textcolor{{tanzaniablue}}{{Tier 2: Macro Statistical Data}}}}
        \begin{{itemize}}
          \item National Bureau of Statistics (NBS)
          \item Bank of Tanzania (BoT) Bulletins
        \end{{itemize}}
        \vspace{{2pt}}
        \textbf{{\textcolor{{darkcharcoal}}{{Tier 3: Policy \& Academic Studies}}}}
        \begin{{itemize}}
          \item University research, donor reviews
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Statistical Evidence Lab Workspace}}{{Dual-Folder Architecture for Statistical Ingestion}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day3_workspace.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=suagreen, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Data Organization}}]
        \scriptsize
        \begin{{itemize}}
          \item \texttt{{budget\_books/}}: Volume II ministerial estimates.
          \item \texttt{{nbs\_surveys/}}: Household budget surveys and census.
          \item \texttt{{cag\_audited/}}: Financial audit tables and actuals.
          \item \texttt{{dossiers/}}: Sectoral statistical briefs for committees.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Dual-Pane Fact-Checking Architecture}}{{Split-Screen Verification of Ministerial Budget Statements}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day3_fact_checking_panes.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Fact-Checking Flow}}]
        \scriptsize
        \begin{{itemize}}
          \item \textbf{{\textcolor{{tanzaniablue}}{{Step 1:}}}} Minister speech claims 95\% budget execution in water projects.
          \item \textbf{{\textcolor{{suagreen}}{{Step 2:}}}} Ingest MoFP exchequer releases and CAG audit volume.
          \item \textbf{{\textcolor{{darkcharcoal}}{{Step 3:}}}} AI exposes that actual disbursement was only 48.2\%.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Empirical Budget Variance Analysis}}{{Exposing Discrepancies Across Tanzanian Regions}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.60\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_empirical_budget_variance.png}}
    \end{{column}}
    \begin{{column}}{{0.38\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=suagreen, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Key Findings}}]
        \scriptsize
        \begin{{itemize}}
          \item High variance between \textcolor{{tanzaniablue}}{{\textbf{{approved allocation}}}} vs \textcolor{{suagreen}}{{\textbf{{actual release}}}}.
          \item Peripheral regions (Kigoma, Kagera) face disbursement lags $>35\%$.
          \item Provides parliamentary committees with statistical justification for reallocation.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Constructing the Sectoral Statistical Dossier}}{{Standardized Empirical Template for Committee Sessions}}
  \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Core Sections of a Committee Statistical Dossier}}]
    \small
    \begin{{enumerate}}
      \item \textbf{{\textcolor{{tanzaniablue}}{{Executive Overview:}}}} 3 bullet points summarizing macro-economic status.
      \item \textbf{{\textcolor{{suagreen}}{{3-Year Budget Trend Table:}}}} Approved vs Disbursed vs CAG Actuals.
      \item \textbf{{\textcolor{{tanzaniablue}}{{Regional Equity Matrix:}}}} Per-capita capital spending across 26 mainland regions.
      \item \textbf{{\textcolor{{suagreen}}{{Targeted Scrutiny Questions:}}}} 5 direct PQs citing exact table and page numbers.
    \end{{enumerate}}
  \end{{tcolorbox}}
  \vspace{{4pt}}
  \begin{{center}}
    \textbf{{\textcolor{{suagreen}}{{Deliverable:}}}} Standalone, clean PDF dossier distributed to MPs 24 hours prior to debate.
  \end{{center}}
\end{{frame}}
"""
    return title + body


def build_day4_deck() -> str:
    """Builds the Day 4 presentation deck."""
    title = render_title_slide(
        day_title="Day 4 Practical Presentation",
        day_subtitle="Multi-Criteria Policy Analysis (MCPA) & Stakeholder Simulations",
        doc_id="SUA/COEBS/PARL-AI/DOC-04",
        dates="Thursday, 12th November 2026"
    )

    body = rf"""
\begin{{frame}}{{From Description to Decision}}{{Why Parliamentary Committees Require Multi-Criteria Policy Analysis}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{The Descriptive Trap}}]
        \small
        \begin{{itemize}}
          \item Most research briefs merely \textcolor{{tanzaniablue}}{{\textbf{{summarize}}}} what the draft bill states.
          \item Committees are left without clear comparative options or trade-off assessments.
          \item Unintended economic and social consequences emerge after bill enactment.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=calloutbg, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{The MCPA Methodology}}]
        \small
        \begin{{itemize}}
          \item Systematically evaluate \textcolor{{suagreen}}{{\textbf{{competing policy alternatives}}}} against standard criteria.
          \item Simulate reactions from \textcolor{{tanzaniablue}}{{\textbf{{key stakeholder groups}}}}.
          \item Give committee leadership defensible amendments backed by empirical scoring.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{The 4 Pillars of Parliamentary MCPA}}{{Rigorous Assessment Framework for Legislative Proposals}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day4_mcpa_pillars.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.2mm, boxrule=0.7pt, title=\textbf{{The 4 Evaluation Pillars}}]
        \scriptsize
        \textbf{{\textcolor{{tanzaniablue}}{{1. Fiscal Sustainability:}}}} Revenue yield, debt impact, and administrative costs.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{suagreen}}{{2. Economic Equity:}}}} Distributional impact on vulnerable \& rural citizens.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{darkcharcoal}}{{3. Admin Feasibility:}}}} Institutional capacity of TRA / local councils.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{tanzaniablue}}{{4. Legal Alignment:}}}} Compliance with Constitution \& EAC treaties.
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Analytical Transition Architecture}}{{Transforming Raw Legislative Text into Strategic Option Sets}}
  \begin{{center}}
    \includegraphics[width=0.96\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day4_analytical_transition.png}}
  \end{{center}}
\end{{frame}}

\begin{{frame}}{{4-Way Stakeholder Perspective Simulation}}{{Simulating Competing Policy Pressures in Committee Rooms}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day4_stakeholder_simulation.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=suagreen, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Simulated Groups}}]
        \scriptsize
        \textbf{{\textcolor{{tanzaniablue}}{{Treasury / TRA:}}}} Focus on revenue targets and compliance.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{suagreen}}{{Private Sector (TPSF):}}}} Competitiveness, capital flight, and investment security.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{darkcharcoal}}{{Civil Society / Citizens:}}}} Cost of living, basic social services, equity.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{tanzaniablue}}{{Local Government (TAMISEMI):}}}} Revenue sharing and grassroots service delivery.
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Constructing the Policy Trade-Off Matrix}}{{Evaluating 3 Concrete Policy Options for the Committee}}
  \begin{{center}}
    \small
    \begin{{tabularx}}{{0.94\textwidth}}{{@{{}}>{{}}p{{2.5cm}}>{{}}p{{3.5cm}}>{{}}p{{3.8cm}}X@{{}}}}
      \toprule
      \textbf{{\textcolor{{tanzaniablue}}{{Policy Option}}}} & \textbf{{\textcolor{{tanzaniablue}}{{Fiscal Yield}}}} & \textbf{{\textcolor{{tanzaniablue}}{{Social \& Equity Impact}}}} & \textbf{{\textcolor{{tanzaniablue}}{{Strategic Recommendation}}}} \\
      \midrule
      Option A: Status Quo (Zero reform) & Low revenue growth; persistent collection leaks & No immediate citizen backlash; high long-term deficit & \textcolor{{darkcharcoal}}{{\textbf{{Rejected:}}}} Deficit expands; unsustainable. \\
      \addlinespace
      Option B: Blanket Universal Levy & High immediate revenue (TZS 450B estimated) & Regressive; heavily hits rural smallholders & \textcolor{{tanzaniablue}}{{\textbf{{Modified:}}}} Introduce exempt basic consumer goods. \\
      \addlinespace
      Option C: Tiered Progressive Model & Moderate-High yield (TZS 380B) & Progressive; shields low-income households & \textcolor{{suagreen}}{{\textbf{{Recommended:}}}} Best multi-criteria balance. \\
      \bottomrule
    \end{{tabularx}}
  \end{{center}}
\end{{frame}}
"""
    return title + body


def build_day5_deck() -> str:
    """Builds the Day 5 presentation deck."""
    title = render_title_slide(
        day_title="Day 5 Practical Presentation",
        day_subtitle="Ethical AI Guardrails, Tripartite Briefings & Strategic Institutionalization",
        doc_id="SUA/COEBS/PARL-AI/DOC-05",
        dates="Friday, 13th November 2026"
    )

    body = rf"""
\begin{{frame}}{{The Non-Negotiable Mandate}}{{Data Privacy, Institutional Sovereignty, and Ethical Verification}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{The Risks of Ungoverned AI}}]
        \small
        \begin{{itemize}}
          \item Leaking \textcolor{{tanzaniablue}}{{\textbf{{confidential government white papers}}}} or draft cabinet bills to public LLMs.
          \item Accepting AI hallucinations without primary legal and statistical verification.
          \item Erode parliamentary sovereignty and public trust in legislative oversight.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=calloutbg, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{The Ethical Guardrails}}]
        \small
        \begin{{itemize}}
          \item \textcolor{{suagreen}}{{\textbf{{Sovereign Local Desks:}}}} All processing conducted within private workspace folders.
          \item \textcolor{{tanzaniablue}}{{\textbf{{Human-in-the-Loop:}}}} AI proposes synthesis; parliamentary researchers verify and sign off.
          \item Compliance with Tanzania \textcolor{{darkcharcoal}}{{\textbf{{Personal Data Protection Act 2022}}}}.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Ethical AI Governance Pillars}}{{Architectural Framework for Responsible Parliamentary AI}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day5_ethical_pillars.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.2mm, boxrule=0.7pt, title=\textbf{{The 4 Guardrails}}]
        \scriptsize
        \textbf{{\textcolor{{tanzaniablue}}{{1. Non-Disclosure \& Privacy:}}}} Zero sensitive data leakage.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{suagreen}}{{2. Evidentiary Traceability:}}}} Every claim tied to exact clause/page.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{darkcharcoal}}{{3. Non-Partisan Objectivity:}}}} Unbiased multi-option evaluation.\\
        \vspace{{2pt}}
        \textbf{{\textcolor{{tanzaniablue}}{{4. Sovereign Institutionalization:}}}} Bunge-owned research assets.
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Tripartite Legislative Reporting Architecture}}{{Serving the Three Critical Audiences of Parliament}}
  \begin{{center}}
    \includegraphics[width=0.96\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day5_tripartite_architecture.png}}
  \end{{center}}
\end{{frame}}

\begin{{frame}}{{The 3 Core Legislative Deliverables}}{{Matching Information Density to Decision-Maker Roles}}
  \begin{{columns}}[t]
    \begin{{column}}{{0.32\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Deliverable 1: Report}}]
        \scriptsize
        \textbf{{\textcolor{{tanzaniablue}}{{Comprehensive Committee Report}}}}
        \begin{{itemize}}
          \item 20--30 pages of detailed statutory \& statistical analysis.
          \item Target: Standing Committee Clerks \& Chairs.
          \item Full annexes, comparative matrix, and audit tables.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.32\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=suagreen, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Deliverable 2: Brief}}]
        \scriptsize
        \textbf{{\textcolor{{suagreen}}{{2-Page Executive Policy Brief}}}}
        \begin{{itemize}}
          \item 2 pages maximum.
          \item Target: Busy Members of Parliament (MPs) in plenary.
          \item Executive summary, 3 key trade-offs, and 3 sharp PQs.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.32\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=darkcharcoal, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Deliverable 3: Dossier}}]
        \scriptsize
        \textbf{{\textcolor{{darkcharcoal}}{{Verification Audit Dossier}}}}
        \begin{{itemize}}
          \item Complete archival trail.
          \item Target: Committee Legal Counsel \& Hansard archive.
          \item Dual-pane source snippets and prompt logs.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Institutionalization Roadmap}}{{Transforming Individual Skills into Permanent Institutional Capacity}}
  \begin{{center}}
    \small
    \begin{{tabularx}}{{0.94\textwidth}}{{@{{}}>{{}}p{{2.5cm}}>{{}}p{{3.5cm}}>{{}}p{{3.8cm}}X@{{}}}}
      \toprule
      \textbf{{\textcolor{{tanzaniablue}}{{Phase}}}} & \textbf{{\textcolor{{tanzaniablue}}{{Operational Focus}}}} & \textbf{{\textcolor{{tanzaniablue}}{{Core Output}}}} & \textbf{{\textcolor{{tanzaniablue}}{{Institutional Champion}}}} \\
      \midrule
      Phase 1: Pilot & Rollout in PAC, LAAC \& Budget Committees & 10 Certified Committee Research Desks & Lead Facilitator \& Committee Chairs \\
      \addlinespace
      Phase 2: Standard & Formalization of Bunge AI Research Protocols & Official Parliamentary Research Guideline & Clerk of the National Assembly \\
      \addlinespace
      Phase 3: Scale & Full training across all standing committees & Sovereign Parliamentary AI Knowledgebase & Parliamentary Service Commission \\
      \bottomrule
    \end{{tabularx}}
  \end{{center}}
\end{{frame}}
"""
    return title + body


def build_master_deck() -> str:
    """Builds the Comprehensive 5-Day Master Curriculum deck."""
    title = render_title_slide(
        day_title="Master Parliamentary AI Presentation",
        day_subtitle="Comprehensive 5-Day Applied AI Research & Legislative Scrutiny Curriculum",
        doc_id="SUA/COEBS/PARL-AI/MASTER-01",
        dates="9--13 November 2026"
    )

    body = rf"""
\begin{{frame}}{{Executive Curriculum Overview}}{{Transforming Legislative Research Across the National Assembly}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{The Strategic Vision}}]
        \small
        \begin{{itemize}}
          \item Position the \textcolor{{tanzaniablue}}{{\textbf{{National Assembly of Tanzania}}}} as a continental pioneer in AI-assisted legislative research.
          \item Empower non-programming researchers to process complex multi-hundred-page bills in minutes.
          \item Ensure strict compliance with national privacy and data sovereignty laws.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=calloutbg, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Pedagogical Foundations}}]
        \small
        \begin{{itemize}}
          \item \textcolor{{suagreen}}{{\textbf{{Zero-Manual-Copy Mandate:}}}} Native document drop into structured folders.
          \item \textcolor{{tanzaniablue}}{{\textbf{{Dual-Pane Verification:}}}} Zero unverified assertions leave the research desk.
          \item \textcolor{{darkcharcoal}}{{\textbf{{Tripartite Output:}}}} Tailored briefs for clerks, MPs, and archival records.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Master Ingestion Architecture}}{{The 5-Stage Direct Ingestion, Verification, and Reporting Pipeline}}
  \begin{{center}}
    \includegraphics[width=0.96\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_master_auto_ingestion_arch.png}}
  \end{{center}}
\end{{frame}}

\begin{{frame}}{{Day 1: VS Code Desk \& Ingestion}}{{Establishing the Digital Workbench for Parliamentary Analysts}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day1_auto_ingestion_arch.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Key Outcomes}}]
        \scriptsize
        \begin{{itemize}}
          \item Standardized folder tree (\texttt{{raw\_bills/}}, \texttt{{parent\_acts/}}, \texttt{{briefs/}}).
          \item Direct file-grounded indexing via \texttt{{@filename}}.
          \item 1-Click Markdown PDF publishing pipeline.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Day 2: Statutory Scrutiny \& Audit Queries}}{{Parent Act vs Bill Scrutiny & CAG Discrepancy Extraction}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day2_clear_framework.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=suagreen, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Key Outcomes}}]
        \scriptsize
        \begin{{itemize}}
          \item CLEAR Prompting Framework mastery.
          \item 4-column statutory comparative matrices.
          \item 3 evidence-grounded Parliamentary Questions (PQs) per bill.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Day 3: Empirical Statistical Evidence Lab}}{{NBS Macro-Data Ingestion & Budget Variance Reconciliations}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day3_fact_checking_panes.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Key Outcomes}}]
        \scriptsize
        \begin{{itemize}}
          \item Dual-pane empirical fact-checking.
          \item Reconciliation of budget estimates vs CAG audited disbursements.
          \item Standalone sectoral statistical dossiers.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Day 4: Multi-Criteria Policy Analysis (MCPA)}}{{Simulating Competing Stakeholder Pressures and Trade-Offs}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day4_mcpa_pillars.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=suagreen, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Key Outcomes}}]
        \scriptsize
        \begin{{itemize}}
          \item 4-Pillar MCPA evaluative framework.
          \item 4-way stakeholder perspective simulations (Treasury, Business, Citizens, Local Gov).
          \item Weighted policy options matrices.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Day 5: Ethical Governance \& Tripartite Briefings}}{{Producing the Three Core Parliamentary Deliverables}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.56\textwidth}}
      \includegraphics[width=\textwidth,height=5.2cm,keepaspectratio]{{figures/fig_day5_tripartite_architecture.png}}
    \end{{column}}
    \begin{{column}}{{0.41\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=darkcharcoal, arc=1.2mm, boxrule=0.7pt, title=\textbf{{Key Outcomes}}]
        \scriptsize
        \begin{{itemize}}
          \item 20--30 page Comprehensive Committee Report.
          \item 2-page High-Impact Executive Policy Brief for MPs.
          \item Archival Verification \& Audit Trail Dossier.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}

\begin{{frame}}{{Institutional Impact \& Certificate of Competency}}{{Empowering the Next Generation of Parliamentary Research Leaders}}
  \begin{{columns}}[c]
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=lightgrey, colframe=tanzaniablue, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Institutional Competencies}}]
        \small
        \begin{{itemize}}
          \item Independent operation of sovereign AI workstations.
          \item Rapid statutory scrutiny of urgent government bills.
          \item Zero data leakage and strict NDA adherence.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
    \begin{{column}}{{0.48\textwidth}}
      \begin{{tcolorbox}}[colback=calloutbg, colframe=suagreen, arc=1.5mm, boxrule=0.8pt, title=\textbf{{Certification Criteria}}]
        \small
        \begin{{itemize}}
          \item 100\% attendance in hands-on afternoon labs.
          \item Successful submission of verified Tripartite Deliverables.
          \item Joint certification by SUA (COEBS) \& AB Consult.
        \end{{itemize}}
      \end{{tcolorbox}}
    \end{{column}}
  \end{{columns}}
\end{{frame}}
"""
    return title + body


# Registry of available slide decks
DECK_REGISTRY = {
    "executive_overview_presentation": {
        "title": "Executive Curriculum Outline",
        "short_title": "Executive Overview",
        "builder": build_executive_deck,
        "desc": "5-Day Executive Hands-On Program Outline & Strategic Roadmap"
    },
    "day_1_presentation": {
        "title": "Day 1: Direct File Ingestion in VS Code",
        "short_title": "Day 1 Presentation",
        "builder": build_day1_deck,
        "desc": "Automated Native File Ingestion & Workspace Setup in VS Code"
    },
    "day_2_presentation": {
        "title": "Day 2: Statutory Scrutiny & Audit Queries",
        "short_title": "Day 2 Presentation",
        "builder": build_day2_deck,
        "desc": "Statutory Scrutiny, CAG Audit Ingestion & Parliamentary Questions"
    },
    "day_3_presentation": {
        "title": "Day 3: Statistical Ingestion & Fact-Checking",
        "short_title": "Day 3 Presentation",
        "builder": build_day3_deck,
        "desc": "Statistical Ingestion, NBS Fact-Checking & Sectoral Dossiers"
    },
    "day_4_presentation": {
        "title": "Day 4: MCPA & Stakeholder Simulation",
        "short_title": "Day 4 Presentation",
        "builder": build_day4_deck,
        "desc": "Multi-Criteria Policy Analysis (MCPA) & Stakeholder Simulations"
    },
    "day_5_presentation": {
        "title": "Day 5: Ethical AI & Tripartite Reporting",
        "short_title": "Day 5 Presentation",
        "builder": build_day5_deck,
        "desc": "Ethical AI Guardrails, Tripartite Briefings & Strategic Institutionalization"
    },
    "master_parliamentary_ai_presentation": {
        "title": "Master 5-Day Applied AI Curriculum",
        "short_title": "Master Presentation",
        "builder": build_master_deck,
        "desc": "Comprehensive 5-Day Master Applied AI Parliamentary Curriculum Deck"
    },
}


def compile_slide_deck(deck_id: str, lualatex_bin: str) -> Optional[Path]:
    """Compiles a specific slide deck into a publication-grade PDF."""
    if deck_id not in DECK_REGISTRY:
        print(f"Error: Unknown deck ID '{deck_id}'")
        return None

    deck_info = DECK_REGISTRY[deck_id]
    short_title = deck_info["short_title"]
    raw_tex = get_beamer_preamble(short_title) + "\n\\begin{document}\n" + deck_info["builder"]() + "\n\\end{document}\n"
    tex_content = sanitize_slide_tex(raw_tex)

    tex_file = OUTPUT_DIR / f"{deck_id}.tex"
    pdf_file = OUTPUT_DIR / f"{deck_id}.pdf"

    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(tex_content)

    print(f"\n[Compiling] {deck_id}.tex ...")
    
    # Pass 1: Build document and calculate layout
    cmd1 = [lualatex_bin, "-interaction=nonstopmode", f"{deck_id}.tex"]
    res1 = subprocess.run(cmd1, cwd=OUTPUT_DIR, capture_output=True, text=True)
    if res1.returncode != 0:
        print(f"Error in Pass 1 for {deck_id}:")
        for line in res1.stdout.split("\n"):
            if line.startswith("!"):
                print("  " + line)
        return None

    # Pass 2: Finalize total slide numbers and cross-references
    cmd2 = [lualatex_bin, "-interaction=nonstopmode", f"{deck_id}.tex"]
    res2 = subprocess.run(cmd2, cwd=OUTPUT_DIR, capture_output=True, text=True)
    if res2.returncode != 0:
        print(f"Error in Pass 2 for {deck_id}:")
        return None

    # Clean up auxiliary LaTeX files
    for ext in [".aux", ".log", ".nav", ".out", ".snm", ".toc", ".vrb"]:
        aux = OUTPUT_DIR / f"{deck_id}{ext}"
        if aux.exists():
            aux.unlink()

    if pdf_file.exists():
        size_kb = pdf_file.stat().st_size / 1024.0
        print(f"SUCCESS: Generated {pdf_file.name} ({size_kb:.1f} KB)")
        return pdf_file
    else:
        print(f"Failed to find generated PDF: {pdf_file}")
        return None


def generate_all_decks(target_deck: Optional[str] = None):
    """Generates all or specified slide decks."""
    print("======================================================================")
    print("PARLIAMENTARY AI TRAINING: HIGH-QUALITY SLIDE DECK GENERATOR")
    print(f"Destination: {OUTPUT_DIR.resolve()}")
    print("======================================================================")

    ensure_symlinks()
    lualatex_bin = get_lualatex_cmd()
    print(f"Using LaTeX compiler: {lualatex_bin}")

    decks_to_run = [target_deck] if target_deck and target_deck in DECK_REGISTRY else list(DECK_REGISTRY.keys())
    results: List[Tuple[str, str, int, int]] = []

    for d_id in decks_to_run:
        pdf_path = compile_slide_deck(d_id, lualatex_bin)
        if pdf_path and pdf_path.exists():
            try:
                import fitz
                doc = fitz.open(pdf_path)
                slide_count = len(doc)
            except Exception:
                slide_count = 0
            size_bytes = pdf_path.stat().st_size
            results.append((d_id, "SUCCESS", slide_count, size_bytes))
        else:
            results.append((d_id, "FAILED", 0, 0))

    print("\n" + "=" * 70)
    print("PRESENTATION BUILD PIPELINE SUMMARY")
    print("=" * 70)
    for d_id, status, slides, size in results:
        status_tag = f"[{status}]"
        print(f"{status_tag:<10} {d_id + '.pdf':<40} | Slides: {slides:>2} | Size: {size:>9,} bytes")

    print("\nAll presentation slide decks generated successfully in:")
    print(f"{OUTPUT_DIR.resolve()}\n")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    generate_all_decks(target)
