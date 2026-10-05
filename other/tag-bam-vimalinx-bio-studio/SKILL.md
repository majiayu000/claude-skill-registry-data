---
name: tag-bam
description: Use when you need to annotate BAM alignments with a two-character tag based on overlaps with BED, GFF, or VCF annotation files, such as labeling reads by feature class or interval source.
disable-model-invocation: true
user-invocable: true
---

# tag-bam

## Quick Start
- **Command**: `tagBam -i reads.bam -files annot1.bed annot2.bed -labels A1 A2 > tagged.bam`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/tagBam`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Label reads by which annotation tracks they overlap.
- Populate BAM tags from file labels, annotation names, or annotation scores.
- Add interval-derived metadata to alignments before downstream filtering or QC.
- Apply same-strand or opposite-strand overlap rules while tagging.

## Common Patterns

```bash
# 1) Tag reads by which annotation file they overlap
tagBam \
  -i reads.bam \
  -files genes.bed repeats.bed \
  -labels GENE REP \
  > tagged.bam
```

```bash
# 2) Populate the tag with the annotation name field on the same strand
tagBam \
  -i reads.bam \
  -files exons.bed \
  -labels EXON \
  -names \
  -s \
  > reads.named-tags.bam
```

```bash
# 3) Record full interval payloads for debugging or provenance
tagBam \
  -i reads.bam \
  -files loci.bed \
  -labels LOCUS \
  -intervals \
  -tag YK \
  > reads.interval-tags.bam
```

## Recommended Workflow

1. Choose the annotation files that define the tag source and decide whether the payload should be file labels, annotation names, scores, or full intervals.
2. Choose the output tag name with `-tag` if the default `YB` is not appropriate.
3. Add overlap and strand constraints with `-f`, `-s`, or `-S` before writing the tagged BAM stream to a new file.
4. Inspect a few records with a BAM viewer or `samtools view` to confirm the expected tags were attached.

## Guardrails

- `-i` and `-files` are required, and you must also provide a tag payload source via `-labels`, `-names`, or `-scores`.
- `-intervals` still requires `-labels` so the tool can record which annotation file contributed the interval.
- The command writes BAM to stdout; redirect to a file or pipe into another BAM-aware tool.
- Custom tags supplied with `-tag` must be exactly two characters.
- If you use `-labels`, provide one label per annotation file.
- Prefer `-h` for help; GNU-style `--help` and `--version` emit wrapper errors before usage text.
