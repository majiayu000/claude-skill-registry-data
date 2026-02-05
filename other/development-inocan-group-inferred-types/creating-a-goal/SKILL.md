---
name: creating-a-goal
description: Use when setting up a new open-ended goal for autonomy tracking, before starting the first iteration
---

# Creating a Goal

## Overview

Set up a new open-ended goal by creating the directory structure, writing the goal definition, and preparing for iteration tracking.

**Core principle:** One-time setup. Run this once per goal, then use starting-an-iteration for all subsequent work.

## When to Use

Use this skill when:
- User runs `/create-goal` command
- Starting a brand new open-ended goal
- No existing autonomy goal directory exists

**DO NOT use for:**
- Continuing existing goal (use starting-an-iteration instead)
- Closed goals with definition of done (use ed3d-superpowers workflow)

## Quick Reference

| Step | Action | Tool |
|------|--------|------|
| 1. Verify no existing goal | Check for autonomy directory | Glob |
| 2. Get goal details | Prompt user for goal statement | User interaction |
| 3. Generate directory name | Convert to kebab-case | Manual |
| 4. Create structure | Make directory | Bash |
| 5. Write goal.md | Document goal definition | Write |
| 6. Announce ready | Tell user to run /start-iteration | Direct output |

## Process

### Step 1: Verify No Existing Goal

Check that no goal already exists:

```bash
# Use Glob to check
pattern: "autonomy/*/goal.md"
```

**If goal.md found:**
```
"An autonomy goal already exists: [goal-name]
Use '/start-iteration' to continue working on this goal.
If you want to create a different goal, first archive or remove the existing one."
```
Stop here - don't create duplicate goals.

**If no goal found:**
Proceed to Step 2.

### Step 2: Get Goal Details from User

Prompt user for goal information:

```
"What open-ended goal would you like to pursue?

This should be a goal that never truly completes - ongoing optimization, continuous improvement, or iterative exploration.

Examples:
- Maximize monthly recurring revenue
- Improve developer productivity
- Reduce customer churn
- Optimize application performance

Your goal:"
```

**User provides goal statement.**

Then ask about success criteria:

```
"What metrics or indicators should we track for this goal?

Since this is open-ended, there's no 'done' state, but we can track progress.

Examples:
- MRR: Starting at $45k/month
- Churn rate: Currently 13%
- Build time: Currently 5 minutes

Your metrics (or 'none' if not applicable):"
```

**User provides metrics or indicates none.**

### Step 3: Generate Directory Name

Convert goal statement to kebab-case:

**Rules:**
- Lowercase all characters
- Replace spaces with hyphens
- Remove special characters
- Keep concise (max 50 chars)

**Examples:**
- "Maximize monthly recurring revenue" → `maximize-monthly-recurring-revenue`
- "Improve developer productivity" → `improve-developer-productivity`
- "Reduce customer churn by 50%" → `reduce-customer-churn`

### Step 4: Create Directory Structure

Create the goal directory:

```bash
# Use Bash to create directory
mkdir -p autonomy/[goal-name]
```

### Step 5: Write goal.md

Create the goal definition file:

```markdown
# Goal: [Original goal statement]

## Goal Statement
[Full description from user]

## Success Criteria
[Open-ended - note that this has no completion state]

## Metrics to Track
[If user provided metrics:]
- [Metric 1]: [Starting value]
- [Metric 2]: [Starting value]

[If no metrics:]
- No specific metrics defined
- Progress will be qualitative

## Current Status
Active - Ready for iteration 1

## Started
[Current date: YYYY-MM-DD]

## Notes
[Any additional context from user]
```

Write this file to: `autonomy/[goal-name]/goal.md`

### Step 6: Announce Ready

Inform user that goal is created:

```markdown
**Goal created: [goal-name]**

Directory: `autonomy/[goal-name]/`
Goal definition: `autonomy/[goal-name]/goal.md`

---

**Next step:** Run `/start-iteration` to begin the first iteration.

This will:
- Create iteration-0001-[today's date].md
- Set up workspace for working toward the goal
- Track progress in iteration journals
```

## Important Notes

### Single Goal Per Project

Currently, autonomy supports one goal per project directory:
- If goal.md exists, creation fails
- User must archive/remove existing goal to create new one
- Future enhancement could support multiple goals

### Goal Naming

Keep directory names:
- **Descriptive** but **concise**
- **Stable** (won't change over time)
- **Filesystem-safe** (kebab-case, no special chars)

### Open-Ended Requirement

Verify goal is truly open-ended:

**Good examples:**
- "Maximize X" - always can improve
- "Reduce Y" - continuous optimization
- "Improve Z" - never fully complete

**Bad examples:**
- "Build authentication system" - has done state (use ed3d-superpowers)
- "Fix bug #123" - has done state
- "Write documentation" - has done state

If user suggests closed goal, guide them:
```
"This goal seems to have a clear completion state. For goals with a definition of 'done',
consider using the ed3d-superpowers development workflow instead.

Autonomy is designed for never-ending optimization and improvement goals.

Would you like to reframe this as an open-ended goal, or would a different workflow be better?"
```

### Metrics Are Optional

Not all open-ended goals have quantifiable metrics:
- "Improve code quality" - may be qualitative
- "Increase team knowledge" - hard to measure
- "Enhance user experience" - subjective

Accept "none" or "qualitative" as valid answers.

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "I'll create goal even though one exists" | NO. One goal per project. Check first. |
| "User goal is closed-ended but I'll create anyway" | NO. Guide to appropriate workflow. |
| "I'll skip metrics prompt to save time" | NO. Always ask - user may have important metrics. |
| "Directory name can have spaces" | NO. Use kebab-case only. |
| "I'll start first iteration automatically" | NO. Let user run /start-iteration when ready. |

## After Creating

Once goal is created:
- goal.md exists with definition
- Directory ready for iteration journals
- User runs `/start-iteration` to begin work
- Iteration 1 will create first journal entry
