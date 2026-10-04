---
name: refactoring-and-tech-debt
description: Use when tracking tech debt across a codebase, when planning a refactor, when deciding whether to rewrite vs incrementally improve, when a workaround has appeared in three places, or when a refactor PR is about to be combined with feature work.
---

# Refactoring and Tech Debt

## Overview

Make tech debt visible, accountable, and resolvable — *before* it compounds. Output is `.forge/tech-debt-registry.md` — every known debt item with location, type, cost-to-fix, cost-of-not-fixing, owner, and trigger. Sets the refactor patterns (extract, inline, rename, strangler-fig) and enforces the rule that **refactor PRs are refactor-only**. Pairs with `code-review-and-quality` (review enforces the registry) and `planning-and-task-breakdown` (debt items get scheduled like features).

## When to Use

- A codebase is older than 6 months and the team can name "the bad part" but it's not tracked
- A refactor is being proposed and the team is debating "rewrite vs incremental"
- The same workaround (try/catch with comment, copy-pasted helper, manual cleanup script) appears in 3+ places
- A perf or security finding requires a refactor in addition to the immediate fix
- A team member is leaving and the bus-factor on a module is 1

## When NOT to Use

- A greenfield project — no debt yet
- A trivial rename or extract that's part of a feature task (do it as part of the feature work, don't ceremony it)
- A speculative "this might be debt someday" — wait for the third occurrence

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We'll fix it later" | Later never comes without a ticket and a trigger. The debt registry is the ticket. |
| "Just rewrite it" | Rewrites without a strangler-fig plan create two broken systems running in parallel. The new system inherits the old system's bugs because the old system *encoded* the bugs as decisions. |
| "It works, don't touch it" | Working code that nobody understands has a bus factor of zero. The first incident on that code is also a knowledge incident. |
| "Refactoring is a waste of time" | The time you save skipping refactoring you spend debugging. Debt compounds; refactor pays it down. |
| "We'll refactor while we add this feature" | Mixed PRs are impossible to review and impossible to revert independently. The next bisect points at the refactor commit even when the feature caused the regression. |
| "Strangler-fig is overkill, just swap it" | Big-bang swaps fail. Strangler-fig keeps the system running while you migrate, one consumer at a time. |

## Red Flags

- A "refactor" PR that adds, changes, or removes user-visible behavior
- A rewrite started without a strangler-fig migration plan
- The same workaround copy-pasted in 3+ places, no extraction
- A "we'll fix it later" comment with no linked ticket
- A debt registry that's been stale for >90 days
- Bus factor 1 on a critical module
- A perf or security fix that "needs a refactor first" but the refactor never starts

## Core Process

### Step 1: Audit the codebase for debt

Walk the codebase. Look for:
- Copy-pasted code blocks (3+ occurrences of a near-identical pattern → candidate for extract)
- Workaround comments (`// TODO`, `// HACK`, `// FIXME`, `// XXX`, `// temporary`) → triage each
- Modules with high churn but low test coverage (changes break things, tests don't catch it)
- Functions over 100 lines or files over 500 lines → split candidates
- Cyclic imports → architectural debt
- Dead code (no callers, no tests) → delete candidates
- "The bad part" everyone names — the legacy module, the auth flow, the billing code → entry candidates

### Step 2: Classify each debt item

In `.forge/tech-debt-registry.md`, one entry per item:

```markdown
## DEBT-042: auth/session.ts — manual cookie parsing

**Location:** src/auth/session.ts:14-87
**Type:** Workaround (predates the framework's session helper)
**Bus factor:** 1 (only the original author understands it)
**Cost to fix:** 2 engineer-days
**Cost of not fixing:** 1 incident every ~3 months; each incident ~6 engineer-hours
**Owner:** @assigned-engineer
**Trigger:** Third recurrence in 6 months, OR before adding multi-tenant auth, OR a security finding
**Pattern:** Replace with framework helper. Strangler-fig: new sessions use helper, old sessions migrate on next login.
**Tracking:** ISSUE-LINK
```

Types: `workaround`, `duplicate-code`, `architectural` (boundaries leaky), `dependency` (outdated, unmaintained), `dead-code`, `test-gap`, `documentation-gap`, `bus-factor`.

### Step 3: Set refactor triggers

A debt item is *picked up* when one of its triggers fires:

- **Third-occurrence rule** — the same workaround appearing in 3+ places triggers extraction
- **Adjacent-work rule** — touching a debt-flagged module for any feature work triggers fixing the debt as a *prior* PR (not combined)
- **Budget-breach rule** — a performance or cost budget breach traceable to the debt
- **Security/compliance rule** — a finding requires the refactor as part of remediation
- **Calendar rule** — items with `cost-of-not-fixing > cost-to-fix` over a year are scheduled, not waited on

### Step 4: Choose the pattern per item

| Item shape | Pattern |
|---|---|
| Duplicate code, stable shape | Extract to shared module |
| One-line wrappers used everywhere | Inline; remove indirection |
| Old name, new meaning | Rename (with deprecation alias for the window) |
| Big module needs replacing while running | Strangler-fig (route new traffic to new module, migrate old traffic over time) |
| Cyclic imports | Introduce a third module that owns the shared types |
| Dead code | Delete; no aliases, no "just in case" |
| Test gap | Add characterization tests for the existing behavior *before* refactoring |

### Step 5: Enforce refactor-only PRs

A refactor PR contains **no behavior change**. Tests that pass before pass after, unchanged. New tests added for newly-exposed seams are allowed; changes to existing test assertions are not. Cross-reference `code-review-and-quality`.

If a refactor needs a behavior change to land safely, split into:
1. PR A: extract / restructure (no behavior change, all tests green)
2. PR B: behavior change (now testable because of A)

### Step 6: Strangler-fig template for rewrites

When a module is being replaced (not refactored in place):

1. Build the new module behind a feature flag, with no callers
2. Add a router: callers go to `new` if flag on, `old` if off
3. Migrate one caller at a time. Each migration is its own PR with its own tests.
4. When all callers are migrated, remove the router and the old module
5. Each step is independently revertible

Big-bang rewrites are forbidden. If a rewrite cannot be strangler-figged, write an ADR explaining why.

## Verification

- [ ] `.forge/tech-debt-registry.md` exists and was updated in the last 90 days
- [ ] Every debt item has owner, estimate, and trigger
- [ ] Every TODO/HACK/FIXME comment in the codebase is either resolved or linked to a registry entry
- [ ] No refactor PR in the last 30 days mixed behavior changes with refactoring
- [ ] Every rewrite in flight has a strangler-fig plan documented (or an ADR justifying why not)
- [ ] No copy-pasted code block appears 3+ times without an extraction ticket
- [ ] No critical module has a bus factor of 1 without a documented mitigation
