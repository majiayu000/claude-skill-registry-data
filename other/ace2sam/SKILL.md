---
name: ace2sam
description: Use when converting ACE assembly files into SAM while preserving legacy ACE-specific padded or contig-sequence behavior.
disable-model-invocation: true
user-invocable: true
---

# ace2sam

## Quick Start

- **Command:** `ace2sam [-p] [-c] assembly.ace > alignments.sam 2> header.txt`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/ace2sam`
- **Reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Convert legacy ACE assembly files into SAM for downstream inspection with SAM/BAM-aware tools.
- Preserve ACE padding with `-p` when you need padded coordinate representation.
- Emit contig sequence information with `-c` when reconstructing richer reference context from ACE.
- Bridge older assembly/editing workflows into modern SAM-centric tooling.

## Common Patterns

```bash
# 1) Convert ACE to SAM, capturing stderr header text separately
ace2sam \
  assembly.ace > assembly.sam 2> assembly.header.txt
```

```bash
# 2) Keep padded coordinates in the SAM body
ace2sam \
  -p \
  assembly.ace > assembly.padded.sam 2> assembly.header.txt
```

```bash
# 3) Include contig sequence information
ace2sam \
  -c \
  assembly.ace > assembly.with-contigs.sam 2> assembly.header.txt
```

## Recommended Workflow

1. Validate that the input really is ACE and still follows the ordering assumptions expected by the converter.
2. Decide whether downstream consumers need padded coordinates (`-p`) or contig sequence output (`-c`) before conversion.
3. Capture stdout and stderr separately so you do not lose the header text emitted on stderr.
4. Inspect a few output records before loading the converted SAM into later tools.

## Guardrails

- `ace2sam` does not use GNU-style long flags; `--help` and `--version` are treated as invalid short-option bundles before usage text is shown.
- The program writes header text to `stderr` and the headerless SAM body to `stdout`; redirect both deliberately.
- Input ACE fields must appear in the documented order `(CO->[BQ]->(AF)->(RD->QA))`, and the read order in `AF` and `RD` must match.
- `-p` changes coordinate semantics by emitting padded SAM, so do not mix padded and unpadded outputs in the same downstream workflow.
