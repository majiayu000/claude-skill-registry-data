---
name: cdev-planner
description: Use when planning work inside a single CDev-conditioned repository — turning an objective into batches in the local SPRINTS.md with observable acceptance, or sweeping the repo for gaps (verification debt, stale blocks, coverage/parity holes, plan↔git divergence, contradictory docs) and proposing the next sprints. Also when the user invokes /cdev-planner or asks "plan this repo", "what's next here", "qué falta por hacer".
---

# CDev Planner

Planning brain for **one** conditioned repository. **Never implements code.** The single-repo
counterpart of `cdev-monorepo-planner`: same two modes, scoped to this repo's own plan. Without
a clear argument, run both: gap analysis first, then materialize what is approved.

Requires a conditioned repo (`docs/develop/` with `SPRINTS.md`, `AGENT_PROGRESS.md`, protocol,
clarity map). Not conditioned → propose the right bootstrap skill and stop; do not improvise a plan.

## Mode 1 — Materialize an objective (objective → executable batches)

1. **Read the repo state first**: repo guide → local protocol → `SPRINTS.md` → last
   `AGENT_PROGRESS.md` entries → `git status` and recent commits. If plan and git disagree,
   flag and reconcile before planning on top — a plan built over a drifted state is poisoned.
2. **Locate the objective in the clarity map** (`PRODUCT.md`):
   - **DEFINED** → plan it fully;
   - **PARTIAL** → plan the clear part; with a human present the unclear part becomes
     questions (§ Closing open decisions); every assumption still made is recorded, dated, in
     `DECISIONS.md`;
   - **ABSENT** → do not plan it. Write the open question instead. Inventing an ABSENT area
     is forbidden.
3. **Place work respecting the local order**:
   - an existing batch already covers it → **adopt** it, don't duplicate;
   - fits the ACTIVE sprint's objective → append batches at the end of that sprint;
   - belongs to a later phase → next `PENDING` sprint, or a new sprint drafted as `PROPOSAL`
     (a human ratifies; the planner never activates it). Never a second ACTIVE sprint,
     never renumber.
4. **Close the batch's open decisions before writing it** — § Closing open decisions. This
   step and the next run per batch, interleaved: ask → write → next batch.
5. **Write each batch executable as-is**: acceptance criteria observable and written before the
   work (not "endpoint implemented" but "this call returns this shape and this check proves
   it"); verification per the repo's real protocol; `depends_on` between batches where order
   matters; sized to be finishable and provable in one sitting.
6. **Declare gates**: any step whose blast radius exceeds the working branch (schema on a
   shared database, deploy, publishing) is marked prepare-don't-execute, naming the human
   decision required.
7. **Promote to `READY`** only when the batch's open decisions are closed, acceptance is
   observable, dependencies exist, and the plan still satisfies the invariants (exactly one
   ACTIVE sprint, no unresolved placeholders).
8. **Record planning decisions**, dated, in `DECISIONS.md`.

## Closing open decisions (before each batch is written)

What operators call "closing gaps": the decisions a batch would otherwise fix on its own. Not
Mode 2's gap analysis, which looks for missing work in the repo. **This section is the rule's
single home**; `cdev-monorepo-planner` applies it by reference.

**With a human present:**

1. Show the batch grouping first — titles, one line each — before any batch is written.
2. Then batch by batch, in plan order: put that batch's open decisions as questions, each with
   two or more suggested answers and one marked recommended. Record the answers, **write that
   batch**, move to the next. Ask → write → ask → write.
3. A batch that raises no open decision asks nothing.
4. What counts as an open decision is your judgment — there is no written threshold. Hold it
   conservatively: assume almost nothing, and never ask what the repository's evidence already
   settles. The permissions and tool connections a batch will need are open decisions too.
   What you judge not worth a question is still recorded as a dated assumption.
5. A question closes something undecided. The human's prompt is the statement of intent:
   interpret it; never hand it back for confirmation.
6. Decisions that belong to the whole sprint may be asked once, up front. They never replace
   the per-batch rounds.
7. A free-text answer is an answer. Answers go to `DECISIONS.md`, dated, per batch.

Never one questionnaire covering every batch. Never a question about a batch already written.

**With no human present** (invoked from an unattended loop): a batch with open decisions is
written `BLOCKED`, each one naming the minimum human decision and your suggested answer. Never
`READY`; never carried forward on the recommendation.

*Host binding:* where the host offers a structured question tool, use it. Otherwise, numbered
questions with lettered options, one batch per message.

## Mode 2 — Gap analysis (find what to do, and what is silently missing)

Sweep the repo and produce actionable candidates, each with evidence:

1. **Verification debt, aggregated**: batches `DONE` with checks `not-run`, runtime evidence
   missing where the protocol demands it, blocked verifications never re-run. Sum it and show
   the total — individually honest entries add up to a plan that reads finished over work
   never fully verified.
2. **Stale state**: `BLOCKED` batches whose blocker may have cleared, `IN_PROGRESS` with no
   matching working tree, plan↔git divergence, registry-style claims no longer true.
3. **Coverage and parity**: untested areas the protocol gates on, parity gaps between targets
   (multi-target repos), marked debt (debt sections, deferred TODOs).
4. **Documentation consistency**: operational docs that contradict each other — the loop trusts
   instructions, so a contradiction is an incident waiting; clarity map stale against specs
   that have since arrived; leftover placeholders.
5. **Plan health**: no ACTIVE sprint (plan exhausted — natural next-sprint candidate),
   acceptance criteria not observable, blocked units missing their named human decision.

Output: table candidate → evidence (file/line/commit) → proposal (draft batch or open
question). Approved candidates enter `SPRINTS.md` via Mode 1 as `PROPOSAL`/`PENDING`.
**Findings not derivable from evidence are not invented** — open question in `DECISIONS.md`.

## Rules

- The repo is the source of truth; the planner reads, references and proposes — it never marks
  work `DONE`, never implements, never activates a `PROPOSAL` sprint.
- Self-directed planning stays inside DEFINED/PARTIAL areas of the clarity map.
- Every finding cites evidence (file/line/commit), never impressions.
- Invariant violations found while planning (two ACTIVE sprints, `DONE` without evidence) are
  reported as planning bugs with a proposed correction — not silently repaired.
