---
name: asn2ref
description: Use when converting `Seq-entry` ASN.1/XML-like citation content into compact `CITATION` XML blocks for EDirect-style matching workflows.
disable-model-invocation: true
user-invocable: true
---

# asn2ref

## Quick Start

- **Command:** `PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH /home/vimalinx/miniforge3/envs/bio/bin/asn2ref < seq_entry.xml`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/asn2ref`
- Full reference: [references/help.md](references/help.md)

## When To Use This Tool

- Extract accession and citation metadata from `Seq-entry` records.
- Reformat nested article / journal metadata into compact `CITATION` XML blocks.
- Prepare citation payloads for downstream EDirect tools such as `cit2pmid`.

## Common Patterns

```bash
# 1) Convert Seq-entry records into compact citation XML
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/asn2ref \
  < seq_entry.xml
```

```bash
# 2) Pipe the result into downstream citation-matching logic
upstream_seq_entry_command | \
  PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/asn2ref
```

## Recommended Workflow

1. Start from `Seq-entry` content that still contains publication metadata.
2. Run `asn2ref` as a stdin-driven filter.
3. Inspect the emitted `CITATION` XML for `ACCN`, `FAUT`, `LAUT`, `TITL`, `JOUR`, `VOL`, `ISS`, `PAGE`, and `YEAR`.
4. Pass the compact citation XML into later citation-matching steps only after confirming the key fields survived extraction.

## Guardrails

- This wrapper is just an `xtract` recipe; it depends on sibling EDirect tools being available on `PATH`.
- Output is compact XML-like citation data, not human-readable reference text.
- `PAGE` is normalized to the first page number only.
- There is no dedicated help or version mode.
