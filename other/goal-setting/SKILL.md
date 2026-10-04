---
name: goal-setting
description: "PM-GATED. Raw vision into ratified OKRs and roadmap seeds."
version: 1.0.0
user-invocable: true
---

# Goal-Setting — Vision to OKRs to Scaffolded Stubs

> **Posture:** vision-in, OKR-out; neither rubber-stamp nor gate. Each KR must be
> weekly-perceptible (observable moving this week); one that fails is a later-impact aspiration,
> surfaced as a shaping question, not a rejection.

**Entry points:**

1. **Direct invocation** — the PM arrives with raw vision, no formed OKR yet.
2. **Pickup-from-goal-seed** — a deferred `kind: goal-seed` stub; run this skill on the captured
   vision.
3. **Conform intake from a sizing-object** — `coordinator:sizing` hands an optional
   `state/sizings/<id>.yaml` ahead of Step 1 (`route: pm-decision`+`xl_exit: roadmap`, legacy
   `route: roadmap`, or direct-routed `route: goal-setting` XXL). Receive-and-use-if-present, never
   a wall: absent one, Step 1 runs exactly as today, and the sizing lobby never gates or refuses a
   `goal-setting` invocation. Field-crossing table: wiki.

**What this skill produces:** a ratified OKR (one Objective + ≤5 Key Results, weekly-perceptible)
via `coordinator-doc-new --type goal`; `kind: roadmap-seed` stubs pre-tagged to the goal, one per
roadmap-worth-of-work; optionally `kind: goal-seed` stubs for deferred vision-slices; an OFFER to
chain into `/roadmap-planning` (PM-gated, never auto-run).

<HARD-GATE>
This skill DOES NOT auto-author roadmap plans, invoke `/roadmap-planning` without PM
acknowledgment, or bypass its PM gate. It scaffolds stubs and offers the chain. The PM decides
whether and when to fire each stub.
</HARD-GATE>

---

## When NOT to invoke

- **Problem not yet converged** (still deciding *what* to build) → `coordinator:shape` or
  `coordinator:brainstorming` first.
- **Single-feature scope**, no broader OKR arc → straight to `coordinator:plan`.
- **Roadmap already has goals** — picking up an existing roadmap-seed stub against an
  already-ratified goal → `/roadmap-planning` directly.
- **Several seeds or goal-setting sizings at once** → `coordinator:goal-blitz`, the batched route, where the VP-Product Reviewer sets and ratifies the OKRs.

---

## Ceremony

### Step 1 — PM states Objective and candidate Key Results

The PM names the **Objective** (qualitative, direction-setting) and one or more **candidate KRs**
(raw is fine). Do NOT prompt for a specific format — the ceremony imposes structure through
critique, not intake.

**When a sizing-object is present** (Entry point 3), it pre-populates this step's raw framing in
body prose only, never new frontmatter (`appetite` is never a KR or stub `cost:`). Field-by-field
crossing: wiki.

**PM-assent record for a direct-routed XXL:** once this step's PM utterance happens, write
`pm_resolution.xl_route_assent` on the sizing-object recording it. Detail: wiki.

### Step 1b — Offer to record competitive context (optional)

If the PM's vision names or implies a domain and `state/strategic/self-description.yaml`'s
`competitors[]` is empty, offer once (else skip silently):

> This reads like <inferred domain> work — want me to record inspirations / peers / competitors /
> aspirational-targets? Goes in your repo's strategic self-description. (Skip freely.)

On opt-in, record via `coordinator:strategic-self-description-refresh`'s scaffold path (schema:
`coordinator/schemas/strategic-self-description.schema.json`; `provenance: curated`) — never a
second marking store. On decline, proceed to Step 2 without repeating the offer.

### Step 2 — Dispatch the VP-Product Reviewer as full OKR critic

> **Do not ask whether to dispatch** — invoking this skill IS the request for the dispatch this
> step names; it dissolves no gate this skill's own body names.

**Dispatch via `Agent(subagent_type: "coordinator:vp-product", model: "opus")`.** Inline verbatim:

