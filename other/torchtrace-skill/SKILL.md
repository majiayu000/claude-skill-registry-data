---
name: torchprofiler-trace-analysis
description: Analyze PyTorch profiler and vLLM trace files with Perfetto SQL evidence. Use when working with torch profiler traces, merged_trace files, vLLM profiling logs, Perfetto trace analysis, GPU kernel hotspots, synchronization waits, rank imbalance, prefill/decode bottlenecks, or optimization reports.
---

# TorchProfiler Trace Analysis

## Purpose

Use this skill to analyze PyTorch profiler traces from vLLM/VAP runs. Prefer evidence from Perfetto SQL and structured trace metadata over raw JSON snippets.

## Attribution

This project is inspired by the evidence-driven workflow design of:

- `Gracker/Perfetto-Skills`: standard Agent Skill structure, workflow routing, SQL-backed evidence, and report contracts.
- `Gracker/SmartPerfetto`: AI-assisted Perfetto analysis, evidence workflows, reports, and trace-processor-backed SQL analysis.

No code or SQL is copied from those projects. The SQL presets and workflows in this project are original and specialized for PyTorch profiler / vLLM traces.

## Workflow

1. Identify the latest or requested trace.
2. Prefer merged traces named like `*-merged_trace.json` or `*-merged_trace.json.gz`.
3. Run trace overview queries first.
4. Collect evidence for:
   - synchronization waits
   - GPU kernel hotspots
   - CPU operator hotspots
   - rank imbalance
   - memory copies
   - prefill/decode spans
   - idle gaps
5. Summarize findings with evidence.
6. Separate confirmed evidence from hypotheses.
7. Recommend next inspections in Perfetto/TensorBoard.

## Report Format

Use this structure:

```markdown
# TorchProfiler Trace Report

## Executive Summary
Short summary of the most likely bottleneck.

## Trace Metadata
- Trace file:
- Merged trace:
- Event count:
- Time span:
- Ranks:

## Evidence
| Area | Evidence | Interpretation |
|---|---|---|

## Bottleneck Hypotheses
1. Hypothesis with supporting evidence.

## Perfetto Inspection Guide
- Tracks/events to inspect next.

## Optimization Suggestions
- Concrete model/config/benchmark changes to try.

## Evidence Gaps
- Missing data or uncertainty.
```

## Safety

Do not infer causal conclusions from a query that only parsed successfully. Label uncertain conclusions as hypotheses. Do not request raw trace JSON unless a focused preview is necessary.

## Utilities

- Query presets: [queries.yaml](queries.yaml)
- Runner: [runner.py](runner.py)
- Workflow details: [WORKFLOWS.md](WORKFLOWS.md)
