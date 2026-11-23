---
name: event-recap
description: "Event recap editor for Claude: turns conference, launch, meetup, festival, workshop or party footage into a 60-120 s beat-cut recap with speaker soundbites, sponsor visibility and a 9:16 version, plus short speaker clips. Use when the user says 'make an event recap', 'aftermovie', 'highlight video of our conference', 'recap reel of the launch party', 'summit sizzle', 'cut a recap from these clips', or hands over a folder of event footage and a track. Runs on video-studio-core (timeline montage, beats, music fit, colour, deliver, QC)."
license: MIT
---

# Event Recap

Ninety seconds that make people who missed it wish they had come, and make the sponsors happy they paid.

- **Best for:** conferences, product launches, meetups, workshops, festivals, brand activations, corporate offsites
- **Inputs:** a folder of event clips (venue, crowd, stage, speakers), 2-4 speaker soundbites, logo, licensed track
- **Default skin:** `event-promo` · alternatives `chaos-stack`, `kinetic-launch`, `frame-studio`
- **Formats:** 16:9 recap, 9:16 recap, 9:16 speaker clips
- **Durations:** recap 60-120 s (vertical 30-60 s), speaker clips 15-45 s
- **Genre preset:** `--genre event-recap` (`python CORE/scripts/editor.py genre event-recap`)

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- Ask for: event name, date, city, the next date / CTA, sponsor list (who must be visible and for how long), speaker
  names and titles, logo file, and the track (licensed for this use).
- **Consent:** attendees were filmed at a public-ish event; still drop anyone who opted out (check the photo-consent
  list or lanyard colours) and avoid close-ups of children without consent.

## How a pro cuts this

**Structure (% of length)**

| beat | % | what goes here |
| --- | --- | --- |
| energy open | 15 | the best 3-4 shots: crowd peak, stage lights, applause; title hit on the drop |
| arrival / venue | 15 | doors, badges, signage, wide of the room filling up |
| speakers + soundbites | 35 | 2-3 short lines (5-8 s each) that say what the event was about, J-cut under crowd shots |
| crowd / moments | 20 | networking, laughter, demos, hands-on, sponsor booths |
| logo + next date | 15 | logo, "See you in 2027", URL / date |

**Pacing.** ASL 1-3 s on the music; soundbites slow it down (hold the speaker 2-4 s, then cut to the room while they keep
talking). Visual change at least every 4 s. Vary: three quick shots, one long one.

**Cut rules.** Cut on beats, change every 2nd or 4th beat, not every beat. A soundbite is a complete thought: cut after the
word decays, never mid-sentence. J-cut the speaker's voice 0.5-1 s under the previous crowd shot; L-cut it over a reaction.
Show it looked full: wides of a full room; never a wide of empty chairs.

**Transition grammar.** Cuts on the beat; whips between sections (one direction); a speed ramp into the title; a dip to
black before the logo. Pick two at most.

**Music and sound.** The track leads (bed ~-12 dB), dips 8 dB under soundbites, keeps crowd cheers and applause
breathing underneath. One impact on the title hit, one whoosh per whip; nothing else.

**Colour.** `punchy` or `clean-commercial` for corporate, `music-video-neon` for parties and festivals,
`teal-orange-pro` for a cinematic recap. Match stage and hall cameras first.

**Captions.** None on the montage. Speaker soundbites get a `lowerthird` (name, role) and, for the vertical version,
`clean` captions for the soundbite only.

**What the client judges.** Energy, sponsor logos visible, that it looks well attended, speakers looking good, the
next-date CTA.

**Common mistakes.** Opening on the logo; long speeches; every shot the same length; sponsors missing; music fading out
mid-phrase; empty-room shots; uncredited speakers.

## Make the edit

Montage orders clips by file modification time and bakes the track into the assembled audio. Soundbites need their own
audio, so the usual pro route is a hand spec built from a montage dry-run.

```bash
# 1. beat-cut draft (b-roll only), ~90 s
python CORE/scripts/timeline.py auto event/ --work er --mode montage --music track.wav --duration 90 --format 16:9 --dry-run
# 2. find soundbites in the talk recordings
python CORE/scripts/prep.py talk1.mp4 --work t1
python CORE/scripts/transcribe.py --work t1 --model base
python CORE/scripts/clip_candidates.py --work t1 --min 5 --max 12 --top 6
```

