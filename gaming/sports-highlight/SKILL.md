---
name: sports-highlight
description: "Sports highlight and recruiting-reel editor for Claude: finds the big moments in game footage from crowd and commentary peaks, orders them best-first or chronologically, adds freeze-frame spotlights on the athlete, a player ID card and a scoreboard, and cuts it to a high-energy track in 16:9 and 9:16. Use when the user says 'make a highlight reel from this match', 'recruiting video for my son', 'game highlights', 'best plays compilation', 'cricket / football / basketball highlights', 'season highlight', or hands over game footage. Runs on video-studio-core (timeline highlights, freeze, speed ramps, beats, colour, deliver, QC)."
license: MIT
---

# Sports Highlight

The plays that matter, in the right order, with the right player unmistakably marked.

- **Best for:** match and season highlights, recruiting / scouting reels, school and club sport, esports clips (see gaming-vod)
- **Inputs:** game footage (broadcast, sideline or phone), player name / number / position / stats, team logo, track
- **Default skin:** `data-story` · alternatives `chaos-stack`, `bold-bounce`, `countdown-list`
- **Formats:** 16:9 reel, 9:16 clips
- **Durations:** recruiting reel 2-4 min (under 5), match highlights 1-3 min, social clips 15-45 s
- **Genre preset:** `--genre sports-highlight` (`python CORE/scripts/editor.py genre sports-highlight`)

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- Ask for: player name, jersey number and colour, position, grad year / school, height-weight or key stats, coach
  contact (recruiting), team names and final score, and timestamps of plays they already know.
- **Rights and minors:** broadcast footage is usually owned by the league or broadcaster; use it for a private
  recruiting link, not public monetised posts. Minors: get a parent's OK before posting.

## How a pro cuts this

**Structure (% of length)**

| beat | % | what goes here |
| --- | --- | --- |
| best play | 10 | the single best moment first (recruiters often stop after 30 s) |
| highlights | 75 | 10-25 plays; recruiting: grouped by skill (scoring, defence, passing); match: chronological |
| stats / contact card | 15 | player card, stats, school, contact, coach reference |

**Pacing.** ASL 2-5 s. Each play: 1-2 s of set-up, the action, 0.5-1 s of reaction, out. Do not trim so tight the play
loses context (where the ball came from). Replays: one slow repeat for the very best plays only.

**Identification (what the client judges).** Before every play the viewer must know which player to watch: a freeze
frame with a spotlight / ring on the athlete for ~1 s, then the play at full speed. Same marker style every time.

**Cut rules.** Start each clip before the action (pass, snap, run-up); cut after the result and one reaction beat.
No cutaways in the middle of a play. Speed ramps only into the key contact (0.4-0.5x), then snap back.

**Transition grammar.** Straight cuts between plays on the beat; a dip to white (8-12 frames) before a replay; dip to
black before the player card. No glitch, no spin.

**Music and sound.** High-energy track (bed ~-10 dB), keep crowd roar and the ball sound under it; for recruiting reels
some coaches prefer game sound only: ask. SFX: an impact on a big hit or the freeze, sparingly.

**Colour.** `punchy` or `bleach-bypass` (gritty) for match reels; `documentary-natural` for recruiting (accurate jersey
colours). Match broadcast and phone footage first.

**Captions.** None on the plays. Text = player card, scoreboard / minute, skill labels ("Defence").

**What the client judges.** Clear player identification, best plays first, length under 5 min, correct stats.

**Common mistakes.** Opening with a slow intro; plays without a marker; 20 s of nothing before each play; music drowning
the action; wrong jersey number; long slow-motion everywhere.

## Make the edit

`highlights` mode scores loudness + motion every 0.25 s and keeps the top windows (~3 s each, up to 6 per file):
crowd roar and commentary spikes become candidates. It cannot read the scoreboard, see the ball or know which player
is yours: you pick the real plays. `run.py` does not pass `--model` to `timeline.py auto`, so dry-run it directly.

```bash
python CORE/scripts/timeline.py auto game1.mp4 game2.mp4 --work sh --mode highlights --duration 150 --format 16:9 --model base --dry-run
#   watch each candidate (in/out in sh/timeline_spec.json), drop non-plays, widen windows (start 2 s earlier),
#   add plays you know by time, reorder (best first), add freezes and ramps (below), set "audio": "keep" or "duck"
python CORE/scripts/run.py - --timeline sh/timeline_spec.json --style SKILLS/data-story --genre sports-highlight --format 16:9 --no-cut --music track.wav --model base --work sh --stop-after plan
python CORE/scripts/render.py sh/plan.json --frames 1,8,20,45,90
python CORE/scripts/render.py sh/plan.json
python CORE/scripts/finish.py sh/plan.json --platform youtube
```

