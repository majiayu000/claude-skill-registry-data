---
name: pmc2info
description: Use when converting PubMed Central article XML into normalized PMCInfo XML for local archive building or section-aware downstream parsing.
disable-model-invocation: true
user-invocable: true
---

# pmc2info

EDirect shell pipeline that converts PMC `<article>` XML into a normalized `PMCInfo` XML record set. It extracts citation metadata, title, abstract, authors, license text, and section passages, then normalizes common section titles such as introduction, results, and methods.

## Quick Start

- **Command:** `pmc2info`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/pmc2info`
- **Environment prerequisite:** add `/home/vimalinx/miniforge3/envs/bio/bin` to `PATH` so `xtract`, `transmute`, and related EDirect helpers are available

## When To Use This Tool

- Convert PMC full-text XML into `PMCInfo` XML for archive or indexing workflows.
- Extract normalized article metadata and sectioned text from PMC articles.
- Process PMC XML fetched by `efetch -db pmc -format xml` or extracted from open-access tar archives.
- Use this when you need PMC full text; do not use it for PubMed `PubmedArticle` XML.

## Common Patterns

```bash
# 1) Convert one PMC article fetched live from NCBI
export PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH

efetch -db pmc -id 6260607 -format xml | pmc2info > article.pmcinfo.xml
```

```bash
# 2) Convert PMC article XML streamed from an OA archive tarball
export PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH

tar -xOzf oa_bundle.tar.gz --to-stdout | pmc2info > batch.pmcinfo.xml
```

```bash
# 3) Inspect the first part of the normalized PMCInfo output
export PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH

efetch -db pmc -id 6260607 -format xml | pmc2info | sed -n '1,40p'
```

## Recommended Workflow

1. Start from PMC article XML, either via `efetch -db pmc -format xml` or an extracted OA archive payload.
2. Activate the bio environment or export the EDirect bin directory into `PATH` before invoking the wrapper.
3. Inspect one converted article first to verify the expected `PMCInfo` structure, citation block, and normalized passage labels.
4. Scale to bulk conversion only after confirming the section mapping and output schema meet your downstream parser's expectations.

## Guardrails

- There is no real help mode. With dependencies available, `pmc2info -help` still runs the pipeline and errors only because no XML input was supplied.
- Without the bio bin directory on `PATH`, the live failure is a series of `xtract: command not found` and `transmute: command not found` messages.
- With dependencies available but no XML input, the live failure is `No data supplied to xtract from stdin or file`.
- This script expects PMC `<article>` XML, not PubMed `PubmedArticle` or DocumentSummary XML.
- Section normalization is driven by an internal title map for common headings such as `introduction`, `results`, `discussion`, `materials and methods`, and `statistical analysis`. Unmapped headings pass through less cleanly.
