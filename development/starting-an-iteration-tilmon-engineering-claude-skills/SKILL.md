---
name: starting-an-iteration
description: Use when beginning a new conversation to work on an open-ended goal, loading context from previous iterations through iteration journals
---

# Starting an Iteration

## Overview

Begin a new iteration for an open-ended goal by loading context from previous iterations, setting up the workspace, and preparing to continue progress.

**Core principle:** Each conversation is one iteration. Load recent state, understand where you left off, continue the journey.

## When to Use

Use this skill when:
- User runs `/start-iteration` command
- Beginning work on an ongoing open-ended goal
- Need to load context from previous conversation sessions

**DO NOT use for:**
- Closed goals with definition of done (use ed3d-superpowers workflow instead)
- First-time brainstorming (use brainstorming skill first)
- One-off tasks that don't need iteration tracking

## Quick Reference

| Step | Action | Tool/Agent |
|------|--------|------------|
| 1. Detect goal | Check for autonomy directory | Glob |
| 2. Load recent context | Read last 3-5 iterations | Task (journal-reader) |
| 3. Load older context | Summarize if >5 iterations | Task (journal-summarizer) |
| 4. Present state | Show context to user | Direct output |
| 5. Create journal | Write initial journal entry | Write |
| 6. Ready to work | Create TodoWrite tracker | TodoWrite |

## Process

### Step 1: Detect Existing Goal

Check if a goal already exists in the current project:

```bash
# Use Glob to check for autonomy directory
pattern: "autonomy/*/goal.md"
```

**If goal.md found:**
- Extract goal name from directory path
- Proceed to Step 2 (Load Recent Context)

**If no goal found:**
```
"No autonomy goal found in this project.

Use `/create-goal` to set up a new open-ended goal first, then run `/start-iteration` to begin work."
```
Stop here - cannot start iteration without a goal.

### Step 2: Load Recent Context

For existing goals, load context from recent iterations:

1. **Count iterations:**
   ```bash
   # Use Glob to find iteration files
   pattern: "autonomy/[goal-name]/iteration-*.md"
   ```

2. **Determine iteration number:**
   - Count existing files: N
   - This iteration will be: N+1

3. **Dispatch journal-reader agent:**
   ```
   Task tool with subagent_type: "autonomy:journal-reader"
   Prompt: "Read last 3-5 iterations for goal '[goal-name]' and extract:
           - Current state
           - Open blockers and questions
           - Recent progress
           - Key metrics
           - Recommended next steps"
   Model: haiku
   ```

4. **Wait for agent response** with structured context

### Step 3: Load Older Context (if >5 iterations)

If more than 5 iterations exist, summarize older ones:

1. **Check if summary.md exists:**
   ```bash
   # Use Read to check
   file: "autonomy/[goal-name]/summary.md"
   ```

2. **Determine what needs summarizing:**
   - If summary.md exists: Check which iterations it covers
   - If summary.md missing OR outdated: Summarize iterations 1 through (N-5)

3. **Dispatch journal-summarizer agent:**
   ```
   Task tool with subagent_type: "autonomy:journal-summarizer"
   Prompt: "Summarize iterations [range] for goal '[goal-name]'.
           Extract major initiatives, persistent blockers, key learnings,
           strategic pivots, and metric trends. Update summary.md."
   Model: haiku
   ```

4. **Wait for agent to write summary.md**

### Step 4: Present State to User

Combine findings from journal-reader (and summary if applicable):

```markdown
**Iteration [N] started for goal: [goal-name]**

## Current State
[From journal-reader: most recent ending state]

## Recent Progress (Last 3-5 Iterations)
[Condensed summary of what was accomplished]

## Open Blockers
- [Blocker 1]
- [Blocker 2]

## Open Questions
- [Question 1]
- [Question 2]

## Key Metrics
- [Metric]: [Current value] (was [previous value])

## Recommended Next Steps
[From previous iteration's suggestions]

---

**Ready to continue. What should we work on this iteration?**
```

### Step 5: Create Initial Journal Entry

Before beginning work, create the journal file for this iteration:

1. **Determine iteration number and filename:**
   - Count: N existing iterations
   - This iteration: N+1
   - Filename: `iteration-NNNN-YYYY-MM-DD.md` (today's date)

2. **Prompt user for iteration intention:**
   ```
   "What do you want to accomplish this iteration?

   This helps keep us honest about the goal. We'll check against this intention when ending the iteration."
   ```

3. **Write initial journal entry:**

```markdown
# Iteration NNNN - YYYY-MM-DD

## Beginning State
[From journal-reader output or user context:
- Current progress summary
- Known blockers from previous iteration
- Open questions being addressed
- Current metric values if tracked]

## Iteration Intention
[User's stated intention for this iteration]

## Work Performed

### Skills & Workflows Used
[Will be filled during checkpoint or ending]

### Key Decisions Made
[Will be filled during checkpoint or ending]

### Artifacts Created/Modified
[Will be filled during checkpoint or ending]

### External Context Gathered
[Will be filled during checkpoint or ending]

### Reasoning & Strategy Changes
[Will be filled during checkpoint or ending]

### Blockers Encountered
[Will be filled during checkpoint or ending]

### Open Questions
[Will be filled during checkpoint or ending]

## Ending State
[Will be filled when ending iteration]

## Iteration Metadata
[Will be filled when ending iteration]
```

4. **Write file** to: `autonomy/[goal-name]/iteration-NNNN-YYYY-MM-DD.md`

### Step 6: Ready to Work

1. **Create TodoWrite tracker** for current iteration work:
   ```
   TodoWrite with todos:
   - [First task based on next steps or user intention]
   - [Additional tasks as identified]
   ```

2. **Begin work** on the goal

## Important Notes

### Iteration Numbering

- Use 4-digit zero-padded numbers: `0001`, `0002`, ..., `0999`, `1000`
- Format: `iteration-NNNN-YYYY-MM-DD.md`
- Date is when iteration occurred (today)

### Context Loading Strategy

- **Iterations 1-5:** Load all in detail with journal-reader
- **Iterations 6+:** Load last 3-5 in detail, older iterations via summary
- **Update summary** every 5 iterations (5, 10, 15, 20, etc.)

### Agent Delegation

**Always use Task tool** to dispatch journal-reader and journal-summarizer:
- Prevents context pollution in main conversation
- Uses Haiku model for efficiency
- Returns structured findings

**Never read journals yourself** - always delegate to agents.

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "I'll quickly read the journals myself" | NO. Always dispatch agents. Journals can be large. |
| "User goal seems closed-ended, but I'll use autonomy anyway" | NO. Autonomy is for open-ended goals only. |
| "I'll skip loading older iterations to save time" | NO. Context is critical. Always load per strategy. |
| "I'll create summary.md myself" | NO. Dispatch journal-summarizer agent. |
| "Goal exists, so I'll skip asking user what to work on" | NO. Always present state and ask for direction. |

## After Starting

Once iteration is started:
- Journal file created with Beginning State and Intention
- Work normally on the goal using appropriate skills and workflows
- Track progress mentally or with TodoWrite
- Use `/checkpoint-iteration` to save progress before compaction or at interim points
- When ready to conclude, use `/end-iteration` to finalize journal entry
