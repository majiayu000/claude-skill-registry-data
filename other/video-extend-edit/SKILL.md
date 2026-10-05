---
name: video-extend-edit
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai, plus a video you already have. Makes an existing clip longer, or replaces its ending. Use when a user wants more of footage they already have, e.g. "extend this 5-second clip to 15", "keep going from where this one ends", "re-shoot the ending from 4 seconds on", or "add another shot onto this". A frame is pulled out of the clip at zero cost and becomes the first frame of a newly generated segment, which is then joined onto the original. Do not use to change what is inside the picture — measured, the API accepts an edit mode field and silently ignores it, so no content-editing route exists here and none returns an error either; for two stills you already have see keyframe-animation, and for a clip from nothing see the seedance-* scenarios.
license: MIT
version: "2.0.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/video-extend-edit
metadata:
  author: ofoxai
  version: "2.0.0"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq, ffmpeg]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "⏩"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/video-extend-edit
---

# video-extend-edit: carry an existing clip forward from one of its own frames

The user has footage. They want it longer, or they want a different ending.
The mechanism is always the same and it is always a **frame**: pull one out of
their clip locally for nothing, hand it to a new video job as its first frame,
and join the result onto the original.

```
their clip ──> last-frame  ──┐
           └─> frame-at N ───┴─> that PNG as --frame-first-image ──> new segment ──> join
```

Both extractions are local: no API call, no key, no cost. The only billable
step is the new segment.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns which frame to take,
what the new segment will and will not inherit, the join, and the pre-flight
check that keeps a doomed job from being submitted; `ofox-video-core` owns
talking to the Ofox API correctly and safely (the `OFOX_API_KEY` handling, the
no-resubmit rule, error-code mapping, download/verification, and reporting the
downloaded file's absolute `VIDEO_PATH`). **Read that skill's safety contract
before using this one** — it is not restated here.

The shared prompt craft is in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md),
the pre-prompt question rules in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md),
and the spend rule in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).
This file carries only what is specific to continuing footage that already
exists.

## Read this before planning anything

**Re-shooting from second N regenerates everything after N.** There is no
mechanism here for changing the middle of a clip and keeping the ending you
already have. What you can do is keep everything up to second N and replace
the rest; what you cannot do is keep second 0–3, change 3–5, and keep the
ending that used to run 5–10. If a user asks for the middle, the honest answer
is that this route re-shoots the tail, and the old tail is gone.

**And nothing here edits the picture.** The new segment is generated from a
frame and a prompt. Removing an object from footage, swapping a background, or
changing what a clip shows are not things this skill does — see "When NOT to
use".

**Why this skill takes the long way round, and why that is now measured.**
The public Seedance gallery contains prompts run in an `extend` mode and an
`edit` mode, set with a `mode` field on the create request. Until 2026-09-16
this file's position — the frame route is the only way to lengthen a clip —
rested on the **inference** that Ofox does not expose them. It now rests on a
run, and the run says something sharper than "unsupported":

> `mode` is **accepted and discarded**. Job
> `4686f434-16b0-451f-8941-970e5b3d4a15` sent an invented value
> (`this_is_not_a_real_mode_xyz`) inside an otherwise ordinary text-to-video
> request. It returned `200`, completed as a plain 4-second t2v clip, and
> billed $0.44 at the ordinary t2v rate. A value that cannot be implemented
> anywhere cannot have been honoured, so the field was dropped.

Two consequences for how you talk about it:

- **There is no error to catch and none to show the user.** Anyone who
  believes extend is "rejected" will go looking for a 400 that never arrives,
  and a `200` on a `mode` request means nothing at all. Say "the field has no
  effect", not "the API refuses it".
- **The route in this file does not change.** Frame out, generate, join is
  still the only way to make a clip longer here. What changed is that the
  reason is a measurement instead of a guess. `duration: -1` — the form the
  gallery's official edit case uses to lock the output to the input's length —
  returns `502 route_error`, which is the one place something does fail
  loudly, and it fails at routing rather than validation.

