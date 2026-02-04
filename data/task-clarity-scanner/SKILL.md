---
name: task-clarity-scanner
description: Scans daily notes using Personal Kanban structure. Clarifies tasks, manages Today's 3 vs Ready, flags stale items, and helps swap between columns. Use when reviewing todos, scanning task lists, or managing your Kanban board.
allowed-tools: Read, Glob, Grep, Edit, Write, AskUserQuestion
---

# Task Clarity Scanner

## What This Does
Scans your daily note, identifies unclear or vague tasks, manages the Personal Kanban flow (Today's 3 ↔ Ready), flags stale items, and updates the file once you approve changes.

## When to Use
- "Scan my tasks"
- "Review my daily note"
- "Clarify my todos"
- "Check my task list for today"
- "What can you help me with today?"
- "Swap tasks" / "Update my Today's 3"

## Default Daily Note Location

Ed's daily notes live in Obsidian at:
```
/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md
```

When invoked without a specific file, check today's date and look for that file automatically.

## Daily Note Structure (Personal Kanban)

The daily note has this structure:
```markdown
## Ship This = Win Day
[Single focus - WIP limit 1]

## Today's 3
[Active work - pulled from Ready, WIP limit 3]

## Ready
[Backlog - all carried-forward tasks live here]

## Waiting For
[Blocked/delegated items with dates]

## Done Today
[Completed items]

## Captures
[Links to docs created today]

## Scratch
[Quick notes]
```

## Instructions

This skill uses the **Batch Pattern** - clarify all tasks first, then execute work.

**Note:** If you need to triage mobile captures first, use the `daily-review` agent which
runs inbox-triage before this skill.

---

### PASS 0: Kanban Health Check

**Before clarifying tasks, assess the board:**

1. **Count Today's 3** - Are there exactly 3 tasks? More? Fewer?
2. **Check for stale items** - Any tasks marked `[STALE]`?
3. **Review Ready size** - Is the backlog growing out of control?

Report findings:
```
## Board Status
- Today's 3: [N] tasks (target: 3)
- Ready: [N] tasks
- Stale items: [N] (rolling 3+ days)
- Waiting For: [N] blocked items
```

If Today's 3 has more than 3 items, offer to help prioritize.
If stale items exist, flag them for decision (do, delegate, drop).

---

### PASS 1: Clarify (One by One)

**Step 1: Read the Daily Note**
If no file specified, use today's date to find the daily note in the Zettelkasten folder.
Look for tasks in `## Today's 3` and `## Ready` sections.

**Step 2: Quick Triage**
Briefly categorize tasks:
- **Clear** - Ready to act on
- **Unclear** - Needs clarification
- **Stale** - Rolling 3+ days, needs decision
- **Done** - Already completed, can skip

**Step 3: Clarify One at a Time**
For each unclear task, present it individually (NOT a wall of text):

```
**Task:** "[the task]"

- **Issue:** [what's unclear]
- **Suggested rewrite:** "[agentic-ready version]"
- **What's needed:** [missing context]
```

Then ask ONE question with options:
1. **Clarify** - "Here's what I mean: [context]"
2. **Accept rewrite** - Use the suggested version
3. **Skip** - Leave as-is for now
4. **Someday/Maybe** - Park it with #someday tag
5. **Create project file** - Start a living doc for this task
6. **Move to Ready** - Not for today, but keep visible

Move to the next task after each response. Keep momentum.

**Step 3a: Stale Item Handling**
For tasks marked `[STALE]`:

```
**Stale Task:** "[STALE] [task text] (MM-DD)"
This has been rolling for [N] days.

Options:
1. **Do it now** - Move to Today's 3, commit to finishing
2. **Delegate** - Move to Waiting For with context
3. **Drop** - Remove entirely (it's not happening)
4. **Reframe** - Break into smaller pieces
5. **Someday** - Park with #someday tag
```

**Step 3b: Project File Creation**
When user selects "Create project file":

1. **Create in Obsidian Zettelkasten** at:
   `/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/PROJECT - [Task Name].md`

2. **Seed the file** with this template:
```markdown
---
type: project
status: planning
created: YYYY-MM-DD
linked-from: [[YYYY-MM-DD]]
---
# PROJECT: [Task Name]

## What We're Building
[One paragraph describing the goal and why it matters]

## Constraints & Scope
- In scope: ...
- Out of scope: ...
- Dependencies: ...

## Context Gathered
[Brainstorming notes, research findings, decisions made so far]

## Steps (when ready)
- [ ] Step 1
- [ ] Step 2

## Done State
[How we know this is complete]

## Open Questions
- [ ] Question 1
```

3. **Update daily note** - Replace original task with:
   `- [ ] [[PROJECT - Task Name]] - [brief description]`

4. **Offer to continue brainstorming** in the project file right now

**Step 4: Rewrite Principles**
When suggesting rewrites:
- State the specific action
- Include context needed
- Define the done state
- Make it agent-handoff ready
- **Include URLs/links** so tasks are self-contained
- **Preserve date suffix** - Keep `(MM-DD)` for staleness tracking

Example:
- Before: "Make Google Drive AI Ready"
- After: "Organize Google Drive for AI access: Create 'AI-Ready' folder, move key docs, document what each folder contains (01-04)"

**Step 4b: Flag Task Dependencies**
While clarifying, watch for blocking relationships:
```
- [ ] Convert project to skill ← Do first
  - [ ] Upload skill ZIP ← Blocked by above
```
Suggest marking blocked items in Waiting For section.

**Step 4c: Surfaced Tasks**
Clarifying one task often surfaces additional tasks. Track these as you go:
- New research needed
- Dependencies discovered
- Related updates required

These go to the Ready section when updating the file.

**Step 4d: Final Check**
Before moving to PASS 2, ask: **"Did we miss anything?"**

---

### PASS 1.5: Kanban Swaps (Optional)

If user wants to adjust Today's 3:

**Swap Interface:**
```
## Current Today's 3:
1. [Task A]
2. [Task B]
3. [Task C]

## Ready (available to pull):
1. [Task D]
2. [Task E]
3. [Task F]

What would you like to do?
- Swap: "swap 2 with D" - Replace Task B with Task D
- Add: "add E" - Pull Task E into Today's 3 (if under limit)
- Remove: "remove 1" - Move Task A back to Ready
- Done: "done 2" - Mark Task B complete, move to Done Today
```

Apply changes and confirm.

---

### PASS 2: Update the File

**Step 5: Batch the Changes**
After all tasks are clarified, summarize:
```
Ready to update your daily note:

## Today's 3 Changes:
- [Task moved in from Ready]
- [Task rewritten]

## Ready Changes:
- Task 1: [original] → [rewrite]
- Task 2: Skipped
- Task 3: → Someday/Maybe (#someday added)

## Stale Items:
- [Task] → Dropped
- [Task] → Moved to Waiting For

## New Tasks (surfaced):
- [New task discovered]
```

Get final approval before making edits.

**Step 6: Apply Edits**
- Use Edit tool to modify the original file
- Keep tasks in their proper sections (Today's 3 vs Ready)
- Move completed items to Done Today
- Move blocked items to Waiting For
- Add #someday tag for parked items
- Preserve all other content exactly
- Confirm: "Updated [N] tasks."

---

### PASS 3: Execute (Future)

**Step 7: Spin Up Agents**
For tasks marked "Ready to Go", offer to spin up agents:
```
These tasks are ready for agents:
- [task 1] - I can do this now
- [task 2] - Needs a research agent
- [task 3] - I can do this now

Want me to start working on these?
```

Execute approved tasks, report back when done.

## Guidelines

1. **Respect the Kanban structure** - Today's 3 = active work, Ready = backlog
2. **Don't over-engineer** - A slightly vague task that's obvious to Ed doesn't need rewriting
3. **Preserve voice** - Rewrites should sound like Ed, not corporate jargon
4. **Flag unknowns honestly** - If you don't know what something means, say so
5. **Suggest, don't assume** - Always get approval before modifying
6. **Keep the human in the loop** - Help Ed move faster, don't take over
7. **Preserve date suffixes** - The `(MM-DD)` format enables staleness tracking

## The Project File Pattern

For tasks that are too big to clarify inline, create a project file instead:
- The file is a living document that grows over sessions
- Daily note links to the project file (keeps it visible)
- When ready to execute, the project file IS the spec
- If parked for 1+ week, move to [[Someday-Maybe]] file

**When to suggest a project file:**
- Task involves multiple sub-tasks
- Needs research before execution
- Will take multiple sessions to complete
- Has dependencies on other work
- User says "let me think about this"

## Research Task Pattern

Research tasks have a distinct completion format:

**Format:**
```
- [x] ~~[Research Topic]~~ → **Finding:** [Summary]. See [[Document Name]]
```

**Ultrathink Bundling:**
When you see 3+ related research tasks, suggest:
"These research tasks are related and could run in parallel. Consider bundling as 'Ultrathink - [Topic] Research YYYY-MM-DD'"

## Examples

### Input (from daily note):
```
## Today's 3
- [ ] Review PR for auth changes (01-02)
- [ ] [STALE] Fix the login bug (12-30)
- [ ] Write newsletter intro

## Ready
- [ ] Convert Offer Diamond to skill (01-03)
- [ ] Set up Gmail App Password (01-01)
- [ ] Research API options
```

### Output (report):
```
## Board Status
- Today's 3: 3 tasks (target: 3) ✓
- Ready: 3 tasks
- Stale items: 1 (Fix the login bug - 5 days)
- Waiting For: 0

## Needs Attention

### Stale Item
**Task:** "[STALE] Fix the login bug (12-30)"
Rolling for 5 days. Decision needed:
1. Do it now
2. Delegate
3. Drop
4. Reframe
5. Someday

### Unclear Task
**Task:** "Write newsletter intro"
- Issue: Which newsletter? What's the topic?
- Suggested rewrite: "Write intro for LBR article on [topic] - 2-3 sentences, hook + promise (01-04)"
- What's needed: Article topic and angle

### Ready to Go
- "Review PR for auth changes" - Clear, actionable
- "Convert Offer Diamond to skill" - Clear process exists
```
