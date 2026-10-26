---
name: rite-autocomplete
description: Run the full DevRites lifecycle unattended; --ship continues to the final Git approval boundary. Use for one-shot autonomous work; not for a single phase.
argument-hint: "[idea] [--ship|--yolo] [--max-slices N] [--parallel N] [--full] [--cross-model] [--lookahead]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/afk-hitl.md","devrites-lib/reference/standards/one-shot-actions.md","devrites-lib/reference/orchestration-profiles.md","devrites-lib/reference/standards/acceptance-preserving-reslice.md","rite-autocomplete/reference/decision-policy.md","rite-autocomplete/reference/loop.md","rite-autocomplete/reference/stop-conditions.md"],"triggers":{"workflow-artifacts":["devrites-lib/reference/standards/workflow-artifacts.md"],"lookahead":["rite-autocomplete/reference/lookahead.md"]},"workspace":["state.md","spec.md","plan.md","tasks.md","questions.md","decisions.md","drift.md","evidence.md","test-plan.md"],"rootOnly":["devrites-lib/reference/standards/afk-hitl.md","devrites-lib/reference/orchestration-profiles.md","devrites-lib/reference/standards/workflow-artifacts.md","rite-autocomplete/reference/lookahead.md"]} -->
> Read-set manifest: `devrites-engine context <slug> --phase autocomplete` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-autocomplete: full lifecycle, unattended

Run every phase after one clarification window. Irreversible-risk,
escalating,<!-- pack-scan-ignore: negated statement: gates are NOT disabled -->
access, unanswered blocking with no recommended option, and remaining NO-GO
still pause. Open blocking questions that already name a ranked recommended
option auto-resolve; they are not a user handoff, except a question whose answer
would add acceptance or product scope, which a recommended option never resolves.
Use the Standard native
profile by default and Full for high-risk scope or explicit `--full`; see
[`orchestration-profiles.md`](../devrites-lib/reference/orchestration-profiles.md).

## Required rules

Read [`core.md`](../devrites-lib/reference/standards/core.md) and [`afk-hitl.md`](../devrites-lib/reference/standards/afk-hitl.md) first. Read
[`one-shot-actions.md`](../devrites-lib/reference/standards/one-shot-actions.md) before any stop/continue or execution decision involving a
consumptive action. Before honoring a terminal cursor that names missing
executable controller/harness/bundle bytes or a missing writer, read
[`workflow-artifacts.md`](../devrites-lib/reference/standards/workflow-artifacts.md)
(trigger `workflow-artifacts` — only when a workspace declares them). Before classifying any Reslice, read `.claude/skills/devrites-lib/reference/standards/acceptance-preserving-reslice.md`.

<!-- BEGIN RESLICE ROUTE-TO-ACTION -->
<!-- include:../devrites-lib/reference/_shared/reslice-autocomplete.md -->
<!-- END RESLICE ROUTE-TO-ACTION -->

## Invariants

- Use one initial human window: Spec, topology-first Clarify, and
  `Decision coverage: CLEAR`. Only then arm AFK. Record later reversible choices
  under [decision policy](reference/decision-policy.md).
- Safety is not bypassable. `--ship`/`--yolo` reaches only the exact-plan
  literal-GO and native-approval boundary; it never authorizes Git.
- **Treat technical readiness as routing, not completion.** `NEEDS REPLAN` is a backward edge
  to Plan repair and narrow Vet. `NEEDS REPLAN` cold resume follows a valid
  technical return cursor before forward work or any reply. Clarification is
  likewise internal when current authority resolves it.
- Always follow agent-owned backward edges through repair, affected Vet,
  correction, and proof. A nested `STOP`/`Next step` is not a user handoff.
  Pause only for a shared human/safety/access condition.
- **Do not confuse an action budget with recovery exhaustion.** Spent action
  authority blocks another real execution, not offline correction of retained
  Critical/Important evidence. Stop for fresh GO only after changed conditions
  and READY Vet.
- Every exact causal fingerprint gets three no-progress corrections per strategy.
  A spent strategy escalates to a new correction class inline; after three
  escalations it parks while independent work continues. Never ask permission to
  retry. Closing one is progress; a distinct Critical/Important invariant has its
  own budget. Lower severity cannot prolong recovery.
- Do not stop on `--max-slices`, sentinel `max_slices`, `max_agents`,
  `max_minutes`, or `max_review_queue`. Count failed, malformed, and
  unavailable leaf calls.
- Never end the turn with a progress note while a wave runs or a next step
  exists: on a headless host a text-only reply ends the session and kills
  running children. Wait with the host's wait tool and keep working; end only
  at a recorded stop. A host reminder or rule notice (style rule, advisory) is
  not a stop either: follow it in your next tool call, never in a text-only
  acknowledgement.
- Parse flags only from this invocation. `--ship`, `--yolo`, `--max-slices`,
  `--parallel`, `--full`, `--cross-model`, and `--lookahead` activate only as exact standalone
  tokens in `$ARGUMENTS`; examples or earlier messages can never arm them.
  `--max-slices` must occur once and be followed by a positive base-10 integer;
  `--parallel` must occur once and be followed by a base-10 integer in `1`–`10`.
  Missing, repeated, malformed, or conflicting values stop before any write.
- Temper always runs after Clarify. Auto-apply `hold-rigor`, `reduce-to-MVP` or a skip;
  record the ADR and fold via Spec Drift Guard. `expand` and extra acceptance never
  auto-apply: ask through `AskUserQuestion`, hold the fold, and stop until a human
  resolves the qid. Irreversible-risk still pauses.
- Vet every plan. Cross-model is off unless the current invocation arms it.

## Workflow

