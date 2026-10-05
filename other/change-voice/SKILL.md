---
name: change-voice
metadata: {packVersion: 1.3.0}
description: >-
  Replaces the voice in a video or audio file with one from the Novoads voice
  catalog, over the REST API. Converts the SPEECH in the source to a voice you
  pick, keeps the original timing so lip-sync survives, and returns audio that
  gets muxed back over the untouched picture locally. Casts by MEASURING the
  source voice against auditioned candidates instead of reading labels, refuses a
  source with no speech before anything is charged, fences sound effects and music
  so they survive from the original track, and verifies the finished file by
  transcribing it. Use when an actor's voice sounds robotic, flat, thin or simply
  wrong, and for "change the voice", "voice swap", "swap the voice on this ad",
  "re-voice my ad", "the actor's voice sounds bad", "make him sound human",
  "different voice for this video", "speech to speech", "same video better voice".
  Not for narrating a silent clip (that is a voice-over), not translation, and it
  changes neither pronunciation nor accent.
---

# Change Voice

One video in. The same video out, with the speech re-performed by a voice you chose.

The picture never moves. The timing never moves. What changes is who is speaking, and
the entire craft of this skill is in three decisions the endpoint cannot make for you:
**which voice**, **which spans of audio to replace**, and **whether the result is
actually good**. The HTTP call in the middle is one request.

**Every HTTP mechanic here belongs to the pack, not to this skill.** Auth, strict
bodies, status codes, rate limits and error envelopes are written out once in
[`skills/novoads-api/SKILL.md`](../novoads-api/SKILL.md) and its
[`reference.md`](../novoads-api/reference.md). Read those for mechanics; this file
names the endpoint and the fields that matter to a re-voice.

## Before anything: this runs on a Novoads account

- **Base URL:** `https://api.novoads.ai/v1` (host overridable with `NOVOADS_BASE_URL` —
  host only, you append `/v1`).
- **Auth:** `Authorization: Bearer $NOVOADS_API_KEY`, read from `.env` at the repo root.
- **Check:** `./scripts/check-novoads-env.sh`. If it is missing, run `./scripts/setup.sh`.
- **ffmpeg on your machine.** Hard dependency, not optional: the local speech check, the
  casting measurement and the whole assembly are local ffmpeg work. `ffmpeg -version`
  before you start.
- **Never** print API keys, commit `.env`, or paste a key into `MASTER_CONTEXT.md`.

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

A `401` means the key is wrong, revoked, or from another account. A `403` with
`error.details.reason` of `plan_required` or `subscription_inactive` means the key is
fine and the account has no live subscription. Different problems, different fixes — say
which one it is.

No account yet? **<https://novoads.ai/?utm_source=claude-code&utm_medium=github&utm_campaign=skill-pack>**
There is no free tier and no trial: every plan is a paid monthly subscription,
published at novoads.ai/pricing. Never call it free.

**If this deployment does not offer voice changes yet.** The endpoint is behind a flag.
With it off, `POST /v1/voice-changes` and a `kind: "voice-change"` estimate both answer
**`400 invalid_input`** with a message naming what the API does offer, and neither the
path nor the estimate arm appears in `GET /v1/openapi.json`. Read that as "this
deployment cannot do it", say so in one line, and stop. It is not a `404` and it is not
a retry.

## What the endpoint does, and the four things it does not

