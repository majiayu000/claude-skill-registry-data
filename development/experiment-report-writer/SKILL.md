---
name: experiment-report-writer
description: >
  Write structured experiment sections (methods + results + discussion) for
  NQS + SQD projects in this repository, based on contents of results/ and
  figures/.
license: Proprietary. For internal research writeups only.
---

# Experiment Report Writer

## Purpose

Given:
- processed result tables in `results/processed/` (CSV / Parquet),
- plots in `results/figures/`,

produce structured write-ups that could be dropped into a paper, report, or
slide deck.

## Output Format

When asked to summarize experiments, produce:

1. **Experimental setup**
   - Molecule, encoding (e.g. 12-bit H₂), Hamiltonian details if provided.
   - NQS architecture (FFNN / Transformer; layers, heads, hidden sizes).
   - SQD configuration (sample counts, iteration limits, configuration
     recovery, etc.).

2. **Results**
   - Tables summarizing:
     - estimated energies and reference values,
     - bias / RMSE vs. reference,
     - variance and empirical confidence intervals.
   - Short bullet list of main numerical observations.

3. **Discussion**
   - Interpretation of trends (e.g., how NQS helps or fails under low
     sample counts).
   - Hypothesized causes of discrepancies.
   - Concrete suggestions for follow-up experiments.

## Instructions

- Read the relevant result files **before** writing.
- For each figure, include:
  - what is plotted on each axis,
  - key trends,
  - any notable anomalies.
- If some information is missing, explicitly state assumptions.
