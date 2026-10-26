---
name: feature-report
description: Generate the evidence report for a feature — diff summary, Argent screenshots, AC-to-test traceability, verification verdicts — into docs/reports/NNN-slug.md (Markdown, the artifact PMs and reviewers actually read). Use when feature work is verified and the user says "report", "feature report", "document what we did", or as the reporting phase before a PR.
argument-hint: [spec number or slug]
allowed-tools: Read Write Glob Grep Bash(git diff*) Bash(git log*) Bash(cp *) Bash(mkdir *)
---

## Context

- Branch & changes: !`git branch --show-current && git diff --stat main...HEAD | tail -5`

## Task

Produce `docs/reports/<NNN-slug>.md` for **$ARGUMENTS** (Markdown only — no PDF), following the exact structure in `docs/reports/README.md`.

1. **Gather inputs:** the spec folder (spec/plan/tasks), the real diff (`git diff main...HEAD`, plus `git log --oneline main...HEAD`), the `/verify-ui` attestation, and the Argent screenshots captured during verification. No screenshots → stop and run `/verify-ui` first; a report without evidence is marketing.
2. **Curate evidence:** `mkdir -p docs/reports/<slug>/img` and copy ONLY the screenshots referenced by the report into it (the ephemeral `reports/` scratch dir stays gitignored). Reference them with relative paths. `docs/reports/` is excluded from docs-lint, so report internals won't block the gate.
3. **Write the report** — sections in the README order: header (spec link, branch, date) · what & why (3 sentences from the spec, no marketing) · **AC → evidence table** (every AC: the test that proves it + the Argent screenshot + verdict — this table is the report's reason to exist) · screenshots with one-line captions (before/after when modifying existing UI; include empty/loading/error/offline) · changes by layer (`app`/`features`/`shared`) with notable decisions from the actual diff · verification summary (`npm run verify`, Maestro/Argent results, persona verdicts from `/review`) · follow-ups (declined P3s, ticketed items).
4. **Honesty rules:** verdicts come from real runs, not optimism; unresolved issues appear under follow-ups, not omitted; numbers (files changed, tests added) come from `git`, not estimates.
5. **Link it:** reference the report in the PR description and in `specs/README.md`'s row for this spec. Mirror the summary to the Notion project's Feature Specs / GitHub page if the MCP is connected.

Write for a reader who was on holiday during the work: by the end they know what shipped, proof it works, and what's consciously left open.
