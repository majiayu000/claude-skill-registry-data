---
name: trailer-teaser
description: "Trailer and teaser editor for films, series, games, events, courses and launches: abridged three-act structure, copy cards between acts, dialogue buttons, music-driven cutting with risers into hits, 0.5-1 s of silence before the drop, an accelerating montage, the title card and a button after it. Teaser 30-60 s (mood + one hook), trailer 90-150 s. Use when the user says: make a trailer, cut a teaser, movie trailer from my film, hype video, coming soon video, launch trailer, series trailer, sizzle reel. Default skin kinetic-launch for the copy cards; any Video Studio skin works."
license: MIT
---

# Trailer / Teaser

Sell the feeling, hide the plot: three acts, cards, risers, silence, hit, title, button.

- **Best for:** short-film / feature / series trailers, event and product hype, course or channel trailers
- **Inputs:** the film or footage (clips or one long file), the strongest dialogue lines, the music (licensed; ideally a trailer track with builds and hits), title, date / CTA copy
- **Default skin:** `kinetic-launch` · alternatives `event-promo`, `logo-sting`, `swiss-poster` (use `--no-matte`)
- **Formats:** 16:9 1920x1080 (2.39 letterbox optional), 9:16 teaser, textless version, stems
- **Duration target:** teaser 30-60 s, trailer 90-150 s; genre preset `trailer-teaser`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre trailer-teaser`.
- Run `python CORE/scripts/beats.py music.wav --out tr/beats.json` first: you cut to its downbeats and hits.
- Ask: what must NOT be revealed (twist, ending), the age rating, the release date and the exact title spelling.

## How a pro cuts this

| act | % | what happens |
| --- | --- | --- |
| act 1: world | 0-30 | calm open on an image + a line; who and where; music low |
| card | - | copy card ("THIS WINTER"), 1.5-2.5 s, between acts |
| act 2: conflict | 30-65 | the problem, the stakes; dialogue lines as buttons; music builds |
| silence / drop | - | 0.5-1 s of near-silence before the big hit |
| act 3: montage | 65-88 | accelerating cuts on the beat (every beat, then every half beat), biggest images |
| title | 88-96 | title card on a hit |
| button | 96-100 | one last line or joke after the title, then date / CTA |

- **Pacing:** act 1 holds 3-5 s; act 2 2-3 s; act 3 0.5-1.2 s on the beat. Vary: never cut on every beat for long.
- **Cut rules:** cut on downbeats and phrase changes; put lines in the music's gaps; end dialogue on a hit. Out-of-context lines are normal in trailers, but they must not misrepresent the film's genre or a real person's words.
- **Transitions:** hard cuts and dip-to-black between acts; flash-white on hits sparingly; no wipe zoo.
- **Music/SFX:** music leads (no ducking except under lines); risers into hits (`riser` at hit - 1.2 s, `riser-long` at hit - 4 s), `braam` / `impact` / `boom` on hits, `sub-drop` under the title; silence before the drop.
- **Colour:** `teal-orange-pro` 0.8-1.0 or the film's own look pushed; `bleach-bypass` for action.
- **Captions:** none; text is copy cards and the title.
- **Client judges:** what it makes you feel, what it hides, whether you'd watch the film.
- **Common mistakes:** telling the whole plot, the twist in the trailer, cards on screen too short to read, every cut on every beat, no silence before the drop, the title without a hit, music cut mid-phrase.

## Make the edit

Fast first assembly on the beat (then hand-tune the spec):

```bash
python CORE/scripts/beats.py music.wav --out tr/beats.json
python CORE/scripts/timeline.py auto footage/ --work tr --mode montage --music music.wav --duration 60 --format 16:9 --dry-run
#  -> tr/timeline_spec.json: every cut on a beat. Re-order clips into the three acts, insert the dialogue clips
#     (audio "keep", put them in the music's quiet bars), dip-black between acts, then build:
python CORE/scripts/timeline.py build tr/timeline_spec.json --work tr --no-transcribe
python CORE/scripts/make_plan.py --work tr --style SKILLS/kinetic-launch --genre trailer-teaser --format 16:9 --beats tr/beats.json
python CORE/scripts/editor.py review tr/plan.json --genre trailer-teaser --fix
python CORE/scripts/render.py tr/plan.json --frames 3,15,30,50
python CORE/scripts/render.py tr/plan.json
python CORE/scripts/finish.py tr/plan.json --platform youtube
```

The montage spec puts the music in the spec (`"music": {"volume": 0.9, "duck": false}`), so the assembled file already carries it. For a trailer with many dialogue lines, set `"duck": true` there so the music dips under the lines. `make_plan.py` needs `words.json`; with `--no-transcribe` and no speech, write `{"words": []}` to `tr/words.json` first if it is missing.

Always pass `--format` matching the project: run.py and make_plan.py otherwise use the skin's own format (many skins default to 9:16).

## Refine the plan

- **Copy cards:** `{"type": "titlecard", "title": "THIS WINTER", "start": 17.9, "end": 20.0, "in": "blurIn", "out": "fade"}` - one idea per card, <= 4 words, on screen >= 1.5 s.
- **Title:** `{"type": "titlecard", "title": "FILM TITLE", "subtitle": "In cinemas 12.12", "start": 52.4, "end": 56.0, "in": "zoomOut"}` on a downbeat; `"sfx": [{"t": 51.2, "kind": "riser", "gain": 0.5}, {"t": 52.4, "kind": "braam", "gain": 0.7}, {"t": 52.4, "kind": "sub-drop", "gain": 0.5}]`.
- **Silence before the drop:** cut the music bed for 0.5-1 s (end the montage clip's music, or put a 1 s `freeze` clip with `"audio": "mute"` there) and hit on the next downbeat.
- **Flashes:** `{"type": "flash", "times": [41.2, 43.0], "color": "#fff", "opacity": 0.6, "dur": 0.12}` on the biggest hits only.
- **Scope:** `{"type": "letterbox", "ratio": 2.39}` or `"finish": {"letterbox": 2.39}`.
- **Look:** `"color": {"look": "teal-orange-pro", "intensity": 0.85}`, `"finish": {"grain": 6, "halation": 0.25}`.
- **Remove** any skin captions element (`"elements"` without `captions`).

## Deliver

```bash
python CORE/scripts/deliver.py tr/plan.json --to youtube,reels --out-dir tr/deliver
python CORE/scripts/qc.py tr/deliver/final_youtube.mp4 --plan tr/plan.json --platform youtube
```

- Teaser 9:16: rebuild the spec with `"format": "9:16"` (and `"reframe": "face"` on character shots), 30-45 s, one hook + title.
- Textless: copy the plan, remove the cards, `"outputFile": "trailer_textless.mp4"`; deliver `prores-422hq` for festivals/distributors.

## Check before delivering

- No spoilers the user flagged; dialogue lines represent the film honestly.
- Every card readable (>= 1.5 s, <= 4 words); title on a hit; button after the title.
- Silence before the drop actually silent; music ends on a resolved bar; no music cut mid-phrase.
- `qc.py`: -14 LUFS / -1 dBTP; flash frames under the photosensitivity limit (< 3 flashes per second).
- Tell the user: structure with times, music used (licence), files.

## Example requests

- "Cut a 2-minute trailer for my short film - three acts, cards, big title hit."
- "60-second teaser for our conference from last year's footage, on this track."
- "Make a vertical teaser: one line, music build, title, release date."
