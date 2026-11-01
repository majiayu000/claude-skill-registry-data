---
name: salmon-output-parsing
description: Use when when you have salmon quant.sf.gz output files from pseudoalignment-based transcript quantification and need to convert transcript-level abundance estimates and counts into gene-level matrices for differential expression analysis with edgeR, DESeq2, or limma-voom.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - tximport
  - readr
  - salmon
  - tximeta
  - edgeR
  - DESeq2
  - limma-voom
derived_from:
- doi: 10.12688/f1000research.7563.1
  title: tximport
evidence_spans:
- Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages
- Importing transcript abundance with tximport
- While tximport works without any dependencies, it is significantly faster to read in files using the readr package
- significantly faster to read in files using the readr package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tximport
    doi: 10.12688/f1000research.7563.1
    title: tximport
  dedup_kept_from: coll_tximport
schema_version: 0.2.0
---

# salmon-output-parsing

## Summary

Parse and import salmon transcript-level quantification files (quant.sf.gz) into R-compatible data structures for downstream summarization to gene-level counts, abundance, and length matrices. This skill bridges pseudoalignment-based RNA quantification and statistical analysis by automating format conversion and aggregation.

## When to use

When you have salmon quant.sf.gz output files from pseudoalignment-based transcript quantification and need to convert transcript-level abundance estimates and counts into gene-level matrices for differential expression analysis with edgeR, DESeq2, or limma-voom.

## When NOT to use

- Input is already gene-level counts or a feature table (use directly for downstream analysis instead)
- Transcript-level differential analysis is the primary goal (use txOut=TRUE parameter or alternative transcript-level method)
- Quantification was performed with alignment-based tools (e.g., featureCounts, HTSeq) rather than pseudoalignment (use those tools' output directly)

## Inputs

- salmon quant.sf.gz files (transcript-level quantification output)
- tx2gene mapping data.frame or file (transcript ID to gene ID associations, typically from Gencode GTF)

## Outputs

- gene-level abundance matrix (TPM)
- gene-level counts matrix (estimated counts)
- gene-level length matrix (average transcript length weighted by sample-specific abundance)

## How to apply

Load salmon quantification files using the tximport function with type='salmon' argument, providing a tx2gene mapping data.frame that associates transcript IDs to gene IDs. tximport automatically parses the quant.sf.gz format and extracts transcript-level abundance (TPM), estimated counts, and effective transcript length. The function then aggregates these estimates to gene-level by summing counts across isoforms and computing length-weighted average transcript lengths per gene. The 'length' matrix output serves as an offset for downstream differential analysis, correcting for potential changes in gene length across samples from differential isoform usage.

## Related tools

- **tximport** (primary tool for parsing salmon quant.sf.gz files and summarizing to gene-level matrices) — https://github.com/thelovelab/tximport
- **readr** (optional dependency to accelerate file reading performance)
- **salmon** (upstream pseudoalignment quantification tool that produces quant.sf.gz files)
- **tximeta** (extended alternative offering same functionality plus automatic annotation metadata addition)
- **edgeR** (downstream differential analysis package accepting tximport gene-level matrices)
- **DESeq2** (downstream differential analysis package accepting tximport gene-level matrices)
- **limma-voom** (downstream differential analysis package accepting tximport gene-level matrices)

## Examples

```
tx2gene <- read.csv('tx2gene.gencode.v27.csv'); txi <- tximport(files = c('sample1.quant.sf.gz', 'sample2.quant.sf.gz'), type = 'salmon', tx2gene = tx2gene)
```

## Evaluation signals

- Output list contains exactly three named elements: 'abundance', 'counts', and 'length'
- All three matrices have identical row names (gene IDs) and column names (sample identifiers)
- Matrix dimensions match: rows = unique genes in tx2gene mapping, columns = number of input salmon files
- Abundance values are positive and in TPM scale (typically sum to ~1 million per sample)
- Counts are non-negative integers after rounding; length values are positive and represent effective transcript length in base pairs
- No missing values (NA) in output matrices, indicating complete transcript-to-gene mapping coverage

## Limitations

- Requires a pre-constructed tx2gene mapping with all transcripts in salmon quantification present; missing transcripts will cause import failure or incomplete summarization
- Cannot recover strand or exon-level information from salmon quant.sf.gz files alone; full GTF annotation needed separately if strand-aware analysis required
- Transcript abundance aggregation assumes transcript IDs in salmon output exactly match tx2gene mapping identifiers (case-sensitive, version-sensitive)

## Evidence

- [methods] tximport with type='salmon' successfully parses quant.sf.gz files: "Read the six salmon quantification files (quant.sf.gz) using tximport with type='salmon' argument."
- [intro] tx2gene mapping is required for gene-level aggregation: "Transcripts need to be associated with gene IDs for gene-level summarization. If that information is present in the files, we can skip this step... We first make a data.frame called tx2gene with two"
- [intro] Output is a list of three matrices: abundance, counts, and length: "A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level"
- [intro] Length matrix can be used as offset for differential analysis: "The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices"
- [intro] tximport corrects for differential isoform usage across samples: "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [readme] tximport imports transcript-level estimates and summarizes to matrices: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom."
- [intro] readr improves file reading performance: "it is significantly faster to read in files using the readr package"
