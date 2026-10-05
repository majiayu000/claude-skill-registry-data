---
name: auto-author-goal
description: >
  Turn a plan into a model-judgeable goal doc the user binds with
  `/goal <doc-path.md>`. Use when the user says "generate a goal for this
  plan", "make a goal doc", "write a /goal for <plan>", "write a goal doc for
  this run", or wants auto to phrase an exit predicate from a plan. This skill
  AUTHORS the
  goal doc and writes it to disk; it does NOT run `/goal` — binding is the
  user's action (auto can neither arm nor clear a native goal). The doc is
  written to TRACK auto's own exit predicate so the model-judged goal and
  auto's deterministic Stop hook are as aligned as possible.
---

# auto-author-goal (the goal compiler)

A **goal doc** is a saved, model-judgeable exit predicate derived from a plan.
The user binds it with `/goal <doc-path.md>` (a file-referenced goal — the
model judges the file's whole content as the "done" condition). This skill
writes that doc; it never runs `/goal`.

## The binding model (read first)

The user runs `/goal .claude/auto/goals/<slug>.md` themselves. The model then
judges the **entire doc** as the goal at each stop attempt. Two consequences
drive how the doc is written:

1. **The doc IS the condition.** Everything in it is read as the predicate, so
   write it AS a judgeable spec — observable "done" criteria, not rationale
   prose the judge would have to interpret. The ONLY permitted aside is a single
   footer line carrying OPERATIONAL instructions (how to release the goal), never
   rationale or authoring commentary — the judge reads it but won't mistake a
   release instruction for a criterion.
2. **It's an independent, model-judged gate.** Auto's own deliberate-stop is a
   deterministic run-record read (`lib/on-stop.py`); a native `/goal` is
   model-judged and shares NO verdict with it. They can DIVERGE — a goal judged
   stricter than the run-record keeps re-prompting "Goal not yet met… continuing"
   even after auto reaches `done` (the spam class the Stop-hook fix addressed,
   now self-inflicted via the goal). We can't guarantee agreement; we write the
   doc to TRACK auto's predicate to minimize divergence. `/goal clear` is the
   escape — name it in the doc. Auto never arms or clears this goal; the user
   does. See `skills/auto/SKILL.md` §1.

## Phrasing rules — a model-judgeable exit predicate

The criteria the model judges should each be:

1. **Binary & terminal.** Describe the DONE state, not the process. "every step
   in the plan is implemented and reviewed clean" — not "work through the plan."
2. **Observable.** Verifiable from repo state or the transcript: tests pass,
   files exist, no open review findings, a command exits 0. Nothing only an
   external system knows.
3. **Agent-completable — the agent can REACH the done-state on its own.**
   Observable is not enough. If a criterion requires a manual human action the
   agent cannot perform — toggle a UI/LD flag, drag-and-drop, click through a
   flow, do something *while a job is running*, exercise a device — then the
   model-judged goal can NEVER flip to met autonomously and re-prompts "Goal not
   yet met… continuing" forever. This is the **never-met loop**: the worst case
   of the divergence above, because no amount of agent work can satisfy it. Every
   criterion must name a state the agent can both REACH and verify. Any
   human-gated / manual-QA step goes on the **out-of-scope** line, NOT in the
   criteria. If the goal is *inherently* a manual test (its whole point is a human
   exercising the UI), say so and do NOT author it as a `/goal` — it cannot be
   one; recommend a checklist or a test the agent can drive instead.
4. **Scoped to THIS plan, and INLINED.** The doc IS the condition, so write the
   specific acceptance outcomes INTO the doc — do not just cite "AE1–AE4 in
   `<plan>`" and assume the judge opens the plan (that's an unverified second-file
   read). Name the plan as provenance, but spell out the concrete done-states the
   judge can check from repo/transcript without leaving the doc.
5. **No vague adjectives unless operationalized.** Not "clean / good / done
   well" — instead "no P0/P1/P2 review findings remain" or "the suite is green."
