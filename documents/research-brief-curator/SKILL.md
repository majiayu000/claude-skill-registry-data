---
name: research-brief-curator
description: Curate public-source links, saved notes, newsletters, documentation updates, release notes, market signals, and research snippets into safe daily or weekly briefs with source tracking, public/private visibility labels, archive decisions, and human review. Use when the user asks to make a research brief, summarize saved links, build an AI news digest, organize reading notes, create a public-safe source roundup, prepare a weekly intelligence brief, or separate public-ready notes from private research without exposing credentials, raw prompts, logs, local paths, account data, client material, or private source lists.
---

# Research Brief Curator

## Overview

Use this skill to turn public links and approved notes into a short, reviewable research brief. Keep the source trail visible, label each item by visibility, and require human approval before anything is posted, sent, archived publicly, or reused as client-facing material.

## Workflow

1. Clarify the brief scope: topic, audience, time window, output format, and whether the brief is internal-only, public-ready, client-facing, or draft research.
2. Read `references/public-source-boundaries.md` before using user-provided links, notes, exports, screenshots, or copied text.
3. Normalize every item into a simple record: title, source, URL or citation, date, topic, visibility, status, summary, why it matters, and recommended next action.
4. Read `references/brief-template.md` before drafting the final daily or weekly brief.
5. Separate records into:
   - `public_ready`: safe to summarize with source link after review.
   - `needs_review`: claims, wording, or source quality need checking.
   - `private_research`: useful internally but not suitable for public reuse.
   - `archive`: duplicate, stale, or background material.
6. Draft the brief with source-aware language and short decision notes. Do not copy long excerpts from sources.
7. End with a safety verdict: `BLOCK`, `REVIEW`, or `READY`, plus the remaining manual checks.

## Optional Script

Use `scripts/build_brief_skeleton.py` when the user provides structured JSON records or wants a repeatable Markdown skeleton.

```bash
python scripts/build_brief_skeleton.py items.json --title "Weekly AI Research Brief" --date 2026-05-28 --output brief.md
```

The script does not fetch URLs or publish anything. It only formats provided records and flags suspicious local paths or credential-like terms for review.

## Safety Rules

- Use public links, user-approved notes, and fake examples only.
- Do not expose API keys, tokens, cookies, browser profiles, raw prompts, private source lists, logs, account data, dashboards, exports, local paths, client names, or private implementation details.
- Do not summarize paywalled, private, login-only, confidential, or internal-only material for public output unless the user explicitly confirms it is approved.
- Do not present uncertain claims as facts. Mark them `needs_review` and ask for source verification.
- Do not auto-post, auto-send, create public tickets, update a CMS, or push changes. Return a brief and review checklist.
- Keep quotes short and attribute them. Prefer paraphrase and links over copied text.

## Output Format

Return:

1. Safety verdict: `BLOCK`, `REVIEW`, or `READY`.
2. Brief title, date, audience, and source count.
3. Public-ready highlights with source links.
4. Needs-review items and why they are held.
5. Private-research or archive decisions.
6. Recommended next actions.
7. Manual review checklist before publishing or sharing.

If the user provides risky material, do not include it in the brief. Explain the minimum safe rewrite or redaction needed.
