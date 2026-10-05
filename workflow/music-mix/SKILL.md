---
name: music-mix
metadata: {packVersion: 1.3.0}
description: >-
  Lays a music bed under a finished video — the music is trimmed and faded to the
  video's exact length and ducks beneath the voice, while the video stream is copied
  untouched. Use when the user asks to add music, add a background track, add a music
  bed or soundtrack, or asks for something like "make a lofi mix of this": "put music
  under this ad", "add a background track", "give me a couple of music versions".
  Entered from a finished cut — captions already burned is the preferred input, not a
  problem. It never edits the picture and never changes the video's length.
---

# Music mix

Puts a music bed under a finished video. The bed is trimmed to the video's exact
duration, faded out at the tail, and ducked under the voice. This is the last step of
the pack: base video → b-roll overlay → burned captions → **music**.

Mixing mechanics live entirely in `scripts/music_mix.py`. This file is judgment only —
when to enter, what track to pick, where the music comes from, what the user sees.

## Entry condition

**A finished video the user has signed off on.** Captions already burned in is the
preferred input, because music is genuinely the last thing that happens. That is safe
because the script copies the video stream packet for packet (`-c:v copy`) and verifies
afterwards that the output's video packets hash identical to the input's — so burned
captions come through bit-exact, not "re-encoded but probably fine".

If the cut is still moving, wait. Remixing is cheap; re-rendering the pipeline is not.

## Track judgment

- **Match the genre to the ad's mood, not to your taste.** Calm skincare and a punchy
  supplement ad do not want the same bed. Read the script's tone first.
- **Lofi is the default** — it is what the reference edit used, and it sits under a
  talking head without competing with it. Depart from it deliberately, and say why.
- **Always produce 2–3 named variants.** The reference edit shipped a `final-mixes`
  folder with `lofi-jazzy` and `lofi-warm` of the same cut. Vary the track or
  `--music-gain`, name them for what they are, and let the user pick — each extra mix
  is one ffmpeg pass and no credits.
- **Instrumental only.** Lyrics compete with the voiceover for the same attention.

## Sourcing the music

> **REST key required. A Novoads MCP connector is not a substitute.** If
> `NOVOADS_API_KEY` is missing or still the placeholder, stop before any
> generation work and tell the user: "Before continuing, create an API key at
> <https://novoads.ai/dashboard/settings?tab=api> and paste it into `.env`."
> That holds even when `mcp__novoads__*` tools are connected and authenticated in
> the session. Never call `mcp__novoads__*` tools from this repo's workflows: they
> are a different surface with different behavior, including the units they quote
> costs in. Repo installs verify with `./scripts/check-novoads-env.sh`; a solo
> install checks `NOVOADS_API_KEY` in the environment.

**Pack version.** Every `/v1` response carries `X-Novoads-Pack-Version`; mention a newer pack at <https://github.com/novoads/agent-skills> only when that header names a version NEWER than this file's `metadata.packVersion` — equal or older is nothing to say, and it is never a reason to stop.

**(a) Generated through the Novoads API — the default.** `POST /v1/music` on the
`$NOVOADS_API_KEY` this pack already uses: no second account, no second bill. Price it
with `POST /v1/estimates` `{"kind":"music"}` and get approval first, like every
generation here — that arm takes the kind and nothing else. Then poll
`GET /v1/generations/{jobId}` to terminal, about 75 seconds. Fields, limits and failure
modes: `novoads-api` skill, `reference.md` § `POST /music`.

**One request returns two tracks**, as `audio[]` on the succeeded job, both yours for
the one charge — so the 2–3 variants above cost one generation, not three. Download
**both** `audio[].url`; they are presigned at read time, so re-poll rather than reuse a
stale one. Tracks run one to two minutes whatever you hint — the script trims them.

**(b) When (a) is not available, diagnose before you improvise.** There is no second
generation vendor in this pack. Two different things can block (a), and they have
different answers:

