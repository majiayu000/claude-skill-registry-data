---
name: discussion-management
description: |
  Manage Discussion entities — structured, multi-turn conversations that explore questions and produce decisions. Use when a question or design choice needs multi-turn exploration before a decision is reached — RFCs, design debates, trade-off analyses.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-discussion-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 4
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: decision-record
        purpose: Record consequential decisions made during this skill's workflow.
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
      - skill: id-management
        purpose: Allocate unique entity identifiers via central ID generation.
    provides:
      primitives: [Discussion]
      mcp_tools:
        - open_discussion
        - get_discussion
        - transition_discussion
        - add_outcome
        - list_discussions
      templates: [discussion]
    commands:
      - name: pk-discuss
        args: "topic or question to discuss"
        description: "Start a structured discussion on a topic: research, challenge assumptions, present alternatives, work toward a conclusion"
---

# Discussion Management

## Intro

A Discussion is a structured, multi-turn conversation exploring a question.
It captures the back-and-forth of research, proposals, objections, and
convergence — producing (or failing to produce) a DecisionRecord as its
outcome. Think of it as the audit trail behind a decision.

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses reach its tools by reading a single MCP config
> file at startup, so the contents of `mcp/mcp-config.json` must be merged
> into the harness's MCP config and placed at the harness-specific path
> before this skill is usable. If processkit was installed by an installer,
> that wiring is the installer's responsibility; if processkit was
> installed manually, the project owner must do it by hand.

## Overview

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v2
kind: Discussion
metadata:
  id: DISC-002
  title: "aibox Refocus — Core Principles and Scope"
  created: 2026-04-05
  participants: [owner, claude]
spec:
  state: active          # active | resolved | archived
  question: "What is aibox's core scope? What belongs in processkit? What is out of scope entirely?"
  related: [DISC-001]
---

# Discussion body

## 1. Problem statement
...

## 2. What aibox IS
...

## Decisions (DEC-NNN records)
- DEC-017: Scope refocus
- DEC-018: Two-repo split
...
```

### Workflow

1. Start a Discussion when a non-trivial question arises.
2. Write the `question` as one crisp sentence.
3. Use numbered sections in the body: problem statement, options considered,
   analysis, decisions.
4. As decisions crystallize, write DecisionRecords and list them at the bottom
   of the Discussion.
5. When converged, set `state: resolved`. Log `discussion.resolved`.

### Discussions vs DecisionRecords

| Discussion                     | DecisionRecord                          |
|--------------------------------|-----------------------------------------|
| Multi-turn, exploratory        | Single outcome, crisp                   |
| Captures reasoning journey     | Captures the destination                |
| May produce 0–many DEC records | Produced by at most one Discussion      |
| Often long-form                | Tightly structured                      |

Use a Discussion when you don't yet know the answer. Use a DecisionRecord
when you do.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Opening a Discussion when the choice is already obvious.** If
  the user already knows what they want, write a DecisionRecord
  directly. Discussions are for genuinely open questions where the
  reasoning trail matters; using one for a settled call wastes
  ceremony.
- **Letting Discussions go stale.** A Discussion with no activity
  for weeks should either resolve (with an outcome) or close
  (state: archived). Open-forever discussions clutter the index
  and signal pretend-thinking.
- **Not recording the outcome as a DecisionRecord on convergence.**
  When a Discussion reaches an answer, the answer must become a
  DecisionRecord referenced in the discussion's `outcomes` field.
  Without that promotion, the value of the discussion evaporates
  the next time someone asks "what did we decide".
- **Putting decisive content in the body but leaving `outcomes`
  empty.** The `outcomes` field is what downstream queries read.
  If the body says "we decided X" but `outcomes: []`, the index
  doesn't know a decision was made and can't link the discussion
  to the DecisionRecord.
- **Confusing Discussion (pre-decisional) with DecisionRecord
  (post-decisional).** Discussions capture reasoning in flight;
  DecisionRecords capture settled choices. Don't write reasoning
  into a DecisionRecord, and don't write conclusions into a
  Discussion body without also creating the DecisionRecord.
- **Forgetting to add participants.** The `participants` field is
  how queries like "what is Alice currently thinking about" work.
  An unattributed Discussion is invisible to participant queries.
- **Treating one user message as a "discussion".** A Discussion is
  multi-turn by definition. If there's only one back-and-forth, it
  doesn't need the structure — answer directly or write a
  DecisionRecord.

## Full reference

### Fields

| Field          | Type           | Notes                                          |
|----------------|----------------|------------------------------------------------|
| `state`        | enum           | `active` / `resolved` / `archived`             |
| `question`     | string         | The driving question                           |
| `participants` | list[string]   | Actor IDs                                      |
| `related`      | list[string]   | Other discussion IDs                           |
| `outcomes`     | list[string]   | DEC IDs produced                               |
| `opened_at`    | datetime       | When the discussion started                    |
| `closed_at`    | datetime       | When it was marked resolved                    |

### Long-running discussions

Some discussions span weeks or months. Keep them in one file — use section
dividers with dates rather than creating multiple files. The index MCP
server can show discussion activity over time by reading LogEntries that
reference it.

### Archiving

When a discussion is old and no longer actively referenced, move it to
`context/archive/discussions/` and set `state: archived`. Do not delete —
the reasoning is often the most valuable context for future work.

### Example: DISC-002

The DISC-002 document in the aibox repo is a full example of a processkit
Discussion — multi-section, multiple open questions resolved over time,
producing DEC-017..DEC-024. It predates this skill (was written in plain
Markdown) and can be retroactively brought into the format by adding the
frontmatter block.
