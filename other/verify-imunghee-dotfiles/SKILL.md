---
name: verify
description: "Goal-backward verification that a completed feature actually achieves its goal, run before a PR or when work is declared finished. Skip mid-task progress checks, PR review comments (code-review), and pre-code planning (design)."
argument-hint: "[feature or goal description]"
allowed-tools: Bash, Read, Glob, Grep, Agent, Skill
disable-model-invocation: false
---

Verify that the completed work actually achieves its goal.

Goal: $ARGUMENTS (if empty, infer from recent commits or ask)

## System — design's read-only post-step

verify is an **optional read-only step after implementation** — not a pm-* loop node (it owns no per-task artifact, so the canonical loop is unchanged). It consumes the **session-bound plan** that `design` writes and `retro` later reads, using its `## Verifiable Success Criteria` as truth conditions (Step 1). It **persists nothing** and changes no status — confirming the goal is met is verify's job; closing the loop (plan→terminal, item→`closed.md`) stays `retro`'s. With `grill` (design's read-only pre-step) it forms the two read-only satellites bracketing `design`. Outside the loop (no explicit or session-bound plan) it just verifies a goal.

## Current Context
- Recent commits: !`git log --oneline -5 2>/dev/null || echo "N/A"`
- Changed files: !`git diff --stat HEAD~5 2>/dev/null || echo "N/A"`

## Plan delta (optional)

Resolve an explicitly supplied plan with `resolve-plan`; otherwise resolve the originating
session through the shared read-only engine using exact injected metadata:

```bash
root="$(git rev-parse --show-toplevel)" || exit 1
PM_SESSION_TOOL="<injected session tool>" PM_SESSION_ID="<exact injected session id>" node "$HOME/.config/ai/lib/worktree.mjs" resolve-session --root "$root" --tool "<injected session tool>"
```

`status: ok` supplies `plan`, immutable `base_commit`, `branch`, and `execution_root`.
Re-root every file, Git, and test command there. Any routing or mapping error blocks
verification with the engine output as evidence; never fall back to the caller checkout.

If found, compare planned vs actual:
- **Planned files**: `files_affected` from plan frontmatter
- **Actual files**: `git -C <execution_root> diff --name-only <base_commit>...HEAD`
- Report delta as informational (files added/removed vs plan). Do NOT block on delta — plans evolve during implementation.

If the session is unbound, do not inspect main launcher state. Use an explicit plan/goal
when supplied; otherwise skip this section entirely.

## Product-surface proof (when applicable)

Before deriving a READY truth condition for product-surface work, resolve exactly one
durable carrier:

- Plan-required work uses the validated active plan's
  `## Product Surface Proof Obligations`. Require matching execution root/branch/base, the
  approved `Surface Obligations` rows, any `## Artifact Ledger` entry, the approval tokens,
  and one repo-relative Durable contract path.
- Work below the independent design trigger uses the explicit no-plan handoff. Require
  `plan_requirement: not required`, no invented plan, a git execution root, the exact
  contained contract path, and the same packet already persisted under Decision Log.

Reject a missing/escaping contract path, unbound required route, unexpected plan
substitution, absent durable packet, or generic technical summary replacing rows. Read
the exact contract and require:

1. The approved `Surface Obligations` rows, the `## Artifact Ledger` entries, and the
   approval tokens under `## Decision Log & Open Questions`.
2. Exactly one `## Implementation Bridge`, carrying the implementation-stage obligations and
   their evidence.
3. Unique known row IDs, complete coverage, truth-table-valid classification/status pairs,
   affirmative code/test/render evidence for every PASS, and a repeated concrete reason for
   every N/A.

**Coverage walks the ancestor chain.** An implementation obligation covers every obligation
it derives from, and theirs in turn — follow `Derives from` upward rather than expecting a
direct link. An applicable experience or interface obligation with no implementation
obligation among its descendants is uncovered, and uncovered is not READY.

Where an artifact carries the visual decision, recompute its revision. A mismatch, an
external reference, or an artifact contradicting an approved decision is `ARTIFACT DRIFT` and
blocks READY.

A material `Craft Findings` entry — `unusable` or `degrades the task` — blocks READY even
when every obligation row passes. Contract-row closure is not the same as a sound surface.

Always recheck Required approvals and Recorded approvals before READY. Every required token must
be recorded, unique, and supported by explicit user evidence. Approval prose cannot
replace a missing token, and coverage PASS cannot authorize a stage.

Recompute the outcome from the obligation rows without mutating them:

- Any Experience/Interface GAP or Implementation contract gap -> `BLOCKED` and the exact
  design owner.
- Otherwise any implementation FAIL, NOT VERIFIED, remaining PENDING, duplicate,
  unknown, sourceless, unmapped row, incomplete evidence, or unjustified N/A ->
  `Design-Fit Outcome: NOT VERIFIED`.
- Only complete aligned applicable PASS proof plus justified non-applicable rows ->
  `Design-Fit Outcome: READY`.

A completed proof explicitly presented to this skill keeps structured `owner: verify`
while it classifies missing render evidence, invalid N/A, or final readiness. Only a
contract gap changes owner to the exact design owner; do not rewrite owner to
`ui-engineering` merely because correction may follow.

A passing test that asserts behavior contrary to approved intent is contract drift +
FAIL. Document-level or page-level substitutes do not prove a more specific contracted
component transformation. Product-surface goal verification cannot pass unless this
durable aggregation is READY. This skill remains read-only and persists no record or
lifecycle change.

## Optional acceleration — `verifier` subagent

**All verification runs inline by default** — including 5+ truth conditions and Level 3/4 depth. The steps below are self-contained; you never *need* a subagent, and there is no loss of coverage when running inline.

As an **optional** speed-up, if a `verifier` subagent is installed in your environment you may offload broad verification to it purely to keep the main context clean — useful when verification would otherwise read many files or run a long test suite (goal spans multiple modules, Level 3/4 grep across 10+ files, etc.):
- **Claude Code**: `Agent(subagent_type: "verifier", description: "<short>", prompt: "Goal: <...>. Depth: <1-4>. Plan path: <optional>. Changed files: <optional>.")` — **only if that agent is present** (pm-skills does not bundle it).
- **Codex CLI**: spawn a `codex exec` subprocess with the same focused prompt (Goal / Depth / Plan path / Changed files).

If no such agent is available, run every step inline — that is the default path. When you do dispatch, pass the plan path so the agent seeds truth conditions from the plan's `## Verifiable Success Criteria` (same as inline Step 1), and return its report directly — do NOT re-run checks inline after dispatch.

## Approach: Goal-backward

Do NOT check "were tasks completed." Instead ask:
"What must be TRUE for this goal to be achieved?" — then verify each condition.

## Steps

### 1. Derive truth conditions

If the Plan delta step found a plan with a `## Verifiable Success Criteria` section (written by `/design`), use those conditions as the truth conditions — that section is `/design`'s seed for exactly this step. Otherwise derive them: from the goal, list 3-7 concrete conditions that MUST be true.
Format:

```
Truth conditions for: [goal]
- [ ] [condition 1]
- [ ] [condition 2]
...
```

### 2. Verify each condition at appropriate depth

For each condition, apply verification levels based on scope:

**Level 1 — Exists**: the file, function, route, or config entry is present.

**Level 2 — Substantive**: not a stub — no `TODO`, `FIXME`, `NotImplementedError`,
`throw new Error('not implemented')`, empty body, or bare `pass`.

**Level 3 — Wired**: reachable from the rest of the codebase — imported, called,
routed, or registered. Prefer a call-graph query over text search when the toolchain
offers one; a grep also matches comments and dead code, so it can pass an orphan.

**Level 4 — Flowing**: real data moves through it. Run it and show the output. For a
user-facing surface, drive the running app — Claude Code bundles a `run` skill that
launches and drives it. Tests and type checks corroborate Level 4; they do not satisfy it.

### 3. Determine depth per condition

| Change scope | Required levels |
|---|---|
| Single function edit | 1 (Exists) + 2 (Substantive) |
| Feature complete | + 3 (Wired) |
| PR-ready / release | + 4 (Flowing) |

If unsure about scope, default to all 4 levels.

### 4. Report

Update the checklist from Step 1 with results:

```
Truth conditions for: [goal]
- [x] [condition 1] — Level 3 verified: [evidence]
- [ ] [condition 2] — FAILED at Level 2: stub found at file:line
...

Verdict: X/Y conditions verified
```

Each condition MUST have a fenced code block showing the verification output.
Failed conditions — report to the user with specific failure point.

## Rules

- Never mark a condition as verified without showing evidence
- If a condition fails, do NOT fix it silently — report the failure
- Stub detection is mandatory for Level 2 (grep for patterns above)
- This skill verifies. It does not modify code.