- **`$NOVOADS_API_KEY` is absent.** Stop. Do not look for another credential. Tell the
  user to create a key at
  [novoads.ai/dashboard/settings?tab=api](https://novoads.ai/dashboard/settings?tab=api)
  and put it in `.env` (see `scripts/setup.sh`), then resume.
- **Music is off on that deployment.** `invalid_input` is also what a typo'd body
  returns, so confirm which before concluding anything. The reliable test is the free,
  keyless `GET /v1/openapi.json`: **no `/music` path means the deployment has music
  off; a `/music` path means your request was malformed.** If music really is off, say
  so plainly and fall back to (c). If the path is there, fix your body and retry (a).

Never send a user to a second signup, and never over a malformed field.

**(c) A file the user supplies.** Always allowed, no questions. Licensing is theirs.

Music from (a) is **AI-generated** and its clearance is the user's call, not
this skill's to guarantee: Novoads' terms §11 "AI-Generated Music" make no
representation that it is free of third-party rights and put use (their jurisdiction,
their platforms) on the customer. Say that once for client-facing or paid media, and
improvise no legal advice past it.

## Hard rule: mixing always goes through the script

Never hand-write mixing ffmpeg for this task. `music_mix.py` owns validation, rendering
and verification, and it fails loudly on what fails silently by hand: a track shorter
than the video, a re-encoded picture, a duration that drifts, loudness that will get
turned down by the platform, an output path that would overwrite one of its own inputs,
and — the sneakiest one — a bed so quiet it is not in the mix at all.

That last one is caught **before** the render, and it is worth knowing why: the audio is
re-encoded on every path, so a finished file with no music in it looks exactly like one
with music. The script measures the music's own loudness up front and refuses a silent
track or a gain that would put the bed below audibility. A verifier cannot do that job.

**Escape hatch:** if a request genuinely doesn't fit this model — music that must hit a
specific cut point, a track that needs an intro trimmed off the front, stems, a
mid-video music change — say so and ask the user how to proceed. Do not improvise
around the script.

## Running it

```
python3 scripts/music_mix.py video.mp4 music.mp3 out-lofi-warm.mp4
```

- `--music-gain DB` — bed level, default −18 dB, range ±60. The main knob between
  variants, and the first one to reach for when loudness verification fails.
- `--no-duck` — flat bed, no ducking. For a video with no voiceover.
- `--dry-run` — validate and print the plan, render nothing.
- `--verify-only OUT --video INPUT` — re-check any existing output, including one from
  an old session. Standalone: mixing it with render arguments is an error.

**Report the script's verification line verbatim** — the measured loudness and true
peak, not a paraphrase. Do not upgrade it: it establishes duration, an un-re-encoded
picture, rebuilt audio and the loudness envelope, and says nothing about how the bed
*sounds*. Exit codes: `2` validation, `3` render, `4` verification. A nonzero exit is a
real failure — surface it, don't retry blindly.

**The refusals worth recognising**, so you fix the input instead of retrying:

| Message | What to do |
|---|---|
| `music is Xs, video is Ys — the track is too short` | Get a longer track. Never loop or pad. |
| `music track is silent` / `music inaudible at these gains` | Wrong file, or `--music-gain` is too low. |
| `input voice is silent/near-silent` | This is not a music-bed job; the video needs a soundtrack. |
| `has N audio streams` | Pick one voice track with ffmpeg first — the script will not guess. |
| `output ... is the same file as the video` | The output path aliases an input (hardlink, symlink, or a case-variant name on macOS). Choose a new name. |
| `master gain clamped` | The input is more than 30 dB off target; fix its level upstream. |

## Evals

`evals.md` defines the six scenarios this skill is held to (MM1–MM6).
`scripts/test_music_mix.py` implements the five mixing ones mechanically against
synthetic fixtures, in 15 cases — run it after touching the script. MM6 (sourcing on the
Novoads key alone) is a text-and-flow eval; the script has no part in it.
