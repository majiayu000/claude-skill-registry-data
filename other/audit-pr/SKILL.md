---
name: audit-pr
user-invocable: true
version: 5.4.0
argument-hint: <pr-number> (optional — defaults to the current branch's PR)
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Audit a whole PR against the delivery contract and return MERGE-READY or
  evidenced blockers with the full URL. Consumes the current review-change
  REVIEW-PASS receipt instead of re-running review axes; posts a SHA-bound
  ready comment; never edits or merges. Triggers: "audit-pr", "is this PR
  ready", "merge gate".
---

# Audit PR

The manager's **"can this ship?"** gate. A read-first audit over the *entire* PR —
its SPEC, all phases, docs, CI status, and review receipt — that returns a single
verdict: **merge-ready** or a ranked list of **blockers**. **Never edits,
refactors, or merges.** The human merges, or an active
`advance --fullauto` invocation consumes the SHA-bound verdict and performs
its separate fail-closed merge step.

`audit-pr` does **not** re-review the diff. It consumes the current SHA-bound
`review-change` receipt (the `REVIEW-PASS` comment marker) as the review
evidence, blocks on a missing or stale receipt routed to `/review-change`, and
independently evaluates only the delivery gates below.

## Turn contract — verify before ending the turn

```
✓ The review receipt was consumed from one PR snapshot: `headRefOid` + newest
  matching `review-change:pass` marker fetched together; absent or any SHA
  mismatch → blocker routed to `/review-change`, current → its scope/axes/
  acceptance coverage/manual checks acknowledged without re-review
✓ Terminal hygiene was read from state, not assumed: tree clean, branch pushed,
  PR not a draft (`bun scripts/audit-pr-gate.mjs hygiene --pr <N> --apply`)
✓ Upstream lineage was re-verified (current plan receipt + parent spec receipt,
  digests recomputed), every obligation row is `verified`/`n/a`, and no planning
  finding is open — stale or missing lineage is a blocker, never a formality
✓ The verdict block was printed in the fixed format: `VERDICT: MERGE-READY | BLOCKED` with ranked, evidenced blockers
✓ The PR's FULL URL is printed in the verdict header (the user may be juggling
  several projects and agents without a CI monitor — the link in the chat is
  the contract, never "PR #N" alone)
✓ MERGE-READY verdict? Then the comment was POSTED by
  `bun scripts/audit-pr-gate.mjs comment` (re-reads, exits non-zero unless the newest marker
  names the head) — a comment, never a commit-message tag. BLOCKED → no comment
✓ Nothing was edited, refactored, or merged; merge authorization is outside
  this skill and cannot be inherited from docs or an earlier session
✓ No review pass was composed or reconstructed: a missing/stale receipt is a
  blocker, never a prompt to re-run review axes from this skill
✓ Closure integrity was evaluated and its result stated explicitly: pass /
  blocker / n-a (fix-governed PRs are always n-a; never skipped
  silently)
✓ Scope integrity (descope) was evaluated and its result stated explicitly:
  pass / blocker / n-a (no unit-referencing issues born on the branch → n-a;
  never skipped silently)
✓ Architectural-invariant preservation was evaluated and its result stated
  explicitly: pass / blocker / n-a (no project document → n-a; never skipped)
✓ The closing `→ Next:` block is printed as the ABSOLUTE last output
```

About to end the turn with any box unchecked? The turn is NOT done — complete
the missing box first (weak models drop end-of-document duties; this list is
first on purpose).

## When to use

- After the work is "done" and before merging — the final gate once `review-change`
  is clean (its `REVIEW-PASS` receipt is posted) and all phases are committed.
- When you want one defensible answer to "is this PR actually ready?" rather than
  trusting that every loose end was tied off.

`review-change` reviews the *diff* for quality and posts its SHA-bound receipt;
`audit-pr` consumes that receipt and audits the *PR as a unit of delivery* — that
everything the SPEC promised is present, traceable, and green. A missing or stale
receipt is a blocker routed back to `/review-change`, never re-litigated here.

## Scope

The whole pull request: the branch vs. the default base, **plus** its SPEC and
planning artifacts, the roadmap entry, the doc map, the PR body, issue links, and
CI. Default target is the current branch's PR; accept a PR number to target another.

## Step 0 — Discover the project & the PR (always first)

1. **Project contract.** Per the agent guide's **Workflow conventions** +
   **documentation map**, then read what THIS skill needs: the roadmap and the
   project's verification gate (type-check / tests / build / CI). Do **not** load
   full feature/fix templates — the SPEC below is the only planning artifact this
   audit reads (AC 14).
2. **The PR.** Identify it and read it in full (forge CLI per the project's
   Workflow conventions — examples use `gh`):
   ```sh
   gh pr view <N> --json number,url,title,body,baseRefName,headRefName,headRefOid,isDraft,mergeable,mergeStateStatus,files,commits,statusCheckRollup,closingIssuesReferences
   ```
   If no PR number is given, resolve the current branch's PR
   (`gh pr view --json ...`). If none exists yet, audit the branch vs. the default
   base and say "no PR open yet" — the contract still applies.
3. **The SPEC.** Locate the governing SPEC — `docs/features/<NN>-<slug>/` (feature)
   or `docs/fix/<n>-<topic>/` (fix) — and its planning artifacts (`PLAN.md`,
   `TASKS.md`, `progress.md`, `testing.md`, `known-issues.md`, `decisions.md`) when
   present. The SPEC is the source of truth for what "done" means.

## Step 1 — Consume the review receipt (always, before any gate)

The review evidence is the SHA-bound `REVIEW-PASS` receipt `review-change` posts
on the PR — **never** a re-review composed here. Fetch `headRefOid` and the PR's
comments together, then find the **newest** comment carrying the marker
`<!-- review-change:pass sha=<40-hex> contract=v1 -->`:

```sh
gh pr view <N> --json headRefOid,comments
```

- **current** — marker `sha` equals that snapshot's `headRefOid` (the current
  head SHA). Acknowledge
  its scope/axes, acceptance coverage, invariant result, and manual checks as the
  review evidence, then evaluate the delivery gates below.
