---
name: github-repo-mining
description: Mine shortlisted repositories for code-level patterns (devcontainer, mise, CI, setup, policy) using strict query qualifiers and evidence-backed PatternRecords.
---

# GitHub Repo Mining

## Overview

Use this skill for Phase B/C repository deep extraction.
Focus on code and workflow evidence, not README claims.

## Query Grammar

Repository discovery queries must include:
- `stars:>N`
- `pushed:>=YYYY-MM-DD`
- `archived:false`
- topical tags where available (`topic:devcontainer`, `topic:dotfiles`, `topic:chezmoi`, `topic:mise`).

Code queries must include qualifiers like:
- `path:.devcontainer`
- `content:mise`
- `content:chezmoi`
- `.github/workflows`

## Required Outputs

Write:
- `reports/research-ros/<date>-phase-b-repo-mining.md`
- `reports/research-ros/<date>-pattern-records.jsonl`

Records must match `docs/research/schemas/pattern-record.schema.json`.

## Scoring Rubric

Score 1-5 for:
- bootstrap idempotency
- devcontainer maturity
- CI verification depth
- toolchain authority
- policy enforceability

Include `adopt|adapt|reject` recommendation per pattern with portability risk.

## Exit Criteria

- Minimum 10 repositories mined.
- Minimum 5 high-confidence portable patterns.
