---
name: adr-discovery
description: "Proactively identify when a design choice or codebase change requires documenting an Architectural Decision Record (ADR) based on Architecturally Significant Requirements (ASRs). Trigger this skill when inspecting system design documents, code changes, or PRs to check if an ADR should be created or updated. Keywords: ASR, architectural significance, decision trigger, architectural impact."
---

# ADR Discovery - Identifying Architectural Significance

This skill helps the agent and team determine when a technical decision rises to the level of an Architectural Decision (AD) and requires formal documentation in an Architectural Decision Record (ADR).

## Progressive Disclosure & External Resources

- **External Resources**: This is a self-contained skill. No external runtime scripts are required. Keep all rules and schemas within the prompt context.
- **Reference**: For more details, refer to the AD practices homepage at [adr.github.io/ad-practices/](https://adr.github.io/ad-practices/).

## Freedom Calibration & Constraints

- **Constraint Level: Medium**
  - **High Rigidity**: Identifying ASRs must strictly follow the standard categorization (e.g., Quality Attributes, Constraints, Technical Debt). Deciding "not to create an ADR" for changes affecting high-risk components must be explicitly justified.
  - **High Freedom**: The exact scoring and evaluation of architectural impact can be tailored to the specific project size and tech stack.

## Decision Tree: Choosing the Right Approach

```
Design/Code Change Proposal
 ├─ Modifies a Core Quality Attribute (Performance, Security, Reliability) → [ASR Triggered: Run ADR Evaluation]
 ├─ Introduces a New Core Library, Framework, or External Service → [High Impact: Require ADR]
 ├─ Defines/Alters APIs, Protocols, or Data Schema Contracts → [High Impact: Require ADR]
 └─ Local Refactoring or Bug Fix within existing architecture → [Low Impact: Defer/No ADR Needed]
```

## Professional Mindset & Design Principles

1. **Focus on the "Why"**: Code shows *what* was built. Git history shows *when*. An ADR must capture *why* (the architectural rationale) and the trade-offs considered.
2. **ASR-Driven Decision Making**: Decisions are not made in a vacuum; they must address one or more Architecturally Significant Requirements (ASRs).
3. **Immutability and Traceability**: Once approved, decisions are immutable records. Future changes supersede them; they do not edit them.

---

## Step-by-Step Execution Procedure

### Step 1: Analyze the Decision Input

- Inspect the design proposal, issue description, or git diff.
- Identify the core technology, pattern, or dependency being introduced, modified, or retired.

### Step 2: Evaluate Against Architectural Significance Indicators (ASRs)

Check if the decision impacts any of the following criteria:

- **Quality Attributes (Non-Functional Requirements)**: Does it change the system's performance, scalability, security, cost, or maintainability profile?
- **Constraints**: Does it introduce new organizational constraints, compliance requirements, or language/framework limitations?
- **Scope & Boundaries**: Does it alter how components communicate, change the network topology, or define API/data models exposed to external systems?
- **Reversibility Cost**: How expensive, complex, or time-consuming would it be to undo this decision in 6 months? (If high, an ADR is required).

### Step 3: Recommend Action and Next Steps

- If **Architecturally Significant**: Recommend drafting a new ADR using the `adr-authoring` skill.
- If **Superseding**: Identify the existing ADR that is being replaced and note it for the `adr-lifecycle-management` skill.
- If **Not Significant**: Document the rationale briefly in the PR description or issue comments without creating a full ADR.
- Trigger the local memory capture using the standardized capture script.

---

## Critical Anti-Patterns (NEVER List)

| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** ignore silent architecture creep | Letting minor changes pile up and change system topology without any ADR. | Run this evaluation on any design proposal or PR touching core APIs or infrastructure. |
| **NEVER** write ADRs for simple code style | Creating ADRs for trivial formatting, variable naming, or micro-optimizations. | Limit ADRs to decisions with long-term, high-reversibility costs. |
| **NEVER** assume everyone knows "why" | Omitting an ADR because the current team is aligned verbally. | Write the record for the future team members and external stakeholders. |

---

## Common Error Scenarios & Fallbacks

### Scenario 1: Ambiguity in Architectural Impact

- **Root Cause**: The change is complex or requirements are vague, making it hard to judge reversibility cost.
- **Fallback**:
  1. Trigger an interactive `/grill-me` session to clarify constraints and options.
  2. Perform a lightweight risk analysis (impact vs. likelihood of failure).
  3. Default to creating a lightweight ADR (e.g., MADR format) if the team remains undecided.


