---
name: update-memory
description: Use this skill when important project knowledge should be preserved in persistent memory, especially after debugging, setup fixes, experiment decisions, workflow changes, or repeated mistakes that Claude should avoid in future sessions.
---

# Update Memory

This skill captures durable project knowledge so future sessions start from the right assumptions and avoid repeating solved mistakes.

## Use this skill when

- A debugging session uncovered a non-obvious fix.
- A version pin, command pattern, or workflow convention has been validated.
- The team made a project-level decision that should persist across sessions.
- A repeated failure mode has been identified and should be prevented.
- A user explicitly asks to “remember,” “save this,” or “update memory.”

## Do not use this skill for

- Temporary plans or one-off todos.
- Large narrative summaries of a whole session.
- Raw logs or verbose experiment output dumps.

## Objective

Write concise, durable memory entries that improve future performance without cluttering memory with transient detail.

## What belongs in memory

Good candidates:
- validated setup commands,
- package/version pins that matter,
- canonical run commands,
- known hook-path quirks,
- dataset access constraints,
- naming conventions,
- stable repo structure notes,
- repeated user preferences for how work should be done.

Bad candidates:
- temporary experiment plans,
- one-off hypotheses,
- long transcripts,
- noisy logs,
- outdated intermediate results.

## Memory-writing principles

- Be brief.
- Be durable.
- Prefer “facts future Claude should act on” over storytelling.
- Record both the issue and the correct behavior.
- If a fact may expire, mark it as conditional.

## Suggested entry format

Use compact bullets such as:

- Decision:
- Verified:
- Avoid:
- Canonical command:
- Known issue:
- Next-time rule:

## Workflow

### Step 1: Extract durable knowledge

From the current task or session, identify 1–5 items that are likely to matter again.

### Step 2: Filter aggressively

Only keep information that is:
- reusable,
- stable across sessions,
- actionable.

### Step 3: Update the right memory location

If the project uses:
- `CLAUDE.md` for stable onboarding rules,
- `MEMORY.md` for evolving operational notes,

prefer:
- `CLAUDE.md` for broad, stable project-wide guidance,
- `MEMORY.md` for validated operational findings and recurring lessons.

Do not bloat `CLAUDE.md` with session-level detail.

### Step 4: Write clearly

Turn findings into short imperative or declarative bullets. Avoid vague notes like “watch out for setup issues.”

Good example:
- Verified: Gemma multimodal smoke test is not considered passed until a real forward pass with image inputs succeeds.
- Avoid: Assuming emotion labels are single-token; always verify tokenizer behavior before logit comparisons.

### Step 5: Confirm impact

After updating memory, summarize what was added and how future sessions should benefit.

## Guardrails

- Do not store secrets, tokens, or credentials.
- Do not save speculative claims as facts.
- Do not duplicate large chunks of existing memory.
- Do not turn memory into a checklist manager.
- Do not write entries that will obviously go stale in a day unless they are clearly dated and conditional.

## Completion criteria

This skill is complete when:
- the durable lessons are extracted,
- weak or temporary notes are filtered out,
- the right memory file is updated cleanly,
- the saved entries are concise and actionable.

## Example invocations

- “Remember this fix for future sessions.”
- “Update project memory with today’s setup lessons.”
- “Save the canonical command sequence for Stage A.”
- “Record the known TransformerBridge pitfall.”