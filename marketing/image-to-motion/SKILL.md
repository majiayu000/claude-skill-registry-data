---
name: image-to-motion
metadata: {packVersion: 1.3.0}
description: >-
  Turn any still image into a professional motion graphic through the Novoads API on
  Seedance 2.5. Covers how to read a reference image, motion vocabulary for any image
  type — UI, marketing hero, flat-lay, key art, collage, product, character — the prompt
  clauses that control camera, timing, frozen regions and text fidelity, and the upload
  mechanics. Use whenever the user supplies an image and wants it animated, moving, or
  turned into video — including "animate this", "turn this into a motion graphic", "make
  this move", "この画像動かして", "モーショングラフィックにして", "I want the cards to pop in",
  "I want the bars to slide up", or when they describe motion beats for a static image.
  Also use when asked to write a Seedance prompt for an existing image. Do NOT use for
  text-to-video with no source image, restyling existing footage (this skill takes no video
  input), cloning a reference video (use clone-video-ad), or a product photo that should
  seed a new scene rather than move as-is (use novoads-api).
---

# Image → Motion Graphic

Any still can become a professional motion graphic. The work is direction, not damage control: decide what moves, in what order, and say it precisely enough that there is nothing left to interpret.

Vague prompts produce vague motion. Specific prompts produce the shot you pictured. That is the whole discipline.

> **Resolved, 2026-08-12 — `seedance-2.5` takes a start image again, and the render honours
> the `aspectRatio` you ask for.**
>
> Earlier the same day, `POST /v1/videos` with `"model": "seedance-2.5"` and a
> `startImageAssetId` failed server-side every time (isolated with nine single-variable
> probes; credits were charged and refunded automatically). The platform fix shipped and was
> verified live 2026-08-12: the same call that failed now renders, and a source image whose
> shape differs from the requested `aspectRatio` is fitted to the ask server-side with
> content-safe padding — nothing is cropped away, and the output arrives at the ratio you
> requested. No workaround is needed; write the call as this skill documents it.

## Before anything: this runs on a Novoads account

- **Base URL:** `https://api.novoads.ai/v1` (host overridable with `NOVOADS_BASE_URL` — host
  only, you append `/v1`).
- **Auth:** `Authorization: Bearer $NOVOADS_API_KEY`, read from `.env` at the repo root. The key
  is `novo_` plus 64 hex.
- **Check:** `./scripts/check-novoads-env.sh`; if the key is missing, run `./scripts/setup.sh`.
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

No account yet? **<https://novoads.ai/?utm_source=claude-code&utm_medium=github&utm_campaign=skill-pack>**
There is no free tier and no trial: every plan is a paid monthly subscription,
published at novoads.ai/pricing. Never call it free.

**Every HTTP mechanic here belongs to the pack, not to this skill.** Auth, strict bodies,
status codes, the poll loop, concurrency and error envelopes are written out once in
[`novoads-api/SKILL.md`](../novoads-api/SKILL.md) and its
[`reference.md`](../novoads-api/reference.md). This file carries the craft and the two or
three fields this genre needs.

**The cost gate.** Before the first render, price the exact configuration and wait for a
yes. **`prompt` is required on the estimate** — the body is strict and omitting it is a
`400`, which would leave you improvising past the one guard rail between the user and a
charge. Send the prompt you are about to render:

```json
{"kind":"video","model":"seedance-2.5","durationSeconds":8,"resolution":"720p","prompt":"<the full prompt>"}
```

The estimate charges nothing. There are no rates in this file on purpose: a written price rots
silently and a quote that disagrees with the invoice is worse than no quote. **N takes is N
charges** — say the multiplication out loud before it happens.

It does not see everything the render sees. `aspectRatio`, `startImageAssetId` and
`referenceAssetIds` are not on the estimate body, so a clean quote is not proof the
generation body is valid: the two-modes `400` below is invisible here and moderation runs
only at generation. A clean estimate prices the call, it does not bless it.

The pack's other spending gate, the one where a spoken line is approved on its own, does not
apply here: nothing speaks. That is one gate fewer, not permission to skip the cost gate.

