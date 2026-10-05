---
name: note-management
description: |
  Captures, reviews, and promotes Note entities — the lightweight knowledge capture primitive in processkit. Notes are quick-capture units (thoughts, insights, questions, references) that are reviewed periodically and promoted to WorkItems, DecisionRecords, or other primitives when they ripen. Use when the user says "remember this", "note that", "I had an idea", or when running a periodic note review session.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-note-management
    version: "2.0.0-alpha.1"
    created: 2026-04-08T00:00:00Z
    category: processkit
    layer: 2
    commands:
      - name: pk-note
        args: "title or short description of the note"
        description: "Capture a new fleeting note with the given title"
      - name: pk-note-review
        args: ""
        description: "Review all fleeting notes and decide what to promote or discard"
      - name: pk-note-promote
        args: "note-id"
        description: "Promote a fleeting note to a more permanent artifact"
    provides:
      primitives: [Note]
      mcp_tools:
        - create_note
        - capture_inbox_item
        - claim_inbox_item
        - complete_inbox_item
        - fail_inbox_item
---

# Note Management

## Intro

Notes are processkit's capture layer — the place where ideas land
before they are ready to become backlog items, decisions, or
artifacts. Inspired by the Zettelkasten model: capture fast (fleeting),
refine deliberately (permanent), link explicitly, and promote when
something becomes actionable. The review cycle is what gives notes
their value — unreviewed notes are just noise.

In v2, note-management also owns the hook inbox. External or
agent-generated interrupts enter as Notes with `spec.inbox`, then move
through captured, claimed, completed, or failed before they are
promoted or linked into tracked work.

Hook adapters use a filesystem hand-off layout rooted at `tasks/`:
`tasks/inbox/`, `tasks/claimed/`, `tasks/done/`, and `tasks/failed/`.
Run `prepare_hook_inbox_dirs()` before wiring a drop adapter. The
adapter may place raw payloads in `tasks/inbox/`, but the canonical
processkit record is still created through `capture_inbox_item()` as a
`Note(type=fleeting, state=captured)` with `spec.inbox`.

The note-management MCP server may be reached directly from this skill's
`mcp/mcp-config.json` or through the processkit gateway. Gateway
deployments must surface only the processkit servers present in the
installed/merged MCP configuration; this skill does not imply that
unrelated processkit tools are available.

## Overview

### Note types

Note types map to the Luhmann/Ahrens Zettelkasten taxonomy:

| Type | Luhmann equivalent | When to use | Review horizon |
|---|---|---|---|
| **fleeting** | Fleeting note | Quick thought, idea, or observation — not yet refined | Within 1 week |
| **insight** | Permanent note | A self-contained conclusion or realization; part of the knowledge base — never discarded | Evergreen (not discarded, only promoted or refined) |
| **reference** | Literature note | Pointer to an external source, with your own summary | Evergreen |
| **question** | — | An open question you want to revisit | Until answered |

Start with `fleeting` when in doubt. If a note survives a review
session unchanged and seems worth keeping, refine and set to `insight`
or `reference`. **Insight notes are permanent — they are never
discarded, only promoted or further refined.**

### Note file location and format

Notes live in `context/notes/` as individual Markdown files with YAML
frontmatter:

```
context/notes/
  NOTE-20260408_1432-amber-fox-better-error-messages.md
  NOTE-20260408_1455-silver-wolf-rag-chunking-question.md
  ...
```

File naming: `{id}.md` where `{id}` is the full ID returned by
`generate_id("Note", slug_text=title)`. No separate INDEX.md —
the SQLite index (via `index-management`) replaces it.

```yaml
---
apiVersion: processkit.projectious.work/v2
kind: Note
metadata:
  id: NOTE-20260408_1501-amber-fox-error-field-names
  created: 2026-04-08
spec:
  title: "Error messages should cite the field that caused the \
error, not just the error code"
  type: insight
  state: captured
  tags: [ux, error-handling, api-design]
  review_due: 2026-04-15
---

When a validation error returns `code: 400`, the user has no way to
know which field failed. Every error response should include `field`,
`message`, and a `docs_url` for context. I've seen this pattern
in Stripe's and GitHub's APIs — it's the right model.
```