6. **Make auto's exit predicate the PRIMARY criterion; everything else is what
   it entails.** Auto exits when *all steps are terminal AND only P3 findings
   remain*. Lead with that as the sufficient condition, and frame the plan's
   acceptance examples / tests-green as what it ENTAILS ("which means AE1–AE4 are
   satisfied and `tests/run.sh` is green"), NOT as separate bullets ANDed on top.
   Any independent gate ANDed onto the predicate can only make the goal STRICTER
   than the run-record — re-introducing the divergence (re-prompt-after-`done`) from
   the binding model above. **If you DO want a stricter gate deliberately** (e.g.
   keep the session going until tests pass, beyond auto's review-loop), that is a
   valid choice — but say so explicitly, because the extra "continuing" prompts
   are then INTENDED, not the spam failure mode.
7. **Tight.** A focused checklist, not an essay. Exclude deferred/out-of-scope
   items explicitly so the judge doesn't hold the goal open on them.

## Procedure

1. **Locate the plan.** Take the plan path from the user (or the most recent
   `docs/plans/*.md`). Read it. Pull: the requirements trace (R1…), acceptance
   examples (AE1…), scope boundaries, deferrals, and any explicit success /
   "done when" criteria.
2. **Compose the condition** per the rules above — lead with auto's exit
   predicate as the primary/sufficient criterion, then inline the concrete
   acceptance outcomes it entails (observable, spelled out, grounded in the
   plan's acceptance examples / explicit success lines). **Screen every criterion
   for agent-completability (rule 3): route any human-gated / manual-QA step to
   the out-of-scope line — it must never be a criterion.** Add the out-of-scope
   line for deferrals too, so the goal doesn't hang on them. If the only "done"
   state is a manual human test, STOP — tell the user this can't be a `/goal` and
   suggest a checklist instead.
3. **Write the goal doc** to `<repo>/.claude/auto/goals/<plan-slug>.md` using
   the template below (create `goals/` if absent). `.claude/auto/` is gitignored
   runtime state — the doc is a local artifact, not a committed file.
4. **Surface the bind command** — the path plus:
   - `/goal .claude/auto/goals/<slug>.md` ← run this to bind
   - `/goal clear` ← run this to release it

## Goal-doc template

The whole file is the condition — keep it criteria-focused.

~~~markdown
# Goal: <plan title>

Source plan: `<relative/path/to/plan.md>`

This goal is met when auto's exit predicate holds: every step in the plan is
implemented and reviewed, and only P3 review findings remain (P0/P1/P2 all
resolved). Concretely, that state means:

- <inlined acceptance outcome 1 — e.g. "a circle shape can be drawn and persists across reload">
- <inlined acceptance outcome 2 — observable, spelled out, not a citation>
- `tests/run.sh` exits 0.

Out of scope (do NOT hold this goal open on these): <deferred items, and any human-gated/manual-QA steps the agent can't perform itself, or "none">.

<!-- note: model-judged goal, independent of auto's Stop hook; release with `/goal clear`. -->
~~~

## Invariants

- **Never run `/goal`.** Author and surface only; the user binds.
- **The doc is the condition.** Write judgeable criteria, not rationale prose —
  the model reads the whole file.
- **Every criterion is agent-completable.** A criterion the agent can't reach on
  its own (manual UI action, human QA) makes a never-met loop — `/goal` re-prompts
  "continuing" forever. Human-gated steps go out-of-scope; a goal that is ONLY a
  manual test must not be authored as a `/goal` at all.
- **Ground in the plan.** Every criterion traces to a requirement / acceptance
  example / explicit success line — no invented scope. State deferrals as
  out-of-scope so the goal doesn't hang on them.
- **Track auto's predicate** to minimize (not eliminate) divergence; the goal is
  an independent model-judged gate, `/goal clear` is the escape.
