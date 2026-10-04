---
name: superpowers-plan-eng-review
description: >
  Engineering plan review. Lock in the execution plan — architecture, data flow,
  diagrams, edge cases, test coverage, performance. Walks through issues interactively
  with opinionated recommendations. Use when asked to "review the architecture",
  "engineering review", or "lock in the plan". Proactively suggest when the user
  has a plan or design doc and is about to start coding.
benefits-from: [superpowers-office-hours]
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
  - Bash
  - WebSearch
---

> **DEPRECATED** — use `/plan-eng-review` instead. This skill is a legacy alias and will be removed in a future cleanup.
# Plan Engineering Review — Lock In the Plan

**Purpose:** Review an implementation plan before writing code. Catch architecture issues, missing tests, and unhandled failure modes BEFORE they become bugs.

**Output:** An improved plan with tests specified, diagrams added, and failure modes documented.

---

## Engineering Preferences

Use these to guide recommendations:
- **DRY is important** — flag repetition aggressively
- **Well-tested code is non-negotiable** — too many tests > too few
- **Engineered enough** — not under (fragile) and not over (premature abstraction)
- **Explicit over clever** — code readable by anyone
- **Minimal diff** — achieve the goal with fewest files touched
- **Handle more edge cases, not fewer** — thoughtfulness > speed

---

## Step 0: Detect base branch

```bash
gh pr view --json baseRefName -q .baseRefName 2>/dev/null || \
  gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null || \
  echo "main"
```

---

## Before You Start

### Design Doc Check
```bash
SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null | tr '/' '-' || echo 'no-branch')
DESIGN=$(ls -t ~/.claude/.context/*-$BRANCH-design-*.md 2>/dev/null | head -1)
[ -z "$DESIGN" ] && DESIGN=$(ls -t ~/.claude/.context/*-design-*.md 2>/dev/null | head -1)
[ -n "$DESIGN" ] && echo "Design doc found: $DESIGN" || echo "No design doc found"
```
If a design doc exists, read it. Use it as the source of truth for the problem statement, constraints, and chosen approach.

### Prerequisite Skill Offer
If no design doc is found, offer via AskUserQuestion:
> "No design doc found for this branch. `/superpowers-office-hours` produces a structured problem statement and explored alternatives — it gives this review much sharper input. Takes about 10 minutes."

Options:
- A) Run /superpowers-office-hours now
- B) Skip — proceed with standard review

If A: Run `/superpowers-office-hours` inline. After it completes, re-run the design doc check above. If no design doc was produced, proceed with standard review.

### Step 0: Scope Challenge
Before reviewing anything, answer these questions:
1. **What existing code already partially or fully solves each sub-problem?** Can we reuse existing flows?
2. **What is the minimum set of changes?** Flag any work that could be deferred.
3. **Complexity check:** If the plan touches 8+ files or introduces 2+ new classes/services, challenge whether the same goal can be achieved with fewer moving parts.
4. **Search check:** For each architectural pattern or infrastructure approach:
   - Does the runtime/framework have a built-in? Search: `"{framework} {pattern} built-in"`
   - Is the approach current best practice? Search: `"{pattern} best practice"`
   - Are there known footguns? Search: `"{framework} {pattern} pitfalls"`
5. **TODOS cross-reference:** Read `TODOS.md` if it exists. Any deferred items blocking this plan?
6. **Completeness check:** Is the plan doing the complete version or a shortcut? With AI-assisted coding, the cost of completeness is near-zero. Recommend the complete version. Boil the lake.
7. **Distribution check:** If the plan introduces a new artifact (CLI binary, package, container), does it include build/publish pipeline?

If the complexity check triggers, recommend scope reduction via AskUserQuestion. If it doesn't, present your Step 0 findings and proceed to Section 1.

---

## Review Sections

Always work through: Architecture → Code Quality → Tests → Performance. One section at a time. Max 8 top issues per section.

### 1. Architecture Review
Evaluate:
- Overall system design and component boundaries
- Dependency graph and coupling concerns
- Data flow patterns and potential bottlenecks
- Scaling characteristics and single points of failure
- Security architecture (auth, data access, API boundaries)
- Whether key flows deserve ASCII diagrams
- For each new codepath or integration point: one realistic production failure scenario
- Distribution architecture: if introducing a new artifact, how does it get built/published?

**STOP.** AskUserQuestion for each issue individually. One issue = one call.

### 2. Code Quality Review
Evaluate:
- Code organization and module structure
- DRY violations — be aggressive here
- Error handling patterns and missing edge cases (call these out explicitly)
- Technical debt hotspots
- Areas that are over- or under-engineered relative to the preferences above

**STOP.** AskUserQuestion for each issue individually.

### 3. Test Review

**100% coverage is the goal.** Every codepath in the plan must have a test specified.

#### Detect test framework:
1. Read CLAUDE.md — look for a `## Testing` section
2. If missing, auto-detect:
```bash
[ -f Gemfile ] && echo "RUNTIME:ruby"
[ -f package.json ] && echo "RUNTIME:node"
[ -f requirements.txt ] || [ -f pyproject.toml ] && echo "RUNTIME:python"
[ -f go.mod ] && echo "RUNTIME:go"
[ -f Cargo.toml ] && echo "RUNTIME:rust"
ls jest.config.* vitest.config.* playwright.config.* cypress.config.* pytest.ini 2>/dev/null
```