### The estimate's warnings are UGC rules. One response, and it is not "comply".

`POST /v1/estimates` returns an advisory `warnings` array. It never refuses a call and never
changes a price. Its rules were written for talking-head UGC with an actor in frame, and they
match on substrings, so on a motion graphic they fire and fall silent for reasons that have
nothing to do with whether the shot is any good.

**`missing_actor_descriptor` is the one to understand.** Read literally it asks you to put a
person in the frame. **Never do that.** An agent that "fixes" it by inserting "a woman in her
20s in a grey zip hoodie" into a dashboard animation has destroyed the render to satisfy a
linter. Say you are overriding it and why.

**Do not read anything into whether it appears.** Its check is a bag of actor words that also
contains a two-digits-then-`s` pattern, put there to catch "a woman in her 20s" — so a beat
list timed `0.15s apart`, or one that mentions a `10s` mark, satisfies it by accident and the
warning vanishes. Measured both ways, 2026-08-10. Its absence is not a verdict on your prompt
and its presence is not a defect to fix.

**`banned_polish` from a quoted string is the other unfixable one, and it is common.** The
rule matches `perfect`, `flawless`, `cinematic`, `4k`, `masterpiece` and friends, and its
remedy is "delete the word and describe the real thing". That remedy is impossible when the
word arrived inside a string you transcribed off the reference: deleting it re-letters the
render, which is the one thing this skill exists to prevent. Check where the hit came from
before you touch anything — if it is inside quotes, override it and say so. Measured on a
real pricing page 2026-08-10, where the single warning traced to a card subtitle reading
"Perfect for scaling your AI video ads". Marketing copy is full of these words, so expect it.

**This file states no warning count, deliberately.** Three earlier drafts each asserted one
and each was wrong, because the count moves with incidental digits in the beat timings and
with words the craft itself recommends (`cinematic` in the key-art class trips a polish rule;
`then` in a beat sequence trips a chained-motion rule; a dash-prefixed beat list trips a
formatting rule). Read what comes back, judge each one against the prompt in front of you,
and say which ones you are overriding. That instruction stays true as the rules change; a
number does not.

## Step 1: Read the image

Look at it properly before writing anything. Record:

- **Dimensions and ratio.** If the requested output ratio differs from the source, the layout gets rebuilt rather than cropped — say so, and describe the new arrangement in the prompt rather than hoping for it.
- **Photographic or illustrated.** State this explicitly in the prompt. Omitting it is the most common way a painted reference comes back photoreal, or vice versa.
- **Light direction and quality.** Hard raking light and soft ambient light imply completely different motion. Long shadows moving is a beat; flat light has nothing to reveal.
- **Layer depth.** What sits in front of what. This is where parallax and staggered entrances come from.
- **Every legible string, transcribed verbatim.** You will quote these back in the prompt.
- **The accent structure.** Most strong reference images run on one saturated accent against a restrained field. Whatever draws the eye is what should move last, or move most.

## Step 2: Choose the motion

Match the vocabulary to what the image *is*. This is genre craft — a flat-lay wants different motion from a character render, and reaching for the wrong grammar is what makes AI motion look generic.

**UI, app screens, toolbars, widgets, dashboards**
Panels slide or scale into place and settle. Cursors travel along an arc and click. Press states compress and spring back; hover states lift and deepen their shadow. Tooltips, menus and toasts appear on the interaction that triggers them. Toggles flip, progress fills, counters and badges land. Decide whether screen contents scroll or hold — either is available, but choose deliberately and say which.

**Marketing hero — headline, device, floating cards**
Headline rises and fades in as a block. Device and hand slide in from the frame edge with a slight overshoot and settle. Floating cards pop from slightly under full scale with a bouncy overshoot, staggered rather than together. Progress arcs draw their stroke. Then a gentle out-of-phase idle float so the frame never feels frozen. If figures should count up, say so explicitly; if they should hold, say that instead.

**Flat-lay, evidence board, desk scene**
Items drop in and settle with their shadows catching up a beat late. String, thread and connecting lines draw along their path. Papers can lift and flutter at the corner. A slow light sweep across the surface reads beautifully and costs nothing. Magnifiers and lenses can glide.

