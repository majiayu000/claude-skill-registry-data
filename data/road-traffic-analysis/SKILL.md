---
name: road-traffic-analysis
description: "Use this skill for road traffic tasks, including Baidu realtime services, route planning, weather, geocoding, around-location traffic, local/uploaded CSV traffic data analysis, local/uploaded CSV traffic forecasting, local/uploaded CSV traffic anomaly detection, and Xi'an 2024 traffic annual-report RAG retrieval. Do not use for OSM graph parsing, legacy congestion reports, or generic non-road network traffic."
metadata:
  short-description: Road traffic realtime query, forecasting, anomaly detection, and RAG.
---

No need to check real-time traffic unless you ask for it.

Prioritize local data and methodologies for data sourcing; web searching is not required.

# Road Traffic Analysis

This is the single road-traffic skill. It covers realtime API tasks, CSV data analysis, forecasting, anomaly detection, RAG evidence retrieval, and one local CSV data source:

For queries involving multiple tasks, account for their logical dependencies and perform task chain decomposition.

The model should preferentially use the native skills included in this scope, such as traffic anomaly detection, prediction, and API querying.

For real-time traffic analysis queries, actively consider weather factors.

If the user requires chart plotting, refer to the chart-visualization skill.

| Family | Use For | Script |
| --- | --- | --- |
| Realtime services | Baidu route, weather, geocode, single-road traffic, around-location traffic | `scripts/simple_baidu_services.py` |
| CSV data analysis | Understand, summarize, compare, aggregate, and explain uploaded/local CSV traffic data | inspect with `scripts/forecast_runner.py`, then LLM-authored pandas analysis |
| Forecasting | Predict future traffic flow from uploaded CSV or inline history | `scripts/forecast_runner.py` |
| Anomaly detection | Detect abnormal traffic flow from uploaded CSV or inline history | `scripts/anomaly_runner.py` |
| RAG knowledge retrieval | Retrieve cited background facts from the 2024 Xi'an traffic annual report | `scripts/rag_xian2024_min.py` |

Local CSV database:

- Path: `/mnt/skills/custom/road-traffic-analysis/data/csv`
- Use for built-in/sample/local road-traffic CSV data.
- Choose a CSV by browsing directory and filenames, then handle it as uploaded CSV data for analysis, forecast, or anomaly detection.

Use `/mnt/skills/custom/road-traffic-analysis/...` in the agent sandbox. In repo-local debugging, use `skills/custom/road-traffic-analysis/...`.

`BAIDU_AK` must come from the environment for Baidu realtime services. Do not place API keys in prompts, examples, logs, or tracked files.

## Prompt-Driven Document Routing

The LLM decides whether a request needs annual-report RAG. Do not build or call any script-level intent classifier for document routing.

Use `rag_xian2024_min.py query` only when the user asks for at least one of these:

- Recent years traffic report facts or indicators
- Xi'an recent-years traffic congestion, traffic operation trends, congestion changes, bottleneck areas, or congestion governance context
- citywide background, annual trend, benchmark, or planning context
- comparison against annual-report metrics
- source-backed wording for a governance, leadership, or decision-support report
- explanation of realtime findings using annual-report context

When citing, please list evidence sources in detail, including the specific file, line number, page, or section.

Do not use RAG for direct current-status tasks unless the user also asks for background, benchmark, or cited report context:

- current road congestion
- today's weather
- route planning
- CSV forecasting
- CSV anomaly detection

For mixed governance questions, decompose in this order:

1. Get current measurements from realtime tools.
2. Retrieve annual-report context with RAG.
3. Synthesize the answer and keep the evidence types separate.

For broad Xi'an historical/background questions such as "近年来西安市交通拥堵情况",
"近几年西安交通运行趋势", "西安拥堵变化", or "西安拥堵治理情况", prefer
`rag_xian2024_min.py query` immediately. Do not first search `/mnt/user-data/workspace`,
ask for uploaded CSV data, or use web search unless the user explicitly asks for uploaded
data analysis, realtime status, or web search.

## Prompt Guidance

The LLM decides the task family from the user's wording. Do not build script-level intent classifiers or rigid keyword rules.

1. Realtime traffic, route, weather, geocoding, and nearby road-condition requests use `simple_baidu_services.py`.
2. Descriptive CSV questions use CSV data analysis. This includes requests to analyze past days, summarize traffic conditions, compare roads/sensors/time periods, calculate averages/totals, describe peak/off-peak patterns, or explain historical trends.
3. Future traffic-flow prediction uses `forecast_runner.py`.
4. Abnormal flow, outlier, sudden jump, threshold breach, or anomaly detection uses `anomaly_runner.py`.
5. Citywide Xi'an traffic background, recent-years congestion situation, traffic operation trends, annual-report facts, benchmark indicators, development context, and source-backed governance-report wording use `rag_xian2024_min.py query` after prompt-based intent judgment.
6. If a user asks for realtime status plus policy/background explanation, run the realtime API first, then retrieve RAG evidence for context. Do not let RAG replace realtime measurements.
7. If the user asks to use built-in, sample, local, existing, or database CSV data, list `/mnt/skills/custom/road-traffic-analysis/data/csv`, choose the best matching `.csv` by filename/path, then handle it like an uploaded CSV. If one local CSV clearly matches the user request, proceed with that file.
8. If no local CSV matches or multiple files are equally plausible, ask the user to choose from candidate filenames.
9. Uploaded/local CSV tasks must run `inspect` first, then perform semantic column mapping from actual columns.
10. For CSV data analysis, the LLM decides the analysis plan after inspection:
   - required: `timestamp_col` when time-window or trend analysis is requested
   - common optional: traffic volume/count column, speed column, congestion column, road/sensor/location column, peak/off-peak column
   - after mapping, write a small task-specific pandas analysis in bash; do not use a fixed summary script and do not read the whole CSV into model context
