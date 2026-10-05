---
name: music-video
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai, plus the music file the finished video must carry. Your audio never reaches the API (measured) — the visuals are written to the track's tempo, mood and sections, then your own file is laid on locally at zero cost. One job caps at 30 seconds, so a three-minute song is six jobs minimum and the cost table says that before anything is spent. Use when a user has a specific piece of music and wants visuals for it, e.g. "make a music video for this track", "visuals for my song", "an MV for this instrumental", "generate footage cut to this beat". Do not use for cheap vertical social drafts (shorts-reels), a brand film that happens to have a music bed (seedance-ad-creative), or when there is no particular audio file the finished video has to carry.
license: MIT
version: "2.0.1"
homepage: https://github.com/ofoxai/skills/tree/main/skills/music-video
metadata:
  author: ofoxai
  version: "2.0.1"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq, ffmpeg]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "🎵"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/music-video
---

# music-video: visuals written to a track's structure, your own audio laid on at the end

The user has a piece of music. This skill produces picture for it: the track's
length, tempo, mood and section boundaries are read **locally**, the visuals
are written to that structure, the segments are generated so they stay
continuous with each other, and the user's own audio file is muxed on at the
end — locally, with no API call and at no cost.

`ffmpeg` is a hard requirement here, not an enhancement: the last step of the
deliverable is a local mux, and stitching the segments needs it too.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns the track analysis,
the section-to-segment mapping, the visual prompt craft for music, the
multi-job cost arithmetic and the final mux; `ofox-video-core` owns talking to
the Ofox API correctly and safely (the `OFOX_API_KEY` handling, the
no-resubmit rule, error-code mapping, download/verification, and reporting the
downloaded file's absolute path). **Read that skill's safety contract before
using this one** — it is not restated here.

Shared prose is linked rather than copied: the prompt formula, the camera and
transition vocabularies, the cut-density measurements and the negative-list
items are in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md);
the pre-prompt question rules in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md);
the spend rule in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).

## The first thing to say out loud: your music never reaches the model

People ask for "visuals generated from this track", and the natural reading of
that is that the model listens to the song. **It does not**, and this is
measured rather than assumed, so say it in the first reply rather than after
the bill:

- The API's `input_references` field does accept an `audio_url` element. The
  server parses it, validates it, and really does fetch the file — a
  deliberately unresolvable URL came back with a DNS error naming the
  hostname, which is how far the server got before giving up. So "it is
  accepted" is true.
- **And the delivered clip does not carry that audio.** A real 5-second speech
  clip was supplied as a `data:` URI on `bytedance/seedance-2.5` (job
  `d8561509-dcc6-4f2c-8864-a193cd239b14`, 2026-09-15, 55 cents). The job
  completed normally and the track that came back is not the track that was
  sent: compared as RMS envelopes, the input is near-continuous speech and the
  output is sparse, correlation 0.41. The model generated its own audio,
  exactly as it does with no reference at all.
- Every video model in the catalog reports `capabilities.audio_input: false`.
  That flag described the outcome better than the parameter table's "≤3 audio
  clips, each ≤15s" limits did.

So this skill **does not send the user's audio to the API at all.** What it
does instead:

```
1. read the track locally           duration, tempo, where the sections change
2. write the visuals to that        section boundaries become segment boundaries;
   structure                        cut density follows the energy, not a click track
3. generate the segments            chain, so each one opens on the previous one's
                                    closing frame and the piece stays continuous
4. lay the user's track on          ofox-video.sh mux-audio — local, no API call,
                                    no key, no cost, and the only way to get a
                                    specific track onto a clip
```

### When the visual concept comes with several images

Images can guide the generated visuals even though the audio cannot. Use the
shared
[`Identity-reference recipe — the authoritative copy`](../ofox-video-core/references/prompt-structure.md#identity-reference-recipe--the-authoritative-copy)
for `input_references`, canonical `@imageN` labels, and the required
“supplies / ignore” sentence for each asset. This is the route suggested by
gallery cases 57 and 59, with an important limit: this repo has measured only
two images and the API accepts at most nine. Case 59's 18-image arrangement
cannot be reproduced as one Ofox job; do not silently drop half the assets.
The user's track still stays local and is muxed after generation.

**What that buys, stated honestly, because it is the sentence the user is
actually paying against:** the visuals are cut to a structure *you* describe
from the music — its sections, its energy, its feel. They are **not**
synchronised by the model to the waveform. Nothing here lands a cut on a
particular snare hit. If beat-frame-accurate cutting is the requirement, the
honest answer is an editor: generate longer continuous material here and cut
it to the grid in software, where a frame is a frame.

That is not a hedge. Cut timestamps inside one job land to about **±1 second**
when they land at all, and one 15-second job that wrote three explicit cut
stamps kept one of them and delivered two nobody asked for
(`9cd773d0-b84e-4135-bc75-8f4e8963be2b`). A second is several beats at any
dance tempo.

## Not this skill

| The user wants… | Skill |
|---|---|
| **a specific audio file to come out the other end on the finished video** | **this one** |
| several cheap vertical drafts to choose between, for a feed | [`shorts-reels`](../shorts-reels/SKILL.md) — the cheap-drafts ladder. Composes with this one: draft a look there, run the piece here |
| a brand or product film that happens to have a music bed | [`seedance-ad-creative`](../seedance-ad-creative/SKILL.md) — the ad beat structure is its own craft, and the music is laid on afterwards there too |
| anime or manga-styled sequence work, music or not | [`seedance-anime-drama`](../seedance-anime-drama/SKILL.md) — it has image-based character consistency, which this skill does not |
| an article or release note said out loud | [`explainer`](../explainer/SKILL.md) — the model generates the speech; you cannot hand it audio there either |
| a portrait plus a script, as one person speaking | [`talking-head`](../talking-head/SKILL.md) |
| one still animated, or two stills tweened | [`seedance-product-video`](../seedance-product-video/SKILL.md), [`keyframe-animation`](../keyframe-animation/SKILL.md) |
| a longer clip extended, or a new ending from a chosen second | `video-extend-edit` |

**The distinguishing question is whether there is a particular track the
finished file has to carry.** "Something energetic with music" is not this
skill — that is a scenario skill plus an editor, and it will be cheaper. "Here
is my song, I need picture for it" is this skill, and the mux at the end is
the reason.

The visual *style* is still somebody else's craft. If the piece calls for
anime, read `seedance-anime-drama` for the look; if it is product-led, read
`seedance-ad-creative`. This skill owns the structure, the arithmetic and the
audio, not every genre's vocabulary.

## Where the core skill lives

Resolve once, before the first call:

```bash
for d in ../ofox-video-core \
         ../ofoxai-skills-ofox-video-core \
         ~/.agents/skills/ofox-video-core \
         ~/.agents/skills/ofoxai-skills-ofox-video-core \
         ~/.claude/skills/ofox-video-core; do
  [ -f "$d/references/ofox-video.sh" ] && echo "$d" && break
done
```

Examples below are written as `../ofox-video-core/...` (the skills.sh /
ClawHub / `npx ofox-skills` layout, where a skill's directory is named after
the skill). If the probe found a different directory — LobeHub unpacks each
skill as `ofoxai-skills-<name>`, so the sibling there is
`ofoxai-skills-ofox-video-core` — substitute it, in the `ofox-video.sh`
commands and in the `references/*.md` links alike.

**That `../` is relative to this skill's own directory**, which is also where
the probe has to run. From anywhere else nothing resolves — use the absolute
path the probe printed (candidates 3–5 are absolute already), or, in a clone
of this repo, `skills/ofox-video-core/references/ofox-video.sh` from the repo
root.

Nothing found → the core skill isn't installed; see "If the script isn't
found".

**This skill needs `ofox-video-core` 2.0.0 or newer.** From that version the
billable subcommands refuse to run without `--approved`, and every real-run
command below passes it. An older core does not know the flag and stops with
`unknown option '--approved'` before any request — nothing is submitted and
nothing is billed, so the fix is to update the core, never to drop the flag.

## Before generating: the availability check

Run this once per session (not on every request):

```bash
bash ../ofox-video-core/references/ofox-video.sh check
```

If it fails, follow `ofox-video-core`'s guidance (install `curl`/`jq`, or get
an `OFOX_API_KEY` at `https://app.ofox.ai`) — don't dead-end the conversation,
and don't re-run this check on every subsequent request once it has passed.

`check` reports whether the key is **present**, not whether it is valid, and
makes no network call. **It does not check `ffmpeg`**, which this skill needs
for the mux and for stitching, so check that separately:

```bash
command -v ffmpeg ffprobe
```

Missing on macOS: `brew install ffmpeg`; Debian/Ubuntu:
`sudo apt-get install ffmpeg`. Both binaries come from the same package.
Find this out **now** rather than after the segments are paid for — `chain`
refuses to start a multi-shot run without `ffmpeg` for exactly that reason,
and a piece with its audio still missing is not the thing the user asked for.

