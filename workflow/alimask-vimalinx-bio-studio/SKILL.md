---
name: alimask
description: Use when masking columns or coordinate ranges in multiple-sequence alignments before downstream HMMER or alignment-processing steps.
disable-model-invocation: true
user-invocable: true
---

# alimask

Alignment-mask editing tool for multiple-sequence alignments. Local runtime is blocked by a missing shared library, so the behavior documented here is anchored in binary strings and option text rather than live execution.

## Quick Start

- **Command:** `alimask`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/alimask`
- **Runtime status in this environment:** blocked at startup by missing `libopenblas.so.0`

## When To Use This Tool

- Mask explicit alignment-column ranges before downstream profile or consensus work.
- Convert between model coordinates and alignment coordinates with `--model2ali` or `--ali2model`.
- Add or update mask lines in an existing multiple-sequence alignment.
- Prepare Stockholm-like alignment data for subsequent HMMER / Easel processing.

## Common Patterns

```bash
# 1) Mask alignment-coordinate columns and write a new alignment
alimask --alirange 10-20,30-40 alignment.sto > masked.sto
```

```bash
# 2) Mask in model coordinates instead of alignment coordinates
alimask --modelrange 5-15 alignment.sto > masked.sto
```

```bash
# 3) Translate ranges without emitting a masked post-MSA alignment
alimask --model2ali 5-15 alignment.sto
alimask --ali2model 10-25 alignment.sto
```

## Recommended Workflow

1. Decide whether your mask is defined in alignment coordinates or model coordinates before choosing flags.
2. Start with one small range and inspect the resulting alignment or coordinate mapping before applying many masks at once.
3. Use `--informat` if you must read the alignment from stdin and `--outformat` if downstream tooling needs a non-default MSA format.
4. Only use `--appendmask` when you intentionally want to preserve and extend an existing mask rather than replace it.

## Guardrails

- The binary cannot currently start here because `libopenblas.so.0` is missing, so `-h` / `--help` were not runnable.
- Binary strings show you must specify one masking or mapping mode: `--modelrange`, `--alirange`, `--model2ali`, or `--ali2model`.
- The strings also show `--model2ali` and `--ali2model` are reporting modes with `no postmsa`, so do not expect a masked alignment file from those calls.
- If the input alignment comes from stdin (`-`), the embedded option text says you must also provide `--informat`.
- `--hand` requires an RF line according to the binary's own error text: `Model file does not contain an RF line, required for --hand.`
- The option surface recovered from the binary includes alignment-type assertions (`--amino`, `--dna`, `--rna`), weighting controls, `--appendmask`, `--informat`, and `--outformat`; validate the exact combination in a healthier runtime before using it in production automation.
