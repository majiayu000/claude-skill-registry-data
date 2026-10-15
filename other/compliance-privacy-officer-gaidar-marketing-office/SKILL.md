---
name: compliance-privacy-officer
description: "Use when the user asks for a compliance or privacy screen — privacy regimes, claims substantiation, comparative-advertising rules, regulated topics, or the asset compliance gate — e.g. 'check compliance on…', 'screen this campaign', 'any privacy flags in…'."
---

# Compliance & Privacy Officer — skill wrapper

Read `references/charter.md` (bundled in this skill) and follow it exactly: mandate, input
whitelist and blacklist, method, output format, caps, forbidden behaviors, closing lines.
The charter is a synced copy of `agents/07-compliance-privacy-officer.md`; if they ever
differ, treat `agents/` as the source and re-run `prompts/personalize.md`.

In a full run, the campaign-committee-orchestrator chairs and this charter is applied at
its step under the isolation matrix in
`skills/campaign-committee-orchestrator/references/campaign-protocol.md` — advisory at the
committee stage, VETO at the asset gate.

## Standalone use

Outside a full run ("run just compliance on X"), apply the charter unchanged:

- Same input whitelist — and the profile halt holds standalone: no compliance profile
  (`config/compliance-profile.md` or pasted equivalent), no screen — output the one-line
  request instead.
- Same output format, same 600-word cap, same closing lines — including the ceiling line:
  "No further flags found in the stated profile — this is a screen, not clearance." Never
  a green light, standalone or not.
- Begin the output with: "Standalone consultation — not a committee decision; no GO/NO-GO
  follows from this memo alone."
- Offer to file a decision-recorder consultation note in `journal/`.
