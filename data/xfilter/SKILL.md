---
name: xfilter
description: Use when filtering a UID stream against a local postings index with a query expression in the `x*` local-archive toolchain.
disable-model-invocation: true
user-invocable: true
---

# xfilter

Local-postings filter built on `xcommon.sh`, `word-at-a-time`, and `rchive -query`. It consumes UIDs from stdin or command-line sources, applies a query expression against a local postings index, and emits either raw filtered UIDs or an `ENTREZ_DIRECT` wrapper message.

## Quick Start

- **Command:** `xfilter -query "<expression>"`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/xfilter`
- **Critical environment:** `EDIRECT_LOCAL_ARCHIVE`

## When To Use This Tool

- Filtering UIDs against a local postings index instead of using remote `efilter`
- Narrowing a local UID set with a query expression after `xfetch`/`xsearch`-style workflows
- Producing either raw UID output (`-raw`) or an `ENTREZ_DIRECT` XML wrapper for downstream local tools
- Working inside a fully local PubMed/PMC archive setup

## Common Patterns

```bash
# Filter a UID stream with a local query
printf '2539356\n' | xfilter -db pubmed -query 'dna repair'
```

```bash
# Emit raw UIDs instead of ENTREZ_DIRECT XML
printf '2539356\n' | xfilter -db pubmed -raw -query 'dna repair'
```

```bash
# Show usage
xfilter -h
```

## Recommended Workflow

1. Ensure the local postings environment is configured through `EDIRECT_LOCAL_ARCHIVE`.
2. Supply UIDs by `-id`, `-input`, stdin, or an upstream `ENTREZ_DIRECT` message.
3. Use `-query` with the local postings syntax you intend to test.
4. Add `-raw` only when a downstream stage expects plain UID lines instead of wrapper XML.

## Guardrails

- This is a local-postings query tool, not a remote Entrez filter.
- `-h`/`--help` are safe and show usage examples; `--version` is not supported and locally triggered the missing-path error plus `ERROR: Unrecognized option --version`.
- Source inspection shows `xfilter` always calls `FindPostingsFolder` before querying, so a valid local postings directory is mandatory.
- In live testing without local postings configured, `printf '2539356\n' | xfilter -db pubmed -query 'dna repair'` failed with `Unable to get folder Postings for database pubmed`.
- Query handling prepends `[PIPE] AND` in the common case, and UID input is tokenized through `word-at-a-time` before being sent to `rchive -query`.
