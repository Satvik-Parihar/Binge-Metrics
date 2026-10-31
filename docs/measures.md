# Power BI DAX Measures & Star Schema Documentation

This document defines the production star-schema relationships and official DAX measures created for the **Movie and OTT Platform Content Analysis** dashboard.

---

## 1. Star Schema Architecture

```
         +-----------------------+
         |     dim_platform      |
         +-----------------------+
         | platform_id (PK)      |
         | platform_name         |
         | catalogue_code        |
         +-----------+-----------+
                     | 1
                     |
                     | *
+--------------------+---------------------+      1 +------------------------+
|                   fact_titles            +--------+     title_overlap      |
+------------------------------------------+        +------------------------+
| platform_title_id (PK)                   |        | title_key (PK)         |
| platform_id (FK)                         |        | platform_count         |
| platform_name                            |        | on_netflix             |
| title_key (FK)                           |        | on_amazon_prime        |
| title                                    |        | on_disney_plus         |
| type (Movie / TV Show)                   |        | shared_flag            |
| release_year                             |        +------------------------+
| movie_runtime_minutes                    |
| tv_seasons                               |
| rating_group                             |
| suspicious_short_runtime_flag            |
+--------------------+---------------------+
                     | 1
                     |
         +-----------+-----------+
         | *                     | *
+--------+---------------+ +-----+-----------------+
|   bridge_title_genre   | |  bridge_title_country |
+------------------------+ +-----------------------+
| platform_title_id (FK) | | platform_title_id (FK)|
| genre_raw              | | country_raw           |
| genre_group            | +-----------------------+
+------------------------+
```

### Relationship Specifications:
1. `dim_platform[platform_id]` (1) -> `fact_titles[platform_id]` (\*): Single directional (dim filters fact).
2. `fact_titles[title_key]` (\*) -> `title_overlap[title_key]` (1): Bi-directional or Single (enables filtering by cross-platform availability).
3. `fact_titles[platform_title_id]` (1) -> `bridge_title_genre[platform_title_id]` (\*): Bi-directional (allows genre filtering on titles).
4. `fact_titles[platform_title_id]` (1) -> `bridge_title_country[platform_title_id]` (\*): Bi-directional (allows country filtering on titles).

---

## 2. Production DAX Measures Reference

### Measure 1: Total Platform Titles
- **DAX Formula:**
  ```dax
  Total Titles = DISTINCTCOUNT(fact_titles[platform_title_id])
  ```
- **Description:** Counts the distinct number of titles in the current filter context at the platform-title level.
- **Fields Used:** `fact_titles[platform_title_id]`
- **Limitations:** Multi-platform titles are counted independently per platform.

---

### Measure 2: Total Movies
- **DAX Formula:**
  ```dax
  Total Movies = CALCULATE(DISTINCTCOUNT(fact_titles[platform_title_id]), fact_titles[type] = "Movie")
  ```
- **Description:** Count of film productions.
- **Fields Used:** `fact_titles[platform_title_id]`, `fact_titles[type]`

---

### Measure 3: Total TV Shows
- **DAX Formula:**
  ```dax
  Total TV Shows = CALCULATE(DISTINCTCOUNT(fact_titles[platform_title_id]), fact_titles[type] = "TV Show")
  ```
- **Description:** Count of episodic series productions.
- **Fields Used:** `fact_titles[platform_title_id]`, `fact_titles[type]`

---

### Measure 4: % Movies & % TV Shows
- **DAX Formula:**
  ```dax
  % Movies = DIVIDE([Total Movies], [Total Titles], 0)
  ```
  ```dax
  % TV Shows = DIVIDE([Total TV Shows], [Total Titles], 0)
  ```
- **Format:** Percentage (`0.0%`)
- **Description:** Proportion of current catalogue dedicated to movies vs series.

---

### Measure 5: Distinct Content Across Platforms
- **DAX Formula:**
  ```dax
  Distinct Content Count = DISTINCTCOUNT(fact_titles[title_key])
  ```
- **Description:** Counts unique content productions across the streaming landscape (deduplicating identical titles shared across services).
- **Matching Logic:** `clean_title + type + release_year`.

---

### Measure 6: Titles on Multiple Platforms
- **DAX Formula:**
  ```dax
  Shared Titles Count = CALCULATE(DISTINCTCOUNT(title_overlap[title_key]), title_overlap[shared_flag] = 1)
  ```
- **Description:** Count of distinct productions licensed on more than one OTT service simultaneously.

---

### Measure 7: Median Movie Runtime (Quality Controlled)
- **DAX Formula:**
  ```dax
  Median Movie Runtime = 
  CALCULATE(
      MEDIAN(fact_titles[movie_runtime_minutes]),
      fact_titles[type] = "Movie",
      fact_titles[suspicious_short_runtime_flag] = 0
  )
  ```
- **Description:** Robust central tendency of feature film duration, cleanly excluding erroneous 0-5 minute placeholders without discarding the raw records.

---

### Measure 8: Average TV Seasons
- **DAX Formula:**
  ```dax
  Average TV Seasons = 
  CALCULATE(
      AVERAGE(fact_titles[tv_seasons]),
      fact_titles[type] = "TV Show"
  )
  ```
- **Format:** Decimal (`0.0`)
- **Description:** Average lifecycle / longevity of episodic series.

---

### Measure 9: Titles Count Through Bridge (Pair Count Caveat)
- **DAX Formula:**
  ```dax
  Title Genre Associations = COUNTROWS(bridge_title_genre)
  ```
- **Caveat for Viva:** When slicing by raw genre or country, a single movie associated with 3 genres generates 3 association records. Always use `[Total Titles]` (`DISTINCTCOUNT`) to count distinct titles, and use `COUNTROWS(bridge)` when reporting tag frequency.

