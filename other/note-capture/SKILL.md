---
name: note-capture
description: How agents capture conversations, brainstorms, and thinking as notes in the Hero knowledge base.
compatibility: opencode, cursor, claude
metadata:
  audience: agents
  purpose: knowledge-capture
---
## What I do

Teach agents how to capture valuable conversations and thinking as notes in the Hero knowledge base. Notes are the lowest-friction knowledge type — no structure required, no status workflow, just timestamped captures of thinking that gets indexed and searchable.

## When to use me

Load this skill when:
- A user asks you to "save this conversation as a note"
- A user says "capture this" or "remember this" or "turn this into a note"
- You've had a particularly productive brainstorm or design discussion and the user wants to preserve it
- A debugging session produced valuable insights worth recording
- The user is dictating stream-of-consciousness thinking they want preserved

## The golden rule

**Include both sides of the conversation.** The agent's analysis, reasoning, suggestions, and code examples are often the most valuable part. Do not strip out your own contributions. Do not aggressively summarize. Preserve the thinking.

## How to capture a note

### Step 1: Determine the slug

Derive a short kebab-case slug from the topic:
- `auth-flow-brainstorm`
- `redis-vs-postgres-session-store`
- `why-we-chose-grpc`
- `debugging-memory-leak-april-12`

If the user doesn't provide a topic, ask: "What should I title this note?"

### Step 2: Create the note file

Run:
```
hero note <slug>
```

This creates `.hero/knowledge/notes/<slug>/spec.md` with minimal frontmatter.

### Step 3: Write the full content

Open the created file and replace the placeholder with the captured content. Use this structure:

```markdown
---
title: <descriptive title>
type: note
created: <date>
tags: [<relevant>, <tags>]
---
# <Title>

## Context
What prompted this conversation. One or two sentences.

## Discussion

**Human:** <user's message>

**Assistant:** <your response>

**Human:** <user's follow-up>

**Assistant:** <your analysis>

(Continue for the full relevant conversation)

## Key Takeaways
- Bullet point the conclusions, decisions made, or open questions
- Include any action items that emerged
- Note anything that should become a spec later
```

### Step 4: Confirm

Tell the user:
- Where the note was saved
- How many key points were captured
- Suggest tagging if they didn't specify tags

## What to include vs. exclude

### Include
- The full back-and-forth dialogue (both sides)
- Code snippets and examples discussed
- Architectural diagrams or data models sketched out
- Trade-off analysis and reasoning
- Conclusions and decisions reached
- Open questions that remain

### Exclude
- Greetings, pleasantries, and small talk
- Repeated corrections of typos or misunderstandings (just include the corrected version)
- Tool output that's purely mechanical (e.g., full test suite output — summarize instead)
- Sensitive information (credentials, tokens, personal data) — redact these

## Different capture modes

### Full conversation capture
The user says "save this whole conversation as a note." Capture everything substantive from the session.

### Selective capture
The user says "save the part about auth as a note." Extract only the relevant portion of the conversation.

### Live note mode
The user says "let's brainstorm about X — capture this as a note when we're done." Continue the conversation normally, then at the end, save everything discussed about X.

### Quick thought
The user says "note: we should probably add rate limiting to the API." Just run:
```
hero note "we should probably add rate limiting to the API"
```
This creates a one-liner note. Fast, minimal friction.

## Relationship to other knowledge types

Notes are the entry point for knowledge. Over time, notes may graduate:

| From | To | When |
|---|---|---|
| Note about a pattern | Convention (`/convention`) | The pattern is worth standardizing |
| Note about a decision | Decision (`/decide`) | The decision needs formal documentation |
| Note about a feature idea | Spec (`/design`) | The idea is ready to become actionable work |
| Note about a bug pattern | Bug spec (`/diagnose`) | The pattern needs investigation |

When saving a note, if you notice it's really a decision or convention in disguise, mention that to the user: "This looks like it could be a decision record. Want me to create a `/decide` instead?"

## Notes are searchable

Once saved, notes are indexed by `hero index` and searchable via `hero search`. The full text is indexed with FTS5 porter stemming, so even rough notes become findable later.
