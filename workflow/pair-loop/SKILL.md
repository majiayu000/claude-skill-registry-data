---
name: pair-loop
description: "Unattended delivery loop: per iteration, selects eligible cards via pair-next, runs a dependency + mutex analysis, composes implement-batch for a mutex-safe parallel batch (or drives one card sequentially), hands the autonomy policy (until / prepare / merge) to the batch — which merges a review-approved card only when the merge gate allows it — and evaluates the stop predicate. In an environment with a fan-out runner it delegates the whole unattended run to the pair-loop workflow; elsewhere it drives exactly one eligible card and reports a continue-token."
version: 0.2.0
author: Foomakers
---

# /pair-loop — Unattended Delivery Loop

Advance the backlog unattended, within a policy the team controls, context-safe, halting only where the tier policy requires a human. Reads its policy from [`tech/automation.md`](../../../.pair/knowledge/guidelines/collaboration/automation/automation-policy.md) (adoption delta over the KB default schema, D21) and composes `/implement-batch` (#219) for the actual per-card implement→PR→review pipeline — this skill never re-implements it.

## Arguments (optional)

| Argument | Value | Effect |
| --- | --- | --- |
| `--root` | an issue id (epic or story) | Scope every `/pair-next` call this run makes to that subtree, exactly as `/pair-next --root` does. |
| `--predicate` | a `<selector> ⇒ <condition>` string | Overrides `tech/automation.md`'s `## Stop Predicate` for this invocation only (Argument > Adoption > KB default). |
| `--filter` | a label (or, with `## Autonomy`, a list, or `*` = every card in scope) | Selection: which cards `/pair-next` returns this run. Replaces the `## Eligibility` tier comparison this loop used to make itself. |
| `--assignee` | a login or `@me` | Selection: keep issues assigned to that user (`/pair-next --assignee`). |
| `--status` | comma-separated canonical macrostates | Selection: keep issues in those macrostates (`/pair-next --status`). |
| `--until` | `ready` \| `pr` \| `merged` | How far each card is driven; handed to the batch (the delivery cycle on N cards). Default `pr`: nothing merges. |
| `--prepare` | a gate: `hold-always` \| `hold-never` \| `hold-when[; has: <labels>][; lacks: <labels>]` | The prepare gate, handed to the batch (US-523): who prepares a Draft / Ready-without-breakdown card — `hold-always` (default) parks it for a human, `hold-never` proceeds alone recording assumptions, `hold-when` proceeds alone unless a boundary escalates (`needs-review`; an escalated card is not re-picked until a human acts). |
| `--merge` | a gate, same grammar | The merge gate, handed to the batch: the batch merges a review-approved card only when it allows it (default `hold-always`: parks `awaiting-human`). |
| `--iteration` | a positive integer | The starting iteration count — used when re-invoking from a printed continue-token; never required on a fresh run. |

Precedence: argument > argument preset > explicit adoption key (`## Autonomy`, then translated legacy sections) > adoption preset > KB default — every effective value is printed with its source.

This loop SELECTS and REPEATS; it does not merge. `--until` / `--prepare` / `--merge` are handed to `/implement-batch`, which is `/pair-workflow-cycle` on N cards — same rules, merge per the merge gate, escalation at every stage boundary — and the rule lives only in `autonomy-policy.mjs` (D18).

## Core Rule: Zero Merit Logic (D18)

This skill classifies nothing and judges nothing. It reads tags, board state and the policy file verbatim, and evaluates a predicate — that is the whole of its decision surface. Every acceptance criterion below is grep-verifiable against that constraint.

## Step 0: Read the Policy — Fail-Closed

1. **Act**: Read `.pair/adoption/tech/automation.md` (project-relative, resolved the normal adoption-file way).
2. **Note**: `## Autonomy` is honoured, not refused: whether it is declared is `autonomy-policy.mjs`'s `parse().declared` (an empty section is off, exactly as in the cycle, `pair-cli run` and `/pair-next`). This skill reads no key of it — selection keys reach `/pair-next`, `until` / `prepare` / `merge` reach the batch, and the batch's policy script resolves them (argument > adoption > default).
3. **Check**: Does a filter resolve? The selection filter resolves argument > `## Autonomy` > `## Eligibility` (the `filter:` key, the translated legacy tier) (`autonomy-policy.mjs resolve`, the same cascade the workflow runs) — a file without `## Eligibility` is NOT off while an argument or `## Autonomy` supplies the filter.
4. **Act**: **Empty `## Autonomy` — ask the preset once (US-576).** When the resolution shows nothing declared or passed (every effective source `default`, no translated legacy section) and a human is present, ask `full / escalate-red / supervised` (Enter = `supervised`) and write `preset: <answer>` under `## Autonomy` in `.pair/adoption/tech/automation.md` through `/pair-capability-record-decision`, then resolve again. Unattended (no human to answer): write nothing, run with the KB defaults (every gate held — the supervised behaviour) and print how to set one (`preset: escalate-red` under `## Autonomy`, or `--preset` on `pair run`). If NO source then supplies a filter (or the file is absent), report "automation is off — no filter resolved (no argument, no `## Autonomy` `filter:` or `preset:`, no `## Eligibility`)" and **exit cleanly**. This is not an error (D21) — never fall back to the KB's recommended `risk:green` default on the project's behalf.
5. **Act**: When `## Eligibility` is declared, extract and validate it (the seven HALT triggers), `## Auto-Advance`, `## Stop Predicate`, `## Max Parallelism`, `## Audit Location` — the full algorithm lives in [automation-policy.md](../../../.pair/knowledge/guidelines/collaboration/automation/automation-policy.md) and is **not restated here** (D18: the matching/parsing rule has one owner). A malformed value at any of the five knobs **HALTs before any card is touched**, naming the file and the offending value. `## Auto-Advance` may only ever name the SAME tier `## Eligibility` declares — a card outside eligibility is never selected in the first place, so no other tier could legally advance.
6. **Act**: Resolve `tech/risk-matrix.md`'s `## Tag Projection` declaration — every label this project actually emits (e.g. `risk:green`, `risk:yellow`, `risk:red`) — and hold it ready to pass as `tagProjectionFamily`. This is what lets `## Max Parallelism`'s per-tier override keys be checked against real, emitted tiers rather than shape alone (a tier that is emitted but never eligible, like a maintained-but-idle `risk:red` override, is still a legal narrowing target).
7. **Verify**: All five knobs resolved (or their fail-closed default applied), and the Tag Projection family resolved. Proceed to Step 1.

## Step 1: Realization — Three Tiers (ADR-017 §4, amended by ADR-021)

Fan-out is ONE capability with THREE realizations, in preference order: **(1) in-harness** (Claude Code's `Workflow`, Codex subagents), **(2) external driver** (`pair-cli run` — a fresh engine process per iteration, re-invoking on the continue-token: the portable baseline, and a legitimate choice even where subagents exist, since a separate process respects ADR-017 §3's context isolation more strongly than a subagent does), **(3) degraded** (one card + a continue-token a human/CI/cron re-invokes). Tier 2 is what retired ADR-017's "No portable unattended loop" limitation: the caller §4 leaves to a human is automated, not replaced.

1. **Check**: Does the current environment expose a fan-out runner (Claude Code's `Workflow` tool)?
2. **Act — Claude Code**: Delegate the entire unattended run to the `pair-loop` workflow (distributed alongside `pair-implement-batch` in the `workflows` registry), passing `{ policyText, root, filter, assignee, status, until, prepare, merge, overrides, predicateOverride, startIteration, tagProjectionFamily }` — the resolved policy text (still REQUIRED here: this loop's own `## Eligibility` / `## Auto-Advance` / `## Stop Predicate` / `## Max Parallelism` / `## Audit Location` knobs are read from it; the batch itself no longer requires it), `--root`, `--filter`, `--assignee`, `--status` (selection, only those given) and `--until` / `--prepare` / `--merge` (only those given), any run-argument overrides (pin-sequential, exclude), `--predicate` as `predicateOverride` (the Argument tier of the cascade, replacing the adoption file's `## Stop Predicate` for this invocation only), `--iteration` as `startIteration` (resuming the counter from a continue-token rather than restarting at 0), and the Tag Projection family from Step 0.5. The workflow validates every one of these by type and content before touching any card — `root` and the predicate reach agent prompts that run `gh`. It then drives every iteration — selection, dependency + mutex analysis, batch composition, `implement-batch` composition (the batch is the cycle on N cards: it decides every stage boundary through `autonomy-policy.mjs`, and under `until: merged` merges a review-approved card through `cycle-merge.mjs` ONLY when the merge gate allows it — the tier re-read, head pinning and `pair-review` / `pair-explicit-approval` checks live in that script, not here), recording each card's outcome (merged, awaiting-human, escalated, target-ready, PR-ready, failed), audit (write verified, never assumed), stop-predicate evaluation — in fresh per-card subagents (ADR-017 §3, architectural invariant: this orchestrator's context never grows with the number of cards). A card the run is DONE with this run — `escalated` (an autonomy condition fired: not re-drivable), failed, already merged, parked awaiting human, or halted by a refused merge — is excluded from every later iteration in the same run, never silently re-driven from scratch.
3. **Act — any other tool** (no in-harness fan-out runner): take the **one-card path** below — never iterate multiple cards in this session's own context. Whether that single card is the WHOLE run (tier 3, degraded) or one iteration of an unattended run (tier 2) is the CALLER's business, not this skill's: an external driver re-invokes on the continue-token this step prints, in a fresh process each time, so the steps here are identical either way. Say which tier the invocation is in the output only when the caller told you (e.g. `pair-cli run` states its own resolution):
   - Run `/pair-next` once, scoped by `--root`, `--filter`, `--assignee` and `--status` (those given, else the adoption's resolved values) — the selection is `/pair-next`'s, never re-filtered here. The same holds for a card's control state: macrostate through the State Mapping, DoR fallback, out-of-process, conflict flag — `/pair-next`'s Control-State Resolution, referenced here and never re-derived.
   - Apply the dependency analysis (ordering only — a single-card run has no parallel set to compute) and pick the first unblocked card. An untagged card is `risk:red` (quality-model §3.2 fail-safe).
   - Drive that one card with `/pair-workflow-cycle --card <id>` passing the same `--until` / `--prepare` / `--merge` (only those given): the sequential fallback IS the cycle one card at a time with the same arguments, and every rule, the merge included, is the cycle's — this skill merges nothing itself. Where `/pair-workflow-cycle` is not installed, `/implement-batch` with a single-story batch (passing `policyText`, the verbatim Read of `tech/automation.md`, `""` only when the file does not exist, and the same `until` / `prepare` / `merge`) is the same engine.
   - Record the outcome the cycle printed (merged | awaiting-human | escalated | target-ready | PR-ready | failed): only TERMINAL outcomes (merged, awaiting-human, PR-ready, target reached) and DURABLE failures (`failed-*`, `escalate` — the review/fix budget is spent and a human decision is owed — or any status the loop does not know) end a card's drive for the run; an `escalated` card (an autonomy gate fired, `needs-review`) is skipped while the selection still reports it escalated and re-picked once it reports `escalated: false`; only a TRANSIENT failure (a dead dispatch, a stall, an engine/API error, a card the batch returned no outcome for) is retried, within a per-run budget (default 1), then excluded as `retry budget exhausted` (maintainer decisions 2026-10-06; the same rules as `pair-cli run --watch`); an unconfirmed awaited-human comment is recorded, never swallowed.
   - Append the iteration to the audit file at the resolved `## Audit Location`.
   - Write/update the checkpoint via `/pair-capability-checkpoint` for the driven card's story.
   - Stop, and print a **continue-token**: `pair-loop [--root <id>] [--filter <v>] [--assignee <v>] [--status <v>] [--until <v>] [--prepare <v>] [--merge <v>] [--predicate '<text>'] --iteration <n+1>` — only the arguments given or effective, each value single-quoted (shell-safe: a value with spaces or `;` pastes back whole); a resumed run accepts them all, so a stricter argument (e.g. `--merge hold-always` over an adoption `merge: hold-never`) is never lost. The caller (human/CI/cron) pastes it back to resume. No new persistence format (Assumption 7): the token is the loop's scope + arguments + predicate + iteration counter rendered as a re-invocation line.
4. **Verify**: Exactly one card advanced this invocation (degraded path) or the workflow ran to its own stop condition (fan-out path). Never both cards and context growth in the same session.

## Boundaries — What This Skill Does Not Do

- **Never re-implements the per-card pipeline.** Implement→PR→review is `/implement-batch`'s (#219); this skill composes it and consumes its outcomes only (PR opened/updated, review-approved, escalated, failed).
- **Never merges.** Merge authority has ONE owner: the merge gate of the delivery cycle (`cycle-merge.mjs`, run by `/implement-batch` / `/pair-workflow-cycle`, default: nothing merges). This skill holds no merge call and no merge rule; it only records what the batch reports.
- **Never posts its own per-task progress comments.** The breakdown-to-task feedback loop — checklist ticks plus one batched comment per run iteration — belongs to `/pair-process-implement` ([task-progress-feedback.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/task-progress-feedback.md)), which this skill reaches through `/implement-batch`, so a supervised run already carries it. A second writer here would double every line. The one comment this skill does post is its own: the card-level "awaits human action" note in the degraded path, which reports the loop's decision, not a task's outcome.
- **Never modifies `/pair-next`.** Selection stays the frozen atom (ADR-017 §1) — this skill only ever passes `--root` / `--filter` / `--assignee` / `--status`.
- **Never widens an override.** A pin-sequential or exclude override may only narrow the parallel set the dependency+mutex analysis computed; it can never add back an excluded card.

## Output Format

```text
LOOP RUN:
├── Policy:        [tech/automation.md — filter: <resolved list> (source) | none resolved, automation off]
├── Mode:          [in-harness fan-out (workflow) | one card + continue-token (driver-re-invoked or manual)]
├── Iterations:    [N]
├── Cards driven:  [id, id, ...]
├── Merged:        [id (merged by the batch under the merge gate) | none]
├── Parked:        [id (awaiting-human | escalated: conditions + stage) | none]
├── Audit:         [<working_path>/<Audit Location>]
└── Stop reason:   [predicate satisfied | max-iterations reached | nothing eligible | HALT — <reason>]
```

One-card path only (tiers 2 and 3), appended — this line is what an external driver reads to re-invoke:

```text
CONTINUE-TOKEN: pair-loop [--root <id>] [--filter <v>] [--assignee <v>] [--status <v>] [--until <v>] [--prepare <v>] [--merge <v>] [--predicate '<text>'] --iteration <n+1>
```

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) for the standard scenarios. Additional cases:

- **`tech/automation.md` absent, or no filter resolves (no argument, no `## Autonomy` `filter:`, no `## Eligibility`)**: not a degradation — automation is off by design (D21), report and exit cleanly.
- **`/pair-capability-checkpoint` not installed** (degraded path): skip the checkpoint write; the continue-token and the audit file remain the resume mechanism.
- **`/pair-capability-verify-quality` not installed**: the merge stage never merges without a locally-verified gate set — that card halts for the human instead of guessing green.

## Notes

- **Host runtime (US-479 T-25, t9d-1).** This loop runs in the Workflow sandbox: no shell, so it cannot run the engine's host recipe (`cycle-runtime.mjs entry/observe/finalize`). Metrics and the ONE PR synthesis still reach the PR because the final reviewer runs `finalize` when no host runtime is present (ADL 2026-09-13); a shell host (`pair-cli run`) is where the full recipe belongs.
- This skill and the `pair-loop` workflow share one contract: the workflow is the fan-out realization, this file is the entry point, the degradation guard, and the portable single-card path. Neither re-derives the automation-policy.md schema — both read it through the same extraction rules.
- Non-Claude-Code note (ADR-017 §5, amended by ADR-021): every other supported harness runs the one-card path — as tier 2 when an external driver (`pair-cli run`) re-invokes it unattended, as tier 3 when a human/CI/cron does. This is not a lesser mode by accident: it is the same safety property (no in-context multi-card iteration) applied without a fan-out primitive to lean on, and under tier 2 the fresh process per iteration makes the isolation stricter, not weaker.

- **Automation overview**: see the [automation overview](../../../.pair/knowledge/guidelines/collaboration/automation/delivery-cycle.md) for the whole delivery cycle — stages, autonomy gates, realizations.

**Timeouts, stalls and retries.** What bounds a hung stage or selection, which failures are retried (transient only) and how this skill behaves outside Claude Code (one card per invocation, continue-token) is owned by `.pair/knowledge/guidelines/collaboration/automation/delivery-cycle.md#9-timeouts-stalls-and-retries-by-surface` — not repeated here.

**Troubleshooting — `SyntaxError: Unexpected keyword 'export'` when launching `pair-loop` by name.** The Workflow runtime accepts exactly one top-level `export` (`export const meta`); every pair workflow script ships that way since the loop script's helper exports were removed. The error therefore means the runtime is evaluating a STALE copy: a script cached when the session started (before an update), or an older installed `.claude/workflows/pair-loop.js` (releases up to the fix shipped 17 helper exports). Pair registers workflows nowhere else — only `<project>/.claude/workflows/` — so: restart the session (the by-name registry is read at start), run `pair update` if the installed file still has more than one `export`, or launch with `scriptPath` pointing at the current file, which is read fresh.
