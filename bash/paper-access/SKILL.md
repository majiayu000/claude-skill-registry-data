---
name: paper-access
description: Use when an agent needs to resolve OA URLs, probe PDF endpoints, and download local paper artifacts from DOI or URL inputs.
---

# Paper Access

## Overview

Resolve paper access paths and download local artifacts from explicit DOI and URL inputs. URL resolution prefers upstream `open_access_pdf_url`, then `oa_url`, then Unpaywall fallbacks. The script writes a canonical `access_result.json` plus one local artifact per document.

## When to Use

Use this skill when:
- a paper candidate already exists and the next step is acquisition
- an upstream retriever already exposed `open_access_pdf_url` or `oa_url`
- an agent needs OA resolution from DOI metadata
- a downloader must verify whether a URL really serves a PDF

Do not use this skill for parsing.

## Execution

```bash
python scripts/run_skill.py \
  --workspace-root . \
  --execution-cwd "$PWD" \
  --script skills/paper-access/scripts/paper_access.py -- \
  --request-json /path/to/request.json \
  --output-dir /tmp/paper-access-out
```

Read `references/contracts.md` for request examples and environment variables.

Downstream callers should read `access_result.json` and gate later steps on:
- `source_url_kind`
- `artifact_kind`
- `is_readable_local_pdf`
