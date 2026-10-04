---
name: review
description: Plan-aware graph-enhanced code review before merge. CRITICAL issues block merge. Use after fix/verify.
mcp: codebase-memory-mcp
---

# /supergraph:review

Final gate before merge. Graph-enhanced review with plan awareness.

## Prerequisites

- `/supergraph:fix` completed (tests pass, lint clean)

## Usage

`/supergraph:review` | `plan auth-login` | `plan auth-login task 2`

## Steps

### 0. Announce
"🔍 /supergraph:review — starting graph-enhanced code review..."

### 1. Select Plan Context
0 plans → skip | 1 → use | >1 → ask | `plan <slug>` → match.
Parse tasks, scope to `task N` if provided.

### 2. Capture Git Range
```bash
BASE_SHA=$(git rev-parse origin/master || git rev-parse origin/main || git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)
git diff --stat "$BASE_SHA..$HEAD_SHA" && git diff --name-only "$BASE_SHA..$HEAD_SHA"
```
Use plan checkpoint commits as range if available. No changed files → check plan for incomplete tasks.

### 3. Graph Analysis (tiered)
Reindex first for `CBM_PROJECT` (see `references/codebase-memory-contract.md#Lifecycle`): `index_status`; if stale/degraded → `index_repository` (skip if `BASE_SHA` unchanged and `.supergraph-env` fresh). Then `codebase-memory-mcp` `detect_changes`, `trace_path`, `get_graph_schema`.

Tiered recipes (pick by blast radius):
- Micro (≤2 files, <20 lines, no hub/bridge): `cycles` + `test-gaps` only (0.04s)
- Standard (≤5 files, no cross-boundary): `cycles`/`hubs`/`test-gaps` + optional `cross-boundary`
- Full (>5 files or hub/bridge/cross-boundary): all `cycles, hubs, bridges, test-gaps, complexity, cross-boundary` (0.12s). Per file: `query_graph(query_type="tests", target=file)`.

**3b. Serena (optional, selective):** See `serena/SKILL.md:Setup`. If scan not run, call `initial_instructions` first. Only for hub/bridge or `complexity>10` files: `find_referencing_symbols`/`find_implementations` per symbol and `get_diagnostics_for_file` per file. Otherwise skip. Pass as "Serena findings". Skip if unavailable.

### 4. Dispatch Code Reviewer (tiered, parallel with tests)
Tiered (pick by blast radius):
- Micro (≤2 files, <20 lines, no hub/bridge): **skip** code-reviewer agent — `tests+lint` + `cycles+test-gaps` đủ, `Critical` chỉ từ `tests/lint/circular` (LLM 30-60s saved)
- Standard (≤5 files, no cross-boundary): Stage1 Spec Compliance only, parallel with tests
- Full (>5 files or hub/bridge/cross-boundary): 2-stage (Spec→Quality), parallel with tests. Join before Step 6.
```
Agent(subagent_type="supergraph:code-reviewer", prompt="Review BASE_SHA..HEAD_SHA. Spec first, then quality (Standard: Stage1 only). BASE_SHA/HEAD_SHA, git diff --stat + git diff (first 300 lines, or --name-only + snippets for large diffs), Graph: hubs/bridges/surprise/flows/gaps, Serena findings, Plan requirements. Output: strengths, Critical/Important/Minor, verdict YES|WITH_FIXES|NO")
```

### 5. Verify Tests + Lint (parallel with Step 4 when reviewer runs)
Run `$TEST_CMD` and `$LINT_CMD`; if reviewer skipped (Micro), run tests alone. **Dedup:** if `verify` just passed with same `HEAD_SHA` and `<120s` ago and `git diff` unchanged, reuse `verify` evidence; else rerun fresh. Failures → add to Critical. Join both before Classify.

### 6. Classify Issues

| Severity | Sources | Action |
|---|---|---|
| **Critical** | Reviewer Critical, tests/lint fail, circular deps, broken hub API, surprise>0.7, `in_progress` tasks | Block merge |
| **Important** | Reviewer Important, surprise 0.5-0.7, missing hotspot tests, bridge node without validation, `stuck` tasks | Fix unless risk accepted |
| **Minor** | Reviewer Minor, clean graph, good coverage | Note only |

### 7. Checklist
| Gate | Check |
|---|---|
| Blast radius | All affected files handled? |
| Hub safety | Callers tested? API compatible? |
| Bridge | Cross-community impact? |
| Surprise | >0.7 investigate, 0.5-0.7 document |
| Gaps | Untested hotspots? |
| TDD | RED/GREEN evidence? |

### 7.1 Durable Review Boundary

Review the generated `review-<base>..<head>.diff` and task report, then **re-review only changed scope** after a fix. Re-read any illegible evidence instead of rerunning unrelated work. Record reviewer verdicts, conflict rulings, and the **circuit-breaker** state in `ledger.md` and the finish report.

### 8. Act on Feedback

Critical → fix immediately, no exceptions.
Important → fix unless user accepts risk. Push back with evidence, not opinion.
Minor → note, optional.

**When human gives review feedback:**
- Clarify ALL unclear items first, implement together
- Grep codebase before implementing suggested "professional" features (YAGNI)
- Push back gracefully if reviewer is wrong — technical reasoning + tests/proof
- Never performative agreement ("You're absolutely right!")

### 9. Generate Verdict

```markdown
## Review Report
- Verdict: PASS | NEEDS_CHANGES | BLOCKED
- Changed: N files | Blast radius: M
- Hub/Bridge: [list/none] | Surprise: [list/none]
- Tests: PASS|FAIL | Lint: PASS|FAIL
- Critical: N | Important: N | Minor: N
- Reasoning: [summary]
```

Verdict rules:
- `PASS` → 0 Critical, reviewer YES
- `NEEDS_CHANGES` → 0 Critical, >0 Important or reviewer WITH_FIXES
- `BLOCKED` → >0 Critical or reviewer NO

### 10. Update Plan

PASS + all tasks reviewed → mark `Status: completed`, add review log.
BLOCKED → mark affected tasks `stuck`, append blocker list.

### 10b. Update CONTEXT.md (if review surfaced new domain invariants)

If review revealed undocumented domain rules, invariants, or terminology:
```bash
printf '\n## <term or invariant>\n[what was discovered]\n' >> CONTEXT.md
```
Examples: hidden ordering constraints, shared state assumptions, boundary rules between modules.

**Serena memory (optional — for non-PASS verdicts):**
On BLOCKED or NEEDS_CHANGES, persist findings for the next fix cycle:
```
mcp__serena__write_memory(
  title="<plan-slug>-review-verdict",
  content="Verdict: [BLOCKED|NEEDS_CHANGES]. Critical: [...]. Callers affected: [...]. Diagnostics: [...]"
)
```
Skip if Serena unavailable or verdict is PASS.

### 11. Handoff

PASS → ready to merge.
NEEDS_CHANGES → `/supergraph:fix`, then re-review. Max 2 cycles, then escalate.
BLOCKED → escalate immediately, no auto-fix.

## Rules

- Dispatch code-reviewer per tier (Micro skip, Standard Stage1, Full 2-stage); always join with tests before Classify
- Critical issues block merge — no exceptions
- Hub/bridge changes need extra scrutiny
- Max 2 fix-review cycles, then escalate
- Never pass if tests or lint fail
- Surprise connections must be investigated or documented
