---
name: Promote
description: Take a slice of the current conversation and promote it to a durable vault artifact — concept note, project update, person profile, or doctrine entry. Pairs with /close. /close writes the daily note (transient outcome record); /promote elevates specific insights to permanent vault content the framework can refer back to.
---

# Promote

The conversation is a substrate. Most of what happens in it is ephemeral — task-specific, session-bound, useful in the moment and gone after. But some exchanges produce durable insights: a new architectural understanding, a person fact worth remembering, a doctrine pattern emerging, a decision that should be logged.

Without `/promote`, those insights live in the conversation transcript and decay. With `/promote`, the principal can elevate them to vault content the framework will surface in future sessions.

## When to use

- The conversation produced an insight that should outlive this session
- The principal said "we should remember that" or "make a note that…"
- A doctrine pattern is starting to emerge from the discussion
- A new person, project, or concept came up that needs a vault entry
- Triggered by Caddy on prompts like: "/promote", "promote that", "make a note that", "save that insight", "elevate to doctrine", "capture this conversation", "remember that we decided", "this should be a vault note"

## How to execute

### Step 1 — Identify the slice to promote

Ask: which part of the conversation should become durable?

If the principal points to specific turns ("the last 10 messages about X"), use those. Otherwise:
- Default to the last 5-10 turns AND any explicitly-referenced earlier exchanges
- If unclear, ask one focused question: "Promote the {topic A} discussion or the {topic B} discussion?"

### Step 2 — Categorize the artifact

Map the slice to a vault category:

| If the slice is about... | Promote to... |
|---|---|
| A new concept, doctrine, or pattern | `vault/concepts/{slug}.md` |
| A person (collaborator, advisor, contact) | `vault/people/{name}.md` |
| A project (current or new) | `vault/projects/{slug}.md` |
| A decision with reasoning | append entry to `vault/memory/DECISION_LOG.md` |
| A learning sweep on a tool/framework | `vault/concepts/learning/{slug}.md` (use `/learn` instead) |
| A person/process rejection with reasoning | append entry to `vault/concepts/What I Am Not Building.md` |

If the slice is about multiple categories, produce multiple artifacts. Don't bundle.

### Step 3 — Extract the durable content

From the conversation slice, extract:
- **The insight or fact** (the load-bearing claim)
- **The reasoning that led to it** (why this is true / matters)
- **The context** (what triggered the conversation)
- **Open questions** (what's NOT yet resolved)

Drop:
- Conversational noise ("good point", "right", "that makes sense")
- Tool calls and intermediate exploration that doesn't matter to the conclusion
- Prior context that's already in other vault notes (link to those instead)

### Step 4 — Write the artifact

Use the appropriate vault note structure (frontmatter with title/tags/created/aliases, then content). Cross-link to existing notes that the slice references.

### Step 5 — Confirm and link

Output:

```
✅ Promoted to vault/{path}.md

Cross-references added:
- [[Existing Note 1]]
- [[Existing Note 2]]

Open questions captured:
- {question 1}
- {question 2}

Update [[MOC]] or [[MEMORY]] if this is high-signal? (y/n)
```

If the principal says yes, append a one-line entry to the appropriate MOC or to MEMORY.md.

### Step 6 — Optional: append to DECISION_LOG

If the promoted artifact reflects a decision (not just an insight), also append a one-line entry to `vault/memory/DECISION_LOG.md`:

```markdown
- 2026-04-27: {decision summary} → see [[promoted-artifact]]
```

This will trigger the decision-aging loop ([[Cost of Confidence]] sister doctrine) and surface 30/60/90-day check-ins via `/open`.

## What this skill is NOT

- **Not a transcript saver.** The daily note (`/close` artifact) handles that. `/promote` is for selective elevation.
- **Not a summarizer.** `/promote` extracts insights; it doesn't condense a long conversation. If the slice doesn't have a durable insight, don't promote — just let it stay in the transcript.
- **Not automatic.** The principal decides what graduates. Auto-promotion would dilute the vault.

## Anti-patterns this prevents

- Insights captured in chat transcripts that nobody reads later
- The principal saying "we already discussed this" but not knowing where
- Decisions made in conversation that don't make it to DECISION_LOG → lost reasoning
- Doctrine emerging in real-time but never crystallizing into a vault note → never applied

## Connects to

- `/close` — writes the daily note (transient outcome record)
- `/learn` — sister skill for tool/framework evaluations specifically
- `/decision-log` (forthcoming) — sister skill for decisions specifically
- [[Self-Improving CLAUDE.md]] — the broader pattern of converting conversation to durable rules
- [[Legibility Thesis]] — the meta-doctrine that demands ephemera become legible artifacts
- `vault/memory/MEMORY.md` — the index that gets updated when promoted artifacts are high-signal