**This skill needs `ofox-video-core` 2.0.0 or newer.** Two separate reasons
now: `mux-audio` arrived in 1.25.0 — on an older core the segments generate
fine and the final step, the whole reason this skill exists, fails with an
unknown subcommand — and 2.0.0 is where `chain` began refusing to run without
`--approved`, which every real-run command below passes. Confirm it before
quoting a piece, not after generating one:

```bash
grep -m1 '^version:' ../ofox-video-core/SKILL.md
```

A failing `check` is not a stop sign: the whole track analysis, the segment
plan and the price can be settled with no key at all — see "Pricing a job with
no API key".

## Before anything else: the brief

The shared rules — the three tiers, one round of at most four questions, the
"Let the AI decide" discipline, the order with the approval gate, the fallback
without `AskUserQuestion` — are in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md).
This section adds only this scenario's question set.

| Tier | music-video axes |
|---|---|
| **must-ask** | the audio file itself (a track nobody can open is not a track), and what the visuals are *of* |
| **ask-if-open** | the section map, the aspect ratio, whether the whole piece or one section is being made |
| **never-ask** | resolution, provider, `--generate-audio` (always `false` here), the segment duration (arithmetic), the model (a row in the cost table, not a question — unless the user names one, which always wins) |

### The question set

| # | Tier | `header` | Question | Options — first is recommended; "Let the AI decide" last where it appears | Ask when |
|---|---|---|---|---|---|
| 1 | must-ask | `Track` | Where is the audio file? I need the actual file — the finished video carries your track, laid on locally at the end. | free text: a local path. **No AI option** — a file that does not exist cannot be invented, and a streaming link is not a file | No readable audio path was given |
| 2 | must-ask | `Visuals` | What should the picture be of? | free text, with two or three concrete suggestions drawn from the track's feel. **No AI option** when nothing at all was given — "visuals for a song" is not a subject, and six segments of the model's own guess is an expensive way to find that out | The request names a track and nothing else |
| 3 | ask-if-open | `Scope` | The whole piece, or one section? | `The whole track (recommended when it is under four minutes)` — <N> segments priced as one table, N from the arithmetic in "Step 2" / `One section — a chorus, a hook, a 30-second cut` — one job, and the cheapest way to see whether the look works / `Let the AI decide` — one section first | The user did not say, and the track is long enough for the difference to be real money |
| 4 | ask-if-open | `Sections` | Where do the sections change? Rough timestamps are plenty — "intro to 0:14, verse to 0:42, chorus to 1:10". | free text / `Even segments is fine` — the picture then changes where the music does not / `Let the AI decide` — **even segments, named as even segments**; "Let the AI decide" never means inventing a structure, because nothing here has heard the track | The scope is the whole piece and no section map was given |
| 5 | ask-if-open | `Aspect` | Where will it be watched? | `16:9 landscape (recommended)` — the default shape for music / `9:16 vertical` — feeds / `1:1` / `Let the AI decide` | No platform word and no ratio in the input |

If more than four are open, ask in this order: `Track`, `Visuals`, `Scope`,
`Sections`. The aspect ratio is the one to drop — 16:9 is a safe default and
it is cheap to say so in the recap.

### Skip rows specific to this scenario

On top of the generic rows in `creative-brief.md`:

| Input says… | Axis | Value |
|---|---|---|
| "for TikTok", "Reels", "Shorts", "vertical" | Aspect | 9:16 |
| "for YouTube", "for the release page" | Aspect | 16:9 |
| "just the chorus", "a 30-second cut", "a teaser" | Scope | one section |
| a track under 30 seconds | Scope | one segment; the arithmetic is already answered |
| "something moody / driving / dreamy" | Visuals | a starting point, not a subject — still ask what is on screen |
| "with the lyrics on screen" | — | not available from a description; see "Lyrics and on-screen text" and offer the editor route |
| "cut on the beat", "synced to the drums" | — | correct the expectation **before** quoting; see the top of this file |
| the user names a model or a shorthand | model | use it; never silently substitute |

### The recap for this scenario

```
Brief
- Track: /Users/me/music/coast-road.wav — 3:12 (192s, read with ffprobe)
- Visuals: an empty coastal road at dusk, mist, sodium lamps — no people (you chose)
- Scope: the whole piece — 7 segments of 28s (196s of picture for 192s of music),
  because one job caps at 30s and 192 over 7 rounds to 28
- Sections: intro 0:00-0:28, verse 0:28-1:02, chorus 1:02-1:36, ... (yours)
- 16:9, 720p, audio generation OFF on every segment
- What this is NOT: the model does not hear your track. The visuals are cut to the
  structure described above; your file goes on at the end, locally and free. Nothing
  here lands a cut on a specific beat.
- What has been run here: a 3-segment chain, both seams clean, the mux working
  — at 10s segments, and with a synthesised tone rather than real music.
  7 segments, 28s segments and a real track are all outside that. Treat the
  first segment as the experiment and decide on the rest after you see it
```

**When no section map was given, that `Sections` line changes shape and must
not keep the vocabulary:**

```
- Sections: none given, so 7 even segments of 28s. The picture changes every 28s
  whether or not the music does. I have not heard your track — if you send four
  rough timestamps I will move the boundaries onto them before anything is generated.
```

Then the segment prompts, then the cost table, all in one message.

## Step 1: read the track

