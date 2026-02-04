---
name: rfc-process
description: Request for Comments (RFC) process for technical proposals
allowed-tools: Read, Glob, Grep, Write, Edit
---

# RFC Process Skill

## When to Use This Skill

Use this skill when:

- **Rfc Process tasks** - Working on request for comments (rfc) process for technical proposals
- **Planning or design** - Need guidance on Rfc Process approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Facilitate the Request for Comments (RFC) process for technical proposals and design decisions.

## MANDATORY: Documentation-First Approach

Before creating RFCs:

1. **Invoke `docs-management` skill** for RFC patterns
2. **Verify RFC best practices** via MCP servers (perplexity)
3. **Base guidance on IETF RFC style adapted for software teams**

## RFC vs ADR

```text
RFC vs ADR Comparison:

RFC (Request for Comments):
• For proposals BEFORE decision is made
• Invites discussion and feedback
• May be accepted, rejected, or revised
• Typically larger scope than ADRs
• Used for significant changes requiring consensus

ADR (Architecture Decision Record):
• Documents decisions AFTER they are made
• Records the decision and rationale
• Immutable once accepted
• Focused on single decisions
• Used for all significant architecture decisions

Relationship:
RFC (Proposal) → Discussion → Decision → ADR (Record)
```

## RFC Template

```markdown
# RFC-[NUMBER]: [TITLE]

| Property | Value |
|----------|-------|
| **RFC Number** | RFC-[NUMBER] |
| **Title** | [Short, descriptive title] |
| **Author(s)** | [Name(s)] |
| **Status** | [Draft \| Open for Comment \| Final Comment \| Accepted \| Rejected \| Withdrawn] |
| **Created** | [YYYY-MM-DD] |
| **Updated** | [YYYY-MM-DD] |
| **Target Decision Date** | [YYYY-MM-DD] |
| **Stakeholders** | [Teams/Individuals] |

---

## Summary

[One paragraph executive summary. What is being proposed and why?]

---

## Motivation

### Problem Statement

[What problem does this RFC solve? Why is the current situation inadequate?]

### Goals

- [Goal 1]
- [Goal 2]
- [Goal 3]

### Non-Goals

- [Non-goal 1: What this RFC explicitly does NOT address]
- [Non-goal 2]

---

## Proposal

### Overview

[High-level description of the proposed solution]

### Detailed Design

[In-depth technical description. Include:
- Architecture changes
- API changes
- Data model changes
- Algorithm descriptions
- Integration points]

### Example Usage

```csharp
// Code example showing how the proposal would be used
public class ExampleUsage
{
    public async Task Example()
    {
        // Demonstrate the proposed API or pattern
    }
}
```

### Migration Plan

[How will existing systems/data be migrated?]

1. Phase 1: [Description]
2. Phase 2: [Description]
3. Phase 3: [Description]

---

## Alternatives Considered

### Alternative 1: [Name]

**Description:** [What this alternative entails]

**Pros:**

- [Pro 1]
- [Pro 2]

**Cons:**

- [Con 1]
- [Con 2]

**Why Not Chosen:** [Reason for rejecting this alternative]

### Alternative 2: [Name]

[Same structure...]

### Status Quo (Do Nothing)

**Description:** Continue with current approach

**Pros:**

- No migration effort
- No learning curve

**Cons:**

- [Problems that motivated this RFC remain]

---

## Trade-offs

| Trade-off | Chosen Path | Alternative Path |
|-----------|-------------|------------------|
| [Trade-off 1] | [What we accept] | [What we give up] |
| [Trade-off 2] | [What we accept] | [What we give up] |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Medium/High | Low/Medium/High | [Mitigation strategy] |
| [Risk 2] | Low/Medium/High | Low/Medium/High | [Mitigation strategy] |

---

## Implementation Plan

### Timeline

| Phase | Description | Duration | Dependencies |
|-------|-------------|----------|--------------|
| Phase 1 | [Description] | [Duration] | [Dependencies] |
| Phase 2 | [Description] | [Duration] | [Dependencies] |

### Resource Requirements

- [Resource 1: e.g., "2 senior engineers for 4 weeks"]
- [Resource 2: e.g., "Infrastructure team support"]

### Success Criteria

- [ ] [Criterion 1: Measurable success indicator]
- [ ] [Criterion 2: Measurable success indicator]

### Rollback Plan

[How to revert if the implementation fails]

---

## Security Considerations

[Security implications of this proposal]

- [Consideration 1]
- [Consideration 2]

---

## Privacy Considerations

[Privacy implications of this proposal]

- [Consideration 1]
- [Consideration 2]

---

## Testing Strategy

[How will this be tested?]

- Unit tests: [Approach]
- Integration tests: [Approach]
- Performance tests: [Approach]
- Rollout plan: [Canary, percentage rollout, etc.]

---

## Documentation Updates

[What documentation needs to be created or updated?]

- [ ] [Doc 1: e.g., "API reference"]
- [ ] [Doc 2: e.g., "Developer guide"]
- [ ] [Doc 3: e.g., "Operations runbook"]

---

## Open Questions

[Questions that need to be resolved during the comment period]

1. [Question 1]
2. [Question 2]

---

## Feedback

### Comments

[Space for discussion - may link to external discussion thread]

| Date | Author | Comment | Resolution |
|------|--------|---------|------------|
| [Date] | [Name] | [Comment] | [Resolution] |

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | [Date] | [Name] | Initial draft |
| 0.2 | [Date] | [Name] | [Changes made] |

---

## References

- [Reference 1]
- [Reference 2]
- [Related RFC/ADR]

```text

