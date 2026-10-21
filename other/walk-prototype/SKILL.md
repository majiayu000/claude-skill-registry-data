---
name: walk-prototype
description: Understand a working prototype by using it, the way the people it serves would. Works out who it serves and what each sets out to do, then walks each journey a step at a time through the walk_prototype.py browser script — click, type, press a key, go back — and records every step and what it showed, until the person gets what they came for or the prototype stops them. Writes journeys.yaml (who, sets out to do, steps, ends with) with every captured view placed on a journey or named as not walked, with why; the step pictures and text are kept as evidence. Never changes data on a deployed site the person has not cleared. Used by /intent before it drafts intents from a prototype (C15).
user-invocable: false
model: sonnet
effort: medium
allowed-tools: Read, Write, Bash, Glob
---

# walk-prototype

A screen shows what a prototype has. A journey shows what it is *for*: who comes to it, what
they set out to do, and what they get. `/intent` drafts business intents from that — so a
business intent says what a person gets, not what the screens hold or what rules they enforce.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `source` | yes | The prototype: a file path, a local page, or a link |
| `source_manifest` | yes | The capture's manifest — its `view-…` files are the views the journeys must cover |
| `may_change_data` | yes | `true` for a file or a local prototype; for a deployed site, what the person said (`true` only when they said it is safe) |
| `walk_script` | yes | `<play-dir>/scripts/walk_prototype.py` |
| `check_script` | yes | `<play-dir>/scripts/check_journeys.py` |
| `journeys_path` | yes | Where to write `journeys.yaml` |
| `evidence_dir` | yes | Where the step pictures and text go (`<source evidence>/journeys/`) |

## Process

1. **Read the captured views** — every `view-…` text (and picture) the manifest lists, and the
   first screen. List the views by name.
2. **Work out who the prototype serves and what each sets out to do.** Start from its main
   sections — the tabs, the top-level menu, the parts of its first screen. **Every main section
   is some journey's goal** (a person comes to it for a reason), so a section is never only a
   step on the way to another goal; a review tool's product view is a journey of its own, not
   part of reading one change. From what the screens
   say to their users — headings, help text, empty states, the names of actions — name each
   kind of person and each thing they come to do. Write the goal as what they want to have at
   the end, in their words ("get through everything the drive changed and approve it"), not as
   a feature ("use Catch up"). Sample data inside a prototype is sample data: the shop in a
   review tool's mockup is what is being reviewed, not who the tool serves.
3. **Walk each journey a step at a time.** Start from the first screen. Each step is one call:

   ```bash
   python3 <walk_script> --source <source> --steps <evidence_dir>/<journey>.steps.json \
       --out-dir <evidence_dir> --name <journey>-NN --session <journey> [--allow-changes]
   ```

   The steps file holds every step so far plus the next one (`click`, `type`, `press`, `back`;
   a target by its words or `#n`). `--session` keeps the journey's browser open, so a step
   costs well under a second. The answer tells you **only what changed** (`added` lines, `gone`
   count) and the `controls` and `fields` now on screen: read that, not the whole page — open
   `<journey>-NN.txt` only when the change is not enough to decide. Choose the next step from
   what a person with this goal would do now. When the journey ends, run
   `python3 <walk_script> --session <journey> --stop`. Go on until the person has what they came for, or the prototype stops
   them (a step that cannot be taken is a finding, not a failure — note it and try another
   way). Walk deeply: through cards one after another, into a piece and back out, a comment
   typed, an answer given. Pass `--allow-changes` only when `may_change_data` is `true`.
4. **Cover every view.** For each captured view no journey reached, find the journey that
   would — a person who needs it — and walk it; or, if no person's goal leads there (a help
   panel, a decorative toggle), list it under `not_walked` with why.
5. **Write `journeys.yaml`:**

   ```yaml
   journeys:
     - id: approve-a-drive
       who: the product owner who asked for the drive
       sets_out_to: get through everything the drive changed and approve what is right
       steps:
         - do: open Catch up
           shows: the first changed piece as a card, 18 to go
           view: [approve-a-drive-01.png, approve-a-drive-01.txt]
           covers: [view-14-catch-up--18]      # the captured views this step reached
         - do: press → on a business intent
           shows: it is approved and the next card opens
           view: [approve-a-drive-02.png, approve-a-drive-02.txt]
       ends_with: every change answered; Finish review unlocks
       could_not: []                           # steps the prototype did not allow, with why
   not_walked:
     - view: view-35-later-keep-unread
       why: the same card as the step before, reached by swiping left
   ```

6. **Check it:**

   ```bash
   python3 <check_script> --journeys <journeys_path> --source-manifest <source_manifest> \
       --evidence-dir <evidence_dir> --out <journeys_path dir>/journeys-check.json
   ```

   Fix every gap (walk the missing journey, add the step's `shows`, name the view with why) and
   run it again until it reads `ok: true`.

## Output

`journeys.yaml` at `journeys_path`, the step files under `evidence_dir`, and
`journeys-check.json` beside `journeys.yaml`.

## Rules

- Walk; do not guess. Every `shows` is what the step's answer shows.
- Every main section of the prototype is some journey's goal.
- A goal is what the person wants to have, never a screen or a rule.
- Never take a data-changing step on a deployed site unless `may_change_data` is `true`.
- No view is left silent: on a journey, or named as not walked, with why.