Two numbers and one list. The duration is the one the arithmetic needs; get it
from the file rather than from the user's memory of it:

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 /path/to/track.mp3
```

| What | How to get it | What it decides |
|---|---|---|
| **Duration**, in seconds | `ffprobe`, as above | the segment count, and therefore the price. This is the number the cost table is built on |
| **Tempo / feel** | **ask the user** — "fast and driving", "mid-tempo", "slow and open" is enough. `ffprobe` gives a duration and nothing else, so unless you genuinely ran a local tempo tool and can say so, this number came from them or it is a guess | the cut-density register (below). A BPM number is useful for *your* planning; it is not an instruction the model executes |
| **Sections and where they change** | ask the user — they wrote or chose the track and know where the chorus lands. Timestamps to the nearest second are plenty | where the segment boundaries go |

**Ask for the section map rather than guessing at it.** "Intro to 0:14, verse
to 0:42, chorus to 1:10, …" takes the user ten seconds to write and is the
single most valuable input this skill receives. Without it, everything below
still works — segments simply fall on even boundaries and the picture changes
where the music does not.

### It is the most valuable input and it is still `ask-if-open`. Here is why, and what that costs

Those two things look like a contradiction and are not, but the gap between
them is where this skill can quietly start lying, so both halves are written
down.

**Why it stays `ask-if-open`:** must-ask is for the axes without which there
is **no job at all** — a file nobody can open, or no idea what the picture is
of. A user who has the track and the subject but no timestamps has a complete
job; what they lose is where the boundaries land, not whether anything can be
made. Blocking on it would turn "I have a song and ten seconds" into a
refusal, and the whole piece still runs on even segments. Most valuable is not
the same as load-bearing.

**What that costs, and the rule that pays it:**

> 🚨 **You have not heard the track. Never present a structure you invented as
> a structure you were given.**

That is not a style note. `ffprobe` gives you a duration and nothing else —
no tempo, no downbeats, no section changes. "Intro, verse, chorus" written
without the user's timestamps is a **guess about their music**, and it is a
guess that reads as fact in a recap because everything around it is measured.
So:

- **Timestamps given** → use them, and mark them `(yours)` in the recap.
- **No timestamps** → the segments are **even**, and they are called even.
  Not "intro", not "chorus", not "the drop" — in the recap, in the cost
  table's Section column, in the segment prompts' names and in the hand-over.
  A section name is a claim about the music, and you have no evidence for one.
- **Proposing a structure to be corrected is fine, and it is labelled.** "My
  guess: intro to 0:28, then verses of about 30s **(invented — I have not
  heard your track; correct these and I will re-cut the boundaries before
  anything is generated)**". The label goes on every line it applies to, not
  once at the top of the message.
- **The worked example later in this file is a filled-in template, not a
  reading of a real song.** Do not copy its confident intro/verse/chorus
  shape onto a track whose structure nobody told you.

The honest version of the un-mapped case, said before the cost table: *the
picture will change every 28 seconds regardless of what the music does there;
give me four timestamps and it changes where the song does.* That sentence
often produces the map on the spot, which is the cheapest possible outcome.

## Step 2: the segment plan, and why it is the cost conversation

**One job is one clip of at most 30 seconds** on `bytedance/seedance-2.5`, and
less on some models — `ofox-video.sh models` prints each model's real range
and Hailuo 3 caps at half that. So the segment count is arithmetic, not a
preference:

```
segments  = ceil( track duration / the model's maximum duration )
seconds   = ceil( track duration / segments )      <- one --duration for all of them
each
```

The second line matters and is easy to skip. Taking the model's ceiling for
every segment overshoots by up to a whole segment — 7 x 30s is 210 seconds of
picture for a 192-second track, 18 of them paid for and then trimmed off by
the mux. Dividing the track by the segment count instead gives 7 x 28s = 196
seconds: the same seven jobs, the same continuity, four seconds of overshoot
instead of eighteen, and a smaller bill, because the API charges by the
second. **It is still guaranteed to be at least as long as the track**, which
is the property that matters.

| Track | Segments at a 30s ceiling | Segment length | Picture | Evidence |
|---|---|---|---|---|
| 0:45 | 2 | 23s | 46s | within the measured scale |
| 1:30 | **3** | 30s | 90s — exact | **the largest scale actually run here** (at 10s segments, not 30s) |
| 3:00 | **6** | 30s | 180s — exact. The common case, and six separately billed jobs | ⚠️ twice the measured segment count |
| 3:12 | **7** | 28s | 196s for 192s of music; the 4 spare seconds are trimmed by the mux | ⚠️ untested |
| 5:00 | 10 | 30s | 300s — `chain` is capped at 10 shots per run, so this is the edge | ⚠️ the cap has never been approached |
| 6:00 | 12 | 30s | past one `chain` run; see "Longer than one chain run" | ⚠️ untested, and needs a mechanism that is itself untested |

⚠️ **The arithmetic is sound and the scale is mostly unmeasured, and those are
different things.** The segment count falls out of the track's length and the
model's ceiling — there is nothing to verify there. What has actually been
generated is **three segments and two seams**, and at **10-second** segments
rather than the 20–30s this table produces. Everything from six segments up is
an extrapolation across four or more unverified seams.

**So do not present seven jobs as a routine ask.** Lead with the scale that
has evidence:

- **Quote the whole track's total** — that rule is unchanged and is the point
  of this section. Nobody should be shown one segment's price and then pay for
  seven.
- **And say, in the same message, where the evidence stops**: three segments
  and two seams have been run; a seven-segment chain has not, and what drifts
  across four, five or six seams — palette, brightness, whether the style
  anchor survives being re-read that many times — is unmeasured.
- **Draft one segment first** (see below). On a long track that is the single
  most useful thing to do before committing the total.

Check the segment length against the model's **minimum** as well — it is 4
seconds on Seedance 2.5 and differs elsewhere, and `models` prints it. A
sub-minimum duration is rejected locally, free, before anything is submitted.

Two consequences the user must see **before** any money moves:

1. **Nobody should ever be quoted one segment's price for a song.** Someone
   who is shown the price of a 30-second clip and then pays for six has been
   misled by this skill, not by the API. The cost table shows
   *track length → segment count → total*, and the total is the number the
   yes is given against.
2. **Both roundings go up, so the picture is longer than the music**, which is
   the right direction: `mux-audio` runs the result to the shorter of the two,
   so an over-long picture loses its tail and the song still finishes.
   Under-long picture would cut the song off mid-phrase, which is audible and
   bad. **Measured 2026-09-16** on this skill's own run — 30.2s of chained
   picture, a 28-second track, a `NOTE:` saying the picture was truncated by
   2.2s, and a 28.000s deliverable with the song complete.

### Land the segment boundaries on the section boundaries

This is the one structural decision worth making deliberately, and it follows
directly from the ±1 second tolerance: **a boundary that drifts a second at a
section change reads as an edit; a boundary that drifts a second inside a
phrase reads as a mistake.** So push each segment's end toward the nearest
section change rather than cutting the track into even 30-second blocks.

The constraint to work inside: `chain` takes **one** `--duration` for the
whole run, so the segments are equal length. Two ways to get uneven ones:

- **Round the sections to a shared length** — a 26-second verse and a
  32-second chorus both become 29. Usually good enough, and it keeps the whole
  piece in one command. When the sections happen to average close to the
  arithmetic above, this costs nothing at all.
- **Generate the odd segment on its own** with `generate --duration <n>`,
  opening it on the previous segment's closing frame
  (`last-frame`, then `--frame-first-image`). That is exactly what `chain`
  does internally, done by hand. It costs one more command and keeps the
  continuity. **This repo has not run a mixed chain-plus-manual sequence end to
  end** — the pieces are each measured, the combination is not.

### Longer than one chain run

`chain` caps at 10 shots per run — a cap on how much one command can spend,
not a limit of the API. A track needing more than 10 segments is more than one
run, and the second run does not automatically open where the first one
closed. Carry it by hand:

```bash
bash ../ofox-video-core/references/ofox-video.sh last-frame /path/to/segment-10.mp4
# then pass that PNG to the next run's first shot via --frame-first-image
```

Each run gets its own cost table. Splitting is not a discount.

### Draft cheap, render the keeper — it matters more here than anywhere

The spread between the cheapest video tier and the flagship is several times
the per-second rate at the same resolution, and this is the skill where a
piece is longest, so the multiplier is largest. Drafting one representative
30-second segment on the cheap tier before committing to six on the flagship
is the difference between finding out a look does not work for the price of
one segment and finding out for the price of the album.

⚠️ **The draft is thrown away. It does not become segment 1, and it does not
come off the price of the chain.** This is not a policy — it falls out of how
`chain` works. Segment 2 opens on segment 1's **real closing frame**, extracted
from the file `chain` itself generated during that run, so `chain` always
generates its own segment 1. A draft made beforehand, at another tier or
another model, is a different file that the run never sees. You pay for
segment 1 twice: once to look at it, once inside the chain.

That is still usually worth it — one segment against the whole piece is a
cheap look — but it has to be **presented** as what it is:

- **Two stages, two approvals, and the total is both added together.** Stage 1
  is one row: the draft, at the draft's model and tier. Stage 2 is the full
  chain, every segment including segment 1 again. Never write the chain's
  price as "the rest" — nothing was subtracted.
- **Say the word "discarded" out loud** when asking for the draft. A user who
  believes they are paying for the first segment of their video, and then sees
  it billed again, was misled by this skill rather than by the API.
- **What the draft buys is information, not footage**: does this look work, is
  the cut density right, did the model draw lettering nobody asked for. Judge
  it, write down what changes, then quote the chain.

There *is* one route where the draft survives into the delivered piece: keep
it as link 1 by extracting its closing frame with `last-frame` and starting a
chain of the remaining segments from it with `--frame-first-image`. Two honest
caveats before offering it — the piece then carries one segment at the draft's
tier and model, so the first seam is a visible quality change, and **this repo
has not run that composition end to end** (the same caveat as the mixed
chain-plus-manual sequence in "Land the segment boundaries"). Offer it as the
experiment it is, or draft, discard and pay for the clean run.

Read the rates live — free, no API key — and never from memory or from this
file:

```bash
bash ../ofox-video-core/references/ofox-video.sh models                  # rank: every model, its tiers and ranges
bash ../ofox-video-core/references/ofox-video.sh providers <MODEL-ID>    # quote: that model's per-resolution rates
```

`providers` with no model argument prints the flagship's matrix, not the
catalog — pass the id you mean. The rate `models` prints is the one at each
model's **own default resolution**, which differs between models, so it ranks
rather than quotes. A cheaper model is a different look, not just a smaller
bill; offer the ladder and let the user pick the model.

[`shorts-reels`](../shorts-reels/SKILL.md) owns that ladder properly if the
user wants several drafts of the look to choose between. Write the segment
prompt here, run the draft set there, bring the winner back.

## Before anyone pays: what is measured here, and what is not

**This skill has one paid run of its own, and it exercised the pipeline end to
end.** 2026-09-16, `bytedance/seedance-2.5` on `byteplus`: a three-shot
`chain` at 10 seconds each, 480p, 16:9 on shot 1 and `adaptive` on the rest,
text-to-video with no image attached, `STATUS chain_completed`,
`CHAIN_COST_TOTAL` **3 dollars 30** (1 dollar 10 a shot). Then `mux-audio`
onto the joined file. What it settled, and what it did not, is immediately
below; the summary is that the mechanism this file describes works and the
*scale* this file recommends is still untested.

### The first run — 2026-09-16

| Shot | Job | Seed |
|---|---|---|
| 1 | `ccc0ee59-c738-46fa-b750-1db316f549ca` | `987776252` |
| 2 | `44f6ab24-b7c2-47e9-b30f-4c6f6c966371` | `822047377` |
| 3 | `849a8cdc-aa20-44e6-ab2c-7e0a9b4a8136` | `150420425` |

Joined output 854x480, just over 30 seconds of picture.

- **Three shots chained, and this is the first chain past two in this repo.**
  Every earlier measurement of `chain` was a two-shot run, so "the frame is
  carried" and "a sequence holds" were the same observation. They are now two.
- **Both seams carried, and the second was no worse than the first.** Shot 1's
  closing frame into shot 2's opening: street, signs, wet reflections and
  framing all continued. Shot 2 into shot 3: the tram's position, the signs
  and the reflections all continued. Read frame by frame either side of each
  join, not from a scene score.
- **`mux-audio` works on real `chain` output**, and the length mismatch was
  reported exactly as this file promises. Picture 30.2s against a deliberately
  28-second track:

  ```
  NOTE: the picture is 30.2s and the audio is 28.0s — the result runs 28.0s;
  the picture is truncated by 2.2s.
  ```

  The result is **28.000s with exactly one audio stream** — and the segments
  had come back carrying the model's own generated audio, so this is a
  measurement of `mux-audio` **replacing** a track rather than mixing onto a
  silent file.
- **So the arithmetic's whole design reason is now measured rather than
  reasoned.** Both roundings in Step 2 go up, the picture outlasts the track,
  `mux-audio` runs to the shorter of the two, and what gets lost is the tail
  of the picture while the song finishes. That is what happened, on a real
  chain product, with the note saying so at the time.

🚨 **What this run does not license, and it is the part a user is being asked
to approve.** The arithmetic in Step 2 has a three-minute track landing on
**seven** jobs. Three were run. **Three segments is the verified scale of this
skill; seven is an untested ceiling**, and the difference belongs in front of
the user rather than in this section alone — Step 2's table now carries it.

- **Four segments and up are untested**, and so is everything about what
  drifts across four, five or six seams — palette, brightness, whether the
  style anchor survives being re-read that many times. Two seams held; that is
  what was measured, and two is not four.
- **The 10-shot cap was never approached.**
- **Segments were 10 seconds, not the 20–30 this file's arithmetic normally
  produces.** A longer segment is a longer single job, not three of these — so
  even the three-segment result is evidence at a segment length this file
  rarely recommends.
- **The audio was a synthesised tone, not music.** Nothing here says how a
  real song sits against these visuals — the model never hears it either way,
  so what is untested is the *judgement*, not the mechanism. It is also why
  the run cannot speak to the thing a user actually cares about.
- **480p, and `--generate-audio` was left at the server default** rather than
  set to `false` as this file recommends. The mux replaced the track anyway,
  which is the point of the default rather than a contradiction of it.

**The deliberate decision not to close this gap**, recorded so nobody reopens
it by accident: generating a full seven-segment chain at the lengths this file
recommends would cost about $7.70, and the repo owner chose on 2026-09-17 to
**scope the documentation to the measured scale instead of buying the
measurement**. That is a cost decision, not a claim that seven segments fail.
If a real seven-segment run ever happens, this section is where it lands.

The rest of what this file rests on:

| Claim | Strength |
|---|---|
| A supplied audio track does not become the clip's audio | **Measured**, job `d8561509-dcc6-4f2c-8864-a193cd239b14`, 55 cents, 2026-09-15 — envelope correlation 0.41 between the supplied speech and the delivered track |
| `mux-audio` puts a specific track on a clip locally, at no cost | **Measured** on this skill's own run above — real `chain` output, the clip's own audio replaced rather than mixed, the result running to the shorter of the two, and the `NOTE:` naming which one was cut and by how much |
| `chain` carries a shot's closing frame into the next shot's opening frame | **Measured** across three shots and two seams on this skill's own run, and on an earlier two-shot run where shot 2 opened on very nearly the exact frame it was fed. Brightness can shift slightly across a seam |
| Cut timestamps inside one job are executed as cut boundaries, to about ±1 second | **Measured**, two jobs at 8s/480p (`fe6e7130`, `13b75096`), in two different timestamp notations |
| A cut written at one named second is weaker than a cutting *rhythm* | **Measured** — `9cd773d0` wrote three hard-cut stamps in 15 seconds, one landed, two cuts arrived that nobody asked for |
| Whether a written hard cut renders at all depends on the **mix** of the timeline | **Measured**, six jobs. A timeline where 3 of 9 boundaries were hard cuts rendered **none** of them; 3 of 8, 3 of 6, 5 of 7, 4 of 4 and 6 of 6 all rendered every one. Weighting the mix toward hard cuts is what buys a cutting rhythm |
| The measured envelope inside one job: 10 shots, up to 6 hard cuts, 8–30 seconds, 480p and 720p | **Measured**. More shots, more hard cuts, 1080p or the `volcengine` upstream is past it — price a first attempt as an experiment |
| Asking this model for music can fail output moderation on copyright | **Measured** once, job `1ff72400`, unbilled: "the output audio may be related to copyright restrictions". It decides the `--generate-audio false` default below |
| A photoreal person in an **attached** frame is refused at submission on `bytedance/seedance-2.5` | **Measured** 2026-08-30, `input_moderation_failed`, nothing billed. It decides the performer limit below |
| A fixed seed does not reproduce a take | **Measured** 2026-09-15 — three submissions of one byte-identical request on seed `424242`: two completed as visibly different clips, one failed outright |
| "Cut density by energy", "sections become segments", the whole mapping from a piece of music to a segment plan | **This skill's own reasoning**, built on the measurements above. The run above exercised the mechanism — segments, seams, mux — and nothing in this repo has yet cut a piece to a real track and judged whether it works as a music video |

Practical consequence: the **pipeline** is no longer the experiment — three
segments, two seams and the mux have been run. The **scale** still is: four
segments and up, 20–30-second segments and a real track have not. Draft one
segment cheaply, look at it, then price the **whole** chain — segment 1
included, because the chain regenerates it. The draft is information, not the
first link.

## Step 3: writing the visuals

The shared craft is not repeated here — the vendor's formula, the header
manifest, the timeline shapes, the camera and transition vocabularies, the
consistency lock and the negative-list rows are all in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md).
What follows is what is specific to writing picture for a piece of music.

### Cut density is a register, not a number

Pick the register from the section's energy and write the shot lengths into
the timeline. The ranges are measured across the prompt gallery and this
repo's own runs:

| Section feels | Register | Written as |
|---|---|---|
| driving, high energy, a chorus or a drop | **dense** — 2–3 seconds a shot | timestamped hard cuts, most or all boundaries hard. 10 shots in 30 seconds is the top of the measured envelope |
| moving, a verse | **mid** — 3–5 seconds a shot | timestamped cuts; nothing collected holds a cut shot longer than about five seconds |
| open, ambient, an intro or a breakdown | **one continuous shot** | declare `one continuous shot, no cuts` in the first sentence and give the camera somewhere to travel — the measured one-takes change what they are looking at every six to eight seconds, so a static camera holding for 30 seconds is the one shape that is not in the evidence |

**If a section needs to cut, weight the whole segment toward hard cuts.** This
is measured and it is the lever with evidence behind it: a timeline where only
3 of 9 boundaries were labelled hard cuts rendered **zero** of them, while
every job whose hard-cut share was 3-of-8 or higher rendered all of them.
A chorus that is nominally a cutting section but is written with mostly
continuous transitions can come back as one flowing take.

### A number in the prompt is a wish

Measured repeatedly and it matters here more than in any other scenario,
because music is where the temptation to write numbers is strongest: **what a
thing looks like renders; a quantity attached to it does not.** `a full 360
degrees` came back as about half a turn, twice. Three interior waypoints in a
four-second move produced two.

So:

- **BPM belongs in your arithmetic, not in the prompt.** Use it to choose the
  register and the shot count; writing "cuts on the beat at 128 BPM" into the
  prompt does not synchronise anything and costs words.
- **Do not promise "the cut lands on the drop".** Write the drop's section as
  its own segment so the *segment boundary* — which you control, because it is
  a separate job — falls there, and write the segment's opening as the
  strongest picture in the piece.
- A **budget** phrasing is the one time-axis instruction measured to hold:
  `at most 0.2 seconds of slow motion, only at the moment the figure lands`
  was honoured where flat prohibitions on tempo were not.

### The energy arc is a property of the whole piece, not of one segment

Each segment is a separate job that shares nothing with its neighbours except
the frame `chain` carries. So the arc has to be written into the segment
prompts deliberately:

- **Repeat the consistency lock word for word in every segment** — palette,
  subject, setting, light direction, style anchor. Copy it, do not rephrase
  it; a rephrased lock is a different instruction.
- **Escalate one axis at a time** across the segments — density of movement,
  how close the camera is, how much of the frame the subject fills, how warm
  or cold the light is. Naming the axis per section is what makes an arc
  rather than six unrelated clips.
- **The chain's carried frame is a strong constraint and a gift**: segment N
  opens on segment N-1's closing frame, so the piece is visually continuous
  whether or not you asked. Write each segment's *opening* as a continuation
  of what the previous one ended on.

### No music in the prompt. Ever. In this skill above all

Three reasons, stacked:

1. **You are replacing the audio anyway.** `mux-audio` overwrites the clip's
   own track with the user's. A generated score is bought and thrown away.
2. **Asking for music has failed output moderation on copyright** — measured,
   unbilled, with the upstream message naming audio copyright. On a `chain`
   that failure stops the whole run, so it costs the segments you already paid
   for in wall clock and the ones you have not reached in rework.
3. `--generate-audio false` **removes the audio stream entirely** rather than
   muting it (measured, three runs). That is exactly the state you want before
   a mux: one video stream in, one audio stream in, no ambiguity.

So: `--generate-audio false` on every segment, `No music.` in the `SOUND`
line, and the music words in `AVOID` — score, soundtrack, instrumental,
melody, rhythm track, percussion, named instruments, humming, singing. Naming
them in both places is what the two clean runs in this repo did.

### Lyrics and on-screen text: not from a description

The classic music-video ask is lyrics on screen. **Text rendered from a
description comes back invented or garbled** — measured across several jobs
here — while text approved on a still image and attached as a frame is
preserved. So:

- **Do not promise lyric text.** Put the text items in `AVOID` (subtitles,
  captions, on-screen text, lyrics, watermarks, logos) and keep lettered
  surfaces out of the set — a negative list alone has been measured failing on
  a set full of signage.
- **Lyrics go on in an editor afterwards**, where they are free, correct,
  timed to the actual waveform and editable. This is usually good news and
  worth saying early: an editor can sync words to a beat, and this API
  demonstrably cannot.

### Performers: the wall to state before anyone plans a band

**A photoreal person in an attached frame is refused at submission** on
`bytedance/seedance-2.5` (`input_moderation_failed`, nothing billed, measured
2026-08-30). `chain` attaches a frame to every segment after the first. So:

**The rule is about the attached picture, not about the video's content** —
which is the distinction that decides what is still available here. Measured:
a job whose first frame held a product with no person in it ran fine while a
model walked into shot at 4 seconds and stayed there for seven or eight. So in
a chain, what has to be free of a photoreal person is each segment's **closing
frame**, because that is the picture the next job attaches.

| Visual subject | Chains? |
|---|---|
| landscape, abstract, product, architecture, texture, motion graphics | **yes** — the measured-good case |
| illustration, anime, a non-photoreal character | **yes** — an anime pair passed as an attached frame completed |
| a photoreal person written in text, **who has left the frame before the segment ends** | **yes** — this is the measured route above, applied per segment. It is also the fiddliest thing in this file: every segment has to be written to end on the place rather than on the person |
| a photoreal person **still in shot at the segment's last frame** | **no** on this model. The chain stops at the next submission, unbilled — the segments before it are kept and paid for |
| **the same** photoreal performer across the whole piece | **no** by any route measured here. Each job generates its person fresh, and the mechanism that would carry them is the refused one |

So a piece that needs a performer has four honest options: write them in and
end every segment on the set (they will not be the same person from segment to
segment — fine for a montage, not for a narrative); make them non-photoreal;
drop the performer and let the piece be about the place; or use a different
model — and note that two other models have been measured accepting a
real-person portrait for image-to-video, while **their `chain` behaviour has
never been tested in this repo.** Do not promise it.

**One thing that is measured and still does not change the table above.**
`--real-person true` lifts seedance-2.5's submission refusal (2026-09-16 —
[`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)
→ "`--real-person true` lifts that refusal on 2.5"), and `chain` would pass
the flag through to every segment. It is not a route out of this wall, for two
separate reasons: the flag is how a caller asserts they hold the rights to a
**real person's** likeness, which a face the model invented in the previous
segment is not, and no chain has ever been run with it set. Offering it here
would be inventing an authorisation and a measurement at once.

