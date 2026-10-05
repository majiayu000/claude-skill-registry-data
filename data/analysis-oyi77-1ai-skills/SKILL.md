---
name: analysis
description: Use when full-stack data analysis pipeline — clean, detect anomalies,
  generate reports, and create visualizations with production pandas. Turn raw data
  into paid deliverables.
domain: data
author: oyi77
license: Apache-2.0
subdomain: data-engineering
tags:
- analytics
- data-cleaning
- anomaly-detection
- reporting
- visualization
- pandas
- money-making
version: 1.0.0
category: data
---
## Overview

This skill is the full-stack data analysis pipeline — cleaning, anomaly detection, report generation, and visualization with production pandas. Use it when raw data must become a paid deliverable. It covers the workflow from ingest to the finished report.



# Data Analysis Pipeline — Clean, Analyze, Report, Visualize



## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Money-Making Overview

| Service | Client Price | Your Time | ROI |
|---------|-------------|-----------|-----|
| Data cleaning & preparation | $200–$800/project | 1–3 hrs | $150–$400/hr |
| Anomaly detection & audit | $500–$2,000/report | 2–4 hrs | $250–$500/hr |
| Custom report generation | $300–$1,500/report | 1–3 hrs | $200–$500/hr |
| Data visualization dashboard | $500–$3,000/dashboard | 3–8 hrs | $150–$375/hr |
| Full pipeline (clean→analyze→report→viz) | $1,500–$5,000/engagement | 4–12 hrs | $300–$500/hr |

**Target clients:** SaaS companies, e-commerce stores, real estate agencies, marketing agencies, startup founders who need data clarity but can't afford a full-time data analyst.

**Delivery model:** Fixed-price per pipeline or hourly consulting at $150–$400/hr.

## Combined Capabilities

| Capability | Tools | Output |
|-----------|-------|--------|
| **Data Cleaning** | pandas, numpy, pyjanitor | Clean, validated dataset + cleaning report |
| **Anomaly Detection** | pandas, scipy, sklearn, PyOD | Anomaly scores + flagged records + summary |
| **Report Generation** | Jinja2, pandas, HTML/PDF templates | Branded report (PDF, HTML, Markdown) |
| **Data Visualization** | matplotlib, seaborn, plotly, altair | Static charts + interactive dashboards |

## Concrete Action Flow

### Phase 1: Ingest & Profile (30 min)

```python
import pandas as pd
import numpy as np
from pathlib import Path

def profile_dataset(df: pd.DataFrame) -> dict:
    """Generate a comprehensive data profile in one pass."""
    profile = {
        "rows": len(df),
        "columns": len(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing": df.isnull().sum()[df.isnull().sum() > 0].to_dict(),
        "missing_pct": (df.isnull().mean() * 100).round(2).to_dict(),
        "duplicates": df.duplicated().sum(),
        "numeric_stats": df.describe().to_dict(),
        "unique_counts": {c: df[c].nunique() for c in df.select_dtypes("object").columns},
    }
    return profile

# Usage
df = pd.read_csv("client_data.csv")
profile = profile_dataset(df)
print(f"{profile['rows']} rows, {profile['duplicates']} duplicates, {len(profile['missing'])} columns with nulls")
```

### Phase 2: Clean (1–2 hrs)

