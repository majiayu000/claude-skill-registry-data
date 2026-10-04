---
name: plan-review
description: "Review product, business, and engineering decisions and plans: clarify requirements, challenge assumptions, and assess risks."
license: MIT
compatibility: "None - works on any decision context"
metadata:
  source: iuliandita/skills
  date_added: "2026-09-20"
  effort: high
  argument_hint: "<decision-or-plan>"
---

# Plan Review

Review product, business, and engineering decisions before implementation. Clarify unresolved requirements or critique a settled proposal through constructive and adversarial lenses.

1. **Clarification** turns an unresolved plan into a decision record, then stress-tests it.
2. **Settled-decision critique** challenges an existing decision or artifact without reopening choices that evidence does not invalidate.

Use both lenses by default: identify who benefits, who pays, what becomes hard to undo, and the constraint that preserves the useful upside. Honor an explicit Jekyll-only or Hyde-only request while still naming cost bearers, reversibility, and a concrete next step.

## When to use

- Clarify a feature, infrastructure, architecture, product, business, or fiction plan before building.
- Challenge a settled strategy, roadmap, pricing, platform, governance, or design decision.
- Pressure-test assumptions, failure paths, incentives, reversibility, and second-order effects.

## When NOT to use

- Review existing code for bugs, security flaws, or repository health: use the appropriate code or **repo-audit** skill.
- Create an implementation plan from scratch when the user has not offered a decision to review.
- Perform hands-on interface design: use **frontend-design**.
- Capture or prioritize a backlog: use **roadmap**.
- Turn an accepted engineering decision into executable steps: use **dev-cycle** or the repository's planning workflow.
- Format or improve a prompt: use **prompt-generator**.

## Workflow

1. **Classify:** determine whether the target is unresolved (clarification) or already settled (critique), the domain, stakeholders, reversibility, evidence, and missing context. Inspect available files and load the relevant question bank from `references/domains.md` before asking. State material assumptions.
2. **Clarify unresolved plans:** walk upstream decisions before dependent ones. Give each question a recommended answer and reason; question pacing for interactive and headless use is in Rules. Sort every unresolved item into: decision, sharp open question, not-yet-specified fog, or prerequisite.
3. **Record decisions:** write the resolved choices, reasons, options rejected, constraints, open questions, fog, prerequisites, owner/trigger, and next action using `references/decision-record.md`. A precise blocked question is open; an unformulable future concern is fog.
4. **Challenge the plan:** identify load-bearing assumptions, failure and abuse paths, incentives under pressure, cost bearers, operational/security/reputation risks, and a three-month pre-mortem. For every material risk, accept it with rationale or mitigate it; if it invalidates an upstream decision, return to Step 2 for that decision and update the record.
5. **Critique settled decisions:** load `references/jekyll.md`, `references/hyde.md`, or `references/dual-lens.md` for the selected lens; start an unqualified critique with the dual lens. Load `references/operator-patterns.md` when the decision mechanism (default, pricing, data, governance, dependency, workflow, culture) matches an operator pattern or the user asks for a founder, operator, or tech-leader comparison. Do not relitigate settled choices without evidence; record the evidence, changed condition, owner, and decision that must reopen. Follow with constructive constraints that keep user benefit, reliability, trust, and changeability.
6. **Recommend:** state the path, tradeoff, guardrail, next action, and review trigger. Use the smallest output that makes the decision actionable.

## AI Self-Check

- [ ] The mode matches the target: unresolved plans clarify; settled artifacts critique.
- [ ] Facts, assumptions, risks, and opinions are distinct; material evidence was inspected before asking.
- [ ] Upstream choices are resolved before dependent choices, and every deferral has the right bucket.
- [ ] Risks name cost bearers, incentives, reversibility, and a mitigation, acceptance rationale, or reopening trigger.
- [ ] The constructive recommendation preserves useful upside and has a measurable review trigger.
- [ ] Cross-cutting hygiene is applied from `references/agent-hygiene.md`.

## References

- `references/domains.md` - domain question banks.
- `references/decision-record.md` - durable clarification artifact.
- `references/dual-lens.md` - user-benefit, incentives, and adversarial critique.
- `references/jekyll.md` and `references/hyde.md` - constructive and adversarial lenses for Step 5; `references/operator-patterns.md` - on-demand operator patterns (see Step 5).
- `references/output-contract.md` - required reporting format.

## Output Contract

Use `references/output-contract.md`.

- **Skill name:** PLAN-REVIEW
- **Deliverable:** clarification: `docs/local/deliverables/plan-review/<YYYY-MM-DD>-<slug>.md`; artifact critique: the same path with the full audit contract.
- **Mode:** conditional. Advice may remain conversational; clarification always writes a decision record; review of an existing artifact writes a full deliverable.
- **Priority:** P0-P3 and info for artifact critiques. Decision records use risk priority without inventing a defect scale.

## Rules

- No persona theater. The Jekyll/Hyde lenses are concrete user-benefit, incentive, abuse-path, and operating-constraint checks.
- Strong strategy is not automatically a dark pattern. Name the mechanism, affected party, and condition that changes the recommendation.
- Resolve terms before building decisions on them. Do not hide unanswered work as an open question when it is actually fog or a prerequisite.
- In interactive clarification, do not batch questions. In headless use, state assumptions and emit the full tree in one pass.
- Do not use a risk list as a substitute for a final decision. End with a recommendation or a clear decision frame.
