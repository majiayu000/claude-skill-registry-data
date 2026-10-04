---
name: auto-knowledge-capture
description: How agents automatically detect and persist learnings at the end of major workflows.
compatibility: opencode, cursor, claude
metadata:
  audience: agents
  purpose: knowledge-capture
---
## What I do

Teach agents how to silently evaluate whether a work session produced knowledge worth capturing, and if so, persist it without prompting the user. This is the "smart auto-capture" skill — it only fires when there's actually something to capture.

## When to use me

This skill is embedded in the final step of `/deliver`, `/diagnose`, `/retro`, and `/design`. You don't load it manually — it activates automatically at the end of these workflows when `knowledge.auto_capture` is enabled in `hero.json` (default: on).

## The decision: capture or skip?

Before writing anything, evaluate whether the session produced **novel, reusable knowledge**. Ask yourself:

### Capture if ANY of these are true:
- A technical constraint was discovered that isn't documented (e.g., "FTS5 can't handle hyphens in MATCH queries")
- A design decision was made with trade-offs discussed (e.g., "chose SSE over WebSockets for MCP transport")
- A pattern was established that future work should follow (e.g., "all CLI flags use package-level vars and resetFlags()")
- A workaround was needed for a tool/library limitation (e.g., "Cobra flag state persists across test runs")
- An integration or API behavior was learned empirically (e.g., "Figma API can't generate designs, only read them")
- A architectural boundary or constraint was established (e.g., "no new Go dependencies")

### Skip if ALL of these are true:
- The work was straightforward implementation of an existing spec
- No surprises or unexpected behavior was encountered
- No decisions were made — just execution
- The knowledge already exists in `.hero/knowledge/`

### When in doubt, skip. Noise in the knowledge base is worse than gaps.

## How to capture silently

When you determine something is worth capturing:

1. **Don't prompt the user.** Don't ask "should I save this?" Just do it.
2. **Classify the learning** into the right knowledge type:
   - Pattern/style → convention (`.hero/knowledge/conventions/<slug>/spec.md`)
   - Technical choice → decision (`.hero/knowledge/decisions/<slug>/spec.md`)
   - Hard constraint → rule (`.hero/knowledge/rules/<slug>/spec.md`)
   - Background info → context (`.hero/knowledge/context/<slug>/spec.md`)
   - Rough insight → note (`hero note <slug>`)

3. **Write concisely.** Knowledge entries should be scannable:
   - Title: clear, specific (not "Database Notes" — instead "SQLite FTS5 Hyphen Handling")
   - Body: 3-10 sentences. What, why, and how to apply it.
   - Tags: 2-4 relevant tags for discoverability

4. **Mention it briefly at the end of your response.** One line, not a sales pitch:
   - "Captured convention: sqlite-fts5-hyphen-handling"
   - "Captured decision: sse-over-websockets-mcp-transport"
   - Or if nothing: say nothing. Don't announce "no knowledge captured."

5. **Run `hero index`** after writing to make it searchable.

## Knowledge entry templates

### Convention
```markdown
---
title: <Pattern Name>
type: convention
status: active
tags: [<tag1>, <tag2>]
created: <YYYY-MM-DD>
---

## Convention

<What the pattern is. 1-2 sentences.>

## Rationale

<Why this pattern exists. What goes wrong without it.>

## Examples

<Good and bad examples if helpful.>
```

### Decision
```markdown
---
title: <Decision Title>
type: decision
status: accepted
tags: [<tag1>, <tag2>]
created: <YYYY-MM-DD>
---

## Decision

<What was decided. 1 sentence.>

## Context

<What prompted this decision.>

## Alternatives Considered

<What else was evaluated and why it was rejected.>
```

### Rule
```markdown
---
title: <Rule Name>
type: rule
status: active
tags: [<tag1>, <tag2>]
created: <YYYY-MM-DD>
---

## Rule

<The constraint. 1 sentence.>

## Rationale

<Why this rule exists.>
```

## Deduplication

Before writing, mentally check against existing knowledge. If you recall that a similar convention or decision already exists from earlier in the conversation or from reading the knowledge base, don't create a duplicate. If the existing entry needs updating, update it instead of creating a new one.

## Volume control

A typical session should produce 0-3 knowledge entries. If you find yourself wanting to write more than 3, you're probably being too granular. Consolidate related learnings into a single entry.
