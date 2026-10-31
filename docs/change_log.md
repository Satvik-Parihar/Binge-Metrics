# Project Change Log: Starter vs. Final Production Architecture

This document logs every architectural, pipeline, and visual decision made between the original starter repository (`NikitaPande13/OTT-Power-BI-Dashboard`) and this production academic project.

---

## 1. What Was Preserved
- **Core Raw Datasets:** Kept the original snapshot datasets for Netflix, Amazon Prime, and Disney+ intact in `original_backup/` and `data/raw/` with verified cryptographic hashes.
- **Foundational Concepts:** Preserved the concept of analyzing OTT library composition by Content Type (Movies vs TV Shows), Genre distribution, and Release Year.
- **Multi-Platform Focus:** Kept the cross-platform lens across Netflix, Amazon Prime, and Disney+.

---

## 2. What Was Fixed / Re-Architected

| Issue in Starter Repo | Root Cause | Engineering Solution in Production | Justification |
| :--- | :--- | :--- | :--- |
| **Netflix Discrepancy (8,809 vs 8,807)** | Screenshot showed 8,809 titles, whereas raw CSV only contains 8,807 distinct rows. | Enforced distinct primary key identification (`platform_title_id`) and automated validation checks. | Ensures 100% mathematical integrity in viva. |
| **Shifted Rating/Duration Rows** | 3 Louis C.K. titles on Netflix had runtimes ('74 min', etc.) in the `rating` column and empty `duration`. | Implemented regex-based automated repair in `clean_data.py` to move values to duration and set rating to NULL. | Prevents corrupted rating distributions without fabricating missing data. |
| **Mislabelled Release Trend Line Chart** | Line chart on Netflix/Disney pages was bound to `date_added.Year` instead of `release_year`, mixing up library licensing year with production year. | Standardized trend analysis on `release_year`. Separated `date_added` into a catalogue intake dimension. | Content released in 1990 added to Netflix in 2020 was falsely shown as 2020 production in the starter report. |
| **Raw Multi-Valued Slicers** | Genre slicers used unseparated strings (`listed_in`), presenting comma-separated combinations. | Created a normalized `bridge_title_genre` table with an overarching `genre_group` taxonomy. | Allows students and users to filter cleanly by single genres (e.g., "Comedy" or "Drama"). |
| **Misleading "Hotstar" Label & Logo** | Starter repo labelled Disney+ as "Hotstar" using the Indian Hotstar logo, despite 81.7% of content being from the United States. | Re-labelled platform honestly as **"Disney+"** and removed proprietary logos in favor of clean accessible styling. | Accurate data provenance and ethical copyright compliance. |
| **Missing Cross-Platform Overlap** | No relationship or comparison existed across the three platforms. | Implemented `title_overlap` dimension using normalized title keys (`norm_title + type + release_year`). | Reveals catalogue exclusivity, showing that 19,705 out of 19,925 titles are exclusive. |
| **Fragile Absolute File Paths** | Legacy Power BI queries used machine-specific local paths that break on new machines. | Provided standardized relative CSV structures and export parameters. | Ensures the report can be opened and refreshed seamlessly on any computer. |

