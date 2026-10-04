---
name: verify
description: Verify-before-done — exercise the current change end-to-end against its acceptance criteria (the SDD plan's, or the ticket's) and report a per-criterion PASS/FAIL verdict, then record the outcome to memory. This is the concrete action that satisfies moflo's verify-before-done gate (`gates.verify_before_done` / `/flo -v` / `/flo -sd`). Use before `gh pr create` when the change must be proven to work, not just tested in passing. Verifies only — it does not fix; on FAIL it reports the gaps and stops.
arguments: "[issue-number | spec-slug]  (defaults to the current branch's issue/spec)"
---

# /verify — Verify Before Done

Prove the current change **actually does what it was supposed to** before it ships. `/verify` is the end-to-end completion check for moflo's SDD cycle: it takes the change's **acceptance criteria**, exercises the change against each one with concrete evidence, and returns a per-criterion verdict. It is the action that makes the [verify-before-done gate](../../guidance/moflo-sdd.md) mean something — running it is what unblocks `gh pr create` when `gates.verify_before_done` is on.

**Arguments:** $ARGUMENTS

`/verify` **verifies, it does not fix.** If a criterion fails, it reports the gap and stops — the caller (you, or the `/flo` flow) decides what to do. This separation is deliberate: a checker that also patches can rationalise its way to green.

## What satisfies the gate

Invoking this skill (name `verify`) trips the `record-verify-run` hook, which flips the `verifyRun` state. **That alone does not open the gate**: `check-before-done` also requires the recorded verdict to be `PASS`, which reaches it from the `metadata.overall` your Step 5 store writes. So a run returning FAIL leaves `gh pr create` blocked — as it should, since the change did not meet its criteria — and a run that stores prose without `metadata` counts as *no verdict* and blocks too.

**Only `/verify` satisfies it** — `/ward` and `/quicken` are targeted audits, not an end-to-end verification. A source edit *after* verifying invalidates both the flag and the verdict, so run `/verify` as the last step before the PR.

## Step 0 — Memory first

Search memory before reading files, same as any task (satisfies `memory_first`, surfaces prior verify runs for this area):

```
mcp__moflo__memory_search { query: "verify <feature keywords>", namespace: "verify" }
```

**Search `verify`, never `learnings`.** Verdict records moved out of `learnings` — see Step 5.

## Step 1 — Locate the acceptance criteria

Resolve the criteria to check against, in priority order — **stop at the first that exists**:

| Source | How to find it | When |
|--------|----------------|------|
| SDD **plan** | `flo sdd list` → the slug for this branch → read its `plan.md` "Acceptance Criteria" | `--sdd` runs |
| SDD **spec** | same slug → `spec.md` "Acceptance Criteria" | spec authored, no plan criteria |
| **Ticket** | `gh issue view <n>` → the `## Acceptance Criteria` section | plain `-v` run, no spec |
| **Inferred** | derive 2–4 checkable criteria from the diff + PR intent, and say so | nothing above exists |