```python
def clean_dataset(df: pd.DataFrame, config: dict = None) -> pd.DataFrame:
    """
    Production cleaning pipeline.
    config keys: drop_duplicates, fill_strategy, drop_high_missing, type_coercions
    """
    result = df.copy()
    config = config or {}

    # 1. Drop duplicates
    if config.get("drop_duplicates", True):
        before = len(result)
        result = result.drop_duplicates()
        dupes = before - len(result)
        if dupes:
            print(f"Dropped {dupes} duplicate rows")

    # 2. Handle missing values
    fill_strategy = config.get("fill_strategy", {})
    for col, strategy in fill_strategy.items():
        if col not in result.columns:
            continue
        if strategy == "median" and result[col].dtype.kind in "fc":
            result[col] = result[col].fillna(result[col].median())
        elif strategy == "mode":
            result[col] = result[col].fillna(result[col].mode().iloc[0] if not result[col].mode().empty else "")
        elif strategy == "zero":
            result[col] = result[col].fillna(0)
        elif strategy == "forward":
            result[col] = result[col].ffill()
        elif isinstance(strategy, (int, float, str)):
            result[col] = result[col].fillna(strategy)

    # 3. Drop columns with >80% missing
    high_missing_pct = config.get("drop_high_missing", 80)
    missing_pct = result.isnull().mean() * 100
    cols_to_drop = missing_pct[missing_pct > high_missing_pct].index.tolist()
    if cols_to_drop:
        result = result.drop(columns=cols_to_drop)
        print(f"Dropped {cols_to_drop} ({high_missing_pct}%+ missing)")

    # 4. Type coercions
    for col, dtype in config.get("type_coercions", {}).items():
        if col in result.columns:
            try:
                result[col] = result[col].astype(dtype)
            except (ValueError, TypeError):
                print(f"Warning: could not coerce {col} to {dtype}")

    return result


def cleaning_report(before: pd.DataFrame, after: pd.DataFrame) -> str:
    """Generate a human-readable cleaning summary."""
    lines = ["# Data Cleaning Report", ""]
    lines.append(f"Rows: {len(before)} → {len(after)} ({len(before)-len(after)} removed)")
    lines.append(f"Columns: {len(before.columns)} → {len(after.columns)}")
    lines.append("")
    lines.append("## Missing Values Before")
    for c in before.columns:
        m = before[c].isnull().sum()
        if m:
            lines.append(f"- {c}: {m} ({m/len(before)*100:.1f}%)")
    lines.append("")
    lines.append("## Missing Values After")
    for c in after.columns:
        m = after[c].isnull().sum()
        if m:
            lines.append(f"- {c}: {m} ({m/len(after)*100:.1f}%)")
    return "\n".join(lines)
```

### Phase 3: Anomaly Detection (1–2 hrs)

```python
from scipy import stats
from sklearn.ensemble import IsolationForest

def detect_outliers_iqr(df: pd.DataFrame, columns: list[str], multiplier: float = 1.5) -> pd.DataFrame:
    """
    IQR-based outlier detection. Returns a flagged copy.
    """
    result = df.copy()
    for col in columns:
        if df[col].dtype.kind not in "fc":
            continue
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - multiplier * IQR
        upper = Q3 + multiplier * IQR
        result[f"{col}_outlier"] = (df[col] < lower) | (df[col] > upper)
    return result


def detect_anomalies_isolation_forest(
    df: pd.DataFrame,
    feature_cols: list[str],
    contamination: float = 0.05,
) -> pd.DataFrame:
    """
    Isolation Forest anomaly detection for multivariate patterns.
    Returns scores and flags.
    """
    model = IsolationForest(contamination=contamination, random_state=42)
    df_clean = df[feature_cols].select_dtypes(include=[np.number]).dropna()
    scores = model.fit_predict(df_clean)
    result = df.copy()
    result.loc[df_clean.index, "anomaly_score"] = model.score_samples(df_clean)
    result.loc[df_clean.index, "is_anomaly"] = scores == -1
    return result


def anomaly_summary(df: pd.DataFrame, anomaly_col: str = "is_anomaly") -> str:
    """Summarize anomalies found."""
    total = df[anomaly_col].sum() if df[anomaly_col].dtype.kind in "iu" else df[anomaly_col].sum()
    lines = ["# Anomaly Detection Summary", ""]
    lines.append(f"Total anomalies: {int(total)} ({total/len(df)*100:.1f}% of data)")
    if df.get("anomaly_score") is not None:
        lines.append(f"Score range: {df['anomaly_score'].min():.3f} to {df['anomaly_score'].max():.3f}")
    return "\n".join(lines)
```

### Phase 4: Report Generation (1 hr)