## The prompt template

One prompt per segment. A 30-second segment is long enough for the full
skeleton; a shorter one drops the manifest. Slots in `<angle brackets>`.

```
<STYLE: the medium and texture anchor, written identically in every segment — film stock or era, grain, palette in named colours>
<SUBJECT: what the piece is about, described physically, identically in every segment>
<SCENE: where it is, the light source and its direction, the foreground layer>

<0-3s>   <shot size>, <camera position>, <movement or "static">. <one action>. <what the light does>
<3-6s>   <Hard cut. | Without cutting,> <shot size>, ... 
<6-9s>   ...
<...>    ...
<T-2 - T s>  <the closing picture — this is what the next segment opens on, so make it a picture worth continuing from>

CAMERA: <the register: "hard cuts every 2-3 seconds, one camera movement per shot" | "one continuous shot, no cuts; the camera crosses the space">
CONSISTENCY: <subject>, <palette>, <setting>, the light direction and the <style anchor> stay identical for the whole segment.
SOUND: <room tone or the ambience of the place>. No music.
AVOID: subtitles, captions, on-screen text, lyrics, watermarks, logos; music, score, soundtrack, instrumental, melody, rhythm track, percussion, cello, strings, piano, drums, humming, singing; <the style you are not making>; extra or warped limbs; a phone, a camera or a tripod visible in frame.
```

