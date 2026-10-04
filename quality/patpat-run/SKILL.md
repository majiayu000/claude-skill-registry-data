---
name: patpat-run
description: Drive, checkpoint, validate, resume, or safely take over multi-phase engineering work through a deterministic local state machine. Use for long work, arbitrary branch or handoff pickup, and tasks that must survive context loss without granting delivery authority.
---

# Patpat Run

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) in full. Do not load the router.

Read [sequence verifiable units](../patpat-loop/principles/sequence-verifiable-units.md), [proof over proxy](../patpat-loop/principles/proof-over-proxy.md), and apply the [multi-phase run playbook](../patpat-loop/playbooks/multi-phase-run.md).

Use [`scripts/run_state.py`](scripts/run_state.py) for durable graph state. Require a Git worktree with at least one commit and store state under Git metadata. Print the absolute store path at each checkpoint. Do not commit run state or create a tracked handoff unless the user explicitly requests it. Keep an append-only [human decision trail](references/decision-trail.md) at `<git patpat/runs>/<run-id>/decisions.tsv` next to `state.json`; same privacy as run state.

For a checked multi-unit plan, initialize [`scripts/program_state.py`](scripts/program_state.py) from the validated plan. Reject unordered units with exact, ancestor, or conservatively overlapping glob ownership. Keep dispatch closed until the integration owner supplies an absolute content-bound parallel-gate receipt that binds the plan digest, every unit's unique isolation identity, and all earned-parallelism checks. Open dispatch with `set-gate dispatch open --receipt /absolute/path --integration-owner <identity>`, then assign each dependency-ready frontier unit with an explicit actor, receipt-bound isolation identity, and expected generation. Pass the returned generation on every worker-controlled head, state, verdict, and unit-inbox mutation; never infer the current generation for a caller. Change a unit head only with its expected current head (`none` for the first head), and require that head to contain every declared dependency head in its Git ancestry. Treat each verdict slot as write-once until head change or reassignment. Reassignment increments the fencing token and rejects stale worker output. Closing dispatch revokes every active assignment; reopening it requires fresh assignment calls. Record unit events through the inbox with that unit's current head. Require the bound integration owner for program-wide events and acknowledgement; peek first and acknowledge a sequence only after processing the handoff. A changed dispatch receipt clears the inbox so a new authority epoch cannot inherit unattributed events. Bind verification and independent review to commits present in the repository. Require a fresh passing verification before review, and reject the verifier, assigned worker, or integration owner as reviewer. Recheck dependency ancestry before verdicts, completion, and delivery. Open delivery only when every dependency has fresh evidence. Any unit head change clears that unit's proof and inbox; a changed dependency head also revokes downstream assignments and evidence before work can resume. The program store coordinates state only; its local identities are self-asserted labels, not authentication. It does not stop an old process from writing an external surface, spawn workers, observe providers, or grant commit, push, merge, publish, or deploy authority.

Before fan-out, write the earned-parallelism receipt as bounded JSON and pass its absolute path to [`scripts/team_shape.py`](scripts/team_shape.py) with `--parallel-gate-receipt`, `--program-id`, `--plan-digest`, `--integration-owner`, every `--unit`, observed capacity, and an explicit worker budget. Writable selection fails closed unless those expected values match the receipt; receipt-internal claims do not bind themselves to the active job. A boolean claim alone cannot admit writable fan-out. Accept serial fallback; the recommendation and receipt never grant authority. Send typed handoff cards and evidence pointers, never full worker transcripts. Mutation commands print bounded receipts by default; request `--full` only for deliberate ledger inspection. Use `status --brief` or `status --unit <id>`, and page the inbox with `--after` plus `--limit`.

Record declared authority and prohibitions at initialization, but never treat that record as fresh delivery approval. Require a structured proof contract before `ACT`, a content-bound `file:<absolute-path>` evidence receipt before `REVIEW`, and independent review evidence before `LEARN` or `REPORT`. Use the host's native absolute-path form; both POSIX and Windows paths are valid. Invalidate proof when committed, staged, unstaged, untracked, assume-unchanged, or embedded-repository state changes. After three consecutive failures with the same blocker, graph node, and snapshot, stop the run as `BLOCKED`.

Never record secrets, tokens, raw private logs, or sensitive payloads in run state or receipts. Point only to a safe, inspectable evidence file. Treat deletion or content change as stale evidence.

If a process interruption leaves a lock, inspect it first. Use `unlock` for a run or `recover-lock` for a program only when the engine proves a same-host owner is dead. Let the engine reject live, malformed, or cross-host locks; never delete them by assumption.

Route completion through `patpat-ship` when delivery intent exists. Explicit Patpat activation alone does not authorize default commit-and-PR; see the operating protocol and default-delivery playbook. Durable-run mechanical gates remain separate. Overnight stops merge-ready. Merge only with explicit land or merge language and green checks.

On resume, validate the store, compare live repository state, inspect intentional and pre-existing changes, and continue from the earliest valid graph node. Never trust a checkpoint merely because it parses.

When inheriting an arbitrary branch, transcript, or handoff without a valid Patpat store, apply the [session takeover playbook](../patpat-loop/playbooks/session-takeover.md) before initializing a new run.

When taking over, lock the time window, do not reconstruct from transcripts alone, and verify surfaced PRs, branches, and tickets with live git and gh.

Program stores created before assignment fencing are schema v1. Do not trust or silently upgrade their actor labels or evidence. Run `migrate-v1 --invalidate-legacy-evidence` explicitly; migration preserves plan and heads, clears legacy evidence and inbox, closes gates, and requires fresh dispatch plus assignments.

When the request is a queue of independent PRs or a linear verified stack, apply the [autopilot playbook](../patpat-loop/playbooks/autopilot.md). Owners build and prove. The root verifies. Landing still requires a named delivery action.

For a multi-PR queue or stack, write a bounded host-neutral JSON plan and validate it with [`scripts/validate_plan.py`](scripts/validate_plan.py) before fan-out or implementation. Give every unit an id, dependencies, disjoint ownership unless dependency order serializes an overlap, build command or `N/A: <reason>`, observable proof, targeted/live/performance checks or explicit `N/A: <reason>`, `exact-head` evidence binding, and `independent-pass-before-delivery` review gate. Record claimed delivery authority once for the plan, then prove that authority again at execution time; a valid plan and an open dispatch gate never grant permission. Do not encode fixed model or lane counts.

## Proof closure

Close repository mutations through:

- [`patpat-verify`](../patpat-verify/SKILL.md)
- [`patpat-review`](../patpat-review/SKILL.md)
