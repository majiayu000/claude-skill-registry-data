---
name: insights-report
description: Use when building a GEPA pipeline insights report for a completed or in-progress pipeline run, when asked to document pipeline results, or when comparing pipeline run metrics across experiments.
---

# GEPA Pipeline Insights Report

Build publication-quality insights reports for GEPA pipeline runs with data-driven diagrams and cross-run comparison tables.

## Overview

An insights report documents a single pipeline run's performance: score trajectory, per-container analysis, feature assessment, and comparison against prior runs. Reports live in `docs/insights_reports/` with diagrams in `docs/images/`.

## When to Use

- User asks to "build an insights report" or "document pipeline results"
- A pipeline run has completed or is far enough along to analyze
- User wants to compare runs or assess new features

## Environment Setup

Source project variables from `.env` before any data access:

```bash
set -a && source .env && set +a
```

Key variables used throughout this workflow:

| Variable | Used For | Example |
|----------|----------|---------|
| `GOOGLE_CLOUD_PROJECT` | GCS client, Pipeline SDK | `hybrid-vertex` |
| `BUCKET_NAME` | GCS log/artifact bucket | `my-pipeline-artifacts` |
| `EXPERIMENT_NAME` | GCS path prefix | `sup-chain-test-v1` |
| `AGENT_ENGINE_ID` | Memory Bank namespace | `5646775610664550400` |
| `GOOGLE_CLOUD_LOCATION` | Pipeline SDK region | `us-central1` |
| `GOOGLE_CLOUD_MODEL_LOCATION` | Gemini endpoint | `global` |

**Always use these variables** — never hardcode project IDs, bucket names, or experiment names.

## Quick Reference

| Step | Action | Tool/Skill |
|------|--------|------------|
| 1. Get pipeline metadata | Parameters, state, task details | `inspect-vai-pipes` skill |
| 2. Download GCS logs | Per-table JSONL + progress.json | `gsutil` or Python GCS client |
| 3. Extract metrics | Scores, phases, tools, data sources | Python script (inline) |
| 4. Read prior reports | Comparison metrics from existing reports | Read tool on `docs/insights_reports/` |
| 5. Generate architecture diagram | GCP-styled 5-tier pipeline | `gcp-diagram` skill |
| 6. Generate data diagrams (4x) | Score trajectory, cross-run, container, feature | `paperbanana` skill |
| 7. Write report | Markdown with embedded images | Write tool |

## Step 1: Pipeline Metadata

Use the `inspect-vai-pipes` skill with the run name:
```
/inspect-vai-pipes my-pipeline-run-YYYYMMDD-HHMMSS
```

This gives: state, parameters (epochs, concurrency, fitness_scaling_factor, novelty_weight, worker_timeout, explore_rate, topic), task details, and timing.

### Run Name to GCS Path Mapping

Pipeline run names map to GCS paths by reformatting the timestamp:
```
my-pipeline-run-20260328-175751
                ↓
run-2026_03_28_17_57_51
```

Pattern: `YYYYMMDD-HHMMSS` → `YYYY_MM_DD_HH_MM_SS`

GCS base path:
```
gs://{bucket}/{experiment}/run-{YYYY_MM_DD_HH_MM_SS}/pipeline_root/evidence_reports/
```

## Step 2: Download GCS Logs

```python
from google.cloud import storage
import json

client = storage.Client(project='hybrid-vertex')
bucket = client.bucket('my-pipeline-artifacts')
prefix = '{experiment}/run-{timestamp}/pipeline_root/evidence_reports/'

# Discover tables
tables = set()
for blob in bucket.list_blobs(prefix=prefix):
    parts = blob.name[len(prefix):].split('/')
    if len(parts) >= 2 and parts[0] not in ('checkpoint_dir', 'code'):
        tables.add(parts[0])

# Download per-table logs and progress
for table in sorted(tables):
    log_blob = bucket.blob(f'{prefix}{table}/react_loop_fanout_log.json')
    prog_blob = bucket.blob(f'{prefix}{table}/progress.json')
    # Download and parse...
```

## Step 3: Extract Metrics

Parse JSONL log entries. Each line has this structure:
```json
{
  "epoch": 5,
  "evaluation": {
    "overall_score": 0.85,
    "scores": {"novelty": 0.7, "relevance": 0.9, "impact": 0.8, "actionability": 0.85, "specificity": 0.9, "trace_audit": 1.0},
    "should_persist": true,
    "justification": "..."
  },
  "evolution_phase": "Crossover",
  "persona": "synthesis-crossover-1234",
  "tools_used": ["generate_table_insights", "run_code_analysis"],
  "tools_declared": ["generate_table_insights"],
  "data_sources": ["1P", "GDELT", "Trends"],
  "diversity_score": 0.95,
  "source_dataset": "stores"
}
```

### Key Metrics to Compute

| Metric | Formula |
|--------|---------|
| Scored | Count of entries with `evaluation.overall_score` |
| Persisted | Count where `evaluation.should_persist == true` |
| Floors | Count where `overall_score <= 0.10` |
| Mean(NF) | Mean of scores > 0.10 |
| Trajectory | `(late_third_mean - early_third_mean) / early_third_mean * 100` |
| Per-container | Group all above by `source_dataset` |
| Phase distribution | Group by `evolution_phase` |

## Step 4: Read Prior Reports

Extract comparison metrics from these reports (read the Executive Summary tables):

| Report | File |
|--------|------|
| Tuned 28-Ep (Cold) | `docs/insights_reports/tuned_gepa_50epoch_report.md` |
| 25-Ep Asteroid | `docs/insights_reports/25epoch_evolution_report_20260325.md` |
| 30-Ep Supply Chain | `docs/insights_reports/supply_chain_30epoch_report_20260326.md` |
| 25-Ep H5 Cal | `docs/insights_reports/supply_chain_25epoch_h5_calibration_20260327.md` |
| 25-Ep H5v2 | `docs/insights_reports/supply_chain_25epoch_h5v2_20260328.md` |
| 50-Ep v1 (WIP) | `docs/insights_reports/supply_chain_50epoch_v1_20260330.md` |

