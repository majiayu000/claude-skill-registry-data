---
name: skill-tuning-loop
description: >
  Empirically test whether a lacquer skill needs an edit by mining real
  session transcripts for friction, proposing a bounded fix, and validating
  it against held-out cases before it ships. Use when a skill in
  core/skills/ or profiles/*/skills/ keeps getting corrected in practice, when
  triaging a scheduled tuning-pass PR, or when skill-authoring-standard's
  manual rubric isn't enough to tell whether a proposed edit actually helps.
  Distinct from skill-authoring-standard (a static prose rubric checked by a
  human) — this is an empirical, evidence-gated loop checked by rollouts.
---

# Skill Tuning Loop

A skill earning its place in the lacquer (per `skill-authoring-standard`) is
a judgment call today. This loop adds a second, empirical bar: does a
proposed edit measurably reduce the friction real sessions hit, without
regressing what already works? Run it via the `skill-tuning-loop` Workflow —
never edit a skill's behavior-affecting content based on mined evidence
without going through the validation gate below.

## When to run this

- A skill keeps needing the same correction across unrelated sessions —
  that's a signal worth mining, not a one-off to shrug off.
- Before accepting an automation-proposed edit (see the continuous-tuning
  design this skill's workflow implements) — the gate is what makes an
  unattended proposal safe to merge.
- Never on every session, and never on a single session's evidence — one
  grumpy correction is noise, not a pattern. Require independent evidence
  from multiple sessions before proposing a change.

## The loop (implemented in the `skill-tuning-loop` Workflow)

1. **Mine.** Search recorded sessions (via the agentsview MCP tools) for
   invocations of the target skill plus friction phrases ("no that's wrong",
   "actually", "don't do that"). Pull the surrounding messages for anything
   that looks skill-relevant.
2. **Reflect.** Have an agent read the current `SKILL.md` against that
   evidence and name concrete, recurring patterns — what the skill says (or
   omits) and what went wrong because of it. Require ≥2-3 independent
   sessions per pattern; thin evidence gets flagged, not acted on.
3. **Propose.** Generate a *bounded* edit — add/replace the few lines
   implicated by the evidence, not a rewrite — that still satisfies
   `skill-authoring-standard` (trigger-oriented description, instruction over
   exposition, no padding).
4. **Validate.** Run the same small held-out task set (`references/eval-cases.md`
   if the skill has one, else 3 representative tasks derived from its
   description) against the old and new skill text in parallel, judged by an
   independent agent running on a stronger model than the one that drafted
   the proposal — the same posture as `advisor-checkpoint`, spending the
   expensive model at the one load-bearing moment (the ACCEPT/REJECT
   verdict) rather than throughout. Accept only if the new version doesn't regress any
   case and strictly improves at least one. A good eval case is a task plus
   an explicit, checkable success criterion — not "handles it well," but the
   specific behavior that counts as a pass — and the set should include at
   least one edge or ambiguous case, not just the obvious path. If you're
   authoring `references/eval-cases.md` by hand for a skill, hold it to that
   same bar.
5. **Report, don't merge.** A REJECT verdict ends the loop — log the
   rejected proposal and reasoning so a future pass doesn't re-propose it
   without new evidence. An ACCEPT verdict produces a diff and its evidence
   (session excerpts, before/after eval scores) for a PR — a human merges it.
   This loop never commits, pushes, or merges on its own.

## Guardrails

- **Bounded edits only.** A diff that touches more than the lines implicated
  by the evidence is a rewrite wearing a tuning-loop's clothes — reject it
  and re-propose narrower.
- **Validation gate is non-negotiable.** Mined evidence proposes; held-out
  eval disposes. Skipping the gate turns this into "one user's bad session
  rewrites a shared skill," which is worse than not running the loop at all.
- **Human merges.** Same posture as this repo's git-safety rules generally —
  an accepted proposal is a reviewable PR with its evidence attached, never
  an auto-applied change.
- **A "this tool/skill doesn't exist" finding is never trustworthy on its
  own.** Reflect and Propose can only grep this repo's own committed files —
  they have no visibility into Claude Code's system-level tools
  (`ScheduleWakeup`, `EnterPlanMode`, `CronCreate`, `TaskCreate`, ...) or
  plugin-provided skills installed outside `core/skills/`/`profiles/*/skills/`
  (`flowdeck`, `swift-concurrency-pro`, ...). A real run proposed "fixes" for
  all three of those, replacing a correct reference with worse text because
  the tool/skill was real but invisible to a repo-only grep. The workflow
  script forbids finding, proposing, or accepting an edit based on such a
  claim; still spot-check any accepted proposal whose rationale leans on a
  tool or skill "not existing" before applying it — this class of mistake
  reads as confident and well-verified right up until it isn't.