**Painted key art, illustrated scene, game art**
The most permissive class. Parallax between depth layers, drifting dust and light shafts, water and cloth movement, slow reveals, ambient particle motion. A slow push-in or drift works here when you want cinematic rather than graphic.

**Collage, paper-cut, halftone**
Assemble-from-empty: elements fly, snap or hinge into place in sequence with slight rotation overshoot. Suits stepped, stop-motion timing rather than smooth easing. Textures can breathe.

**Product still, object, packaging**
Slow turntable rotation, light sweep across the surface, lid lift, pour, unfold, exploded-view separation, hero reveal from shadow.

**Character, mascot, avatar**
Idle breathing, blink, head turn, expression shift, hair and cloth secondary motion, a gesture into a hold.

Across all of them: **stagger paired elements.** Two things entering simultaneously read as one flat sheet; a fifth of a second apart reads as two independent objects with their own weight. That single choice does more for perceived production value than any other.

## Step 3: Write the prompt

Structure the shot as timed beats. Include every clause below — each one removes a decision the model would otherwise make for you.

```
[Shot type] of [subject]. [If nothing should speak, which is the norm here:
"A silent motion graphic with no spoken dialogue."]

CAMERA: [either "The camera is locked off and never moves: no pan, no tilt, no
zoom, no push-in, no orbit, no drift." — or the specific move you want, with its
speed and direction.] Lighting is [constant / describe the change].

The reference image is the exact composed state — every colour, shadow, layout
position and glyph matches it precisely.

TEXT: all text stays perfectly intact and pixel-identical to the reference image
at every frame — [quote every string individually]. Same font, same weight, same
size, same position, correctly spelled. Text is never redrawn or re-lettered; it
travels rigidly with the object it sits on.

[If any region should not animate:]
[REGION] holds completely still: no scrolling, no swiping, no changing content.

TIMED BEATS:
0.0s — [the opening state, including anything that is ABSENT]
[t–t]s — [one object, one motion, with easing]
...
[final]s — Everything holds. [Any permitted idle drift.] No fade out.

[Negatives:] No film grain, no vignette, no lens flare, no added elements,
no watermark, no extra text.

[Close on the ratio, in words, matching the aspectRatio you send:]
Vertical 9:16. — or Square 1:1. — or Horizontal 16:9. — or Classic 4:3. etc.
```

**Two of those lines are additions rather than craft, and both come from the pack's own
Seedance doctrine** (`novoads-api/SKILL.md`, the `audioEnabled` section): keep the silence
sentence *as well as* the flag, because the prose is what stops the model staging a talking
shot in the first place while the flag governs the audio track. And state the ratio in words
even though you also send `aspectRatio`, because the model will infer a shape from the prompt
when the prompt implies one. Neither is a reliable way to quiet the linter — a correctly
stated `4:3` still draws `no_aspect_ratio`, measured — so add them for the render, not for
the warnings array.

The prompt ceiling on this model is **4,000 characters**, which a full beat list fits
comfortably. Compose long prompts in a file under `prompts/` rather than passing them as a
shell argument.

Five clauses that carry most of the weight:

**Say the text should be perfectly intact, and quote every string.** This is the single highest-value line in the prompt. Asking for it explicitly works far better than leaving it implied, and naming each string individually works better than a general instruction.

**State the opening frame including what is absent.** If a tooltip, badge or card is visible in the reference and you want it to appear partway through, the prompt must say it is not there at 0.0s. Otherwise it is present from frame one and the reveal never happens. This is logic, not model behaviour — it applies no matter how capable the model is.

**Declare anything that holds still.** A region that should not move needs saying so. Silence is not an instruction.

**End with an explicit hold.** Without a final beat pinning the last state, models tend to invent a drift, a fade or a camera move to fill the remaining time.

**One object per beat, with easing named.** "The cards pop in" is three possible shots. "Each card scales up from slightly under full size with a soft bouncy overshoot, 0.2s apart" is one.

## Step 4: Run it

