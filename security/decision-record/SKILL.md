---
name: decision-record
description: |
  Record decisions with rationale, alternatives, and consequences — the ADR pattern as a primitive. Use when a consequential choice is made — architecture, tooling, process, scope, trade-off. Capture WHY, not just WHAT.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-decision-record
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 2
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: actor-profile
        purpose: Resolve and validate Actor IDs referenced by this skill's entities.
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
      - skill: id-management
        purpose: Allocate unique entity identifiers via central ID generation.
    provides:
      primitives: [DecisionRecord]
      mcp_tools: [record_decision, query_decisions, link_decision, supersede_decision]
      templates: [decisionrecord]
    commands:
      - name: pk-dec
        args: "decision-title"
        description: "Record a new architectural or product decision with the given title"
      - name: pk-dec-find
        args: "filter"
        description: "Query existing decisions by keyword, status, or topic"
---

# Decision Record

## Intro

A DecisionRecord captures a single consequential choice: what was decided,
why, what alternatives were rejected, and what consequences are expected.
This is the classic **Architecture Decision Record (ADR)** pattern, promoted
to a first-class primitive in processkit.

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses reach its tools by reading a single MCP config
> file at startup, so the contents of `mcp/mcp-config.json` must be merged
> into the harness's MCP config and placed at the harness-specific path
> before this skill is usable. If processkit was installed by an installer,
> that wiring is the installer's responsibility; if processkit was
> installed manually, the project owner must do it by hand.

## Overview

### When to record a decision

Record a decision when the choice:

- Has consequences someone will ask about in six months ("why are we using X?").
- Rules out real alternatives that took thought to reject.
- Affects more than one file, component, or person.
- Is the kind of thing that "we decided in a meeting" but nobody wrote down.

Don't record: trivial choices made inside a single function, preference calls
with no downside, decisions already documented somewhere authoritative.

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-steady-river
  created: 2026-04-06T00:00:00Z
spec:
  title: "Use official Python MCP SDK with uv PEP 723 inline dependencies"
  state: accepted
  context: "Skill MCP servers need a runtime. Options vary from zero-dep stdlib to full SDK."
  decision: "Use the official mcp Python SDK, distributed as standalone scripts with PEP 723 inline deps, launched via uv."
  rationale: |
    - The SDK is the standard; rolling our own JSON-RPC means maintaining protocol code.
    - PEP 723 + uv eliminates per-skill env setup; uv caching amortizes first-run cost.
    - Container already has Python ≥3.10 and uv — no base image change.
  alternatives:
    - option: "Raw JSON-RPC with zero dependencies"
      rejected_because: "Reimplements the protocol, fragile for complex servers."
    - option: "Pydantic-only minimal server"
      rejected_because: "Kept as escape hatch if container size becomes critical; not default."
  consequences: |
    - +300-400 MB image size per skill with MCP server.
    - First-run 5-10s for uv resolution; cached thereafter.
    - Escape hatch documented if size becomes an issue.
  deciders: [ACTOR-owner, ACTOR-claude]
  decided_at: 2026-04-05T00:00:00Z
---