Four notes:

- **The `STYLE`, `SUBJECT` and `CONSISTENCY` blocks are copied verbatim
  between segments.** That plus the carried frame is the whole of the
  continuity mechanism.
- **The closing beat of each segment is load-bearing**, because it becomes the
  next segment's first frame. End on a picture, not mid-move.
- **`hold the final frame` buys about two seconds, not one** (measured on two
  clips of very different lengths). On a 30-second segment that is fine; on a
  short one it is a quarter of the clip, so schedule the last action to finish
  early rather than restating the number.
- **No music line, per above.** The `SOUND` line still earns its place: room
  tone and diegetic sound shape what the model *pictures*, even though the
  track is discarded.

### Worked example — one 28-second segment, written against an invented track

**This has not been generated.** It is the template filled in — and the "3:12
track" it belongs to is not a real song. Its length, its chorus and its
section boundaries were invented for the illustration. The example reads with
the confidence of the measured sections around it, so: **do not carry that
confidence onto a track whose structure nobody has told you.** With no
section map, this is `even segment 3 of 7`, not "the chorus".

```
STYLE: 16mm colour film texture, visible fine grain, slight gate weave; a cold blue-grey and sodium-amber palette throughout, highlights rolling off rather than clipping.
SUBJECT: an empty coastal road at dusk, wet tarmac, low scrub either side, a line of concrete power poles running to the horizon.
SCENE: the sun is already down; the sky holds a cold blue band low over the sea to the left, and a single sodium lamp on the third pole is the only warm source. Sea mist drifts across the road at knee height.

0-3s: Extreme wide, low angle from the road surface, static. The poles recede into the mist; the sodium lamp flares softly. Wet tarmac holds a long amber reflection.
3-5s: Hard cut. Macro insert, static, on a puddle at the roadside; the amber reflection breaks as a drop lands in it.
5-8s: Hard cut. Wide, eye level, a slow lateral track to the right past the scrub; the mist moves against the camera's direction.
8-11s: Hard cut. Low angle looking up the nearest pole into the blue band of sky, static, the lamp burning at the top of frame.
11-14s: Hard cut. Extreme wide from behind, the road running away; the mist thickens and the far poles disappear into it.
14-17s: Hard cut. Macro insert on the wet surface, the amber reflection sliding as the light source passes.
17-21s: Hard cut. Wide, low angle, a slow push down the centre line toward the sodium lamp, which grows in frame.
21-24s: Hard cut. Close on the lamp housing itself, the filament colour resolving out of the flare, the mist moving through the beam.
24-28s: Hard cut. Extreme wide, high angle, the whole road and the line of poles with the sea beyond; the mist settles; the frame holds on that picture.

CAMERA: hard cuts throughout, one camera movement per shot, nothing held longer than four seconds. Aggressive cutting, but each picture stays readable.
CONSISTENCY: the road, the line of poles, the single sodium lamp, the blue-grey and amber palette, the mist height and the 16mm grain stay identical for the whole segment.
SOUND: wind across open ground, distant surf, the tick of the lamp. No music.
AVOID: subtitles, captions, on-screen text, lyrics, watermarks, logos; music, score, soundtrack, instrumental, melody, rhythm track, percussion, cello, strings, piano, drums, humming, singing; people, vehicles, animals; CGI sheen, plastic surfaces, over-exposed glow; a phone, a camera or a tripod visible in frame.
```

Eight boundaries, all of them hard cuts — an 8-of-8 hard-cut share, which is
above every mix measured to render its cuts, and 9 shots in 28 seconds sits
just inside the measured envelope of 10 shots in 30. The closing wide is
written as a held picture on purpose: it is what the next segment opens on.
The *last* segment of the piece wants the same treatment for a different
reason — the mux's four-second trim lands there, and a held picture is the one
thing that can lose four seconds without losing anything.

## Before you spend: the approval gate

**Never submit a paid job until the user has seen a cost table and said yes.**
The rule, the required columns and where the numbers must come from are
written down once for every Ofox skill in this repo:
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).
Its "Batches get an itemised table, not one total" section governs this skill
— a piece is a batch by another name.

Get the number from `chain --dry-run`, which validates everything, prices the
**whole sequence**, and sends no request:

