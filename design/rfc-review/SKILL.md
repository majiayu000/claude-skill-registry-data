---
name: rfc-review
description: Guide OAK RFC validation with quality assessment frameworks, review rubrics, and structured feedback patterns.
---

# RFC Review Expertise

Guide comprehensive review and validation of RFC documents using structured assessment frameworks and quality rubrics.

## OAK RFC Validation Workflow

```
Identify RFC  →  Run Automated Checks  →  Manual Review  →  Provide Feedback  →  Verify Fixes
```

### CLI Commands

| Command | Purpose |
|---------|---------|
| `oak rfc validate RFC-{number}` | Run structural validation |
| `oak rfc validate RFC-{number} --strict` | Strict mode (all checks) |
| `oak rfc show RFC-{number}` | View RFC details and metadata |
| `oak rfc list --status review` | Find RFCs pending review |

## Review Process

### Step 1: Context Gathering
Before reviewing content, gather context:

1. **RFC Metadata**: Check status, author, creation date, tags
2. **Related RFCs**: Search for RFCs with similar tags or scope
3. **Constitution Alignment**: Review `oak/constitution.md` for applicable standards
4. **Codebase Impact**: Identify affected modules, services, or components

### Step 2: Automated Validation
Run `oak rfc validate RFC-{number}` to check:
- Required sections present
- Metadata completeness
- No placeholder text remaining
- Proper markdown structure

### Step 3: Manual Review
Apply the quality rubric below to assess content quality beyond structural checks.

## Quality Assessment Rubric

Score each dimension 1-5 with evidence:

### Clarity & Narrative Flow (1-5)
| Score | Criteria |
|-------|----------|
| 5 | Executive can understand problem and solution in 2 minutes |
| 4 | Clear flow with minor ambiguities |
| 3 | Understandable but requires re-reading sections |
| 2 | Confusing structure or inconsistent terminology |
| 1 | Cannot follow the proposal's logic |

**Questions to ask**:
- Can someone unfamiliar with the project understand the problem?
- Does the summary accurately reflect the full proposal?
- Are technical terms defined or commonly understood?

### Technical Depth & Feasibility (1-5)
| Score | Criteria |
|-------|----------|
| 5 | Implementation-ready with clear architecture and edge cases |
| 4 | Solid design with minor gaps that won't block review |
| 3 | Conceptually sound but missing key implementation details |
| 2 | Significant technical gaps or questionable feasibility |
| 1 | Not implementable as specified |

**Questions to ask**:
- Could an engineer start implementation from this spec?
- Are data flows and state changes clearly described?
- Are edge cases and error conditions addressed?

### Risk Identification & Mitigation (1-5)
| Score | Criteria |
|-------|----------|
| 5 | Comprehensive risks with owned mitigations and triggers |
| 4 | Major risks covered with reasonable mitigations |
| 3 | Some risks identified but gaps in mitigation |
| 2 | Obvious risks missing or mitigations inadequate |
| 1 | No meaningful risk analysis |

**Questions to ask**:
- What happens if this fails in production?
- Are operational risks (monitoring, on-call) addressed?
- Who owns each mitigation, and what triggers escalation?

### Alignment with Standards (1-5)
| Score | Criteria |
|-------|----------|
| 5 | Fully aligned with constitution and existing patterns |
| 4 | Minor deviations with documented rationale |
| 3 | Some inconsistencies with project conventions |
| 2 | Significant departures from established patterns |
| 1 | Contradicts existing architecture or standards |

**Questions to ask**:
- Does this follow patterns established in prior RFCs?
- Is the approach consistent with `oak/constitution.md`?
- Are deviations from standards justified?

### Rollout & Measurement Readiness (1-5)
| Score | Criteria |
|-------|----------|
| 5 | Phased rollout with metrics, monitoring, and rollback plan |
| 4 | Clear rollout plan with minor gaps in observability |
| 3 | Basic rollout plan but missing rollback or metrics |
| 2 | Vague rollout with no clear success criteria |
| 1 | No rollout plan or success metrics |