```

## RFC Lifecycle

```text
RFC Status Flow:

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│    ┌──────────┐     ┌─────────────────┐     ┌──────────────────┐            │
│    │  Draft   │────▶│ Open for Comment │────▶│  Final Comment   │           │
│    └──────────┘     └─────────────────┘     └──────────────────┘            │
│         │                    │                       │                       │
│         │                    │                       │                       │
│         ▼                    ▼                       ▼                       │
│    ┌──────────┐         ┌──────────┐           ┌──────────┐                 │
│    │ Withdrawn│         │ Withdrawn│           │ Accepted │                 │
│    └──────────┘         └──────────┘           └──────────┘                 │
│                                                      │                       │
│                              ┌──────────┐            │                       │
│                              │ Rejected │◀───────────┤                       │
│                              └──────────┘            │                       │
│                                                      ▼                       │
│                                              ┌──────────────┐                │
│                                              │ Implemented  │                │
│                                              └──────────────┘                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

Timeline:
• Draft: Author preparing, not ready for review
• Open for Comment: 2 weeks minimum for feedback
• Final Comment: 1 week for last objections
• Accepted/Rejected: Decision made
• Implemented: Work completed
```

## When to Write an RFC

| Situation | RFC Needed? |
|-----------|-------------|
| New microservice | Yes |
| Change in data model | Yes |
| New public API | Yes |
| Internal refactoring | Maybe |
| Bug fix | No |
| Minor enhancement | No |
| Breaking change | Yes |
| New technology adoption | Yes |
| Deprecation | Yes |

## RFC Roles

| Role | Responsibility |
|------|----------------|
| **Author** | Writes RFC, addresses feedback, drives to decision |
| **Reviewer** | Provides technical feedback |
| **Stakeholder** | Represents affected team or system |
| **Approver** | Makes final accept/reject decision |
| **Editor** | Ensures RFC meets standards (optional) |

## Lightweight RFC (Design Doc)

For smaller proposals, use this abbreviated format:

```markdown
# Design Doc: [TITLE]

**Author:** [Name]
**Date:** [Date]
**Status:** [Draft/Review/Approved]

## Context

[What problem are we solving?]

## Proposal

[What are we going to do?]

## Alternatives

[What else did we consider?]

## Decision

[What did we decide and why?]
```

## RFC Registry

```markdown
# RFC Registry

## Active RFCs

| RFC | Title | Author | Status | Target Date |
|-----|-------|--------|--------|-------------|
| RFC-012 | [Title] | [Author] | Open for Comment | 2025-02-15 |
| RFC-013 | [Title] | [Author] | Draft | - |

## Accepted RFCs

| RFC | Title | Accepted | ADR |
|-----|-------|----------|-----|
| RFC-010 | [Title] | 2025-01-10 | ADR-025 |
| RFC-011 | [Title] | 2025-01-15 | ADR-026 |

## Rejected/Withdrawn RFCs

| RFC | Title | Status | Reason |
|-----|-------|--------|--------|
| RFC-008 | [Title] | Rejected | [Brief reason] |
| RFC-009 | [Title] | Withdrawn | [Brief reason] |
```

## Best Practices

### For Authors

1. **Start discussions early**: Share drafts before formal RFC
2. **Be thorough**: Address obvious concerns preemptively
3. **Stay objective**: Present alternatives fairly
4. **Respond promptly**: Engage with feedback quickly
5. **Know when to pivot**: Be willing to change or withdraw

### For Reviewers

1. **Be constructive**: Suggest improvements, not just problems
2. **Be timely**: Respect deadlines
3. **Focus on substance**: Don't bikeshed
4. **Ask questions**: Clarify before criticizing
5. **Propose alternatives**: If you disagree, suggest alternatives

## Workflow

When creating RFCs:

1. **Identify Need**: Recognize significant change requiring consensus
2. **Draft RFC**: Use template, focus on clarity
3. **Pre-Review**: Share informally for early feedback
4. **Publish**: Move to "Open for Comment"
5. **Discuss**: Engage with feedback, revise as needed
6. **Finalize**: Move to "Final Comment"
7. **Decide**: Accept, reject, or withdraw
8. **Record**: Create ADR if accepted

## Further Reading

For detailed guidance:

---

**Last Updated:** 2025-12-26