#### Trace every codepath:
For each planned feature, follow data through every branch:
1. Where does input come from?
2. What transforms it?
3. Where does it go?
4. What can go wrong at each step?

Draw an ASCII coverage diagram:

```
CODE PATH COVERAGE
===========================
[+] src/services/billing.ts
    │
    ├── processPayment()
    │   ├── [★★★ TESTED] Happy path + card declined + timeout
    │   ├── [GAP]         Network timeout — NO TEST
    │   └── [GAP]         Invalid currency — NO TEST
    │
    └── refundPayment()
        ├── [★★  TESTED] Full refund
        └── [★   TESTED] Partial refund (checks non-throw only)

USER FLOW COVERAGE
===========================
[+] Payment checkout flow
    │
    ├── [★★★ TESTED] Complete purchase
    ├── [GAP] [→E2E] Double-click submit — needs E2E
    └── [GAP]         Navigate away during payment

─────────────────────────────────
COVERAGE: 3/5 paths tested (60%)
GAPS: 2 paths need tests (1 needs E2E)
─────────────────────────────────
```

Quality scoring: ★★★ (edge + error paths) > ★★ (happy path only) > ★ (smoke/existence)

#### E2E decision matrix:
- **Recommend E2E** [→E2E]: User flow spanning 3+ components, integration points where mocking hides failures, auth/payment/data-destruction flows
- **Recommend UNIT**: Pure functions, internal helpers, edge cases of single functions
- **IRON RULE**: Any REGRESSION (existing behavior the diff breaks) gets a test added as CRITICAL — no AskUserQuestion, no skipping

#### Add missing tests to the plan:
For each GAP: what test file, what it should assert, whether unit/E2E/eval.

**STOP.** AskUserQuestion for each test gap.

### 4. Performance Review
Evaluate:
- N+1 queries and database access patterns
- Memory-usage concerns
- Caching opportunities
- Slow or high-complexity code paths

**STOP.** AskUserQuestion for each issue.

---

## Outside Voice (optional)

Offer via AskUserQuestion:
> "Want an independent second opinion on this plan? A different AI model gives a brutally honest challenge — logical gaps, feasibility risks, blind spots."

Options:
- A) Get outside voice (recommended)
- B) Skip — proceed to outputs

If A: dispatch a general-purpose subagent with the plan content and prompt it to find: logical gaps, unstated assumptions, overcomplexity, feasibility risks, missing dependencies.

Present findings. Note cross-model tensions. For each substantive tension, offer to add to TODOs via AskUserQuestion.

---

## Required Outputs

### "NOT in scope" section
Every plan review MUST produce a "NOT in scope" section listing work explicitly deferred, with rationale.

### "What already exists" section
Existing code/flows that partially solve sub-problems. Does the plan reuse or rebuild?

### TODOS.md updates
Present each potential TODO as its own AskUserQuestion. Never batch. Never skip silently.

Format:
- **What:** One-line description
- **Why:** The concrete problem it solves
- **Pros/Cons**
- **Context** — enough for someone to pick it up in 3 months
- **Depends on**

Options: **A)** Add to TODOS.md **B)** Skip **C)** Build it now in this PR

### Diagrams
Identify which files should get inline ASCII diagram comments: Models (data relationships, state transitions), Services (processing pipelines), Tests (what's being set up).

### Failure modes
For each new codepath: one realistic way it could fail in production, whether a test covers it, whether error handling exists, whether the user sees a clear error or silent failure.

If any failure mode has no test AND no error handling AND would be silent → **critical gap**.

### Completion Summary
```
Step 0: Scope Challenge — [scope accepted / scope reduced]
Architecture Review: ___ issues found
Code Quality Review: ___ issues found
Test Review: diagram produced, ___ gaps identified
Performance Review: ___ issues found
NOT in scope: written
What already exists: written
TODOS.md updates: ___ items proposed
Failure modes: ___ critical gaps flagged
Outside voice: ran / skipped
```

---

## Review Log

```bash
mkdir -p ~/.claude/.context
echo '{"skill":"plan-eng-review","timestamp":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","status":"STATUS","unresolved":N,"critical_gaps":N,"issues_found":N,"commit":"'"$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"'"}' >> ~/.claude/.context/reviews.jsonl
```

- **STATUS**: "clean" if 0 unresolved AND 0 critical gaps; otherwise "issues_open"
- **unresolved**: number of unresolved decisions
- **critical_gaps**: number of critical failure gaps
- **issues_found**: total issues across all review sections

---

## Next Steps

- If UI scope exists and no design review has run: recommend `/superpowers-plan-design-review`
- If significant product change with no CEO review: recommend `/superpowers-plan-ceo-review`
- If all reviews complete or not needed: "All relevant reviews complete. Run `/superpowers-executing-plans` when ready."

---

## Completion Status

- **DONE** — All sections complete, plan updated, review logged
- **DONE_WITH_CONCERNS** — Completed with unresolved decisions
- **BLOCKED** — Cannot proceed
- **NEEDS_CONTEXT** — Missing information required to continue
