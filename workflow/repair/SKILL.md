---
name: repair
description: Use when paired-end reads need to be reordered so mates appear consecutively, or when preparing BAM files for featureCounts by adding dummy reads for singletons.
disable-model-invocation: true
user-invocable: true
---

# repair

`repair` is a pair-order repairer for SAM/BAM. It rewrites output as BAM, optionally adds dummy mates for singletons/unpaired reads, and is designed to make the output acceptable to `featureCounts`.

## Quick Start

- **Command:** `repair -i input.bam -o output.bam`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/repair`
- **SAM input switch:** add `-S` when the input is SAM rather than BAM

## When To Use This Tool

- Reordering paired-end reads so mates from the same pair appear next to each other in the output
- Adding dummy reads for singleton reads that lack a pair, making output compatible with featureCounts
- Converting SAM to BAM while repairing pair order
- Processing BAM/SAM files to ensure proper paired-read alignment for downstream counting tools

## Common Patterns

```bash
# 1) Repair a BAM file with default dummy-read behavior
repair -i input.bam -o repaired.bam
```

```bash
# 2) Repair SAM input
repair -S -i input.sam -o repaired.bam
```

```bash
# 3) Suppress dummy mates for singleton reads
repair -d -S -i input.sam -o repaired.bam
```

## Recommended Workflow

1. Decide whether you want featureCounts-compatible dummy mates; if not, add `-d`.
2. Use `-S` explicitly for SAM input and leave it off for BAM input.
3. Write to a fresh BAM path and inspect the output with `samtools view`.
4. Only then pass the repaired BAM into counting or other pair-sensitive downstream tools.

## Guardrails

- Input and output files must be specified with `-i` and `-o` (no defaults)
- Output is always BAM format; there is no SAM output option
- `-h` and `--help` are not clean help flags; they are treated as invalid options and then the program prints its usage banner (`repair Version 2.1.1`).
- In local tests, singleton or unpaired reads caused `repair` to add dummy mates with sequence `N` and quality `A`.
- `-d` really suppresses dummy-read insertion: a singleton SAM stayed singleton in the repaired BAM when this flag was used.
- A two-read smoke test with flags `73` and `137` was treated as two unpaired reads and produced one dummy mate for each, so pair interpretation is strict.
- The binary's own strings include `ERROR: featureCounts does not support counting long paired-end reads.`, which is a clue that this tool is narrowly targeted at featureCounts compatibility rather than general duplicate/repair logic.
