---
name: xsearch
description: Use when searching a local NCBI EDirect archive/postings index with Boolean, title, word, or pair queries inside the `x*` local-cache workflow.
disable-model-invocation: true
user-invocable: true
---

# xsearch

Local search front-end built on `xcommon.sh` plus `rchive`. It defaults to `pubmed`, supports `-query`, `-match`, `-exact`, `-title`, `-words`, and `-pairs`, and usually emits an `ENTREZ_DIRECT` wrapper unless you switch to `-raw` or use one of the direct `rchive` lookup modes.

## Quick Start

- **Command:** `xsearch -query "<search terms>"`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/xsearch`
- **Critical environment:** `EDIRECT_LOCAL_ARCHIVE`

## When To Use This Tool

- Searching a prepared local PubMed-style archive instead of the live NCBI service
- Building an `ENTREZ_DIRECT` UID set for downstream `xlink`, `xfilter`, or `xfetch` steps
- Running Boolean or fielded local queries such as `AND`, `NOT`, `[TREE]`, or `[YEAR]`
- Doing title-oriented lookup modes like `-title`, `-match`, `-exact`, `-words`, or `-pairs`

## Common Patterns

```bash
# Boolean query against the local archive
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
xsearch -db pubmed -query 'C14.907.617.812* [TREE] AND 2015:2018 [YEAR]'
```

```bash
# Title lookup
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
xsearch -title 'Genetic Control of Biochemical Reactions in Neurospora.'
```

```bash
# Emit raw UIDs instead of ENTREZ_DIRECT XML
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
xsearch -raw -query 'CRISPR AND 2024 [YEAR]'
```

## Recommended Workflow

1. Point `EDIRECT_LOCAL_ARCHIVE` at a valid local archive/postings root.
2. Pick the search mode that matches the lookup you need: `-query` for general Boolean search, `-title`/`-match`/`-exact` for title-style matching, or `-words`/`-pairs` for tokenized title scoring.
3. Use wrapped output for downstream `x*` tools, or add `-raw` when the next stage expects plain UID lines.
4. If a query fails immediately, verify the local postings directory before debugging the search syntax.

## Guardrails

- This is a local archive/postings tool, not a remote `esearch` replacement.
- `-h`/`-help` are safe and show usage examples; `-version` prints the EDirect version string.
- Live testing without `EDIRECT_LOCAL_ARCHIVE` failed with `Must supply path to local data by setting EDIRECT_LOCAL_ARCHIVE environment variable` followed by `Unable to get folder Postings for database pubmed`.
- Source inspection shows `-query` wraps UID hits in `ENTREZ_DIRECT` XML unless `-raw` is set; `-match`, `-exact`, and `-title` call `rchive` directly instead.
- `-words` and `-pairs` tokenize the query through `word-at-a-time` and `filter-stop-words`, then rank title hits with `sort-uniq-count-rank -n`.
- If you omit `-db`, the script defaults to `pubmed`.
