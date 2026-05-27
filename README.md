# FDA Adverse Event Dashboard

**Built by Muhammad Uzair RPh (PharmD) · University of Peshawar**

An interactive dashboard for exploring FDA Adverse Event Monitoring System (AEMS) data across Q3 2025 – Q1 2026. Built as a Health Informatics portfolio project.

---

## Features

| Tab | What it does |
|---|---|
| 📊 Overview | KPI metrics, drug/reaction charts, age distribution, quarterly trend, stacked age-group chart |
| 🔍 Drug Safety Search | Type any drug name → get full adverse event profile, risk level, age distribution, export |
| ⚡ Drug Comparison | Compare two drugs side by side — reactions, demographics, head-to-head metrics |
| 🚨 High Risk Alerts | All drugs classified as CRITICAL / HIGH / MEDIUM / LOW by report volume percentile |
| 📋 Public Safety Summary | Plain-language summary, top 10 drugs and reactions, demographic breakdown, CSV download |

---

## Tech Stack

- **Python** · **Pandas** · **Plotly** · **Streamlit**
- Data: FDA Adverse Event Monitoring System (AEMS) — Public Dataset

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/medication-error-dashboard
cd medication-error-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download FDA AEMS data

The data files are not included in this repository (too large). Download them from the FDA:

**URL:** https://www.fda.gov/drugs/surveillance/fda-adverse-event-reporting-system-faers

Download the quarterly ZIP files for:
- Q3 2025 (faers_ascii_2025q3.zip)
- Q4 2025 (faers_ascii_2025Q4.zip)
- Q1 2026 (faers_ascii_2026q1.zip)

Extract each ZIP and copy these files into a `data/` folder:
```
data/
├── DEMO25Q3.txt
├── DRUG25Q3.txt
├── REAC25Q3.txt
├── DEMO25Q4.txt
├── DRUG25Q4.txt
├── REAC25Q4.txt
├── DEMO26Q1.txt
├── DRUG26Q1.txt
└── REAC26Q1.txt
```

### 4. Run the dashboard
```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## Author

**Muhammad Uzair RPh (PharmD)**  
University of Peshawar, Pakistan  
Health Informatics Portfolio Project

---

## Data Source

FDA Adverse Event Monitoring System (AEMS) — Publicly available government data.  
https://www.fda.gov/drugs/surveillance/fda-adverse-event-reporting-system-faers
