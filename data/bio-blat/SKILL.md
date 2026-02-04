---
name: bio-blat
description: "Runs local BLAT searches for DNA sequence alignment against hg38 or CHM13 using local .2bit references. Use when a user wants to align a DNA sequence without relying on UCSC API access."
user_invocable: true
---

# BLAT API Searching

## Quick start

Run BLAT locally via the Python CLI script. The script manages reference downloads.

## Utility script

Install dependencies:

```bash
uv pip install typer
```

Run BLAT with a FASTA file:

```bash
python scripts/run_blat_local.py run --reference hg38 --fasta path/to/query.fasta
```

Run BLAT with a raw sequence:

```bash
python scripts/run_blat_local.py run --reference CHM13 --sequence ACTG...
```

Save JSON output to a file:

```bash
python scripts/run_blat_local.py run --reference hg38 --sequence ACTG... --output blat.json
```

## When to read references

- **Local BLAT setup and references**: See `references/local_blat.md`

## Workflow (local-only)

1. Confirm the reference assembly (`hg38` or `CHM13`).
2. Ensure the 2bit reference exists in `~/.local/share/blat`.
3. Use the CLI script to run BLAT and get a PSL output.
4. If FASTA has multiple sequences, split into one sequence per file.
