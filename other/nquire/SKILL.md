---
name: nquire
description: Use when making raw HTTP, E-utilities, PubChem, datasets, or FTP requests through the low-level EDirect transport wrapper.
disable-model-invocation: true
user-invocable: true
---

# nquire

Low-level EDirect transport wrapper for HTTP and FTP requests. It can issue GET or POST requests, expose EUtils and PubChem shortcuts, list or download FTP content, and optionally use Aspera when configured.

## Quick Start

- **Command:** `nquire`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/nquire`
- **Observed version:** `24.0`

## When To Use This Tool

- Send raw requests to NCBI E-utilities, PubChem PUG/PUG View, or NCBI Datasets endpoints.
- Fetch XML, JSON, or plain-text payloads before parsing them with `xtract` or `transmute`.
- Use the low-level EDirect HTTP / FTP layer instead of a higher-level wrapper such as `ecollect`.
- List or download remote files when an EDirect workflow needs FTP-style access.

## Common Patterns

```bash
# 1) Check the installed nquire version
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
nquire -version
```

```bash
# 2) Fetch NCBI database metadata with a direct GET request
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
nquire -get https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi |
sed -n '1,20p'
```

```bash
# 3) Use the built-in EUtils shortcut instead of spelling out the base URL
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
nquire -eutils esearch.fcgi -db pubmed -term 'tn3 transposition immunity'
```

## Recommended Workflow

1. Decide whether the endpoint expects POST (`-url`) or GET (`-get`) before constructing the request.
2. Prefer built-in shortcuts such as `-eutils`, `-pubchem`, `-pugrest`, or `-datasets` when they match your target service.
3. Smoke-test one request and inspect the raw payload before building a larger parser or downloader around it.
4. Pipe successful responses into `xtract`, `transmute`, or downstream shell filters only after the transport layer is behaving predictably.

## Guardrails

- `-h` and `--help` both print the same built-in usage text; `-version` returns the plain string `24.0`.
- This wrapper appends its own bin directory to `PATH`, so sibling EDirect helpers remain discoverable even when you invoke it by absolute path.
- `-url` means HTTP POST, while `-get` means HTTP GET. Mixing them up is an easy way to get confusing server responses.
- FTP-style listing is not always reliable in the current environment. A live `-lst ftp://ftp.ncbi.nlm.nih.gov/...` smoke test failed here with `curl: (56) response reading failed`.
- Optional Aspera downloads (`-asp`) depend on a working client install and can be disabled with `EDIRECT_NO_ASPERA=true`.
- Hidden environment knobs such as `NQUIRE_HELPER`, `NQUIRE_TIMEOUT`, and `NQUIRE_IPV4` can change transport behavior, so record them in reproducible workflows if you use them.
