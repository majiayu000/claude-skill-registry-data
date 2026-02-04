---
name: end-reason
description: Oxford Nanopore read end reason QC analysis. Use when analyzing nanopore sequencing quality, checking for adaptive sampling efficiency, investigating read termination patterns, diagnosing sequencing issues, or running QC on POD5/Fast5 data. Integrates with ont-experiments for provenance tracking via Pattern B orchestration. Supports signal_positive, unblock_mux_change, data_service_unblock_mux_change analysis with quality thresholds.
---

# End Reason Analysis - ONT QC

Analyze Oxford Nanopore read end reasons for quality assessment and adaptive sampling efficiency.

## Integration

Run through ont-experiments for provenance tracking:

```bash
ont_experiments.py run end_reasons exp-abc123 --json results.json --plot qc.png
```

Or standalone:

```bash
python3 end_reason.py /path/to/data --json results.json
```

## End Reason Categories

| End Reason | Description | Expected % |
|------------|-------------|------------|
| `signal_positive` | Normal completion | 80-95% |
| `unblock_mux_change` | Adaptive sampling rejection | 0-15% |
| `data_service_unblock_mux_change` | Basecall-triggered rejection | 0-10% |
| `mux_change` | Pore mux change | 1-5% |
| `signal_negative` | Signal lost | <5% |

## Quality Assessment

| Status | Criteria |
|--------|----------|
| ✓ OK | signal_positive ≥75% |
| ⚠ CHECK | signal_positive <75% or anomalies |
| ✗ FAIL | signal_positive <50% |

## Options

| Option | Description |
|--------|-------------|
| `--json FILE` | Output JSON summary |
| `--csv FILE` | Output per-read CSV |
| `--plot FILE` | Output bar chart (PNG/PDF) |
| `--format FORMAT` | Force format (pod5, fast5, summary) |
| `--quick` | Sample 10k reads only |

## Supported Formats

- POD5 (fastest, recommended)
- Fast5 (legacy)
- sequencing_summary.txt

## Output JSON

```json
{
  "total_reads": 15000000,
  "quality_status": "OK",
  "signal_positive_pct": 90.0,
  "unblock_mux_pct": 8.0,
  "data_service_pct": 1.0,
  "end_reasons": {
    "signal_positive": {"count": 13500000, "pct": 90.0},
    "unblock_mux_change": {"count": 1200000, "pct": 8.0}
  }
}
```
