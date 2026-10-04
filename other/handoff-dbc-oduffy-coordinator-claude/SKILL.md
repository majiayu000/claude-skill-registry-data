---
name: handoff
description: Mid-workstream save-state under context pressure; a continuation.
allowed-tools: ["Read", "Write", "Bash", "Grep", "Glob"]
argument-hint: "[optional context]"
---

# Session Handoff — Save State for Next Session

## Handoff Lineage

**Predecessor is the baton this session was born with.** A session that writes a CONTINUATION
always has one — the assembler resolves it, never the EM. Deflection kinds (`spinoff`,
`goal-seed`, `roadmap-seed`) carry `predecessor: none` by schema invariant
(`handoff.schema.json`'s `kind`/`predecessor` cross-field rule) — also not an EM inference; this
does not mean every handoff has a predecessor. Spinoffs are PM-authorized forks only, never
self-authored. Tripwire: `A-SESSION-IS-NEVER-STANDALONE`.

> **The baseline trigger is involuntary** — context pressure forcing a stop mid-workstream before
> the next action can land. Reaching for `/handoff` because the work *feels* like a good place to
> pause is the disqualifier. Workstreams end via `/workday-complete`, `/merging-to-main`, or
> `/quick-wrap`, never via handoff. **Four deliberate triggers also fire. 1 — the PM asks:** their
> ask IS the authority; no context-pressure test applies or is owed back. **2 — parking:** the next
> action is blocked outside this session's reach (a PM decision, a sibling repo, a peer's landing)
> for longer than this session, and the remit is *resume when the blocker clears*. **3 —
> plan→execute:** review-integration done and the plan is ready to execute. **4 —
> review-owed close** (§ Step 0): the owed review is un-runnable in this session for a reason on
> the ratified closed class of un-runnable-here reasons, cited by name.

> **Continuation vs. fork.** This skill writes a *continuation* — work this session was doing that
> someone resumes. A *different* mid-session topic for someone to pick up cold is `/spinoff`
> (`kind: spinoff`, `predecessor: none`). **The next phase of the same multi-phase workstream
> (research → goal-setting → plan → execute → verify) is a continuation**, even when the phase
> boundary reads as a new topic — never redirect it to `/spinoff`.

> **A `roadmap-baton`'s successor is a `roadmap-baton`** and inherits `stub_id`, `roadmap_id`,
> `blocks`, `blocked_by`, `sprint`, `wave`. The predecessor is superseded and archived in the same
> move — succession kills the originator, roadmap batons included. Both halves or neither:
> `blocked_by` resolves by `stub_id`: inheriting without archiving duplicates a globally-unique id,
> archiving without inheriting strands the dependent.
>
> **The archival half runs via `d6`'s supersession route** (see § Supersession) — `mode='supersede'`
> needs `--continued-into` naming the successor; do not hand-stamp `deployment_state: continued`
> as a substitute, and do not restore `handoff.reconcile_open` (superseded by K-057).

The mechanical spine — deliverable/initiative id inheritance, frontmatter scaffolding,
`handoff_phase` stamping, tracker refresh, and (on a clean chain) predecessor archival — is
computed by `baton-assemble brief handoff`, which fires at entry. The brief, its open
decisions, the decisions-file template and the literal `apply` line arrive with this invocation.
Write your answers into the template at the named path and run the rendered line. An unanswered `<CHOOSE: …>` or `<NOTE: …>` placeholder makes
the file unparseable, and `apply` refuses it.

**The brief names the rung the lineage resolved from.** If it is not the artifact this handoff is
written from, that is the mis-link — on the plan→execute trigger the source is the PLAN, and a
wrong rung gives plan and executing handoff different `deliverable_id`s. Stop and resolve before
running `apply`.

**Divergent `deliverable_id`s are a judgment point.** The earliest artifact's id wins; name the
survivor and how you know.

**`apply` is the single route out — never hand-execute the directive list.** `apply` cannot run? Repair `PATH` and retry; still blocked → leave the draft at its target path and name it in the final report (`coordinator-tripwires/a-non-path-path-is-a-break-class-fault-reported-not-worked-around.md`).

