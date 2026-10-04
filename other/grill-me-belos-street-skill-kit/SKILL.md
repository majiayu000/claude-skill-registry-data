---
name: grill-me
description: Iteratively grill users to clarify vague requirements via layered questioning. Use when requirements are ambiguous, incomplete, or need refinement before implementation.
license: MIT
metadata:
  author: belos-streets
  tags: [workflow, requirements, clarification, analysis]
---

# Grill Me

> Iteratively grill users to clarify vague requirements before any implementation begins.

This skill defines two modes for requirement clarification:

- **/grill-me**: Pure questioning flow — no file writes, chat-only, outputs a structured summary at the end.
- **/grill-with-docs**: Full questioning flow + automatically creates/incrementally updates a root `CONTEXT.md` file to persist business rules, terminology, and requirement boundaries.

Both modes follow the same systematic layered questioning approach covering business goals, input/output specs, edge cases, and hard constraints.

## When to Apply

Reference these guidelines when:

- Requirements are vague, incomplete, or self-contradictory
- A feature request lacks clear acceptance criteria
- Multiple interpretations of a requirement exist
- Building a feature that touches multiple systems or stakeholders
- Before writing any code to ensure shared understanding

## Modes

| Mode | Description | Reference |
|------|-------------|-----------|
| /grill-me | Pure questioning, no file writes, structured summary output | [grill-me](references/grill-me.md) |
| /grill-with-docs | Full grill + auto-create incremental CONTEXT.md persistence | [grill-with-docs](references/grill-with-docs.md) |

## Core Methodology

### Four-Layer Questioning

The questioning follows a strict layered sequence:

| Layer | Focus | Key Questions |
|-------|-------|---------------|
| 1. Business Goal | Core problem, end users, usage scenarios | What core problem? Who are the users? |
| 2. Input & Output | Data format, parameters, display/storage | What inputs/outputs? Format constraints? |
| 3. Edge & Exception | Empty data, errors, conflicts, failures | How to handle edge cases? Fallback logic? |
| 4. Hard Constraints | Tech stack, performance, security, acceptance | What are the limits? Acceptance criteria? |

### Termination Rule

- Continue layered questioning until the user explicitly states "all details are clear"
- Do NOT stop based on your own judgment of completeness
- After termination, output a structured Requirement Clarification Summary

### Self-Check Before Summary

Before presenting the Requirement Clarification Summary, verify all checklist items are resolved:

- [ ] **Business Goal answered** — core problem, target users, main scenario
- [ ] **Input/Output specified** — data format, parameters, display/storage
- [ ] **Edge cases addressed** — empty data, errors, conflicts, failures
- [ ] **Tech constraints documented** — stack, performance, security
- [ ] **Acceptance criteria defined** — verifiable, testable standards
- [ ] **Terminology aligned** — no ambiguous or inconsistent terms

If any item is unchecked, continue questioning. Do NOT proceed to summary until all are resolved.

### Hard Rules

1. Never provide code, interface design, database schema, or architecture plans during the entire grill process.
2. Do not make assumptions to fill ambiguous descriptions — keep asking.
3. Do not read or modify project files unless using /grill-with-docs mode.

## Output: Requirement Clarification Summary

After the user confirms "all details are clear" and self-check passes, output the summary using this exact template:

```markdown
## Requirement Clarification Summary

**Feature:** [feature name]

### 1. Business Goal

- **Core problem:** [what problem does this solve]
- **Target users:** [who are the end users]
- **Main scenario:** [core user operation and usage scenario]

### 2. Data Spec

- **Inputs:** [parameters, formats, constraints]
- **Outputs:** [results, display location, storage]

### 3. Edge & Exception Handling

| Scenario | Behavior |
|----------|----------|
| Empty data | [fallback] |
| Network failure | [fallback] |
| Permission denied | [fallback] |
| Concurrent conflict | [fallback] |
| Other | [additional cases] |

### 4. Constraints

- **Tech stack:** [languages, frameworks, versions]
- **Performance:** [latency, throughput, scale targets]
- **Security:** [auth, data protection, compliance]
- **Browser/Platform:** [compatibility requirements]

### 5. Acceptance Criteria

- [ ] [criterion 1 — verifiable]
- [ ] [criterion 2 — verifiable]
- [ ] [criterion 3 — verifiable]

### 6. Terminology Dictionary

| Business Term | Code Naming | Description |
|---------------|-------------|-------------|

```

## Transition Protocol

Once the summary is presented, propose the next step based on requirement maturity:

| Requirement State | Recommended Next Step |
|------------------|----------------------|
| Design exploration needed | Invoke [brainstorming](../brainstorming/SKILL.md) |
| Requirements fully clear, multi-step task | Invoke [writing-plans](../writing-plans/SKILL.md) |
| Requirements simple, single-step | Proceed directly to implementation |

**Transition message template:**

> "Requirements have been clarified and documented above. Based on the maturity of these requirements, I recommend: [next step]. Shall I proceed?"

## Quick Reference

### Key Principles

- **Question limit per round**: 3-5 questions only
- **Layers must be followed in order**: Business Goal → Input/Output → Edge/Exception → Constraints
- **Termination**: Only when user says "all details are clear"
- **No code, no design, no architecture** until grill is complete

### CONTEXT.md Structure (grill-with-docs)

The persisted document follows 7 sections:
1. Core Business Goal
2. User Roles & Core Usage Scenarios
3. Data Spec: Input / Output
4. Edge & Exception Handling Rules
5. Tech Constraints, Security & Performance Requirements
6. Feature Acceptance Criteria
7. Project Terminology Dictionary (Business Term → Unified Code Naming → Description)
