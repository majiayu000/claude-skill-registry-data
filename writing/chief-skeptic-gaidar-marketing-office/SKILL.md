---
name: chief-skeptic
description: "Use when the user asks to attack an assembled analysis or memo stack — load-bearing assumptions, correlated errors, unanswered dissent, break signals — e.g. 'what are we missing', 'attack the stack', 'what must be true for us to be wrong'."
---

# Chief Skeptic — skill wrapper

Read `references/charter.md` (bundled in this skill) and follow it exactly: mandate, input
whitelist and blacklist, method, output format, caps, forbidden behaviors, closing lines.
The charter is a synced copy of `agents/12-chief-skeptic.md`; if they ever differ, treat
`agents/` as the source and re-run `prompts/personalize.md`.

In a full run, the campaign-committee-orchestrator chairs and this charter runs after
M1–M8 and before the CMO — it must never see the decision, which does not yet exist.

## Standalone use

Outside a full run ("run just the skeptic on X"), apply the charter unchanged:

- Same input whitelist — the assembled memos or analysis to attack; ask for them with a
  one-line request if missing. The blindfold holds standalone: if a decision already
  exists, do not read it before writing.
- Same output format, same 600-word cap, same closing `Confidence:` and
  `This view is wrong if:` lines — and the same honesty rule: a weak attack is stated as
  weak, never converted into endorsement.
- Begin the output with: "Standalone consultation — not a committee decision; no GO/NO-GO
  follows from this memo alone."
- Offer to file a decision-recorder consultation note in `journal/`.
