---
name: responsible-autonomy
description: Use to govern how deployed AI autonomy matures over time, at the Learn-phase cycle review and as a standing Responsible AI Posture. Runs a short interview to set the posture (the current autonomy ceiling and the next cycle's proposed step up), write if-then maturity gates that tie each step up to pre-committed evidence (the eval pass^k bar), choose an independent verifier scaled to the stakes (the builder is never the verifier) and name a separate authorizer, set deception-aware held-out checks, and define trip-wires and a reversible brake that can lower autonomy, not only raise it, then produces a one-page Responsible Autonomy Sheet. Use when the user asks about responsible AI, an AI risk or maturity posture, maturing or rolling out agent autonomy, an ARB or review-board gate, independent verification, or who signs off before production, or runs /goal-govern. This governs how autonomy matures across cycles; setting a single step's autonomy level at a point in time is agency-design instead.
---

# Responsible Autonomy

The responsible-AI layer of GOAL, and the missing brake on the Hill Climbing Machine. `agency-design` sets how far an agent acts at each step; this skill governs **how that autonomy matures across cycles: how fast the ceiling is allowed to rise, and what forces it back down**. Its premise is GOAL's: **AI serves humanity, with the human in the lead.** Autonomy matures only as trust is demonstrated, and the organization must always be able to slow it or roll it back. The output is a one-page **Responsible Autonomy Sheet**, holding a standing **Responsible AI Posture**, that rides alongside the Agency Map.

The enterprise lever is the rate at which a company grants autonomy and reach to the agents it deploys, not the rate it trains models. Two commitments define the skill: **govern the maturity, do not build the controls** (GOAL plans the responsible-AI posture; the org, its ARB, or Specify and Build implement the gates, monitors, and kill switch), and **bidirectional by design** (slowing and lowering autonomy is a first-class move, not a failure).

## What to do

Interview the user briefly (one step at a time is fine), then fill `references/responsible-autonomy-template.md`, save it as `responsible-autonomy.md` in the working project, and show it to the user.

1. **Branch, then set or revisit the Responsible AI Posture.** Are we authoring the standing posture for the first time, or running the per-cycle Learn review of one that exists? Then state the current autonomy ceiling, the next cycle's proposed step up (Level and reach), who owns the posture (often Enterprise Architecture), the portfolio maturity budget for this cycle, and the aggregate blast radius of agents that share a model, tool, credential, or data store (correlated agents fail together).
2. **Map to existing governance, and reuse it.** Name the org's ARB, risk committee, model-risk policy, and three-lines-of-defense structure, and plug into them. Do not invent a parallel compliance stack.
3. **Write the maturity gates.** For each planned step up, pull the real step from the Agency Map and the real pass^k bar, trial count, and held-out set from the Eval Plan. Make each gate multi-axis (reliability, security, data-privacy and PII, blast-radius) with a maximum tolerable failure severity, pre-register it before the cycle, and expire it on any provider model-version change. No placeholder thresholds. Raise the default tier if the domain is regulated or high-risk.
4. **Choose the verifier, and name the authorizer.** Pick the independence tier by stakes (fresh pod, ARB, second-line risk, internal audit, external), enforce that the builder is not the verifier and does not hold the held-out set, and confirm findings are recordable and uneditable. Then name, separately, the accountable owner who accepts the residual risk and authorizes the step up. See `references/verification-ladder.md`.
5. **Set deception-aware checks.** Name the held-out or adversarial check for any step up where the system could optimize to the test, keep the held-out set in the verifier's custody, and name the production monitoring for eval-versus-production divergence. The reliability mechanism lives in `eval-driven-development`.
6. **Define the trip-wires, the brake, the controls, and the audit substrate.** Name (do not build) the conditions that pause or lower autonomy, who can pull the brake and the kill switch, the circuit breakers, the standing blast-radius limits, the canary or shadow stage, the incident-and-root-cause path (no step up until the cause is closed), the change records, the segregation of duties, and where the tamper-evident audit lives and who reads it.
7. **Hand off.** State what the org must implement to enforce the posture (the gates, the monitors, the kill switch), pointing at existing governance tooling or the ARB process, then Specify and Build.

## Self-check before you finish

Check the Responsible Autonomy Sheet against this rubric, and fix anything that fails:

- The sheet lands this cycle's decision (step up approved, held, or conditional), with the condition and a revisit date.
- The Responsible AI Posture names the ceiling, the next step up (Level and reach), and its owner, and states a portfolio maturity budget and the aggregate blast radius of correlated agents.
- Every planned step up has a pre-registered if-then maturity gate that pulls real steps from the Agency Map and real numbers from the Eval Plan (no placeholder thresholds) and re-validates on any model-version change.
- Each step up is gated on more than reliability: security, data-privacy, and blast-radius evidence, and a maximum tolerable failure severity, with a statistically sufficient trial count.
- Every step up names the verifier's independence tier scaled to its stakes (mapped to the three lines of defense), and the builder is not the verifier and does not hold the held-out set.
- The sheet names, separately from the verifier, the accountable owner who accepts the residual risk and authorizes the step up; neither is the builder.
- Standing blast-radius limits are set, and the step up reaches full scale through a canary or shadow stage, not a single jump.
- A kill switch exists alongside the reversible brake, its owner is named, and brake and kill authority are independent of the delivery team.
- A fired trip-wire opens an incident with a root-cause review, and no step up occurs until the cause is closed.
- The audit substrate is tamper-evident, append-only, retained, readable by the verifier and internal audit without the builder, and reconstructs any single action end to end.
- If the domain is regulated or high-risk, the default verification tier rises, compliance review is not deferred, and the agent is in the model and agent inventory.
- The sheet reuses the org's existing governance rather than inventing a parallel stack, and it matures autonomy without freezing the machine (the brake can lower autonomy, not only pause it).

## Phase state (for the GOAL status-line HUD)

This skill runs at two altitudes. The **standing** Responsible AI Posture is authored once and does not change the phase. When you run the **per-cycle** review, this is the Learn phase: if the user runs the HUD (`docs/statusline.md`), set `.goal/state.json` in the working project to `{ "phase": "Learn", "project": "<the project folder name>" }`.

## Hand off

The Responsible Autonomy Sheet rides alongside the Agency Map and governs how fast its Levels are allowed to rise. `agency-design` names what earns a step's climb; this skill turns that into a gate, adds the independent verifier and the downward brake, and hands the enforcement (gates, monitors, kill switch) to the org's governance tooling, the ARB, or Specify and Build. `eval-driven-development` produces the reliability evidence the gates check. `forward-deployed-pod` is the lightweight verifier tier, advisory only.

See `references/verification-ladder.md` for the verifier tiers and the standard controls, and `references/examples/` for two worked sheets: `enterprise-comms-workflow.md` (ARB and second-line gated) and `single-team-coding-agent.md` (a lighter, fresh-pod-verified step up).