11. For CSV forecasting/detection, mapping is LLM-decided after inspection:
   - required: `timestamp_col`, `value_col`
   - optional: `series_id_col`
12. Ask only for missing required fields or necessary disambiguation. Do not guess city, file, timestamp/value mapping, frequency, horizon, threshold, or model/detector preference when unclear.
13. If the user asks for CSV data analysis, forecasting, or anomaly detection without uploaded CSV, local CSV, or inline history data, ask for the data source. Do not infer trends from a single realtime Baidu response.
14. Do not use web search for realtime weather or traffic unless the user explicitly asks to search the web.

## Reference Loading

Load only the reference needed for the current task:

- Realtime Baidu services: `references/realtime.md`
- CSV data analysis: `references/data-analysis.md`
- Forecasting: `references/forecasting.md`
- Anomaly detection: `references/anomaly-detection.md`
- Local CSV database selection: `references/local-csv-db.md`
- RAG knowledge retrieval: `references/rag.md`
- Examples and mixed workflows: `references/examples.md`

## Quick Commands

Realtime capabilities:

```bash
python /mnt/skills/custom/road-traffic-analysis/scripts/simple_baidu_services.py --action capabilities
```

Forecast model catalog:

```bash
python /mnt/skills/custom/road-traffic-analysis/scripts/forecast_runner.py --action models
```

Anomaly detector catalog:

```bash
python /mnt/skills/custom/road-traffic-analysis/scripts/anomaly_runner.py --action detectors
```

Local CSV database listing:

```bash
find /mnt/skills/custom/road-traffic-analysis/data/csv \
  -maxdepth 2 \
  -type f \
  -name "*.csv" \
  -printf "%p\n"
```

CSV data analysis inspect:

```bash
python /mnt/skills/custom/road-traffic-analysis/scripts/forecast_runner.py \
  --action inspect \
  --file /mnt/skills/custom/road-traffic-analysis/data/csv/traffic.csv \
  --head 100
```

RAG query for Xi'an 2024 annual-report evidence:

```bash
python /mnt/skills/custom/road-traffic-analysis/scripts/rag_xian2024_min.py \
  query "西安市中心城区主干路高峰期平均速度是多少" \
  --top-k 5
```

RAG uses the Elasticsearch index `xian_traffic_2024_min`. If the index is missing, import the prepared chunks first:

```bash
python /mnt/skills/custom/road-traffic-analysis/scripts/rag_xian2024_min.py build
```

The RAG script defaults to `--retrieval-mode auto`: vector retrieval is used when embedding dependencies are installed; otherwise it uses Elasticsearch text search.

CSV forecast inspect:

```bash
python /mnt/skills/custom/road-traffic-analysis/scripts/forecast_runner.py \
  --action inspect \
  --file /mnt/user-data/uploads/traffic.csv \
  --head 100
```

CSV anomaly inspect:

```bash
python /mnt/skills/custom/road-traffic-analysis/scripts/anomaly_runner.py \
  --action inspect \
  --file /mnt/user-data/uploads/traffic.csv \
  --head 100
```

## Output Discipline

Always include:

- selected task family and script/action used
- input parameters or CSV mapping used
- selected CSV path when local/uploaded CSV is used
- key measured results first
- assumptions and missing fields when applicable
- output file path for forecast/anomaly exports
- RAG citations as source, section path, and page range when RAG is used

Keep interpretation conservative. For anomaly detection, describe results as abnormal, notable, suspicious, or investigation-worthy; do not claim incident cause or intent unless the data directly supports it.

## Boundaries

- Realtime Baidu APIs do not provide historical model training data.
- Forecasting requires uploaded CSV, local CSV, or inline numeric history.
- Anomaly detection requires uploaded CSV, local CSV, or inline numeric history.
- CSV data analysis requires uploaded/local CSV data and must inspect schema before analysis.
- Local CSV database currently supports `.csv` files only.
- RAG currently covers the 2024 Xi'an traffic annual report only, stored in Elasticsearch index `xian_traffic_2024_min`. It provides background evidence and benchmark context, not realtime road conditions.
- This skill no longer includes OSM graph parsing, graph retrieval, evidence building, or legacy congestion reports.
