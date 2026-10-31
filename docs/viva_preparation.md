# College Viva Examination Guide: Questions & Model Answers

This document prepares the student to confidently defend every data engineering, statistical, and architectural decision during their semester viva.

---

### Q1: Why did you convert the raw CSVs into a Star Schema instead of using the raw tables directly in Power BI?
**Answer:**
"Using raw, denormalized CSVs directly creates severe data modeling issues:
1. **Multi-valued fields:** The `listed_in` (genres) and `country` fields contain comma-separated values. Slicing directly on these raw strings creates messy combinations (like `'Comedy, Drama'`). By splitting them into bridge tables (`bridge_title_genre` and `bridge_title_country`), a user can filter by single genres cleanly.
2. **Cardinality & Performance:** A centralized fact table (`fact_titles`) linked to dimension tables (`dim_platform`, `title_overlap`) follows Power BI tabular modeling best practices, optimizing memory compression and making DAX measures simpler and faster.
3. **Cross-Platform Comparison:** Without a unified fact table and an overlap bridge, comparing shared titles across Netflix, Prime, and Disney+ within the same visual would be impossible."

---

### Q2: How did you handle the shifted rows and missing data in the Netflix and Prime datasets?
**Answer:**
"I adhered strictly to the rule of never fabricating data:
1. **Shifted Netflix Rows:** Three titles (`Louis C.K.` comedy specials) had runtime strings like `'74 min'` mistakenly located in the `rating` column while `duration` was empty. My Python pipeline detected this pattern, transferred the runtime string to `duration`, extracted the numeric runtime (74 min), and set `rating` to `NULL`. I did not guess the age rating.
2. **Missing Metadata in Prime:** Amazon Prime has ~98.4% missing `date_added` and ~93% missing `country`. Instead of dropping rows or imputing synthetic values, I created explicit boolean quality flags (`date_added_missing_flag`, `country_missing_flag`) and display labels like `'Unknown'`. In cross-platform comparisons, I used percentages of known data and explicitly displayed missingness."

---

### Q3: How did you match content across platforms to find overlap? What are the risks of false matches?
**Answer:**
"I constructed a deterministic composite key:
$$\text{title\_key} = \text{clean\_title} + \text{'\_' } + \text{type} + \text{'\_' } + \text{release\_year}$$
- The title was normalized by converting to lowercase, stripping punctuation, and compressing excess whitespace.
- Including `type` prevents confusing a film with a television adaptation.
- Including `release_year` prevents conflating original movies with same-titled remakes (e.g., *The Lion King* 1994 vs 2019).
- **Risks & Limitations:**
  - *False Misses:* Subtitle differences (e.g., *'Star Wars: Episode IV'* vs *'Star Wars'*), translation variations, or international release year mismatches ($\pm 1$ year) will result in missing an overlap.
  - *False Matches:* Extremely generic short titles released in the same year could theoretically collide, though combining title, type, and year makes this rare."

---

### Q4: When filtering by genre using the bridge table, why do row counts exceed the total number of titles?
**Answer:**
"This is the difference between counting **titles** versus counting **title-genre associations**:
- In the bridge table, a title categorized under three genres (e.g., Action, Sci-Fi, Thriller) generates 3 rows.
- If you simply execute `COUNTROWS(bridge_title_genre)`, you get 47,000+ association pairs.
- To accurately report distinct titles, our official DAX measure uses:
  $$\text{Total Titles} = \text{DISTINCTCOUNT(fact\_titles[platform\_title\_id])}$$
  This ensures that even when filtering by multiple genres, titles are never double-counted."

---

### Q5: Amazon Prime has 9,668 titles while Disney+ has only 1,450. Can we conclude that Amazon Prime is a better or more popular streaming platform?
**Answer:**
"**No, absolutely not.** Our analysis is strictly a **catalogue inventory analysis**, not a market share, audience viewership, or content quality analysis:
1. **No Viewership Data:** Our dataset contains no subscriber numbers, view counts, or box-office revenue.
2. **Library Strategy:** Amazon Prime maintains a large volume of independent, niche, and legacy films, whereas Disney+ focuses on high-production-value, proprietary family IP (Disney, Pixar, Marvel, Star Wars). A larger catalogue simply reflects licensing volume, not consumer preference."

---

### Q6: Why did you re-label the third platform as Disney+ instead of Disney Plus Hotstar?
**Answer:**
"In the original GitHub project, the platform was labelled 'Hotstar' and used the Indian Star/Hotstar logo. However, when I audited the geographical metadata of the `disney_plus_titles.csv` file:
- **1,184 out of 1,450 titles (81.7%)** originated from the **United States**.
- Only **5 titles (0.3%)** originated from **India**.
The dataset corresponds to the global/US launch of Disney+. Labelling it as Hotstar was factually inaccurate. Labelling it as Disney+ ensures complete academic truthfulness."