- **absent** — no matching marker on the PR → **BLOCKER**: no review evidence at
  the head; route to `/review-change`.
- **stale** — a marker exists but its `sha` does not equal `headRefOid`. Any SHA
  mismatch voids the receipt → **BLOCKER**: route to `/review-change` for a
  re-review. Do not use a local `git diff` to override the PR-head comparison.

Never compose, reconstruct, or "spot-check" the review from the diff to clear a
missing/stale receipt — that is `review-change`'s turn, and re-litigating axes
here is exactly what the receipt gate removes (AC 13).


## Progressive loading — mandatory audit route

The reference allowlist is exactly the six linked paths below. Never invent or
read another `references/` path. After discovery and the Step 1 receipt check,
every audit loads and applies exactly these five mandatory resources in order:

1. [01 merge gates](references/01_MERGE_GATES.md) for delivery, CI, traceability,
   review-receipt, and mergeability evidence.
2. [02 closure and scope gates](references/02_CLOSURE_AND_SCOPE_GATES.md) for
   capability closure and descope provenance.
3. [03 audit process](references/03_AUDIT_PROCESS.md) to gather, decide, persist
   blockers, and post the SHA-bound MERGE-READY comment.
4. [04 verdict](references/04_VERDICT.md) before output, then
   [05 routing and guardrails](references/05_ROUTING_AND_GUARDRAILS.md). These
   mandatory resources own the `docs/workflow/REPOSITORY_STATE.md` evidence
   rules and Architectural invariants gate.

Read [portability](references/PORTABILITY.md) only when the declared forge or
agent actually lacks a named primitive; otherwise skip it. The project artifact
`docs/workflow/REPOSITORY_STATE.md` is evidence, not a skill reference. All
resources are one hop from this file. Missing evidence or a missing required
resource is a blocker; never infer a pass.

## Merge ownership

This skill **never merges**, including when project docs contain `merge: auto`,
the user previously approved a merge, or a tool retained an earlier permission.
Those signals cannot change this skill's read-first boundary.

The **sole automated merge authority** is the AUDIT stage of an actively invoked
`advance --continue --fullauto` run. Its MERGE-READY comment is evidence,
not permission; the repository wrapper independently verifies that comment,
the forge's current head/default base, green checks, and the `merge: fullauto`
decision fetched at that head. The wrapper owns fresh sync checks, transient
state, merge execution, cleanup, and the automerge PR comment. A standalone/
manual call to this skill always hands the MERGE-READY URL to the human.


## Portability

Translate forge commands, never the gate semantics. Use the explicit fallbacks
in [portability](references/PORTABILITY.md).

## Relationship to other skills

```
execute-phase (all phases done) ─▶ review-change (REVIEW-PASS receipt posted) ─▶ audit-pr ─▶ merge
                                                                                │
                     blockers ─┬─ receipt absent/stale ──▶ /review-change ──────┘ (re-review, re-audit)
                               ├─ in-scope            ──▶ execute-phase ────────┘ (fold, re-audit)
                               ├─ out-of-scope        ──▶ unit-lane --fix
                               └─ deferral            ──▶ triage-issue
```

- Consumes the `review-change` `REVIEW-PASS` receipt (its scope/axes, acceptance
  coverage, invariant result, manual checks) plus the artifacts of `unit-lane` /
  `execute-phase` (SPEC, phases, docs, `Closes #N`).
- `audit-docs` is the cross-document coherence check; `audit-pr` is per-PR merge
  readiness; `product-audit` is the periodic, product-wide full sweep.

## Done when

- The review receipt was consumed: a current marker was acknowledged, or a
  missing/stale one became a blocker routed to `/review-change` (never re-reviewed
  here).
- Every applicable gate has a pass / blocker / n-a verdict backed by cited evidence.
- A single top-line verdict (**MERGE-READY** or **BLOCKED** with ranked blockers) is
  reported **with the PR's full URL in the header**, each blocker routed, with the
  human's manual-verification list explicit.
- On MERGE-READY the merge owner is explicit: a standalone audit hands the URL
  to the human; an active `advance --fullauto` AUDIT stage receives the
  SHA-bound verdict and owns every later merge check.
- The **closing `→ Next:` block is printed** (merge link → then the next unit via
  `/unit-lane <unit>` or `/triage-issue`; BLOCKED → the routed fix, then re-audit).
- Nothing was edited, refactored, or merged.
