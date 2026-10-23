---
name: revisit-followups
description: Find verified deferred work in completed changes and instructions.
---

# Revisit follow-ups

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/revisit-followups/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use to turn explicit deferred work into a curated backlog. Read local `AGENTS.md`,
issue policy, and review-record conventions first.

1. Confirm the requested lookback window and collect only explicit deferred-action signals from
   completed changes, repository instructions, and closed work records.
2. Reject settled decisions, standing policy, completed checklists, and incidental TODO-like text.
   A zero-candidate result is valid.
3. Verify each remaining candidate against the current base, its history, closed-work disposition,
   existing issues, and active changes before proposing new work.
4. Group related candidates into self-contained issue drafts that preserve the original evidence and
   explain why the work remains needed.
5. Remain read-only unless the caller or consumer wrapper explicitly authorizes issue creation. If
   authorized, route every candidate through
   [github-issue](../github-issue/SKILL.md), including its denied-external tracking behavior; do not
   duplicate repository or label authorization. Then clean up temporary collection artifacts and
   report skipped, covered, and created items.

## Scope and collection

- Accept a duration (`1w`, `2d`, `1m`) or ISO date. If absent, ask, proposing a one-week default,
  then compute a date-only cutoff and fetch the base remote.
- Treat comments on changes and issues as opt-in sources; bodies are the default.
- Collect bodies first: for closed issues, unchecked boxes and partial numbered work lists are
  candidates, and comments are fetched only for body candidates unless comments were requested. Do
  not exclude a whole plan issue or rely on a fixed heading allowlist.
- Search merged and closed work with `--limit 500`. A full page is truncation, not exhaustion: split
  the date range at its midpoint, retaining both bounds for interior chunks; only the top-level
  final chunk may be open-ended.
- Keep splitting a full single day by timestamp (search dates accept ISO-8601 times); report
  truncation only when the smallest timestamp bucket is still full.
- Use an OS-temp scratch directory with separate candidate and verdict files; each delegated
  collector gets its own file, and never append concurrently. Do not print fetched bodies outside
  scratch files, and remove all scratch files after collection.

Consumer wrapper owns: review journal format, default lookback, hosting provider, repository,
issue taxonomy, and confirmation mechanism.
