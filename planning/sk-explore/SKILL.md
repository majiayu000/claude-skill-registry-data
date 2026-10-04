---
name: sk-explore
description: First-link discovery. Gather repo context and write a structured report that feeds into sk-alternatives or sk-planning.
---

# Explore

## When to use

- Starting work when the problem, scope, or repo context is unclear.
- The user asks to explore, research, or understand X in this repo.
- Before `sk-alternatives` or `sk-planning` when context is missing.

## Goal

Produce a self-contained `0 - EXPLORE.md` so the next phase can proceed without re-exploring.

## Slug and flow folder

1. Derive a short kebab-case slug from the goal (confirm with the user if not provided).
2. Create `.agents/flows/sk-<slug>/` if needed.
3. Create or update `RUNBOOK.md` with all phases `pending`; mark `0` as `in-progress`.
4. Write `0 - EXPLORE.md` and set row `0` to `done` with a one-line summary.
5. Add `.agents/flows/sk-*/` to `.gitignore` if this is the first flow in the repo.

## Output

`0 - EXPLORE.md` includes:

- **Goal**: restated scope.
- **Files and Context**: relevant files and inline facts.
- **Findings**: what exists, what's missing, patterns, constraints, edge cases.
- **Assumptions and Open Questions**: unknowns with acceptance impact.
- **Risks**: known blockers or high-risk areas.
- **Next Step Recommendation**: `sk-alternatives` or `sk-planning` with a one-line reason.

## Steps

1. **Clarify** — restate goal and scope. If ambiguity is high, ask or list assumptions.
2. **Search** — find relevant code, tests, docs, and config.
3. **Read** — inline the relevant snippets or facts.
4. **Synthesize** — summarize current state, constraints, and gaps.
5. **Recommend** — `sk-alternatives` if the approach is unclear, `sk-planning` if it is clear.
6. **Write** — save the report and update `RUNBOOK.md`.

Do not edit non-report files.
