---
name: reality-show
description: >-
  Keep serialized build-in-public content continuous: read one canon file of season, arcs, beats
  and loops and say which narrative beat to advance next, so episodes chain into a series. Pairs
  with the episode adapter, which does the writing. Triggers: "/reality-show", "season state",
  "what arcs are open".
license: MIT
---

REALITY-SHOW v2 — the season continuity layer on top of a SINGLE CANON

GOAL: make the stream of episodes read like a SERIES. `/episode` writes one episode with dramaturgy (palette [[style-reality-show]]); THIS skill remembers the SEASON and suggests the next narrative move.

**SOURCE OF TRUTH = the canon:** `$OBSIDIAN_VAULT/04-Projects\show-canon\`
(season-01.md · arcs\ · beats\ · loops\ · rules\; the map is `_SHOW-CANON.md`).
⛔ **season-state.json is FROZEN as of 2026-07-10** (`_imports\content-factory\season-state.json` + season_state.py) — it was the third diverging spine after THREADS/SHOW-STATE; decision `decision-single-canon-story-state`. Do NOT read it as truth, do NOT update it.

## MODES

### `status` (default, read-only, 0 LLM tokens)
Read `season-01.md` (the season question, active arcs, open loops, the board) + the headers of `arcs\*.md` (status, current_state) + `loops\*.md` (open?) → a one-line digest for the owner: the season + arcs with their stakes + dangling cliffhanger loops + story_day. Nothing is changed.

### `next` — propose the beat for the next episode (authorial model, cheap)
1. Read: season-01.md + open loops + fresh beats in `beats\` (happened, latest by occurred_on) + the 📝 inbox `_imports\content-factory\triage\posts.md` (fresh post material). Do NOT read the whole corpus.
2. Judgement (top-tier model): which OPEN arc today's material should advance; which loop to close or sharpen; which motif to bring back (running gag). It must connect to a REAL beat — never invent events. `beat_kind` hints at the dramaturgy: 🌀 twist / 💥 fail = cliffhanger; 🏆 milestone = payoff; 📡 external = fuel for the season's intrigue.
3. Output 1-2 options: "arc X → sharpen (loop '…'), bring back the motif '…', anchored on beat-YYYY-MM-DD-slug". After that `/episode` writes the episode.

### `intake` — process the beats inbox (sensor candidates → canon)
At night this is done by the routine `canon-writer-nightly` (01:00); here it is the same thing on demand.
`python $IMPORTS_ROOT/content-factory\canon_intake.py list` → judge fitness and the ARC (only from the live dictionary!) → `... accept <beat_id> --arcs arc-a,arc-b` or `... reject <beat_id> --why "..."`.
The script itself: validates arc_id against the arc files, sets the derived `story_day`, moves it into `beats\`, appends the back-link into the arc, cleans `_README`. Never move beats by hand.
`canon_intake.py verify` — the detector of half-finished intake (a beat sits in `beats\` while the arc does not reference it: a break, or a race between two writers). Runs at the end of the nightly pass; exit 1 = fix it.

### `board` — the season board (derived, not handwritten)
`python $IMPORTS_ROOT/content-factory\show_canon_sync.py board` (before→after) / `board --apply` (write it).
`season-01.active_arcs` / `open_loops` are rebuilt from the `status:` fields in the arc/loop files. Rule: **the board is never edited by hand** — otherwise the copy falls behind the truth (the BOARD-DRIFT incident 07-27: an arc lived in the files for 16 days while the board did not show it). `show_canon_sync.py arcs` prints the live arc_id dictionary — the contract for the sensors.

### Updating the state = EDITING THE CANON (with explicit actions, not silently)
Everything that used to be written into json is now an edit of canon cards, from the templates:
- a new line → `arcs\arc-<slug>.md` (modelled on the existing ones); escalation/closure → edit the arc's `current_state`/`status`;
- open/close a cliffhanger → `loops\loop-<slug>.md` (status: open/closed + current_best_answer);
- link an episode → append consequences to the anchoring beat ("episode <slug> published") and to the arc's beats[].
After the edits: `python $IMPORTS_ROOT/content-factory\canon_render.py` (the GitHub registries update themselves; the linter will complain about broken fields).

### `recap --arc <id>` — "previously on"
The arc's beats (beats[] from the arc card, by occurred_on) + its open loops → a 1-2 line recap for the new episode.

### `check` — the weekly health scorecard of the series
A deterministic engine (0 tokens): `python $IMPORTS_ROOT/content-factory\show_canon_check.py check` (+ `status` for context). Axes: (1) Continuity — the season question is set + ≥3 beats happened; (2) Change — the share of active arcs that have beats; (3) Loops — more than 4 open = a jam, more than 2 in one arc = overload; (4) Trust (manual, receipts; the script reports the share of fresh beats carrying evidence_refs). Plus board drift (season-01.open_loops vs the real loop files) and a jammed beats inbox. Exit 0=OK · 1=FLAGS (a diagnosis) · 2=could not measure. The judgement verdict belongs to the top model / the owner. Weekly (routine `reality-show-health-weekly`) or on demand.

## HOW IT WIRES INTO THE PIPELINE
An event → a BEAT into the canon (template `beats\_TEMPLATE-beat.md`) → `/reality-show next` (pick the move) → `/episode` writes the episode → publication through the gates → `/reality-show` records the consequences IN THE CANON → canon_render.py refreshes the public registries.

## BOUNDARIES
- Read-only by default (`status`/`recap`/`next`/`check`); canon edits happen through explicit, announced actions.
- The owner's voice = the top-tier model (if the session runs a weaker one, delegate the `next` judgement to a subagent with `model:'opus'`).
- Draft-first outbound: `/episode` publishes on a "+". Tier-2 outbound → pause and ask.
- Privacy: secrets OUT; respect the `reveal` axis (never burn live_hold/spoiler_until in outbound recaps). Serialization comes from REAL beats, never from invention.
- AK-47: one SKILL.md, no separate store any more (the canon IS the store). Canon laws: `decision-single-canon-story-state` + `_SHOW-CANON.md`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
