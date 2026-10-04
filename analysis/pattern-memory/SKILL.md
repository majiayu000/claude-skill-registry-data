---
name: pattern-memory
description: "Fires after call processing and on deal close (won or lost). Produces: reusable selling patterns extracted from deal intelligence — what tactics worked, what signals predicted outcomes, timing insights, competitive dynamics. On deal close: full win/loss synthesis with 3-5 lessons. Output contract: patterns are deduplicated against existing patterns before storing, occurrence counts incremented for recurring patterns."
user-invocable: false
---

# Pattern Memory Skill

## Purpose

Extracts reusable sales intelligence from individual deal interactions and stores them as searchable patterns. These patterns compound over time, making every future meeting prep, weekly review, and deal strategy command smarter.

## When Referenced

- After every call debrief: extract 0-2 pattern notes from the call
- On deal close (Won or Lost): run a win/loss synthesis extracting 3-5 lessons
- During meeting prep: search patterns for matches on company industry, deal size, stage, competitor, MEDDPICC profile
- During weekly review: compare all active deal states against pattern library
- During deal strategy: load patterns tagged with the relevant competitor or deal stage

## Pattern Types

| Type | Trigger | Example |
|------|---------|---------|
| signal-pattern | Detected during call debrief or quick note | "When champion uses phrase 'need to check with finance' → 70% chance EB not yet identified" |
| win-pattern | Extracted on Closed Won | "Deals that moved from Discovery to Proposal within 14 days of EB identification closed at 2x rate" |
| loss-pattern | Extracted on Closed Lost | "3 of 4 lost deals had no direct EB contact by Qualification stage" |
| competitive-pattern | Detected when same competitor appears across deals | "Gong consistently loses on pricing when deal size is under $50K" |
| timing-pattern | Detected from deal velocity data | "Average time in Qualification for won deals: 18 days. Current deal: 31 days — outside normal range" |

## Pattern File Format

**File:** `data/patterns/pattern-{YYYY-MM-DD}-{sequential}.md`

```yaml
---
_schema: 1
type: pattern
id: pattern-{YYYY-MM-DD}-{seq}
pattern_type: signal-pattern | win-pattern | loss-pattern | competitive-pattern | timing-pattern
confidence: low | medium | high
source_deals: [deal-slugs that contributed to this pattern]
source_notes: [call-note IDs that evidenced this pattern]
tags: [relevant tags: competitor names, deal stages, MEDDPICC elements]
occurrences: 1
created: {date}
updated: {date}
---

{One clear sentence describing the pattern}

**Evidence:** {Specific references to deals/notes where this was observed}

**Implication:** {What an AE should do when this pattern appears again}
```

## When Patterns Are Written

1. **After every call debrief:** The system extracts 0-2 pattern notes from the call. Not every call produces a pattern. Only write a pattern when something is genuinely reusable — a signal that predicts an outcome, a tactic that worked or failed, a competitive dynamic worth remembering.

2. **On deal close (Won or Lost):** Run a synthesis across all call notes and signals for that deal. Extract 3-5 patterns covering: what worked, what didn't, timing insights, competitive dynamics, and relationship dynamics.

3. **During weekly review:** If cross-deal analysis reveals a pattern (same signal across multiple deals), write it as a new pattern or increment the `occurrences` count on an existing one.

## When Patterns Are Read

1. **During meeting prep:** Search patterns for matches on: company industry, deal size range, current stage, active competitor, MEDDPICC profile. Surface the top 2-3 most relevant patterns.

2. **During weekly review:** Compare all active deal states against pattern library. Flag deals that match historically risky patterns.

3. **During deal strategy:** Load all patterns tagged with the relevant competitor or deal stage.

## Pattern Deduplication

Before writing a new pattern, search existing patterns for semantic overlap. If a similar pattern exists:
- Increment `occurrences`
- Add the new source deal/note to the evidence
- Update `confidence` if warranted (more occurrences = higher confidence)
- Update `updated` timestamp

## Confidence Scoring

- **Low:** Observed once. Could be coincidence.
- **Medium:** Observed 2-3 times across different deals. Likely a real pattern.
- **High:** Observed 4+ times, or validated by a won/lost outcome.

## Personalization Notes

Pattern memory is empty on day one. It builds entirely through use. After 10+ call debriefs and 2-3 deal closes, the pattern library becomes a meaningful competitive advantage. After 20+ deals, it's a personalized coaching engine that no generic tool can replicate.
