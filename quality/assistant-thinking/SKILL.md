---
name: assistant-thinking
description: "Reason through architecture decisions and complex trade-offs. Use for explicit stress tests, debate, first principles, or hypotheses."
---

# Thinking Tools

## Contracts

| Contract | File | Purpose |
|---|---|---|
| **Input** | `contracts/input.yaml` | Problem, tool selection, stakes level |
| **Output** | `contracts/output.yaml` | Key insights, recommendation, confidence, dissenting view |
| **Phase Gates** | `contracts/phase-gates.yaml` | Tool selection → Analysis → Synthesis gates |

**Rules:**
- Analysis must follow the loaded tool's methodology — not ad-hoc thinking
- Dissenting views must be considered, not suppressed
- Confidence level must reflect actual analysis depth, not default to HIGH

On-demand structured reasoning. Use when you or the user needs deeper analysis — not on every task.

## Goal

Apply the smallest suitable reasoning method to clarify a decision, stress-test an assumption, compare trade-offs, or debug uncertainty without turning simple execution into ceremony.

Reasoning must be company-safe and evidence-aware: prefer local/repo evidence, do not require third-party tools, do not expose proprietary code or secrets, and separate facts from assumptions.

## Success Criteria

- The selected thinking tool matches the problem and stakes level.
- Analysis follows the tool method instead of free-form rumination.
- A dissenting view or counterpoint is included when confidence matters.
- The recommendation includes confidence and the gaps that limit it.
- For debugging/investigation, at least three distinct falsifiable hypotheses are considered before pursuing one.
- For planning/architecture, trade-offs are tied to concrete constraints, source-backed facts, explicit ownership/lifecycle boundaries, design-pressure checks (control/early exit, ownership/disposal, resource envelope, extension registration, representative path), and falsifiable quality scenarios rather than generic preferences.

## Constraints

Migration note: assistant-thinking contracts are v6. v5 consumers must replace
the scalar Deep Think feature-preparation evidence inputs with up to 32 exact
`feature_preparation_evidence_bindings` entries `{evidence_ref, item_id,
claim_or_question}`. Every validated candidate must match exactly one input
entry; missing, stale, mismatched, duplicate, or extra bindings remain
candidate-only. v4 consumers must bind every validated Deep Think promotion to
the exact canonical feature-preparation evidence ref and item id; missing,
stale, mismatched, or unresolved evidence remains candidate-only. v3 consumers must retain
Deep Think output as candidate concerns or criteria until a canonical
feature-preparation evidence row validates promotion in existing-system feature
preparation. v2 consumers must add the
typed independent challenge evidence for `review_intensive` Architecture
Decision Pack updates: `challenge_ref`, `dissent_or_validation`, `resolution`,
and `selected_design_impact`. Applicable direct-user,
`AGENTS.md`, and active-skill instructions now trigger delegated Perspectives
and high-stakes Stress Test work; `subagent_trigger_scope` records provenance
and covered work without a second permission question.

- Do not invoke deep reasoning for simple execution tasks.
- Do not use this skill for broad brainstorming; route option generation to `assistant-ideate`.
- Ask every material question that would change the selected method or recommendation. Group questions by decision topic, state why and risk if guessed, and give a safe default where one exists; do not suppress a material question to satisfy a numeric limit.
- For `Perspectives` and high-stakes `Stress Test`, resolve `subagent_policy_state`, `subagent_execution_mode`, `subagent_trigger_scope`, and conditional `policy_blocking_source` before spawning. A direct user request or applicable `AGENTS.md` or active-skill instruction triggers `delegation_triggered`: infer the covered roles and dispatch without a separate permission question. Sequential fallback requires explicit user opt-out, a real unavailability failure or supported configuration proof, or policy-disallowed evidence; `policy_disallowed` requires an exact blocking rule with no applicable trigger exception. Delegation never bypasses parent sandbox, action/tool approvals, external-write, install, destructive-operation, or secrets safeguards.
- Do not invent evidence. Mark unverified claims as assumptions and identify how to validate them.
- Do not paste secrets, proprietary source, customer data, or sensitive logs into external tools as part of reasoning.

## Available Tools

