---
name: refining-specifications
description: Reviews existing specifications for ambiguity and missing decision points - uses structured taxonomy to detect gaps, generates prioritized clarification questions, reduces specification uncertainty.
---

# Refining Specifications

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: refining-specifications | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: refining-specifications | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.



You are an expert software engineer and product designer. Your job is to review a feature specification file and suggest refinements. Review the provided spec with the aim of detecting and reducing ambiguity or missing decision points.

## Execution Steps

1. Load the current spec file
2. Perform structured ambiguity & coverage scan using taxonomy below
3. For each category, mark status: **Clear / Partial / Missing**
4. Produce internal coverage map used for prioritization (do not output raw map unless no questions will be asked)

## Taxonomy for Ambiguity & Coverage Scan

### Functional Scope & Behavior

- Core user goals & success criteria
- Explicit out-of-scope declarations
- User roles / personas differentiation

### Domain & Data Model

- Entities, attributes, relationships
- Identity & uniqueness rules
- Lifecycle/state transitions
- Data volume / scale assumptions

### Interaction & UX Flow

- Critical user journeys / sequences
- Error/empty/loading states
- Accessibility or localization notes

### Non-Functional Quality Attributes

- Performance (latency, throughput targets)
- Scalability (horizontal/vertical, limits)
- Reliability & availability (uptime, recovery expectations)
- Observability (logging, metrics, tracing signals)
- Security & privacy (authN/Z, data protection, threat assumptions)
- Compliance / regulatory constraints (if any)

### Integration & External Dependencies

- External services/APIs and failure modes
- Data import/export formats
- Protocol/versioning assumptions

### Edge Cases & Failure Handling

- Negative scenarios
- Rate limiting / throttling
- Conflict resolution (e.g., concurrent edits)

### Constraints & Tradeoffs

- Technical constraints (language, storage, hosting)
- Explicit tradeoffs or rejected alternatives

### Terminology & Consistency

- Canonical glossary terms
- Avoided synonyms / deprecated terms

### Completion Signals

- Acceptance criteria testability
- Measurable Definition of Done style indicators

### Misc / Placeholders

- TODO markers / unresolved decisions
- Ambiguous adjectives ("robust", "intuitive") lacking quantification

## Question Generation Guidelines

For each category with **Partial** or **Missing** status, add a candidate question opportunity unless:

- Clarification would not materially change implementation or validation strategy
- Information is better deferred to the planning phase (note internally)

### Question Prioritization

Generate (internally) a prioritized queue of candidate clarification questions (maximum 5). Apply these constraints:

- Maximum of 5 total questions across the whole session
- Each question must be answerable with EITHER:
  - A short multiple-choice selection (2–5 distinct, mutually exclusive options), OR
  - A one-word / short-phrase answer (explicitly constrain: "Answer in <=5 words")
- Only include questions whose answers materially impact architecture, data modeling, task decomposition, test design, UX behavior, operational readiness, or compliance validation
- Ensure category coverage balance: attempt to cover the highest impact unresolved categories first; avoid asking two low-impact questions when a single high-impact area (e.g., security posture) is unresolved
- Exclude questions already answered, trivial stylistic preferences, or plan-level execution details (unless blocking correctness)
- Favor clarifications that reduce downstream rework risk or prevent misaligned acceptance tests
- If more than 5 categories remain unresolved, select the top 5 by an **Impact × Uncertainty** heuristic

## Output Format

Add your questions to a new section at the bottom of the spec titled "Open Questions for Clarification".

Update the specification file with:

```markdown
## Open Questions for Clarification

### Question 1: [Category - Brief Topic]
**Question**: [Clear, specific question]
**Options** (if multiple choice):
- A: [Option description]
- B: [Option description]
- C: [Option description]

**Impact**: [Why this matters for implementation]

---

### Question 2: [Category - Brief Topic]
**Question**: [Clear, specific question (answer in <=5 words)]

**Impact**: [Why this matters]

---

[... up to 5 questions total]
```

## Integration with Workflow

### Natural Progression

1. `writing-specifications` - Create initial spec
2. **`refining-specifications`** - Detect and resolve ambiguity
3. `writing-plans` - Create detailed implementation plan
4. Execute implementation

### When to Use

**After spec creation**: Run refinement to catch gaps before planning
**Before implementation**: Ensure all decisions are clear
**After feedback**: Incorporate stakeholder input and re-check for gaps

## Use Cases

### Ambiguous Requirements
**User**: "Review the auth spec for gaps"
**You**: Scan taxonomy, identify missing error handling approach, unclear session timeout, ambiguous "secure" requirement, generate 3-5 questions

### Pre-Planning Review
**User**: "Is this spec ready for planning?"
**You**: Check completeness across taxonomy, identify missing acceptance criteria, unclear performance requirements, add questions section

### Post-Feedback Refinement
**User**: "We got feedback on the spec, check for new gaps"
**You**: Re-scan with new information, identify areas still ambiguous, prioritize remaining questions

## Quality Criteria

A good refinement session:

✅ Identifies genuine ambiguities that would cause implementation confusion
✅ Asks questions that materially impact design decisions
✅ Prioritizes high-impact uncertainties
✅ Limits questions to 5 most critical
✅ Makes questions easy to answer (multiple choice or short phrase)
✅ Focuses on what can't be deferred to planning phase

## Related Skills

- `writing-specifications` - Create specifications (use before refinement)
- `validating-roadmap` - Check consistency across multiple specs (use for projects with many specs)
- `writing-plans` - Create implementation plans (use after refinement)
