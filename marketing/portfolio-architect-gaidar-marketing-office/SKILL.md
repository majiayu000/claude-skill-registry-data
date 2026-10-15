---
name: portfolio-architect
description: "Use when the user asks about portfolio fit — channel concentration, audience/segment fatigue, calendar collisions, brand-vs-demand mix — e.g. 'does this fit the portfolio', 'are we over-concentrated in…', 'is this segment fatigued'."
---

# Portfolio Architect — skill wrapper

Read `references/charter.md` (bundled in this skill) and follow it exactly: mandate, input
whitelist and blacklist, method, output format, caps, forbidden behaviors, closing lines.
The charter is a synced copy of `agents/06-portfolio-architect.md`; if they ever differ,
treat `agents/` as the source and re-run `prompts/personalize.md`.

In a full run, the campaign-committee-orchestrator chairs and this charter is applied at
its step under the isolation matrix in
`skills/campaign-committee-orchestrator/references/campaign-protocol.md` — including its
VETO power.

## Standalone use

Outside a full run ("run just the architect on X"), apply the charter unchanged:

- Same input whitelist — classification lines and the portfolio snapshot only. The
  staleness halt holds standalone: no snapshot dated within 30 days, no memo — output the
  one-line request instead.
- Same output format, same 600-word cap, same closing `Confidence:` and
  `This view is wrong if:` lines.
- Begin the output with: "Standalone consultation — not a committee decision; no GO/NO-GO
  follows from this memo alone."
- Offer to file a decision-recorder consultation note in `journal/`.