`POST /v1/videos` with `"model": "seedance-2.5"`, and the still in `startImageAssetId`, which
animates it as the literal first frame. **Always send `model` explicitly.** This skill's whole
grid below is 2.5's; the API's own default when the field is omitted is `seedance-2.0`, which
has a different duration grid and a different schedule, so an omitted field renders a model the
cost gate did not price.

- `durationSeconds` — an integer from the grid, which on this model runs **4 to 30**. Match
  it to the beat list; leave a beat of hold at the end. Out-of-grid values are rejected,
  never rounded. Most motion graphics live at the short end, and the schedule is per-second,
  so price the duration you actually need rather than the one the grid allows. Never rank it
  against other models from memory: which cell is dearest depends on the provider this
  deployment routes to, and the estimate is the only thing that knows.
- `aspectRatio` — `16:9` (default), `9:16`, `1:1`, `4:3`, `3:4`, `21:9`.
- `resolution` — `480p` or `720p`. **720p is this model's ceiling**, not a floor: 1080p and
  4k belong to other models and are a `400` here.
- `audioEnabled` — `false` unless sound is wanted.
- **Four takes gives useful choice.** There is no variations-per-call field, so that is four
  submissions of the identical payload, and **four charges** — which is why it belongs
  inside the cost gate rather than after it. At most **five** generations may be in flight
  per organization; a sixth comes back `429` with `details.reason: concurrency_limit`, which
  means wait for a slot rather than lengthen the backoff.

Submit returns `202` with `jobId` and `creditsCharged`. **The poll payload does not carry the
charge**, so log it from the `202` while you have it — a line written without it cannot be
completed later. Poll `GET /v1/generations/{jobId}` every 15 seconds until
a **terminal** status, then `GET /v1/generations/{jobId}/watch` for the file into
`outputs/<descriptive-name>/`. Nothing here has measured a `seedance-2.5` wait: say it is
unknown rather than lending it `seedance-2.0`'s range. Full sequence in
[`novoads-api/SKILL.md`](../novoads-api/SKILL.md).

If the still needs building or rebuilding first, generate it before animating. A crisp, correctly-composed, correctly-lettered source frame is the foundation of the whole shot — the video stage carries forward what it is handed. Both [`chatgpt-image-ad`](../chatgpt-image-ad/SKILL.md) (`gpt-image-2`) and [`nano-banana-image-ad`](../nano-banana-image-ad/SKILL.md) (`nano-banana-pro`) are available, and the decision tree between them is in [OVERVIEW.md](../../shared/skills/image-ad-prompting/OVERVIEW.md); when it matters, run the same prompt through both and compare rather than assuming. `POST /v1/images` usually answers with the finished still. One still going after about 105 seconds answers `status: "running"` with no images instead (API 2.39.0): poll `GET /v1/generations/{jobId}` to a terminal status and read `images[]` there. Never resubmit it: that job is already paid, and a resubmit is a second charge. Either way, the finished image's `assetId` goes straight into `startImageAssetId` with no download-and-re-upload hop.

Both of those generators auto-append three always-on guard clauses to whatever prompt you
hand them — no platform chrome, an 84% edge-safe zone, no glyph soup inside body text — so do
not write those constraints into the prompt yourself. Read
[safety-suffixes.md](../../shared/skills/image-ad-prompting/prompting/safety-suffixes.md)
when a still comes back with clipped text, invented emoji or in-feed UI in it, and **before
passing `--allow-chrome` or `--no-safe-zone`** to turn one off. A start frame with a headline
running off the edge animates into a video with a headline running off the edge.

**This skill takes no video input.** Since API 2.30.0 `omni-flash` accepts one reference
video (`referenceVideoAssetId`, see novoads-api) that guides a new render, but there is
no in-place restyle of existing footage and no multi-turn edit: `omni-flash` here is one stateless call, not the conversational editor its
vendor documentation describes. If the ask is to restyle a clip, say so and stop. A **timed
multi-scene switch** is different and is still reachable — it needs no video input, only a
prompt that describes each scene and when it changes. `omni-flash` is the model for it, and
its guide is [gemini-omni-flash](../../shared/skills/gemini-omni-flash/prompting/guide.md).
**Its grid is not the one above**: 20,000-character prompt ceiling, `durationSeconds` 4/6/8/10
only, `aspectRatio` `9:16` (default) or `16:9` and nothing else, **no `audioEnabled`**: the variant omits it and the body is strict, so sending it is a `400`.
Since API 2.30.0 it also takes `referenceAssetIds`, which this skill does not send. Read its grid before you carry any field across.

