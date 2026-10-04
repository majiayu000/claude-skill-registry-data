---
name: timeline
description: Build or extend a dated chronology of the issue from material/ and sessions/, separating what is documented from what is recalled. Use when the user asks "what does the timeline look like", when preparing for an appointment, or when accounts of the same period disagree.
---

# timeline

A chronology is the highest-value artefact in this workspace and the one a person is least able
to build for themselves while inside the thing. It is also what a therapist, a lawyer, an HR
process or a doctor will ask for first.

## Sources, in order of weight

1. **Documented** — anything in `material/`: messages with timestamps, emails, calendar entries,
   photos with EXIF dates, medical letters, payslips.
2. **Recalled** — session notes. Dated to when the event happened, not when it was told to you.
3. **Approximate** — "sometime that spring". Keep it, mark it.

Never silently promote recalled to documented. The distinction is the value of the artefact.

## Output

`artefacts/timeline.md`, rebuilt in place (this artefact is the exception to append-only; keep
the previous version in `archive/` when it changes substantially).

```markdown
---
type: artefact
kind: timeline
updated: 2026-08-14
built_from: [material/*, sessions/260714-*, sessions/260801-*]
---

# Timeline — <issue>

| Date | What happened | Source | Confidence |
| --- | --- | --- | --- |
| 2024-03-11 | <one line, factual, no interpretation> | material/240311-email.eml | documented |
| 2024-04 (approx) | ... | sessions/260714-first | recalled |

## Gaps
Periods with nothing in them, and whether that's because nothing happened or because
nothing was kept.

## Contradictions
Where two sources disagree about the same event. State both. Do not resolve them
by picking the more recent account.
```

## Procedure

1. Inventory `material/` — list what exists and what date range it covers.
2. Extract dated events. One row per event. Factual sentence only: who did what, when. No
   adjectives, no motive.
3. Pull recalled events from session notes, dating them to the event.
4. Sort. Mark gaps of more than a month where the issue was presumably still live.
5. Flag contradictions explicitly rather than choosing.
6. Show the person the gaps and ask if they have material that fills them — this is usually the
   moment they remember the folder of screenshots.

## Rules

- **One line per event, no interpretation.** "M said the project was fine" not "M was being
  dishonest about the project".
- **Absolute dates always.** Approximate is `2024-04 (approx)`, never "last spring".
- **Cite every row.** A row without a source is a row you invented.
- **Do not fill gaps by inference.** An empty stretch stays empty.
- If the material is emotionally heavy to go through, say so before starting, and offer to do it
  in passes rather than one sitting.
