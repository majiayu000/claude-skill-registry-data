---
name: evo-usgs-flood-detection
description: "Detects flooding events at USGS streamgages by comparing daily streamflow against historical 90th percentile thresholds using the dataretrieval package. Use when analyzing flood occurrences over a date range for a list of USGS station IDs."
---

# evo-usgs-flood-detection

## Overview
End-to-end pipeline for detecting flooding at USGS streamgages. Reads station IDs from a file, fetches daily streamflow values and historical statistics via `dataretrieval.nwis`, computes flood-day counts by comparing observed daily mean streamflow against the 90th percentile historical threshold for each calendar day, and writes filtered results to CSV.

## Key Concepts

### Flood Definition
A **flood day** is defined as a day where the observed daily mean streamflow (`00060_Mean`) exceeds the 90th percentile (`p90_va`) of historical daily mean streamflow for that same calendar day (month + day).

### Data Sources
- **Daily Values**: `nwis.get_dv(sites, parameterCd='00060', start, end)` → returns `(DataFrame, metadata)` tuple
- **Historical Stats**: `nwis.get_stats(sites, statReportType='daily', parameterCd='00060')` → returns `(DataFrame, metadata)` tuple with columns `month_nu`, `day_nu`, `p90_va`

### Station ID Handling
USGS station IDs have leading zeros (e.g., `04193500`). Always read as strings, never as integers.

## Functions

### `load_stations(filepath: str) -> List[str]`
Reads station IDs from a flat text file (one per line) or CSV with `station_id` header. Preserves leading zeros.

### `get_station_flood_thresholds(site_id: str) -> pd.DataFrame`
Fetches 90th percentile historical daily streamflow thresholds. Returns DataFrame with `month_nu`, `day_nu`, `p90_va`.

### `detect_floods_for_site(site_id: str, start_date: str, end_date: str) -> int`
Fetches daily values, merges with thresholds on month/day, counts days where observed > p90. Returns integer count.

### `run_flood_detection_pipeline(stations_file, out_file, start, end) -> pd.DataFrame`
Orchestrates the full pipeline. Processes all stations, filters to those with >=1 flood day, writes CSV.

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-usgs-flood-detection/scripts')
from utils import load_stations, detect_floods_for_site, run_flood_detection_pipeline

# Run full pipeline
results = run_flood_detection_pipeline(
    stations_file='/root/data/michigan_stations.txt',
    out_file='/root/output/flood_results.csv',
    start='2025-04-01',
    end='2025-04-07'
)
```

## Output Format
CSV with two columns:
- `station_id`: 8-digit USGS station ID (string with leading zeros)
- `flood_days`: Number of days with flooding (positive integer, max 7 for a 7-day window)

Only stations with at least 1 flood day are included.

## Dependencies
- `dataretrieval` 1.0.10
- `pandas` 2.2.3
- Python 3.x
