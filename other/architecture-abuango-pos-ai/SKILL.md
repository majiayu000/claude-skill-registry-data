---
name: architecture
description: System design review, architecture decision records, and component structure analysis. Use when designing systems, reviewing architecture, making technology decisions, or when user mentions "architecture", "system design", "ADR", "component structure", or "design review".
allowed-tools: Read, Glob, Grep, Bash
---

# Architecture Skill

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

You are performing architecture design or review for a POS project. Architecture decisions are the hardest to reverse — measure twice, cut once.

## Process

### Step 1: Understand Context

1. **Identify the project** — Read the project YAML and existing codebase
2. **Load existing architecture docs** — Check for:
   - `docs/architecture/` or `docs/adr/` in the repo
   - Existing `AGENTS.md` or system diagrams
   - `PROJECT_INDEX.yaml` for file structure overview
3. **Clarify scope** — Is this a new system design, a review of existing architecture, or a change proposal?

### Step 2: Analyze (Review Mode)

When reviewing existing architecture:

- [ ] **Component boundaries** — Are services/modules cohesive with minimal coupling?
- [ ] **Data flow** — Is data ownership clear? No circular dependencies?
- [ ] **API contracts** — Are interfaces between components well-defined?
- [ ] **Scalability** — Can the system handle 10x load without redesign?
- [ ] **Single points of failure** — Are there components whose failure cascades?
- [ ] **Technology fit** — Do chosen technologies match the problem domain?
- [ ] **Security boundaries** — Are trust zones and auth boundaries explicit?
- [ ] **Operational concerns** — Logging, monitoring, deployment, rollback?

### Step 3: Design (Creation Mode)

When designing new architecture:

1. **Define constraints** — Budget, team size, timeline, existing tech stack
2. **Identify key decisions** — Database choice, communication patterns, hosting model
3. **Map components** — Services, data stores, external integrations, client apps
4. **Define interfaces** — API contracts between components
5. **Document trade-offs** — Every decision has trade-offs; make them explicit

### Step 4: Produce ADR

For every significant architecture decision, create an Architecture Decision Record.

## ADR Template

Save to: `{repo}/docs/adr/{NNNN}-{title}.md`

```markdown
# ADR-{NNNN}: {Title}

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
**Date:** {DATE}
**Decision Makers:** {who}

## Context

{What is the issue? What forces are at play?}

## Decision

{What is the change being proposed or made?}

## Alternatives Considered

### Option A: {Name}
- Pros: {list}
- Cons: {list}

### Option B: {Name}
- Pros: {list}
- Cons: {list}

## Consequences

### Positive
- {consequence}

### Negative
- {consequence}

### Neutral
- {consequence}

## References
- {links to relevant docs, RFCs, prior art}
```

## Architecture Review Output

```markdown
# Architecture Review: {PROJECT}

**Date:** {DATE}
**Scope:** {what was reviewed}

## Summary

{1-2 sentence overall assessment}

## Component Map

{Describe the major components and their relationships}

## Findings

### Strengths
- {What's working well architecturally}

### Concerns
| Concern | Severity | Recommendation |
|---------|----------|----------------|
| {issue} | High/Med/Low | {what to do} |

### Recommended ADRs
- ADR needed for: {decision that should be formally documented}

## Decision

**Status:** SOUND / NEEDS_CHANGES / REDESIGN_REQUIRED
```

## Integration with POS

- Architecture reviews feed into `/plan-generation` — review first, plan second
- Use `/excalidraw` to generate visual diagrams from the architecture analysis
- Save reviews to: `{teams_dir}/{team}/projects/{project}/reviews/arch-{date}.md`

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
