---
name: gbf2fsa
description: Use when converting GenBank format (.gbf) files to FASTA format (.fsa) as part of sequence data preprocessing
disable-model-invocation: true
user-invocable: true
---

# gbf2fsa

## Quick Start
- **Command**: `gbf2fsa [input.gbf] > output.fsa`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/gbf2fsa`
- **Reference**: See `references/help.md` for full documentation

## When To Use This Tool

- Convert GenBank flatfiles into plain FASTA sequences.
- Flatten annotation-rich GenBank records down to sequence headers plus raw sequence for downstream sequence tools.
- Reuse the existing `gbf2xml | xml2fsa` pipeline without rebuilding it by hand.

## Common Patterns

```bash
# 1) Convert a GenBank flatfile into FASTA
gbf2fsa < records.gbf > records.fsa
```

```bash
# 2) Stream GenBank output straight from efetch into FASTA
efetch -db nuccore -id TEST0001 -format gb | gbf2fsa > TEST0001.fsa
```

## Recommended Workflow
1. Verify input file is valid GenBank format (.gbf)
2. Run `gbf2fsa` through stdin redirection or a pipe.
3. Inspect the FASTA header and sequence on a small sample first.
4. Proceed with downstream FASTA-based analysis

## Guardrails
- Input must be valid GenBank format
- This wrapper is just `gbf2xml | xml2fsa`, so `transmute`, `xtract`, and the companion wrappers must all be on `PATH`.
- The wrapper does not provide meaningful `--help` / `--version` output.
- Output FASTA headers follow the `xml2fsa` accession-plus-definition pattern, so confirm they match downstream expectations.
