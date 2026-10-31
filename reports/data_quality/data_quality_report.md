# Data Quality & Transformation Report

## Executive Summary
- **Total Raw Records Loaded:** 19,925
- **Total Fact Titles Exported:** 19,925 (100% row preservation; no rows discarded)
- **Bridge Genre Pairs:** 41,542
- **Bridge Country Pairs:** 22,410
- **Unique Platform Dimensions:** 3
- **Unique Content Keys Evaluated for Overlap:** 19,684

## Platform Level Summary
| Platform | Raw Rows | Processed Fact Rows | Movies | TV Shows | Missing Country | Missing Date Added | Missing Rating | Short Movies (<=5m) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Netflix** | 8,807 | 8,807 | 6,131 | 2,676 | 831 (9.4%) | 10 (0.1%) | 4 (0.05%) | 2 |
| **Amazon Prime** | 9,668 | 9,668 | 7,814 | 1,854 | 8,996 (93.0%) | 9,513 (98.4%) | 337 (3.5%) | 46 |
| **Disney+** | 1,450 | 1,450 | 1,052 | 398 | 219 (15.1%) | 3 (0.2%) | 3 (0.2%) | 37 |
| **Total** | **19,925** | **19,925** | **14,997** | **4,928** | **10,046** | **9,526** | **344** | **85** |

## Cross-Platform Overlap Summary
- **Distinct Title Keys:** 19,684
- **Titles Available on Multiple Platforms:** 226
  - Netflix & Amazon Prime: 194
  - Netflix & Disney+: 26
  - Amazon Prime & Disney+: 6
  - Across All 3 Platforms: 0

## Cleaning Decisions Log
- **[Netflix] Netflix Rating/Duration Shift Repair:** Moved duration from rating column to duration, set rating to NULL. No rating fabrication. (Affected rows: 3)
- **[Netflix] Standardization & Parsing:** Processed 8807 rows. Parsed dates, separated movie_runtime vs tv_seasons (flagged 2 short movies), mapped rating groups. (Affected rows: 8807)
- **[Amazon Prime] Standardization & Parsing:** Processed 9668 rows. Parsed dates, separated movie_runtime vs tv_seasons (flagged 46 short movies), mapped rating groups. (Affected rows: 9668)
- **[Disney+] Standardization & Parsing:** Processed 1450 rows. Parsed dates, separated movie_runtime vs tv_seasons (flagged 37 short movies), mapped rating groups. (Affected rows: 1450)
