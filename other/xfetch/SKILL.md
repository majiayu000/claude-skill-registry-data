---
name: xfetch
description: Use when retrieving records from a local EDirect archive via the `x*` local-cache stack, not when calling the remote NCBI `efetch` service directly.
disable-model-invocation: true
user-invocable: true
---

# xfetch

Local-archive fetch helper built on `xcommon.sh` plus `rchive`. It takes UIDs from `-id`, `-input`, stdin, or an `ENTREZ_DIRECT` message, then fetches matching records from a configured local archive/postings installation rather than from the live NCBI service.

## Quick Start

- **Command:** `xfetch -db <database> -id <uid>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/xfetch`
- **Critical environment:** `EDIRECT_LOCAL_ARCHIVE`

## When To Use This Tool

- Fetching records from a prepared local PubMed/PMC/etc. archive instead of the live E-utilities endpoint
- Streaming or turbo-fetching locally archived XML by UID
- Consuming UIDs from stdin or an upstream `ENTREZ_DIRECT` message and retrieving the matching local records
- Working inside a local/offline EDirect archive workflow

## Common Patterns

```bash
# Fetch one UID from a local archive
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
xfetch -db pubmed -id 2539356
```

```bash
# Read UIDs from stdin
printf '2539356\n' | xfetch -db pubmed
```

```bash
# Use stream mode against the local archive
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
xfetch -db pubmed -stream -input ids.txt
```

## Recommended Workflow

1. Point `EDIRECT_LOCAL_ARCHIVE` at a valid local archive root.
2. Supply `-db` plus a UID source (`-id`, `-input`, or stdin).
3. Use plain fetch mode for wrapped XML output or `-stream` when you want streamed archive content.
4. If the command prints wrapper XML but no records, debug the local archive/postings configuration before blaming UID parsing.

## Guardrails

- `xfetch` is a local-cache tool, not a remote `efetch` synonym.
- `-h`/`--help` are safe and show usage; `-version` works and prints `24.0`, but `--version` is unrecognized.
- In local testing without a configured archive, `xfetch -db pubmed -id 2539356` still printed the PubMed XML wrapper prologue/epilogue and then failed with `Insufficient command-line arguments supplied to rchive`.
- The script sources `xcommon.sh`, loads database-specific wrappers from `xfetch.ini`, and then delegates to `rchive -fetch` or `rchive -stream`.
- If `EDIRECT_LOCAL_ARCHIVE` is missing, the shared helper prints the missing-path error first.
