---
name: plan
description: >
  Structured planning for multi-item task lists. Produces a tiered, actionable
  plan that separates what the agent can do now from what needs operator action,
  identifies blockers, and recommends execution order. Supports three modes:
  smart (default, tiered by actionability), lazy (minimal, YAGNI-filtered, top
  1-2 actions only), thorough (deep investigation, dependency graph, risk
  analysis, alternatives per item). Use when the user says "plan", "plan in
  smart mode", "plan in lazy mode", "plan in thorough mode", "how should we
  approach", or wants to compare planning approaches. Do NOT use for single-step
  tasks or when the user wants immediate execution without planning.
argument-hint: "[smart|lazy|thorough] <context or task list>"
version: 0.1.0
execution-mode: advisory
triggers:
  - plan
  - plan in smart mode
  - plan in lazy mode
  - plan in thorough mode
  - how should we approach
  - make a plan
  - planning mode
chains:
  - apex
  - ponytail
  - start-session
  - end-session
category: fleet-ops
status: candidate
---

# Plan

You are operating in **PLAN MODE** — structured assessment before action.
Plan produces a tiered, actionable plan. It does not execute. The caller
or operator decides what to act on after reviewing the plan.

## Persistence

ACTIVE FOR ONE PLANNING CYCLE. The plan is produced once, presented to the
user, and the skill is done. If the user wants to re-plan with a different
mode, invoke again with the new mode.

## Mode Selection

The mode is extracted from the first argument. If no mode is specified,
default to **smart**.

| Mode | Keyword | Philosophy |
|------|---------|------------|
| Smart | `smart` | Tiered by actionability. What I can do now vs what needs operator action. Execution order. Blockers surfaced. |
| Lazy | `lazy` | Minimal. YAGNI-filtered. Top 1-2 actions only. If it's not blocking, it's not in the plan. |
| Thorough | `thorough` | Deep. Dependency graph. Risk analysis per item. Alternatives. Edge cases. Full investigation before ranking. |

## Workflow

### Step 1 — Gather context

Before producing any plan, gather the current state:

1. **Read the coordination bus** (if accessible) for recent HANDOFF, STATUS, and SITREP entries from other agents.
2. **Check open PRs and issues** via `gh pr list --state open` and `gh issue list --state open`.
3. **Check CI status** on open PRs — any failing checks, any queued checks.
4. **Check git state** — current branch, uncommitted changes, stale branches.
5. **Read AGENTS.md** for active constraints, guardrails, and conventions.
6. **Identify active constraints** — any issues, rules, or bus entries that constrain write/push operations.

If the user provides an explicit task list or context, use that as the primary
input and skip steps that don't apply.

### Step 2 — Enumerate open items

List every open item from the gathered context:

- Open PRs (with CI state and review status)
- Open issues (with age, labels, priority)
- Bus HANDOFF entries (open items from prior sessions)
- Hygiene warnings (detached HEAD, stale branches, untracked files)
- Operator-action-needed items (permissions, provisioning, cross-machine tasks)

### Step 3 — Apply mode-specific analysis

#### Smart mode (default)

Tier every item into one of four tiers:

| Tier | Criteria | Example |
|------|----------|---------|
| **Tier 1: Do now** | Agent can execute, no blockers, high impact | Merge a green PR, push a fix |
| **Tier 2: Investigate first** | Agent can do but needs verification before action | Check if a fix is already applied, verify scope |
| **Tier 3: Needs operator** | Requires permissions, cross-machine access, or human judgment | Org membership provisioning, SSH key authorization |
| **Tier 4: Monitor** | No action needed, just watch | CI re-running, waiting for review |

For each item, state:
- What it is (one line)
- What action is needed
- Effort (1 cmd / small edit / medium / large)
- Impact (unblocks X / clears Y / low urgency)
- Whether the agent can do it or the operator must

Produce a recommended execution order.

#### Lazy mode

Apply YAGNI filter ruthlessly:

1. **Does this need to be in the plan at all?** If it's not blocking something else and not due within this session, drop it. Say so in one line.
2. **Of the remaining items, which 1-2 have the highest impact-to-effort ratio?** Those go in the plan. Everything else is a one-line "deferred" list.
3. **For each of the 1-2 items:** what's the single smallest action that unblocks or resolves it?

Output format:
```
DO: <action 1> — because <reason>
DO: <action 2> — because <reason>
DEFERRED: <item> — <why it can wait>
DEFERRED: <item> — <why it can wait>
```

No tiers, no tables, no dependency graphs. The lazy plan fits on a sticky note.

#### Thorough mode

For each open item, produce a structured analysis:

1. **Description** — what it is, full context
2. **Current state** — what's been done, what's pending, with evidence (file paths, line numbers, commit SHAs, bus entries)
3. **Dependencies** — what blocks this, what this blocks (draw the dependency graph)
4. **Risk analysis** — what could go wrong, likelihood, impact, mitigation
5. **Alternatives** — at least 2 approaches per item, with trade-offs
6. **Edge cases** — what's not covered by the obvious approach
7. **Recommendation** — which alternative, why, and what the execution sequence looks like

After per-item analysis, produce:
- **Dependency graph** (text-based, showing which items block which)
- **Risk-weighted priority matrix** (impact × likelihood)
- **Execution sequence** respecting dependencies
- **Confidence assessment** — where is the plan uncertain, what would change the plan

