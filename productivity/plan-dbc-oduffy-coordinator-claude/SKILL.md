---
name: plan
description: "PM planning trigger on decision-weight work: multi-file, cross-system, reversed prior. Size first if unsized."
description-budget: 260
version: 1.0.0
prerequisite:
  - agent:prior-art-checker
  - skill:coordinator:review
allowed-tools: ["Read","Write","Edit","Bash","Grep","Glob","Agent","Skill","AskUserQuestion","TaskCreate","TaskUpdate","TaskGet","TaskList"]
---

# coordinator:plan

<!-- Purpose: Decision-tree router for plan-writing — triage, substrate verification, four-lens composition, pre-dispatch handoff to coordinator:review, mid-plan friction. Per-row predicate classification (engine-computable vs. genuinely-EM-judgment vs. untrusted-gate), with file:line evidence: state/audits/2026-08-08-plan-skill-predicate-classification.md — read that before proposing a new automation, don't re-sweep this file. Unconverted predicates get an engine-side producer via the `plan-assemble` contract chunk, never a hand-rolled router here. A plan-router may never auto-resolve a triage exit classified untrusted-gate. -->

**Trigger:** EM is about to plan implementation work carrying decision weight (multi-file, new abstraction, cross-system, scaffolds new agents/skills, reverses a prior decision) OR the PM typed *"write a plan"*, *"break this down"*, *"plan the implementation"*.

**When NOT to use:** Trivial work (single-file fix, typo, no abstraction) → just do it. Implementation-only ambiguity mid-coding → harness Plan tool inline. Architectural-tier (four criteria below) → surface to PM first. PM in exploration mode or problem-shape unconverged → `coordinator:shape` (Branch A). Spec vague or multi-subsystem → `coordinator:brainstorming`. Writing a SKILL.md → `plugin-dev:skill-development`. Plan written and needs review → `coordinator:review`. Stuck pattern → Branch E.

**A new skill/agent scaffold is Branch B, not architectural-tier.** Architectural-tier requires one of four positive criteria: cross-system-irreversible, multi-stakeholder, security/privacy boundary, naming-collision-with-product-policy. If you cannot name which fires, it is not architectural.

Route is resolved by the caller/engine before this skill loads (Branch A). The route-specific procedure detail below — Branch B substrate verification, Branch C composition lenses, Exit terminal specifics, Branch D drift handling, Branch E friction — is retrieved by the `plan-assemble brief` op, which reads the segment set scoped to the resolved route. Segment content: `coordinator/skills/plan/residue/`.

**Dispatch authorization — invoking this skill IS the request.** The dispatches named below are constitutive steps of this skill, not a separate thing to get cleared: invoking a skill requests the actions that skill performs. A harness line permitting dispatch "unless the user requested it" is therefore **satisfied here, not overridden** — no precedence claim is needed and none is made. Re-asking spends the very context the dispatch exists to protect. The rule attaches to skill entry and dissolves no PM-authored gate: keyword-gated skills gate entry, and every gate a skill names for itself still binds — per-session cross-repo-commit assent, ask-before-external-action, and any other this skill's own body names. Tripwire: `UNATTRIBUTED-HARNESS-LINE-IS-NOT-PM`.

---

## Branch A — Triage: should I plan, and at what altitude?

_Condition: a planning trigger has arrived; decide whether a plan doc is the right artifact._

