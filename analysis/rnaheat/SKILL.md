---
name: rnaheat
description: Use when computing RNA specific heat profiles from sequence data to analyze melting behavior and thermal stability across temperature ranges.
disable-model-invocation: true
user-invocable: true
---

# rnaheat

## Quick Start

- **Command**: `RNAheat [OPTIONS] [<input>]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAheat`
- **Full reference**: See [`references/help.md`](references/help.md) for complete options and details

## When To Use This Tool

- Compute specific heat curves to study RNA melting behavior.
- Compare thermal stability across sequences or parameter settings.
- Scan a temperature range before choosing a biologically relevant folding temperature.
- Include circular-RNA or G-quadruplex assumptions in thermal profiles.

## Common Patterns

```bash
# 1) Compute a default heat-capacity profile
echo 'GGGAAAUCC' | RNAheat > heat.tsv
```

```bash
# 2) Restrict the temperature range and step size
echo 'GGGAAAUCC' | RNAheat --Tmin 10 --Tmax 80 --stepsize 0.5 > heat.tsv
```

```bash
# 3) Model a circular RNA with G-quadruplex support
echo 'GGGAAAUCC' | RNAheat --circ --gquad > heat.tsv
```

## Recommended Workflow

1. Prepare input RNA sequence(s) in plain text or FASTA-like format
2. Set temperature range with `--Tmin` and `--Tmax` (default 0–100°C) and adjust `--stepsize` as needed
3. Run `RNAheat` with appropriate options (e.g., `--circ` for circular RNA, `--gquad` for G-quadruplex)
4. Parse output pairs of temperature (°C) and specific heat (kcal/(mol*K)) for downstream analysis

## Guardrails

- Output is tabular (temperature, specific heat) to stdout; redirect to file for persistence
- Input stops at a line containing only `@` or EOF; ensure proper sequence delimiting
- Smoothing via `-m/--ipoints` affects curve shape; higher values produce smoother results at cost of resolution