### Step 4 — Present the plan

Present the plan in the mode-appropriate format:

- **Smart**: Tiered table + execution order (the format used in the session that prompted this skill's creation)
- **Lazy**: Sticky-note format (DO/DEFERRED)
- **Thorough**: Full structured analysis with dependency graph and risk matrix

End with: "Shall I proceed with this plan?" — the operator decides what to act on.

## Constraints

- **No execution**: Plan mode never executes. It produces a plan. The operator or caller decides what to act on.
- **No file mutations**: Plan mode is read-only. No edits, no commits, no pushes.
- **Evidence-based**: Every claim in the plan must be backed by evidence (file path, git command output, bus entry, CI status). No speculation.
- **Mode fidelity**: If the user asked for lazy mode, do not produce a thorough plan. If they asked for thorough, do not truncate to smart. The mode controls depth, not content.
- **Bus awareness**: If the coordination bus is accessible, check it for recent HANDOFF entries that contain open items from prior sessions.
- **Active constraints**: Check for and surface any active constraints (issues, rules, bus entries) that would block write/push operations before recommending them.

## Mode Comparison

When the user wants to compare modes (e.g., "plan in smart mode" then "plan in lazy mode" on the same context), the skill should:

1. Produce the first mode's plan
2. When invoked again with a different mode, produce the second mode's plan on the same context
3. Highlight what changed between the two plans — what was dropped, what was promoted, what was deepened

This comparison is the primary use case for the mode parameter. The same open items, analyzed through different lenses, produce different action priorities. That difference is the signal.

## Examples

### Smart mode (default)

```
> plan in smart mode

## Plan — Smart Mode

### Tier 1: Do now
| # | Item | Action | Effort | Impact |
|---|------|--------|--------|--------|
| A | PR 1832 all CI green | Merge | 1 cmd | Closes open PR |
| B | PR 1828 audit fix pushed | Watch CI | 5 min | Unblocks branch |

### Tier 2: Investigate first
| # | Item | What to verify | Then |
|---|------|---------------|------|
| C | caveman-ponytail H1 | Find arrow token in SKILL.md | Fix if present |

### Tier 3: Needs operator
| # | Item | Why | Operator action |
|---|------|-----|-----------------|
| D | Issue #1810 | Needs admin:org scope | gh auth refresh, add @reubenbowlby to org |

### Tier 4: Monitor
| # | Item | Status |
|---|------|--------|
| E | PR 1827 CI | Re-running with H1+MED fix |

### Execution order: A → B (parallel with C) → D (operator) → E
```

### Lazy mode

```
> plan in lazy mode

DO: Merge PR 1832 — all CI green, no reason to wait
DO: Watch PR 1828 CI — audit fix is being evaluated right now
DEFERRED: caveman-ponytail H1 — not blocking any merge
DEFERRED: Issue #1810 — needs operator, not agent-actionable
DEFERRED: PR 1827 — CI will either pass or not, checking later is fine
DEFERRED: Workstation detached HEAD — hygiene, not blocking
```

### Thorough mode

```
> plan in thorough mode

## Item A: PR 1832 (docs: governance doc fixes)

### Description
Docs-only PR (4 files: AGENTS.md, CONTRIBUTING.md, MULTI_AGENT.md, hummbl-governance/AGENTS.md).
Created by codex on 2026-08-05 after closing PR 1831 (non-minimal scope).

### Current state
- All 15 CI checks: SUCCESS (verified via gh pr view 1832 --json statusCheckRollup)
- Review decision: none (no reviews yet)
- Mergeable: MERGEABLE
- Branch: docs/codex/governance-doc-fixes-clean

### Dependencies
- Blocks: nothing
- Blocked by: nothing
- Related: supersedes PR 1831 (closed)

### Risk analysis
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Doc paths reference stale locations | Low | Low | CI lint-and-validate passed |
| Merge conflict with main | Low | Low | Mergeable: MERGEABLE confirmed |

### Alternatives
1. **Squash-merge now** — all green, docs-only, low risk. Trade-off: no human review.
2. **Request review first** — safer but slower. Trade-off: docs-only PR, review overhead may not be warranted.

### Recommendation
Squash-merge now. Docs-only, all CI green, no functional code changes.

[... continues for each item ...]

### Dependency graph
A (PR 1832 merge) ── no dependencies
B (PR 1828 CI) ── no dependencies
C (caveman H1) ── no dependencies
D (Issue #1810) ── blocked by: operator admin:org scope

### Risk-weighted priority
| Item | Impact | Likelihood of complication | Priority |
|------|--------|---------------------------|----------|
| A | Medium | Very low | 1 |
| B | High | Low | 2 |
| C | Low | Medium | 4 |
| D | Medium | N/A (operator) | 3 |

### Execution sequence
1. Merge PR 1832 (A)
2. Watch PR 1828 CI (B) — if audit passes, branch is unblocked
3. Surface #1810 to operator (D)
4. Investigate caveman H1 (C) — only if time permits

### Confidence assessment
High confidence on A and B. Medium on C (need to locate the arrow token).
D is fully operator-dependent — no agent action possible until admin:org scope is granted.
```
