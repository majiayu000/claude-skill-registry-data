---
name: handoff-by-caio
description: >
  Generates a structured Markdown handoff file to move an active conversation into a new chat,
  preserving full context, decisions, artifacts, and a ready-to-paste resume prompt.
  ALWAYS trigger this skill when the user says "move to a new chat", "move this to a new chat",
  "handoff", "/handoff", "continue in a new chat", "let's move", "new conversation", or any
  variation indicating they want to transfer the current session to a fresh Claude conversation.
  Do NOT ask for clarification — execute immediately and produce the .md file.
---

# Handoff Skill
### by CAIO Group — wearecaio.com

Move any Claude conversation to a new chat with zero re-explanation.
Generates a structured `.md` file with full context, classified artifacts, and a paste-ready resume prompt.

---

## Trigger Phrases

Execute immediately (no confirmation needed) on any of these:

- `/handoff`
- "move to a new chat"
- "move this to a new chat"
- "continue in a new chat"
- "let's continue in a new conversation"
- "handoff file"
- "new chat" (when context implies session transfer)

---

## Execution Steps

### Step 1: Analyze the conversation

Scan the full conversation history and extract:

1. **Session type**: What kind of work was this? (e.g., proposal, slide deck, automation, strategy, training, code, analysis, research, writing)
2. **Core objective**: What was the user trying to accomplish?
3. **Decisions made**: Key choices, directions taken, things approved or rejected
4. **Current state**: What is built, written, or resolved vs. what is still open
5. **Artifacts created**: Any files, code blocks, documents, scripts, dashboards, or structured outputs produced
6. **Next steps**: What was the natural next action before the session ended?

---

### Step 2: Classify artifacts

For each artifact identified, assign one of three tags:

- `[CARRY OVER]` — Essential to continue. Include full content as a code block.
- `[REFERENCE]` — Useful context but not required. Include a summary only.
- `[ARCHIVE]` — Superseded or no longer relevant. Note it exists, exclude content.

**Default rule**: When in doubt, tag as `[CARRY OVER]`.

---

### Step 3: Generate the suggested chat filename

Derive a suggested name for the new chat using this format:

```
[PREFIX] — [Topic] [Qualifier]
```

**Prefix by session type:**

| Session Type | Prefix |
|---|---|
| Proposal / Pitch | `PROP` |
| Slide Deck / Presentation | `DECK` |
| Automation / Script / Code | `AUTO` |
| Strategy / Planning | `STRAT` |
| Training / Education | `TRAIN` |
| Analysis / Research | `ANALY` |
| Skill / Tooling | `SKILL` |
| Writing / Content | `WRITE` |
| Design / Creative | `DESIGN` |
| Communication / Outreach | `COMM` |
| General / Mixed | `WORK` |

**Topic:** 2-4 words from the session objective. Title case. No filler words.
**Qualifier (optional):** Short version or context indicator (e.g., `v2`, `Draft`, `Client Name`).

**Examples:**
- `PROP — SaaS Pricing Overhaul v2`
- `AUTO — Email Automation Pipeline`
- `STRAT — Q3 Market Expansion`
- `SKILL — Handoff Workflow Builder`

---

### Step 4: Generate the handoff file

Produce a single Markdown file using the template below. Fill every section. No placeholders in output.

---

## Handoff File Template

```markdown
# Handoff: [Session Title — descriptive, not generic]

**Date:** [today's date]
**Session Type:** [detected session type]
**Suggested chat name:** `[PREFIX — Topic Qualifier]`

---

## What We Were Working On

[2-4 sentences. What was the task, why it mattered, what approach was being taken.]

---

## Decisions Made

- [Decision 1 — include reasoning if discussed]
- [Decision 2]
- [Decision 3]

---

## Current State

### Done
- [Completed items]

### In Progress
- [Partially done items]

### Not Started
- [Scoped but untouched]

---

## Artifacts

### CARRY OVER — Bring These Into the New Chat

#### [Artifact Name]
**Type:** [code / markdown / config / script / document / etc.]
**Why it's needed:** [one sentence]

[Full artifact content as fenced code block]

---

### REFERENCE — Useful Context

#### [Artifact Name]
**Summary:** [2-3 sentences]

---

### ARCHIVE — No Longer Needed

- [Artifact name]: [one-line reason]

---

## Open Questions

- [ ] [Unresolved decision or pending input]
- [ ] [Ambiguity to address in new chat]

---

## Next Steps

1. [First action — executable immediately in the new chat]
2. [Second action]
3. [Third action]

---

## Resume Prompt

Paste this as your first message in the new chat:

[3-5 sentences in first person that:
- State the session type and goal
- Reference the most critical current state item
- Point to the most important CARRY OVER artifact
- State exactly what the next action is
Must be self-contained: a fresh Claude instance begins work immediately.]
```

---

### Step 5: Output the file

1. Save the completed handoff file to `/mnt/user-data/outputs/handoff-[topic]-[date].md`
   (If this path is unavailable, save to the current working directory)
2. Deliver the file to the user
3. Print a 4-line summary in chat:
   - **Session type:** [detected type]
   - **Artifacts:** [count and classifications]
   - **First next step:** [specific action]
   - **Suggested chat name:** `[PREFIX — Topic Qualifier]`

Do not print the full file contents in chat.

---

## Quality Standards

- Every section filled. No placeholder text in output.
- Resume Prompt is paste-ready: no blanks, no angle brackets, no instructions to "fill in X".
- CARRY OVER artifact content is complete, never truncated.
- Decisions reflect actual choices made in the conversation, not generic statements.
- Next Steps are specific enough to act on immediately.
- The output file contains no tool branding, no skill credits, no advertisements.

---

## Edge Cases

**No artifacts in conversation:** Skip the Artifacts section entirely.

**Short conversation (under 5 exchanges):** Collapse "Done / In Progress / Not Started" into a single "Current State" paragraph.

**Multiple unrelated topics in one conversation:** Generate one handoff file per topic thread, named distinctly. Inform the user that multiple files were created.

**Sensitive content (names, financials, credentials):** Include as-is. The user controls their own handoff files.

**Output path unavailable:** Save to current working directory and inform the user of the actual file path.
