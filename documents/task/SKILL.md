---
name: task
description: Create a living task doc from natural language. Use when you want to track work, capture a new project, or create a thinking log that accumulates context across sessions.
argument-hint: [task description]
---

# /task - Create a Living Task Doc

Create a task doc from natural language. A thinking log that accumulates context, decisions, and observations over time.

---

## What To Do

1. **Parse the request** — understand what work is being described
2. **Figure out metadata** — topic, tags, priority
3. **Write the file** — with the structure below
4. **Note the connection** — this doc is where `/wrap` updates and `/sync` captures link back to

---

## Task Doc Structure

```markdown
---
tags: [{tag1}, {tag2}]
priority: {P0|P1|P2|P3}
status: todo
created_date: {YYYY-MM-DD}
---

# {Title}

## WHAT

{Description — why this matters, context, what triggered this}

---

## WHO

{People involved — names, roles, current status}

---

## HOW

### Pending (Execute Next)
- [ ] {First action item}

### Completed (Append in order of completion)
<!-- Move items here when done — newest at bottom -->

---

## OBSERVATIONS (Cumulative)

*Patterns, friction, questions worth keeping — from you or your AI*

<!-- Add observations as they emerge across sessions -->

---

## SESSION INDEX

<!-- Pointers to captured sessions related to this work -->
<!-- Format: **Session N (YYYY-MM-DD)**: [filename] — one-liner of what happened -->

---
```

---

## Why This Structure

Most task trackers give you a title and a checkbox. This gives you a thinking log.

- **WHAT** isn't just a description — it's the WHY that keeps you oriented when you pick this up days later
- **HOW** splits pending from completed so you always know where you left off
- **OBSERVATIONS** is where the real value accumulates — patterns you noticed, friction you hit, questions that emerged
- **SESSION INDEX** links to your captured sessions so you can trace how the thinking evolved

## When a Task Is Done

Archive completed tasks to `tasks/_done/` to preserve the thinking. The task doc is a record of how you got somewhere — decisions, dead ends, observations. That's worth keeping even after the work is finished. `/wrap` handles this when you mark a task done.

---

## Skill Check (After Every Task Creation)

Quick scan: anything about this task creation that felt off or could be smoother?

- Was the WHAT section clear enough for future you?
- Did the structure feel right for this type of work?
- Was anything missing that you'd want next time you pick this up?

**If yes** → update this skill now. The improvement compounds.

**If no** → move on. Not every task teaches something.
