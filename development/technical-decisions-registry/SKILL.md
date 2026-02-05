---
name: Technical Decisions Registry
description: This skill provides access to a project's recorded technical decisions and architectural patterns. Use this skill to understand established patterns, validate proposals against decisions, and cite decisions when reviewing code or specifications. Works with any project that maintains a decisions registry.
---

# Technical Decisions Registry Skill

## Purpose

This skill gives access to a project's technical decision registry. It enables:
- **Pattern lookup**: Find the established approach for a specific concern (e.g., "What's our validation pattern?")
- **Proposal validation**: Check if a new spec or code change violates established decisions
- **Decision citation**: Reference decisions by ID when reviewing code or specifications
- **Constraint understanding**: Learn the context, tradeoffs, and examples for architectural choices

## When to Use This Skill

Invoke this skill when:
- **Creating proposals or specifications**: Validate early against decisions to catch pattern violations
- **Reviewing specifications or code**: Check alignment and cite decisions for clarity
- **Asking architectural questions**: "What's our approach to X?" or "Should we use Y or Z?"
- **Understanding constraints**: Learn why a decision was made and its tradeoffs
- **Onboarding new features**: Understand which patterns apply to a new domain

## Getting Started

1. **Create your decisions registry**: Add `docs/decisions.md` to the project
2. **Document decisions**: Use the decision structure above
3. **Cite in proposals**: Have proposal authors reference relevant decisions
4. **Iterate**: Update decisions as your project evolves

## Decision Registry

The registry is documented [here](references/decisions.md).

Reference the project's decisions registry for the complete, authoritative list. The registry should be located at `docs/decisions.md`.

## Common Interaction Patterns

### Scenario 1: Validating a New Proposal

**User says**: "I'm creating a new feature spec. What decisions should I enforce?"

**Skill response**:
```
Query results from decisions registry by category or feature domain.

Relevant Decisions:
1. [Decision ID] — [Title and brief description]
2. [Decision ID] — [Title and brief description]
...

Action: Include a "Conventions (Required)" or "Architecture Constraints" section
in your proposal that cites these decision IDs. Implementers will know exactly
which patterns apply.
```

### Scenario 2: Code Review Comment

**Reviewer finds code that violates a decision**

**Reviewer cites**: "This violates `decision-id-name`. [Suggest correct approach]."

**Skill provides**: Full decision context, examples of correct/incorrect approaches, related decisions

**Example**:
```
"This design violates our architectural decision on [topic].
See decision: `decision-id` for the rationale and correct approach."
```

### Scenario 3: Architectural Question

**Developer asks**: "How should we approach [architectural concern]?"

**Skill response**:
```
Reference decision: decision-id

Summary: [What the decision says]
Context: [Why this decision was made]
Tradeoffs: [Pro/con analysis]

Example of correct approach: [code/design]
Example to avoid: [code/design]
```

### Scenario 4: Onboarding / Feature Planning

**New team member or feature lead asks**: "What patterns should I follow when building [feature]?"

**Skill response**:
```
The following decisions apply to [feature]:

1. decision-id-1 — [Title]
2. decision-id-2 — [Title]
3. decision-id-3 — [Title]

See each decision for context, examples, and related patterns. Ask if you need
clarification on any decision.
```

## Keeping Decisions Current

**When decisions change**:
1. Update the decisions registry file (include rationale for change)
2. Mark old decision as "Superseded" with link to new one
3. Add new decision with full context and examples
4. Skill automatically uses updated version in next session

## Tips for Effective Use

1. **Cite by ID**: When giving feedback, reference decisions by ID to enable quick lookup
2. **Include context**: When validating code or proposals, provide snippets for analysis
3. **Check related decisions**: Most decisions interact with others; review related decisions for full picture
4. **Use in proposals**: All new proposals should include a "Conventions (Required)" or "Architecture Constraints" section citing relevant decisions
5. **Update when needed**: If a decision no longer makes sense, propose updating it (don't ignore it)
6. **Share rationale**: When citing a decision, explain why it applies to the situation
