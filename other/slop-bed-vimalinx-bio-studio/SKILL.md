---
name: slop-bed
description: Use when you need to expand genomic intervals by adding flanking base pairs to features in BED, GFF, or VCF files.
disable-model-invocation: true
user-invocable: true
---

# slop-bed

## Quick Start
- **Command**: `slopBed -i <input> -g <genome> -b <int>` or `bedtools slop -i <input> -g <genome> -b <int>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/slopBed`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Expand intervals outward by a fixed amount on both sides.
- Add asymmetric upstream/downstream flanks with `-l` and `-r`.
- Build strand-aware promoter or neighborhood windows with `-s`.
- Scale flanking size as a fraction of interval length with `-pct`.

## Common Patterns

```bash
# 1) Add 200 bp of symmetric flank to every interval
slopBed \
  -i peaks.bed \
  -g genome.sizes \
  -b 200
```

```bash
# 2) Create a strand-aware promoter window: 2 kb upstream, 200 bp downstream
slopBed \
  -i transcripts.bed \
  -g genome.sizes \
  -l 2000 \
  -r 200 \
  -s
```

```bash
# 3) Expand each interval by 25% of its own length on both sides
slopBed \
  -i intervals.bed \
  -g genome.sizes \
  -b 0.25 \
  -pct
```

## Recommended Workflow

1. Prepare a genome file (or FASTA `.fai`) so bedtools knows the chromosome bounds.
2. Choose symmetric expansion with `-b` or asymmetric expansion with `-l` plus `-r`.
3. Add `-s` only when left/right should be interpreted relative to feature strand, and add `-pct` only when flank sizes should scale with feature length.
4. Inspect a few results to confirm the biological interpretation and the expected boundary clipping at chromosome edges.

## Guardrails

- `-i` and `-g` are both required.
- Use either `-b` alone or `-l` together with `-r`; these modes are mutually exclusive.
- With `-pct`, values are fractions of feature length rather than base pairs.
- `-s` changes how left and right are interpreted for negative-strand records; it is essential for true upstream/downstream flanks.
- Starts are clipped to 0 and ends are clipped to chromosome length when expansion would cross chromosome boundaries.
