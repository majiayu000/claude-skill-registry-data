---
name: seqkit
description: Use when working with FASTA or FASTQ files for statistics, filtering, transformation, format conversion, searching, or set operations.
disable-model-invocation: true
user-invocable: true
---

# seqkit

## Quick Start
- **Command:** `seqkit <subcommand> [options] <input>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/seqkit`
- **Version:** 2.13.0
- **Full reference:** See [references/help.md](references/help.md) for complete subcommand options

## When To Use This Tool

- General-purpose FASTA/FASTQ inspection, filtering, conversion, and manipulation.
- Quick sequence operations without writing custom scripts.
- Use it when you need one clean subcommand instead of an ad hoc awk or Python one-liner.
- Especially useful for stats, grep-like selection, subsequences, and format conversion.

## Common Patterns

```bash
# 1) Basic FASTQ summary statistics
seqkit stats reads.fastq.gz
```

```bash
# 2) Filter sequences by minimum length and keep only IDs
seqkit seq -m 200 input.fa.gz
```

```bash
# 3) Search by ID or pattern
seqkit grep -p TP53 proteins.fa.gz
```

```bash
# 4) Convert FASTA/Q to tabular form
seqkit fx2tab reads.fastq.gz
```

```bash
# 5) Remove duplicates
seqkit rmdup input.fa.gz -o dedup.fa.gz
```

## Recommended Workflow

1. Start with `seqkit stats` to understand the file you are about to manipulate.
2. Choose the narrowest subcommand that matches the operation instead of overloading shell text processing.
3. Keep outputs compressed when appropriate; SeqKit handles compressed I/O directly.
4. Use subcommand-specific help for anything beyond the common workflows.

## Guardrails
- `seqkit version` is the version command; `seqkit --version` is not the right interface here.
- Use `seqkit <subcommand> --help` for real usage details, because the top-level command is just a dispatcher.
- Output compression is handled automatically from the filename suffix.
- SeqKit can parse IDs with its own regex rules, so be explicit if FASTA headers use unusual formats.
