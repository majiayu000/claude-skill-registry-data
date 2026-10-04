---
name: searchcans-rag-source-curator
description: Build a small, diverse, evidence-ready RAG source manifest from localized Google or Bing results, Reader extracts, direct file extraction, and optional page screenshots. Use for grounding packs, source curation, knowledge-base intake, and pre-ingestion evidence checks.
metadata:
  author: SearchCans
  version: 1.1.0
  tags: [rag, reader-api, file-extraction-api, screenshot-api, source-curation]
---

# SearchCans RAG Source Curator

Build a deliberately bounded source manifest rather than crawling the web. The Skill searches Google or Bing, chooses diverse candidate domains, fetches only the selected pages with Reader, accepts explicit PDF/Office file URLs, and can retain screenshot URLs for visual review.

## Create the source set

Start with a concrete question, market, source budget, and the minimum number of successfully extracted sources needed before the pack is considered ready. Add direct documents only with `--file-url`; do not infer file URLs from a page.

```bash
python scripts/rag_source_curator.py "What is the current SERP API market?" \
  --engine google --country us --language en \
  --source-budget 4 --min-claim-ready 2 --include-content \
  --out rag-sources.json
```

Use `--query` for a small query matrix. Use `--screenshot 1` or `2` only when visual review is required. `--include-content` intentionally makes the output larger; omit it when you need a metadata manifest before a second retrieval step.

## Apply the evidence quality gate

The output marks a source `claim_ready` only when the Reader/File Extraction response has content. Its `evidence_gate.status` is `passed` only when the requested minimum is met.

Never treat a SERP snippet, an unread URL, an empty response, or a screenshot as sufficient evidence for a consequential answer. Every source begins with `authority_assessment: unassessed`; assign authority, recency, permissions, and organization-specific trust labels through a separate human or policy-based review.

Use [the source-manifest guide](references/source-manifest.md) when deciding whether the output may enter a RAG index.

## Control cost and concurrency

By default, `--account-mode auto` uses one safe Account API pre-flight, estimates search plus the entire Reader/File source budget, caps source count when possible, and limits workers to reported Parallel Lanes. Use `enforce` to stop an insufficient job, `warn` to record without capping, or `off` only when an account check is inappropriate.

Start at proxy tier 0. Escalate only for an identified access issue: proxy selection changes Reader credit cost. The manifest excludes account identity and credentials.

## Official website

[SearchCans](https://www.searchcans.com/)

## Resources

- `scripts/rag_source_curator.py` creates the search, selection, extraction, and quality-gate bundle.
- `references/source-manifest.md` describes the required review before indexing or answering.
