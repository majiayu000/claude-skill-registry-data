---
name: convo
description: Complete conversation lifecycle management - start (understanding & alignment), capture (mid-conversation context), and exit (debrief & improvement). Use automatically at conversation boundaries and checkpoints.
---

# Conversation Lifecycle

> Manages the full conversation lifecycle: start, capture, and exit.

---

## Overview

| Phase | When | Purpose |
|-------|------|---------|
| **Start** | Beginning of conversation | Establish understanding and alignment |
| **Capture** | Mid-conversation | Save context for continuity |
| **Exit** | End of conversation | Debrief, feedback, and improvement |

---

# Part 1: Start

> Establishes understanding and alignment before diving into execution.

## When to Start

- **Automatically** at the start of every new conversation
- When user explicitly says "convo-start"
- When topic shifts significantly mid-conversation

## Phase 1: Understanding

**Actions**:
1. **Read the request carefully**
2. **Identify**:
   - What type of work is this? (feature, spec review, planning, research, fix)
   - Which agents/patterns are relevant?
   - What context do I need?
3. **Gather initial context** (follow research-priority pattern)

**Research Priority Pattern**:
1. Repo docs (CLAUDE.md, README, existing specs)
2. Linear/issue tracker (if referenced)
3. Ask user for clarification
4. External sources (last resort)

## Phase 2: Alignment

### 1. State Your Understanding
```markdown
I understand you want to [specific goal].

This involves:
- [Scope item 1]
- [Scope item 2]
```

### 2. Propose Execution Plan
```markdown
Here's my approach:
1. [Step 1]
2. [Step 2]
3. [Step 3]

I'll use:
- [Relevant agent/pattern]
- [Another relevant pattern]
```

### 3. Wait for Confirmation
Do NOT proceed until user confirms or corrects the plan.

## Quick Templates

**For simple tasks:**
```markdown
Got it - you want [X]. I'll [approach]. Sound good?
```

**For complex tasks:**
```markdown
Let me make sure I understand:

**Goal**: [What you want to achieve]
**Scope**: [What's included/excluded]
**Approach**: [How I'll tackle it]
**Output**: [What you'll get]

Anything to adjust before I start?
```

## When to Skip Full Alignment

**Skip when**:
- Simple question requiring quick answer
- User explicitly says "just do X"
- Continuing prior conversation with established context

**Never skip when**:
- Creating or modifying documents/code
- Work will take significant time
- Multiple approaches are possible
- User's intent is unclear

---

# Part 2: Capture

> Saves context mid-conversation for continuity and handoff.

## When to Capture

### Automatic Triggers

1. **Significant decision made** - Architecture choice, approach selected, scope change
2. **Large work completed** - Document created, major code changes, phase finished
3. **Topic shift detected** - Before switching to new topic
4. **Natural breakpoint** - Before user goes to meeting, logical pause

### On Request

- User asks "save where we are"
- User needs to leave but wants to continue later
- Handoff to another person/session

## What to Capture

| Element | Why It Matters |
|---------|----------------|
| **Current state** | Where we are right now |
| **Decisions made** | What was decided and why |
| **Files changed** | What was created/modified |
| **Next steps** | What comes next |

## Capture Formats

### Inline Capture (Quick)

```markdown
---
**Checkpoint**: [Brief description]

**Status**: [Current state of work]
**Just completed**: [What was done]
**Next**: [What's queued]
---
```

### Context File (Detailed)

Create `convo-captures/YYYY-MM-DD-HHMM-topic.md`:

```markdown
# Context Capture: [Topic]

**Date**: YYYY-MM-DD HH:MM
**Status**: In Progress / Paused / Blocked

## Current State
[Where we are in the work]

## Decisions Made
| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| [Choice] | [Why] | [Other options] |

## Files Changed
**Created**: [list]
**Modified**: [list]

## Next Steps
1. [ ] [Immediate next step]
2. [ ] [Following step]

## To Resume
[Instructions for picking this back up]
```

---

# Part 3: Exit

> Wraps up conversations with debrief, feedback, and knowledge capture.

## Triggers

- User says "we're done", "that's it", "looks good"
- Conversation naturally concluding
- User explicitly requests exit/debrief
- Topic drift suggests starting fresh

## Exit Protocol

### Step 1: Review

```markdown
Let me review our conversation:

**Original goal**: [State the goal]

**What we accomplished**:
- [Outcome 1]
- [Outcome 2]

**Files created/modified**:
- `path/file.md` - [Brief description]
```

### Step 2: Tasks Remaining

```markdown
**Tasks Remaining**:

For this effort:
- [ ] [Remaining task 1]
- [ ] [Remaining task 2]
```

### Step 3: Ask for Feedback

```markdown
**Your feedback**:

1. What worked well in this conversation?
2. What would you have liked to see improved?
3. Were there moments where I was unclear or off-track?
```

### Step 4: Propose Changes

After receiving feedback:

```markdown
**Based on our conversation, I propose these changes**:

1. [File path]: [Specific change]
2. [File path]: [Specific change]

Should I make these changes?
```

### Step 5: Create Convo-Exit Document

**File**: `convo-exits/YYYY-MM-DD-HHMM-topic.md`

```markdown
# Conversation Exit: [Topic]

**Date**: YYYY-MM-DD HH:MM
**Repo**: [which repo(s) were involved]

## Original Goal
[What we set out to do]

## Outcomes
**Files Created**: [list]
**Files Modified**: [list]
**Decisions Made**: [list]

## User Feedback
**What worked well**: [feedback]
**What could improve**: [feedback]

## Improvements Made
- [ ] [Change 1] - [Status]

## Next Steps
**Immediate**: [list]
**Future**: [list]
```

### Step 6: Activity Log Update

If brain repo has `personal/activity-log.md` AND significant work was done:

```markdown
## YYYY-MM-DD HH:MM - [Topic]

**What I accomplished**:
- [Accomplishment 1]
- [Accomplishment 2]

**Repos affected**: [list]
**Related**: `convo-exits/YYYY-MM-DD-HHMM-topic.md`
```

---

# Anti-patterns

| Wrong | Right |
|-------|-------|
| Immediately starting work | State understanding first, get confirmation |
| Acting on assumptions | Explicitly state assumptions, ask for confirmation |
| No record of decisions | Capture decisions with rationale |
| Context dump without resume instructions | Clear "To continue, do X" instructions |
| Skipping debrief | Always offer exit protocol for significant work |

---

# Success Metrics

## Start
- [ ] User never confused about what you're doing
- [ ] Plan is specific enough to evaluate
- [ ] User can correct misunderstandings early

## Capture
- [ ] Can resume work without context loss
- [ ] Can hand off to someone else smoothly
- [ ] Past decisions are understandable

## Exit
- [ ] Clear record of what was accomplished
- [ ] Learnings captured for future
- [ ] Improvements made to the system
- [ ] User feels heard and in control