> You are the VP-Product Reviewer (VP of Product, they/them). You are reviewing a draft OKR set for strategic rigor.
> Your job is to act as a full OKR critic, not a rubber-stamp.
>
> Assess: (1) Is the Objective a real Objective — qualitative, direction-setting, not a metric or
> tactic in disguise? (2) Are the KRs real Key Results — measurable outcomes, not activity/output
> proxies? (3) Is the SET reasonable — ≤5 KRs; more means the Objective is unfocused? (4)
> Weekly-perceptibility per KR — can an agent or PM observe it move this week? If not, flag as a
> later-impact aspiration with a weekly-perceptible rewrite, or note the PM should defer it.
>
> Return: verdict per element (PASS/FLAG/REJECT), specific rewrite suggestions for
> flagged/rejected elements, a SET-level verdict (GO/REVISE/REFRAME). Give the EM and PM the
> material to revise it themselves — do not rewrite the whole OKR yourself.

The dispatch runs in the background: tell the PM to expect a wait, and stand down until the VP-Product Reviewer's idle
notification — no polling or re-dispatch.

### Step 3 — EM+PM integrate the VP-Product Reviewer's critique in-dialogue

No artifact exists on disk yet. REJECT items are rewritten or dropped; FLAG items rewritten or
accepted with a stated rationale; weekly-perceptibility notes rewritten or deferred to a
`kind: goal-seed` stub. EM presents the critique, proposes a revised shape, asks the PM to confirm.

**Do NOT proceed to Step 4 without explicit PM confirmation on the revised OKR.**

### Step 4 — Scaffold the goal artifact

Resolve every CLI in Steps 4-5 (incl. 5a/5b) per the ladder in
`${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`.

`coordinator-doc-new --type goal --title "<objective-slug>"`, resolved per that ladder.

Fill: `objective:` (ratified text), `key_results:` (≤5, weekly-perceptible), `period:` (one of the
schema enum `day|week|repo|quarter|year` — e.g. `period: quarter`, `period_value: Q3-2026`),
`status: active`.

Once filled, invoke `emit-goal-from-artifact <path>` (the goal-pipeline emitter per
`goals-okr-system.md` § Emit → Cockpit → Cockpit Pipe), resolved per the same ladder, where
`<path>` is the `state/goals/*.yaml` path `coordinator-doc-new --type goal` printed — scaffolding
alone does not emit. On doubt about flags, run `emit-goal-from-artifact --help`.

### Step 5 — Spawn downstream stubs

**5a. Roadmap-seed stubs** — one per roadmap-worth-of-work (roughly: one `/roadmap-planning`
invocation, one coherent capability arc; when in doubt, fewer/larger — the PM can split at
pickup):

`coordinator-doc-new --type roadmap-seed --goals "<goal-id>" --title "<roadmap-topic>"`.

Each stub carries `kind: roadmap-seed`, `origin_goal_id:` FK (via `--goals`), `deployment_state:
awaiting_gate`, a one-line title naming the capability arc.

**5b. Goal-seed stubs (optional)** — for vision-slices out of scope this period, or KRs deferred
rather than rewritten:

`coordinator-doc-new --type goal-seed --title "<deferred-vision-slice>"`.

Each stub carries `kind: goal-seed`, `deployment_state: awaiting_gate`, and a brief body
capturing the vision-slice verbatim — raw over polished.

### Step 6 — Offer the PM-gated chain

> _"Goal artifact and {N} roadmap-seed stub(s) scaffolded. Want me to chain into
> `/roadmap-planning` now, or review the stubs first?"_

**Wait for PM response.** Never invoke `/roadmap-planning` without explicit PM direction.

### Step 7 — Commit goal + stubs

Stage only the goal artifact and stubs this run scaffolded — no blanket add:

Commit per `snippets/scoped-commit-route.md`, subject `goal-setting: ratify <objective-slug> +
scaffold {N} downstream stubs`, pathspec exactly the goal artifact plus the stubs this run
scaffolded.

---

## Out of scope

- **Roadmap authoring** — `/roadmap-planning` owns it; auto-chaining bypasses the PM.
- **KR tracking infrastructure** — cockpit-contract `goal.schema.json` owns event emission.
- **Deferred-goal fleshing without PM pickup** — a `kind: goal-seed` stub stays dormant until entry
  point 2.

---

## Self-verify before reporting DONE

The VP-Product Reviewer dispatched via `coordinator:vp-product`; PM confirmed the revised OKR before any artifact hit
disk; goal artifact scaffolded then emitted; each roadmap-seed stub carries `origin_goal_id:` and
`deployment_state: awaiting_gate`; `/roadmap-planning` offered, not auto-invoked; commit scoped to
goal artifact + stubs.
