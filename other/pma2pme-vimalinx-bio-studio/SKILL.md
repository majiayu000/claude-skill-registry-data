---
name: pma2pme
description: Use when converting `PubmedArticle` XML into `Pubmed-entry` ASN.1 text, or into the intermediate XML form used before final ASN.1 emission.
disable-model-invocation: true
user-invocable: true
---

# pma2pme

## Quick Start

- **Command:** `efetch -db pubmed -id <PMID> -format xml | pma2pme`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/pma2pme`
- **Primary modes:** default ASN.1 text, `-xml` for intermediate XML, `-std` or `-ml` for author encoding style

## When To Use This Tool

- Convert PubMed XML into `Pubmed-entry` records for older NCBI / EDirect archival or interchange workflows.
- Choose between Medline-style author strings (`-ml`, default) and split standard author fields (`-std`).
- Inspect the intermediate XML structure before the final ASN.1 rendering step.
- Stay in a shell / EDirect pipeline instead of rewriting the transformation in another language.

## Common Patterns

```bash
# 1) Default Pubmed-entry ASN.1 text
efetch -db pubmed -id 2539356 -format xml | pma2pme
```

```bash
# 2) Use standard split author fields instead of Medline-style names
efetch -db pubmed -id 2539356 -format xml | pma2pme -std
```

```bash
# 3) Keep the intermediate XML instead of flattening to ASN.1
efetch -db pubmed -id 2539356 -format xml | pma2pme -xml
```

## Recommended Workflow

1. Fetch one or more `PubmedArticle` records as XML with `efetch`.
2. Pick the author style deliberately: default `-ml` for Medline-like compact names, or `-std` for separate last name / initials fields.
3. Use `-xml` when debugging transformations or when another XML-aware step should consume the record before ASN.1 conversion.
4. Validate the generated identifiers, title, journal block, and author representation before archiving the output.

## Guardrails

- The wrapper reads XML from stdin and does not fetch PMIDs on its own.
- There is no built-in `--help` or `--version`; unknown arguments fail with `Unrecognized argument ...`.
- Default behavior is `-ml` plus ASN.1 output; `-asn` merely reasserts the default final rendering mode.
- `-xml` skips the last `xtract` flattening step and returns the intermediate XML record instead of ASN.1 text.
- Accepted author-style flags include `std/-std/-STD` and `ml/-ml/-ML`.
- The wrapper depends on EDirect helpers such as `transmute` and `xtract` being available on `PATH`.
