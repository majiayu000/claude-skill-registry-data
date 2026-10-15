---
name: decision-recorder
description: "Use when the user asks to journal a decision or run, log an override, file a consultation note, or run the quarterly audit of predictions vs. actuals — e.g. 'log this decision', 'record the override', 'run the quarterly audit', 'write the journal entry for…'."
---

# Decision Recorder — skill wrapper

Read `references/charter.md` (bundled in this skill) and follow it exactly: mandate, input
whitelist (everything, including the principal's action and override text), method, output
format, forbidden behaviors. The charter is a synced copy of
`agents/11-decision-recorder.md`; if they ever differ, treat `agents/` as the source and
re-run `prompts/personalize.md`. Journal entries and audits follow
`templates/journal-entry.md` and are exempt from the 600-word cap.

In a full run, the campaign-committee-orchestrator chairs and this charter closes every
run — no run of any kind is complete without its entry or note.

## Standalone use

Outside a full run, apply the charter unchanged:

- Same rules — every field filled ("not stated"/"none" valid, blanks not); overrides
  verbatim, in quotes, dated; nothing paraphrased; ask for missing facts with a one-line
  request instead of reconstructing them.
- The audit works standalone too: replay entries against actuals the user pastes; missing
  actuals are "no data pasted", scored unresolvable — never invented.
- Note at the top of the entry that it was produced standalone, and which run or event it
  records.