```python
from datetime import datetime
import json

def generate_report(
    profile: dict,
    cleaning: str,
    anomaly: str,
    charts: list[str],
    title: str = "Data Analysis Report",
) -> str:
    """
    Generate a standalone HTML report from all analysis phases.
    charts: list of <img> tags or Plotly HTML divs.
    """
    sections = f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{title}</title>
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 960px; margin: auto; padding: 2rem; }}
  h1 {{ color: #1a1a2e; border-bottom: 3px solid #e94560; }}
  h2 {{ color: #16213e; margin-top: 2rem; }}
  .stat {{ background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; }}
  .anomaly {{ background: #fff3cd; padding: 1rem; border-left: 4px solid #ffc107; }}
  pre {{ background: #f4f4f4; padding: 1rem; overflow-x: auto; }}
  .chart {{ margin: 1.5rem 0; }}
</style></head>
<body>
<h1>{title}</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

<h2>Dataset Overview</h2>
<div class="stat">
  <strong>Rows:</strong> {profile['rows']} |
  <strong>Columns:</strong> {profile['columns']} |
  <strong>Duplicates:</strong> {profile['duplicates']}
</div>

<h2>Data Cleaning</div>
<pre>{cleaning}</pre>

<h2>Anomaly Detection</div>
<div class="anomaly">{anomaly}</div>

<h2>Visualizations</h2>
{"".join(f'<div class="chart">{c}</div>' for c in charts)}
</body></html>"""
    return sections


def report_to_markdown(profile: dict, cleaning: str, anomaly: str) -> str:
    """Generate a Markdown report suitable for GitHub or Notion."""
    lines = [
        f"# Data Analysis Report",
        f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        "",
        "## Dataset Overview",
        f"- Rows: {profile['rows']}",
        f"- Columns: {profile['columns']}",
        f"- Duplicates: {profile['duplicates']}",
        "",
        "## Data Cleaning",
        cleaning,
        "",
        "## Anomaly Detection",
        anomaly,
    ]
    return "\n".join(lines)
```

### Phase 5: Visualization (1–2 hrs)

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

def plot_numeric_distributions(
    df: pd.DataFrame,
    columns: list[str],
    output_dir: str = "charts",
) -> list[str]:
    """Generate distribution plots for numeric columns, return file paths."""
    Path(output_dir).mkdir(exist_ok=True)
    paths = []
    for col in columns:
        if col not in df or df[col].dtype.kind not in "fc":
            continue
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(f"Distribution of {col}")
        plt.tight_layout()
        path = f"{output_dir}/{col}_dist.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        paths.append(path)
    return paths


def plot_correlation_heatmap(
    df: pd.DataFrame,
    columns: list[str] = None,
    output_dir: str = "charts",
) -> str:
    """Generate a correlation heatmap, return file path."""
    numeric = df.select_dtypes(include=[np.number])
    if columns:
        numeric = numeric[[c for c in columns if c in numeric.columns]]
    Path(output_dir).mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(numeric.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title("Feature Correlation Matrix")
    plt.tight_layout()
    path = f"{output_dir}/correlation_heatmap.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_time_series(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    output_dir: str = "charts",
) -> str:
    """Generate a time series line chart."""
    Path(output_dir).mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(14, 5))
    plot_df = df[[date_col, value_col]].dropna().sort_values(date_col)
    ax.plot(plot_df[date_col], plot_df[value_col], linewidth=1)
    ax.set_title(f"{value_col} over Time")
    ax.set_xlabel(date_col)
    plt.xticks(rotation=45)
    plt.tight_layout()
    path = f"{output_dir}/{value_col}_timeseries.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
```

### Phase 6: Deliver & Bill

```python
#!/usr/bin/env python3
"""
Full pipeline orchestration script.
Usage: python run_pipeline.py --input client_data.csv --output report.html
"""
import argparse
import pandas as pd
from pathlib import Path

