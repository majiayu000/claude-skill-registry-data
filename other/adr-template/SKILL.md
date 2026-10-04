---
name: adr-template
enabled: true
description: |
  Use when performing adr template — structures an Architecture Decision Record
  (ADR) to capture the context, decision, and consequences of significant
  architectural choices. This template ensures decisions are documented with
  sufficient detail for future teams to understand not just what was decided,
  but why.
required_connections:
  - prefix: wiki
    label: "Documentation Platform"
config_fields:
  - key: adr_number
    label: "ADR Number"
    required: true
    placeholder: "e.g., ADR-042"
  - key: title
    label: "Decision Title"
    required: true
    placeholder: "e.g., Use PostgreSQL for user data storage"
  - key: deciders
    label: "Decision Makers"
    required: true
    placeholder: "e.g., Backend team leads"
features:
  - ADR
  - DOCUMENTATION
  - ARCHITECTURE
---

# Architecture Decision Record

## Phase 1: Context

Define the situation that motivates this decision.

1. - [ ] Describe the technical or business context
2. - [ ] Identify the forces at play (technical, political, organizational)
3. - [ ] List any constraints or assumptions
4. - [ ] Reference related ADRs or design documents
5. - [ ] State the urgency and timeline for the decision

**Status:** Proposed / Accepted / Deprecated / Superseded

**Date:** ___

## Phase 2: Options Analysis

Enumerate and evaluate all viable options.

| Option | Description | Pros | Cons | Effort | Risk |
|--------|------------|------|------|--------|------|
| A      |            |      |      |        |      |
| B      |            |      |      |        |      |
| C      |            |      |      |        |      |

**Evaluation Criteria:**

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Performance | | | | |
| Maintainability | | | | |
| Cost | | | | |
| Team familiarity | | | | |
| Ecosystem maturity | | | | |
| Scalability | | | | |
| **Weighted Total** | | | | |

## Phase 3: Decision

- [ ] State the chosen option clearly
- [ ] Explain the primary rationale
- [ ] Note any dissenting opinions and how they were addressed
- [ ] Specify the scope and boundaries of this decision

## Phase 4: Consequences

Document the expected outcomes of this decision.

**Positive consequences:**
- [ ] List expected benefits

**Negative consequences:**
- [ ] List expected drawbacks or trade-offs

**Risks:**
- [ ] Identify risks introduced by this decision
- [ ] Define mitigation strategies for each risk

**Reversibility:**
- [ ] Is this decision easily reversible? Y/N
- [ ] What would reversal cost? (effort, time, risk)
- [ ] Under what conditions should this decision be revisited?

## Phase 5: Implementation Notes

- [ ] Key implementation steps or considerations
- [ ] Migration plan (if replacing existing approach)
- [ ] Timeline for implementation
- [ ] Success metrics to validate the decision

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "We can skip some steps for this case" | Adapt the workflow steps, don't skip them | Skipped steps are where incidents and oversights originate |
| "The user seems to already know what to do" | Complete all workflow phases with the user | The workflow catches blind spots that experience alone misses |
| "This is a minor case, full process is overkill" | Scale the process down, don't turn it off | Minor cases become major when unstructured; the process scales, not disappears |
| "I'll fill in the details later" | Complete each section before moving on | Deferred details are forgotten; real-time capture is more accurate |
| "The template output isn't necessary" | Always produce the structured output format | Structured output enables comparison, audit trails, and handoff to other teams |

## Output Format

### ADR Summary

- **ADR:** ___
- **Title:** ___
- **Status:** ___
- **Date:** ___
- **Deciders:** ___
- **Decision:** One-sentence summary of the decision

### Action Items

- [ ] Update relevant system design documents
- [ ] Communicate decision to affected teams
- [ ] Create implementation tickets
- [ ] Schedule decision review at ___ (if time-bounded)
- [ ] Update ADR index/registry
