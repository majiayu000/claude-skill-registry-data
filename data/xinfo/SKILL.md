---
name: xinfo
description: Use when inspecting fields, indexed terms, or term counts from a local EDirect postings index rather than the remote `einfo` endpoint.
disable-model-invocation: true
user-invocable: true
---

# xinfo

Local metadata and counts helper built on `xcommon.sh` plus `rchive`. It reports available postings fields, indexed terms, and count/totals summaries from a configured local postings directory.

## Quick Start

- **Command:** `xinfo -db <database> -fields`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/xinfo`
- **Critical environment:** `EDIRECT_LOCAL_ARCHIVE`

## When To Use This Tool

- Listing local postings fields for a database
- Counting or expanding indexed terms from a local archive setup
- Getting local totals for a field such as `PROP` or `YEAR`
- Debugging local postings contents rather than querying remote `einfo`

## Common Patterns

```bash
# Show help
xinfo -h
```

```bash
# List local fields
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
xinfo -db pubmed -fields
```

```bash
# Get local term counts
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
xinfo -db pubmed -count 'catabolite repress*'
```

## Recommended Workflow

1. Configure `EDIRECT_LOCAL_ARCHIVE` so the tool can discover the postings directory.
2. Start with `-fields` to confirm the local postings layout.
3. Move on to `-terms`, `-count`, `-counts`, or `-totals` once the field structure looks sane.
4. Treat failures as local-postings problems first, not as remote NCBI outages.

## Guardrails

- `-h`/`--help` are safe and show usage, but `--version` is not supported; locally it triggered the missing-path error and `ERROR: Unrecognized option --version`.
- This is a local postings tool, not a wrapper around remote `einfo`.
- Source inspection shows `-fields` literally changes into the postings directory and lists subdirectories, while `-count`/`-counts`/`-totals` delegate to `rchive`.
- In local testing without `EDIRECT_LOCAL_ARCHIVE`, `xinfo -db pubmed -fields` printed the missing-path error and then accidentally listed the current working directory because `cd "$postingsBase"` fell through with an empty path.
