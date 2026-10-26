---
name: rite-temper
description: Temper a readied spec before planning. Use when the user says "temper this", "strategy review", "pre-mortem the spec", or asks if we are over/under-building. Not for code review or final seal.
argument-hint: "[feature-slug] [--mode expand|selective|hold-rigor|reduce-to-MVP]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md","devrites-lib/reference/orchestration-profiles.md","devrites-lib/reference/standards/agents.md","rite-temper/reference/significance.md","rite-temper/reference/scope-modes.md","rite-temper/reference/review-dimensions.md","rite-temper/reference/strategy-template.md","rite-temper/reference/anti-patterns.md"],"triggers":{"afk":["devrites-lib/reference/standards/afk-hitl.md"],"applicability":["devrites-lib/reference/standards/repository-topology.md","devrites-lib/reference/standards/data-integrity.md","devrites-lib/reference/standards/integration-reliability.md"],"documentation":["devrites-lib/reference/standards/documentation.md"],"elicitation":["devrites-lib/reference/standards/elicitation.md"],"yagni":["devrites-lib/reference/standards/patterns.md","devrites-lib/reference/standards/coding-style.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md","decision-coverage.md","strategy.md","design-brief.md"],"workspaceByRole":{"strategy-reviewer":["brief.md","spec.md","decision-coverage.md","decisions.md","strategy.md","state.md"]},"rootOnly":["devrites-lib/reference/standards/code-index.md","devrites-lib/reference/orchestration-profiles.md","devrites-lib/reference/standards/afk-hitl.md"]} -->
> Read-set manifest: `devrites-engine context <slug> --phase temper` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-temper: review scope and risk before planning

Review the readied spec for ambition, scope, pre-mortem risk and unnecessary surface. Fold accepted decisions into the canonical contract before
`/rite-define`. This step is optional for small work and skips low-stakes specs, but
`/rite-autocomplete` always invokes it. **Read the active workspace first**; if there
is no readied `spec.md`, tell the user to run `/rite-spec`. Review depth follows
[`devrites-lib/reference/orchestration-profiles.md`](../devrites-lib/reference/orchestration-profiles.md);
the required exact strategy reviewer never changes with profile.

## Rules consulted (read on demand from `.claude/skills/devrites-lib/reference/standards/`)
Pull on demand: [`patterns.md`](../devrites-lib/reference/standards/patterns.md) +
[`coding-style.md`](../devrites-lib/reference/standards/coding-style.md) (the over-engineering / YAGNI rubric, trigger `yagni`; reuse the pack's standard, don't
invent one), [`documentation.md`](../devrites-lib/reference/standards/documentation.md) (ADR-style `decisions.md` entries), [`afk-hitl.md`](../devrites-lib/reference/standards/afk-hitl.md)
(irreversible-risk list + gate ceiling), [`elicitation.md`](../devrites-lib/reference/standards/elicitation.md) (the move-set to deepen a section
that needs more than the default pre-mortem) selected by the section's risk). Load
[`repository-topology.md`](../devrites-lib/reference/standards/repository-topology.md), [`data-integrity.md`](../devrites-lib/reference/standards/data-integrity.md), or [`integration-reliability.md`](../devrites-lib/reference/standards/integration-reliability.md) only when
the spec applicability map triggers that risk family.

## Operating rules
- **Raise outcome ambition without expanding the solution unnecessarily.** Solve the
  underlying problem without adding speculative capability or abstraction.
- **Route every scope change through the Spec Drift Guard.** A scope change takes effect
  only when `spec.md` records the confirmed decision. Growth (`expand`, extra
  acceptance) needs a resolved human `questions.md` qid, so an unattended run holds it
  open. Irreversible-risk still pauses.
- **Apply maximum caution to hard-to-reverse changes.** Auth, migration, public API, and
  data-model changes always pause under the irreversible-risk list.