No brief block in context means the entry hook failed open: run `baton-assemble brief handoff`
with no artifact-path, resolved per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`
(`coordinator-tripwires/an-autofire-hook-that-did-not-fire-is-silent.md`).

Once `apply`'s commit lands, best-effort trigger project-rag's SCIP rebuild in the background —
never waits, never blocks this ceremony: `"$_py"
"${CLAUDE_PLUGIN_ROOT:-<content-root>/coordinator}/bin/scip-rebuild-at-ceremony.py" --ceremony handoff`
(§ Plugin-local `coordinator/bin/`, `resolve-coordinator-bin.md`).

Procedure detail — body authoring, `d5` release, next-steps durability,
`carried_items` minting and its disposition gate, dirty-tree case-(c) and safe-commit grouping,
supersession, orientation refresh — arrives with this invocation from
`coordinator/skills/handoff/residue/`; you should not need to open it.

**`d5` releases the plan artifact-claim only — the path-touch plane is a separate close-time
check.** Before this session ends, run `session-claim-cli list-claims-by-session <sid>` and
release each `path\t<p>` line it does not need with `session-claim-cli release-artifact artifact
<path>`. Recheck any path a safe-commit already committed but this session then edited again.
`coordinator/docs/wiki/coordinator-tripwires/touch-claim-retirement-is-commit-path-specific-who-claims-path-is-the-only-instrument-that-sees-it.md`.

---

## Step 0: Trigger Check — Is Context Pressure Actually Forcing This?

Confirm at least one trigger fires and no NO-test trips. The PRIMARY question: can this session
still take its next action? If it can *and nothing outside the session blocks it*, you are
deferring, not handing off — a violation regardless of how tidy the state looks. If nothing fires,
STOP and take the next action here.

**Two triggers skip this gate.** A PM ask is self-authorizing — write it, don't audit it against
context pressure and don't answer with a trigger analysis. A blocked next action is real too: name
the blocker and the event that clears it in the successor's remit.

**On a box whose successor cannot be reached (a cloud session), context pressure is not a handoff
trigger at all.** Append what the post-compaction self needs to the baton this session already has
(`baton.carry_forward`; the context-pressure advisory names the path), and continue the run. The
engine selects this posture with no configuration —
`coordinator/docs/wiki/coordinator-tripwires/tripwire-registry/a-mode-default-can-be-answered-by-the-environment.md`;
tripwire `A-HANDOFF-NAG-ASSUMES-A-SUCCESSOR-THAT-IS-CHEAP-TO-REACH`.
A PM ask and a blocked next action still qualify anywhere.

**Trigger 4 (review-owed close) is an instance of this same blocked-next-action skip, not a
second discharge.** The ratified closed class of un-runnable-here reasons is stated once, at
`coordinator/docs/wiki/coordinator-tripwires/two-ceremonies-two-predicates-one-handover.md`
(which cites its own ruling record); the roster is reproduced inline only so no second file need
be opened. Trigger 4 qualifies only when the
owed review is un-runnable in this session for a reason on that class — a hard-stop oracle
disagreement, a
quota-exhausted dispatch, a live peer's files this session must not touch, or the `review_scale`
gate returning unresolved on the row-4 brightline inputs where the per-owned-commit summation
that would otherwise name the scale by hand is itself un-runnable in this session for a
separately named external reason (not merely un-performed) — each with its clearing event outside
this session's reach. Name the blocker and the event that clears it, in the
successor's remit, exactly as above — no parallel discharge for the review case, and no reason
admitted off this roster by analogy.
**A successor session existing is not itself a qualifying clearing event:** the clearing event is
the outside-the-session fact (a PM/reviewer-pool decision, a quota reset, a peer's landing) that
lets the review actually run, never merely the fact that a successor could pick this up. Naming a
successor without naming that fact is the "the next session can review this" tell
`workstream-complete/SKILL.md:82` already forbids, and does not qualify. `/handoff` itself reviews
nothing (`residue/065-does-not-review.md`) — the successor runs the owed review, against the
settled diff, at its own close.

**A parked successor's frontmatter is `deployment_state: awaiting_gate` plus a named gate —
`blocked_by` when a stub or handoff on the graph clears it, `gate_notes` when nothing on the
graph does (a sibling plane's ruling) — with `pickup_ready` false or omitted.** The scaffold hands
you `ready_to_fire` + `pickup_ready: true`; leaving that above blocker prose advertises the baton
as available work. Authorization-pending is not a
gate — a PM handoff or `/pickup` is itself the authorization, so never author `awaiting_gate` for
that reason; a parked baton stays legal only when its blocker is something else — a sibling repo's
landing, a peer's dependency, a PM product decision.

**Inverted antipattern:** picking up a handoff does not license appending progress to the
predecessor's (now `status: claimed`) body instead of writing a successor; the pickup index treats
it as historical. About to edit a
`status: claimed` body to record what you just did? STOP and run this skill from the top.
