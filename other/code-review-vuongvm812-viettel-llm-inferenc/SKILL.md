---
name: code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Code Review — 5 Parallel Lenses

**Core principle:** Five specialized reviewers in parallel, each with a confidence score. Synthesize into one verdict.

## When to Request Review

**Mandatory:** After completing a feature, before merge to main, after each task in subagent-driven development.

**Optional:** When stuck, before refactoring (baseline), after fixing a complex bug.

---

## Step 1: Get the Diff Range

**Local branch:**
```bash
BASE_SHA=$(git merge-base HEAD origin/main)
HEAD_SHA=$(git rev-parse HEAD)
```

**PR review:**
```bash
gh pr view <number> --json baseRefOid,headRefOid \
  --jq '"BASE=\(.baseRefOid[:8]) HEAD=\(.headRefOid[:8])"'
```

**Recent commit:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)
```

---

## Step 2: Dispatch 5 Parallel Subagents

Launch ALL five simultaneously. Each uses `code-reviewer.md` with its `{LENS}` filled in.

| # | Lens | Focus |
|---|------|-------|
| 1 | **Correctness** | Bugs, logic errors, edge cases, data races, panics |
| 2 | **Architecture** | Design patterns, coupling, DDD alignment, type safety |
| 3 | **Performance** | Allocations, clone/copy, hot paths, complexity |
| 4 | **Security & Safety** | Unsafe blocks, input validation, error propagation, secrets |
| 5 | **Tests & Requirements** | Coverage, spec compliance, test quality, TDD adherence |

**Dispatch template** (repeat for each lens, all in parallel):

```
Agent: general-purpose
Prompt: [code-reviewer.md with placeholders filled]
  LENS: <lens name>
  LENS_FOCUS: <focus from table above>
  WHAT_WAS_IMPLEMENTED: <feature description>
  PLAN_OR_REQUIREMENTS: <requirements or task>
  BASE_SHA: <base>
  HEAD_SHA: <head>
  DESCRIPTION: <one-line summary>
```

---

## Step 3: Synthesize Results

After all 5 agents return, produce a unified report:

### Synthesis Format

```
## Code Review — Synthesis

### Lens Results

| Lens | Confidence | Critical | Important | Minor |
|------|-----------|----------|-----------|-------|
| Correctness    | XX% | N | N | N |
| Architecture   | XX% | N | N | N |
| Performance    | XX% | N | N | N |
| Security/Safety| XX% | N | N | N |
| Tests & Reqs   | XX% | N | N | N |
| **Overall**    | **XX%** | **N** | **N** | **N** |

> Overall confidence = weighted average (Correctness×0.25, Architecture×0.20,
> Performance×0.20, Security×0.20, Tests×0.15)

---

### Critical Issues (Must Fix)
[Deduplicated across all lenses — file:line, what, why, fix]

### Important Issues (Should Fix)
[Deduplicated across all lenses]

### Minor Issues (Nice to Have)
[Deduplicated across all lenses]

### Strengths
[Specific positives from all lenses]

### Verdict

**Ready to merge?** Yes / No / With fixes

**Confidence:** XX% — [what drove the score up or down]

**Reasoning:** [2-3 sentences technical assessment]
```

### Deduplication Rule

If two lenses flag the same issue: keep the higher-severity instance, note which lenses agreed (increases confidence).

### Confidence Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100% | High confidence, thorough review | Proceed normally |
| 70-89% | Good coverage, minor gaps | Note gaps, proceed |
| 50-69% | Moderate — complex or large diff | Flag for extra scrutiny |
| < 50% | Low — diff too large or domain unclear | Consider splitting the PR |

---

## Step 4: Act on Feedback

| Severity | Action |
|----------|--------|
| Critical | Fix immediately — do not proceed |
| Important | Fix before merging |
| Minor | Note for later or fix now |
| Reviewer wrong | Push back with code/test evidence |

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed past Important issues without fixing them

---

## PR Review Mode

For GitHub PRs, add PR context to each subagent:

```bash
gh pr view <number> --json title,body,additions,deletions,changedFiles
gh pr diff <number>
```

Pass PR title + body as `{PLAN_OR_REQUIREMENTS}` so each lens can check spec compliance.