### Uploading the still

```
POST /v1/uploads  {"contentType":"image/png","sizeBytes":<exact bytes>}  → 201
  { assetId, uploadUrl, method, headers, expiresInSeconds: 900, maxBytes }
PUT the raw bytes to uploadUrl with the returned headers, byte for byte  → 200
pass assetId as startImageAssetId
```

Two things worth knowing before they cost a call:

- **`Content-Type` and `Content-Length` are both signed into the URL.** If either differs
  from what was returned, storage rejects the PUT with a `403` that looks like an auth
  failure and is not one. Measure the file, do not estimate it.
- **The `assetId` is durable and reusable without limit** — it is the storage key itself.
  Upload the image once and reuse it across every iteration and every model. The 900-second
  expiry belongs to the **upload URL**, not to the asset. That distinction is the one most
  likely to be conflated, and re-uploading between takes is wasted work.

`startImageAssetId` and `referenceAssetIds` are **separate modes and cannot be combined** —
a body with both is a `400` naming exactly that, before any charge. Start frame animates one
image; references composite several into a new scene. This skill is the start-frame mode, so
it sends exactly one image.

For the record, because vendor tutorials quote wildly different numbers: **reference images
cap at 9** on `seedance-2.5` here, and the larger figures floating around belong to the raw
providers underneath rather than to this API. Read it off `referenceAssetIds`'s `maxItems` in
the live `openapi.json` rather than from any file, this one included. It is stated only so a
tutorial's 30 or 50 does not look authoritative — **a job that wants that mode is not this
skill**, and it routes to `novoads-api`.

## Step 5: Review and iterate

Generate several, pick, then refine the prompt rather than rerunning it unchanged. Look at:

- **Did the beats fire in order,** or collapse into one simultaneous move? If collapsed, spread the timings further apart and shorten each one.
- **Is the camera doing what you asked?** Unrequested drift usually means the camera clause was too short — expand it into the explicit no-pan-no-zoom-no-push list.
- **Read every quoted string at full size.** Check the small labels, not just the headline.
- **Did anything hold still that should have moved,** or move that should have held? Both are prompt clarity problems, not model problems.
- **Shadow and light consistency**, especially in flat-lay and product work where one light direction is the only depth cue.

When something is off, add specificity rather than emphasis. Naming the object, the distance, the direction and the easing beats restating the same instruction more forcefully. If a beat keeps coming out wrong, describe it as a rigid transform of a named object — that is almost always clearer than describing the effect you want.

## Hard rules

1. **Price it live before every render**, from `POST /v1/estimates` in this session, and
   **send `prompt`** — it is required, and a body without it is a `400`. No rate lives in
   this file.
2. **N takes is N charges**, said out loud before the first one fires.
3. **720p is the ceiling** on this model. Do not offer or submit higher.
4. **Never send `startImageAssetId` and `referenceAssetIds` together.** Separate modes.
5. **Upload once.** The asset is durable; the URL is what expires.
6. **The 0.0s beat names what is absent**, or the reveal cannot happen.
7. **Quote every string individually** in the TEXT clause, and read every one back at full
   size in QA.
8. **Text fidelity on our render path is unverified.** Write the clause because it is what
   the model responds to. Do not tell a user it has been verified here until eval E6 has
   been run. See [evals.md](evals.md).
9. **Never add an actor to satisfy `missing_actor_descriptor`.** Override it out loud, and
   read nothing into whether it appeared — its check is keyed on substrings a beat list
   trips by accident.
10. Working files go in `outputs/<name>/` and long prompts in `prompts/`. Never invent a new
    top-level directory.
