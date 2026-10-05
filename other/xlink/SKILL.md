---
name: xlink
description: Use when following local EDirect link relations such as PubMed `CITED`, `CITES`, or `PMCID` from an incoming UID stream or `ENTREZ_DIRECT` message.
disable-model-invocation: true
user-invocable: true
---

# xlink

Local link resolver built on `xcommon.sh`, `xlink.ini`, and `rchive -link`. It reads UIDs from stdin, `-id`, `-input`, or an upstream `ENTREZ_DIRECT` message, follows a named link target, and emits either raw linked UIDs or a wrapped local result set for the destination database.

## Quick Start

- **Command:** `xlink -target <link-name>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/xlink`
- **Critical environment:** `EDIRECT_LOCAL_ARCHIVE`

## When To Use This Tool

- Traversing record-to-record links inside a prepared local EDirect archive
- Moving from one UID set to another after `xsearch`, `xfilter`, or manual ID input
- Translating link targets into the destination database defined in `xlink.ini`
- Working with PubMed citation or PubMed Central link-outs in the `x*` local stack

## Common Patterns

```bash
# Follow PubMed citation links in the local archive
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
xsearch -db pubmed -query 'Havran W* [AUTH]' | xlink -target CITED
```

```bash
# Jump from PubMed IDs to linked PMC IDs
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
printf '2539356\n' | xlink -db pubmed -target PMCID -raw
```

```bash
# Feed linked IDs into the next local step
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
xsearch -query 'dna repair' | xlink -target CITED | xfetch
```

## Recommended Workflow

1. Set `EDIRECT_LOCAL_ARCHIVE` and make sure the upstream step is producing valid local UIDs or an `ENTREZ_DIRECT` message.
2. Supply the source database with `-db` when it is not already encoded in the incoming message; otherwise the script falls back to `pubmed`.
3. Choose a link target such as `CITED`, `CITES`, or `PMCID`.
4. Keep wrapped output for downstream `x*` stages, or add `-raw` if the next command wants plain UIDs.

## Guardrails

- This is a local link-following tool, not a remote Entrez elink client.
- `-target` is mandatory; the script exits with `ERROR: Insufficient arguments given to xlink` if you do not supply it.
- Source inspection shows `xlink.ini` currently maps `[pubmed] CITED=pubmed`, `CITES=pubmed`, and `PMCID=pmc`.
- Without `-raw`, linked UIDs are wrapped in `ENTREZ_DIRECT` XML using the destination database from `xlink.ini`; with `-raw`, plain linked UIDs are sent to stdout.
- The script accepts input from `-id`, `-input`, stdin, or an upstream `ENTREZ_DIRECT` message parsed by shared `xcommon.sh` helpers.
- A configured local postings/archive installation is still required before link traversal works.
