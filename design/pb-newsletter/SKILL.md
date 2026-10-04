---
name: pb-newsletter
description: >-
  Turn a pb-ship recap, a changelog range or a quick recap into a newsletter
  email draft where every claim cites a source line, and send it only after
  GO. Use for "newsletter from the recap", "write the release newsletter",
  "email update from the changelog".
category: design-ui-ux
kind: playbook
trigger: ["newsletter from the recap", "release newsletter", "email update from the changelog"]
inputs: [recap, audience]
requires:
  skills: [quick-recap, copywriting, pb-ship]
  agents: []
  mcps: []
  store: [brand-voice, email-ops]
go_points: ["send newsletter"]
outputs: ["facts.md", "newsletter.md", "run-log.md"]
verify: "every product claim in newsletter.md cites a line in facts.md"
difficulty: intermediate
est_time: 20-40 min
---

# Newsletter from a recap
What you get: a newsletter draft (subject, preheader, body) built only from facts you can trace, sent after your GO.

## Inputs
- recap — a pb-ship run log, a CHANGELOG range, or quick-recap output
- audience — who reads it, asked once
- A save folder — asked once; default `./pb-newsletter-<date>/`

## Steps
1. Check the store — `test -d ~/.claude/skills/brand-voice` and `test -d ~/.claude/skills/email-ops` → `run-log.md` (create the folder only after the recap file or range is confirmed readable) — an absent item is logged "Missing store item: <name>, install via aos-store" and the run continues with copywriting
2. quick-recap — the recap → `facts.md`, one line per fact with its source line or file — every fact cites a source
3. brand-voice if present, else copywriting — `facts.md` and the audience → `newsletter.md` with subject, preheader and body, no claim outside `facts.md` — stops for approval, edits applied until approved
4. [GO] send newsletter — through a connector the human names (email-ops if present); the recipients or list, the subject and the full text shown first. The run stops here until the human types GO. Without a connector, the GO releases a hand-off file instead: `newsletter.md` with the recipient list, you send it yourself. A sending connector is not hook-guarded, so this GO is its only guard. The GO covers exactly the audience and message shown; a changed audience needs a fresh GO.

Run log: `run-log.md` in the save folder, never committed

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