### Capturing a note

When the user says something note-worthy ("remember this", "I had
an idea", "note that"):

1. **Generate the Note ID** via `generate_id("Note", slug_text=title)`
   → e.g. `NOTE-20260408_1432-amber-fox-better-error-messages`
2. **Pick the type**: fleeting (quick thought) or one of the specific
   types if already clear
3. **Write the title as a self-contained claim or question** — not
   a topic label. "Error messages should include the field name" is
   a note title; "Error messages" is a topic, not a note.
4. **Set `review_due`**: today + 7 days for fleeting, today + 30 days
   for insight/question, none for reference
5. **Write `context/notes/{id}.md`** — no INDEX.md update needed

Notes are discovered and queried via the SQLite index
(`index-management`). To list active notes, use:

```
query_entities(kind="Note")
search_entities(text="<keyword>")
```

There is no hand-maintained INDEX.md — the index is authoritative.

### Running a review session

A periodic review session works through all notes whose
`review_due` has passed or is within 2 days:

For each overdue note, make one of four decisions:

**Promote** — the idea is ready to become a real primitive:
1. Create the downstream entity (WorkItem, DecisionRecord, etc.)
2. Add `promotes_to: { kind: WorkItem, id: BACK-042 }` to the
   note frontmatter
3. Transition the note to `promoted`

**Keep as permanent** — the note is worth keeping but not yet
actionable:
1. Refine the body if the capture was rough
2. Set type to `insight` (permanent note — never discarded) or
   `reference` (literature note — evergreen)
3. Transition state to `permanent`
4. Set `review_due` to null (permanent notes don't expire) or to a
   far-future date if you want a reminder to link it further
5. Add `links` to related notes with relation and context sentence

**Archive** — the note is no longer useful:
1. Transition state to `archived`

**Defer** — not ready to decide yet:
1. Keep state at `captured`
2. Extend `review_due` by 7 days
3. Add a one-line note on why it was deferred

### Linking notes

The `links` field is how Zettelkasten insight is built. Every link must
name the relation and provide a context sentence explaining *why* the
connection matters — not just *that* it exists. Tags group notes by
topic; links with context build arguments.

```yaml
links:
  - target: NOTE-20260408_1455-SilverWolf-rag-chunking-question
    relation: elaborates
    context: "Both notes address retrieval quality; this note proposes
      a concrete chunking strategy for the problem identified there."
```

| Relation | When to use |
|---|---|
| **elaborates** | This note expands on or adds depth to the target |
| **contradicts** | This note challenges or refutes the target |
| **supports** | This note provides evidence for the target |
| **is-example-of** | This note is a concrete case of an abstract claim |
| **see-also** | Loosely related; reader may find the target useful |
| **refines** | This note improves on or supersedes the target |
| **sourced-from** | This note's ideas draw from the target (for literature notes) |

Links are directional (from this note → to target). Bidirectional
linking is intentional — add the reciprocal link in the target note
when the relationship is symmetric (e.g. two `supports` notes).

### Promotion patterns

| Note type | Common promotion target | Trigger |
|---|---|---|
| question | WorkItem (spike), Discussion | The question needs research or a team answer |
| insight | DecisionRecord | The insight captures a choice that was made |
| fleeting | WorkItem (task/chore) | The quick idea turns out to be actionable |
| reference | Artifact | The source becomes a formal reference material |

This skill also provides the `/pk-note`, `/pk-note-review`, and
`/pk-note-promote` commands for direct invocation — see
`commands/pk-note.md`, `commands/pk-note-review.md`, and
`commands/pk-note-promote.md`.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Capturing topic labels instead of claims or questions.** "Error messages" is not a note — it's a tag. A note's title must be a self-contained claim ("Error messages should include the field name, not just the error code") or a specific question ("Does the auth middleware re-validate tokens on every request?"). Vague labels create a pile of notes with no re-discoverable content.
- **Reviewing notes without making a decision.** Reading through notes and doing nothing is not a review — it resets the review clock without advancing the note. Every note in a review session must exit with one of four decisions: promote, keep as permanent, archive, or defer with a reason and new date.
- **Never archiving notes.** A notes index that only grows and never shrinks stops being useful. Not every idea deserves to become permanent — many are superseded, wrong in retrospect, or simply no longer interesting. Archive aggressively; promoted and permanent notes are the signal.
- **Promoting a fleeting note without refining it first.** A rough, first-draft thought promoted directly to a DecisionRecord or WorkItem brings the roughness with it. Before promoting, read the note and refine: does the title accurately capture the claim? Is the body complete enough for a newcomer to understand without the original context?
- **Writing notes that require the original context to make sense.** "The thing we discussed about the API" is meaningless six weeks later. A note must be self-contained: include enough context that the note makes sense to the author (or an agent) who has no memory of the conversation or session where the idea was captured.
- **Not writing the review decision back to the file.** After a
  review session, every note that was touched must have its `state`,
  `review_due`, and (if promoted) `promotes_to` fields updated in
  the file. The SQLite index is kept current by re-indexing, but
  the file is the source of truth.
- **Using notes as a dumping ground for everything instead of a capture layer for non-backlog ideas.** Notes are for ideas not yet ready to be backlog items. Things that are clearly tasks should go directly into a WorkItem. Things that are clearly decisions should go into a DecisionRecord. Notes are the intermediate capture for things that haven't crystallized yet — not a general-purpose inbox for all project work.

## Full reference

### Note ID assignment

IDs are generated by `generate_id("Note", slug_text=title)` and
follow the standard processkit timestamp-word-pair format:
`NOTE-YYYYMMDD_HHMM-word-pair[-slug]`

Example: `NOTE-20260408_1432-amber-fox-better-error-messages`

IDs encode the capture time and are globally unique. No counter or
INDEX.md is needed — the SQLite index replaces both.

### State transitions

```
captured → reviewing → permanent
                     → promoted  (terminal)
                     → archived  (terminal)
captured → archived
permanent → reviewing
permanent → promoted
permanent → archived
```

### Review cadence

Suggested cadence for a solo developer:

| Frequency | Action |
|---|---|
| Daily | Capture freely — do not review |
| Weekly | Review all fleeting notes past their review_due |
| Monthly | Review all permanent notes; check if any should be promoted |
| Quarterly | Archive anything in permanent that hasn't been revisited in >90 days |

For teams, assign a note review owner per sprint or rotate the
responsibility on a weekly basis.

### Note template

```markdown
---
apiVersion: processkit.projectious.work/v2
kind: Note
metadata:
  id: NOTE-{{YYYYMMDD_HHMM}}-{{word-pair}}[-{{slug}}]
  created: {{date}}
spec:
  title: "{{self-contained claim or question}}"
  type: {{fleeting|insight|reference|question}}
  state: captured
  tags: []
  review_due: {{date + 7 days for fleeting, + 30 for question, null for insight/reference}}
  # links: optional — add when you know related notes
  # links:
  #   - target: NOTE-xxx-yyy
  #     relation: elaborates  # see relation table above
  #     context: "One sentence explaining why this connection matters."
---

{{Note body — enough context to understand without memory of the
session}}
```

File name: `context/notes/{id}.md` (the full ID, no extra suffix).

### Relationship to other primitives

| Primitive | How notes relate |
|---|---|
| **WorkItem** | Notes often promote to WorkItems when an idea becomes a task |
| **DecisionRecord** | Insight notes about choices promote to DecisionRecords |
| **BACKLOG.md** | High-priority, well-understood items go here directly — not in notes |
| **STANDUPS.md** | Standups reference the work done; notes capture the ideas generated |
