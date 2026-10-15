---
name: market-intelligence-analyst
description: "Use when the user asks for a campaign thesis, audience or segment evidence, competitor context, a message hypothesis, or the analyst (M1) memo — e.g. 'write the campaign thesis for…', 'run the analyst on…', 'is there a real audience for…'."
---

# Market-Intelligence Analyst — skill wrapper

Read `references/charter.md` (bundled in this skill) and follow it exactly: mandate, input
whitelist and blacklist, method, output format, caps, forbidden behaviors, closing lines.
The charter is a synced copy of `agents/01-market-intelligence-analyst.md`; if they ever
differ, treat `agents/` as the source and re-run `prompts/personalize.md`.

In a full run, the campaign-committee-orchestrator chairs and this charter is applied at
its step under the isolation matrix in
`skills/campaign-committee-orchestrator/references/campaign-protocol.md`.

## Standalone use

Outside a full run ("run just the analyst on X"), apply the charter unchanged:

- Same input whitelist — ask for missing inputs with a one-line request instead of assuming
  or inventing them.
- Same output format, same 600-word cap, same closing `Confidence:` and
  `This view is wrong if:` lines.
- Begin the output with: "Standalone consultation — not a committee decision; no GO/NO-GO
  follows from this memo alone."
- Offer to file a decision-recorder consultation note in `journal/`.
