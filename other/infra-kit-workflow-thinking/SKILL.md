---
name: infra-kit.workflow.thinking
description: Apply structured thinking, bias checks, and decision frameworks to infrastructure troubleshooting, change planning, and architecture trade-offs.
---

# Infrastructure Thinking

Use this skill when the user needs higher-quality reasoning around infrastructure work: incident triage, root-cause analysis, migration choices, risk trade-offs, or when requirements are vague and the next step is unclear.

This skill is about thinking quality and decision hygiene. Pair it with domain skills (`infra-kit.domain.k8s-doctor`, `infra-kit.domain.iac`, `infra-kit.domain.helm`, `infra-kit.domain.github`, `infra-kit.workflow.audit`) once the problem is framed and the next tests/actions are explicit.

## Output Rules

- When producing an incident workspace, decision record, or structured analysis, write it to Markdown file(s) in the repo (not only chat output).
- If the content is large, split it into multiple Markdown files and keep each file narrow.
- Prefer a stable location such as `docs/infra-thinking/<topic>/`.

## Outcomes

- Turn a vague infra problem into a crisp problem statement and a short list of testable hypotheses
- Separate facts, assumptions, and unknowns so investigation stays evidence-driven
- Choose actions using reversibility and risk (safe-to-try first, high-blast-radius last)
- Produce decisions that are explainable: constraints, alternatives, trade-offs, and why now

## Where This Fits In The Flow

- Use at the start when requirements are vague, signals conflict, or you need hypotheses and tests.
- Use to turn the ticket into crisp inputs for `infra-kit.workflow` `spec.md` / `plan.md`.

## Workflow

1. Establish the context and goal.
2. Write a one-paragraph problem statement:
   - symptom
   - impact (users/SLO)
   - time window
   - scope boundary (what is explicitly out of scope)
3. Build an evidence table:
   - Facts: confirmed from logs/metrics/code/commands
   - Assumptions: believed true but not verified
   - Unknowns: blocking questions
4. Generate 3-7 hypotheses. Each hypothesis must have a proposed test and expected observation.
5. Prioritize tests by:
   - fastest-to-disprove first
   - biggest blast-radius reduction first
   - highest expected information gain first
6. Run a bias and failure-mode check before committing to a path:
   - confirmation bias: what evidence would change my mind
   - anchoring: what else could explain this
   - availability: am I over-weighting the last incident
   - pre-mortem: if this plan fails, why
7. Decide using reversibility:
   - reversible step: do now, learn, iterate
   - irreversible step: require stronger evidence, rollback plan, and explicit approval
8. Communicate as BLUF:
   - Bottom line
   - key evidence
   - next 1-3 actions
   - risks and rollback

## Hallucination Guardrails

- Do not claim a cause without evidence. If the cause is not proven, present competing hypotheses and what would falsify each.
- When referencing defaults or behavior of cloud/Kubernetes/tooling, require version context or cite an authoritative source.
- Always label assumptions as assumptions.

## Templates

### Incident Triage

- Problem: <one paragraph>
- Impact: <users/SLO/cost>
- Timeline: <what changed when>
- Facts:
- Hypotheses + tests:
- Next actions (safe-to-try first):
- If wrong, rollback:

### Decision Record (lightweight)

- Decision: <what we are choosing>
- Why now:
- Options considered:
- Constraints:
- Trade-offs:
- Risks + mitigations:
- Reversibility + rollback:

## References
