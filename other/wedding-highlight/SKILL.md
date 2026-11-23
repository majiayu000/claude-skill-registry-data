---
name: wedding-highlight
description: "Wedding highlight editor for Claude: turns a day of wedding footage, photos, vows and speeches into a 3-5 min cinematic highlight film, a 60 s vertical teaser and a ceremony cut, cut on the music with the vows as the story spine. Western weddings, elopements, engagement and anniversary films. Use when the user says 'edit my wedding video', 'make a wedding highlight', 'wedding teaser for Instagram', 'cut our vows into a film', 'same-day edit', 'wedding trailer', or hands over wedding clips plus a song. Runs on video-studio-core (timeline, beats, music fit, colour, deliver, QC). For Indian multi-event weddings use wedding-india."
license: MIT
---

# Wedding Highlight

The couple's day as a 3-5 minute film that makes the family cry at the right moment, plus a teaser they can post this week.

- **Best for:** Western weddings, elopements, civil ceremonies, engagement and anniversary films
- **Inputs:** clips from the day (prep, ceremony, portraits, party), optional photos, the vows/speech audio (camera or lav), one licensed song
- **Default skin:** `cinematic-phone` · alternatives `soft-gradient`, `minimal-mono`, `frame-studio`
- **Formats:** 16:9 highlight (master), 9:16 teaser, 16:9 ceremony
- **Durations:** teaser 30-60 s, highlight 3-5 min, ceremony as it happened (lightly cut)
- **Genre preset:** `--genre wedding-highlight` (see `python CORE/scripts/editor.py genre wedding-highlight`)

## Before you start

- This skill needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run on a machine: `python CORE/scripts/check_env.py` and fix what it reports.
- Ask before you cut: the couple's names (spelling), the date, the song (and its licence), which family members must
  appear, anything that must NOT appear (an ex, a fall, a guest who did not consent to filming).
- **Consent and privacy:** wedding footage shows guests and often children. Deliver privately; post publicly only
  with the couple's OK, and blur or drop guests who asked not to be shown.
- Copy the card dumps to a work area first. Never edit inside the camera folders or the skill folders.

## How a pro cuts this

**Structure (highlight, % of length)**

| beat | % | what goes here |
| --- | --- | --- |
| prep / anticipation | 15 | details (rings, dress, invitations), getting ready, nerves, a letter being read |
| first look / arrival | 15 | the reveal, walk down the aisle, the partner's face |
| vows / ceremony | 25 | the vows as the spoken spine, ring exchange, the kiss, recessional |
| speeches | 15 | 2-3 best lines (laugh + tear), cut as soundbites over reactions |
| celebration peak | 20 | entrance, first dance, party at the song's biggest section |
| send-off | 10 | sparklers / exit / last portrait, end on a resolved bar |

