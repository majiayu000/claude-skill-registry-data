---
name: sort-bed
description: Use when you need to sort BED, GFF, or VCF interval files for downstream bedtools processing, or rank records by feature size or score.
disable-model-invocation: true
user-invocable: true
---

# sort-bed

## Quick Start
- **Command:** `sortBed -i <input.bed>` or `bedtools sort -i <input.bed>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/sortBed`
- **Full reference:** See `references/help.md` for complete options and usage details

## When To Use This Tool

- Coordinate-sort BED, GFF, or VCF files before running bedtools operations that assume sorted inputs.
- Reorder intervals according to a trusted genome file or FASTA index.
- Rank features by size or score for reporting or manual review.
- Preserve leading headers while sorting interval records.

## Common Patterns

```bash
# 1) Default chromosome/start sort
sortBed \
  -i peaks.bed \
  > peaks.sorted.bed
```

```bash
# 2) Sort using reference chromosome order from a FASTA index
sortBed \
  -i variants.vcf \
  -faidx genome.fa.fai \
  -header \
  > variants.sorted.vcf
```

```bash
# 3) Rank features by descending score within chromosome order
sortBed \
  -i peaks.bed \
  -chrThenScoreD \
  > peaks.by-score.bed
```

## Recommended Workflow

1. Decide whether you need true coordinate sorting for downstream interval algorithms or a ranking sort for reporting.
2. Use the default mode for simple chromosome/start sorting, or supply `-g` / `-faidx` to impose reference-consistent chromosome order.
3. Add `-header` if the file contains a header that must remain at the top.
4. If the sorted output will feed a later `-sorted` bedtools step, verify you used a coordinate sort mode rather than a size/score ranking mode.

## Guardrails

- Default chromosome ordering is lexical, so names like `chr10` may sort before `chr2`; use `-g` or `-faidx` for reference order.
- `-sizeA`, `-sizeD`, `-chrThenSizeA`, `-chrThenSizeD`, `-chrThenScoreA`, and `-chrThenScoreD` are ranking modes, not substitutes for coordinate-sorted input to chromsweep-based workflows.
- `-header` only preserves the leading header from the input; it does not infer or reconstruct missing metadata lines.
- Prefer `-h` for help; GNU-style `--help` and `--version` emit wrapper errors before usage text.