| Tool | File | When to use |
|---|---|---|
| **Clarify** | `clarify.md` | Stuck or challenging assumptions. Classifies hard vs soft constraints. |
| **Perspectives** | `perspectives.md` | Challenge a genuinely contested architecture/design decision; use only the perspectives and rounds that change the decision. |
| **Stress Test** | `stress-test.md` | Validating important decisions. Steelman + counter-argument. |
| **Deep Think** | `deep-think.md` | Candidate concerns and criteria. Multiple analytical lenses (8 lenses). |
| **Hypothesize** | `hypothesize.md` | Debugging, investigation. Goal-first + hypothesis plurality (3+ hypotheses). |
| **Creative** | `creative.md` | Naming, breakthrough ideas. Low-probability sampling for diverse output. |

## Usage

Read the relevant tool file when the situation calls for it. These are tools, not mandatory phases.

**When to reach for a thinking tool:**
- Decision feels uncertain or high-stakes -> Stress Test or Perspectives
- Stuck on a problem -> Clarify or Hypothesize
- Need to explore options broadly -> Creative or Deep Think
- Architecture/design choice with genuinely viable alternatives or conflicting quality drivers -> Perspectives; otherwise use the workflow Architecture Decision Pack directly.
- Debugging with multiple possible causes -> Hypothesize

**When NOT to use:**
- Simple, clear tasks with obvious solutions
- When the user just wants you to execute, not deliberate

## Method Selection Rules

Pick the smallest method that changes the outcome:
- **Clarify**: assumptions/constraints are tangled, but the main goal is visible.
- **Perspectives**: several architecture/design options are viable, quality drivers conflict, or an Architecture Decision Pack needs an independent challenge.
- **Stress Test**: a proposal is likely to be accepted unless actively challenged.
- **Deep Think**: candidate concerns or criteria are needed because requirements are incomplete or stakeholder/failure modes are hidden. In existing-system feature preparation, it does not promote them to requirements or Product questions without workflow evidence.
- **Hypothesize**: root cause is unknown; generate 3+ testable hypotheses before testing.
- **Creative**: naming or unusual options are needed after ordinary choices feel stale.

Stakes set depth:
- **low**: one pass, concise synthesis.
- **medium**: apply the selected method fully, include dissent.
- **high**: include evidence, counter-argument, validation plan, and explicit uncertainty.

## Debugging / Hypothesis Discipline

When using `hypothesize`:
1. Define the symptom, success indicator, and anti-goals.
2. Gather observations from local evidence before guessing.
3. List at least three distinct hypotheses.
4. For each hypothesis, state the cheapest test and what would disprove it.
5. Test the highest-signal/lowest-cost hypothesis first.
6. Report confirmed, refuted, or inconclusive — do not collapse uncertainty into confidence.

## Decision Output Shape

For architecture/planning decisions, include:
- options considered
- criteria used to compare them
- recommendation
- dissenting view
- validation step or rollback trigger
- when a workflow Architecture Decision Pack applies: freshness status, boundary/type-ledger implications, and a measurable quality scenario or an explicit unknown

## Output

Return:
- **Result** - concise synthesis of the selected thinking tool's outcome.
- **Key insights** - the few observations that materially change the decision.
- **Recommendation** - proposed next step with confidence level.
- **Dissenting view** - strongest counterpoint, risk, or alternative interpretation.
- **Gaps** - assumptions, unknowns, or questions that limit confidence.
- **Evidence / observations** - facts, observations, test results, or user constraints used in the reasoning.
- **Decision artifacts** - for decision outputs: options considered, criteria, selected option, and validation/rollback step.
- **Architecture Pack update** - when supplied: the Pack reference, whether it remains fresh, questions or claims it invalidates, semantic type/primitive-exception findings, and quality-scenario verification implications.
- **Candidate concerns or criteria** - for Deep Think in existing-system feature preparation: candidate-only observations plus their evidence-promotion status and, only when validated, one exact per-candidate `{evidence_ref, item_id, claim_or_question}` binding from the canonical input set.
- **Independent challenge evidence** - for `review_intensive` Pack updates: challenge reference, dissent or validation, resolution, and effect on the selected design.
- **Delegation path** - for Perspectives and Stress Test: delegated vs sequential fallback, policy state, execution mode, and trigger scope.
- **Debug artifacts** - for debugging outputs: hypotheses, tests, disconfirming evidence, and conclusion.

## Stop Rules

- Stop and ask when the decision frame or stakes are unclear enough to change the method.
- Stop after synthesis unless the user asks to implement the recommendation.
- If the chosen method cannot be applied with available context, report the gap instead of inventing analysis.
