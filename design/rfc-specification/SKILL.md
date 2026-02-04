---
name: rfc-specification
description: RFC (Request for Comments) specification writing with objective technical analysis. Use when creating technical specifications, design documents, or architecture proposals that require structured evaluation of options and trade-offs.
---

# RFC Specification Writing Skill

This skill automatically activates when writing technical specifications, design documents, or architecture proposals that require structured evaluation and stakeholder review.

## When This Skill Activates

- Creating a new technical RFC or design document
- Proposing architectural changes or new systems
- Evaluating technical options objectively
- Documenting technical decisions with rationale
- Writing system design specifications

## Core Principles

### Objective Technical Analysis

RFCs must maintain strict neutrality when evaluating options:

1. **Evidence-Based Evaluation**
   - Support claims with data, benchmarks, or documented experience
   - Avoid subjective language ("better", "best", "obvious choice")
   - Present measurable criteria for comparison

2. **Balanced Trade-off Analysis**
   - Every option has advantages AND disadvantages
   - Document both explicitly for each alternative
   - Avoid dismissing options without clear justification

3. **Separation of Facts and Opinions**
   - Clearly label assumptions vs verified facts
   - Cite sources for technical claims
   - Distinguish between team preferences and technical constraints

4. **Stakeholder Neutrality**
   - Present options without advocating for a predetermined choice
   - Let evaluation criteria drive the recommendation
   - Document dissenting opinions fairly

## RFC Document Structure

### Required Sections

1. **Header Metadata**
   ```yaml
   ---
   rfc_id: RFC-XXXX
   title: [Descriptive Title]
   status: DRAFT | REVIEW | APPROVED | IN_PROGRESS | COMPLETED | SUPERSEDED
   author: [Name]
   reviewers: [List of reviewers with status]
   created: YYYY-MM-DD
   last_updated: YYYY-MM-DD
   decision_date: YYYY-MM-DD (when approved)
   ---
   ```

2. **Overview** (1-2 paragraphs)
   - What this RFC proposes
   - Why it matters now
   - Expected outcome

3. **Background & Context**
   - Current state of the system
   - Historical context if relevant
   - Glossary of terms
   - Links to related RFCs or documentation

4. **Problem Statement**
   - Specific problem being addressed
   - Evidence of the problem (metrics, incidents, user feedback)
   - Impact of not solving (cost, risk, opportunity loss)

5. **Goals & Non-Goals**
   - Explicit scope boundaries
   - What success looks like
   - What this RFC deliberately does NOT address

6. **Evaluation Criteria**
   - Measurable criteria for comparing options
   - Weight or priority of each criterion
   - Minimum thresholds where applicable

7. **Options Analysis**
   For each option (minimum 2):
   ```markdown
   ### Option N: [Name]

   **Description**: [What this option entails]

   **Advantages**:
   - [Pro 1]
   - [Pro 2]

   **Disadvantages**:
   - [Con 1]
   - [Con 2]

   **Evaluation Against Criteria**:
   | Criterion | Score/Rating | Notes |
   |-----------|--------------|-------|
   | ...       | ...          | ...   |

   **Effort Estimate**: [Complexity and resources required]

   **Risk Assessment**: [Potential risks and mitigations]
   ```

8. **Recommendation**
   - Recommended option with justification
   - How it scores against criteria
   - Acknowledged trade-offs being accepted

9. **Technical Design** (for approved RFCs)
   - Architecture diagrams
   - API specifications
   - Data models
   - Security considerations

10. **Implementation Plan**
    - Phases and milestones
    - Dependencies
    - Rollback strategy

11. **Open Questions**
    - Unresolved technical questions
    - Areas needing further investigation
    - Pending stakeholder input

12. **Decision Record**
    - Final decision made
    - Date and approvers
    - Key discussion points
    - Conditions or constraints on approval

## RFC Lifecycle

```
DRAFT → REVIEW → APPROVED → IN_PROGRESS → COMPLETED
                    ↓
               SUPERSEDED (if replaced by newer RFC)
```

### Status Definitions

| Status | Description |
|--------|-------------|
| DRAFT | Initial writing, not ready for review |
| REVIEW | Open for stakeholder feedback |
| APPROVED | Decision made, ready for implementation |
| IN_PROGRESS | Implementation underway |
| COMPLETED | Implementation finished |
| SUPERSEDED | Replaced by newer RFC (link to new RFC) |

## Evaluation Criteria Framework

Use these standard criteria categories (adapt as needed):

### Technical Criteria
- **Performance**: Latency, throughput, resource usage
- **Scalability**: Horizontal/vertical scaling, bottlenecks
- **Reliability**: Fault tolerance, recovery, availability
- **Security**: Attack surface, data protection, compliance
- **Maintainability**: Code complexity, debugging, updates

### Operational Criteria
- **Operability**: Monitoring, alerting, incident response
- **Deployment**: CI/CD integration, rollback capability
- **Documentation**: Learning curve, knowledge transfer

### Business Criteria
- **Time to Implement**: Development effort, dependencies
- **Cost**: Infrastructure, licensing, maintenance
- **Risk**: Technical risk, organizational risk

## Neutral Language Guidelines

### Avoid
- "Obviously the best choice"
- "Everyone agrees that..."
- "This is clearly superior"
- "The only sensible option"
- Dismissing alternatives as "not worth considering"

### Use Instead
- "Based on criteria X, Option A scores higher because..."
- "Option B requires consideration of trade-off Y"
- "The data suggests that..."
- "Stakeholder input indicates a preference for..."
- "Given constraints A and B, Option C is recommended"

## Quality Checklist

Before marking RFC as REVIEW:

- [ ] All required sections are complete
- [ ] At least 2 alternatives are analyzed
- [ ] Evaluation criteria are explicit and measurable
- [ ] Trade-offs are documented for each option
- [ ] Language is objective and evidence-based
- [ ] Technical diagrams are included where helpful
- [ ] Open questions are clearly listed
- [ ] Implementation plan is realistic

## Integration with CTO Architect Workflow

When the CTO Architect agent creates technical specifications:

1. **Use this skill** for any significant technical decision
2. **Follow the template** in `references/rfc-template.md`
3. **Ensure neutral evaluation** of all options
4. **Link to related PRDs** when applicable
5. **Request review** from appropriate technical stakeholders

## File Naming Convention

- RFC documents: `RFC-XXXX-<short-description>.md`
- Example: `RFC-0042-api-gateway-selection.md`

## Directory Structure

```
rfcs/
├── draft/           # Work in progress
├── review/          # Under stakeholder review
├── approved/        # Approved, awaiting or in implementation
├── completed/       # Implementation finished
└── archive/         # Superseded or abandoned
    └── YYYY/
```

## References

- Template: `./references/rfc-template.md`
- Evaluation Matrix: `./references/evaluation-matrix.md`
