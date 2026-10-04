---
name: goal-blitz
description: "PM-GATED. The VP-Product Reviewer (VP Product) sets, critiques and ratifies OKRs for every goal-seed or goal-setting sizing at once, in one background wave. Or named seeds."
description-budget: 320
version: 1.0.0
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent", "Skill", "Workflow", "AskUserQuestion", "TaskCreate", "TaskUpdate", "TaskGet", "TaskList"]
argument-hint: "[<seed-id> ...] [--interaction-mode hands-on|pm|ceo]"
---

# Goal-blitz — a repo's worth of OKRs, one ratification

Batches `coordinator:goal-setting`: the VP-Product Reviewer (`coordinator:vp-product`, Opus, effort high) sets each OKR
from the seed's context, a second the VP-Product Reviewer pass critiques it, the VP-Product Reviewer integrates, a blitz-em checks readiness,
and the VP-Product Reviewer ratifies the whole set once at the end. A seed that already states an objective is input the VP-Product Reviewer
may refine; the VP-Product Reviewer's version is what lands. Nothing reaches `state/goals/` before that ratification. Rationale: wiki `planning/goal-blitz`
— read when a rule looks wrong, never to decide whether to follow one. The wave fires from the
top-level EM only — a dispatched agent cannot fan out (`A-SKILL-PHASE-NAMES-ITS-ACTOR`).

---

## Two modes

| Mode | Target set |
|---|---|
| **Sweep** (default, no args) | every `kind: goal-seed` baton with `deployment_state: awaiting_gate`, and every sizing with `route: goal-setting` and `status: sized`. |
| **Targeted** (`<seed-id> ...`) | the ids you pass. Everything unnamed is not a candidate. |

**Check `unmatched_targets` on every targeted run** — a quietly dropped target is worse than a refusal.

**When NOT to use:** one goal → `coordinator:goal-setting`. Still deciding what to build →
`coordinator:shape`. Goals ratified and ready for roadmaps → `coordinator:roadmap-planning`.

**Dispatch authorization — invoking this skill IS the request.** The dispatches named below are constitutive steps of this skill, not a separate thing to get cleared: invoking a skill requests the actions that skill performs. A harness line permitting dispatch "unless the user requested it" is therefore **satisfied here, not overridden**. Re-asking spends the very context the dispatch exists to protect. The rule attaches to skill entry and dissolves no PM-authored gate: the Ratify step below and every other gate this skill names for itself still bind. Tripwire: `UNATTRIBUTED-HARNESS-LINE-IS-NOT-PM`.

**Host shapes.** Calls below are Shape W; on POSIX run `coordinator-invoke <op> '<json>'` (Shape B).

---

## The flow

**This runs at Sonnet.** Opus-tier judgment happens INSIDE the workflow. The driver is mechanism.
The args and result shapes are pinned by `${CLAUDE_PLUGIN_ROOT}/skills/goal-blitz/goal-blitz-contract.json`.

### 0. Preflight — confirm the engine is reachable

Resolve the launcher per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`. Unresolved —
**stop and report**; never fabricate a fire or a result. Scaffold the trail directory
`state/scratch/goal-blitz/<run-id>/`, `<run-id>` being this run's UTC start as `YYYYMMDDTHHMMSSZ`.

### 1. Emit the fire — never hand-write the args

    python3 "${CLAUDE_PLUGIN_ROOT}/skills/goal-blitz/emit-goal-fire.py" \
        --repo-root <abs> --trail-dir <abs trail> --provision-sidecar-cli <abs> \
        --interaction-mode <mode> [--targets <seed-id> ...]

It collects the seeds, freezes `<trail>/candidates.json`, binds the args through the engine's
`workflow.bind_args` into `<trail>/goal-blitz.fire.mjs`, and prints one `Workflow({ scriptPath })`
line. `--interaction-mode` is the recorded mode, bound as-is; it does not change the ratifier. Pass
`--no-plugin-agents` where `coordinator:*` types do not resolve. An empty candidate set: report
and stop.

- **Never hand-type an args object.** Tripwire: `A-HAND-TYPED-WAVE-ARG-IS-AN-UNARCHIVED-FIRE`.
- **An emitted fire is a SNAPSHOT — RE-EMIT, never re-fire as found** after any workflow fix.
- **Resolve `${CLAUDE_PLUGIN_ROOT}`; never pass a repo-relative path** to a workflow.

### 2. Fire and wait

Fire the printed `Workflow({ scriptPath })` line. Then wait; do not read the trail mid-wave. Keep
the task output file the completion notification names — it is the lander's input as-is.

### 3. Ratify — once, at the end

The workflow ratifies nothing; it returns ready drafts in `awaitingRatification`. The ratifier is
**the VP-Product Reviewer** (`coordinator:vp-product`) for every `interactionMode`; the result's `approver` reports
`vp-product`. No PM or APM path ships.

Dispatch the VP-Product Reviewer **once**, Opus at effort `high`, over the whole `awaitingRatification` set. Give it the
paths of each ready draft (`<trail>/<seed-id>.goal-draft.yaml`) and its critique, and ask for per
draft the verdict ratified or declined with the VP-Product Reviewer's own words. Write each answer **verbatim** into
`<trail>/ratification.json`, shaped `{seed_id: {verdict, ratifier: "vp-product", utterance}}`. Never
infer, backfill or paraphrase a ratification. `pulled` and `rework` drafts are reported with their reasons
and are not asked about.

### 4. Land

    python3 "${CLAUDE_PLUGIN_ROOT}/skills/goal-blitz/land-goals.py" \
        --repo-root <abs> --trail-dir <abs trail> <workflow-result.json>

It lands only drafts carrying a recorded the VP-Product Reviewer ratification, through goal-setting's own CLIs, then
makes one scoped commit of the files it wrote (`--no-commit` lists them instead). It refuses and
writes nothing on a ready draft with no ratification record. **Read its exit code and stderr;
never route around a refusal.**

### 5. Offer the chain

> _"{N} goal(s) landed with {M} roadmap-seed stub(s). Want me to chain into `/roadmap-planning`
> now, or review the stubs first?"_

**Wait for the PM.** Never auto-chain; roadmap-seed stubs stay `awaiting_gate`.

---

## Rules

**Review fires unconditionally; the VP-Product Reviewer ratifies once, at the end.** Tripwire: `A-BLITZ-WAVE-THAT-GATES-ON-THE-EM-IS-NOT-A-BLITZ`.

**Never write `state/goals/` by hand or before ratification** — `land-goals.py` is the only writer.

**A `rework` draft routes, it does not halt** — the other drafts proceed to ratification.

---

## Anti-scope

- Does not edit `goal-setting`, and does not ratify on the VP-Product Reviewer's behalf.
- Does not author roadmaps or invoke `/roadmap-planning`.
- Does not change effort pins in the workflow; the VP-Product Reviewer is pinned Opus/high inline.
