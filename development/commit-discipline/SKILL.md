---
name: commit-discipline
description: Use when committing work in Athena, when staged changes span more than one concern, or when writing a commit message — before running git commit.
---

# Commit Discipline

## Overview

House rule: **one concern per commit.** Do not entangle unrelated changes.
Every commit in the log is one reviewable decision — an ADR acceptance, a
feature increment, a fix — and later ADRs cite commits by hash as evidence
(e.g. "commit 3687d8d" in ADR-0012). An entangled commit breaks that audit
trail.

## Message style (match the existing log)

Conventional commits, lowercase, imperative, with a scope in parentheses
when one module owns the change; a one-line summary that states the decision,
not the diff. Real examples:

```
feat(research): COMPARE mode, mocked build — cited side-by-side, no ranking (ADR-0012)
docs(adr): accept ADR-0012 — COMPARE mode, cited side-by-side over a named set
perf(find): widen FIND recall knobs for the 84-company corpus
fix(edgar): robust section bounds — pipe headings, page headers, prose citations
chore: silence alembic path_separator deprecation warning
```

- Prefixes: `feat` `fix` `chore` `docs` `refactor` `test` `perf`
- Common scopes: `research`, `edgar`, `ingest`, `qa`, `adr`, `db`, `api`,
  `domain`, `retrieval`, `reference`, `repair`
- Cite the governing ADR (and section) in the summary or body when the
  commit implements one.
- ADR acceptance is its own `docs(adr): accept …` commit, separate from the
  implementation commit.

## Splitting entangled work

1. `git status` and `git diff` first — know what's actually in the tree;
   leave other sessions' in-progress files (e.g. apps/web) alone.
2. Stage by path for file-level splits: `git add <files-for-concern-A>`.
3. Stage by hunk when one file mixes concerns: `git add -p <file>`
   (interactive `-i` is unavailable in Claude Code; `-p` works).
4. Commit concern A; repeat for concern B. Verify each commit stands alone
   (`git show --stat`).
5. Drive-by fixes discovered mid-task get their own commit, not a ride-along.

## Red flags

- "and" doing heavy lifting in the summary line ("add X and fix Y").
- `git add .` / `git add -A` when the tree contains unrelated changes.
- A `feat` commit that also reformats untouched files or tweaks docs.
- Committing a migration in the same commit that accepts its ADR.