Spec clip with the athlete marker moment and a ramp into contact:

```json
{"src": "../game1.mp4", "in": 1312.0, "out": 1320.5, "audio": "duck",
 "freeze": [{"at": 1313.2, "dur": 1.0}],
 "speedRamp": [{"at": 1317.6, "rate": 0.45, "ramp": 0.4}, {"at": 1318.6, "rate": 1.0, "ramp": 0.2}]}
```

Vertical clips per play: `python CORE/scripts/track.py reframe sh/source.mp4 --out sh/v.mp4 --format 9:16 --follow primary --mode fast`
works only when the athlete's face is visible and large; for wide game footage use a centre crop or build the vertical
from tighter sideline clips with `--format 9:16`.

## Refine the plan

- **Delete the `captions` element** and clear `words` (commentary transcripts are noise here); set
  `"audio": {"platform": "youtube", "voice": false}` so crowd sound is not compressed like dialogue.
- **Spotlight on the freeze** (times on the cut timeline; read the freeze time from `sh/timeline.json`):
  `{"type": "shape", "kind": "spotlight", "x": 1210, "y": 520, "w": 320, "h": 320, "start": 14.2, "end": 15.2}` plus
  `{"type": "callout", "point": [1210, 520], "x": 1500, "y": 260, "title": "#23 Maya Ortiz", "start": 14.2, "end": 15.2}`.
  Same colour and size for every play. (`anchorTo: "face"` only follows the main detected face, rarely your player in a wide.)
- **Ring alternative:** `{"type": "shape", "kind": "ring", "x": 1210, "y": 520, "w": 220, "h": 220, "color": "#FFD400"}`.
- **Player card (end and/or start):** `card` with `kicker` "CLASS OF 2027", `title` name and number, `items` stats; or
  `counter` elements for 2-3 headline numbers.
- **Skill labels:** `chip` "DEFENCE" for 1.5 s at the start of each group. **Scoreboard:** `chip` "2-1 · 78'" top-left.
- **Music:** `"music": {"src": "track.wav", "under": 10, "duck": false, "fitTo": "beats", "endButton": true}`.
- **SFX:** `{"t": 14.2, "kind": "impact", "gain": 0.4}` on freezes (or none). **Colour:** `"color": {"look": "punchy", "intensity": 0.7}`.
- `python CORE/scripts/editor.py review sh/plan.json --genre sports-highlight`.
- **Footage clean-up (video, before the spec):** phone footage from the stands and floodlit night games: `python CORE/scripts/prep.py game1.mp4 --work fix/g1 --stabilize --deflicker --fps 60` (keep `--fps` at the source rate; prep defaults to 30), then use `fix/g1/source.mp4` in the spec. `--stabilize` = vidstab (crops ~6% at the edges), `--denoise light|strong` = video noise, `--deflicker` = mains-light flicker. Only on clips that need it. Feed `fix/g1/source.mp4` to `timeline.py auto` instead of the raw file. `--denoise light` for dark indoor venues.

## Deliver

```bash
python CORE/scripts/deliver.py sh/plan.json --to youtube --out-dir sh/deliver --burn no --headline "Maya Ortiz #23 2026 Highlights"
python CORE/scripts/deliver.py sh9/plan.json --to reels,tiktok,shorts --out-dir sh9/deliver --burn no
python CORE/scripts/qc.py sh/deliver/final_youtube.mp4 --plan sh/plan.json --platform youtube --strict
```

Recruiting: deliver an unlisted YouTube link plus the MP4; put name, number, position, school, GPA/contact in the first
10 s and on the end card. Name files `maya-ortiz_23_2026_highlights_v001.mp4`.

## Check before delivering

- Every play has the marker on the right player (check jersey number on each freeze); plays start early enough to read.
- Best play inside the first 10 s; total under 5 min for recruiting.
- Stats, name, number, school spelled and correct (ask the player / coach to confirm).
- Freeze frames are silent by design: confirm the music covers them. `qc.py` passes loudness and flash checks.
- Tell the user the plays used (with source timestamps) and which candidates you rejected.

## Example requests

- "Make a recruiting reel for my son, number 7, centre back, best plays first."
- "Highlights of yesterday's match in 2 minutes with the goals and big saves."
- "Vertical clips of each of her three-pointers for Instagram."
