---
name: travel-cinematic
description: "Cinematic travel film editor for Claude: turns trip footage, drone shots and phone clips into a music-led 1-3 min travel film and a 9:16 teaser, with match cuts, direction-matched whips, speed ramps, ambience under the music and a filmic grade. Use when the user says 'make a cinematic travel video', 'edit my trip footage', 'travel reel from my holiday', 'drone montage', 'Bali / Japan / Ladakh travel film', 'hotel or destination promo', or hands over a folder of travel clips and a song. Runs on video-studio-core (timeline montage, beats, speed ramps, music fit, colour, deliver, QC)."
license: MIT
---

# Travel Cinematic

A place, felt: arrival, discovery, the peak moment and the sunset, cut on the music so the viewer wants to book a ticket.

- **Best for:** trip films, destination and hotel promos, drone montages, road trips, honeymoon films
- **Inputs:** clips (gimbal, drone, phone, GoPro), optional VO or a few spoken lines, one licensed song, ambience clips
- **Default skin:** `cinematic-phone` · alternatives `loop-ambient`, `minimal-mono`, `doc-real`
- **Formats:** 16:9 master, 9:16 teaser
- **Durations:** film 1-3 min, teaser 15-45 s
- **Genre preset:** `--genre travel-cinematic` (`python CORE/scripts/editor.py genre travel-cinematic`)

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- Ask for: places in order of the trip, the song (licensed: YouTube Audio Library, Pixabay, a paid licence), which
  shots they love, people who appear (consent for strangers in close-up), and drone rules where it was flown.
- Group clips by place or day; name them after what they show (`market-hanoi.mp4`). Montage order is the file
  modification time, so check order with `--dry-run`.

## How a pro cuts this

**Structure (% of length)**

| beat | % | what goes here |
| --- | --- | --- |
| arrival / establishing | 15 | plane window, road, first wide or drone reveal, the title |
| discovery | 35 | streets, food, people, textures; details and wides alternating |
| peak moment | 30 | the big view, the jump, the festival: the song's biggest section, speed ramps |
| reflection / sunset | 20 | slower shots, golden or blue hour, the last wide, the place name |

**Pacing.** ASL 1-3 s on the beat; drone and wide reveals 3-5 s; details 0.8-1.5 s. Change shot every 1, 2 or 4 beats:
mix them so it breathes. Slow the cut rate in the reflection section.

