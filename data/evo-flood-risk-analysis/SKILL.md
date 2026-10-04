---
name: evo-flood-risk-analysis
description: Detects flooding events at USGS streamgages by fetching instantaneous (15-min) gage height data, computing daily maximums, and comparing against NWS flood stage thresholds from the official NWS All Gauges Report. Outputs a CSV of stations with flood days.
---

# evo-flood-risk-analysis

End-to-end pipeline for identifying flood days at USGS streamgages using gage height data and NWS flood stage thresholds.

## Methodology

1. **Gage height (parameter 00065)** is used — NOT discharge (00060).
2. **Daily maximum of instantaneous (15-min) readings** is the aggregation method. Use `nwis.get_iv()` to fetch instantaneous values, then resample to daily max with `.resample('D').max()`.
3. **NWS flood stage thresholds** come from the NWS All Gauges Report CSV at `https://water.noaa.gov/resources/downloads/reports/nwps_all_gauges_report.csv`. Match stations by USGS site ID (`usgs_id` or `gaugelid` column). The flood stage column is `sigstages.flood.stage` or similar.
4. **Flood condition**: `daily_max_gage_height >= flood_stage` (greater than or equal).
5. Only stations with a valid numeric NWS flood stage are evaluated.
6. Only stations with at least one flood day are included in output.
7. Sort output by `flood_days` descending.

## Key Technical Rules

1. **Preserve leading zeros**: USGS station IDs are 8–15 digit strings (e.g., `04031000`). Always read/store as strings.
2. **Parameter codes**: `00065` = gage height (ft). Use instantaneous values (`get_iv`), NOT daily values (`get_dv`).
3. **Missing data**: Use `pd.to_numeric(errors='coerce')` to handle non-numeric sensor flags.
4. **Tuple unpacking**: `nwis.get_iv()` returns `(DataFrame, Metadata)` — always unpack.
5. **API rate limiting**: Use brief `time.sleep(0.5)` between station requests.
6. **No fallback**: Do NOT use discharge-based methods. Only gage height vs NWS flood stage.

## Usage

```python
import subprocess, sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'dataretrieval', '-q'])

sys.path.insert(0, '/app/environment/skills/evo-flood-risk-analysis/scripts')
from utils import run_flood_analysis

run_flood_analysis(
    stations_file='/root/data/michigan_stations.txt',
    out_file='/root/output/flood_results.csv',
    start='2025-04-01',
    end='2025-04-07'
)
```

## Output

CSV with two columns: `station_id` (string, leading zeros preserved) and `flood_days` (int). Only stations with at least one flood day are included. Sorted by flood_days descending.