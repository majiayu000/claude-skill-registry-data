---
name: ds2pme
description: Use when converting PubMed `DocumentSummary` XML into `Pubmed-entry` ASN.1 text, or into the intermediate XML form before final ASN.1 flattening.
disable-model-invocation: true
user-invocable: true
---

# ds2pme

## Quick Start

- **Command:** `efetch -db pubmed -id <PMID> -format docsum | ds2pme`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/ds2pme`
- **Primary modes:** default ASN.1 text, `-xml` for intermediate XML

## When To Use This Tool

- Convert PubMed `DocumentSummary` records, rather than full `PubmedArticle` XML, into `Pubmed-entry` structures.
- Stay inside a docsum-oriented EDirect workflow when ASN.1 text is the desired downstream format.
- Inspect the intermediate XML before the last flattening step when debugging or archiving conversions.
- Use a lighter-weight alternative to `pma2pme` when your upstream source is already docsum output.

## Common Patterns

```bash
# 1) Default Pubmed-entry ASN.1 text
efetch -db pubmed -id 2539356 -format docsum | ds2pme
```

```bash
# 2) Keep the intermediate XML instead of flattening to ASN.1
efetch -db pubmed -id 2539356 -format docsum | ds2pme -xml
```

```bash
# 3) Feed the result into another XML-aware EDirect step
efetch -db pubmed -id 2539356 -format docsum | ds2pme -xml |
xtract -pattern Pubmed-entry -element pmid_
```

## Recommended Workflow

1. Fetch PubMed records as `-format docsum`.
2. Use plain `ds2pme` when you need final ASN.1 text, or `-xml` when you want the structured intermediate.
3. Confirm that identifiers, title, journal, and article IDs look sensible before storing or reusing the output.
4. Switch to `pma2pme` instead if your upstream source is full `PubmedArticle` XML rather than docsum output.

## Guardrails

- The wrapper expects PubMed `DocumentSummary` XML on stdin, not full `PubmedArticle` input.
- There is no built-in `--help` or `--version`; unknown arguments fail with `Unrecognized argument ...`.
- Accepted mode switches are `xml/-xml` and `asn/-asn`.
- The default mode emits ASN.1 text beginning with `Pubmed-entry ::= {`.
- `-xml` stops before the final `xtract -pattern Pubmed-entry -element "."` flattening step.
- The wrapper depends on EDirect helpers such as `transmute` and `xtract` being on `PATH`.