**Cut rules.** Match cuts carry the film: shape (a round window to a round bowl), motion (pan right into pan right),
colour. Whip transitions only between shots that both move the same direction. Cut on action a third of the way into a
move. Keep camera motion continuous across a cut (don't cut from a fast push to a static frame unless it is the drop).

**Transition grammar.** Cuts on the beat; one whip family in one direction; speed ramps into the peak; dissolve or dip to
black only for the reflection section. No more than two transition kinds.

**Music and sound.** The song leads (near full level, no duck unless there is VO), cut to length on bar lines and end on
a hit. Layer ambience (waves, market, wind) 15-20 dB under the music; drop the music for 1 s before the peak so the
ambience and the hit land. Whoosh on whips, nothing else.

**Colour.** `teal-orange-pro` (the preset grade), `ektachrome` or `fuji-velvia` for landscapes, `golden-hour` warmth,
`cinestill-800t` for night cities. Intensity 0.7-0.85. Match drone and phone first.

**Captions.** None. Place names as small titles (`chip` or `text`), the destination as a title card.

**What the client judges.** Visual flow, a sense of place, the music hit points, colour.

**Common mistakes.** Every drone shot used; shots all the same length; whips in opposite directions; music fading
mid-phrase; tilted horizons; over-saturated skin; silent visuals with no ambience.

## Make the edit

```bash
python CORE/scripts/timeline.py auto trip/ --work tc --mode montage --music song.wav --duration 120 --format 16:9 --dry-run
#   edit tc/timeline_spec.json: order by trip, drop weak shots, add ramps / whips (below)
python CORE/scripts/run.py - --timeline tc/timeline_spec.json --style SKILLS/cinematic-phone --genre travel-cinematic --format 16:9 --no-cut --model base --work tc --stop-after plan
python CORE/scripts/render.py tc/plan.json --frames 2,15,40,70,110
python CORE/scripts/render.py tc/plan.json
python CORE/scripts/finish.py tc/plan.json --platform youtube
```

One-shot draft: `python CORE/scripts/run.py - --clips trip/ --auto montage --music song.wav --duration 120 --format 16:9 --style SKILLS/cinematic-phone --genre travel-cinematic --work tc --stop-after plan`.
`--beats-per-shot 2` (on `timeline.py auto`) gives a calmer two-beat rhythm; edit individual clips for variety.

Spec moves (montage clips are muted; the song is baked into the assembly):

```json
{"src": "cliff-jump.mp4", "in": 3.0, "out": 7.5, "audio": "mute",
 "speedRamp": [{"at": 4.6, "rate": 0.35, "ramp": 0.5}, {"at": 5.8, "rate": 1.6, "ramp": 0.3}], "smooth": true,
 "transition": {"type": "whip", "dur": 0.3}}
```

`smooth: true` interpolates slow motion (slow to render, warps complex motion); footage shot at 60 fps looks better.
Ambience: give an ambience clip `"audio": "keep", "volume": 0.3` instead of mute, or keep the camera sound on a few shots.

## Refine the plan

- **Delete the skin's `captions` element** and clear `words`; set `"audio": {"platform": "youtube", "voice": false}`
  so the song is not run through the dialogue chain.
- **Spoken lines (piece to camera clips with `"audio": "keep"`):** remove the music from the spec, then
  `"music": {"src": "song.wav", "under": 16, "duck": "speech-aware", "fitTo": "beats", "endButton": true}`.
- **Colour:** `"color": {"look": "teal-orange-pro", "intensity": 0.75}`; `"finish": {"grain": 5, "letterbox": 2.39, "halation": 0.2}`
  for the widescreen film feel (not on the 9:16 teaser).
- **Title:** `{"type": "text", "text": "VIETNAM", "split": "chars", "stagger": 0.05, "start": 2.0, "end": 5.0, "in": "blurIn", "out": "fade"}`
  on a downbeat; place names `{"type": "chip", "text": "Hội An", "start": ..., "end": ...}` (check diacritics on the sheet).
- **Route:** `{"type": "map", "pins": [{"x": 0.3, "y": 0.4, "label": "Hanoi"}, {"x": 0.45, "y": 0.7, "label": "Hội An"}]}`
  (stylised dot-grid map, not real map data: say so).
- **SFX:** `{"t": 31.6, "kind": "whoosh", "gain": 0.4}` about 0.4 s before each whip; nothing else.
- `python CORE/scripts/editor.py review tc/plan.json --genre travel-cinematic`.
- **Footage clean-up (video, before the spec):** shaky handheld shots (gimbal and drone footage is already stable), night streets: `python CORE/scripts/prep.py street.mp4 --work fix/street --stabilize --denoise light`, then use `fix/street/source.mp4` in the spec. `--stabilize` = vidstab (crops ~6% at the edges), `--denoise light|strong` = video noise, `--deflicker` = mains-light flicker. Only on clips that need it. Use `--deflicker` on timelapses and hyperlapses that pump.

## Deliver

```bash
python CORE/scripts/deliver.py tc/plan.json --to youtube,youtube-4k --out-dir tc/deliver --burn no --no-post
python CORE/scripts/deliver.py tc9/plan.json --to reels,tiktok,shorts --out-dir tc9/deliver --burn no
python CORE/scripts/qc.py tc/deliver/final_youtube.mp4 --plan tc/plan.json --platform youtube --strict
```

Build the teaser as its own montage (`--format 9:16 --duration 30 --work tc9`) from the 10-15 best shots; a 16:9 film
sent to `reels` only gets a blurred fill. Name files `vietnam_film_v001_16x9.mp4`.

## Check before delivering

- Contact sheet: horizons level, skin not orange, sky not posterised, titles with correct diacritics.
- Whips match direction; ramps feel motivated; no jump from fast motion to static by accident.
- The song ends on a downbeat; ambience audible but under the music; `qc.py` passes loudness, black / flash frames.
- Drone shots legal for where they were flown; strangers in close-up OK to show.
- Tell the user the song credit, the look, and the shot list order.

## Example requests

- "Make a cinematic 2-minute film of our Japan trip with this song."
- "30-second vertical teaser of the Bali drone shots, speed ramps on the cliff jump."
- "Hotel promo from these clips, warm and calm, ends on the sunset."