```bash
bash ../ofox-video-core/references/ofox-video.sh chain --dry-run \
  --shot "<segment 1 prompt>" \
  --shot "<segment 2 prompt>" \
  --shot "<segment 3 prompt>" \
  # ... one --shot per segment, seven of them for the 3:12 track below ...
  --duration 28 --resolution 720p --aspect-ratio 16:9 \
  --generate-audio false \
  --name "<the track's name>" \
  --out-dir /absolute/path/to/out
```

It prints exactly one `Estimated cost:` line covering every shot — the line
says "takes" where it means shots, which is the shared estimator's wording,
not a different unit. **Relay that line; never a figure of your own.** Then
wait for an explicit yes, then re-run the identical command with `--dry-run`
swapped for `--approved`.

`--approved` is where that yes gets typed out. Since `ofox-video-core` 2.0.0
the four billable subcommands — `generate`, `create`, `batch`, `chain` —
refuse to run without it, while `--dry-run` never needs it, so the quote above
is still free and still works with no API key. Be exact about what the flag
does: it records a stance, it cannot prove one. Nothing in a shell script can
observe the conversation you had, and it can be typed without showing anyone a
price. What it changes is that spending without quoting is no longer the
default — it has to be written into the command, where a transcript shows it.
A chain is the worst place to skip that, because one command commits every
segment at once. The rule above is still the rule, and it is still yours to
follow.

🚨 **Before relaying anything, check that `SHOTS_REQUESTED` equals your segment
count.** One `--shot` per segment, always; `--shots-file` reads one prompt per
line and shreds a templated prompt into a job per line. The full rule, with
what was reproduced, is in "Step 4" — read it before building this command,
not after the estimate looks surprising.

⚠️ **A chain dry run does not print the model id.** It validates the first
shot through `generate --dry-run` and discards that output, so what comes back
is the estimate line, `STATUS dry_run` and `SHOTS_REQUESTED` — no `MODEL`
line. The cost table has to name the id that will really be sent, so when the
model was not passed explicitly, get it from a single-shot dry run, which is
also free:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "<segment 1 prompt>" --duration 28 --resolution 720p \
  --out-dir /absolute/path/to/out | grep '^MODEL '
```

### The table this scenario has to show

Rows are segments. The money is the dry run's total. The three lines above the
table are what stop someone approving a sixth of what they are about to spend:

```
Track: "<name>" — 3:12 (192 seconds, read with ffprobe)
One job caps at 30 seconds on <model id>, so this piece is 7 segments minimum.
7 x 28s = 196 seconds of picture for 192 seconds of music; the 4 spare seconds
of picture are trimmed by the mux, and the song finishes.

| Model ID | Type | Parameters | Section | Qty |
|---|---|---|---|---|
| <model id> | video (t2v) | 28s, 720p, 16:9 | intro + verse 1 | 1 |
| <model id> | video (t2v) | 28s, 720p, 16:9 | verse 1 into pre-chorus | 1 |
| ... | | | | |
| **Total** | | **7 segments x 28s = 196s** | | **7** |

