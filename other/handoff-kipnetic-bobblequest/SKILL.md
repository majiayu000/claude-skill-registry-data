---
name: handoff
description: >
  Create a handoff document when context is getting large or work needs to
  continue in a fresh conversation. Writes a structured handoff file to
  ~/docs/plans/handoffs/{date}/{name}.md and gives the user a copy-pastable
  message to start a new conversation with zero friction. Trigger: user says
  "handoff", "do handoff", "hand off", "context is getting large", or
  "continue in new conversation".
---

# Handoff Skill

## Purpose

When a conversation accumulates significant context and work needs to continue, create a structured handoff document that lets any agent — with zero prior context — pick up exactly where this conversation left off.

## When to Use

- User says "handoff", "do handoff", "hand off"
- User indicates context is getting large or wants to continue in a fresh conversation
- Agent recognizes the conversation is approaching context limits and suggests a handoff

## Handoff Procedure

### Step 1: Create the handoff directory

```
~/docs/plans/handoffs/{YYYY-MM-DD}/
```

Use today's date. Create the directory if it doesn't exist.

### Step 2: Write the handoff file

Path: `~/docs/plans/handoffs/{YYYY-MM-DD}/{meaningful-name}.md`

The `{meaningful-name}` should be a lowercase-hyphenated slug that describes the work (e.g., `nutraforge-auth-refactor`, `clickup-backlog-triage`, `neuromorphic-graph-design`).

Use this exact structure:

```markdown
# Handoff: {Title}

**Date:** {YYYY-MM-DD}
**Conversation scope:** {one-line summary of what the conversation covered}

---

## Goal & User Intent

{What the user set out to accomplish and why. Include the broader objective, not just the immediate task. Capture the user's framing and priorities.}

## What Was Done

{Bullet list of concrete accomplishments — files created/modified, PRs opened, tasks updated, decisions made, research completed. Be specific with file paths, task IDs, branch names, PR numbers.}

## Where We Are Now

{What is actively in progress right now. What state is the code/task/system in? What was the agent doing when the handoff was triggered?}

## What's Next

{Ordered list of the remaining work. Be specific enough that a new agent can execute without re-discovery.}

1. {Next immediate step}
2. {Following step}
3. ...

## Important Context & Gotchas

{Things that aren't obvious from the code or task alone. Include:
- Decisions made and WHY (especially non-obvious ones)
- Gotchas encountered (things that didn't work, surprising behavior)
- Constraints or requirements that aren't documented elsewhere
- Relevant ClickUp task IDs with current status
- Branch names, PR links, deployment state
- Any blockers or open questions for the user}

## Key Files & Locations

{Table or list of the most important files/paths touched or relevant to continuing the work.}

| File | Purpose |
|------|---------|
| {path} | {what it is / why it matters} |

---

_Handoff created from conversation on {YYYY-MM-DD}. Resume with the prompt below._
```

### Step 3: Provide the resume prompt

After writing the handoff file, present the user with a copy-pastable message inside a single code block. The message should look like this:

~~~
```
Continue from handoff: ~/docs/plans/handoffs/{YYYY-MM-DD}/{meaningful-name}.md

Read the handoff file above for full context. The short version: {one sentence summary of what we were doing and where we stopped}. Pick up from "{next immediate step from the What's Next section}".
```
~~~

The resume prompt must:
- Reference the handoff file path so the new agent reads it first
- Include a one-sentence summary so the user can verify it's correct before pasting
- Name the specific next step to eliminate ambiguity

### Step 4: Confirm to the user

Tell the user:
- The handoff file path
- The resume prompt (in a code block they can copy)
- That they can start a new conversation and paste the prompt

## Rules

- **No fluff.** The handoff file is a working document, not a narrative. Be direct and specific.
- **Paths, IDs, and names are mandatory.** A handoff that says "the config file" instead of `~/apps/api/src/config/auth.ts` is useless.
- **Capture WHY, not just WHAT.** Decisions without rationale force the next agent to re-derive or guess.
- **Include gotchas prominently.** If something was tried and didn't work, say so — don't let the next agent waste time rediscovering it.
- **ClickUp tasks stay updated.** If working on ClickUp tasks, ensure they are updated BEFORE creating the handoff. The handoff references task state; that state must be current.
- **One handoff per conversation.** If the user asks for another handoff in the same conversation, update the existing file rather than creating a second one.