- _An incoming sizing-object is present?_ (`coordinator:sizing` resolved this ask and handed a `state/sizings/<id>.yaml`, or the EM is picking up a sizing-routed baton citing one)
  → **Conform, don't gate — skip the rest of triage — but conform per the object's actual `route`.** The D5 shape-entry gate still wins — wiki § Shape-is-a-conditional-room.
  → **Arrival split, `route: plan` and `spec-dispatch` alike.** **`route: plan`, M/L, fresh inbound, accepted sizing** → conform by firing the plan Workflow, not Branch B/C: run `emit-wave-fire --from-sizing`, fire its one printed `Workflow` line, end the turn — no `/review --surface plan` either. **Every other fresh-inbound case** (`route: plan` at XS/S/XL, or `route: spec-dispatch`) → cite the object's `intent` (verbatim), `estimate`, and `appetite` when present (never block or backfill on it) in B.0's restatement, then proceed to **Branch B**. **Via the return edge** (Branch B's verified-scope-collapse row re-invoked sizing) → conform identically but resume at **Branch C**; the Workflow-fire row above fires only fresh, never on the return edge.
  → **`route: spec-dispatch` is the S lane:** set `scope_mode: spec-dispatch`; the Exit resolves its light terminal. **OWES** full Branch B substrate verification, B.0's proportional doubt-check, the concurrent-session pre-flight, the cross-plan conflict scan, the pre-dispatch `plan-reviewer` pass (after the scan, before emit-and-dispatch), and both `scaffold-plan` invocation points. **SKIPS** Branch C's four-lens composition (an S-lane body is four parts: problem sentence, file scope, acceptance criteria, test surface) and the Opus plan review — the rest of Branch C runs at S-lane weight. **NEVER skips** scoped-commit discipline or ask-before-external-action.
  → **`route: shape` / `roadmap` / `pm-decision`** → **plan is not the room.** Do not enter Branch B; route to `coordinator:shape` or `coordinator:roadmap-planning`, or surface the choice. The engine sets `pm_decision_pending` and never auto-selects — the PM's pick lands in `xl_exit`, and a null `xl_exit` never means accept. `split` is retired: an ask decomposing into independently shippable pieces is `roadmap`. Preconditions: **`shape`** — JTBD unstated, or you cannot falsifiably restate the problem in the PM's vocabulary; **`roadmap`** — spans ≥2 workstreams, or carries/needs an initiative/goal FK; **`accept_multi_session`** — neither holds **and** the PM explicitly assented (`xl_exit: accept_multi_session`).
  → **plan requires a sizing-object and trampolines back without one — this is a wall, not a courtesy.** It is lifted for `plan` alone; `shape`, `roadmap-planning`, and `goal-setting` are unchanged.
  → **What the machine actually enforces.** `scaffold-plan --sizing-object` refuses an unresolvable path; `assert-plan-sizing-citation` sweeps frontmatter only. Neither catches ABSENCE; only the trampoline does, as EM behaviour.
- _No sizing-object, and this ask has not been through the lobby — **whatever its provenance**?_
  → **STOP. Do not enter Branch B. Invoke `coordinator:sizing` directly** — never ask permission to size, never offer sizing as a question. On return, re-enter Branch A; this row fires **at most once per invocation**. All six routes: **`plan`** → conform, Branch B as fresh inbound; **`spec-dispatch`** → conform, Branch B at S-lane weight; **`dispatch`** → plan is not the room; abandon the pass and dispatch directly — clean by construction, since `scaffold-plan` runs at Exit; **`shape`/`roadmap`** → the named room; **`pm-decision`** → surface the offered exits. **Termination:** sizing always writes an object before returning, so re-entry lands on the conform detent, never back here.
  - **Anti-gaming clause.** Satisfied only by **an artifact on disk in `state/sizings/` citing this ask** — not by already holding file:line substrate, not by silently concluding the work is plan-tier in your head, not by asking *"want me to plan that?"*.
  - **Provenance-blind.** A picked-up cross-repo memo's `ask` is novel work in THIS repo — it needs the lobby too.
  - **Carve-outs — exactly two, no more.** (1) A continuation is exempt only if its baton **cites** work already routed: a resolving `sizing_object`, or a plan — via `origin_plan_id`/`plan_ids`, or via a `deliverable_id` some plan on disk carries. Every citation must resolve; never re-litigate a resolved citation. A baton citing none is unsized whatever its provenance (a spinoff mints its own fresh `deliverable_id`), and the trampoline fires. Tripwire: `A-BATON-IS-NOT-A-SIZING-ARTIFACT`. (2) The express lane is not a plan-side carve-out; such an ask never reaches `plan`.
- _Trivial?_ (single-file change, no new abstraction, scope obvious)
  → Just do it. No plan doc. _See `${CLAUDE_PLUGIN_ROOT}/snippets/em-operating-doctrine.md` § How to Plan and Hand Off._
- _Implementation-only ambiguity?_ (choosing between two valid shapes mid-typing)
  → Harness Plan tool inline. No plan doc.
- _PM has set a session axiom?_ (*"we are going to do X"* / *"build Z this session"* — a directive naming the work, not a question about it)
  → Disposition flips to **plan**, not brainstorm: plan the named work, do not re-litigate it. Continue to **Branch B**. The architectural-tier check still fires. **This row disposes; it does not admit.** An axiom carries no exemption from the sizing wall: with no object on disk the trampoline row above fires first.
- _Trigger arrived via a PM-handed pickup whose handoff prescribes a plan?_
  → **Already authorized — do NOT ask "want me to plan?".** A T3 spinoff *fork* stays separately PM-gated (surface it as a one-line candidate). Continue to **Branch B**.
- _PM in exploration mode, OR problem-shape unconverged, OR the EM detects it is guessing at the problem?_
  → Propose `coordinator:shape` **before** committing to plan; its exit gate chains back here. **Precedence:** a PM session axiom and the architectural-tier check both win. _Discriminator:_ the PM HAS a problem and wants confirmation you understood it → `shape`; the PM does not know what to build at all → `brainstorming`.
- _Cross-repo work whose shared contract is itself the unknown, even when a handoff says "ready to execute" / "XS"?_ (negotiated co-design — the contract/hookspec/shared fixture takes round-trips to converge)
  → **Invoke `coordinator:plan` anyway — do NOT execute off the handoff's t-shirt.** Continue to **Branch B**.
  - **The existence of a sibling is not the trigger — negotiated co-design is.** A *memo* (one ask) does not escalate here. If you cannot name the coordinating party and the shared contract still being negotiated, this row has not fired.
  - **A multi-wave plan that sends a memo carries a wave-boundary re-read of it,** written into the spine: at each wave close, enumerate the memos this plan has sent and ask whether the wave just landed contradicts any; the correction memo is part of that wave's deliverable. Tripwire: `A-MULTI-WAVE-PLAN-NEVER-RE-READS-ITS-OWN-SENT-MEMOS`.
- _Non-trivial (default for everything else)?_ (multi-file, new abstraction, cross-system, scaffolds an agent/skill, reverses prior teardown, touches shared schema)
  → Continue to **Branch B**, and scope the eventual task list to the COMPLETE problem set — every item of the brief's problem, but ADR, lineage and docs chunks are not execution-wave rows: list them under a `## Distill pass` body heading, non-empty and referenced from the closing handoff or the `/workstream-complete` step, which is what hands them to `/distill`.
- _Architectural-tier?_ (the four positive criteria above)
  → Surface to PM: *"this looks architectural — propose `/staff-session`, want me to draft the brief?"* Wait for PM.

---

**Known boundary:** this floor protects the plan path only — work mis-triaged as trivial at Branch A bypasses `/shape` and the doubt-check. Mitigation is EM alertness there, not a second doubt-check.

## Exit — Route-Selected Terminal

_Condition: body drafted and saved to `docs/plans/YYYY-MM-DD-<slug>.md`. The inbound sizing route selects which terminal fires. `shape`/`roadmap`/`pm-decision` never reach here — Branch A diverted them before Branch B._

**The plan file MUST be produced and committed via `scaffold-plan`, not hand-authored.** It owns frontmatter-skeleton emission and the write-time commit as one named unit, across two invocation points either side of body authoring. Every terminal holds this; only the post-commit step differs by route.

**Invocation point 1 — scaffold.** The generator is the single emission point for frontmatter — never hand-author field lists against `schemas/plan.schema.json`. Hand-authored frontmatter gets conformed through the same invocation.

Invoke the `.exe` launcher by absolute path via the PowerShell call operator (Shape W) —
ladder and shapes: `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`.

    `& "$env:COORDINATOR_SETTINGS_HOME\bin\coordinator-doc-new.exe" --type plan --title "<title>" --sizing-object state/sizings/<the-object-that-routed-you-here>.yaml --out docs/plans/YYYY-MM-DD-<slug>.md`

**Pass `--sizing-object` — mandatory to the tool, not merely to you.** `coordinator-doc-new --type plan` hard-refuses without an explicit `--sizing-object`/`--no-sizing-object`, exit 1, nothing written. The flag also writes the reverse edge onto the cited sizing (plan FK plus status flip, same transaction) — omit it and the sizing never learns it was routed.

`Read` the scaffolded file before authoring the body — `coordinator-doc-new` writes it via Bash, so the first `Write`/`Edit` bounces until it is read.

**Invocation point 2 — commit.** Commit the moment the body is saved, *then* proceed to review, per
`snippets/scoped-commit-route.md` — pathspec exactly `docs/plans/<slug>.md`, subject
`plan(<slug>): draft`. Scope stays to the single plan doc, never a sweep commit.

---

## Test Surface

**No runtime test for this skill body** — prose-doctrine, not code. The automated check is skill-body lint / frontmatter validation; the grep-asserts below stand in, one count per token against the named file.

| # | token | file | expect | threshold reason |
|---|---|---|---|---|
| 1 | `Eighth dimension` | core + `shared` segment | ≥2 | core alone false-passes (table self-citation) |
| 1 | `trampoline: true` | core + `shared` segment | ≥2 | DEC-4 signal, same hazard |
| 2 | `plan⇄spike` | core + `shared` segment | ≥2 | same hazard |
| 2 | `plan⇄spike` | `skills/spike/SKILL.md` | ≥1 | greppable from both sides |
| 3 | `coordinator:plan` | `skills/spike/SKILL.md` | ≥1 | spike's `viable` exit route |
| 3 | `coordinator:shape` | `skills/spike/SKILL.md` | ≥1 | spike's `not-viable` exit route |
| 4 | `"viable"` | `schemas/spike-result.schema.json` | ≥1 | verdict enum is schema-backed, not prose |
| 4 | `"not-viable"` | `schemas/spike-result.schema.json` | ≥1 | other arm of that enum |
| 5 | `plan⇄sizing` | core + `plan`-route + `shared` segments | ≥3 | same hazard, split across segments |
| 6 | `plan requires a sizing-object and trampolines back without one` | this file | ≥2 | 1 means only the self-reference survives, gate is gone |