Never hand-write the spec path — get it from `flo sdd` (Rule #1: the CLI builds every path with `path.join`). If an explicit `<issue-number | spec-slug>` argument was passed, use it directly.

## Step 2 — Map each criterion to a concrete check

For every acceptance criterion, pick the **cheapest evidence that actually proves it**:

| Criterion shape | Verification action |
|-----------------|---------------------|
| Logic / behavior / bug-fix | A passing test that **specifically** exercises it — reuse the suite run already done this session (see below); run only a missing/targeted test |
| Build / types / packaging | The project's build or typecheck command — reuse if already run since the last edit |
| Integration / e2e | The project's e2e or integration runner |
| User-facing / UI / CLI output | Run the real thing — use `/run` to launch the app/CLI and observe the actual output (a screenshot or captured stdout is the evidence) |
| Config / docs / non-code | Inspect the artifact directly and confirm it says what the criterion requires |

**Reuse fresh evidence — do not re-run what this session already ran.** This is the key to avoiding a **double verify**. If the tests/build already ran green this session with no source edit since — which is exactly the case when `/flo` invokes `/verify` right after its Tests phase — that run **is** the evidence: cite it, don't execute it again. `/verify`'s job is the *mapping* (which criterion is proven by which existing result) and *gap-finding* (criteria no check covers), **not** re-running the suite. Only execute a check whose evidence doesn't already exist this session.

**Discover the commands from the project — never assume.** When you *do* need to run something (a criterion nothing covered yet), read `package.json` scripts / `Makefile` / language toolchain and use what the repo already uses (`npm/yarn/pnpm test`, `vitest`, `jest`, `pytest`, `cargo test`, `go test`, …). Cross-platform (Rule #1): invoke the project's own scripts, don't shell out to `bash`-only constructs.

## Step 3 — Execute the gaps and gather evidence

Run **only the checks whose evidence doesn't already exist** this session; for everything else, cite the run that already happened. Capture, per criterion, the **specific** evidence: the passing test name, the build exit, the observed output. "The suite passed" is not evidence for a criterion unless a test actually exercises *that* criterion — if none does, that is a **gap**, not a pass (consider `/ward` to fill it, in a separate step). The distinction from a plain test run is the whole point: tests prove the code works; `/verify` proves the change did **what the ticket asked**.

## Step 4 — Verdict

Emit a per-criterion table. **PASS only when every criterion has affirmative evidence.** Any criterion with no covering check is `UNVERIFIED`, which counts as **not passing**.

```
| # | Acceptance criterion | Evidence | Verdict |
|---|----------------------|----------|---------|
| 1 | <criterion>          | <test/output/observation> | ✅ PASS / ❌ FAIL / ⚠️ UNVERIFIED |
```

Overall verdict is PASS iff no row is FAIL or UNVERIFIED.

## Step 5 — Record the outcome to memory

Always store the result (feeds routing/learning and the SDD trail). Store it **twice over**: the prose summary in `value`, and the Step 4 table itself — unflattened — in `metadata`.

```
mcp__moflo__memory_store {
  namespace: "verify",
  key: "verify:<slug-or-issue>",
  value: "<overall PASS/FAIL> — per-criterion: <criterion → evidence → verdict>; commit <sha>",
  tags: ["verify", "sdd"],
  metadata: {
    type: "verify-record",
    issue: "<slug-or-issue>",
    commit: "<sha>",
    overall: "PASS" | "FAIL" | "UNVERIFIED",
    verifiedAt: "<ISO-8601>",
    criteria: [
      { id: 1, statement: "<criterion>", verdict: "PASS" | "FAIL" | "UNVERIFIED",
        evidence: "<test name / observed output>", freshlyExecuted: true }
    ]
  }
}
```

**Store to `verify`, never `learnings`.** A verdict is audit exhaust — one commit, one issue, criteria that never apply again — and `memory_search` returns a bounded set, so every verdict parked in `learnings` displaced a reusable lesson. The move is free: `record-learnings-stored` matches any `memory_store`, and `record-verify-outcome` keys on the `verify:` **key prefix**, not the namespace. Both gates still fire.

**Why both.** `value` is what gets embedded for semantic search, so it stays prose — a JSON blob there would degrade every future `verify` search. `metadata` is stored verbatim and not embedded, so the structure survives without that cost. `memory_retrieve` returns the parsed `metadata` object for non-chunk entries, which is what makes the record readable rather than write-only.

**`freshlyExecuted` is required on every criterion, not optional.** Step 3 deliberately permits *citing* an earlier green run instead of re-executing. That is a sound cost optimisation, but it means evidence may be a citation rather than a fresh result — set `freshlyExecuted: false` when you cited. Without that flag a later reader silently inherits stale evidence and cannot tell a re-verified criterion from a re-cited one.

**Never record an exit code.** Claude Code's `tool_response` for Bash carries `stdout`/`stderr` but **no exit status**, and PostToolUse does not fire at all when a command exits non-zero. `evidence` is therefore descriptive by necessity; a field named `exitCode` would be agent-narrated fiction, which is the problem this record exists to remove.

`overall` MUST agree with the Step 4 rule — PASS iff no criterion is FAIL or UNVERIFIED. Record a FAIL as a FAIL; the store is the audit trail, and a verdict that only ever reads PASS is worth nothing.

## Step 6 — Report

One concise summary: overall verdict, the per-criterion table, and — on FAIL/UNVERIFIED — exactly which criteria are unproven and what evidence is missing. Do **not** open the PR or edit code from here; hand the verdict back to the caller.

## See Also

- `.claude/guidance/moflo-sdd.md` — the SDD cycle and the verify-before-done gate this skill satisfies
- `.claude/skills/fl/sdd.md` — how `/flo` invokes `/verify` at the verify step
- `.claude/skills/ward/SKILL.md` — fills coverage gaps `/verify` surfaces (audit, not a completion gate)
- `.claude/skills/run/SKILL.md` — launch the real app/CLI for user-facing criteria
