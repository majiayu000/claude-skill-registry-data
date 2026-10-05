---
name: rnaplex
description: Use when screening a small query RNA against longer target RNA sequences for inter-molecular hybridization sites, especially when optional RNAplfold accessibility profiles should influence the ranking.
disable-model-invocation: true
user-invocable: true
---

# rnaplex

## Quick Start

- **Command**: `RNAplex -q <query.fa> -t <target.fa>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAplex`
- **Full reference**: See `references/help.md` for complete options and details

## When To Use This Tool

- Use `RNAplex` when you want to scan a query RNA against a longer target and rank likely hybridization sites.
- It is most appropriate for probe-like or small-RNA-like searches where only inter-molecular base pairs are modeled.
- Use `-a` when you already have `RNAplfold` accessibility profiles and want accessibility-aware target scoring.
- Use `-p` and `-Q` when the question is probe melting behavior rather than a generic interaction screen.

## Common Patterns

```bash
# Basic query-vs-target interaction search
RNAplex -q query.fa -t target.fa

# Include precomputed accessibility profiles from RNAplfold
RNAplex -q query.fa -t target.fa -a plfold_profiles/

# Require stronger interactions and allow longer duplexes
RNAplex -q query.fa -t target.fa -l 60 -e -12

# Probe mode with explicit probe concentration
RNAplex -q query.fa -t target.fa -p -Q 0.5
```

## Recommended Workflow

1. Prepare query and target RNA sequences in FASTA files
2. (Optional) Generate accessibility profiles using RNAplfold if incorporating accessibility effects
3. Run `RNAplex -q <query.fa> -t <target.fa> [-a <accessibility_dir>]` to compute duplex structures
4. Parse output: each line contains dot-bracket structure (strands separated by "&"), position ranges, and energy in kcal/mol

## Guardrails

- Only inter-molecular base pairs are considered; intra-molecular folding is ignored
- Default maximal interaction length is 40 nt; adjust with `-l` for longer interactions
- Accessibility profiles must be pre-computed with RNAplfold and provided via `-a` option
