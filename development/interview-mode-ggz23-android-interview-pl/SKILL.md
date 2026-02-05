---
name: interview-mode
description: Ensures proper requirements clarification before implementing features. Activates when asked to implement, build, create, or add features during what appears to be an interview or timed coding exercise.
---

# Interview Mode

When implementing features during an interview, ALWAYS clarify requirements BEFORE writing any code.

## Before Writing Code

1. **Identify Ambiguities**
   - What's explicitly in scope?
   - What's explicitly out of scope?
   - What edge cases need handling?

2. **Ask Clarifying Questions**
   Use AskUserQuestion with specific options:
   - Empty states: How to display when no data?
   - Error states: How to handle failures?
   - Loading states: Show spinner, skeleton, or nothing?
   - Validation: What rules apply to inputs?
   - Success criteria: What defines "done"?

3. **Confirm Understanding**
   Before coding, summarize:
   - What will be built
   - What edge cases will be handled
   - What is out of scope

## Question Format

Use specific options, not open-ended questions:

**Good:**
```
How should empty state be handled?
- Show illustration with message
- Show text message only
- Hide the section
```

**Bad:**
```
What should happen when there's no data?
```

## Why This Matters

- Shows communication skills
- Prevents wasted effort on wrong approach
- Demonstrates systematic thinking
- Catches misunderstandings early
