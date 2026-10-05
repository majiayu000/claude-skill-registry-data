---
name: ralph-wiggum
description: Iterative development loop for solving complex tasks through trial-and-error. Use when you need to "fix until passing", "optimize until metric reached", or "iterate until done".
---

# Ralph Wiggum Skill

This skill defines a disciplined iterative loop for solving stubborn problems.

## The Ralph Loop

When you enter a "Ralph Loop", you commit to the following process:

1.  **Define the Promise**: What exact state signals completion? (e.g., "All 5 tests pass", "Error log is empty").
2.  **Iterate**:
    -   **Action**: Attempt a fix or improvement.
    -   **Verification**: Run the verification command.
    -   **Observation**: Analyze the output.
3.  **Repeat**: Continue until the Promise is met or Max Iterations reached.

## When to Use

- "Keep trying to fix this bug until the tests pass."
- "Optimize this prompt until the score is > 80."
- "Refactor this module, ensuring no regressions."

## Workflow Template

Copy this into your `scratchpad.md` or keep it in your context to track progress.

```markdown
# Ralph Loop Tracking

**Goal**: [Describe Goal]
**Completion Promise**: [Exact condition to stop]
**Max Iterations**: [Number]

## Iteration 1
- **Plan**: [What to do]
- **Action**: [Tool call]
- **Result**: [Outcome]
- **Status**: [PASSED / FAILED / PROGRESS]

## Iteration 2
...
```

See [assets/loop_template.md](assets/loop_template.md) for a raw template.

## Principles

1.  **Iteration > Perfection**: Don't try to solve it all in one perfect shot. Try, fail, learn, retry.
2.  **Failures are Data**: Every error message is a clue. Read them carefully.
3.  **Self-Correction**: If a path isn't working, change direction. Don't repeat the same mistake.