3. Edit `er/timeline_spec.json`: insert 2-3 soundbite clips (`{"src": "../t1/source.mp4", "in": 412.3, "out": 419.0,
   "audio": "keep", "jcut": 0.6, "words": "../t1/transcript.json"}`) between the montage shots, keep the montage shots
   `"audio": "mute"` (paths in the spec are relative to the spec file), and **delete the spec's `music`** (the track goes in the plan so it can duck under the soundbites).

```bash
python CORE/scripts/run.py - --timeline er/timeline_spec.json --style SKILLS/event-promo --genre event-recap --format 16:9 --no-cut --music track.wav --model base --work er --stop-after plan
python CORE/scripts/render.py er/plan.json --frames 1,12,30,55,85
python CORE/scripts/render.py er/plan.json
python CORE/scripts/finish.py er/plan.json --platform youtube
```

Fast music-only version: `python CORE/scripts/run.py - --clips event/ --auto montage --music track.wav --duration 60 --format 9:16 --style SKILLS/event-promo --genre event-recap --work er9 --stop-after plan`.
Speaker clips: run `clip-miner` style edits on each talk recording.

## Refine the plan

- **Captions:** delete the skin's `captions` element (keep it only for soundbite-led verticals, with `"preset": "clean"`).
  Music-only montage: clear `words` and set `"audio": {"platform": "youtube", "voice": false}`.
- **Music:** `"music": {"src": "track.wav", "under": 12, "duck": "speech-aware", "duckDepth": 8, "fitTo": "beats", "endButton": true}`.
- **Title on the drop:** `{"type": "titlecard", "kicker": "BERLIN · 14 MAY 2026", "title": "DevSummit", "start": 2.1, "end": 4.6, "in": "zoomOut", "out": "fade"}`
  timed to a downbeat (`beats.py track.wav --out er/beats.json`, read `downbeats`). Add `{"t": 2.1, "kind": "impact", "gain": 0.5}` to `sfx`.
- **Speakers:** `{"type": "lowerthird", "name": "Dr. Lena Weber", "role": "CTO, Acme", "start": 21.0, "end": 25.5}`.
- **Sponsors:** a `card` with `items` of sponsor names or a logo `image` element (`"image": "sponsors.png"`) for >= 2 s
  near the end; agree the sponsor list in writing.
- **End:** `{"type": "titlecard", "title": "See you in 2027", "subtitle": "devsummit.example", ...}` in the last 3-4 s.
- **Colour:** `"color": {"look": "punchy", "intensity": 0.7}` (or `clean-commercial`, `music-video-neon`).
- `python CORE/scripts/editor.py review er/plan.json --genre event-recap`.
- **Footage clean-up (video, before the spec):** handheld crowd shots, dark venues, LED walls and fluorescent halls: `python CORE/scripts/prep.py hall02.mp4 --work fix/hall02 --denoise light --deflicker`, then use `fix/hall02/source.mp4` in the spec. `--stabilize` = vidstab (crops ~6% at the edges), `--denoise light|strong` = video noise, `--deflicker` = mains-light flicker. Only on clips that need it. `--stabilize` for walking shots.
- **Opt-outs and children:** blur faces of anyone who opted out with `"blurs": [{"x": 1210, "y": 300, "w": 180, "h": 220, "start": 14.2, "end": 16.0}]` (output pixels, top-left box; see `CORE/references/plan-schema.md`), or drop the shot.

## Deliver

```bash
python CORE/scripts/deliver.py er/plan.json --to youtube,linkedin,reels --out-dir er/deliver --burn no
python CORE/scripts/qc.py er/deliver/final_youtube.mp4 --plan er/plan.json --platform youtube --strict
python CORE/scripts/qc.py er/deliver/final_reels.mp4 --platform reels    # no --plan: reframed from a 16:9 plan
```

A 16:9 master sent to `reels` gets a blurred fill; for a real vertical recap, re-run step 1 with `--format 9:16`
(shorter, best shots only). Name files `devsummit26_recap_v001_16x9.mp4`.

## Check before delivering

- Contact sheet: titles and lower thirds inside safe zones, speaker names spelled as on the programme, logos sharp.
- Sponsors on the list each visible; no empty-room shots; no opted-out attendees.
- Soundbites complete and intelligible over the music; the track ends on a downbeat (`endButton`).
- `qc.py` passes loudness (-14 LUFS, -1 dBTP), black / flash frames and (for stage strobes) photosensitivity.
- Tell the client the music credit, which sponsors appear where, and the file list.

## Example requests

- "Make a 90-second aftermovie of our conference with two speaker quotes."
- "Vertical recap of the launch party for Instagram, on this track."
- "Recap of the workshop, make sure all four sponsors are visible."
