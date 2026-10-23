---
name: panel
description: Run a deliberation panel of lenses on one target (a conclusion, argument, bridge or draft section) under the checked panel protocol. Blind round 1, anonymized round 2, anti-conformity with verbatim flaw quotes, locked weights, stance lines, dissent quota, novelty and agreement checks, weighted tally with splits returned to the human. Use for red team, cold bench, or any multi-lens verdict. Triggers on "panel", "convene the lenses", "red team with a panel", "cold bench panel", "have the lenses vote".
---

# Run a panel

The protocol, prompts and file layout are in `groundworks/panel/PROTOCOL.md`. Read it first. The program is `groundworks/panel/panel.py`; it decides whether the protocol was followed, not you.

## Steps

1. **Pick seats and write `panel.json`** in a new `runs/<panel_id>/` directory (inside the instance's private data area, never in this repository).
   - Seats are lenses from the instance's `roles` and `lenses`. Use distinctive seat ids.
   - Options and objection categories come from the role's `panel:` entry in `instance.yaml`.
   - Choose `weighted_seat` now, or `null`. Say why in one sentence to the user.
   - Build each seat's evidence packet from its lens view, with locators.
2. `python groundworks/panel/panel.py lock runs/<panel_id>`
3. **Round 1:** one subagent per seat, all in one message, using the round-1 prompt. Save each returned answer **verbatim** to `round1/<seat>.md`.
4. `python groundworks/panel/panel.py anonymize runs/<panel_id>`. If it fails, re-prompt only the named seats for their stance line.
5. **Round 2:** one subagent per seat, all in one message, using the round-2 prompt with `round1_anon.md` and the seat's own round-1 answer. Save verbatim to `round2/<seat>.md`.
6. `python groundworks/panel/panel.py check runs/<panel_id>`. For each `OWED` line, send the printed re-prompt to that seat only (continue the same subagent when possible), and save its full revised answer over the old file. Repeat. **Budget:** 2 re-prompts per seat per condition; then stop and report "protocol not satisfied" with the owed list.
7. `python groundworks/panel/panel.py tally runs/<panel_id>`.
   - **Exit 0:** write each row of `verdicts.jsonl` through the instance's write surface as a lens-keyed critique at agent grade.
   - **Exit 3 (split):** show the human each option's weight and its strongest argument, plus the minority report. Do not write a consensus.
8. **Report:** seats and weighted seat, result, weights, minority report, enforcement counts, and the "cannot check" list from PROTOCOL.md.

## Never

- Edit, trim or summarize a seat's answer before saving it.
- Infer a stance from prose.
- Change `panel.json` after `lock`, or delete a lock to re-lock.
- Show `anon_map.json` or real seat names to a seat in round 2.
- Treat a panel result as evidence. Gates still decide readiness.
