---
name: factual-communication
description: Restate content as a flat list of atomic facts in the style of av/facts fact sheets. Use when the user says "just facts", "facts only", "as facts", "give me the facts", or replies with a bare "facts" / "facts?" to a previous message — then the scope is that message's content.
---

# factual-communication

Restate content as facts, in the style of av/facts fact sheets (github.com/av/facts). The output is a flat list of atomic claims: short enough to read in full, complete enough that nothing in scope is lost.

## Trigger

- Explicit: "just facts", "facts only", "as facts", "give me the facts".
- Implicit: a bare reply "facts" (or "facts?") to a previous message → the scope is that previous message's content (yours or anyone's). If ambiguous, take the most recent substantive message in the thread.
- Scope = the content, not the conversation. Rehash what was said/reported, not meta-commentary about it.

## Output format

One fact per line, `-` prefixed. Group with `#` headings only when there are 2+ distinct domains; skip headings for short outputs. No intro, no outro, no transitions, no "in summary". The fact list IS the message.

```
# billing
- MRR is $48.2k, up 6% MoM [stripe, 2026-08-25]
- 3 enterprise deals in contract stage
- Brain Restore Centers closed at $500/mo

# risks
- churn concentrated in workspaces without custom skills
- VIK-2058 unassigned until 07:20Z, now with Ivan
```

## Fact-writing rules

- **Atomic** — one fact = one truth. Split compound sentences. Each line stands alone with no dependence on neighbors.
- **Minimal but sufficient** — the test in both directions:
  - Sufficient: a reader with only the fact list loses no decision-relevant information from the source. Numbers, names, dates, statuses, causal links, and caveats all survive.
  - Minimal: remove any fact and something is lost; remove any word and precision drops. No hedging, no adjectives that don't constrain meaning, no restating a fact in different words.
- **Declarative present tense** where possible. "Deploy failed at 14:02" not "it appears the deploy may have failed".
- **Concrete over abstract** — keep the number, drop the characterization ("up 6%" not "healthy growth"). If the source only had the characterization, keep it but keep it short.
- **Preserve epistemic status** — distinguish known / claimed / uncertain. Mark non-verified claims inline: `- vendor claims fix ships Friday (unverified)`. Never upgrade a guess to a fact.
- **Keep attribution and provenance** when it matters: who said it, which source, which date — `[source, YYYY-MM-DD]` for volatile data.
- **Drop entirely:** greetings, transitions, motivation/context the reader already has, recommendations unless they were part of the source content (then state them as facts: `- Viktor recommends X because Y`).
- **Order by importance**, not source order, unless the source is a sequence (timeline, steps) — then preserve order.

## Sizing

- Bare "facts" reply to a message: usually 3–15 lines.
- Rehashing a document/report: sections + facts, still readable in <60 seconds.
- If the source is already minimal, say so in one line and don't pad.

## Anti-patterns

- Bullet-ifying prose sentence-by-sentence (that's reformatting, not fact extraction).
- Losing a caveat or number to hit a line count.
- Adding analysis or facts not present in the source scope. If a critical gap exists, one final line: `- not covered in source: X.`
