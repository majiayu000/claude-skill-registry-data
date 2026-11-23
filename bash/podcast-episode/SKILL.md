---
name: podcast-episode
description: "Full video-podcast episode editor: switches 2-4 synced cameras to whoever is talking with wide-shot resets, removes fillers and crosstalk lightly so people still sound like themselves, matches speaker levels, builds a cold-open teaser, name cards and chapters, and delivers the 16:9 YouTube episode, an audio-only MP3/WAV at -16 LUFS and the material for clips. Use when the user says: edit my podcast, video podcast episode, multicam podcast, switch cameras to who is talking, clean up my interview episode, podcast for YouTube and Spotify, add chapters to my podcast. Default skin pod-frame; any Video Studio skin works."
license: MIT
---

# Podcast Episode

A full episode that looks like a studio show and sounds like a podcast: right camera, clean audio, chapters.

- **Best for:** video podcasts, long-form interviews, panel shows, livestream conversations
- **Inputs:** one camera file per person, each with its own mic, starting at the same moment (or one wide shot); optional wide; host/guest names and roles; intro/outro music
- **Default skin:** `pod-frame` · alternatives `minimal-mono`, `dual-subs` (bilingual), `chapter-pro`
- **Formats:** 16:9 1920x1080 episode (-14 LUFS for YouTube), audio-only MP3 (-16 LUFS) and WAV, chapters, show notes draft, thumbnails
- **Duration target:** 30-120 min; genre preset `podcast-episode`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre podcast-episode`.
- The `--genre` preset sets autocut's pause cut (0.9 s) and run.py respects it; pass `--max-gap` only to override.
- **Sync:** `multicam.py` expects every camera to start at the same instant with that person's own mic. If they don't, trim each to the clap first (`prep.py camA.mp4 --work a --start 3.42` and use `a/source.mp4`).
- Ask for names, roles and spellings; ask whether anything said must come out (legal, private).

## How a pro cuts this

| beat | % | what happens |
| --- | --- | --- |
| cold-open teaser | 0-2 | 30-60 s: the best 2-3 lines of the episode, then a hard cut |
| intro | 2-4 | show sting/music, who the guest is |
| conversation | 4-96 | chronological; chapters at topic shifts every 5-15 min |
| outro + CTA | 96-100 | thanks, where to find the guest, next episode |

- **Pacing:** ASL 4-12 s set by who speaks; minimum shot 2 s; wide reset every 30-60 s and when both talk.
- **Switching:** cut to the speaker at the start of their sentence, not on a one-word "yeah"; show the listener's real reaction now and then (L-cut), never fake one.
- **Cut rules:** light: drop um/uh, false starts and long dead air; keep "you know", laughs and thinking pauses that carry meaning (`fillers: keep-natural`). Cut crosstalk only between words. Don't reorder what people said except for the teaser.
- **Transitions:** cuts only; dip to black only into the outro.
- **Music/SFX:** music only on intro/outro (and under the teaser); no SFX in the conversation.
- **Colour:** match cameras first (same white balance and exposure), then a gentle look (`portra` 0.5 or `cool-corporate` 0.5).
- **Audio:** each voice levelled, de-essed, light denoise; room tone under cuts; -16 LUFS audio feed, -14 LUFS YouTube.
- **Captions:** optional on 16:9 (sidecar SRT always); burned captions belong on the clips.
- **Client judges:** audio quality, the guest looking good, clip quality later.
- **Common mistakes:** ping-pong cutting on every "mm-hm", one voice louder than the other, removing every pause, music under the whole talk, missing name cards, no chapters.

## Make the edit

Multiple cameras (one per speaker, synced):

```bash
python CORE/scripts/multicam.py camA.mp4 camB.mp4 --wide wide.mp4 --min-shot 2.0 --out pod/multicam.mp4
```

One wide camera: skip that step and use the wide file as input. Then:

```bash
python CORE/scripts/run.py pod/multicam.mp4 --style SKILLS/pod-frame --genre podcast-episode \
  --smart-cuts --title "SHOW NAME" --model small --prompt "Guest Name, Company" --work ep --stop-after plan