- **Honest verdict.** Never round "needs work" up to "ready"; record every scope call's *why*.
- **Search before asking.** Apply [`afk-hitl.md`](../devrites-lib/reference/standards/afk-hitl.md) decision ownership; only human-owned calls
  enter the interactive walk.
- **You write; the reviewer judges.** You are the single canonical writer (`strategy.md` +
  the spec edits); the reviewer agent is read-only.
- **Require spec-quality checklists for significant features.** Before hardening,
  confirm `checklists/<domain>.md` exist and pass ([`spec-checklists.md`](../rite-spec/reference/spec-checklists.md)); a
  scope expansion you fold in **adds its own** rows (new Success/Acceptance criteria get
  checklist rows too). A folded expansion with an unquantified criterion is a CRITICAL
  failure that reopens the readiness gate.

## Workflow
0. **Read `.claude/skills/devrites-lib/reference/standards/core.md`**, then
   resolve the active slug, require its `state.md`, and read the cursor directly.
   Then read the workspace: `spec.md`, `decision-coverage.md` (+ `decisions.md`,
   `assumptions.md`, `design-brief.md` if UI), `state.md`. Require `state.md` `spec_gate: passed` (legacy `Spec gate:` accepted): else
   STOP → `/rite-spec`. Require `Decision coverage: CLEAR`: else STOP →
   `/rite-clarify`. If a plan already exists, scope changes route through `/rite-plan
   repair` (record in `drift.md`), not a blind spec edit.
1. **Significance test:** [`reference/significance.md`](reference/significance.md). Low-stakes
   / shape-not-meaning work → write the exact one-line `skipped — low stakes (<trigger>)` verdict to `strategy.md`,
   set `state.md` `Phase: temper` + `Next step: /rite-define`, and recommend it. Otherwise fire the full pass below.
2. **FORWARD pass + mode selection:** [`reference/scope-modes.md`](reference/scope-modes.md).
   First, the **one-sentence-intent test**: state the whole change's intent in a single sentence.
   If you can't without an "and" that joins two unrelated outcomes, it is **two features**: the
   scope-creep signal; recommend splitting or narrowing the spec before continuing.
   Apply the same test to size: a spec whose honest decomposition would exceed the
   [feature ceiling](../rite-plan/reference/slicing.md#feature-ceiling-split-an-epic-never-override-the-budget)
   (roughly ten slices or more than ~20 acceptance criteria) is a feature sequence;
   recommend the thinnest shippable subset now and name the continuations as Non-goals.
   Then consider the 10-star outcome for the underlying problem and choose **exactly one**
   scope mode (`expand` opt-in · `selective` · `hold-rigor` · `reduce-to-MVP`) with its
   rationale and the condition that would change the choice. `$ARGUMENTS` `--mode` is a
   hint, not a command.
3. **INVERSION pass:** pre-mortem in past tense ("it shipped and failed: what went wrong"),
   each top risk carrying likelihood + mitigation + the slice it will bind to; then the **YAGNI
   ledger** (each candidate scope item gets the "imagine the later refactor" test; defer unless
   now-cost is trivial AND deferred-cost is large).
   **Interruption pre-mortem:** audit the spec forecast and assumptions for unresolved behavior,
   proof prerequisites, approvals, access, and irreversible gates. Resolve facts and reversible
   details now; retain only unavailable-pre-code or mandatory action-time checkpoints.
   Challenge each `not applicable` decision against live evidence and each applicable
   topology/data/integration row against its worst credible partial-state/recovery case.
   - **Deepen on demand.** When a scope decision, requirement, or risk needs more analysis
     than the default pre-mortem provides, choose 3-5 techniques from
     [`elicitation.md`](../devrites-lib/reference/standards/elicitation.md) whose *when-to-reach-for-it* matches that
     section's risk (irreversible decision → Red-Team/Blue-Team + Assumption Audit; sizing → Delphi;
     vague requirement → Steelman-then-Attack), offer them, and run the chosen one **on that
     section**. Record what changed, not the technique name. The default passes remain
     sufficient when no deeper analysis is needed.