Estimated cost: <the chain --dry-run line, verbatim>
Laying your track on afterwards: no API call, no cost.
```

Four rules for it:

- **The total is what the yes is given against**, and it is the dry run's
  figure. Do not divide it into a per-segment number and lead with that — the
  per-segment figure is the `BATCH_COST_PER_TAKE` mistake in a different
  costume, and here it understates by six or seven times.
- **The `Section` column says where the names came from.** The example above
  is a table for a track whose sections the user supplied. With no map, that
  column reads `even segment 1 of 7` and so on — never an invented
  intro/verse/chorus, which in a cost table looks exactly like a fact the user
  provided. See "It is the most valuable input and it is still `ask-if-open`".
- **Show the full prompt of at least the first segment** alongside the table.
  The user is paying for the prompts; a piece that costs exactly what you
  quoted and looks nothing like their song is still a wasted spend.
- **Say the mux is free.** People assume the audio step costs something.
- **A draft segment is its own stage above this table, and its cost adds.**
  It is not link 1 of the chain and nothing is subtracted from the total below
  it — see "Draft cheap, render the keeper". Show stage 1 (one row), stage 2
  (this table), and a combined figure, so the yes is given against everything
  that will actually be billed.
- **A chain commits at the yes.** Shots are submitted one at a time and a
  rejected submission stops the rest, so the guard is real — but the whole
  sequence is a single approved number, and the cost table is the only place
  it can be stopped.

Afterwards the **actual** bill is `CHAIN_COST_TOTAL`, built from each job's
own usage. Report it as money, not as a raw ten-decimal string, and say how
many segments it covers.

This skill has exactly **one cost anchor**, and it is a small one: three
10-second segments at 480p on `bytedance/seedance-2.5`, billed **3 dollars 30**
in total, 1 dollar 10 a segment (2026-09-16). A real piece is longer segments,
a higher tier and more of them, so that number ranks rather than quotes — the
`--dry-run` figure at the parameters you are about to send is still the only
one to put in front of anyone.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| command | `chain` | the segments have to stay continuous, and `chain` is the measured mechanism for that. `generate` for a single-section job, where there is nothing to chain |
| `--duration` | `ceil(track / segments)`, where `segments = ceil(track / the model's maximum)` — the arithmetic in "Step 2" | the segment count is set by the model's ceiling (fewer, longer jobs means fewer seams, and the bill is per second either way), and then the length is set by the track, so the overshoot is a few seconds rather than up to a whole segment. `ofox-video.sh models` prints each model's real range, minimum included |
| `--generate-audio` | **`false`**, always | the track is replaced by the mux anyway; a generated score is bought and discarded, and asking for music has failed output moderation on copyright here. It removes the stream entirely rather than muting it, which is what you want before a mux |
| `--resolution` | draft one segment at the cheapest tier, deliver at the tier the piece is for | this is the longest-form scenario in the repo, so the draft-then-render ladder saves the most here. The draft is a **separate, discarded** job — the chain regenerates its own segment 1, so quote the two stages and add them up |
| `--aspect-ratio` | `16:9` unless the brief said otherwise; it applies to segment 1 and the rest inherit their shape from the carried frame — the script prints a `NOTE:` saying so | music is watched landscape unless it is being posted to a feed |
| `--model` | the script's own default — **unless the user named one**, which always wins | see "Draft cheap, render the keeper". A `chain --dry-run` does not name the resolved id; a one-shot `generate --dry-run` prints it on a `MODEL` line, and that is the id the cost table has to carry |
| `--name` | always, named after the track | segments land as `<name>-shot<N>-<short job id>.mp4`, which is what keeps them in order on disk. Without it every segment shares one slug |
| `--seed` | leave it alone | `chain` would pass one seed to every segment, and a fixed seed does not reproduce a take anyway (measured). The script rolls and prints one per shot; that is a record, not a handle |
| `--out-dir` | always, absolute | see "Where the files land" |
| `--shot` | **one per segment, always** | the only safe way to pass a multi-line prompt. See the rule in "Step 4" |
| `--shots-file` | **never in this skill** | it reads one prompt per line, so a nine-line templated prompt becomes nine separately billed jobs. The core rejects the labelled shape and cannot catch a prose-lined one |
| `--no-concat` | not passed | the join is what you mux onto. Skip it only if the segments are going into an editor individually |
| `--real-person` | leave unset | nothing in this skill's route needs it, and `chain` has never been run with it either way. `true` is Ofox's privacy-preserving preprocessing path for **authorised** real-person reference images, measured lifting seedance-2.5's submission refusal on 2026-09-16 — an authorisation route, never a way past the check, and never set on a user's behalf. See [`api-params.md`](../ofox-video-core/references/api-params.md) → "`--real-person true` lifts that refusal on 2.5" |

## Step 4: generating, then the audio

🚨 **One `--shot` per segment. Do not use `--shots-file` in this skill.**
`--shots-file` is **one prompt per line**, and this skill's prompt template is
nine lines, with a nine-line worked example to match. Every non-blank line
becomes **its own shot — its own separately billed, full-length job.** This is
the most tempting place in the repo to reach for that flag, because seven long
prompts on one command line look unwieldy.

Reproduced 2026-09-15 against the real script, at zero cost with `--dry-run`:
a **five-line prompt** came back as `Chaining 5 shots` / `SHOTS_REQUESTED 5`
and was quoted as five full-length segments.

**The dangerous case is the small one, which is the opposite of what you would
guess.** A whole seven-segment piece in one file is over sixty lines, and
`chain` caps at ten shots — so it dies locally with an error, free, before
anything is submitted. But **one** nine-line templated prompt is nine shots,
which is *under* the cap: it validates, prices and runs, and what comes back
is nine separately billed jobs of one segment's worth of writing. Nothing
about that looks wrong until the bill.

`ofox-video-core` **1.26.0** refuses the shape it can recognise — a file whose
lines open with ALL-CAPS labels (`STYLE:`, `CAMERA:`) is rejected before
anything is submitted, naming the reason. **Do not rely on that guard.** It is
a heuristic, it does not exist below 1.26.0, and the same five-line prompt
written as plain prose sentences — which is exactly how the descriptive half
of a segment reads — goes straight through and quotes five jobs. Reproduced
too, in the same session.

**The number that catches it either way is `SHOTS_REQUESTED` in the dry run.**
Read it before every yes. If it is not your segment count, stop — you are
holding a quote for a different piece of work.

Long prompts belong in shell variables, which keeps one `--shot` per segment:

```bash
SEG1=$(cat <<'EOF'
<segment 1 prompt, all nine lines of it>
EOF
)
```

```bash
# 1. the segments, in order, each opening on the previous one's closing frame
bash ../ofox-video-core/references/ofox-video.sh chain --approved \
  --shot "$SEG1" \
  --shot "$SEG2" \
  ... \
  --duration 28 --resolution 720p --aspect-ratio 16:9 \
  --generate-audio false \
  --name "coast road" \
  --out-dir /absolute/path/to/out

# 2. the track, laid on the joined file. Local, no API call, no key, no cost.
bash ../ofox-video-core/references/ofox-video.sh mux-audio \
  /absolute/path/to/out/chain-joined-<stamp>.mp4 \
  /Users/me/music/coast-road.wav \
  --out-dir /absolute/path/to/out
```

`--approved` sits on step 1 only. `mux-audio` is local ffmpeg — no request, no
key, no cost — so there is nothing there to approve. Without the flag step 1
refuses, submits nothing and prints the quote-first steps instead; add it once
the table above has come back with a yes, which the flag itself cannot check
for you.

What `chain` prints: `STATUS chain_completed`, `SHOTS_REQUESTED`,
`SHOTS_COMPLETED`, one `SHOT N <job id> <cost> <path>` line per segment,
`JOINED <path>` for the stitched file, `CHAIN_COST_TOTAL` and
`CHAIN_COST_PER_SHOT`. **`JOINED` is the input to step 2** — mux onto the
joined file, not onto a single segment.

What `mux-audio` prints: `MUXED <path>` — and a `NOTE:` on stderr if the two
durations differ by more than half a second, saying which one was cut and by
how much. **Relay that note.** A user whose song was truncated by four seconds
needs to hear it from you rather than discover it on playback.

The muxed file is the deliverable. Report its **absolute** path on its own
line.

If `chain` stopped partway, the segments it did generate are kept, downloaded
and listed with their real cost, and the remaining ones were never submitted.
A partial run is not a complete one — say how many landed, what the exit code
was, and what it will cost to finish, as a new table.

## After it lands: what to actually check

Four things, before calling it done. None of them is `STATUS chain_completed`.

1. **Does the muxed file carry the right audio, all the way to the end?**
   Play it. This is the whole product; it is also the step where a `NOTE:`
   about a truncated track is easiest to miss.
2. **Did the cuts happen?** Sample frames at 1–2 fps and read either side of
   each written boundary. **Do not trust a scene detector's count** — it
   under-reports cuts whenever two shots share a location and a light, which
   is the normal case in one segment of one music video, and no threshold has
   been right twice in a row in this repo. Read the frames.
3. **Do the seams hold?** Look at the last frame of each segment against the
   first frame of the next. The carried frame makes them very close;
   brightness can shift slightly across a seam, which is expected and is
   usually fixable with a one-frame dissolve in an editor.
4. **Did any lettering get invented?** Check a few frames for captions,
   signage or a logo nobody asked for.

And do not rank the segments by "how much is happening" off a scene score —
it counts pixels, not motion, and on a dark set it inverts the order.

Report what you checked, not just that it finished.

## The unmeasured edges

Written as "no evidence yet", because every one of these is a measurement
nobody has made rather than a thing the API cannot do. A later run that
settles one of them **adds** a path to this file; none of them overturns it.

### Whether an audio reference conditions the visuals at all — undecided

What is settled: a supplied audio track does not become the delivered track.
What is **not** settled: whether the model's *picture* is influenced by an
audio reference at all — pacing, mood, where it chooses to cut. One run cannot
separate "ignored" from "weakly conditioning".

**And the obvious experiment does not work on this API**, which is the part
worth understanding rather than just believing:

> The natural design is "same prompt, same seed, audio versus no audio, look
> at the difference". It does not isolate anything here, because **a fixed
> seed does not make this API reproducible.** Measured 2026-09-15: three
> submissions of one byte-identical request on `bytedance/seedance-2.0-mini`,
> seed `424242` — two completed as visibly different clips (the same subject
> at a different position, with 13x the pixel area at t=1s) and one failed
> outright. With the control arm that unstable, any difference the audio arm
> shows is indistinguishable from the noise between two runs of the control.

Settling it therefore needs a **distribution** comparison — many runs each
side, on a measurable property — not a repeat. That is a real experiment with
a real budget, and it is deliberately not in this skill's scope. Until it is
run, this skill does not send audio, and nothing here should be read as saying
audio conditioning is impossible.

### Whether a chained sequence really holds across six or seven segments

`chain` is now measured across **three** jobs and two seams — 2026-09-16, both
seams carrying street, signage, reflections and framing, the second no worse
than the first — and one job is measured holding up to 10 shots and 6 hard
cuts. A seven-segment piece still multiplies both, and nobody here has run
one: **four, five and six seams are untested**, and so is the 10-shot cap.
What could drift over that distance: the palette, the cumulative brightness
shift, whether the style anchor survives being re-read six times. The run that
exists was also 10-second segments, not the 20–30 the arithmetic normally
produces. Draft the first two segments before committing to seven.

### Endings, when the picture outruns the track

Both roundings in Step 2 go up, so the picture is normally a few seconds
longer than the song, and `mux-audio` trims that difference off the end.
**That is measured now, not just reasoned** — 2026-09-16, 30.2s of chained
picture against a 28-second track: the mux printed which one it cut and by how
much, and the delivered file is 28.000s with the audio intact and the tail of
the picture gone. The
second rounding keeps it to a few seconds rather than up to a whole segment,
which is most of the problem solved — but it is not all of it, because
**whatever you wrote as the final beat may still land inside the trim.** Three
routes exist — generate the last segment on its own at exactly the remaining
seconds (`generate`, opened on the previous segment's closing frame), trim the
picture deliberately before the mux, or simply let the tail go — and **this
round does not choose between them.** The working advice until one is tested:
write the last segment so its final seconds are a held picture rather than a
payoff, and tell the user the tail is trimmed.

The reverse case — picture *shorter* than the track — cuts the song off
mid-phrase. The arithmetic is written to avoid it; if it happens anyway
(a segment failed, a duration was overridden), add a segment rather than
shipping a truncated song.

### Everything about the mapping from music to picture

The cut-density register, sections-become-segments, the energy arc: all of it
is reasoning from measured facts about the API, not a measurement of music
videos. The 2026-09-16 run measured the **mechanism** — segments, seams, mux,
the length note — against a synthesised tone. **No piece has been cut to a
real track and judged against it**, which is the part of this file that is
craft rather than measurement, and the part a first real piece is testing.

### Other models

`chain` and its real-person limit are measured on `bytedance/seedance-2.5`.
Two other models have been measured accepting a real-person portrait for
image-to-video, and their chaining behaviour is **untested here** — that is a
new mechanism on a new model, not a restatement of a measured one.

## Choosing a model

The model stays **never-ask** — the agent doesn't raise it. But never-ask is
not "never listen": if the user names a model id or a shorthand, use it.

**Model ids, prices, resolutions, durations and aspect ratios are deliberately
not tabulated in this file.** They are catalog facts, they change, and this
repo has recorded defects that trace to a hardcoded copy of somebody else's
value table. Read them live with `models` and `providers` (above), free and
with no API key.

Two things specific to this scenario:

- **The maximum duration is the axis that matters most**, because it decides
  the segment count and therefore the bill's shape. A model that caps at half
  Seedance 2.5's ceiling doubles the number of jobs for the same track. Check
  the range before quoting a segment count.
- **Moderation policy is per-model**, so a look refused on one model can be
  accepted on another — changing model after a refusal is a route, not a
  downgrade.

## Pricing a job with no API key

`models`, `providers`, `chain --dry-run` and `generate --dry-run` all work
with `OFOX_API_KEY` unset. So a user who hasn't signed up can have their track
read, the segment plan made and the whole piece priced before deciding whether
to register. **Quote it first; don't open with a signup link.** `mux-audio`
and `last-frame` need no key either.

## If the script isn't found

```
bash: ../ofox-video-core/references/ofox-video.sh: No such file or directory
```

Nothing is broken — this skill delegates all execution to `ofox-video-core`
and reaches it by relative path, and that path just missed. Two different
situations wear this message, so run the probe in "Where the core skill lives"
before deciding which:

- **The probe printed a directory** — the core is installed and only the
  directory *name* was wrong, which is the normal LobeHub case
  (`ofoxai-skills-ofox-video-core`). Re-run against what the probe printed.
- **The probe printed nothing** — `ofox-video-core` really is absent, and
  installing it is the user's call to make, not yours: an install writes
  outside this working directory, so hand over the command and let them run
  it rather than running it for them. Which command depends on the installer
  they already have — skills.sh is
  `npx skills add ofoxai/skills --skill ofox-video-core`, which asks for that
  one skill and answers none of the agent, scope or confirmation questions on
  the user's behalf; this repo's own wrapper is
  `npx ofox-skills ofox-video-core`, the same install with all three answered
  in advance (every agent, user-level, no prompts); on LobeHub or ClawHub,
  install `ofox-video-core` from the same publisher. Ask for the one skill
  that is missing rather than the whole repo, and give all three routes —
  pointing a LobeHub user at the skills.sh line alone reads as "abandon your
  installer", which isn't the advice.

Either way, name the missing skill and where it was expected rather than
relaying the raw path error, which names neither.

A broken link to a shared reference has the same two causes. This skill
degrades gracefully: the arithmetic, the question set, the template, the
defaults and the mux step are all written out here. What is out of reach is
the depth behind them — the full camera and transition vocabularies, the
gallery cases behind the cut-density ranges, and the exact wording of the
spend gate, which stays mandatory either way.

## Exit codes worth knowing

Full table in [`../ofox-video-core/SKILL.md`](../ofox-video-core/SKILL.md).
The ones that come up:

| Code | Meaning | What to do |
|---|---|---|
| `1` | Parameter rejected locally, no network call, nothing billed | Fix the flag and retry freely — a duration past the model's ceiling lands here |
| `2` | Environment problem — `curl`/`jq` missing, no `OFOX_API_KEY`, or **`ffmpeg` missing when `chain` needs it**. Checked before anything is submitted | Install it and re-run; nothing was billed |
| `3` | API rejected it, a job ended failed/cancelled/expired, or a chain stopped partway | Read the mapped message. Segments already generated are kept and listed; a rejected create was not billed |
| `4` | Timed out waiting — **the job is still running and billable** | `poll JOB_ID`, never re-run `chain` from the top |
| `5` | Ambiguous network failure on create | Do not retry blindly; check https://app.ofox.ai first |
| `6` | `--out-dir` unusable | Fix the path; if it happened after a create, `poll JOB_ID` into a writable directory |

## How long to tell the user it will take

Each segment blocks while it polls, up to `--max-wait` (default 540s), and
**`chain` runs them one after another** — its shots are sequential by design,
because each one needs the previous one's closing frame before it can be
submitted. That dependency is irreducible.

So a six-segment piece is six clips' wall clock, not one. A **15-second** 720p
job has been measured here taking over 600 seconds on its own, and the
segments this skill sends are longer than that — so budget generously and tell
the user before starting rather than leaving the wait silent. Half an hour or
more is a normal answer for a three-minute track. If your tool call cannot
stay open that long, run
the segments as separate `generate` calls with `last-frame` between them, so a
timeout never strands a job whose id you never saw.

Never re-run `chain` after a timeout. The segments it paid for are on disk and
the one still running has a job id to `poll`.

## Where the files land

Always pass `--out-dir`, and **make it an absolute path**. Without it the
script writes to the current working directory — which, given that the
examples here run from this skill's own directory, would drop a user's whole
piece inside an installed skill.

What ends up there: one mp4 and one `.json` sidecar per segment, the
`chain-frame-N.png` handoff frames, `chain-joined-<stamp>.mp4`, and after the
mux, `chain-joined-<stamp>-with-audio.mp4`. **Relay the absolute path of the
muxed file on its own line** — it is the deliverable; the rest is working
material.

Each sidecar holds the full job id, the prompt as submitted, the seed and the
real cost. That is what a later re-render of one segment reads its prompt back
out of; a retyped prompt is a new prompt.

## Common failure modes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| The user expected the model to listen to the track | The expectation was never corrected | Correct it **before** the cost table, in the recap. Afterwards there is no remedy but another spend |
| The user says the sections are in the wrong places, or that their song has no chorus there | A structure was invented and presented as theirs. Nothing in this flow hears the track | Preventable only: with no map, call them even segments and label any proposal as invented. After the fact it is a re-generation and a new cost table. See "It is the most valuable input and it is still `ask-if-open`" |
| The cuts do not land on the beat | Expected, and measured: written cut stamps land to about ±1 second, and a stamp is weaker than a rhythm | Not fixable in the prompt. Generate longer continuous material and cut it to the grid in an editor. Say this up front, not here |
| A whole segment came back as one flowing take when cuts were written | Measured: a timeline weighted toward continuous transitions pulls labelled hard cuts continuous with it — 3 of 9 rendered zero | Re-weight the segment so most or all of its boundaries are hard cuts. New job, new cost table |
| The finished video is shorter than the song, and the song is cut off | The picture was shorter than the track and `mux-audio` runs to the shorter | Add a segment and re-join. The `NOTE:` on the mux said this at the time — relay it |
| The last few seconds of picture are missing | Expected: the segment count rounds up, so the picture overruns and the mux trims the tail | Write the final segment to end on a held picture. See "Endings, when the picture outruns the track" |
| Exit `3`, `input_moderation_failed` partway through a chain | A carried frame contains a photoreal person — refused at submission, nothing billed, but the chain stops there | Segments before it are kept. Change the subject, go non-photoreal, or keep faces out of the closing frames. See "Performers" |
| Exit `3`, `output_moderation_failed` mentioning audio copyright | The prompt asked for music | Rewrite `SOUND` as ambience only, keep the music words in `AVOID`, and set `--generate-audio false`. Not billed; a re-run is a new request |
| A music bed on the segments nobody asked for | `--generate-audio` left at the server default (`true`) | Harmless — the mux replaces it — but it is wasted risk. Set `false` next time |
| The joined file has no audio stream at all before the mux | Expected with `--generate-audio false`: the stream is removed, not muted | Nothing to fix. `mux-audio` supplies the audio |
| `mux-audio` is rejected as an unknown subcommand | `ofox-video-core` is older than 1.25.0 | Update the core skill. The segments are unaffected and the mux costs nothing, so nothing is lost but the wait — and this is checkable before spending, see "the availability check" |
| The estimate is several times the segment count, or `SHOTS_REQUESTED` is bigger than the number of segments planned | Almost always `--shots-file`: one prompt per line, so each line of a templated prompt became its own billed job | Rebuild with one `--shot` per segment and re-run the dry run. Free to catch, and only at the dry run — after a yes it is a real bill. See "Step 4" |
| The segments do not look like one piece | The consistency lock was rephrased between segments, or the subject drifted | Copy the `STYLE` / `SUBJECT` / `CONSISTENCY` blocks verbatim. Re-generating one segment mid-chain also re-generates everything after it, since each one feeds the next |
| Invented lyrics or captions on screen | Text rendered from a description is the classic failure; a negative list alone does not hold on a lettered set | Keep the text items in `AVOID` **and** keep lettered surfaces out of the set. Lyrics go on in an editor |
| The segments would not join | Their codecs differed, or `ffmpeg` is missing | The script re-encodes once and says so; a failed join is a `NOTE:`, never a lost segment — the clips are all listed and playable. Join them in an editor |
| Exit `4`, timed out waiting | The current segment is still running upstream, not failed | `poll JOB_ID` with the id printed before the timeout. Never re-run `chain` |
| Exit `5`, ambiguous network failure on create | No HTTP response at all — can't tell whether a job exists | Don't guess or retry; tell the user to check https://app.ofox.ai |

## When NOT to use

- **There is no particular audio file.** "Make something with music" is a
  scenario skill plus an editor, and it will be cheaper. The mux is the reason
  this skill exists.
- **Beat-frame-accurate cutting is the requirement.** Say so plainly, before
  anyone pays: this path does not deliver it. Generate longer continuous
  material and cut it in an editor, where a frame is a frame.
- **Cheap vertical drafts to choose between** — [`shorts-reels`](../shorts-reels/SKILL.md)
  owns that ladder. The two compose: draft the look there, run the piece here.
- **A brand or product film that happens to have a bed under it** —
  [`seedance-ad-creative`](../seedance-ad-creative/SKILL.md). The beat
  structure of an ad is its own craft, and its music is laid on afterwards
  too.
- **A live-action performer has to be the same person across the piece.** The
  carried frame is refused at submission when it holds a photoreal person on
  this model. See "Performers" for the four things that do work.
- **Lyrics have to be legible on screen.** Not available from a description.
  Offer the editor route before quoting.
- **A single 30-second clip is the whole ask** and there is no track to lay
  on. Then it is one `generate` call in whichever scenario skill owns the
  look, and this skill's arithmetic and mux buy nothing.