**Questions to ask**:
- How will we know if this succeeded or failed?
- What's the rollback procedure if issues arise?
- Are metrics defined with baselines and targets?

## Issue Severity Classification

### Critical (Must Fix Before Progressing)
- Missing required sections (Summary, Motivation, Design)
- Incorrect RFC status for the review stage
- Blocking inconsistencies with adopted standards
- No rollback plan for high-risk changes
- Placeholder text in critical sections

### Major (Should Fix Before Approval)
- Ambiguous scope or unclear boundaries
- Weak success metrics (no baselines or targets)
- Alternatives analysis feels superficial or biased
- Risk mitigations lack owners or triggers
- Technical design has significant gaps

### Minor (Nice-to-Have Improvements)
- Stylistic inconsistencies
- Could use more examples or diagrams
- Minor formatting or markdown issues
- Additional alternatives could strengthen the case
- More detail in non-critical sections

## Structured Feedback Template

When providing feedback, use this structure:

```markdown
## RFC Review: RFC-{number} - {title}

### Overall Assessment
**Rating**: Ready / Needs Work / Blocked
**Rubric Scores**: Clarity: X, Technical: X, Risks: X, Alignment: X, Rollout: X

### Critical Issues
1. **[Section]**: [Issue description]
   - Evidence: [Quote or reference]
   - Suggested fix: [Specific recommendation]

### Major Issues
1. **[Section]**: [Issue description]
   - Evidence: [Quote or reference]
   - Suggested fix: [Specific recommendation]

### Minor Issues
- [Section]: [Brief issue and suggestion]

### Strengths
- [What the RFC does well]

### Questions for Author
1. [Clarifying question]
2. [Design question]

### Next Steps
- [ ] [Specific action item]
- [ ] [Specific action item]
```

## Review Questions by Section

### Summary
- Does it explain the problem, solution, AND expected impact?
- Can a busy stakeholder decide if they need to read more?
- Does it avoid implementation details?

### Motivation
- Is there quantitative evidence (metrics, incidents, complaints)?
- Is it clear who is affected and how severely?
- Does it answer "why now?" convincingly?

### Goals / Non-Goals
- Are goals measurable with specific numbers and timelines?
- Are non-goals specific enough to prevent scope creep?
- Do goals align with the stated motivation?

### Detailed Design
- Could an engineer implement from this spec?
- Are component interactions and data flows clear?
- Are edge cases and error conditions addressed?

### Drawbacks / Risks
- Are all obvious risks identified?
- Does each risk have impact, likelihood, AND mitigation?
- Are operational risks (monitoring, on-call) included?

### Alternatives
- Are at least 2 alternatives considered?
- Do alternatives have genuine pros (not strawman)?
- Is the rejection rationale clear and evidence-based?

### Success Metrics
- Do metrics have baselines AND targets?
- Are there both leading and lagging indicators?
- Can the metrics actually be measured with current tooling?

### Rollout Plan
- Are phases clearly defined with criteria for progression?
- Is there a rollback plan with specific triggers?
- Are feature flags or blast-radius controls specified?

## Common Review Findings

| Finding | Typical Fix |
|---------|-------------|
| Summary just restates the title | Add problem evidence + expected outcome |
| "Improve performance" as a goal | Add specific metrics: "Reduce P99 from Xms to Yms" |
| Single weak alternative | Add 2+ alternatives with genuine pros/cons |
| Risks without mitigation owners | Assign owner and add mitigation timeline |
| No rollback plan | Add triggers, procedure, and owner |
| Success metrics without baselines | Research current state and add baseline numbers |
| Placeholder text remaining | Flag as Critical - must replace before review |

## Re-Review Checklist

After fixes are applied, verify:

- [ ] All Critical issues resolved
- [ ] Major issues addressed or explicitly deferred with rationale
- [ ] Automated validation passes (`oak rfc validate`)
- [ ] Cross-references updated if scope changed
- [ ] Status updated appropriately