Optional body: longer narrative, links to the discussion, related research.
```

### Workflow

1. Pick an ID: `DEC-<generated-id>`.
2. Write a declarative `title` — state the decision itself, not a question.
3. Fill in `context` (what prompted this), `decision` (the chosen option),
   `rationale` (why).
4. List `alternatives` with explicit `rejected_because` — this is the part
   future-you will thank present-you for.
5. Write `consequences` — what follows from this decision, positive and
   negative.
6. Set `state: proposed` if still under discussion, `accepted` if finalized.
7. Save to `context/decisions/`.
8. Log `decision.created`; later state changes use
   `decision.transitioned`.

### Superseding

When a decision is replaced by a later one:

1. In the **new** DecisionRecord, set `spec.supersedes: DEC-<old-id>`.
2. In the **old** DecisionRecord, set `spec.state: superseded` and
   `spec.superseded_by: DEC-<new-id>`.
3. Log `decision.superseded` referencing both IDs.

**Never delete or edit the old record.** Its existence is why we can trace
the evolution of the decision.

This skill also provides the `/pk-dec` and `/pk-dec-find` commands for
direct invocation — see `commands/pk-dec.md` and
`commands/pk-dec-find.md`.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Recording a decision before it has actually been made.** A
  proposal in a discussion is not a DecisionRecord. Open a Discussion
  if reasoning is still in flight; only record when the choice is
  settled. Recording too early creates a fictional history.
- **Capturing WHAT but not WHY.** A DecisionRecord without rationale
  is just a workitem in the wrong directory. The whole value of the
  ADR pattern is the reasoning trail — what was considered, why this
  was picked, what was rejected.
- **Omitting the rejected alternatives.** "We decided X" is half a
  decision; "We picked X over Y and Z because …" is a decision.
  Future-you needs the alternatives to know whether the call still
  holds when context changes.
- **Editing an old DecisionRecord instead of superseding it.**
  Decisions are immutable history. If the call needs to change, write
  a NEW DecisionRecord with `supersedes:` pointing at the old one
  and set the old one's state to `superseded`. Never overwrite — the
  old reasoning is part of the audit trail.
- **Recording trivial choices as DecisionRecords.** A DecisionRecord
  is overhead; reserve it for choices a future agent or human will
  ask about in six months. Variable naming inside one function is
  not a DecisionRecord.
- **Putting the rationale in the Discussion body instead of the
  DecisionRecord.** Discussions are pre-decisional reasoning;
  DecisionRecords are post-decisional summary. The rationale must
  be copied (not linked) into the DecisionRecord so the latter is
  self-contained when read in isolation.
- **Hallucinating decision history when the user asks "what did we
  decide about X".** Run `query_decisions` and `search_entities`
  against the actual store before answering. Do not synthesize an
  answer from memory; it will be wrong.

## Full reference

### State machine

See `src/primitives/state-machines/decisionrecord.yaml`:

```
proposed → accepted → superseded (terminal)
    ↓
  rejected (terminal)
```

`rejected` is for decisions considered and declined — kept for history.
`superseded` is for decisions replaced by a later one.

### Full field list

See `src/primitives/schemas/decisionrecord.yaml`. Notable fields:

- `deciders`: list of Actor IDs. Who agreed.
- `supersedes` / `superseded_by`: DEC IDs. Replacement chain.
- `related_workitems`: BACK IDs. Work that prompted or implements the decision.
- `decided_at`: when the decision was finalized. Distinct from
  `metadata.created` (when the file was written).

### Distinguishing decisions from discussions

A **Discussion** (separate primitive) is a multi-turn conversation exploring
a question. A **DecisionRecord** is the crisp outcome. Workflow:

1. Open a Discussion when a question arises.
2. Explore, debate, research.
3. When the group converges on an answer, write a DecisionRecord.
4. Link the Discussion via `spec.related_discussions` (cross-reference).

Not every discussion produces a decision; not every decision is preceded by
a discussion.

### Writing good titles

Good titles are declarative, active, and concrete:

- ✓ "Use official Python MCP SDK with uv PEP 723 inline dependencies"
- ✓ "Two-repo split: aibox + processkit"
- ✗ "Which MCP library to use?" (question, not decision)
- ✗ "Tooling update" (too vague)
- ✗ "Alice's proposal" (credits the person, not the decision)

### Consequences that are honest

Future readers trust the decision record more when you write the real
consequences, including the uncomfortable ones. "Costs 300-400 MB image
size" builds more credibility than "some increase in container size."

### Linking to workitems

When a decision prompts work to happen, link via `spec.related_workitems`:

```yaml
spec:
  related_workitems: [BACK-calm-fox, BACK-swift-oak]
```

This lets queries find "all work that implements DEC-foo" and "all
decisions that motivated BACK-bar."
