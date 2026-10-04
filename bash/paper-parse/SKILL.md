---
name: paper-parse
description: Use when an agent needs to parse a local paper PDF or text artifact into fulltext, sections, snippets, and an extraction report.
---

# Paper Parse

## Overview

Parse a local document into structured text artifacts. This skill is self-contained and assumes only a file path plus optional parser settings. The script always writes a canonical `parse_result.json` to the output directory.

The default PDF stack is an automatic three-layer fallback:
- Small files (up to 10 MB and 20 pages): MinerU Agent Lightweight API
- Larger files: MinerU Precision API when `MINERU_API_TOKEN` is configured
- Final local fallback: PyMuPDF

Text-like inputs do not use the PDF backends. A local `.txt`, `.md`, or `.html` artifact can be parsed even when `mineru` and `pymupdf` are not installed.

## When to Use

Use this skill when:
- a paper has already been downloaded locally
- the next step needs clean fulltext or section boundaries
- an agent needs portable parsing behavior outside the current ChemQA runtime

Do not use this skill for:
- remote paper search
- OA resolution or HTTP downloading

## Execution

Run the parser script with a local input path and output directory:

```bash
python <skill-root>/scripts/paper_parse.py \
  --input /path/to/paper.pdf \
  --output-dir /tmp/paper-parse-out
```

The script writes JSON to stdout and stores artifacts in the output directory, including `parse_result.json`.

For PDF parsing, `paper-parse` uses the official asynchronous MinerU Agent API
with signed file upload and polling. Larger documents use the Precision API
when a token is available. It falls back to PyMuPDF when a cloud backend is
unavailable, rate-limited, over its limits, or rejected by quality gates.

The Agent API and Precision API URLs can be overridden with `agent_api_url` and
`precision_api_url` in `--config-json`, or with `MINERU_AGENT_API_URL` and
`MINERU_PRECISION_API_URL`. Precision authentication reads the environment
variable named by `precision_token_env` (default `MINERU_API_TOKEN`).

The parser does not invoke a local `mineru` CLI or depend on a local
`mineru-api` process.

## Inputs And Outputs

- Input: local `.pdf` path or a UTF-8 text artifact such as `.txt`, `.md`, or `.html`
- Output: normalized `fulltext`, `sections`, `snippets`, extraction report, warnings, and parser metadata

Read `references/contracts.md` for the JSON contract and failure semantics.

## Failure Modes

- Text artifacts parse without importing PDF-only modules
- Invalid PDF header returns structured `fulltext_unusable`
- Agent/Precision extraction rejection or unavailability automatically triggers `PyMuPDF`
- If all cloud backends and PyMuPDF fail, the script returns structured `fulltext_unusable` with attempt metadata instead of crashing
