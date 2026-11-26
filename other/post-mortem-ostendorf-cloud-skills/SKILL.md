---
name: post-mortem
description: "Writes a factual post mortem for an infrastructure incident, built from events, logs and timestamps rather than memory, with a timeline, a ruled out table and no blame. Use after an incident or outage is diagnosed."
---

# Post mortem

Record what broke, in order, from evidence, once an incident is understood.

## When to use

- An incident or outage is diagnosed and resolved, or far enough along that the sequence
  is known.
- Not for a near miss caught before impact, a routine failure a runbook covers, or anything
  one pull request already explains.

## Steps

1. Apply the gate above. If no post mortem is warranted, say so and stop.
2. Read before writing, in this order: events, logs with timestamps, state or status
   timestamps, workflow or pipeline run history. Never reconstruct the sequence from
   memory or from a chat message that described it.
3. File name: `POST_MORTEM_<date>.md` at the repository root when the repository has
   no `docs/` directory. Otherwise `docs/incidents/<date>-<slug>.md`.
4. `<date>` is the day the incident started, `YYYY-MM-DD`. `<slug>` is a few words,
   lowercase, hyphenated.
5. Section order: title, Summary, Timeline, What broke, Ruled out, Why the alerts
   pointed elsewhere, Open. Drop the alerts section when nothing alerted.
6. Title: the component and the approximate duration, for example `<component>
   unreachable for about <duration>, <date>`.
7. Summary: three to five lines. State the UTC offset exactly once here, for example
   "Times are UTC. Local time is CEST, UTC+2." Every timestamp afterward is UTC alone.
8. Timeline: a table, one row per event, each row sourced from something read in step
   2. No row is estimated or remembered.
9. What broke: the mechanism, in the order it was found, with the evidence behind
   each claim.
10. Ruled out: a table, one row per candidate cause, with the evidence against it in
    the next column. A candidate without evidence against it does not belong here.
11. Why the alerts pointed elsewhere: which alert fired, what it actually measured,
    and why that differs from the real cause.
12. Open: only what is genuinely unresolved, one line each, with what would confirm
    it. An empty section is a sign the record is not finished, not a success.
13. Name components and conditions throughout. Never name the person who made a
    change, who was on call, or who responded.
14. File each follow-up action as its own issue in the tracker. Do not keep a
    follow-up list in the post mortem file.
15. Link filed follow-up issues from the Open section by number, once they exist.

## Guardrails

- Gate applied, the incident actually warrants a record.
- Every Timeline and Ruled out row traces to something read, never assumed.
- UTC offset stated once, in the Summary, never repeated per row.
- Ruled out table carries evidence against every row.
- No blame: components and conditions only, no person or team named.
- Follow-ups exist as issues, not as a list inside the file.
- File name and location match the repository layout.
- One page where the incident allows it. Depth goes in the Timeline, not in prose.

## References

- `adr` for a decision the post mortem's follow-up turns into.