## Step 5: Generate Architecture Diagram

Use the `gcp-diagram` skill. Write a text description to `/tmp/pipeline_report/diagram_architecture.txt`, then invoke:

```
/gcp-diagram /tmp/pipeline_report/diagram_architecture.txt "GEPA {N}-Epoch Pipeline Architecture"
```

The description should cover the 5-tier GEPA flow: Discovery → Synthesis → Execution → Evaluation → Persistence. Annotate any new features being tested in this run.

Save output to `docs/images/{prefix}_architecture.png`. Run the icon overlay script after generation.

## Step 6: Generate Data Diagrams (PaperBanana)

For each data diagram, write a text description file to `/tmp/` then use the `paperbanana` skill.

### Required Diagrams (5)

**1. Score Trajectory** — Multi-line chart: per-container + aggregate (dashed) mean(NF) over epochs, with early/mid/late shaded bands and 3-epoch smoothing
```
mcp__paperbanana__generate_diagram(source_context=<contents of /tmp/{prefix}_score_trajectory.txt>, caption="Score trajectory over {N} epochs")
```

**2. Cross-Run Comparison** — Dual-panel grouped bar chart: left panel (Mean(NF) + Trajectory%), right panel (Persist% + Floor%) across all runs
```
mcp__paperbanana__generate_diagram(source_context=<contents of /tmp/{prefix}_cross_run.txt>, caption="Cross-run performance comparison")
```

**3. Container Performance** — Horizontal grouped bars (scored/persisted/floors) per table, sorted by Mean(NF), with trajectory annotations
```
mcp__paperbanana__generate_diagram(source_context=<contents of /tmp/{prefix}_containers.txt>, caption="Per-container performance breakdown")
```

**4. Container Trajectories** — Grouped bars showing Early/Mid/Late mean scores per container + aggregate, with trajectory % annotated above each group
```
mcp__paperbanana__generate_diagram(source_context=<contents of /tmp/{prefix}_container_trajectories.txt>, caption="Per-container learning curves")
```

**5. Feature Assessment** (if new features tested) — Status cards for new features
```
mcp__paperbanana__generate_diagram(source_context=<contents of /tmp/{prefix}_features.txt>, caption="New feature assessment dashboard")
```

### Diagram Text File Format

Each text file should contain:
- Title
- Chart type (line chart, bar chart, status cards, etc.)
- Actual data values (not placeholders)
- Axis labels and annotations
- Color scheme hints
- Layout preferences

Save outputs to `docs/images/{prefix}_*.png`.

## Step 7: Write the Report

See `references/report-template.md` for the full section structure. The report follows this skeleton:

1. **Header** — Title, pipeline metadata block, key result one-liner
2. **Executive Summary** — N-run comparison table, 3-5 key findings
3. **Methodology** — Config changes table, architecture diagram, parameter tuning rationale (if config differs from prior run)
4. **Score Trajectory** — Early/mid/late epoch-range table, trajectory chart, per-epoch mean(NF) trend analysis
5. **Score Distribution** — Floor analysis (critic failures vs legitimate lows), per-dimension scores (novelty, relevance, impact, actionability, specificity, trace_audit)
6. **Container Analysis** — Per-container performance table, per-container trajectory (early/mid/late with pattern labels), per-container trajectory chart, phase distribution with quality analysis, tool usage, data source distribution
7. **Adaptive Threshold Analysis** (if FITNESS_SCALING_FACTOR changed) — Threshold trajectory over epochs, headroom gap (mean score minus threshold), death spiral risk assessment
8. **Concurrency Analysis** (if concurrency issues observed) — Three bottleneck model (Memory Bank writes, reads, Gemini API), effective throughput formula, duration analysis, recommended config by run length
9. **Feature Assessment** (if new features tested) — Per-feature: status (Active/Disabled/Partial), mechanism, quantitative evidence, verdict (Keep/Modify/Remove)
10. **Cross-Run Comparison** — Full comparison table, controlled pairwise delta analysis against closest control run (same topic, fewest param differences)
11. **Discussion** — Why trajectory is positive/negative/flat, cold vs warm start effects, which phases drove quality, concurrency collapse patterns, novelty saturation (if novelty < 0.40), late-epoch quality dips
12. **Recommendations** — Next run config table (current vs recommended vs rationale), immediate actions, future work
13. **Appendix** — Per-epoch detail table, pipeline parameters dump, GCS artifact paths, diagram list with generation method

### File Naming Convention

```
docs/insights_reports/{topic}_{N}epoch_{variant}_{YYYYMMDD}.md
```

Examples:
- `supply_chain_25epoch_h5v2_20260328.md`
- `supply_chain_50epoch_v1_20260330.md`

### Image Reference Format

```markdown
![Caption](../images/{prefix}_{diagram_name}.png)
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using raw Gemini API for diagrams | Use the `paperbanana` and `gcp-diagram` skills |
| Computing epoch as `index / 10` | Use the actual `epoch` field from log entries |
| Missing per-container trajectory | Always include early/mid/late breakdown per table |
| Comparing without controlling for config | Note which params differ in comparison tables |
| Not mentioning Memory Bank state | Always state cold vs warm start |
| Hardcoding GCS paths | Derive from experiment + run name |
| Using Cloud Logging scores | GCS JSONL logs are authoritative (structured, complete) |
| Skipping the icon overlay | GCP diagrams need official icons via `overlay_icons.py` |