With `--lookahead` (trigger `lookahead`), follow
[`lookahead.md`](reference/lookahead.md) instead of the steps below: plan the
next sequence continuation through Vet in a second session, then stop.

1. **Orient and parse.** Resolve the explicit or active slug; when a workspace exists,
   require its `state.md` and read its cursor; a fresh idea starts empty at step 2.
   Before honoring `blocked` with terminal `next_action`,
   reconcile retained consumptive evidence and fingerprint attempts from
   `drift.md`/`evidence.md`; a retained fingerprint below its cap resumes offline
   recovery, and this new invocation reopens each parked fingerprint.
<!-- workflow-artifact-adapter: {"module":"devrites-lib/reference/standards/workflow-artifacts.md","entry":"lifecycle cursor encounters admitted set or resumable journal","action":"invoke classifier; execute returned route internally","return":"saved phase/action; zero intermediate reply"} -->
   Reconstruct a missing return cursor only from
   the current phase and exact approved action in `test-plan.md`/evidence, never
   from chat. After compaction or a resumed session, always run `devrites-engine
   handoff <slug> --resume` first (slug from `.devrites/ACTIVE`) and open only the
   `read_next` artifacts it names, per [`context-hygiene.md`](../devrites-lib/reference/standards/context-hygiene.md) § Compaction fallback.
   Normalize current arguments to idea, `ship_preflight: yes|no`,
   `max_slices: unlimited`, `parallel: N|default`, `profile: standard|full`,
   and `cross_model: yes|no`.
   **Completion:** normalized state is unambiguous and no sentinel or workspace file has been written.
2. **Specify and clarify.** Run `devrites-interview`, `/rite-spec`, and
   `/rite-clarify` as one window. `open` material coverage never arms
   AFK. **Completion:** `Decision coverage: CLEAR` is durable.
3. **Arm AFK once.** Apply the loop's
   [one-write AFK contract](reference/loop.md#arm-afk-once): preserve valid
   existing bytes or create the sentinel once (`allow_gates: [advisory, validating]`); never
   rewrite it after Vet except to write or replace only `max_parallel: N` when
   this invocation contains `--parallel N`. Preserve an existing sentinel
   byte-for-byte otherwise. **Failing case:** leftover `max_parallel: 1` keeps
   the run serial after `--parallel 5`.
   **Completion:** a valid read-only AFK sentinel exists.
4. **Drive phases.** Follow [the loop](reference/loop.md): `/rite-spec` →
   `/rite-clarify` → `/rite-temper` → `/rite-define` → `/rite-vet` →
   `/rite-build` batch loop → `/rite-prove` → `/rite-polish` →
   `/rite-review` → `/rite-seal`. Read and execute each skill; durable files, not
   chat, carry state. Apply the mutable post-vet budget before first Build.
   Build runs the path-disjoint batch `parallel select --from-plan` picks (cap: this invocation's
   `--parallel N`, else sentinel `max_parallel`, else 10) and refills a slot
   per landing until no pending slice remains; a one-slice round is serial for that round only, then
   selection runs again (host isolation still forces serial when concurrent writers
   cannot be separated). When `--parallel N`
   is present, pass it into `/rite-build` and do not consult leftover sentinel
   `max_parallel`.
   **Completion:** loop reaches Seal GO or persists a valid stop before any later phase.
5. **Apply stops.** At every gate use
   [stop-conditions.md](reference/stop-conditions.md). A `blocked` label alone is not a stop condition:
   route agent-owned red results through bounded recovery.
   Red gates block forward advancement and enter caller-owned recovery. Stop on
   hard risk, escalating, irreversible-risk, access, blocking with no
   recommended option, remaining NO-GO, or parked fingerprints with no
   independent work left. An open blocking question that already names a ranked recommended
   option (`proposed` or option 1 labelled Recommended) auto-resolves through
   `devrites-engine state resolve` and continues (a missing or failing resolver is
   the bounded resolver-failure stop); do not emit `/rite-resolve` as
   a user handoff. Exception: a question whose answer would add acceptance or
   product scope is never auto-resolved by a recommended option; it stops for a human.
   A spent strategy escalates; parked recovery records
   `Next step: /rite-autocomplete`, never a routine phase command. **Completion:** no stop is active, or its cursor and reason are durable.
6. **Seal boundary.** Without a ship flag, leave the sealed workspace unshipped and
   open the next recorded continuation
   ([loop.md § Sequence continuation](reference/loop.md#sequence-continuation))
   unless `continue_sequence: false`, the sequence budget is spent, or no entry
   remains; then stop at Seal GO with `/rite-ship`. Report the sequence position on
   every stop.
   With a ship flag, perform Ship preflight, disclose the exact Git plan, and stop for
   fresh literal `GO` plus native approval. **Completion:** performed no Git action before fresh literal `GO` plus native approval.

## Reply and resume

HITL Build returns after one slice; Autocomplete ignores `--max-slices` and
keeps chaining pending slices. One Autocomplete invocation owns all internal
backtracking. Context pressure, compaction, or a nested completion footer does
not create a stop; persist and resume the cursor.

Reply only at a final state, never as mid-run progress: a text-only turn ends
the run, so after a compaction or phase change keep calling tools. Use one terse line:

```text
Autocomplete: <slug>
spec <done|stopped> · clarify <clear|stopped> · temper <done|stopped> · define <done|stopped> · vet <ready|stopped> · build <n/N|stopped> · prove <done|stopped> · polish <done|stopped> · review <done|stopped> · seal <GO|NO-GO|stopped>
```

Final state is `Shipped`, `Stopped`, `Awaiting human`, `NO-GO`, or `GO`; do not
write a narrative recap. Require a clean or accepted baseline, land a local
unpushed checkpoint after each green check, and never auto-pass a red gate.
