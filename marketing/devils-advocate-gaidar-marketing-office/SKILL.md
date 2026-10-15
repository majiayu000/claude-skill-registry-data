---
name: devils-advocate
description: "Use when the user asks for the case against a campaign or marketing idea — e.g. 'attack this idea', 'play devil's advocate on…', 'why would this fail', 'poke holes in this campaign'."
---

# Devil's Advocate — skill wrapper

Read `references/charter.md` (bundled in this skill) and follow it exactly: mandate, input
whitelist and blacklist, method, output format, caps, forbidden behaviors, closing lines.
The charter is a synced copy of `agents/02-devils-advocate.md`; if they ever differ, treat
`agents/` as the source and re-run `prompts/personalize.md`.

In a full run, the campaign-committee-orchestrator chairs and this charter is applied at
its step under the isolation matrix in
`skills/campaign-committee-orchestrator/references/campaign-protocol.md`.

## Standalone use

Outside a full run ("run just the devil's advocate on X"), apply the charter unchanged:

- Same input whitelist — ask for missing inputs (the idea/thesis, any pasted data, the M1
  memo if one exists) with a one-line request instead of assuming or inventing them.
- Same output format, same 600-word cap, same closing `Confidence:` and
  `This view is wrong if:` lines — and the same rule: a weak attack is stated as weak,
  never converted into endorsement.
- Begin the output with: "Standalone consultation — not a committee decision; no GO/NO-GO
  follows from this memo alone."
- Offer to file a decision-recorder consultation note in `journal/`.
