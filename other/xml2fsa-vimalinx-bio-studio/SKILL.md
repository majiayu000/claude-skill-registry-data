---
name: xml2fsa
description: Use when converting NCBI XML sequence records to FASTA format, typically after fetching data with efetch from the Entrez Direct toolkit.
disable-model-invocation: true
user-invocable: true
---

# xml2fsa

## Quick Start

- **Command:** `efetch ... -format gbc | xml2fsa > records.fasta`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/xml2fsa`
- **Full reference:** See [references/help.md](references/help.md) for detailed usage

## When To Use This Tool

- Convert INSDSeq-style NCBI XML sequence records into FASTA.
- Flatten `efetch` XML output into headers and plain sequence strings for downstream sequence tools.
- Extract accession/definition-based FASTA entries without writing a custom `xtract` command.

## Common Patterns

```bash
# 1) Convert streamed INSDSeq XML into FASTA
cat records.xml | xml2fsa > records.fasta
```

```bash
# 2) Pipe efetch-style XML straight into FASTA output
efetch -db nuccore -id ABC123.1 -format gbc | xml2fsa > ABC123.fasta
```

## Recommended Workflow

1. Start from INSDSeq-style XML, usually streamed from `efetch` or another NCBI XML source.
2. Pipe that XML into `xml2fsa`; the wrapper itself is stdin-driven.
3. Inspect the first FASTA header to confirm the accession / definition mapping looks right.
4. Send the resulting FASTA into downstream alignment, indexing, or QC tools.

## Guardrails

- The wrapper is a fixed `xtract` command over `INSDSeq`; it is not a general XML-to-FASTA converter.
- It does not pass through positional filenames, so stdin / pipes are the reliable invocation path.
- `xtract` must be available on `PATH`, and `--help` / `--version` just fall through to xtract-style input errors.
- FASTA headers are constructed from the first available accession/id/locus field plus the definition line, so spot-check headers before batch use.
