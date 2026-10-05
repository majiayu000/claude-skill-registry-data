---
name: pma2apa
description: Use when converting `PubmedArticle` XML from EDirect into APA-style citation text or APA-structured XML for downstream parsing.
disable-model-invocation: true
user-invocable: true
---

# pma2apa

## Quick Start

- **Command:** `efetch -db pubmed -id <PMID> -format xml | pma2apa`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/pma2apa`
- **Primary modes:** default one-line citation text, `-xml` for structured XML, `-ascii` for accent-normalized output

## When To Use This Tool

- Turn PubMed XML records into APA-style citation strings inside shell pipelines.
- Keep an intermediate XML representation of parsed citation fields when downstream `xtract` steps need structure.
- Normalize accented characters to ASCII before exporting to plain-text systems.
- Stay inside EDirect tooling after `efetch -format xml` instead of post-processing citations elsewhere.

## Common Patterns

```bash
# 1) Default APA citation line, prefixed by PMID
efetch -db pubmed -id 19212835 -format xml | pma2apa
```

```bash
# 2) Keep structured APA XML instead of flattening to one line
efetch -db pubmed -id 19212835 -format xml | pma2apa -xml
```

```bash
# 3) Force accent-normalized ASCII output
efetch -db pubmed -id 19212835 -format xml | pma2apa -ascii
```

## Recommended Workflow

1. Fetch `PubmedArticle` XML with `efetch -db pubmed -format xml`.
2. Decide whether you need flat citation text or the structured XML intermediate.
3. Add `-ascii` only when the downstream consumer cannot handle accented characters.
4. Check the emitted title, journal, pages, and DOI fields before storing or reusing the citation.

## Guardrails

- The tool reads `PubmedArticle` XML from stdin; it does not fetch PubMed records by itself.
- There is no built-in `--help` or `--version`; unknown arguments fail with `Unrecognized argument ...`.
- Accepted mode switches are the bare or dashed forms `xml/-xml`, `apa/-apa`, and `ascii/-ascii`.
- Default text mode emits a single tab-delimited line that starts with the PMID and then the formatted citation.
- `-xml` keeps the `<APASet><APAFormat>...</APAFormat></APASet>` intermediate instead of flattening to text.
- The wrapper depends on EDirect helpers such as `transmute` and `xtract` being available on `PATH`.
