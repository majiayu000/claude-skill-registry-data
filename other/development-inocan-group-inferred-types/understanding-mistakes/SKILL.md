---
name: understanding-mistakes
description: Use when user says something went wrong, AI did Y instead of X, or wants to understand why a deviation happened. Manually invoked post-mortem analysis.
---

# Understanding Mistakes

## Overview

Analyze why you deviated from expected behavior. Produce honest self-reflection and document learnings to prevent the same mistake twice.

## Process

**1. Gather Context**

If the issue isn't clear, ask the user:
- "What did you expect to happen?"
- "What actually happened?"

**2. Self-Reflect**

Analyze your own decision-making honestly:
- What information did I have access to?
- What assumptions did I make?
- Why did I choose this approach over the expected one?
- Did I ignore explicit guidance? Why?

**3. Identify the Gap**

Determine root cause:
- Missing information in the instruction?
- Ambiguous wording I interpreted differently?
- Over-engineering instinct?
- Default behavior overriding explicit guidance?
- Assumed I knew better?

**4. Write Learning Document**

Create `docs/learnings/YYYY-MM-DD-<topic>.md` with this structure:

```markdown
# Understanding Mistake: <brief title>

**Date:** YYYY-MM-DD
**Context:** <what task/skill was being executed>

## What Was Requested
<The original instruction or expected behavior>

## What Happened Instead
<The actual behavior/deviation>

## Root Cause Analysis
<Why the AI made this choice>
- What information was available
- What assumptions were made
- What reasoning led to the deviation

## Information Gap
<What was missing or unclear>
- Missing context?
- Ambiguous wording?
- Conflicting signals?

## Prevention
<How to avoid this in the future>
- Suggested instruction improvements
- Patterns to watch for
```

## Principles

| Principle | Meaning |
|-----------|---------|
| Honest self-reflection | No excuses, no defensiveness. Genuinely analyze what happened. |
| Actionable insights | Prevention section must be concrete and usable, not vague. |
| No blame, just learning | Investigative tone. Goal is improving the system. |
| Pattern recognition | These docs build a knowledge base. Look for recurring issues. |

## Common Root Causes

| Pattern | Example |
|---------|---------|
| Over-engineering | Added filters/complexity not in the spec |
| Assumed context | Thought I knew what was needed without checking |
| Ignored explicit guidance | Skill had exact code, I wrote my own |
| Ambiguous instruction | Multiple valid interpretations, picked wrong one |
| Default behavior | Fell back to training patterns instead of following instruction |

## Red Flags in Self-Analysis

If you find yourself thinking:
- "But my way was better" → You ignored explicit guidance
- "I thought it was obvious" → You made assumptions
- "The instruction didn't say NOT to" → You added unrequested complexity
- "I was trying to be helpful" → Over-engineering

These are the insights to document, not excuses to make.
