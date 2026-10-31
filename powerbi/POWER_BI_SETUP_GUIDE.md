# Step-by-Step Power BI Setup & Verification Guide

This guide provides exact, numbered steps for setting up or refreshing the **Movie and OTT Platform Content Analysis** dashboard in Power BI Desktop on Windows.

---

## 1. Quick Data Refresh via CSVs
All cleaned, star-schema CSV tables are located in the relative directory:
`data/processed/`
- `fact_titles.csv` (19,925 rows)
- `dim_platform.csv` (3 rows)
- `title_overlap.csv` (19,705 rows)
- `bridge_title_genre.csv` (47,000+ rows)
- `bridge_title_country.csv` (24,000+ rows)

---

## 2. Setting Up in Power BI Desktop

### Step 1: Open Power BI Desktop
1. Click the Windows Start menu.
2. Type `Power BI Desktop` and press Enter.

### Step 2: Import the Processed CSVs
1. On the **Home** ribbon, click **Get Data** > **Text/CSV**.
2. Navigate to your project folder:
   `c:\Users\vedan\OneDrive\Documents\LJIET\Fourth Year\SEM - 7\Individual Project\data\processed\`
3. Select `fact_titles.csv` and click **Load**.
4. Repeat for the remaining files:
   - `dim_platform.csv`
   - `title_overlap.csv`
   - `bridge_title_genre.csv`
   - `bridge_title_country.csv`

### Step 3: Verify Relationships (Model View)
1. Click the **Model view** icon on the left-hand navigation pane.
2. Verify or create the following relationships:
   - `dim_platform[platform_id]` (1) to `fact_titles[platform_id]` (*)
   - `fact_titles[title_key]` (*) to `title_overlap[title_key]` (1)
   - `fact_titles[platform_title_id]` (1) to `bridge_title_genre[platform_title_id]` (*) [Cross filter: Both]
   - `fact_titles[platform_title_id]` (1) to `bridge_title_country[platform_title_id]` (*) [Cross filter: Both]

### Step 4: Import the Dark Cinematic Theme
1. Switch to **Report view** on the left pane.
2. Go to the **View** ribbon at the top.
3. Click the **Themes** dropdown (arrow) and select **Browse for themes**.
4. Navigate to:
   `powerbi\theme\cinematic_dark_theme.json`
5. Click **Open**. Power BI will apply the dark palette and accessible visual styles immediately.

### Step 5: Add Production DAX Measures
1. On the **Modeling** ribbon, click **New Measure**.
2. Copy and paste each formula from [measures.md](file:///c:/Users/vedan/OneDrive/Documents/LJIET/Fourth%20Year/SEM%20-%207/Individual%20Project/docs/measures.md):
   - `Total Titles = DISTINCTCOUNT(fact_titles[platform_title_id])`
   - `Total Movies = CALCULATE(DISTINCTCOUNT(fact_titles[platform_title_id]), fact_titles[type] = "Movie")`
   - `Total TV Shows = CALCULATE(DISTINCTCOUNT(fact_titles[platform_title_id]), fact_titles[type] = "TV Show")`
   - `% Movies = DIVIDE([Total Movies], [Total Titles], 0)`
   - `% TV Shows = DIVIDE([Total TV Shows], [Total Titles], 0)`

---

## 3. Verification Checklist against Ground Truth
Compare your card and chart values against `src/analysis/expected_metrics.json`:
- **Overall Total Titles:** 19,925
- **Netflix Titles:** 8,807 (6,131 Movies, 2,676 TV Shows)
- **Amazon Prime Titles:** 9,668 (7,814 Movies, 1,854 TV Shows)
- **Disney+ Titles:** 1,450 (1,052 Movies, 398 TV Shows)
- **Cross-Platform Shared Titles:** 220

