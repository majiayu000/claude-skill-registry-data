---
name: nuc-bed
description: Use when profiling nucleotide content (AT/GC percentages, base counts) of genomic intervals against a FASTA reference.
disable-model-invocation: true
user-invocable: true
---

# nuc-bed

## Quick Start
- **Command:** `nucBed -fi reference.fa -bed intervals.bed [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/nucBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Compute AT / GC fraction and base counts for genomic intervals.
- Profile interval sequence composition against a reference FASTA.
- Extract sequence alongside composition with `-seq`.
- Count user-defined sequence motifs with `-pattern`, optionally case-insensitive via `-C`.

## Common Patterns

```bash
# 1) Basic nucleotide composition over intervals
nucBed \
  -fi reference.fa \
  -bed peaks.bed
```

```bash
# 2) Strand-aware sequence composition with extracted sequence
nucBed \
  -fi reference.fa \
  -bed transcripts.bed \
  -s \
  -seq
```

```bash
# 3) Count motif occurrences inside intervals
nucBed \
  -fi reference.fa \
  -bed peaks.bed \
  -pattern CG \
  -C
```

## Recommended Workflow

1. Ensure FASTA headers and interval chromosome names refer to the same coordinate system.
2. Start with the default composition output before adding sequence extraction or motif counting.
3. Add `-s` only when the strand of the intervals matters for interpretation.
4. Validate a few rows manually when motif counts or sequence extraction drive downstream conclusions.

## Guardrails

- `-fi` and `-bed` are both required.
- `-pattern` is case-sensitive unless `-C` is added.
- `-fullHeader` changes FASTA header matching behavior; use it only if the interval identifiers depend on full deflines rather than the first token.
- `-seq` increases output width substantially by appending extracted sequence text.
- Prefer `-h` for help; GNU-style `--help` / `--version` calls on these wrappers are noisy.
