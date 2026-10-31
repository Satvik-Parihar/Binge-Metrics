# Methodology, Analytical Findings & Limitations Report

---

## 1. Research Methodology
The goal of this study is to perform an objective, reproducible content catalogue analysis of three major OTT streaming providers: **Netflix**, **Amazon Prime Video**, and **Disney+**.

### Data Ingestion & Engineering Pipeline
1. **Raw Snapshot Audit:** Datasets compiled by Shivam Bansal from public OTT library listings up to Autumn 2021 were ingested into `data/raw/`.
2. **Deterministic Cleansing (`clean_data.py`):**
   - 100% row preservation across all three platforms ($N = 19,925$).
   - Exact regex repair of shifted duration strings into runtime minutes for Netflix (`s5542`, `s5795`, `s5814`), leaving age ratings as verifiable `NULL` without synthetic imputation.
   - Separate duration tracking: `movie_runtime_minutes` (Movies) vs `tv_seasons` (TV Shows).
   - Flagged 85 anomalous short films ($\le 5$ min) with `suspicious_short_runtime_flag` to protect median runtime metrics without discarding raw catalogue records.
   - Standardized rating groups (`Kids`, `Family`, `Teen`, `Mature`, `Unrated`, `Unknown`).
   - Split multi-valued fields into normalized relational bridges: `bridge_title_genre` (47,000+ pairs) and `bridge_title_country` (24,000+ pairs).
   - Constructed exact matching keys: $\text{norm\_title} + \text{'\_'} + \text{type} + \text{'\_'} + \text{release\_year}$.

---

## 2. Key Verified Findings

### A. Catalogue Volume & Composition
- **[Observed Fact]** Amazon Prime Video possesses the largest catalogue ($9,668$ titles), followed by Netflix ($8,807$ titles) and Disney+ ($1,450$ titles).
- **[Calculated Statistic]** Movies dominate across all three platforms:
  - Amazon Prime: **80.8% Movies** / 19.2% TV Shows
  - Disney+: **72.6% Movies** / 27.4% TV Shows
  - Netflix: **69.6% Movies** / 30.4% TV Shows
- **[Interpretation]** Netflix maintains the highest proportion of episodic series (TV Shows) at 30.4%, reflecting its strategic investment in bingeable serialized programming compared to Amazon Prime's high-volume movie repository.

### B. Content Age & Production Year Trends
- **[Calculated Statistic]** Over 75% of content on all three platforms was produced between **2015 and 2021**.
- **[Observed Fact]** Content additions peak dramatically around 2018–2020 before tapering slightly in 2021 due to snapshot cutoff dates (Sep–Nov 2021) and pandemic-related production delays.

### C. Feature Film Runtime & TV Longevity
- **[Calculated Statistic]** The median movie runtimes (excluding $\le 5$ min anomalies) are:
  - Netflix: **98.0 minutes**
  - Amazon Prime Video: **94.0 minutes**
  - Disney+: **83.0 minutes**
- **[Interpretation]** Disney+'s significantly lower median runtime (83 minutes) is directly attributable to its animated catalogue and classic family features, whereas Netflix and Prime feature longer contemporary feature films.
- **[Calculated Statistic]** The average TV series length is:
  - Disney+: **2.12 seasons**
  - Netflix: **1.76 seasons**
  - Amazon Prime Video: **1.25 seasons**

### D. Cross-Platform Exclusivity & Overlap
- **[Calculated Statistic]** Out of 19,705 unique titles evaluated across all platforms:
  - **19,485 titles (98.9%)** are completely exclusive to a single platform.
  - Only **220 titles (1.1%)** appear simultaneously on multiple services.
- **[Calculated Statistic]** Overlap breakdown:
  - Netflix & Amazon Prime Video: **194 shared titles**
  - Netflix & Disney+: **26 shared titles**
  - Amazon Prime & Disney+: **6 shared titles**
  - All Three Services Simultaneously: **0 titles**
- **[Interpretation]** Streaming platforms operate as highly closed content silos, relying heavily on original IP and exclusive licensing agreements.

---

## 3. Analytical Limitations

1. **Snapshot Timeliness:** All three catalogues represent snapshots ending in late 2021 (Netflix Sep 2021, Prime Oct 2021, Disney+ Nov 2021). Content licensed or produced after 2021 is not present.
2. **Metadata Incompleteness on Amazon Prime:** Amazon Prime has ~98.4% missing `date_added` and ~93% missing `country`. Geographical analyses and library intake velocity cannot be compared against Netflix without noting missingness.
3. **Cross-Platform Matching Conservatism:** The exact matching algorithm requires identical normalized title, type, and release year. Titles with localized naming differences or $\pm 1$ international release variance will count as distinct exclusive titles.
4. **Catalogue Size vs Business Success:** This is an inventory composition study. A larger library does not equate to higher viewership, customer satisfaction, or financial profitability.

