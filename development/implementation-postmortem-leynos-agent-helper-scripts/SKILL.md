---
name: implementation-postmortem
description: Conduct structured implementation postmortems to gather feedback on architecture conformance, library friction, and tooling effectiveness. Use when reviewing completed implementations, PRs, or development phases to surface design gaps, boundary violations, and improvement opportunities. Triggers on requests for code review feedback, implementation retrospectives, architecture audits, or library/tooling evaluations.
---

# Implementation Postmortem Agent

This skill guides structured postmortem analysis of completed implementations. The goal is adversarial review: surface friction, identify architectural drift, challenge assumptions. Implementers can handle honest critique.

## Workflow

### Phase 1: Context Gathering

Before conducting a postmortem, gather sufficient context. Never assume—ask.

#### 1.1 Obtain PR/Implementation Summary

If reviewing a PR, fetch the summary:

```bash
# Get PR details including description and changed files
gh pr view <PR_NUMBER> --json title,body,files,commits,additions,deletions

# Get the diff for detailed analysis
gh pr diff <PR_NUMBER>

# List files changed
gh pr view <PR_NUMBER> --json files --jq '.files[].path'
```

For non-PR work, request:
- The implementation scope (what was built)
- Entry points and key files
- Any design documents or ADRs referenced

#### 1.2 Establish Architecture Context

Ask these questions if the architecture is not already known:

**Structural questions:**
- What architectural pattern does this codebase follow? (hexagonal/ports-adapters, MVC, layered, event-driven, actor-based, codec pipeline, etc.)
- What are the primary module/crate boundaries?
- What invariants must the architecture preserve?

**Implementation questions:**
- What in-house libraries were used? What are they meant to do?
- What tooling was used during development? (test frameworks, code analysis, documentation tools)
- Were there design documents or specifications? Where do they live?

**Scope questions:**
- What was the goal of this implementation phase?
- What constraints or deadlines applied?
- Were any shortcuts intentionally taken (and documented)?

### Phase 2: Select Assessment Framework

Based on the architecture, load the appropriate reference template:

| Architecture Pattern | Reference File |
|---------------------|----------------|
| Hexagonal (ports/adapters) | `references/hexagonal-template.md` |
| MVC / Action-Command pipeline | `references/mvc-action-template.md` |
| Codec / Protocol pipeline | `references/codec-template.md` |
| Other / Custom | Use core dimensions below, adapt as needed |

If the architecture doesn't match a template, use the **Core Postmortem Dimensions** (Section 3) and adapt terminology.

### Phase 3: Conduct Assessment

Work through each dimension systematically. For each finding:

1. **Cite evidence** — file:line references, specific code patterns, measurable data
2. **Classify severity** — architectural violation (fix now) vs technical debt (track and schedule)
3. **Distinguish symptom from cause** — "slow" is a symptom; "O(n²) loop in hot path" is a cause
4. **Note spec ambiguity** — where design docs failed to answer a question the implementation faced

## Core Postmortem Dimensions

These dimensions apply regardless of architecture. Architecture-specific templates extend them.

### 3.1 Specification Fidelity

- Divergences between spec and implementation (intentional vs accidental)
- Ambiguities in spec that caused implementation friction
- Missing requirements discovered during implementation
- Requirements that proved unnecessary or misguided

**Key question:** Where did the spec lie by omission?

### 3.2 Boundary Integrity

Every architecture defines boundaries. Assess:

- Are boundaries enforced by the module/crate system?
- What crosses boundaries that shouldn't?
- Are boundary-crossing types appropriately abstract?

**Smell test:** If you had to replace one component (database, UI framework, protocol), what would break that shouldn't?

### 3.3 State Management

- Where does authoritative state live?
- Is there derived state that can drift from source?
- Are state transitions explicit and auditable?

### 3.4 Error Handling

- Error taxonomy: are different error categories (validation, I/O, business logic) distinguishable?
- Recovery semantics: what errors are recoverable? How?
- Observability: are errors logged with sufficient context?

### 3.5 Testability

- Can components be tested in isolation?
- Are there integration tests for boundary crossings?
- What's untested that should be?

### 3.6 In-House Library Evaluation

For each in-house library used:

```
## [Library Name]

### Fit for Purpose
- How well did the library's model match implementation needs?
- Impedance mismatches requiring workarounds?

### What Worked
- Specific positive example with context

### What Hurt
- Specific friction point
- Impact: [time lost / workaround complexity / bug introduced]
- Suggested fix or documentation improvement

### Documentation Gaps
- What you searched for but didn't find
- What was present but wrong/stale
```

### 3.7 Tooling Effectiveness

For each tool used (test frameworks, analysis tools, documentation generators, MCP servers):

| Tool | Purpose | Effectiveness | Recommendation |
|------|---------|---------------|----------------|
| | | | Keep / Improve / Retire |

**Questions per tool:**
- Did it surface useful insights or noise?
- Integration friction with workflow?
- False positives/negatives?
- Where did it fail you?

## Output Format

Structure the postmortem as:

1. **Executive Summary** (5 bullets maximum, ranked by severity)
2. **Specification Gaps** (ranked by impact)
3. **Architecture Assessment** (using appropriate template)
4. **Boundary Violations** (with file:line references where possible)
5. **Library Feedback** (per-library structured assessment)
6. **Tooling Report Card** (keep/improve/retire recommendations)
7. **Recommendations** (concrete, actionable, with effort estimates: S/M/L)

## Conduct Guidelines

- **Cite evidence.** "The adapter felt bloated" → "OrderAdapter grew to 400 lines; 60% is validation logic that belongs in domain"
- **Distinguish symptoms from causes.** "Tests are slow" is a symptom; "each test spins up a real database" is a cause.
- **Separate architectural violations from technical debt.** Violations need immediate attention; debt can be scheduled.
- **Acknowledge what worked.** If something worked well, say so briefly and move on—dwell on what needs attention.
- **Measure against the spec.** The design documents are the contract. If no spec exists, note that as a finding.
- **Note spec ambiguity as feedback.** Where the spec was unclear and implementation chose reasonably, feed that back to improve the spec.
- **Be direct.** The implementer is reading this to improve. Hedging wastes their time.

## Architecture-Specific Templates

For detailed assessment criteria, see:

- `references/hexagonal-template.md` — Domain/ports/adapters pattern
- `references/mvc-action-template.md` — MVC with action/command pipelines (e.g., GPUI-based apps)
- `references/codec-template.md` — Protocol codec and framing pipelines

Load the appropriate template based on the architecture identified in Phase 1.
