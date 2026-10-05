---
name: rchive
description: Use when building, indexing, or querying local XML record archives from NCBI Entrez databases, creating inverted indices, or managing PubMed local caches.
disable-model-invocation: true
user-invocable: true
---

# rchive

`rchive` is the EDirect local-archive workhorse. The shell script in `bin/` is only a platform dispatcher; it locates and execs a compiled binary such as `rchive.Linux`.

## Quick Start

- **Command:** `rchive`
- **Local wrapper:** `/home/vimalinx/miniforge3/envs/bio/bin/rchive`
- **Version path:** `rchive -version`

## When To Use This Tool

- Creating Entrez index XML from PubMed/Entrez records (`-e2index`)
- Generating inverted indices for fast term searching (`-e2invert`, `-merge`)
- Building local record caches with optional gzip compression (`-archive`, `-gzip`)
- Querying indexed archives with Boolean formulas (`-query`, `-title`, `-exact`)

## Common Patterns

```bash
# 1) Inspect available archive/index flags
rchive --help
rchive -version
```

```bash
# 2) Create Entrez index XML from input records
cat records.xml | rchive -strict -e2index
```

```bash
# 3) Query an existing local postings directory
rchive -path /data/postings -query 'brca1 AND breast'
```

## Recommended Workflow

1. Decide whether you are archiving raw XML (`-archive` / `-fetch`) or working on the index side (`-e2index`, `-e2invert`, `-merge`, `-promote`).
2. Verify the wrapper can find the platform binary with `rchive -version` before launching long archive jobs.
3. Feed valid XML from stdin or use `-input` when building indexes.
4. Separate archive storage, postings storage, and scratch space early because local-cache trees grow quickly.

## Guardrails

- `rchive -version` prints a clean `24.0`, but `rchive --version` is not equivalent; in local testing it fell through to a no-input error.
- The wrapper script resets `PATH` and then execs a platform-specific binary such as `rchive.Linux`; if that compiled binary is missing it prints download instructions instead of running.
- `--help` produced the full built-in help document in this environment, listing archive, index, query, and postings-management flags.
- This is an operational local-archive tool, not a harmless inspector. Many flags create, merge, or delete cache/index artifacts.
- XML-consuming modes require real stdin or `-input`; otherwise you can hit `No data supplied to rchive from stdin or file`.
