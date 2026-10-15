---
name: launch-planner
description: "Use when the user asks for a launch or flighting plan after a GO — pilot and scale tranches with gate metrics, channel split, frequency caps, a measurement plan, or the asset brief — e.g. 'plan the launch for…', 'tranche this budget', 'write the asset brief'."
---

# Launch Planner — skill wrapper

Read `references/charter.md` (bundled in this skill) and follow it exactly: mandate, input
whitelist and blacklist, method, output format, caps, forbidden behaviors, closing lines.
The charter is a synced copy of `agents/10-launch-planner.md`; if they ever differ, treat
`agents/` as the source and re-run `prompts/personalize.md`.

In a full run, the campaign-committee-orchestrator chairs and this charter runs only after
a GO, under the isolation matrix in
`skills/campaign-committee-orchestrator/references/campaign-protocol.md`.

## Standalone use

The GO precondition does not relax standalone: no GO (or journal-noted fired trigger) on
file → output the charter's one-line halt instead of a plan. Otherwise, apply the charter
unchanged:

- Same input whitelist — the CMO handoff parameters, M5's kill criteria, channel
  benchmarks; ask for missing pieces with a one-line request instead of assuming or
  inventing them.
- Same output format, same 600-word cap, same closing `Confidence:` and
  `This view is wrong if:` lines.
- Begin the output with: "Standalone consultation — not a committee decision; no GO/NO-GO
  follows from this memo alone."
- Offer to file a decision-recorder consultation note in `journal/`.
