---
name: knowledge-flywheel
description: Analyze captured knowledge for patterns — detect repeated decisions, suggest conventions, surface "you keep running into X" insights.
compatibility: opencode
metadata:
  audience: any-agent
  purpose: knowledge-amplification
---
## What I do

Analyze the knowledge base (`.hero/knowledge/`) for patterns that should
be promoted to conventions, decisions, or warnings. This turns raw captured
notes into structured team intelligence.

## When to use me

- At the end of a sprint or after 5+ knowledge entries have been captured
- When `/prime` detects a growing knowledge base (>10 entries)
- When the user asks "what have we learned?" or "any patterns?"

## How to use me

1. Read all entries in `.hero/knowledge/notes/`
2. Group by topic (file paths mentioned, error types, technologies)
3. Identify patterns:
   - **Repeated decisions**: same choice made 3+ times → suggest a convention
   - **Recurring issues**: same debugging finding 2+ times → suggest a rule
   - **Converging practices**: similar approaches across specs → suggest codifying
4. For each pattern found, suggest an action:
   - `/convention` to codify a repeated practice
   - Add to an existing convention if one covers the topic
   - Flag as a potential architectural concern if it's a structural pattern

## Output format

```
Knowledge flywheel — N entries analyzed

Patterns detected:

  1. Convention candidate: "Error handling in API routes"
     Seen in: 3 notes (auth-debugging, payment-retry, export-errors)
     Suggestion: /convention codify API error response retry pattern

  2. Recurring issue: "Database connection pool exhaustion"
     Seen in: 2 notes (monday-outage, load-test-findings)
     Suggestion: Add connection pool monitoring to operational runbook

  3. No new patterns (N entries too unique to cluster)
```

## What not to do

- Don't fabricate patterns — only surface what's genuinely repeated
- Don't suggest conventions for one-off decisions
- Don't modify existing knowledge entries
- Don't require an LLM — pattern detection is keyword/topic clustering