Evidence and the free probes that could *not* settle this on their own:
[`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)
→ "`mode` is accepted and has no effect".

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

`check` covers `curl`, `jq` and `OFOX_API_KEY`. **It does not check
`ffmpeg`, and this skill cannot run a single step without it** — the frame
extraction, the join and the verification are all ffmpeg. Check it yourself:

```bash
command -v ffmpeg >/dev/null && echo "ffmpeg ok" || echo "ffmpeg MISSING"
```

Missing → `brew install ffmpeg` (macOS), `sudo apt-get install ffmpeg`
(Debian/Ubuntu). Find that out now rather than after a segment is paid for.
The extraction commands check for it themselves and fail before doing
anything, which is the same discipline `chain` uses so a missing dependency
never costs a paid shot — but knowing at the start beats knowing at step three.

A failing `check` is not a stop sign for the conversation: `models`,
`providers` and `generate --dry-run` all run with no key, so the frame can be
pulled and the job priced before the user has signed up. See "Pricing a job
with no API key".

## What this skill rests on

One paid run of the single-segment route, a two-shot `chain` run seeded from a
frame (2026-09-16 — see "Several segments" below), the `mode` probe that
settled why the frame route is the only route (2026-09-16 — "Read this before
planning anything"), two zero-cost readings of clips that already existed, and
a local reproduction of the join hazard. Where something was not measured,
this file says so rather than reasoning past it.

**Job `35b6aed1` (2026-09-15)**, `bytedance/seedance-2.5` via `byteplus`, 4
seconds, 480p, `adaptive` (forced by the API for image-to-video on this
model), seed `757512526`, **44 cents billed against a 44-cent estimate**.

The input was deliberately built to be hostile in exactly one way. The source
was a 854x480 clip with **no people in it**; `frame-at --at 6.5` took a frame
out of it, and that frame was then resized to **720x480 — a 3:2 shape, which
is not in this model's aspect-ratio list at all**. Everything else was held
constant, so the run tests the frame's shape and nothing else.

### 1. A frame whose shape is not in the catalog is accepted

No `input_moderation_failed`, no aspect-ratio rejection, no 400 of any kind.
The job ran and delivered normally.

**So do not tell a user their clip has to be 16:9.** It does not. Phone
footage, a crop someone made in an editor, an odd export from another tool —
the shape of the frame was not what stopped anything here.

### 2. The new segment's pixel dimensions never come from your clip

Five observations: three paid, two read for free off clips this repo already
had.

| Frame fed in | Its ratio | Tier paid for | Delivered segment | Its ratio |
|---|---|---|---|---|
| 1792x1008 | 16:9, in the catalog | 720p | **1280x720** | 16:9 |
| 1792x1008 | 16:9, in the catalog | 720p | **1280x720** | 16:9 |
| 720x480 | 3:2, **not** in the catalog | 480p | **794x530** | 1.4981 |
| 720x480 — *the same file, a later job* | 3:2, **not** in the catalog | 480p | **794x530** | 1.4981 |
| 794x530 — shot 1's closing frame | 1.4981 | 480p | **794x530** | 1.4981 |

(The first two are `jacket-haul-on-camera-e378f058` and
`kelvin-flask-luxury-ad-cb6b7870`; the third is the paid run above; the last
two are the chain run in "Several segments" below, jobs `69bc799d` and
`2a3ebe06`.)

**All five keep the ratio, and none takes its pixel size from a source clip.**
A catalog ratio lands on that tier's standard size. A non-catalog ratio lands
on a non-standard one, close to the frame's ratio but not exactly it — 1.4981
against 3:2's 1.5, and both figures even, which looks like rounding to even
numbers. The last row only *looks* like the size came from the frame: that
frame was itself a delivered segment, so it already carried the size this
ratio lands on at this tier.

⚠️ **The size mapping is reproducible even though the picture is not.** The
same 720x480 frame went in twice, in two independent jobs, and came back
794x530 both times — while this repo's standing finding is that a fixed seed
does **not** reproduce a clip. Both are true and neither weakens the other:
what is unpredictable is the **content**; what is stable is the
**dimensions**. Don't let a reader of either sentence take it as licence to
doubt the other.

The rule worth carrying, and the only one these five observations support:

> **The delivered segment's dimensions come from the resolution tier you paid
> for and the frame's aspect ratio. They never come from your source clip.**

⚠️ **There is deliberately no formula here for a non-catalog ratio.** Two
observations of the *same* ratio still cannot support one — an arithmetic story
can be told about 794x530 that fits both and has nothing else behind it. What
repeating it establishes is that the mapping is stable for that ratio, not that
it is derivable for another. Measure the delivered file rather than predicting
it:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
  -of csv=p=0 <the new segment>
```

### 3. Which is why joining needs a rescale — and why skipping it is silent

This is the sharpest thing in this file, because the failure does not look
like a failure.

Your original clip and the new segment are two different pixel sizes, by
finding 2, essentially always. Concatenating them without doing anything about
that **does not error**:

```bash
# reproduced locally, at zero cost, on the measured pair of sizes
ffmpeg -f concat -safe 0 -i join.txt -c copy -y joined.mp4   # exit 0, no warning
```

What comes out is a **variable-resolution mp4**. The container header
advertises only the first segment's size, and the decoder quietly
re-initialises partway through. Measured on the joined file: the header says
**854x480**, and the frame at 4 seconds — inside the second part — is really
**794x530**. Players each do their own thing with that; some letterbox, some
stretch, some stutter at the seam.

**Not erroring is worse than erroring**, because an error gets found and this
does not. The user ships it.

The working shape: normalise every part to the source clip's dimensions
first, then join. This was run end to end on parts that differed in size
(794x530 against 854x480), in frame rate (30 against 24) and in whether they
carried an audio stream at all:

```bash
SRC=/absolute/path/to/their-clip.mp4
SEG=/absolute/path/to/the-new-segment.mp4
OUT=/absolute/path/to/out

read W H < <(ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height -of csv=p=0 "$SRC" | tr ',' ' ')
FPS=$(ffprobe -v error -select_streams v:0 \
  -show_entries stream=r_frame_rate -of csv=p=0 "$SRC")

i=0; : > "$OUT/join.txt"
for f in "$SRC" "$SEG"; do
  i=$((i+1))
  ffmpeg -loglevel error -i "$f" -an \
    -vf "scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=${FPS}" \
    -c:v libx264 -pix_fmt yuv420p -y "$OUT/part${i}.mp4"
  printf "file '%s'\n" "$OUT/part${i}.mp4" >> "$OUT/join.txt"
done

ffmpeg -loglevel error -f concat -safe 0 -i "$OUT/join.txt" -c copy \
  -y "$OUT/joined.mp4"
```

Then **verify it, because that is the only thing that catches the silent
case** — probe the frame at several timestamps, at least one on each side of
the seam, and confirm they all report the same size:

```bash
for t in 1 <just before the seam> <just after the seam> <near the end>; do
  ffmpeg -loglevel error -ss $t -i "$OUT/joined.mp4" -frames:v 1 -y /tmp/p.png \
    && printf "t=%ss -> " "$t" \
    && ffprobe -v error -show_entries stream=width,height -of csv=p=0 /tmp/p.png
done
```

Three notes on that recipe, all of which came out of running it:

- **`-an` drops audio from *both* parts, so what this recipe produces is a
  silent file.** That is deliberate — a join across "has a track" and "has no
  audio stream" is its own hazard — but a silent file is not the deliverable,
  and following the recipe and stopping is how a user ends up with fifteen
  seconds of video whose last nine are silent. The audio is a decision you
  have to make out loud: see "The audio hand-off", which is its own section below.
- **The pad is a safety net, not the usual case.** Because the frame came out
  of their own clip, it carries their clip's ratio, so the new segment's ratio
  matches and the scale is a clean resize. The pad only shows as bars if
  someone resized the frame to a different shape before feeding it — which is
  exactly what the measured run did on purpose. If you would rather fill the
  frame than letterbox it, swap `force_original_aspect_ratio=decrease` +
  `pad` for `=increase` + `crop=${W}:${H}`, and accept that it cuts edges.
- **Both parts get re-encoded.** That costs the original one generation of
  quality. It is the price of a file that is one size all the way through, and
  it is cheaper than shipping one that is not.

⚠️ **`chain`'s own concat does not cover this.** It tries a stream copy and
re-encodes only when the shots' **codecs** differ — it never rescales. That is
fine for a chain, whose shots all come back the same size as each other —
measured on 2026-09-16, where both shots of a two-shot chain were 794x530 and
the join needed no rescaling at all — and it is **not** enough for "their clip
plus a new segment", which is this skill's whole case and the one place the
sizes genuinely differ. A joined file from `chain` still has to be joined to
the user's original by the recipe above.

### 4. The result continues the scene — it does not merely reproduce the frame

The delivered segment opens on very nearly the frame it was fed: bottle
position and scale, the shape of the water, the light direction and the
background falloff all carried across. That much was already known from
`chain`; what this run adds is that it holds for a frame that **did not come
from this API**.

And this run separates the two readings that an earlier video-to-video attempt
could not. That one used a motionless cup, so "continued the scene" and "a
style reference redrew a static picture" would look identical. Here the
closing frame shows the bottle **smaller in frame** — the camera really did
pull back, as the prompt asked — and **concentric ripples that are not in the
source clip at all**, which the prompt also asked for. Both are new content
the fed frame did not contain.

**So the promise is continuity of the same set and the same subject**, carried
on from that frame and then following your prompt. It is **not** "keeps the
style" — nothing measured here supports a claim about style, and the phrase
invites a user to expect their grade, their grain and their look to survive.

## The audio hand-off: three options, and silence is what you get by default

The join recipe in finding 3 strips audio from both parts. **So the default
outcome of following this file literally is a video whose generated tail plays
in silence**, and in this skill's own scenario — somebody extending their own
footage — that is almost never what they asked for.

The commands below continue that recipe and reuse its variables: `$SRC` is the
user's clip, `$SEG` the new segment, `$OUT` the output directory, and
`$W`/`$H`/`$FPS` the source clip's dimensions and frame rate as the recipe
read them.

There are three honest endings. **Which one sounds best is craft, not a
finding — nothing here has measured it.** What *is* measured is the trap in
option A, and it is expensive.

| Option | What the user gets | Say this to them |
|---|---|---|
| **A. Their own clip's track, padded** | Their original audio over the original seconds, silence under the generated ones | The added seconds have no sound of their own. The generated part is silent unless they score it |
| **B. Keep the model's track on the new segment** | Their audio, then the model's invented audio, meeting at a hard cut | Two unrelated soundtracks butted together. Get their agreement *before* generating, because it needs `--generate-audio true` on the paid job |
| **C. Deliberately silent** | No audio stream at all | Fine when the clip is going into an editor or onto a muted feed — but say it, don't let them discover it |

Option A comes up most, so its command is written out. `track.m4a` in this
skill comes from **their own clip**; nothing supplies it otherwise:

```bash
# 1. lift the source clip's audio (local, free)
ffmpeg -loglevel error -i "$SRC" -vn -c:a aac -b:a 192k -y "$OUT/source-audio.m4a"

# 2. pad it with silence out to the joined file's length, and fade the tail
VDUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/joined.mp4")
SDUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/source-audio.m4a")
ffmpeg -loglevel error -i "$OUT/source-audio.m4a" \
  -af "apad,afade=t=out:st=$(awk -v s="$SDUR" 'BEGIN{printf "%.2f", (s>1? s-1 : 0)}'):d=1" \
  -t "$VDUR" -c:a aac -b:a 192k -y "$OUT/track.m4a"

# 3. now the mux is safe
bash ../ofox-video-core/references/ofox-video.sh mux-audio \
  "$OUT/joined.mp4" "$OUT/track.m4a" --out-dir "$OUT"
```

⚠️ **Step 2 is not optional, and skipping it destroys the thing you paid
for.** `mux-audio` runs to the **shorter** of its two inputs. Hand it the
source clip's unpadded track — five seconds of audio against a fifteen-second
joined picture — and the result is a **five-second** video: the generated
segment is gone, silently, from the deliverable. Reproduced locally at zero
cost on a 14-second joined file and a 5-second track; the output measured
5.0 seconds. The script does print
`NOTE: the picture is 14.0s and the audio is 5.0s … the picture is truncated
by 9.0s` — **read that note and act on it rather than relaying it as
colour.** With the padding in place the note does not appear at all, which is
the check that it worked.

The fade is craft, not a finding: a track that stops dead where the original
footage ended draws attention to the seam, and a one-second fade is the boring
fix. Shorten it, drop it, or loop a room-tone bed under the tail instead —
those are all reasonable and none of them is measured here.

**Option B changes the join, not just the ending**, so decide it before the
cost table: the segment needs `--generate-audio true`, which means dropping
the `--generate-audio false` default below, and both parts then need an audio
stream that survives the concat. Replace the `-an` loop with this one, which
was also run end to end locally — it re-encodes audio to one codec and layout,
and synthesises silence for any part that has no audio stream at all:

```bash
i=0; : > "$OUT/join.txt"
for f in "$SRC" "$SEG"; do
  i=$((i+1))
  VF="scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=${FPS}"
  if ffprobe -v error -select_streams a:0 -show_entries stream=index -of csv=p=0 "$f" | grep -q .; then
    ffmpeg -loglevel error -i "$f" -map 0:v:0 -map 0:a:0 -vf "$VF" \
      -c:v libx264 -pix_fmt yuv420p -c:a aac -ar 48000 -ac 2 -b:a 192k -y "$OUT/part${i}.mp4"
  else
    ffmpeg -loglevel error -i "$f" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
      -map 0:v:0 -map 1:a:0 -shortest -vf "$VF" \
      -c:v libx264 -pix_fmt yuv420p -c:a aac -ar 48000 -ac 2 -b:a 192k -y "$OUT/part${i}.mp4"
  fi
  printf "file '%s'\n" "$OUT/part${i}.mp4" >> "$OUT/join.txt"
done
```

Note what option B costs beyond the cut: the model's track has been measured
failing output moderation when a prompt asked for music, and `chain` stops the
whole run when that happens. Ambience is the safer ask.

**Whichever you pick, say which one you picked in the hand-over**, next to the
joined path. "The last nine seconds are silent" is a sentence the user should
read from you, not discover on playback.

## The three routes

All three use the same mechanism. Pick by what the user asked for.

### Extend: keep everything, add to the end

```bash
bash ../ofox-video-core/references/ofox-video.sh last-frame /absolute/path/to/their-clip.mp4 \
  --out-dir /absolute/path/to/out
# -> LAST_FRAME /absolute/path/to/out/their-clip-lastframe.png
```

`last-frame` steps back slightly from the true final frame, because the
literal last frame is often a fade. Feed the PNG it prints as
`--frame-first-image`, then join with the recipe above.

### Replace the ending: keep up to second N, re-shoot the rest

```bash
bash ../ofox-video-core/references/ofox-video.sh frame-at /absolute/path/to/their-clip.mp4 \
  --at 4.0 --out-dir /absolute/path/to/out
# -> FRAME_AT /absolute/path/to/out/their-clip-frame-4p0s.png
```

`--at` is required rather than defaulted, deliberately: this frame is about to
be fed to a paid job, and a guessed timestamp is a job billed for the wrong
picture. A timestamp at or past the end is an error naming the clip's real
duration, not an empty file.

Then **trim the original to that same point** before joining, or you will
paste the new tail onto the old one instead of replacing it:

```bash
ffmpeg -loglevel error -i /absolute/path/to/their-clip.mp4 -t 4.0 -c copy \
  -y /absolute/path/to/out/head.mp4
```

`-c copy` trims to the nearest keyframe, so the cut can land slightly off the
requested second. If the exact frame matters, re-encode the head instead
(drop `-c copy`). Join `head.mp4` and the new segment with the recipe above.

### Several segments: `chain`, seeded from their frame

`chain` generates N shots where each opens on the previous shot's closing
frame. Its first shot is normally text-to-video with no frame — but
`--frame-first-image` is passed through to it, so the whole sequence can start
from the user's own footage in one command:

```bash
bash ../ofox-video-core/references/ofox-video.sh chain --approved \
  --frame-first-image /absolute/path/to/out/their-clip-lastframe.png \
  --shot "<what happens next>" \
  --shot "<and then this>" \
  --duration 4 --resolution 480p \
  --name "<what the sequence is>" \
  --out-dir /absolute/path/to/out
```

That is a real run, which is why it carries `--approved` — see "Before you
spend". Swap it for `--dry-run` to price the whole sequence first; `chain`
commits every segment in one command, so the quote is the only place it can
still be stopped. The frame extraction and the join are local ffmpeg, free and
ungated.

**What is verified about that, exactly.** Two things, worth keeping apart:
how the flags route, read out of the script, and what a paid run of the whole
command actually delivered.

The routing is readable in
`ofox-video-core`'s own script and was checked there rather than inferred:
`cmd_chain` collects every flag it does not handle itself into a `passthrough`
array and hands that array to `cmd_generate` for **every** shot, so shot 1
really does receive `--frame-first-image <your PNG>` and is genuinely
image-to-video from your footage. On shots 2+ the flag is therefore present
twice — once from `passthrough`, and once appended afterwards by `cmd_chain`
as the carry-forward — and `cmd_generate` parses it as a plain overwrite, so
**the later one wins and shots 2+ open on the previous shot's closing frame**,
which is what they should do. (That last-wins parse was also confirmed by
running a dry run with two different frames passed and reading which one
reached the payload — no network call, no cost. The script relies on the same
behaviour for `--name`, and says so in a comment beside the carry-forward.)

**And the composed command has now been run end to end.** 2026-09-16, two
shots of 4 seconds at 480p seeded from a frame pulled out of an existing clip:
`STATUS chain_completed`, both shots delivered, **88 cents billed across the
two**, matching the estimate the dry run printed for the sequence.

- **Shot 1 really did open on the supplied frame** (job `69bc799d`) — bottle
  position and scale, the gold cap, the shape of the water and the background
  all match the PNG that was fed in. That is the runtime confirmation of what
  the argument handling above had only predicted.
- **Shot 2 opened on shot 1's closing frame** (job `2a3ebe06`) — the
  concentric ripples shot 1 generated, the dark slab edge at the lower left,
  the position and the light direction all carried across, with the slight
  brightness difference at the seam that `ofox-video-core` already records.

So both halves of the routing are measured rather than read off the script.
Running one `generate` per segment and handing each segment's `last-frame` to
the next yourself is still the same mechanism with the same bill — it is now a
matter of preference, not of staying on measured ground.

⚠️ **What that run does not hand you is a finished join.** The two shots came
back the same size *as each other*, which is why `chain`'s own concat managed
without rescaling anything. The user's source clip is not in that set. So
`chain`'s own `JOINED` output still has to be joined to the original by the
recipe in finding 3, and that is where the sizes really do differ.

## Before you spend: look at the frame

**After extracting, before pricing anything, open the PNG and look at it.**
This is a step, not a formality, and it is the cheapest one in the flow.

**Is there a real person in it?** `bytedance/seedance-2.5` refuses a reference
frame containing a photoreal person at submission —
`HTTP 400 / input_moderation_failed`, "may contain real person". Nothing is
generated and **nothing is billed**, but the default route stops there.

Since 2026-09-16 that is **half-answered rather than a dead end**, and the two
halves have to be kept apart, because only one of them is measured:

- **Measured: `--real-person true` lifts the refusal on
  `bytedance/seedance-2.5`.** Same portrait, same prompt, same parameters, same
  upstream, with and without the flag — with it the job completed, without it
  the identical submission was refused. The flag is Ofox's privacy-preserving
  preprocessing path for real-person references the user is **authorised** to
  use: **an authorisation route, not a way past the check.** Offer it only when
  the user holds the right to use that person's likeness, say so in the same
  breath, and never describe it as a retry for a rejection. The evidence and
  every limit on it are in
  [`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)
  → "`--real-person true` lifts that refusal on 2.5".
- **Not measured — and it is this skill's own case.** The portrait in that run
  was a **synthetic still generated for the test**. A frame lifted out of
  footage is a real person's likeness in a picture nobody posed for, and no
  such frame has been sent, with or without the flag. Whether the preprocessing
  leaves the person recognisable enough for the segment to match the footage it
  joins is unmeasured too.

So **do not tell a user they can now extend footage of people.** What they can
be told is that there is a route worth pricing as an experiment when the
footage is theirs to use, and that its one measurement is a posed synthetic
face rather than anything out of a clip.

The rest of the fallbacks, because the gap here is easy to overstate:

- `alibaba/wan-3.0-prime` and `minimax/hailuo-3` were measured accepting a
  real person's **portrait image**. That is a posed still, not a frame lifted
  out of footage.
- **Neither model's image-to-video behaviour has been measured in this repo at
  all**, and neither has `chain` on them. Offering one is offering an
  experiment; price it as one and say which part is untested.
- The measured run behind this skill used a product clip with **no people in
  it**, on purpose, to isolate the frame-shape question. It therefore says
  nothing about real-person footage, in either direction.

**Read the PNG before you write the ACTION line — every object in it, and the
state each one is already in.** This one is measured. In job
`565e3193-68d7-4223-bb15-337723e89836` the ACTION asked a hard case lid to
close onto its base. In the attached frame that case was **already closed**,
so the instruction had no starting state: nothing closed, nothing moved, and
there was no error, no warning, and nothing in the returned metadata to say a
clause had been dropped. The other half of the same ACTION line — a folded
cloth drawn out of frame to the right — landed in the same job, and was
confirmed to be a real translation rather than the push-in cropping it out.
The difference was not the wording. One object was in a state its action could
start from and the other was not.

The failure mode is specific to this route and worth naming: you are writing
from the scene in your head, which includes the twelve seconds the viewer just
watched. **The model sees one still.** A lid that closed at second 9 of the
source is, at the anchor frame, simply a closed lid. So walk the frame object
by object and ask of each verb you are about to write: can this start from
what is actually in the picture?

Two other things worth a look while the PNG is open, both free to fix and
neither of them measured — they are craft, not findings: whether the frame
lands mid-motion (a blurred frame is a blurry opening second — step a little
earlier), and whether it carries legible text you are about to ask the model
to keep drawing.

## The prompt

The prompt describes **what happens next**, starting from a picture the model
can already see. It does not need to re-establish the set, and re-describing
it in different words is how the set changes.

Vocabulary, the vendor's formula, timestamp rules and the negative-list craft
are in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md)
and are not repeated here. Two of its findings bear directly on this route: a
camera move written only as a verb tends not to happen, so write the frames it
passes through; and negative clauses are honoured more reliably than positive
ones.

⚠️ That second finding is about the **AVOID list** — prohibitions on things
entering the frame. Do not carry it over to a clause inside `CAMERA` that
describes a *framing state*. Measured on this route, one `CAMERA` sentence in
job `565e3193` produced three different outcomes at once:

| Clause | Outcome |
|---|---|
| "a wide shot holding all three objects with margin on every side" | landed |
| "the case is cropped at the right edge" | landed |
| "a close shot on the left lens rim and the hinge, the tortoiseshell grain legible" | landed — though the hinge is peripheral in the delivered frames, not a co-subject |
| "the glasses fill about two thirds of the frame width" | **short.** Measured 52% of frame width at the 6s mark, and the pair was itself cropped at the left edge, so at most about 58% counting the part off-frame |
| "from 8s the case is no longer in frame" | **did not land at all.** The case sat at the right edge for the whole segment |

Two things to take from that, both n=1 and neither a rule:

- **A quantified framing instruction is the same species as a count.** This
  repo has already measured counts as uncontrollable while every quality in the
  same sentence holds — case 1011 asked for three hinge knuckles and got four,
  with the barrel shape and the two materials all correct. "Two thirds of the
  frame width" behaved the same way: right direction, wrong amount. Write the
  size you want as a relation to something visible ("the frame front reaches
  from edge to edge with the temple tips just cropped") rather than as a
  fraction, and expect to check it rather than trust it.
- **A negative framing state was the one clause that did nothing at all.** When
  you need something out of frame, the positive form ("the frame holds only the
  lens rim and the hinge, with pale grey surface to every edge") is the one with
  evidence behind it on this route.

```
CONTINUES FROM: the attached frame is the last frame of the preceding footage — the same <subject>, the same <set>, the same light. Nothing about the scene resets.
ACTION: <what happens next, as one thing, in physical words — in a state the attached frame can actually start from>.
CAMERA: <the move, written as the pictures it passes through, each with its own shot size> — or "the camera holds where it is" if it should not move.
ENDING: <the state the segment finishes in>.
AVOID: a cut back to an establishing shot; the <subject> changing shape, colour or position between the first frame and the second; a new character or object entering that was not in the frame; subtitles, captions, on-screen text, watermarks.
```

A worked example, continuing a product clip whose last frame is a dark
perfume bottle standing in shallow water:

```
CONTINUES FROM: the attached frame is the last frame of the preceding footage — the same dark glass perfume bottle with a gold cap, standing in the same shallow water, lit from the same direction. Nothing about the scene resets.
ACTION: the shallow water beneath the bottle ripples outward in visible concentric rings.
CAMERA: at 0-1s a medium shot with the whole bottle in frame from cap to base and margin around it; by 3s the camera has drawn back far enough that the bottle occupies about half the height it did, with the water surface reaching the bottom corners of the frame. The gold cap catches a highlight that travels across it as the camera pulls away.
ENDING: the rings reach the edge of the frame and the surface settles.
AVOID: a cut; the bottle changing shape, colour or position; a hand or a person entering the frame; subtitles, captions, on-screen text, watermarks.
```

That is close to the prompt job `35b6aed1` actually ran, and the ripples and
the pull-back are the two things that were confirmed in the delivered frames.

**Check the delivered segment the same way**: open its first frame against the
frame you fed in, and its last frame against what the prompt asked for. Never
take `STATUS completed` as evidence that the continuation is the one you
described.

## Before you spend: the approval gate

**Never submit a paid job until the user has seen a cost table and said yes.**
The rule, the required columns and where the numbers must come from are
written down once for every Ofox skill in this repo:
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).
Follow it rather than improvising.

Numbers come from `--dry-run`, which validates everything and prints the
estimate **without sending a request**:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." \
  --frame-first-image /absolute/path/to/out/their-clip-lastframe.png \
  --duration 4 --resolution 480p \
  --out-dir /absolute/path/to/out
```

Relay the `Estimated cost:` line it prints — never a number of your own — then
wait for a yes, then re-run the identical command with `--dry-run` swapped for
`--approved`. The estimate a *real* run prints comes microseconds before the
request goes out, too late to relay.

`--approved` is where that yes gets typed out. Since `ofox-video-core` 2.0.0
the four billable subcommands — `generate`, `create`, `batch`, `chain` —
refuse to run without it, while `--dry-run` never needs it, so the quote above
is still free and still works with no API key. Be exact about what the flag
does: it records a stance, it cannot prove one. Nothing in a shell script can
observe the conversation you had, and it can be typed without showing anyone a
price. What it changes is that spending without quoting is no longer the
default — it has to be written into the command, where a transcript shows it.
The `chain` command above is the one to be most careful with: it commits every
segment at once. The rule above is still the rule, and it is still yours to
follow.

Two things specific to this scenario:

- **An attached frame does not move the job to the dearer video-to-video
  tier.** Image-to-video bills at the text-to-video rate. The dry run reports
  the tier; take it from there rather than assuming an attached input costs
  more.
- **Several segments is several rows plus a total**, one row per segment, per
  the gate's itemised-batch rule. `chain --dry-run` prints one estimate for the
  whole sequence. Do not quote one segment's price when the user asked for
  three.

The one cost figure this file carries, with the parameters it was measured at
because a figure without them is not a measurement: `bytedance/seedance-2.5`,
4 seconds, 480p, one frame attached, **44 cents billed**, matching its
estimate exactly (job `35b6aed1`). That is not a quote for any other
combination — a longer or higher-resolution segment scales from the dry run,
never from this number. No model ids, prices, resolution tiers or duration
ranges are written down anywhere in this file on purpose; they are catalog
facts, they move, and `ofox-video.sh models` / `providers MODEL` read them
live, free, with no API key.

Afterwards the **actual** bill is `VIDEO_COST` from the finished job. Report
it as money, not as the raw ten-decimal string. An estimate is never a bill.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--frame-first-image` | the PNG from `last-frame` or `frame-at` | the whole mechanism. A local file is also the more reliable input — a valid public image URL has been rejected upstream in this repo while the same file base64-encoded went through |
| `--frame-last-image` | not passed | that is `keyframe-animation`'s job. Here the destination is unknown by construction; you are continuing, not interpolating toward a picture you have |
| `--aspect-ratio` | **not passed, on any model** | with a frame attached, `bytedance/seedance-2.5` forces `adaptive` and overrides anything you passed; other models default to it when you pass nothing. The frame decides the shape. Relay the `NOTE:` the script prints |
| `--model` | not passed — the script's default applies, **unless the user named one**, which always wins | the measured run is on the default model. Another model is an untested route here, not a known-good one; say so before switching rather than after |
| `--duration` | the length the user actually wants added, within the model's range | `ofox-video.sh models` prints each model's range — don't quote one from memory. One job is one clip; a longer total than one job allows is several segments, not a longer job |
| `--resolution` | the tier the rule below picks, or the cheapest tier for a draft | the segment is going to sit next to their footage, so a tier far above or below it shows at the seam. "Their clip's own tier" is not by itself something you can execute — see "Which tier is the source clip's tier" right after this table. Draft cheap, then re-render, and put both as rows in the cost table |
| `--generate-audio` | `false` unless the user has chosen option B | the new segment's audio is model-generated and has nothing to do with your clip's audio; joining the two is a hard cut between unrelated soundtracks. `false` removes the stream entirely rather than muting it. **This flag is the audio decision, and it is made before the paid job** — see "The audio hand-off", where option B is the only one needing `true` |
| `--seed` | let the script roll one, and keep it | it prints `SEED` and writes it to the sidecar, which is what lets a segment be described and re-attempted at all. It does **not** reproduce it: measured, an identical request on a fixed seed came back a visibly different clip. Tell the user a re-render is another roll aimed at the same segment before they pay for it |
| `--name` | always | the segment lands as `<name>-<short job id>.mp4` with a matching `.json` sidecar, which is what makes a two-part out-dir readable later |
| `--out-dir` | always, absolute | see "Where the files land" |

### Which tier is "the source clip's tier"

A source clip is a `WIDTHxHEIGHT`; a tier is one number with a `p` on it. Going
from one to the other is a decision somebody has to make, and "match the
source" does not make it — a 1080x1920 phone clip has 1080 on one axis and
1920 on the other, and reading the wrong one picks a different tier and a
different bill.

**Be honest first: nothing here measures which tier "matches" a source best.**
What is measured is finding 2 — the delivered segment's size comes from the
tier you paid for and the frame's ratio, never from your clip — and the join
rescales everything to the source's dimensions regardless. So this choice does
not decide the finished file's size at all. It decides **how much detail
exists to be scaled** at the seam, and how much the segment costs. That is
what makes a convention adequate here where a measurement would be needed for
a promise.

The convention, and it is decidable:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
  -of csv=p=0 "$SRC"          # -> e.g. 1080,1920
```

1. Take the **short side** — the smaller of the two numbers. Tier names have
   always counted the short side, on landscape and vertical alike; a
   1080x1920 phone clip and a 1920x1080 landscape one are both "1080".
2. Read the tiers the chosen model actually offers — live, free, no key:
   `bash ../ofox-video-core/references/ofox-video.sh models`.
3. Pick the **highest offered tier whose number is at or below the short
   side**. If the short side is below every tier the model offers, take the
   lowest one and expect the segment to be sharper than the footage it joins
   — which the rescale at join time flattens out anyway.

So the phone clip above lands on the highest tier at or below 1080, not on
whatever 1920 would suggest.

Two edges worth knowing rather than guessing at:

- **A tier not written as a pixel height does not map this way.** Some models
  name a tier with a `k` rather than a `p`, and the short-side rule has
  nothing to say about those. On one of those, read the model's own list, pick
  deliberately, and measure the delivered file with `ffprobe` rather than
  predicting it.
- **Dropping one tier is the cheap option and it is legitimate**, because the
  tail is the only part affected and the join rescales it anyway. It shows as
  a softer generated section, most visibly on texture and fine text. Put it in
  the cost table as its own row — the user gets to trade money for the seam,
  and neither answer is wrong.

## Unmeasured edges

Everything here is **no evidence yet**, not "impossible". A later measurement
adds a route to this file; none of it overturns what is above.

**One entry has left this list by being measured.** "Whether Ofox exposes a
native `extend` / `edit` mode" used to sit here. It was run on 2026-09-16 and
the answer is that the `mode` field is accepted and has no effect — see "Read
this before planning anything". That is a closed question, not an open edge,
and it is the reason the frame route is the route.

- **Video-to-video / `input_references` as a way to extend.** The API does
  take a video reference, and it is not this skill's route, for reasons that
  are measured rather than assumed: a single job's duration ceiling is
  unchanged by it, so there is **no mechanism there for extending a clip past
  one job's length**; a video reference must be a publicly reachable URL, with
  no local-file or `data:` form; it bills at the dearer video-to-video tier;
  and the one real run on it could **not** distinguish continuing the scene
  from a style reference redrawing a near-static picture, because the subject
  was motionless. None of that says continuation is impossible there — it says
  nobody has shown it. If it is ever shown, it becomes a second route in this
  file, sitting beside the frame route rather than replacing it.
  **The `image` element of the same field was measured on 2026-09-16** (job
  `0f5c8b4e`, two images, 44 cents) and it works — but it is subject and style
  guidance, not a clip to continue, and the duration ceiling is unchanged by
  it. It adds nothing to this skill's problem.
- **Real-person footage.** Half-answered, and the unanswered half is the one
  this skill needs. `--real-person true` is measured lifting the
  `input_moderation_failed` refusal on `bytedance/seedance-2.5` — for
  references the user is **authorised** to use, which is what that flag is for
  and the only thing it is for. What has never been sent is a frame lifted out
  of **live-action footage of a real person**: the measured input was a
  synthetic portrait posed for the test. Whether the preprocessing leaves that
  person recognisable enough to match the footage the segment joins is
  unmeasured, and so is a frame from footage on any other model. See "Before
  you spend: look at the frame".
- **`alibaba/wan-3.0-prime` and `minimax/hailuo-3` image-to-video.** Both were
  measured accepting a real person's portrait image as an input; **neither has
  had its image-to-video behaviour measured in this repo**, so neither is a
  known fallback for the case above, and continuity across a chain on them is
  untested too.
- **Brightness at the seam.** `ofox-video-core` records a slight brightness
  shift across the seams of its own chains. Whether the same happens between a
  user's source footage and a generated segment has not been measured — expect
  it, look for it, and grade it in an editor if it shows.
- **The join recipe on exotic sources.** It was run across a size change, a
  frame-rate change and mixed audio presence. Variable-frame-rate phone
  footage, rotation metadata, HDR and 10-bit sources were not in that test;
  the verification loop is what tells you, and it is free.
- **Any composed command this file has not run**, named where it appears.
  `chain --frame-first-image` used to head this list and has come off it — it
  was run end to end on 2026-09-16, two shots, and what it leaves unmeasured is
  narrower: a chain of more than two shots from a user's frame, and any chain
  on a model other than the script's default.

## When NOT to use

| The user wants… | Use instead | Why it is not this skill |
|---|---|---|
| Motion between **two stills they already have** — "here is the before and the after" | [`keyframe-animation`](../keyframe-animation/SKILL.md) | it locks both ends in one job. Here the ending is unknown by construction — you have a starting frame and a description, not a destination picture |
| **Two screenshots of one interface**, before and after a state change | [`product-demo`](../product-demo/SKILL.md) | same two-ended mechanism, different measured behaviour and prompt advice |
| To **change what is in the picture** — remove an object, swap a background, replace a face, fix a frame | nothing here | no video content-editing route exists in this repo, and **measured 2026-09-16, none exists in the API either** — the `mode` field an edit would be requested through is accepted and has no effect (job `4686f434`, `200`, billed as ordinary t2v), so nothing fails loudly to tell you. [`image-edit`](../image-edit/SKILL.md) edits a **single still**, not footage. Say that plainly rather than re-shooting the tail and hoping |
| A clip **from nothing** — no footage yet | the `seedance-*` scenarios, [`ugc-ads`](../ugc-ads/SKILL.md), [`shorts-reels`](../shorts-reels/SKILL.md) | this skill's entire input is a clip that already exists |
| A **multi-shot sequence generated from scratch**, no existing footage to continue | `ofox-video-core`'s `chain` directly | that is the core capability. This skill is the wrapper for the case where shot 1 is somebody's existing file |
| A **dialogue scene** continuing a drama clip | [`seedance-short-drama`](../seedance-short-drama/SKILL.md) for the prompt craft, then this skill for the mechanism | the two compose. Write the scene there, extend it here — and if the footage has actors in it the default route stops at the real-person check. "Before you spend: look at the frame" has the authorised route and exactly what it does not cover |
| Their clip **trimmed, sped up, re-cropped or re-encoded** | ffmpeg directly | no generation needed, so no money should move |
| A **longer single job** rather than a join | `generate` with a longer `--duration` | if what they want fits inside one job's ceiling and they have no footage to preserve, one job is cheaper and has no seam |

## Pricing a job with no API key

`models`, `providers` and `generate --dry-run` all work with `OFOX_API_KEY`
unset, and both frame extractions are local. So a user who has not signed up
can have their frame pulled, look at it, and see the job priced before
deciding whether to register. **Quote it first; don't open with a signup
link.**

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

This skill needs a core that has `frame-at` — `last-frame` has been there
longer. A core without it answers `frame-at` as an unknown command; the
extend route still works, and only the replace-the-ending route needs the
newer core.

The same two causes explain a broken link to a shared reference: this skill
packages only its `SKILL.md` and `CHANGELOG.md`, so `prompt-structure.md`,
`creative-brief.md` and `approval-gate.md` are out of reach whenever the
script is. The routes, the join recipe and the defaults are written out here,
so nothing becomes unusable — what is lost is the depth behind the rules they
reference.

## Exit codes worth knowing

Full table in [`../ofox-video-core/SKILL.md`](../ofox-video-core/SKILL.md).
The ones that come up here:

| Code | Meaning | What to do |
|---|---|---|
| `1` | Parameter rejected locally, no network call, nothing billed — a duration outside the model's range, or `--at` past the end of the clip | Fix and retry freely |
| `2` | Environment problem — `curl`/`jq`/`OFOX_API_KEY` missing, or **ffmpeg missing** on an extraction | Install it; the extraction commands check before doing anything |
| `3` | API rejected it, the job ended failed, or a frame could not be extracted from the clip | Read the mapped message. A rejected create was not billed |
| `4` | Timed out waiting — **the job is still running and billable** | `poll JOB_ID`, never re-run `generate` |
| `5` | Ambiguous network failure on create | Do not retry blindly; check https://app.ofox.ai first |
| `6` | `--out-dir` unusable | Fix the path; if it happened after a create, `poll JOB_ID --out-dir <writable dir>` |

## How long to tell the user it will take

`generate` blocks while it polls, up to `--max-wait` (default 540s). A short
low-resolution segment is usually one to three minutes. Say so before starting.

If your tool call can't stay open that long, use `create` (submits and returns
a job id in seconds) then `poll`, instead of `generate`, so a timeout can
never strand a job whose id you never saw.

One transport note from the measured run, because it looks alarming and is
not: a `curl (35) SSL_ERROR_SYSCALL` hit the **poll**, the script retried the
poll rather than the create, and the job completed normally. A dropped
connection while polling is never evidence about the job's state, and never a
reason to submit again.

## Where the files land

Always pass `--out-dir`, and **make it an absolute path**. Without it the
script writes to the current working directory — which, given that the
examples here run from this skill's own directory, would drop the user's video
inside an installed skill. The same applies to the extraction commands: with
no `--out-dir` they write the PNG next to the source clip, which is the user's
own folder and may not be where they want it.

Relay the **absolute** paths the script prints, each on its own line — and in
this skill the deliverable is the **joined** file, not the raw segment. Hand
over the joined path first and say plainly what it contains: how much of it is
their original footage and where the generated part starts.

If you muxed a track on, the deliverable is the `-with-audio.mp4` file that
`mux-audio` printed as `MUXED`, not `joined.mp4` — and say which of the three
endings in "The audio hand-off" you took, because the user cannot hear it from
a path.

Pass the same `--out-dir` to the dry run and the real run: the dry run creates
and enters it, so a bad path exits `6` with nothing submitted.

## Common failure modes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| The joined file plays at one size and then jumps, or a player letterboxes half of it | The parts were concatenated without normalising — the silent variable-resolution case | Re-join with the recipe in finding 3, then run the verification loop. Free to fix; no new job needed |
| The joined file looks fine to `ffprobe` but wrong in a player | `ffprobe` on the container reads the **first** part's header only. That is exactly the trap | Probe extracted frames either side of the seam, not the container |
| Exit `3`, `input_moderation_failed` | A photoreal person is in the extracted frame. Refused at submission, nothing billed | This is what the pre-flight look is for. If the footage is the user's to use and they have said so, `--real-person true` is Ofox's route for **authorised** real-person references and is measured lifting this refusal — on a synthetic portrait, not on a frame out of footage, so price it as an experiment. It is an authorisation route, not a way past the check: do not reach for it as a retry |
| Exit `1`, `--at is past the end` | The timestamp is at or past the clip's duration; the error names the real duration | Pick an earlier second, or use `last-frame` if what you wanted was the ending |
| Exit `1`, `references_conflict` | A frame flag and an `input_references` array in `--extra-json` were passed together | Pick one. This skill's route is the frame; `input_references` is not used here at all |
| The finished file is suddenly as short as the original clip and the generated tail has vanished | The source clip's own audio was muxed on unpadded, and `mux-audio` runs to the **shorter** of its two inputs. Reproduced: a 14s picture and a 5s track gave a 5s file | Pad the track out to the joined file's duration first — "The audio hand-off", step 2. Free to fix: re-mux from `joined.mp4`, no new job. The script's `NOTE:` said this at the time |
| The generated part plays in silence | Expected and by design: the join drops audio from both parts, and nothing replaces it until you choose an ending | Pick one in "The audio hand-off" and tell the user which. Free to fix |
| The new segment is a different size from the source clip | Expected, and measured — dimensions come from the tier and the frame's ratio, never from your clip | Nothing to fix upstream. Normalise at join time |
| The new segment's look drifts from the source — grade, grain, contrast | Continuity is of the set and subject, not of style. Nothing measured supports a style promise | Grade the segment to match in an editor. Don't pay for another roll expecting a different answer |
| The seam is visible as a brightness step | Known between chained shots; unmeasured between user footage and a generated segment | Grade it. Report it honestly rather than describing the join as seamless |
| The generated part re-establishes the scene — a wide shot, a new angle | The prompt re-described the set instead of saying what happens next | Rewrite the prompt against the template above and re-run. New job, new cost table |
| The clip the user wanted preserved got overwritten at second N | The original was never trimmed, so the new tail was appended rather than substituted | Trim the head first — see "Replace the ending". Nothing was lost if their source file is untouched, which is why every command here writes to `--out-dir` |
| Exit `4`, timed out waiting | The job is still running upstream, not failed | `poll JOB_ID` with the id printed before the timeout. Never re-run `generate` |
| Exit `5`, ambiguous network failure on create | No HTTP response at all — can't tell whether a job exists | Don't guess; tell the user to check https://app.ofox.ai |
