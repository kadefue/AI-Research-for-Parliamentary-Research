# AI Research for Parliamentary Research
## Sokoine University of Agriculture (SUA) \textbullet{} AB Consult

Official training manuals, curriculum outlines, and automated generation scripts for the 5-day executive capacity-building program: **Application of Artificial Intelligence in Parliamentary Research (Zero-Copy Desktop Ingestion)**.

---

## 🏛️ Program Institutional Metadata

- **Institution:** Sokoine University of Agriculture (SUA), Morogoro, Tanzania
- **College:** College of Economics and Business Studies (COEBS)
- **Consultancy Unit:** AB Consult
- **Lead Technical Facilitator:** Eng. Dr. Kadeghe Fue, PhD (Senior AI & Systems Consultant)
- **Target Trainees:** Parliamentary Researchers, Standing Committee Clerks, Legislators, Social & Political Scientists, Policy Analysts
- **Official Palette:** Tanzanian Blue (`#0066B2`), Tanzanian Yellow/Gold (`#FCD116`), and SUA Green (`#00703C`)
- **Institutional Emblems:** SUA Crest (Header Left) & Tanzanian National Coat of Arms (Header Right)

---

## 📁 Repository Directory Structure

```text
.
├── Logo/                               # Institutional Logos & Official Emblems
│   ├── SUA.png                         # Sokoine University of Agriculture Crest
│   ├── Coat_of_arms_of_Tanzania.svg    # Official Tanzanian Coat of Arms (Vector)
│   ├── Coat_of_arms_of_Tanzania.png    # 300 DPI High-Res Converted PNG
│   └── Coat_of_arms_of_Tanzania.pdf    # Vector PDF Format
├── Raw_Files/                          # Original Raw LaTeX Manuals & Reference PDFs
│   ├── day_1_training_manual.tex
│   ├── day_2_training_manual.tex
│   ├── day_3_training_manual.tex
│   ├── day_4_training_manual.tex
│   ├── day_5_training_manual.tex
│   ├── executive_training_outline.tex
│   └── master_parliamentary_ai_training_manual.tex
├── Scripts/                            # Core Automation & Generation Scripts
│   ├── build_figures.py                # Generates 17 publication-grade figures & diagrams
│   └── build_training.py               # Rectifies raw files and compiles official manuals
├── Training_Materials/                 # Output Deliverables
│   ├── figures/                        # 300 DPI Figures, Flowcharts & Architecture Charts
│   └── Training_Manuals/               # Final Compiled Government-Formatted Documents
│       ├── day_1_training_manual.pdf
│       ├── day_2_training_manual.pdf
│       ├── day_3_training_manual.pdf
│       ├── day_4_training_manual.pdf
│       ├── day_5_training_manual.pdf
│       ├── executive_training_outline.pdf
│       └── master_parliamentary_ai_training_manual.pdf
├── build_figures.py                    # Root wrapper symlink for ease of execution
└── build_training.py                   # Root wrapper symlink for ease of execution
```

---

## 🚀 Execution Instructions

### 1. Generate Figures
To regenerate all 17 high-resolution diagrams, flowcharts, and comparative tables:
```bash
python3 build_figures.py
# or
python3 Scripts/build_figures.py Training_Materials/figures
```

### 2. Rectify Raw Files & Build Official Government Manuals
To rectify all raw files, embed official headers (SUA on left, Coat of Arms on right), apply the Tanzanian color strips (Blue, Yellow, Green), replace placeholder frameboxes with publication-grade figures, and compile the final PDF documents:
```bash
python3 build_training.py
# or
python3 Scripts/build_training.py
```

All compiled PDFs and rectified `.tex` source files will be generated into [`Training_Materials/Training_Manuals/`](Training_Materials/Training_Manuals/).

---

## 📊 Summary of Generated Deliverables

| Deliverable File | Target Audience & Module | Pages | Status |
| :--- | :--- | :---: | :---: |
| **`executive_training_outline.pdf`** | Speaker, Committee Chairs & Trainees (Course Overview) | 3 | Verified |
| **`day_1_training_manual.pdf`** | Day 1: Automated Native File Ingestion in VS Code | 13 | Verified |
| **`day_2_training_manual.pdf`** | Day 2: CLEAR Scrutiny Protocol, Bill Amendments & CAG Audits | 15 | Verified |
| **`day_3_training_manual.pdf`** | Day 3: Statistical Abstracts, Split Fact-Checking & FYDP III | 15 | Verified |
| **`day_4_training_manual.pdf`** | Day 4: 4-Pillar MCPA, 4-Way Stakeholder Simulation & Options | 17 | Verified |
| **`day_5_training_manual.pdf`** | Day 5: Multi-Doc Corpus Ingestion & Tripartite Deliverables | 19 | Verified |
| **`master_parliamentary_ai_training_manual.pdf`** | Master 5-Day Unified Manual & Research Desk Blueprint | 15 | Verified |
