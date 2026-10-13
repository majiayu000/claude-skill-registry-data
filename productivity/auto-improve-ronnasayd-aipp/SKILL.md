---
name: auto-improve
description: >
  After completing any task, extract reusable rules from what worked and what failed. Produces output in the exact format used by agent.instructions.md (## Mandatory: Rules to Follow / ## Mandatory: Rules to Avoid). Trigger after a task finishes when the user asks for a retrospective, lessons learned, or rule extraction — or implicitly with phrases like "what did we learn", "what went wrong", "what should we avoid next time". Do NOT trigger mid-task or before execution completes.
argument-hint: "Optional: path to a task log, plan file, or description of the completed process. If not provided, the skill will analyze the current conversation history."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Task Retrospective

A skill for reflecting on completed tasks and converting experience into lasting rules.

The goal is simple: after finishing work, extract what was learned — both what went well and what failed — and encode that knowledge as concrete, actionable rules in the same format used by `agent.instructions.md`. This prevents repeating the same mistakes and reinforces effective patterns.

---

## When to use this skill

- Immediately after completing a task, feature, plan, or agent workflow
- When the user asks for a reflection, retrospective, or lessons learned
- When an agent wants to close a loop and capture institutional knowledge
- Proactively, at the end of any multi-step execution that involved meaningful decisions

---

## Process

### Step 1: Collect context

Gather the raw material for reflection. Use whatever is available:

- Current conversation history (decisions, corrections, feedback given by the user)
- Task/plan files if provided (e.g., `docs/agents/plans/*.md`, `tasks/todo.md`)
- Git diff or commit history if relevant
- Any error messages, failed attempts, or corrections made mid-task

If a file path was passed as argument, read it. If nothing was provided, analyze the conversation directly.

### Step 2: Identify decision events

Go through the execution timeline and identify discrete moments where a decision was made. For each one, note:

- **What was decided** — the action taken or approach chosen
- **Outcome** — did it work? Was it corrected? Did it cause rework?
- **Category** — Problem Understanding, Planning, Implementation, Communication, Tool Use, Verification, etc.

Focus on consequential decisions. Skip trivial steps.

### Step 3: Classify decisions

Separate into two groups:

**Correct decisions** — actions that led to good outcomes, saved time, or were confirmed by the user as the right approach. Ask: "Why did this work? What principle is this an example of?"

**Wrong decisions** — actions that caused errors, required rework, were rejected by the user, violated stated requirements, or wasted effort. Ask: "Why did this fail? What pattern should be avoided in the future?"

### Step 4: Generalize into rules

Avoid writing rules that are too specific to the current task. The best rules are transferable — they apply across many future tasks.

**Good rule:** "Always read the current file content before editing any section."
**Too specific:** "Always read `agent.instructions.md` before line 47 of that specific file."

For each identified pattern (both good and bad), write a single-line rule. Be direct and imperative. No justifications in the rule itself — just the actionable instruction.

### Step 5: Produce the retrospective report

Output a structured Markdown report using the template below. Never skip sections, even if a section has few items.

---

## Output template

```markdown
# Task Retrospective: <task name or brief description>

**Date:** <yyyy-mm-dd>
**Process evaluated:** <brief description of what was executed>

---

## Summary

<2-4 sentences describing what was done, what the main challenge was, and whether the overall outcome was good.>

---

## Decision Analysis

### Correct Decisions

| #   | Decision        | Category   | Why it worked              |
| --- | --------------- | ---------- | -------------------------- |
| 1   | <what was done> | <category> | <principle it illustrates> |

### Wrong Decisions

| #   | Decision        | Category   | Root cause      |
| --- | --------------- | ---------- | --------------- |
| 1   | <what was done> | <category> | <why it failed> |

---

## Extracted Rules

### Rules to Follow

- <Actionable rule 1>
- <Actionable rule 2>
- ...

### Rules to Avoid

- <Anti-pattern 1>
- <Anti-pattern 2>
- ...

---

## Proposed Update to agent.instructions.md

The following rules are ready to be appended to the relevant sections of `instructions/agent.instructions.md`:

**Add to ## Mandatory: Rules to Follow:**

- <new rule>

**Add to ## Mandatory: Rules to Avoid:**

- <new anti-pattern>
```

---

## Step 6: Offer to persist the rules

After presenting the report, ask the user:

> "Would you like me to append the new rules to `instructions/agent.instructions.md`? I'll add only the rules that don't already exist there."

If the user confirms:

1. Read the current content of `instructions/agent.instructions.md`
2. Identify which rules are truly new (avoid duplicates)
3. Append new rules under the appropriate sections (`## Mandatory: Rules to Follow` / `## Mandatory: Rules to Avoid`) using precise, surgical edits — no rewrites

---

## Quality guidelines for rules

A good rule is:

- **Imperative** — starts with a verb: "Always...", "Never...", "Read X before...", "Validate..."
- **Specific enough to act on** — not vague like "Be careful"
- **General enough to reuse** — not tied to one specific file or context
- **Honest** — derived from an actual failure or success, not hypothetical

Aim for 3–7 rules per section. More than that usually means some rules are redundant or too narrow.

---

## Decision categories (reference)

Use these when classifying decisions in Step 2:

| Category              | Examples                                                       |
| --------------------- | -------------------------------------------------------------- |
| Planning              | Breaking down tasks, defining scope, sequencing steps          |
| Problem Understanding | Reading requirements, asking clarifying questions              |
| Implementation        | Code choices, tool usage, file edits                           |
| Verification          | Testing, validating outputs, checking requirements             |
| Communication         | How information was presented to the user                      |
| Tool Use              | Choosing which tool to call, parameter correctness             |
| Scope Control         | Staying within requested boundaries, avoiding over-engineering |
| File Management       | Creating, editing, deleting files                              |
