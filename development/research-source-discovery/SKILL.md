---
name: research-source-discovery
description: Build candidate source pools for implementation research using source-priority MCP stacks (GitHub, Reddit, HN, curated lists, blogs/news, optional X API) with logged query packs and shortlist rationale.
---

# Research Source Discovery

## Overview

Use this skill to run Phase A candidate discovery for engineering research tasks.
The objective is breadth with traceability: every query and shortlist decision must be logged.

## Source Priority

1. GitHub (`github` / `github-official`) for repository and code discovery.
2. Reddit and Hacker News (`mcp-reddit`, `mcp-hackernews`) for implementation lessons.
3. Curated lists (awesome lists and tool indexes).
4. Blog/news discovery (`brave`, `kagisearch`, `dappier`).
5. X via API (`mcp-api-gateway`) when credentials are available.

Do not start from generic web search unless higher-priority sources are blocked.

## Required Outputs

Write:
- `reports/research-ros/<date>-phase-a-candidates.md`
- `reports/research-ros/<date>-discovery-records.jsonl`

Records must match `docs/research/schemas/discovery-record.schema.json`.

## Discovery Rules

- Log full query strings.
- Prefer recency (`pushed`, `since`) and quality constraints (stars, archived status, engagement thresholds).
- Deduplicate by canonical URL.
- Tag source class: `github`, `social`, `curated`, `blog`, `news`, `x`.

## Exit Criteria

- 50-150 candidate sources collected.
- At least 3 distinct source classes.
- Each candidate has shortlist reason and confidence.
