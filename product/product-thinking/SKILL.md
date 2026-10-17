---
name: product-thinking
description: |
  Run structured product thinking exercises before writing a spec. Use this skill when:
  - You need to think through a feature idea before writing a PRD
  - You want to run the 11-star experience exercise for a feature
  - You need a positioning statement using Geoffrey Moore's framework
  - You want to define product principles and success vision for a new feature
  - You have a raw feature idea and need to turn it into a structured brief
---

# Product Thinking

Interactive skill that builds product thinking through 5 structured exercises. Outputs a Product Thinking Brief that feeds into spec writing.

This is the "thinking before writing" layer — run this BEFORE drafting any spec.

## Workflow

1. **Gather context** — Ask user for: feature idea, target users, motivation
2. **Read source files** — Personas, product context, feedback, competitors (only relevant files)
3. **Run 5 exercises** — Present findings, get user validation at each step
4. **Write brief** — Output to file or print

## The 5 Exercises

### Exercise 1: Problem Statement

Answer four questions with evidence:

| Dimension | What to Answer |
|-----------|---------------|
| **Who** | Specific persona (not generic "users") |
| **Evidence** | Cite feedback, pilot data, research — not assertions |
| **Impact if unsolved** | Quantify or describe the cost of inaction |
| **Why unsolved** | Technical, behavioral, or systemic barriers |

### Exercise 2: 11-Star Experience Ladder

For THIS specific feature, describe star levels 1, 3, 5, 7, 9, 11. Identify realistic target for current phase.

See `references/11-star-framework.md` for the full framework.

Output: Table + "**Target Star Level:** {N} — {rationale}"

### Exercise 3: Positioning Statement

Geoffrey Moore's framework:

> "For [target users], who [need/pain], [product/feature] is a [category] that [key benefit]. Unlike [competitors], it [differentiator]."

- Pull target users from persona files
- Include "current manual process" as a competitor if no direct competitor exists

### Exercise 4: Product Principles

Define 3-5 guardrails for this feature:

| Principle | Description | Following It | Violating It |
|-----------|-------------|-------------|-------------|
| e.g., "Offline-first" | Works without internet | Auto-sync when connected | Require internet for core flow |

### Exercise 5: Success Vision

Answer in 2-3 paragraph narrative:
- **Done well in 6 months** — Describe the ideal outcome
- **Behavior change expected** — How will users act differently?
- **Kill criteria** — What evidence would make us kill this feature?

## Output Format

```markdown
# Product Thinking Brief — {Feature Name}

**Date:** {DD-MM-YYYY}
**Author:** [your name]

## 1. Problem Statement
[table from Exercise 1]

## 2. 11-Star Experience
[table from Exercise 2]
**Target Star Level:** {N} — {rationale}

## 3. Positioning Statement
> For [target users], who [need/pain]...

## 4. Product Principles
[table from Exercise 4]

## 5. Success Vision
[narrative from Exercise 5]

## Next Step
Use this brief as input for your PRD/spec writing skill.
```

## Anti-Patterns

- Don't skip the problem statement — it's the foundation
- Don't set target star level above 7 for early phases — be realistic
- Don't write generic principles — they should be specific enough to be falsifiable
- Don't skip kill criteria — knowing when to stop is as important as knowing what to build

## Quality Checklist

- [ ] Problem statement has evidence, not just assertions
- [ ] 11-star ladder is specific to THIS feature, not generic
- [ ] Positioning statement names a real competitor or current process
- [ ] Principles are falsifiable (you can tell when they're violated)
- [ ] Kill criteria are defined
