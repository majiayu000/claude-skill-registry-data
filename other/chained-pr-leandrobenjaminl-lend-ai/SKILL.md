---
name: chained-pr
description: >
  Chained PRs for large changes — split oversized PRs into sequential,
  reviewable chunks under 300 lines. Stacked PRs or Feature Branch Chain.
  Trigger: When a PR exceeds 300 lines, or SDD forecasts budget risk High.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "4.0"
  model_tier: T2-fast
---

# Skill: chained-pr

Chained PRs. Large changes broken into reviewable chunks that protect reviewer cognitive load.

## Activation Contract

Load this skill when:
- A planned PR may exceed **300 changed lines**
- SDD forecasts `300-line budget risk: High` or `Chained PRs recommended: Yes`
- The user asks for chained/stacked PRs or review slices

## Hard Rules

- Split PRs over **300 changed lines** unless a maintainer explicitly accepts `size:exception`
- Keep each PR reviewable in ≤60 minutes
- One deliverable work unit per PR; keep tests/docs with the unit they verify
- State start, end, prior dependencies, follow-up work, and out-of-scope in every chained PR
- Every child PR must include a dependency diagram marking the current PR with `📍`
- Do not mix chain strategies after the user chooses one

## Decision Gates

| Condition | Action |
|-----------|--------|
| PR ≤300 changed lines and focused | Keep single PR |
| PR >300, each slice can land independently | Use **Stacked PRs to main** |
| PR >300, feature must integrate before main | Use **Feature Branch Chain** with tracker |
| Generated/vendor/migration diff cannot split cleanly | Ask maintainer for `size:exception` |
| SDD provides `delivery_strategy` | Follow it before apply/PR creation |

## Strategy A: Stacked PRs to Main

```
main ← PR1 (refactor base)
     ← PR2 (core logic, base = PR1)
     ← PR3 (integration, base = PR2)
```

1. PR1 targets main, gets reviewed and merged
2. PR2 targets main, but code based on PR1
3. PR3 targets main, but code based on PR2
4. Each merge updates main, next PR rebases

## Strategy B: Feature Branch Chain (with Tracker)

```
main ←──── feature/auth (tracker PR, draft, no merge)
                ← feat/auth-validate (PR #1)
                ← feat/auth-middleware (PR #2, base = PR #1)
                ← feat/auth-integrate (PR #3, base = PR #2)
```

1. Create tracker PR `feature/auth` → draft, targets main, never merged
2. PR #1 targets `feature/auth`, reviewed and merged into tracker
3. PR #2 targets PR #1's branch, reviewed and merged
4. PR #3 targets PR #2's branch, reviewed and merged
5. When all children are in, merge tracker to main

**Critical**: child PRs must NEVER target main directly. If GitHub shows previous slices in a child diff, retarget/rebase until the diff is clean.

## Execution Steps

1. Estimate changed lines and identify independent work units
2. Ask for chain strategy when none is cached and budget is exceeded
3. Create branches/PRs using the chosen strategy only
4. Add **Chain Context** to each PR body (see below)
5. Verify each PR independently: CI, tests, docs, clean diff
6. Keep tracker PR draft/no-merge until all children are reviewed

## Chain Context (add to each PR body)

```markdown
## PR Chain

This is PR **2 of 3** in the `{feature}` chain:
- 📍 **PR #2 — {this PR description}** (you are here)
- PR #1: {description} → {link}
- PR #3: {description} → {link}

| Item | Value |
|------|-------|
| Chain strategy | stacked-to-main / feature-branch-chain |
| Review budget | {additions} + {deletions} = {total} changed lines |
| Depends on | {PR #1 link} |
| Blocks | {PR #3 link} |
```

## Output Contract

Return: chosen strategy, PR order, current PR boundary, dependency diagram, review budget, verification plan, and any `size:exception` rationale.

## Anti-patterns

- ❌ Splitting by file type instead of work unit (models/views/controllers → weak split)
- ❌ Child PR diff includes parent's code (polluted diff → retarget/rebase)
- ❌ Mixing stacked-to-main and feature-branch in same chain
- ❌ Tracker PR merged before children are complete
