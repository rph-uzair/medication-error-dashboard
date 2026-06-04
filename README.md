<div align="center">

# 💊 FDA Adverse Event Dashboard

### A Clinical Data Intelligence Platform for Drug Safety Analysis

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.57-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![FDA Data](https://img.shields.io/badge/FDA-AEMS%20Public%20Data-0064A4?style=for-the-badge)](https://www.fda.gov)
[![Records](https://img.shields.io/badge/Dataset-2.6M%2B%20Records-10B981?style=for-the-badge)](https://github.com/rph-uzair/medication-error-dashboard)

<br>

### 🚀 [**LAUNCH LIVE DEMO →**](https://medication-error-dashboard-d8tfd9qbxwpzwgrsf5wzf9.streamlit.app)

*Live demo runs on 300K records (cloud memory limit) · Full 2.6M record dataset runs on local deployment*

<br>

**Built by [Muhammad Uzair RPh (PharmD)](https://github.com/rph-uzair) · University of Peshawar, Pakistan**  
*Health Informatics Portfolio Project · FDA Adverse Event Monitoring System (AEMS) · Q3 2025 – Q1 2026*

</div>

---

## 📌 Overview

This dashboard provides an interactive, multi-dimensional analysis of **2,647,622 FDA adverse event reports** spanning three quarters of real government pharmacovigilance data. Built as a portfolio project demonstrating the intersection of clinical pharmacy knowledge and health informatics, it enables researchers, clinicians, and public health professionals to explore drug safety patterns across demographics, time periods, and risk categories.

The project combines a **PharmD clinical background** with applied data science — producing a tool that is both technically rigorous and clinically meaningful.

---

## 🎯 Key Features

| Tab | Feature | Description |
|---|---|---|
| 📊 | **Overview** | 6 interactive charts — drug volumes, age distribution, reaction patterns, gender split, quarterly trends, stacked age-group analysis |
| 🔍 | **Drug Safety Search** | Real-time drug lookup with full adverse event profile, risk classification, demographic breakdown, and CSV export |
| ⚡ | **Drug Comparison** | Side-by-side comparison of any two drugs — reactions, demographics, head-to-head metrics table |
| 🚨 | **High Risk Alerts** | Automated risk classification (CRITICAL/HIGH/MEDIUM/LOW) based on report volume percentiles across 5,220 unique drugs |
| 📋 | **Public Safety Summary** | Plain-language public health report with top 10 drugs, top 10 reactions, demographic breakdown, and full dataset export |

---

## 📊 Dataset

| Attribute | Value |
|---|---|
| **Source** | FDA Adverse Event Monitoring System (AEMS) — Public Dataset |
| **Period** | Q3 2025 (Jul–Sep) · Q4 2025 (Oct–Dec) · Q1 2026 (Jan–Mar) |
| **Total Records** | **2,647,622** adverse event reports |
| **Unique Drugs** | 5,220 distinct drug substances |
| **Unique Reactions** | 14,339 distinct adverse reactions |
| **Files** | 9 raw `.txt` files — DEMO, DRUG, REAC for each quarter |
| **Download** | [FDA AEMS Quarterly Data Files](https://www.fda.gov/drugs/surveillance/fda-adverse-event-reporting-system-faers) |

> **Cloud Demo Note:** The live demo loads 300,000 records due to free-tier cloud memory constraints (1GB). The full 2,647,622-record dataset runs completely on local deployment. All features are identical on both versions.

---

## 🖥️ Screenshots

### Overview — Drug Reporting Patterns
![Overview Tab](screenshots/overview.png)

### Drug Safety Search
![Drug Safety Search](screenshots/drug_search.png)

### High Risk Alerts
![High Risk Alerts](screenshots/high_risk.png)

### Drug Comparison
![Drug Comparison](screenshots/comparison.png)

---

## 🛠️ Tech Stack

```
Language      Python 3.11+
Framework     Streamlit 1.57
Visualization Plotly (Graph Objects)
Data          Pandas, NumPy
Data Source   FDA AEMS Public Dataset (government open data)
Deployment    Streamlit Cloud (demo) · Local (full dataset)
```

---

## ⚙️ Local Setup — Full 2.6M Record Version

### 1. Clone the repository
```bash
git clone https://github.com/rph-uzair/medication-error-dashboard
cd medication-error-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the full FDA dataset

Download these quarterly ZIP files from the FDA:
**→ https://www.fda.gov/drugs/surveillance/fda-adverse-event-reporting-system-faers**

| Quarter | File |
|---|---|
| Q3 2025 | `faers_ascii_2025q3.zip` |
| Q4 2025 | `faers_ascii_2025Q4.zip` |
| Q1 2026 | `faers_ascii_2026q1.zip` |

Extract and place these 9 files into a `data/` folder:

```
data/
├── DEMO25Q3.txt    DEMO25Q4.txt    DEMO26Q1.txt
├── DRUG25Q3.txt    DRUG25Q4.txt    DRUG26Q1.txt
└── REAC25Q3.txt    REAC25Q4.txt    REAC26Q1.txt
```

### 4. Enable full dataset (remove row limit)

In `app.py`, find the `load()` function and remove `nrows=100000` from all three `pd.read_csv()` calls. This enables the complete 2,647,622 record dataset.

### 5. Run
```bash
streamlit run app.py
```

Open → **http://localhost:8501**

---

## 📁 Repository Structure

```
medication-error-dashboard/
│
├── app.py                 # Main dashboard application (917 lines)
├── requirements.txt       # Python dependencies
├── slim_drug_files.py     # Utility: compress DRUG files for deployment
├── README.md              # This file
├── .gitignore             # Excludes large data files from version control
│
└── data/                  # FDA AEMS data files (download separately)
    ├── DEMO25Q3.txt · DEMO25Q4.txt · DEMO26Q1.txt
    ├── DRUG25Q3.txt · DRUG25Q4.txt · DRUG26Q1.txt
    └── REAC25Q3.txt · REAC25Q4.txt · REAC26Q1.txt
```

---

## 🔬 Clinical Motivation

During two clinical pharmacy internships, I observed that medication decisions — reconciliation, adverse event monitoring, drug interaction screening — were still handled manually in most settings, without the data systems that exist elsewhere. This dashboard is a direct response to that gap: demonstrating what pharmacovigilance looks like when clinical knowledge meets informatics tools.

The choice of the FDA AEMS dataset was deliberate. It is the world's largest pharmacovigilance database, and analyzing it requires understanding both the technical structure of healthcare data (ICD codes, MedDRA terminology, EHR-linked reports) and the clinical significance of what the numbers represent.

---

## 👨‍⚕️ Author

**Muhammad Uzair RPh (PharmD)**  
Doctor of Pharmacy · University of Peshawar, Pakistan  
2× Clinical Internships · 1× Industrial Internship  

[![GitHub](https://img.shields.io/badge/GitHub-rph--uzair-181717?style=flat&logo=github)](https://github.com/rph-uzair)
www.linkedin.com/in/muhammad-uzair-rph-891278384
---

## 📄 Data License

Data sourced from the FDA Adverse Event Monitoring System (AEMS) — a publicly available US government dataset. Free to use for research and educational purposes.

---

<div align="center">
<i>Built with Python · Pandas · Plotly · Streamlit · FDA Open Data</i>
</div>
