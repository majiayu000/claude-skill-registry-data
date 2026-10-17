---
name: bragi-tradeoff-communication
description: Advise on how to frame options, risks, and decisions so users can make informed choices.
---

# Trade-off Communication

## Purpose

Advise on how to present options and decisions clearly when there is no single right answer. The goal is to equip the user with enough understanding to make an informed decision without overwhelming them.

## When to Use

- When multiple implementation paths exist with different trade-offs.
- When the user must choose between speed, quality, cost, or scope.
- When presenting a recommendation that involves trade-offs.
- When explaining why a preferred approach was not chosen.

## Workflow

1. **Identify the decision to be made.**
   - What is the choice the user must make?
   - What are the viable options? (If more than 3-4, group or prioritize.)
   - What criteria matter most? (cost, time, quality, maintainability, risk)

2. **Frame each option neutrally.**
   - Describe what each option *is*, not just what it sacrifices.
   - State the trade-off explicitly: "Option A is faster to build but harder to maintain."
   - Avoid framing one option as the obvious default unless it truly is.

3. **Structure the comparison.**
   - Option table (rows: options, columns: criteria) — best for 2-4 options with clear dimensions.
   - Narrative with ranking — best when one option is clearly preferred.
   - Decision tree — best when choices cascade.

4. **Make a recommendation and highlight risks.**
   - If one option is clearly better, say so and explain why.
   - Highlight key risks for each option: severity, impact, and known unknowns.

5. **End with a clear ask.**
   - What does the user need to decide?
   - What happens if they don't respond?
   - Offer to research further if more information is needed.

## Quality Criteria

- All viable options are presented (not just the one preferred).
- Trade-offs are explicit, not buried.
- The user can make a decision without asking for additional clarification.
- Risks are called out, not glossed over.

## Anti-Patterns

- **False choice**: Presenting options where only one is actually viable.
- **Analysis paralysis**: Presenting too many options or too much detail.
- **Buried recommendation**: Hiding the recommended path in a wall of text.
- **Risk minimization**: Downplaying risks to steer the user toward a preferred option.
