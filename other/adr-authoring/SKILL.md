---
name: adr-authoring
description: "Guide the selection of ADR templates (e.g., MADR, Nygard, Y-Statement) and author high-quality Architectural Decision Records that focus on context, rationale, and consequences. Trigger when requested to draft, write, or format a new ADR. Keywords: MADR, Nygard, Y-statement, architectural rationale, trade-offs, consequences."
---

# ADR Authoring - Drafting Decisions with Rationale

This skill helps the agent and team author high-quality Architectural Decision Records (ADRs) using industry-standard templates and structures that emphasize context, clear trade-offs, and downstream consequences.

## Progressive Disclosure & External Resources

- **External Resources**: This is a self-contained skill. Templates are described inline. No external scripts are required.
- **Reference**: For more details, refer to the templates list at [adr.github.io/adr-templates/](https://adr.github.io/adr-templates/).

## Freedom Calibration & Constraints

- **Constraint Level: Medium**
  - **High Rigidity**: All drafted ADRs must contain the three fundamental sections: Context, Decision (with status), and Consequences (trade-offs, new risks, required updates).
  - **High Freedom**: The selection of template format (e.g., Nygard vs. MADR vs. Y-Statement) is left to team preference or project conventions.

## Decision Tree: Choosing the Right Template

```
Determine Target Audience & Depth
 ├─ Lightweight, developer-focused, markdown-native → [Use MADR (Markdown ADR) Template]
 ├─ Industry standard, simple, narrative structure → [Use Nygard Template]
 ├─ Formal, enterprise-grade, highly structured, reason-based → [Use Y-Statement Template]
 └─ Agile, brief, minimal overhead → [Use Lightweight Paragraph Template]
```

## Professional Mindset & Design Principles

1. **Consequences over Rationale**: The impact of a decision (what it enables, disables, forces, or limits) is more important than why it was chosen.
2. **Honest Trade-offs**: Every design choice has downsides. Refusing to document negatives in an ADR is an anti-pattern.
3. **No Retrospective Rewriting**: Keep ADRs short, objective, and contemporaneous. Write it when the decision is made.

---

## Step-by-Step Execution Procedure

### Step 1: Choose the ADR Template

Review the decision requirements and choose the template style:

#### Option A: Nygard Template (Classic)
```markdown
# [Number]. [Title]

## Status
[Draft | Proposed | Accepted | Rejected | Deprecated | Superseded by ADR-XX]

## Context
[What is the context and problem we are trying to solve? What are the constraints?]

## Decision
[What is the change/decision we are committing to?]

## Consequences
[What becomes easier or harder? What new problems are introduced? What is the impact?]
```

#### Option B: MADR Template (Markdown ADR)
```markdown
# [Title of Decision Record]

* Status: [draft | proposed | accepted | rejected | deprecated | superseded by [ADR-XX](file:///path/to/adr-XX.md)]
* Deciders: [list of names]
* Date: [YYYY-MM-DD]

## Technical Story
* [Link to Story/Epic/Issue]

## Context and Problem Statement
[Describe the context and problem, e.g., in free text or a set of questions.]

## Decision Drivers
* [driver 1, e.g., performance]
* [driver 2, e.g., cost]

## Considered Options
* [Option 1]
* [Option 2]

## Decision Outcome
Chosen option: [Option X], because [justification].

### Positive Consequences
* [e.g., improves speed]

### Negative Consequences
* [e.g., increases operational cost]

## Pros and Cons of Options

### [Option 1]
* Good, because [argument]
* Bad, because [argument]
```

#### Option C: Y-Statement Template
```0
In the context of [use case/context],
we decided for [chosen option]
and against [alternative options],
to achieve [quality attributes/drivers],
accepting [consequences/downsides].
```

### Step 2: Gather Context and Trade-offs

- Query/discuss the technical drivers (e.g., Performance, Cost, Complexity, Vendor Lock-in).
- List the alternative options that were realistically considered.
- Define the pros and cons of each option.

### Step 3: Write and Review the Record

- Populate the chosen template.
- Ensure the filename follows standard naming patterns: `docs/adr/NNNN-title-in-kebab-case.md` (e.g., `docs/adr/0004-use-postgres-for-caching.md`).
- Validate that the consequences section includes actionable items (e.g., team training, migration scripts, documentation updates).
- Trigger the local memory capture using the standardized capture script.

---

## Critical Anti-Patterns (NEVER List)

| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** hide negatives | Omitting negative consequences or pretending a solution has no downsides. | Devote an equal effort to documenting negative consequences/trade-offs. |
| **NEVER** write a blog post | Writing long, rambling essays instead of a concise, structured record. | Keep ADRs short (1-2 pages maximum). Use bullet points. |
| **NEVER** lose track of status | Forgetting to mark status, leading to confusion about what is active. | Keep the Status section at the top of the file, clear and updated. |

---

## Common Error Scenarios & Fallbacks

### Scenario 1: Lack of Consensus on Trade-offs

- **Root Cause**: Team members disagree on the pros/cons of considered options.
- **Fallback**:
  1. Document all differing opinions honestly in the "Pros and Cons" section.
  2. Let the owner/lead architect make the final decision outcome.
  3. Change status to "Proposed" and open a PR for collective review.


