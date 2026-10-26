---
name: review
description: Run the multi-persona review board on the current changes — frontend architecture, UX, security, performance, and QA lenses — and consolidate findings by severity. Use before any PR, when the user says "review", "check my changes", "is this ready", or as the review phase of feature work. Subsumes the old /review command.
argument-hint: [optional: base ref (default main), or persona names to limit to]
allowed-tools: Read Grep Glob Bash(git diff*) Bash(git log*) Task
---

## Context

- Diff stat: !`git diff --stat ${ARGUMENTS:-main}...HEAD 2>/dev/null | tail -20 || git diff --stat HEAD`

## Task

Convene the review board on the current branch's changes (base: `$ARGUMENTS` or `main`) using the reviewer lenses in `docs/personas/`. This runs locally before merge — there is no cloud CI review (ADR-0008).

1. **Select reviewers by blast radius** (don't waste tokens on irrelevant lenses):
   - Any code → `frontend-architect`
   - User-visible UI/copy/animation → `ux-reviewer`
   - Native config, deps, env, storage, network, CI → `security-engineer`
   - Lists, animations, re-renders, heavy screens → `performance-engineer`
   - Tests, features, CUJ-touching changes → `qa-engineer`
2. **Dispatch the board.** Prefer the `code-reviewer` subagent (`.claude/agents/code-reviewer.md`), which adopts each persona in `docs/personas/` in turn — running it as a subagent keeps this conversation's context clean. For a focused pass you may adopt only the selected personas inline. Each persona reads its own file first and follows its required finding format.
3. **Consolidate** into one report, deduplicated, ordered P1 → P3, each finding with `file:line` and a concrete fix:

```
## Review board — <branch> vs <base>
Verdicts: arch ✗/✓ · ux ✓ · security ✓ · perf ✓ · qa ✓
### P1 (fix now)   ### P2 (fix or ticket)   ### P3 (follow-up)
[P1] path:line — issue — fix
```

4. **Drive resolution.** Offer to fix P1/P2 findings now (or hand to `/implement-feature`); apply approved fixes and re-run `npm run verify`. List P3s for the PR's follow-ups section. A finding you disagree with → argue it explicitly in the report, don't silently drop it; the human reviewer arbitrates.
5. **Encode repeats.** Any finding a persona has now raised twice across PRs is harness debt → end with a `HARNESS:` proposal and run `/encode-lesson` for it.

This board runs _before_ human review so humans spend attention on intent and taste, not on catchable defects.
