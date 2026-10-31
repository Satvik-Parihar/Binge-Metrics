"""
Phase 5: Analysis & Expected Metrics Computation.
Computes ground truth statistics and outputs expected_metrics.json.
Generates standalone backup charts for visual validation.
"""

import json
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def compute_metrics():
    print("Loading processed star-schema tables...")
    fact = pd.read_csv('data/processed/fact_titles.csv')
    bridge_genre = pd.read_csv('data/processed/bridge_title_genre.csv')
    bridge_country = pd.read_csv('data/processed/bridge_title_country.csv')
    overlap = pd.read_csv('data/processed/title_overlap.csv')
    dim_platform = pd.read_csv('data/processed/dim_platform.csv')
    
    # 1. Platform-level KPIs
    metrics = {
        "dataset_snapshot_limits": {
            "Netflix": "Snapshot up to Sep 2021",
            "Amazon Prime": "Snapshot up to Oct 2021 (98% missing date_added, 93% missing country)",
            "Disney+": "Snapshot up to Nov 2021 (Disney+ US/Global library, not Hotstar)"
        },
        "overall": {
            "total_titles_in_fact": int(len(fact)),
            "distinct_cross_platform_title_keys": int(fact['title_key'].nunique()),
            "total_movies": int((fact['type'] == 'Movie').sum()),
            "total_tv_shows": int((fact['type'] == 'TV Show').sum()),
            "pct_movies": round(float((fact['type'] == 'Movie').sum() / len(fact) * 100), 2),
            "pct_tv_shows": round(float((fact['type'] == 'TV Show').sum() / len(fact) * 100), 2),
            "platforms_represented": int(fact['platform_name'].nunique())
        },
        "platforms": {},
        "runtime_statistics": {},
        "overlap_statistics": {}
    }
    
    for p in ['Netflix', 'Amazon Prime', 'Disney+']:
        p_df = fact[fact['platform_name'] == p]
        n_tot = len(p_df)
        n_mov = int((p_df['type'] == 'Movie').sum())
        n_tv = int((p_df['type'] == 'TV Show').sum())
        
        # Valid movie runtimes (> 5 min)
        valid_movies = p_df[(p_df['type'] == 'Movie') & (p_df['suspicious_short_runtime_flag'] == 0)]
        median_runtime = float(valid_movies['movie_runtime_minutes'].median()) if len(valid_movies) > 0 else 0.0
        
        # TV seasons
        tv_shows = p_df[p_df['type'] == 'TV Show']
        avg_seasons = float(round(tv_shows['tv_seasons'].mean(), 2)) if len(tv_shows) > 0 else 0.0
        
        metrics["platforms"][p] = {
            "total_titles": n_tot,
            "movies": n_mov,
            "tv_shows": n_tv,
            "pct_movies": round(float(n_mov / n_tot * 100), 2),
            "pct_tv_shows": round(float(n_tv / n_tot * 100), 2),
            "median_movie_runtime_min": median_runtime,
            "avg_tv_seasons": avg_seasons,
            "missing_country_pct": round(float(p_df['country_missing_flag'].sum() / n_tot * 100), 2),
            "missing_date_added_pct": round(float(p_df['date_added_missing_flag'].sum() / n_tot * 100), 2)
        }
        
    # Overlap metrics
    n_shared = int(overlap['shared_flag'].sum())
    np_shared = int(((overlap['on_netflix'] == 1) & (overlap['on_amazon_prime'] == 1)).sum())
    nd_shared = int(((overlap['on_netflix'] == 1) & (overlap['on_disney_plus'] == 1)).sum())
    pd_shared = int(((overlap['on_amazon_prime'] == 1) & (overlap['on_disney_plus'] == 1)).sum())
    all3_shared = int(((overlap['on_netflix'] == 1) & (overlap['on_amazon_prime'] == 1) & (overlap['on_disney_plus'] == 1)).sum())
    
    metrics["overlap_statistics"] = {
        "titles_on_multiple_platforms": n_shared,
        "shared_netflix_and_prime": np_shared,
        "shared_netflix_and_disney": nd_shared,
        "shared_prime_and_disney": pd_shared,
        "shared_all_three": all3_shared,
        "unique_to_netflix": int(((overlap['on_netflix'] == 1) & (overlap['platform_count'] == 1)).sum()),
        "unique_to_amazon_prime": int(((overlap['on_amazon_prime'] == 1) & (overlap['platform_count'] == 1)).sum()),
        "unique_to_disney_plus": int(((overlap['on_disney_plus'] == 1) & (overlap['platform_count'] == 1)).sum())
    }
    
    os.makedirs('src/analysis', exist_ok=True)
    with open('src/analysis/expected_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=4)
        
    print("Saved expected_metrics.json successfully!")
    return metrics

def generate_backup_charts():
    print("Generating backup visual charts in screenshots/...")
    fact = pd.read_csv('data/processed/fact_titles.csv')
    bridge_genre = pd.read_csv('data/processed/bridge_title_genre.csv')
    overlap = pd.read_csv('data/processed/title_overlap.csv')
    
    # Platform Palette: Netflix (Red #E50914), Prime (Blue #00A8E1), Disney+ (Teal/Navy #113CCF)
    colors = {'Netflix': '#E50914', 'Amazon Prime': '#00A8E1', 'Disney+': '#113CCF'}
    
    # 1. Content Composition Chart (100% Stacked Bar)
    plt.figure(figsize=(8, 4.5), facecolor='#141414')
    ax = plt.subplot(111)
    ax.set_facecolor('#1F1F1F')
    
    platforms = ['Netflix', 'Amazon Prime', 'Disney+']
    movie_pcts = []
    tv_pcts = []
    for p in platforms:
        pdf = fact[fact['platform_name'] == p]
        tot = len(pdf)
        movie_pcts.append((pdf['type'] == 'Movie').sum() / tot * 100)
        tv_pcts.append((pdf['type'] == 'TV Show').sum() / tot * 100)
        
    y_pos = range(len(platforms))
    ax.barh(y_pos, movie_pcts, color='#C8102E', label='Movies', height=0.55)
    ax.barh(y_pos, tv_pcts, left=movie_pcts, color='#C9A227', label='TV Shows', height=0.55)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(platforms, color='#EAEAEA', fontsize=11, fontweight='bold')
    ax.tick_params(axis='x', colors='#EAEAEA')
    ax.set_xlabel('Percentage of Catalogue (%)', color='#EAEAEA', fontsize=11)
    ax.set_title('Catalogue Composition: Movies vs TV Shows by Platform', color='#FFFFFF', fontsize=13, pad=15)
    ax.legend(facecolor='#1F1F1F', edgecolor='none', labelcolor='#EAEAEA', loc='upper right')
    
    for i in range(len(platforms)):
        ax.text(movie_pcts[i] / 2, i, f"{movie_pcts[i]:.1f}%", va='center', ha='center', color='#FFFFFF', fontweight='bold')
        ax.text(movie_pcts[i] + tv_pcts[i] / 2, i, f"{tv_pcts[i]:.1f}%", va='center', ha='center', color='#141414', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig('screenshots/01_catalogue_composition.png', dpi=150)
    plt.close()
    
    # 2. Release Year Trend (1990 - 2021)
    plt.figure(figsize=(9, 4.5), facecolor='#141414')
    ax = plt.subplot(111)
    ax.set_facecolor('#1F1F1F')
    
    modern = fact[(fact['release_year'] >= 1990) & (fact['release_year'] <= 2021)]
    for p, col in colors.items():
        yearly = modern[modern['platform_name'] == p].groupby('release_year').size()
        ax.plot(yearly.index, yearly.values, marker='o', markersize=3, label=p, color=col, linewidth=2)
        
    ax.tick_params(colors='#EAEAEA')
    ax.set_xlabel('Release Year (Content Creation Year)', color='#EAEAEA', fontsize=11)
    ax.set_ylabel('Number of Titles', color='#EAEAEA', fontsize=11)
    ax.set_title('Content Creation Volume by Release Year (1990–2021)', color='#FFFFFF', fontsize=13, pad=15)
    ax.legend(facecolor='#1F1F1F', edgecolor='none', labelcolor='#EAEAEA')
    ax.grid(True, linestyle='--', alpha=0.2, color='#888888')
    
    plt.tight_layout()
    plt.savefig('screenshots/02_release_year_trends.png', dpi=150)
    plt.close()
    
    # 3. Cross-Platform Overlap Breakdown
    plt.figure(figsize=(8, 4.5), facecolor='#141414')
    ax = plt.subplot(111)
    ax.set_facecolor('#1F1F1F')
    
    categories = ['Unique to Netflix', 'Unique to Prime', 'Unique to Disney+', 'Shared: NFLX & Prime', 'Shared: NFLX & Disney+', 'Shared: Prime & Disney+']
    counts = [
        int(((overlap['on_netflix'] == 1) & (overlap['platform_count'] == 1)).sum()),
        int(((overlap['on_amazon_prime'] == 1) & (overlap['platform_count'] == 1)).sum()),
        int(((overlap['on_disney_plus'] == 1) & (overlap['platform_count'] == 1)).sum()),
        int(((overlap['on_netflix'] == 1) & (overlap['on_amazon_prime'] == 1)).sum()),
        int(((overlap['on_netflix'] == 1) & (overlap['on_disney_plus'] == 1)).sum()),
        int(((overlap['on_amazon_prime'] == 1) & (overlap['on_disney_plus'] == 1)).sum())
    ]
    bar_colors = ['#E50914', '#00A8E1', '#113CCF', '#C9A227', '#E06D53', '#48C9B0']
    
    y_pos = range(len(categories))
    ax.barh(y_pos, counts, color=bar_colors, height=0.55)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, color='#EAEAEA', fontsize=10)
    ax.tick_params(axis='x', colors='#EAEAEA')
    ax.set_xlabel('Distinct Title Count', color='#EAEAEA', fontsize=11)
    ax.set_title('Catalogue Exclusivity vs. Cross-Platform Overlap', color='#FFFFFF', fontsize=13, pad=15)
    
    for i, v in enumerate(counts):
        ax.text(v + 150, i, f"{v:,}", va='center', color='#FFFFFF', fontweight='bold', fontsize=10)
        
    plt.tight_layout()
    plt.savefig('screenshots/03_cross_platform_overlap.png', dpi=150)
    plt.close()
    
    print("All backup charts exported to screenshots/")

if __name__ == '__main__':
    compute_metrics()
    generate_backup_charts()

