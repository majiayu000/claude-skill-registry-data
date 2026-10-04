---
name: paper-retrieval
description: Use when an agent needs to search scholarly APIs, normalize paper metadata, deduplicate hits, and return a portable ranked candidate list without relying on ChemQA runtime state.
---

# Paper Retrieval

## Overview

Search OpenAlex, Semantic Scholar, and Crossref from a self-contained script. The output is a normalized candidate list plus diagnostics and provider health.

## When to Use

Use this skill when:
- the task starts from a research question or search query
- an agent needs literature candidates outside the current repo workflow
- normalized DOI/title/year/authorship metadata is needed for later access or parsing steps

Do not use this skill for downloading or parsing documents.

## Execution

```bash
python scripts/run_skill.py \
  --workspace-root . \
  --execution-cwd "$PWD" \
  --script skills/paper-retrieval/scripts/paper_retrieval.py -- \
  --query "Pt/C HER alkaline electrolyte" \
  --output-dir /tmp/paper-retrieval-out
```

Read `references/contracts.md` for request fields and environment variables.