4. **Score the 9 dimensions:** [`reference/review-dimensions.md`](reference/review-dimensions.md).
   Cite evidence *before* the band; **gate on the floor** (the weakest dimension, not an average).
   **Completion:** all nine dimensions have cited evidence, a band, and one explicit floor verdict.
5. **Review human-owned findings with the human; do not batch them.** `strategy.md`
   records the interactive review but does not replace it. Present each material scope decision through
   `AskUserQuestion`, one at a time, best-guess + **why**. Each material scope call ends as a
   **recorded decision**: a resolved `questions.md` qid (HITL) or a `decisions.md` ADR (AFK;
   never for `expand` or extra acceptance, which need a human-resolved qid):
   so the review leaves an auditable record outside chat. (AFK gate policy —
   [`reference/significance.md`](reference/significance.md) — autocomplete applies
   `hold-rigor`, `reduce-to-MVP` and a skip, but holds `expand` and extra acceptance for a human
   qid; irreversible-risk always pauses.)
   Apply objective clarity, mitigation, and assumption fixes directly.
6. **Write `strategy.md` + fold back:** [`reference/strategy-template.md`](reference/strategy-template.md).
   **Choose the drift path based on whether a plan exists:** *no `plan.md` yet* (the normal pre-define
   case) → update `spec.md` **through the Spec Drift Guard**. *Success metrics* (outcome-level, no AC id)
   **and** *Acceptance criteria* for each opt-in expansion / cut, **Non-goals** for every deferred item,
   *Constraints and invariants*, with top failure modes + mitigations folded into *Failure and recovery
   behavior* rows, and the *Open questions* table; *`plan.md`
   already exists* → do **not** edit `spec.md` here: write the deltas to `drift.md` and hand off
   to `/rite-plan repair`. Either way, append `decisions.md` (one ADR per scope call: context ·
   decision · why-not · what-would-change-it) and `assumptions.md` (every "we'll probably need X" →
   assumption-to-verify). (every delta carries the step-5 recorded decision; an untraceable
   fold is invalid). **Re-check the spec Readiness gate** (it fails if
   any folded scope delta lacks its decision or leaves a foreseeable human build choice).
   After any edit to `brief.md`, `spec.md`, `decisions.md`, `assumptions.md`, or
   `questions.md`, re-scan the affected coverage rows, assumption audit, residual uncertainty,
   and closed gates. `open` rows, an unowned material assumption, or an open
   blocking/escalating question routes `/rite-clarify`/HITL. Only after the
   matrix is re-closed may the phase advance.
   Set `Phase: temper`; `Next step: /rite-define` only after verification.
   Unapproved irreversible choices and unresolved growth qids set `Awaiting human`.
   Objective below-bar findings continue correction.
7. **Adversarial verification loop:** ask the exact
   [`devrites-strategy-reviewer`](../../agents/devrites-strategy-reviewer.md)
   through the native fresh-context contract in
   [`agents.md`](../devrites-lib/reference/standards/agents.md), with **only** its `--role strategy-reviewer` read-set
   (hardened spec, `strategy.md`, claim-check artifacts) + rubric, no authoring reasoning. Fold technical findings into one correction;
   exact strategy reviewer rechecks open findings and affected coverage/regressions under
   [the canonical retry contract](../devrites-lib/reference/standards/afk-hitl.md#retry-cap-no-progress-loops-and-self-resolve):
   Product/scope choices and unapproved irreversible risk remain human gates;
   technical exhaustion preserves blocker/reproduction.
   If the named agent is unavailable, stop for HITL. After an accepted edit to a
   coverage-bound input, repeat step 6's native coverage revalidation before handoff.
8. **STOP.** Report the mode, the scope deltas, and the floor verdict; recommend `/rite-define`.

> **Mid-flight discipline.** Do not replace the interactive review with `strategy.md`,
> expand implementation surface without need, grow scope outside the Drift Guard, or score
> before citing evidence. See [`reference/anti-patterns.md`](reference/anti-patterns.md).
