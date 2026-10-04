---
name: sentry-quick-wins
description: Use when the user wants to find and fix the easy bugs from Sentry first — "triage Sentry", "find quick wins", "what should I fix first from Sentry", "pull the top fixable bugs", "clear the easy ones before the hard ones". Fetches unresolved issues, ranks by impact while filtering noise, triages the best quick wins into an approval table, then fixes them one commit at a time.
---

# Sentry Quick Wins

Find the **quick wins** in Sentry — real user-facing bugs with a clear root cause and a small, low-risk fix — and clear them before the complex issues. Two phases with a hard stop between them: triage for approval, then fix.

A **quick win** is:
- a likely real, user-facing bug (not noise)
- root cause clear from the stack trace, breadcrumbs, route, request data, or surrounding code
- fixable with a small, low-risk change touching no more than ~2 files
- no API, schema, architecture, design, or product decision needed
- reproducible, or at least verifiable via the Sentry failing path plus a regression test
- low risk of expanding in scope

## Step 0: Confirm Sentry access

The Sentry MCP must be connected to *this* session — it is not always exposed even when configured globally. Make one small test call (search unresolved issues, limit a handful) and report how many unresolved issues you can see.

If no Sentry tool is available, stop and tell the user to connect the Sentry MCP. Do not fall back to anything else.

## Step 1 — Triage (Phase 1)

Fetch unresolved issues from the last 30 days. Scope to the project the user is working in if the MCP exposes more than one.

Rank by `event count × users affected` as the starting signal, then **down-rank noise**:
- bots, crawlers, browser extensions, third-party scripts (ads, analytics, pixels)
- flaky network errors, cancelled requests
- `ResizeObserver` / chunk-load / hydration errors with no actionable trace
- issues with no actionable stack trace

Select the **5 best quick wins** against the criteria above. For each candidate, call the issue-detail tool, inspect the stack trace and events, and map it to this repo's files and route/component.

Return a ranked table with these columns:

`rank` · `issue title` · `Sentry link` · `events` · `users affected` · `route/component` · `suspected root cause` · `repo files` · `proposed one-line fix` · `confidence (H/M/L)` · `hidden-complexity notes`

Then a **Skipped** section: issues that looked relevant but were rejected as noise, too vague, too risky, or not quick wins — one-line reason each. This is the audit trail; it proves the noise was examined, not silently dropped.

<HARD-GATE>
Stop after the table. Do NOT edit code, reproduce, or fix anything until the user approves which issues to take.
</HARD-GATE>

## Step 2 — Fix (Phase 2, only after approval)

Fix approved issues one at a time. For each:
- reproduce the issue, or cite the Sentry failing path that proves it
- make the smallest root-cause change — no broad refactors, no symptom-only patches. If the change starts touching more than ~2 files or needs a design call, it was not a quick win — drop it and say why
- add or update a regression test where practical
- run the relevant tests/checks
- one commit per fix (conventional-commit style; call the Skill tool with `commit-me` if you want the full commit workflow)
- summarize the diff and how you verified it