python CORE/scripts/story.py outline --work ep --genre podcast-episode     # quotable lines -> teaser, topic shifts -> chapters
python CORE/scripts/editor.py review ep/plan.json --genre podcast-episode --fix
python CORE/scripts/render.py ep/plan.json --frames 5,60,600,1800
python CORE/scripts/render.py ep/plan.json
python CORE/scripts/finish.py ep/plan.json --platform youtube
```

Cold-open teaser: pick 2-3 lines from `outline.md`, then `story.py reorder --work ep --order "s412,s97,s1-s600" --format 16:9` and rebuild through `run.py - --timeline ep/story_timeline.json ...`. Read `story_flags.md`; the teaser lines must keep their meaning.

## Refine the plan

- **The `--title` text becomes a show chip and a first lower third; replace that lower third with the guest name.**
- **Name cards:** `{"type": "lowerthird", "name": "Rahul Mehta", "role": "CEO, Acme", "start": 64.2, "end": 69.0}` at each person's first line (exact spelling from the user).
- **Chapters:** top-level `"chapters": [{"start": 0, "title": "Cold open"}, {"start": 95, "title": "How Acme started"}, ...]` at topic shifts from `outline.md`.
- **Quote pull:** one `quote` element for the best line of the episode (4-5 s).
- **Audio:** `"audio": {"platform": "youtube", "voice": {"denoise": "light", "eq": "broadcast", "deess": true}}, "roomTone": true`.
- **Music:** intro/outro only - `"music": {"src": "theme.mp3", "volume": 0.5, "duck": true, "fadeOut": 2}` covers the start; for the outro either premix or end the episode on the theme's sting.
- **Look:** `"color": {"look": "portra", "intensity": 0.5}` (set the same `match` reference for every camera if they differ: `"match": "hero_frame.png"`).
- **Captions:** keep or remove the skin's caption element for the 16:9 (the SRT sidecar is always produced by deliver.py).
- **Face-aimed punch-ins:** with `W/track.json` the zooms centre on the face instead of the frame centre: after `run.py ... --stop-after cut` (`--stop-after timeline` for a `--timeline` spec) run `python CORE/scripts/track.py analyze W/cut.mp4 --work W`, then `make_plan.py` (it copies the track into the plan). Per zoom, `"cx"`/`"cy"` (0-1) aim elsewhere; `"toFace": false` keeps centre.

## Deliver

```bash
python CORE/scripts/deliver.py ep/plan.json --to youtube,podcast-mp3,audio-wav --out-dir ep/deliver
python CORE/scripts/qc.py ep/deliver/final_youtube.mp4 --plan ep/plan.json --platform youtube
python CORE/scripts/qc.py ep/deliver/final_podcast-mp3.mp3 --platform podcast        # audio-only checks: loudness, peak, duration
```

- `podcast-mp3` is -16 LUFS / -1 dBTP; `audio-wav` keeps the mix untouched for the host's own mastering.
- `chapters.txt` goes in the YouTube description and the podcast show notes; `post.md` has title and description drafts (from the transcript only).
- `podcast-video` is a 16:9 preset at -16 LUFS if the platform wants podcast loudness with video.
- Clips: run `clip-miner-pro` on `ep/final.mp4`.

## Check before delivering

- The camera follows the speaker; no shot shorter than 2 s; a wide reset at least every minute of long answers.
- Both voices at the same perceived level; no clipped laughs; room tone under cuts.
- Names and roles spelled right; chapters valid and correctly timed.
- Audio feed -16 LUFS, YouTube -14 LUFS (`qc.py`); duration and A/V sync right at the end of the episode.
- Tell the user: minutes removed, chapter list, files for each platform.

## Example requests

- "Edit my 2-camera podcast, switch to whoever talks, add name cards and chapters."
- "Make the full YouTube episode plus an MP3 for Spotify at podcast loudness."
- "Clean up this interview episode lightly - keep it natural, remove the ums."