def run_pipeline(input_path: str, output_path: str):
    df = pd.read_csv(input_path)
    profile = profile_dataset(df)

    # Clean
    df_clean = clean_dataset(df, {
        "drop_duplicates": True,
        "fill_strategy": {"age": "median", "category": "mode", "revenue": "zero"},
    })
    cleaning = cleaning_report(df, df_clean)

    # Anomaly detection
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    df_flagged = detect_outliers_iqr(df_clean, numeric_cols)
    anomaly = anomaly_summary(df_flagged, f"{numeric_cols[0]}_outlier" if numeric_cols else None)

    # Visualize
    charts = []
    chart_paths = plot_numeric_distributions(df_clean, numeric_cols[:5])
    for p in chart_paths:
        charts.append(f'<img src="{p}" alt="distribution" style="max-width:100%">')

    # Report
    report = generate_report(profile, cleaning, anomaly, charts)
    Path(output_path).write_text(report)
    print(f"Report written to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="report.html")
    args = parser.parse_args()
    run_pipeline(args.input, args.output)
```

## First Action in 60 Minutes

1. **Find a dataset** — Download any CSV (e.g., Kaggle, your own exports, or mock data via `pip install faker && python -c "from faker import Faker; ..."`)
2. **Run the profile** — `profile_dataset(df)` and note missing values, data types, outliers
3. **Clean & flag** — Apply `clean_dataset()` and `detect_outliers_iqr()` with sensible config
4. **Generate one chart** — `plot_numeric_distributions(df, df.columns[:3])` 
5. **Produce a report** — `generate_report(profile, cleaning, anomaly, charts)`
6. **Package as a deliverable** — Bundle the report HTML + charts into a zip. That's your $500 minimum viable product.

## Verification

- Run the pipeline on a dataset with a known injected anomaly and confirm detection flags exactly that row.
- Verify the cleaning step handles missing values as documented (drop vs impute) and reports counts.
- Check the report/visualization renders from the transformed data — numbers in the report match the computed aggregates.
- Confirm the pipeline is rerunnable end-to-end on fresh data without manual steps.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I need a BI tool for this" | Pandas + matplotlib covers 90% of client needs without $10k/month tooling. |
| "Cleaning is not billable" | Cleaning IS the value. Clients pay for confidence in their data, not for charts. |
| "I will build the report template later" | Every client wants branding. Template-first saves 2 hrs per engagement. Charge for it. |
| "Anomaly detection needs ML" | IQR and z-score catch 80% of real-world anomalies faster than any model. |
| "One pipeline fits every client" | Abstract per-phase but wire per-client. Your `clean_dataset()` config dict is the differentiator. |

## Client Deliverable Checklist

- [ ] Cleaned dataset (CSV/Parquet) with cleaning_log.txt
- [ ] Anomaly-flagged dataset with score column + summary
- [ ] 3–5 distribution charts (PNG or interactive Plotly)
- [ ] Correlation heatmap
- [ ] Time-series chart (if temporal data exists)
- [ ] Branded HTML report or Markdown summary
- [ ] One-page executive brief (top 3 findings)
- [ ] Raw pipeline script for reproducibility (optional upsell)

## Output Format

For every client engagement, deliver a folder:

```
client-name-report/
  data/
    raw.csv              # original untouched
    cleaned.csv          # cleaned dataset
    flagged.csv          # with anomaly flags
  charts/
    age_dist.png
    revenue_dist.png
    correlation.png
    revenue_timeseries.png
  report.html            # full branded report
  executive-summary.md   # 3-bullet findings
  pipeline.py            # reproducible script
```

Bill for the whole folder, not per-file.

## Verification Checklist

- [ ] Dataset profiled (missing, duplicates, dtypes documented)
- [ ] Cleaning applied with config-driven strategy
- [ ] Anomaly detection executed with IQR or Isolation Forest
- [ ] At least one visualization generated per key metric
- [ ] Report generated in deliverable format (HTML or Markdown)
- [ ] Pipeline is reproducible from CLI
- [ ] No hardcoded paths or client data in reusable code
- [ ] Output is client-ready (no debug prints, proper branding)


## When to Use
Use this skill when working with analysis.


## Workflow
See the parent skill for authoritative workflow documentation.
