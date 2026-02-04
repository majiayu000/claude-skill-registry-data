---
name: refine
description: Transform ideas into Product Backlog Items with acceptance criteria. Use when converting ideas to PBIs, adding acceptance criteria, or refining requirements. Triggers on keywords like "create pbi", "refine idea", "convert to pbi", "acceptance criteria", "make actionable".
allowed-tools: Read, Write, Edit, Grep, Glob, TodoWrite, AskUserQuestion
---

# Idea Refinement to PBI

Transform captured ideas into actionable Product Backlog Items.

## When to Use
- Idea artifact ready for refinement
- Need to add acceptance criteria
- Converting concept to implementable item

## Quick Reference

### Workflow
1. Read idea artifact
2. Load business context (entities, existing features)
3. Define acceptance criteria (GIVEN/WHEN/THEN)
4. Identify dependencies and out-of-scope
5. Create PBI artifact
6. Save to `team-artifacts/pbis/`
7. **Validate refinement** (MANDATORY) - Interview user to confirm assumptions, decisions, concerns
8. Suggest next: `/story {pbi-file}`

### Output
- **Path:** `team-artifacts/pbis/{YYMMDD}-pbi-{slug}.md`
- **ID Pattern:** `PBI-{YYMMDD}-{NNN}`

### Acceptance Criteria Format
```
GIVEN {precondition}
WHEN {action}
THEN {expected outcome}
```

### Related
- **Role Skill:** `business-analyst`
- **Command:** `/refine`
- **Input:** `/idea` output
- **Next Step:** `/story`

## Template

See: `team-artifacts/templates/pbi-template.md`

## Validation Step (MANDATORY)

After creating the PBI, validate with user:

### INVEST Criteria Check (Flag-Only)

Before validation questions, verify PBI meets INVEST criteria. Log failures but don't block:

| Criterion        | Check                                      | Explanation                                             |
| ---------------- | ------------------------------------------ | ------------------------------------------------------- |
| **Independent**  | Can be completed without other PBIs        | Minimizes coordination overhead                         |
| **Negotiable**   | Team has flexibility on HOW                | Details emerge during sprint, not locked upfront        |
| **Valuable**     | Clear user/business value                  | Every PBI delivers something stakeholders care about    |
| **Estimable**    | Team can size it                           | If too vague, split or research first                   |
| **Small**        | Fits in 1-2 sprints                        | Enables frequent feedback and course correction         |
| **Testable**     | Acceptance criteria exist                  | "How do we know it's done?" must be answerable          |

If criteria fail, note in validation summary but proceed with questions.

### Question Categories

| Category                | Example Question                                         |
| ----------------------- | -------------------------------------------------------- |
| **Assumptions**         | "The PBI assumes X. Is this correct?"                    |
| **Scope**               | "Should Y be included or deferred?"                      |
| **Risks**               | "This depends on Z. Is that available?"                  |
| **Acceptance**          | "Is criterion X complete or are there edge cases?"       |
| **Entities**            | "Create new entity or extend existing X?"                |
| **Important Decisions** | "Should we use approach A or B? (impacts architecture)"  |
| **Brainstorm**          | "Any alternative approaches we haven't considered?"      |

### Process

1. Run INVEST check, note any failures
2. Generate 3-5 questions from assumptions, scope decisions, dependencies
3. Use `AskUserQuestion` tool to interview
4. Enable brainstorming by asking for alternatives
5. Document in PBI under `## Validation Summary`
6. Update PBI based on answers

### Validation Output Format

```markdown
## Validation Summary

**Validated:** {date}
**INVEST Score:** {pass count}/6

### INVEST Flags
- {criterion}: {Pass/Fail - reason if fail}

### Confirmed Decisions
- {decision}: {user choice}

### Assumptions Confirmed
- {assumption}: Confirmed/Modified

### Brainstorm Notes
- {alternative approaches discussed}
- {ideas for future consideration}

### Important Decisions Made
- {decision 1}: {choice} - {rationale}

### Open Items
- [ ] {follow-up items}
```

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
