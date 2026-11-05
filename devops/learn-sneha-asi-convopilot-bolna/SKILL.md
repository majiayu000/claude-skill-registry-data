---
name: learn
description: Capture decisions, mistakes, and patterns from this session into CLAUDE.md so future Claude sessions don't repeat the same mistakes
argument-hint: "log (capture from current session) OR apply (write captured learnings to CLAUDE.md)"
allowed-tools: Read Glob Grep Write Edit
---

You are capturing session learnings for ConvoPilot.

Action: **$ARGUMENTS**

---

## Two modes

- `/learn log` — Scan the current session, find learnings, save to `working_docs/session-log.md`
- `/learn apply` — Review saved learnings and write the important ones into `CLAUDE.md`

---

## `/learn log` — Capture from this session

### Step 1 — Scan the session for these learning types

| Type | What to look for |
|---|---|
| **DECISION** | A choice was made (e.g. "we're not using OpenAI, only Claude + Gemini") |
| **MISTAKE** | Something was done wrong and corrected (e.g. "used the wrong Langfuse host for traces") |
| **PATTERN** | A reusable approach discovered (e.g. "use @trace_root/@trace_span decorators for tracing") |
| **CONVENTION** | A rule that should be followed going forward (e.g. "always check existing services for reusable patterns first") |

### Step 2 — For each learning found, ask the owner

> "I found this learning: [description]. Should I log it? (yes / skip)"

### Step 3 — Append approved learnings to `working_docs/session-log.md`

Create the file if it doesn't exist. Format:

```markdown
### L-{N}: {short title}
- **Type:** DECISION | MISTAKE | PATTERN | CONVENTION
- **Date:** {today}
- **What happened:** {1–2 sentences}
- **Where to apply:** CLAUDE.md | skill file | both
- **Proposed rule:** {the actual instruction to add}
- **Status:** captured
```

### Step 4 — Summary

Tell the owner: "Logged {N} learnings to `working_docs/session-log.md`. Run `/learn apply` to write them into CLAUDE.md."

---

## `/learn apply` — Write learnings to CLAUDE.md

### Step 1 — Read `working_docs/session-log.md`

Extract all entries with `Status: captured`.

### Step 2 — Present a table to the owner (GATE — wait for approval)

| # | Learning | Target | Draft rule |
|---|---|---|---|
| L-1 | No OpenAI key | CLAUDE.md | "ConvoPilot uses Anthropic Claude and Google Gemini only. No OpenAI." |
| L-2 | Langfuse stage TBD | CLAUDE.md | "Langfuse keys are TBD — do not use prod keys. Await stage project." |

Ask: "Should I apply these to CLAUDE.md? (confirm each or say 'all')"

### Step 3 — Apply approved learnings

Read the target file, add the rule in the appropriate section, write back.

Rules for where things go in CLAUDE.md:
- LLM provider decisions → "External Dependencies & Secrets Needed" section
- Coding conventions → "Coding Standards" section
- Behaviour rules for Claude → "How Claude Must Behave" section
- Infrastructure / deploy decisions → add a new "Key Decisions" section if needed

Keep CLAUDE.md under 200 lines. If it gets longer, tell the owner.

### Step 4 — Mark applied

Update `working_docs/session-log.md` → change `Status: captured` to `Status: applied` for each entry written.

### Step 5 — Summary

Tell the owner: "Applied {N} learnings to CLAUDE.md. Future sessions will follow these rules automatically."

---

## When to use this skill proactively

Offer to run `/learn log` at the end of any session where:
- A decision was made about the tech stack or architecture
- A mistake was corrected (e.g. wrong config, wrong pattern)
- A reusable pattern was discovered
- The owner said "don't do X" or "always do Y"