**Pacing.** ASL 2-4 s; let emotional shots hold 4-6 s (a tear, a parent's face) and run party shots at 1-2 s.
Visual change at least every 4 s. Vary shot length: never a metronome.

**Cut rules.**
- Story comes from sound: lay the vows and speech lines first (radio edit), then cover with picture.
- Cut on the beat in the party, on the phrase in the ceremony. Keep the breath before an emotional line.
- No visible jump cuts in vows or speeches: cover every join with B-roll of the couple, guests or details.
- J-cut the vows 0.5-1.5 s under the last music shot; L-cut a laugh line over the reaction it caused.
- Never fake a reaction (a guest crying at a different line) and never splice words into vows the person did not say.

**Transition grammar.** Straight cuts on beats by default; one dissolve family for time passing (prep to ceremony),
a dip to black before the send-off. Whip only in the party section. No more than two transition kinds per film.

**Music and sound.** The song leads (bed ~-6 dB), dips under vows and speech (`duck: "speech-aware"`). Cut the song to
length on bar lines (`fitTo: "beats"`) and end on a hit, not a fade. Keep natural sound (cheers, laughter, glasses) under
the music in the party. SFX almost none (a soft whoosh on a whip at most).

**Colour.** `wedding-pastel` (soft, lifted blacks) or `portra` for warm skin; `kodak-2383` for a cinematic feel.
Intensity 0.6-0.8. Match cameras first (`color.match`), skin before look.

**Captions.** None in the highlight. In the teaser and the ceremony cut, vow subtitles with `"preset": "clean"`.
Couple names + date as a `titlecard` or `text` at the open or the end.

**What the client judges.** Emotion, that every important person is in it (parents, grandparents, wedding party),
skin that looks like them, the song, and getting the teaser fast (within days).

**Common mistakes.** Opening on a logo; using every drone shot; music too loud over vows; uncovered jump cuts in
speeches; a missing grandparent; party shots all the same length; a fade-out in the middle of a phrase.

## Make the edit

The montage engine cuts on the song's beats. Clips are ordered by file modification time (capture order), so check
the order first with `--dry-run`.

```bash
# 1. beat-cut assembly of the day (clips + photos), 16:9, ~4 min, music bakes into the assembled audio
python CORE/scripts/timeline.py auto day/ --work wh --mode montage --music song.wav --duration 240 --format 16:9 --dry-run
#    edit wh/timeline_spec.json: reorder clips into the beat structure, drop weak shots, set "transition"
python CORE/scripts/run.py - --timeline wh/timeline_spec.json --style SKILLS/cinematic-phone --genre wedding-highlight --format 16:9 --no-cut --model base --work wh --stop-after plan
# 2. look at it
python CORE/scripts/render.py wh/plan.json --frames 2,20,60,120,200
python CORE/scripts/render.py wh/plan.json
python CORE/scripts/finish.py wh/plan.json --platform youtube
```

Quick one-shot version (auto order, no spec editing): `python CORE/scripts/run.py - --clips day/ --auto montage --music song.wav --duration 240 --format 16:9 --style SKILLS/cinematic-phone --genre wedding-highlight --model base --work wh --stop-after plan`.

**Vows-led cut (vows audio under picture).** Transcribe the vows clip on its own, then build a spec where the vows clip
keeps its audio and the B-roll clips are muted:

```bash
python CORE/scripts/transcribe.py --work vows --audio vows.mp4 --model base   # gives vows/transcript.json for "words"
python CORE/scripts/run.py - --timeline wh/vows_spec.json --style SKILLS/cinematic-phone --genre wedding-highlight --format 16:9 --music song.wav --model base --work whv --stop-after plan
```

In `vows_spec.json` give the vows clip `"audio": "keep"`, `"words": "../vows/transcript.json"` and a `"jcut": 1.0`;
give B-roll `"audio": "mute"`. `--music` then goes into the plan, where `finish.py` ducks it under the vows.

**Teaser (9:16, 45 s):** repeat step 1 with `--format 9:16 --duration 45 --work wt` and pick only the best 15-20 shots.

## Refine the plan

Edit `wh/plan.json` before the full render:

- **Remove creator captions** from the highlight: delete the `captions` element (the skin adds one; the genre wants none).
  Also clear `words` when the audio is only music (Whisper may "hear" lyrics).
- **Montage audio is music, not dialogue:** add `"audio": {"platform": "youtube", "voice": false}` so the dialogue chain
  does not compress the song. Vows-led cut: keep the chain, use `"voice": {"denoise": "light", "eq": "warm"}`.
- **Music (vows-led cut):** `"music": {"src": "song.wav", "under": 6, "duck": "speech-aware", "fitTo": "beats", "endButton": true}`.
- **Colour:** `"color": {"look": "wedding-pastel", "intensity": 0.7}` (or `portra`, `kodak-2383`);
  `"finish": {"grain": 4, "vignette": 0.3, "letterbox": 0}`. Mixed cameras: `"color": {"match": "hero_frame.png"}`.
- **Title:** `{"type": "titlecard", "kicker": "12.10.2026", "title": "Anna & Tom", "start": 0, "end": 3.5, "in": "blurIn", "out": "fade"}`
  or an end title in the last 4 s. Check spelling with the couple. `titlecard` is an opaque full frame (it hides the
  footage); to put the names over a shot use `{"type": "text", "text": "Anna & Tom", "y": 900, "in": "maskUp"}`.
- **Vow subtitles (teaser/ceremony):** `{"type": "captions", "preset": "clean", "dodgeFace": true}`; fix names in `words`.
- **Timeline tweaks** (in the spec, then rebuild): `"speedRamp"` into the kiss or the confetti, `"freezeEnd": 1.0` on
  the last portrait, `"transition": {"type": "dissolve", "dur": 0.8}` between parts of the day, `"dip-black"` before the exit.
- Run `python CORE/scripts/editor.py review wh/plan.json --genre wedding-highlight` and read `review.md`.
- **Footage clean-up (video, before the spec):** guest-cam handheld, dark reception and venue LED/tube light: `python CORE/scripts/prep.py c07.mp4 --work fix/c07 --stabilize --denoise light --deflicker`, then use `fix/c07/source.mp4` in the spec. `--stabilize` = vidstab (crops ~6% at the edges), `--denoise light|strong` = video noise, `--deflicker` = mains-light flicker. Only on clips that need it.

## Deliver

```bash
python CORE/scripts/deliver.py wh/plan.json --to youtube,prores-422hq --out-dir wh/deliver --burn no
python CORE/scripts/deliver.py wt/plan.json --to reels,tiktok --out-dir wt/deliver
python CORE/scripts/qc.py wh/deliver/final_youtube.mp4 --plan wh/plan.json --platform youtube --strict
python CORE/scripts/qc.py wt/deliver/final_reels.mp4 --plan wt/plan.json --platform reels --strict
```

Name files `couple_highlight_v001_16x9.mp4`, `couple_teaser_v001_9x16.mp4`. The full ceremony is a separate edit:
run `run.py ceremony.mp4 ... --no-cut` (or `multicam.py camA camB --out ceremony/multicam.mp4` for two angles).

## Check before delivering

- Contact sheet: skin looks natural, horizon level, no guest who asked not to be filmed, names spelled right.
- Watch the vows section with headphones: music dips, every word clear, no click at joins, no uncovered jump cut.
- Every key family member appears at least once (ask the couple for the list and tick it off).
- The film ends on a downbeat, not mid-phrase; `qc.py` passes loudness (-14 LUFS, -1 dBTP) and has no flash frames.
- Tell the couple what is in each file, the song credit, and how many revision rounds remain (two is common).

## Example requests

- "Here's our wedding footage and our song, make a 4-minute highlight with the vows in it."
- "Make a 45-second vertical teaser for Instagram from the best moments."
- "Cut the ceremony as its own video, both cameras, keep everything they said."
