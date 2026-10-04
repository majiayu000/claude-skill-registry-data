---
name: decide
description: Use when the user faces a real decision with stakes and wants it framed cleanly — options, ranked criteria, a recommendation, the falsifier, and reversibility — then logged to decisions/log.md. Trigger on "/decide", "help me decide", "should I X or Y", "frame this decision", "what's the call here", "log this decision".
---

# Decide

Turn a fork in the road into a clear, logged decision — reasoning visible, and the way you'd know you were wrong stated up front.

## When to run
- A real choice with stakes (a tradeoff, a hire, a vendor, a direction, a bet).
- After `/structure` surfaces a "Decision needed."

## The output (always this shape)
```
## Decision — <the question> · <date>
**Context** — why this is on the table now (2–3 lines).
**Options** — each with its main upside + main cost/risk (include "do nothing").
**Criteria** — what actually matters here, ranked.
**Recommendation** — the call + the why, in one paragraph.
**Falsifier** — what we'd later see that would prove this was the wrong call (Verification Gate).
**Reversibility** — one-way or two-way door? (two-way → decide fast and move).
**Owner / next step** — who does what, by when.
```

## Process
1. **Frame the real question.** Strip to the actual choice (`/structure` if fuzzy). Name what is *not* being decided.
2. **Lay out options honestly** — including "do nothing." Each gets a real upside and a real cost. No strawmen.
3. **Make criteria explicit and ranked** — most decisions go wrong because the criteria were never named.
4. **Recommend.** Take a position with the reasoning. State the **falsifier** and the **reversibility** (two-way doors don't deserve one-way-door deliberation).
5. **Verify the inputs (Verification Gate).** Any fact or number the decision rests on → trace to source; flag unknowns as risks, don't paper over them.
6. **Log it.** On the user's confirmation, append the brief to `decisions/log.md` (dated) — the standing record (per "How you work with me").

## Autonomy
**L1–L2** — frames and recommends; the human makes the call. Logs it once the user confirms.

## Guardrails (from CLAUDE.md)
- **Cite, don't invent** — decisions rest on verified facts; unknowns are named as risks.
- **Log decisions** to `decisions/log.md`.
- No confidential figures or PHI/PII in the log (it's committed) — reference the source, don't transcribe.