It takes a source you already have, converts **the speech in it** to the voice you name,
and by default returns **audio**. `200`, not `202` — there is no job to poll. With
`output: "video"` it returns the finished video instead, as a job you poll: see
[Video out](#video-out).

**It preserves timing frame-accurately.** That is the whole reason this exists rather
than a text-to-speech call: the take drops back onto the original picture and the lips
still match. Measured on this skill's acceptance run, across 33 words, the largest
per-word start drift between the source's transcript and the finished output's was
**0.021 seconds**.

**It matches loudness for you.** The converted audio is gained to within 1.5 dB of the
source's own measured mean before it is stored, so the take arrives at the level of the
thing it replaces.

Four things it does not do, each one a real assumption callers arrive with:

| It does not | So |
|---|---|
| **translate** | the words that come back are the words that went in |
| **fix pronunciation, or change an accent** | it reproduces the source's phonemes, mistakes included. A mispronounced brand name comes back mispronounced in a nicer voice. See Gate 3 and the failure modes |
| **detect speech**, on audio out | the gate is "does this have an audio track". A music bed converts into vocal noise, **billed in full**, and answers `200`. Gate 1 is yours and it is free. Video out charges only once its job finds speech (a source with none ends `failed`, or is refused at the request (no job is created) when an earlier attempt already found none; neither is charged), and Gate 1 still runs first; see [Video out](#video-out) |
| **return video, by default** | the default output is audio: muxing the take back over the picture, and choosing which spans to replace, is local work. Deliberately: those are creative decisions. `output: "video"` hands the mux to the server where the workspace has it on — see [Video out](#video-out) |

## The gates run in order. Do not skip to the conversion.

### Gate 1 — is there actually a voice in this file?

Free, local, and it runs **before the upload**, not after.

```bash
python3 skills/change-voice/scripts/check-speech.py <the source file>
```

- **exit 0, `SPEECH`** — proceed. Write down the reported `speech runs A to B`: A is the
  fence the assembly step needs, and the reported pitch is the casting brief's spine.
- **exit 2, `NO-SPEECH`** — **stop, and do not call the endpoint.** Say plainly what it
  is: this file has no talking voice in it, and the endpoint would convert it into vocal
  noise and charge for the minute. If the ask was really a music bed, that is
  `POST /v1/music` and a different skill. If the speech starts later in the file, run
  with `--json`, read `speechStart`, and cut a clip that contains it.
- **exit 3, `UNCLEAR`** — the two measurements disagree. Play the file. Proceeding on
  the optimistic reading is how a charged conversion of nothing happens.

The check reads a whole file, and it has three blind spots worth stating out loud when
they apply: **singing** reads as speech (one singer is one voice); **narration over
a music bed** reads as speech, correctly — but the endpoint will convert the bed too, so
either fence it in assembly or convert a cut where the bed plays alone; and **a sustained
single pitch** (a drone, a synth pad, an organ note) reads as speech, because it is one
periodic thing in the human range. That last one shows in the numbers rather than the exit
code: a reported pitch spread near 0 Hz is a machine, not a person. Read it before you
proceed.

### Gate 2 — price it, announce it, wait

Upload the source, then price it. Both are free.

```bash
# the source: a video, or an audio file. This is the ONE endpoint here that takes
# audio-only uploads (audio/mpeg, audio/wav) as well as video/mp4.
curl -sS -X POST https://api.novoads.ai/v1/uploads -A novoads-skill/change-voice \
  -H "Authorization: Bearer $NOVOADS_API_KEY" -H 'Content-Type: application/json' \
  -d '{"contentType":"video/mp4","sizeBytes":<exact byte count>}'
# → 201 { assetId, uploadUrl, method, headers } — PUT the bytes with `headers` VERBATIM

curl -sS -X POST https://api.novoads.ai/v1/estimates -A novoads-skill/change-voice \
  -H "Authorization: Bearer $NOVOADS_API_KEY" -H 'Content-Type: application/json' \
  -d '{"kind":"voice-change","assetId":"<assetId>"}'
# → { credits, balance, sufficient }

# the conversion is not the only charge in this run. Gate 7 reads the finished file
# back, and reading it against the source needs the source's words too. Price that
# here, on the same assetId, unless you already have the source's own script.
curl -sS -X POST https://api.novoads.ai/v1/estimates -A novoads-skill/change-voice \
  -H "Authorization: Bearer $NOVOADS_API_KEY" -H 'Content-Type: application/json' \
  -d '{"kind":"transcript","assetId":"<assetId>"}'
```

**A source already rendered by this API needs no upload** — pass its `jobId` instead of
`assetId`, in both the estimate and the conversion. At most one of the two, in either
body.

**Name the source in the estimate.** The voice-change price follows the length of the source
audio, by the second above a minimum charge (since API 2.32.0), so a quote with no source is
that minimum and says nothing about a four-minute file. The transcript arm bills per minute of
source, so the same rule applies to it. Never carry a number from here into a message: quote.

**Announce the whole run, not just the conversion.** The conversion is the large charge
and it is not the only one: **the verification in Gate 7 is a charged call too**, and
reading it against the source is a second one unless you already hold the source's script.
Say so in the same line — the conversion at the price quoted above, the source transcript
at the price quoted beside it, and the read-back of the finished file quoted at Gate 7,
because the file it prices does not exist yet. A run that announces one number and spends
three times is a run the operator did not actually approve.

Then proceed. This is an announcement, not a question, with two exceptions:
`sufficient: false` is a blocker — name the shortfall and give the `topUpUrl`; and a
balance that covers this conversion but not a second one is worth one clause, because
**a different voice is a different conversion and a new charge**.

Never state a price from memory, and never estimate one of these calls by reasoning from
another. There are no rate tables in this repo, the estimate charges nothing on every arm, and it
is the only legitimate source of a number.

### Gate 3 — the casting brief

Three inputs, all free, and none of them is the voice catalog yet.

1. **Who is on screen.** Pull two or three frames and look at them.
   ```bash
   ffmpeg -v error -ss 3 -i source.mp4 -frames:v 1 f1.jpg
   ```
   Apparent gender and apparent age are what the catalog filters on. Note them as
   apparent, because that is all a frame supports.
2. **What language, and what register.** The transcript tells you the language and shows
   you the copy. If you have the source's own script, that is enough and this costs
   nothing; otherwise `POST /v1/transcripts` on the same `assetId` reads it back — **a
   charged call**, quoted at Gate 2 and wanted again in Gate 7, so it is one charge and
   not two. Never quote it from memory:
   ```bash
   curl -sS -X POST https://api.novoads.ai/v1/estimates -A novoads-skill/change-voice \
     -H "Authorization: Bearer $NOVOADS_API_KEY" -H 'Content-Type: application/json' \
     -d '{"kind":"transcript","assetId":"<assetId>"}'
   ```
3. **What the current voice measures.** `check-speech.py` already reported it: a median
   pitch and a spread. That number, not an adjective, is what Gate 4 ranks against.

**If the ask is an accent or a pronunciation, stop here and say so.** A voice change
moves timbre and register; it does not re-pronounce anything. Swapping to a voice
labelled `british` gives you a British-sounding instrument saying the source's own
phonemes. The two routes that genuinely answer that ask:

- **Re-render the ad** with a different actor, and spell the awkward word phonetically in
  the new script (`Git-Hub`, `no-vo-ads`). [`clone-video-ad`](../clone-video-ad/SKILL.md)
  is that path when there is a source ad to work from.
- **Lay a fresh `POST /v1/voiceovers` take** over a span with **no lips in frame**. On a
  span where the actor is visible and speaking, a TTS line will not match the mouth and
  the seam is the first thing a viewer sees.

### Gate 4 — audition, then STOP

Read the catalog **filtered**. Unfiltered it is thousands of voices and megabytes of
JSON; on 2026-08-12 `gender=male&language=en` alone returned 5,362 entries and 3.8 MB.

```bash
curl -sS "https://api.novoads.ai/v1/voices?gender=male&age=young&accent=american&language=en" \
  -A novoads-skill/change-voice -H "Authorization: Bearer $NOVOADS_API_KEY" > voices.json
```

`gender` and `age` match whole values (`male`/`female`, `young`/`middle_aged`/`old`);
`accent` is a substring, so `american` also finds `latin american`; `language` matches
the base subtag, so `es` finds `es-CL`. A voice with no labels drops out of a filtered
list **except your own organization's clones**, which come back under every filter and
sort after the matches. `limit` is a cap applied after filtering, not a page — and
because the list is ordered by name, a small `limit` hands you one letter of the
alphabet rather than a sample.

Then measure the candidates against the source and audition them:

```bash
python3 skills/change-voice/scripts/match-voice.py \
  --source source.mp4 --voices voices.json --sample 24 --top 3
```

It downloads each candidate's `previewUrl`, measures its pitch the way it measured the
source's, and ranks by distance in **semitones**. Play the shortlist. Then:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  CASTING GATE — BLOCKING. The human picks the voice.                  ║
║  Never default a voiceId. A voice nobody listened to is a performance ║
║  charged for without being heard.                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

**Why measurement and not the descriptions.** Casting from written labels miscasts, and
it did: on this skill's own reference ad the top pick by description measured a flat
monotone, and the second sat most of an octave above the actor on screen. The labels
narrow the field correctly and say nothing about register, which is exactly what a
viewer hears as "that is not his voice".

**And why the script does not decide.** It has never heard the ad. A preview is a few
seconds of unrelated copy: it carries timbre and register, not the delivery this ad
needs. Under about two semitones from the source reads as the same register, and inside
that band the choice is listening.

### Gate 5 — convert

```bash
curl -sS -X POST https://api.novoads.ai/v1/voice-changes -A novoads-skill/change-voice \
  -H "Authorization: Bearer $NOVOADS_API_KEY" -H 'Content-Type: application/json' \
  -d '{"assetId":"<assetId>","voiceId":"<the one the human picked>"}'
# → 200 { jobId, assetId, url, expiresInSeconds, creditsCharged, billedSeconds, billedMinutes, voiceId }
#   billedSeconds is the probed length the price read; billedMinutes is deprecated (API 2.32.0).
```

Fifteen seconds of source came back in about seven on the acceptance run. **Download
`url` immediately** — it is minted per response and time-limited, and the `assetId` is
the durable handle.

**Write down `jobId` and `creditsCharged` the moment they land.** If the response never
reaches you, do **not** call again: the audio was probably rendered and charged.
`GET /v1/generations?kind=audio` will show it.

**Converting the same source in the same voice again is free** and returns the same
`jobId` and `assetId` with `creditsCharged: 0` and a freshly minted URL. So a retry
after a timeout is not a second charge — verified on the acceptance run, in the response
and in the balance. **A different voice is a different conversion and a new charge**, so
auditioning by conversion is the expensive way to do Gate 4.

**Want the finished video rather than the take?** Add `"output":"video"` to the same
body. It is a job to poll instead of an answer and it needs a video source. The mux
becomes the server's; Gate 6's span choices are not made for you; Gate 7 stays yours.
Read [Video out](#video-out) before sending it.

### Gate 6 — assembly, which is where the ad is won or lost

The endpoint converted **everything it heard**, including the sound effects, the room
tone and any music. Those already exist, correctly, in the original track. So the
finished audio is the original everywhere except the spans where somebody is talking.

```bash
python3 skills/change-voice/scripts/assemble-voice-change.py \
  --source source.mp4 --converted take.mp3 \
  --speech-start <the A from Gate 1> [--speech-end <B>] --out final.mp4
```

It builds one timeline — original head, converted body, original tail — muxes it against
the video stream **copied bit for bit**, and then measures the finished file against the
source. Exit 2 means the file was written and is out of tolerance: read the numbers
rather than shipping it.

Three things it does deliberately, all of which matter:

- **No crossfades at the seams.** `acrossfade` shortens the total by its own duration,
  which slides every later word out from under the lips. The seams get equal-length 20 ms
  fades, which cost no time at all.
- **It states the channel matrix.** The take is mono and an ad's track is usually stereo;
  ffmpeg's default mono-to-stereo rematrix silently costs 3 dB. Measured on the
  acceptance run before it was fixed: a take sitting 0.6 dB under its source came out of
  the mux 3.4 dB under it, with every boundary correct.
- **It re-measures the object it wrote**, not the object it intended to write.

Set the fence at a point where **nobody is talking**. Gate 1's `speechStart` is that
point on a normal ad. Where speech is interleaved with effects, run the assembly per
span, or accept the conversion across an effect and listen to it before shipping.

### Gate 7 — verify by transcribing your own output

> Doctrine: [shared/references/craft.md](../../shared/references/craft.md) § 1. The call
> below is this surface's; the rule is not this skill's.

**This step spends.** It is the last charge in the run and the one most easily mistaken for
housekeeping. Upload the finished file, price the read-back, say the number, then read it.

```bash
# upload the finished file, then price the read-back on ITS assetId — the file did
# not exist at Gate 2, so this is the first moment it can be quoted at all
curl -sS -X POST https://api.novoads.ai/v1/estimates -A novoads-skill/change-voice \
  -H "Authorization: Bearer $NOVOADS_API_KEY" -H 'Content-Type: application/json' \
  -d '{"kind":"transcript","assetId":"<the finished file>"}'

curl -sS -X POST https://api.novoads.ai/v1/transcripts -A novoads-skill/change-voice \
  -H "Authorization: Bearer $NOVOADS_API_KEY" -H 'Content-Type: application/json' \
  -d '{"assetId":"<the finished file>"}' | jq -r '.text'
```

Skipping it to save the charge is not an option on offer: an unread run is not finished,
and the whole point of the gate is that a conversion can drop a word silently. If the
budget only stretches to one read-back, it is this one.

Read it against the source's transcript, word for word. A conversion that dropped or
mangled a word is a failed run, not a note in the report. Timings come back in
**seconds**, so comparing `words[].start` between the two transcripts is also the
cheapest proof that the picture and the new voice still agree.

Then **watch the lip window** — ten seconds of the finished file with the actor's mouth
in frame, at full size. The transcript proves the words survived. Only your eyes prove
the mouth still owns them.

Report the loudness delta the assembly step printed. A number nobody states is a number
nobody checked.

## Video out

`POST /v1/voice-changes` takes an optional `output`: `"audio"`, the default and everything
above, unchanged; or `"video"`, which answers `202 { jobId, status, credits, output: "video" }`.
`status` is the job's current status; retrying the same request is safe and returns the same
job (the same jobId). `queued`: not rendering yet; `running`: already rendering; `succeeded`, with the
finished copy and nothing charged, when the same change was already made. On `queued` or `running`,
poll `GET /v1/generations/{jobId}` until `succeeded` (`outputUrl` is the new mp4) or `failed`
(`voiceChange.reasonCode` names the cause); on `succeeded`, download. The same price as audio
out, from the same `kind: "voice-change"` estimate, but charged differently: audio out at the
request, video out only once the job finds speech in the source (a source with none ends
`failed`, or is refused at the request (no job is created) when an earlier attempt already found none; neither is charged), refunded if the job fails after that. It needs a video source and is
enabled per workspace; both refusals are a `400` with nothing charged. Only the voice
changes. The mux becomes the server's; Gate 6's span choices are not made for you; Gate 7
stays yours.
**Read [references/video-out.md](references/video-out.md) before sending it.**

## The calls

```
POST /v1/uploads        { contentType: "video/mp4" | "audio/mpeg" | "audio/wav" | …,
                          sizeBytes: <exact> }
                        → 201 { assetId, uploadUrl, method, headers } — PUT the bytes
                          with `headers` VERBATIM. Free. The URL expires in 900s; the
                          assetId does not expire.

POST /v1/estimates      { kind: "voice-change" | "transcript", assetId | jobId }
                        Both arms are used here, and both are free. Price the
                        conversion and the read-backs, not just the conversion.
                        → { credits, balance, sufficient, shortBy?, topUpUrl? }
                          Strict. At most one source. No source = the arm's minimum charge.

GET  /v1/voices         ?gender=&age=&accent=&language=&limit=
                        → { voices: [{ id, name, source, previewUrl?, languages?,
                            category?, labels? }] }  Reads only, spends nothing.

POST /v1/voice-changes  { assetId | jobId, voiceId (REQUIRED), productId?,
                          output?: "audio" (default) | "video" }
                        output "audio" → 200 { jobId, assetId, url, expiresInSeconds,
                            creditsCharged, billedSeconds, billedMinutes (deprecated),
                            voiceId }
                          ALREADY DONE — nothing to poll. Audio out; you mux.
                        output "video" → 202 { jobId, status, credits,
                            output: "video" }
                          A JOB. status: queued (new) | running (the same change,
                          already rendering) | succeeded (already made, nothing charged).
                          VIDEO source only, enabled per workspace. See Video out.

GET  /v1/generations/{jobId}
                        Video out only, on queued/running: poll until "succeeded"
                        (outputUrl = the new mp4, voiceChange.videoId = the copy) or
                        "failed" (voiceChange.reasonCode names the cause).

POST /v1/transcripts    { assetId | jobId }
                        → 200 { text, words[], segments[], srt, creditsCharged }
                          CHARGED, per minute of source. Timings in SECONDS. The
                          same source twice is free, which is why Gate 3's read of
                          the source is the same charge Gate 7 compares against.

GET  /v1/generations?kind=audio   → the recovery path when a response never arrived.
```

## Failure modes

- **`400` naming a 5-minute cap.** The source is too long, and **nothing was charged**.
  Split it and convert the parts; do not retry the whole file.
- **`400 invalid_input` naming what the deployment renders.** Voice changes are off on
  this deployment. Not a retry, not a `404`. Say so and stop.
- **`400` on `output: "video"` with an audio upload.** Video out needs a picture, and
  nothing was charged. Send the video source, or omit `output` and mux locally.
- **`400` saying to omit `output`.** Video out is not enabled for this workspace, and
  nothing was charged. Omit it and run Gate 6 yourself. Not a retry.
- **A video-out job ends `failed`.** `voiceChange.reasonCode` names the cause. A source
  with no speech fails with nothing charged (or, if an earlier attempt already found none, it
  is refused at the request, also free); a job that fails after finding speech is refunded.
  Report the cause and the balance before calling again.
- **`404` on the voiceId.** The voice is not yours, or it went inactive upstream. **This
  endpoint never substitutes a near-enough voice** — that is deliberate, because you cast
  a specific performance. Re-list, re-audition, re-pick. If it went inactive mid-request
  the credits are already refunded.
- **`409`.** Either the source job has not succeeded yet, or it has no audio to convert,
  or **a conversion of this source in this voice is already in flight** — the message
  names that job id. Wait a moment and call again: the stored audio comes back without a
  second charge. Anything charged before a `409` is refunded.
- **`429` with `details.reason: voice_change_concurrency_limit`.** Ten conversions are
  already open for the organization. It is its own queue, counted apart from renders,
  captions, transcripts and voice-overs, so this never means "stop generating video".
  Sleep on `Retry-After` and call again. Branch on `details.reason`, never on the status
  alone.
- **`402`.** Not enough credits; `details` carries `required` and `available`. Report
  both and the top-up path. Do not retry.
- **`502`.** The provider failed and the credits are refunded automatically. Read the
  message for whether the refund has landed or is queued.
- **A `403` carrying Cloudflare's `error code: 1010`.** Not your key. The edge refuses
  Python's stdlib `urllib` User-Agent outright, and the body is an edge page rather than
  the API's `{"error":{…}}` envelope. Use `curl`, or send a real `User-Agent`. Do not
  regenerate the key or tell the user their plan lapsed.
- **The new voice says a word wrong.** It was said wrong in the source. Nothing about
  conversion can fix it, and re-running with another voice buys the same mistake in
  another timbre. Two fixes: re-render the source with the word spelled phonetically and
  convert that (see Gate 3), or, **only on a span with no lips in frame**, splice a
  `POST /v1/voiceovers` take of the corrected line.
- **The sound effect turned into a voice.** The fence was wrong, or absent. The effect
  lives in the original track; re-run the assembly with the right `--speech-start`. This
  costs nothing — the conversion is already paid for and cached.
- **The finished file plays quieter than the source.** Read the assembly step's numbers.
  If the take matched the source but the output did not, the loss is in the mux, and it
  is 3 dB shaped like a mono-to-stereo rematrix.
- **The mouth stops matching partway through.** Something re-timed the audio: a
  crossfade, an `atempo`, or a take made from a different cut of the source. The assembly
  script warns when the take's duration and the source's disagree by more than a quarter
  second. Never speed a take up to fit.

## Hard rules

- **The human picks the voice.** Never default a `voiceId`.
- **Gate 1 before the upload.** A music bed converts, succeeds, and bills.
- Every number shown to a user comes from `POST /v1/estimates` in this session. This file
  contains no prices and neither does anything else in this repo.
- **Every charged call in the run is announced, not just the big one.** The conversion is
  one of three: the verification transcript is charged, and so is the source transcript
  when you need it.
- The picture is copied, never re-encoded, and the effects come from the original track.
- Verify by transcribing your own output. A run that was not read back is not finished.
- A different voice is a new charge. Audition with previews, not with conversions.
- Never promise a translation, an accent, or a pronunciation fix.
- Work in `outputs/<ad-name>/`, which is gitignored. Never invent a new top-level
  directory.

## Output format

1. **SOURCE** — what it is, how long, and what Gate 1 measured: speech present, the span,
   the current voice's pitch.
2. **BRIEF** — who is on screen, the language, the register the replacement has to hold.
3. **COST** — the live estimates, in one line, before anything is charged: the
   conversion **and** the transcript read-backs the verification needs. One number for
   one of three charges is not the cost of the run.
4. **SHORTLIST** — two or three candidates with their measurements and their preview
   files. Then **stop** and wait for the pick.
5. Then convert, assemble (on video out: poll), and verify.
6. **DELIVERY** — the output path, the loudness delta, the transcript read against the
   source, and what you looked at in the lip window.
