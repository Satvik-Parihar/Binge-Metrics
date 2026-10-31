# Movie and OTT Platform Content Analysis
**Academic Year:** Fourth Year (Semester 7) | Individual Data Science Project  
**Tech Stack:** Python 3.13, Pandas, Matplotlib, Pytest, Power BI Desktop  
**Data Sources:** Netflix, Amazon Prime Video, Disney+ Catalogues (Shivam Bansal / Kaggle)

---

## 📌 Project Overview
This project delivers a complete, reproducible catalogue analysis across three major streaming platforms: **Netflix**, **Amazon Prime Video**, and **Disney+**. Rather than relying on fragile manual dashboard builds or unsubstantiated assumptions about viewership/revenue, the project employs a rigorous data science architecture:
1. **Reproducible Pipeline:** Automated ingestion, cleaning, schema validation, and normalization.
2. **Production Star Schema:** Separation of title entities (`fact_titles`), dimensions (`dim_platform`), cross-platform availability (`title_overlap`), and multi-valued bridges (`bridge_title_genre`, `bridge_title_country`).
3. **Automated Testing Suite:** 8 comprehensive `pytest` test cases enforcing 100% row preservation, shifted-column repair, and cross-platform key merging.
4. **Interactive Dashboard Architecture:** Cinematic dark theme, calibrated DAX measures, and unbiased catalogue composition visualisations.

---

## 📂 Repository & Target Architecture
```
├── original_backup/            # Read-only untouched copy of the original GitHub repo + SHA-256 hashes
├── data/
│   ├── raw/                    # Original unedited CSVs (Netflix, Prime, Disney+)
│   └── processed/              # Clean star-schema CSVs (fact_titles, bridges, dim_platform, title_overlap)
├── reports/data_quality/       # Data quality audit log and before/after transformation impact report
├── src/
│   ├── pipeline/               # clean_data.py (One-command data pipeline)
│   └── analysis/               # generate_metrics_and_charts.py & expected_metrics.json
├── powerbi/
│   └── theme/                  # cinematic_dark_theme.json
├── docs/                       # Comprehensive documentation (measures, methodology, viva, change log)
├── screenshots/                # Validated analytical charts & visual evidence
├── tests/                      # Automated test suite (pytest)
├── requirements.txt            # Minimal, lightweight dependencies
└── README.md
```

---

## 🚀 Step-by-Step Reproduction Guide

### 1. Environment Setup
Install required packages using Python (virtual environment recommended):
```bash
pip install -r requirements.txt
```

### 2. Execute Data Pipeline
Run the reproducible cleaning and transformation pipeline:
```bash
python src/pipeline/clean_data.py
```
*Expected Output:* Generates clean CSVs in `data/processed/` and logs all actions to `reports/data_quality/data_quality_report.md`.

### 3. Compute Metrics & Visual Assets
Generate the ground-truth metrics and backup visual charts:
```bash
python src/analysis/generate_metrics_and_charts.py
```
*Expected Output:* Creates `src/analysis/expected_metrics.json` and exports high-contrast dark-mode charts into `screenshots/`.

### 4. Run Automated QA Tests
Execute the comprehensive test suite:
```bash
pytest -v tests/test_pipeline_and_quality.py
```
*Expected Output:* `8 passed in ~1.5s` confirming all data assertions hold true.

---

## 📊 Summary of Ground-Truth Findings

| Metric | Netflix | Amazon Prime | Disney+ | Combined / Overall |
| :--- | :--- | :--- | :--- | :--- |
| **Total Titles in Fact** | 8,807 | 9,668 | 1,450 | **19,925** |
| **Movies Count (%)** | 6,131 (69.6%) | 7,814 (80.8%) | 1,052 (72.6%) | **14,997 (75.3%)** |
| **TV Shows Count (%)** | 2,676 (30.4%) | 1,854 (19.2%) | 398 (27.4%) | **4,928 (24.7%)** |
| **Median Movie Runtime** | 98.0 min | 94.0 min | 83.0 min | — |
| **Average TV Seasons** | 1.76 seasons | 1.25 seasons | 2.12 seasons | — |
| **Distinct Cross-Platform Content** | — | — | — | **19,705 unique titles** |
| **Titles Shared on Multiple Platforms**| — | — | — | **220 shared titles** |

---

## 🔒 Scope Limitations (Viva Defense)
- **Catalogue Size != Popularity:** Amazon Prime has the largest catalogue (9,668), but this does not imply higher viewership, subscriber base, or revenue.
- **Metadata Missingness:** Amazon Prime is missing ~98.4% of `date_added` and ~93.0% of `country`. Country and catalogue additions cannot be compared directly with Netflix without explicitly identifying missing data.
- **Snapshot Discrepancies:** Snapshots reflect content availability between September and November 2021.

