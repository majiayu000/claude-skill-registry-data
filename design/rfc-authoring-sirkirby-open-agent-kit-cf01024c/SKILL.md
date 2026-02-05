---
name: rfc-authoring
description: Guide OAK RFC creation with template selection, section-by-section writing expertise, and quality-driven authoring patterns.
---

# RFC Authoring Expertise

Guide the creation of high-quality Request for Comments (RFC) documents using OAK's structured workflow and templates.

## OAK RFC Command Workflow

```
/oak.rfc-create  →  Draft & Iterate  →  /oak.rfc-validate  →  Review Ready
```

### CLI Commands

| Command | Purpose |
|---------|---------|
| `oak rfc create "{title}" --template {type}` | Scaffold new RFC |
| `oak rfc list [--status draft\|review\|adopted]` | Discover existing RFCs |
| `oak rfc validate RFC-{number}` | Check structure and quality |
| `oak rfc show RFC-{number}` | Display RFC details |

### File Structure

```
oak/
├── constitution.md          # Project standards (RFCs must align)
└── rfc/
    ├── RFC-001-{slug}.md    # Engineering RFC
    ├── RFC-002-{slug}.md    # Feature RFC
    └── ...
```

## Template Selection Guide

Choose the template that best matches the RFC's primary purpose:

### Engineering Template
**Use when**: Proposing technical implementation changes, API modifications, infrastructure updates, or system design decisions.

**Key sections**: Detailed Design, API/Interface Changes, Data Model, Migration Strategy, Performance Implications

**Signals to use this template**:
- "We need to change how X works"
- "Add support for Y in the backend"
- "Refactor the Z subsystem"

### Architecture Template (ADR)
**Use when**: Recording significant architectural decisions that affect multiple systems or establish long-term patterns.

**Key sections**: Context, Decision, Consequences (Positive/Negative/Neutral), Alternatives Considered

**Signals to use this template**:
- "Should we use X or Y for this?"
- "We decided to adopt Z pattern"
- "Recording why we chose this approach"

### Feature Template
**Use when**: Proposing user-facing features with UX considerations, acceptance criteria, and rollout planning.

**Key sections**: User Story, User Experience, Functional Requirements, Acceptance Criteria, Rollout Strategy

**Signals to use this template**:
- "Users should be able to..."
- "Add a new capability for..."
- "Improve the experience when..."

### Process Template
**Use when**: Proposing changes to team workflows, operational procedures, or organizational processes.

**Key sections**: Current State, Proposed Process, Roles and Responsibilities, Transition Plan, Training Requirements

**Signals to use this template**:
- "Change how we handle..."
- "Improve our workflow for..."
- "Standardize the process of..."

## Section-by-Section Writing Guide

### Summary / Executive Summary
**Goal**: 2-3 sentences that let a busy stakeholder decide if they need to read more.

**Pattern**: `[Current state problem] + [Proposed change] + [Expected impact]`

**Good example**: "API response times exceed SLA targets during peak hours. This RFC proposes implementing response caching with Redis, reducing P99 latency from 2s to 200ms and improving user satisfaction scores."

**Avoid**: Vague statements, implementation details, or just restating the title.

### Motivation / Problem Statement
**Goal**: Build urgency with evidence. Answer "why now?" and "why does this matter?"

**Include**:
- Quantitative evidence (metrics, incident counts, user complaints)
- Qualitative impact (team frustration, technical debt, missed opportunities)
- Business context (OKRs, commitments, competitive pressure)

**Pattern**: `[Evidence of problem] → [Who is affected] → [Cost of inaction]`

### Goals and Non-Goals
**Goals**: Use measurable outcomes with the SMART pattern (Specific, Measurable, Achievable, Relevant, Time-bound).

**Pattern**: `"Reduce X from Y to Z by [date]"` or `"Enable users to [action] without [constraint]"`

**Non-Goals**: Explicitly exclude adjacent work to prevent scope creep. Be specific about what you're NOT solving.

### Detailed Design / Proposed Solution
**Goal**: Enough detail that a reviewer can assess feasibility, effort, and risks.

**Include**:
- Architecture diagrams or component interactions
- Data flows and state changes
- API contracts (request/response examples)
- Edge cases and error handling

**Avoid**: Implementation-level code (save for PRs), assumptions without evidence.

### Drawbacks / Risks
**Goal**: Show you've thought critically about what could go wrong.

**Pattern**: For each risk, provide:
1. **Risk**: What could happen
2. **Impact**: How severe (High/Medium/Low)
3. **Likelihood**: How probable (High/Medium/Low)
4. **Mitigation**: How you'll prevent or respond

**Tip**: Include operational risks (monitoring gaps, on-call burden), not just technical risks.

### Alternatives Considered
**Goal**: Demonstrate you've evaluated options fairly, not just justified a predetermined choice.

**For each alternative**:
1. Describe the approach objectively
2. List genuine pros (not strawman arguments)
3. List cons with evidence
4. Explain why it wasn't chosen (the decisive factor)

**Tip**: A strong Alternatives section builds trust that the proposal is well-reasoned.

### Success Metrics
**Goal**: Define how you'll know the RFC achieved its objectives.

**Pattern**: `"[Metric name]: [Baseline] → [Target] by [date]"`

**Include**: Leading indicators (can measure soon) and lagging indicators (ultimate success).

## Quality Checklist Before Review

Before submitting for review, verify:

- [ ] **No placeholders**: All `[TODO]` and `> Provide...` prompts replaced with real content
- [ ] **Measurable goals**: Goals include specific numbers and timelines
- [ ] **Evidence-backed motivation**: Problem statement cites data, not just opinion
- [ ] **Fair alternatives**: At least 2 alternatives with genuine pros
- [ ] **Risk mitigation**: Every identified risk has an owner and mitigation plan
- [ ] **Success criteria**: Metrics have baselines and targets
- [ ] **Cross-references**: Related RFCs and ADRs are linked
- [ ] **Constitution alignment**: Proposal follows project standards in `oak/constitution.md`

## Common Pitfalls

| Pitfall | How to Fix |
|---------|------------|
| Summary restates the title | Add problem evidence and expected outcome |
| Goals are vague ("improve performance") | Add specific metrics ("reduce P99 from X to Y") |
| Only one alternative considered | Add at least one more with genuine pros |
| Risks listed without mitigation | Add owner and mitigation plan for each |
| Missing rollback plan | Add specific rollback triggers and procedure |
| No success metrics | Define baseline → target for key metrics |
