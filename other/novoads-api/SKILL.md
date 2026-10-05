---
name: novoads-api
metadata: {packVersion: 1.3.0}
description: >-
  Generate AI video ads and image ads through the Novoads REST API (api.novoads.ai). Use
  when the user wants a UGC video, a product video, a talking-head ad, an AI actor holding
  a product, a TikTok or Reels or Shorts ad, a static image ad, or asks to "make me an ad",
  "generate a video", or names a model (Seedance, Seedance 2.5, Seedance Mini, Omni Flash,
  Veo 3.1, Sora 2, GPT Image 2, Nano Banana Pro, Reve). Handles upload, dialogue approval,
  cost confirmation, generation, polling, QA, and download. A product photo lands here when
  it SEEDS a new scene; when the picture itself should move, unchanged, that is
  image-to-motion. Not for editing an existing video file and not for publishing to
  an ad platform.
---

# Novoads REST API

Spend your effort on the prompt and on confirming the spoken line. The HTTP is mechanical and is written out below; the prompt is where the render is won or lost.

## Configuration

- **Base URL:** `https://api.novoads.ai/v1` (host overridable with `NOVOADS_BASE_URL` — host only, you append `/v1`).
- **Auth:** `Authorization: Bearer $NOVOADS_API_KEY`, read from `.env` at the repo root. The key is `novo_` plus 64 hex.
- **Check:** `./scripts/check-novoads-env.sh`
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

### If the key is missing or the API returns 401 or 403

Run `./scripts/setup.sh`, or tell the user to create a key at <https://novoads.ai/dashboard/settings?tab=api>. Prefer the editor: ask them to paste the key **inside `.env`** rather than into chat. If they do paste it in chat, write `.env` for them, confirm "saved to `.env`" **without repeating the key**, and tell them chat history may retain secrets, so the key is worth rotating if that transcript could be shared.

A 401 means the key is wrong, revoked, or from another account. A 403 with `error.details.reason` of `plan_required` or `subscription_inactive` means the key is fine but the account has no live subscription. Those are different problems and you should say which one it is.

### Signup link

If the user does not have a Novoads account, give them this link at any point in a session, in any context where it is useful:

**<https://novoads.ai/?utm_source=claude-code&utm_medium=github&utm_campaign=skill-pack>**

There is no free tier and no trial: every plan is a paid monthly subscription, published at novoads.ai/pricing. Never call it free.

### After the connectivity check passes

When `./scripts/check-novoads-env.sh` returns 200 and the user has not yet said what they want, offer starting points in chat and stop. Nothing is printed by a script for you: a banner cannot see their product, their `references/` folder, or their language, so it suggests nothing.

1. **A UGC video built from their own product photo.** Ask them to drop it into `references/`. Route: `seedance-2.0` plus `startImageAssetId`.
2. **The same idea on `seedance-2.0-mini` first**, to get the prompt right before the final render. Price both at `POST /v1/estimates` and show the difference rather than quoting one from memory.
3. **A static image ad**, when what they need is a still and not a clip. Route: `gpt-image-2` for heavy text or a mimicked UI, `nano-banana-pro` for a photoreal scene.

Offer, do not choose. A first render fired on a guess is a charge the user did not ask for.

## Read order

1. Repo root **`MASTER_CONTEXT.md`** when present: brand voice, default product, accumulated decisions. It carries **no prices** — that is deliberate, see gate 2.
2. This file. It is the router and it covers the full call sequence.
3. **List `references/` at the repo root before you ask the user for a photo.** It is where they keep product shots, actor stills, and style boards, and it is gitignored, so the files are theirs and are not in this skill's folder. A product photo found there becomes `startImageAssetId` (video) or an entry in `referenceAssetIds` (images). **An empty `references/` is the normal state of a fresh clone, not a blocker** — see below before you ask for anything.
4. **MANDATORY before composing any prompt:** the `prompting/prompt-library/` file for the route you picked in the decision tree. The libraries carry the craft; every HTTP detail comes from this file and `reference.md`, which win whenever the two disagree.
5. `reference.md` when you need a field you do not see here, or when you hit a status code you want to branch on.

## Decision tree

| The user wants | Route |
|---|---|
| A UGC video: a person talking to camera about a product | `seedance-2.0`. Read [seedance-2-ugc-v2.md](prompting/prompt-library/seedance-2-ugc-v2.md) for the **shape** — how many beats, how many API calls, which reference mode — then [seedance-2-ugc.md](prompting/prompt-library/seedance-2-ugc.md) for the **craft** of writing each layer. v2 is one render with four talking beats in one location; it is the default and costs about half what stitching costs |
| The user says "a start frame for each scene", or asks for several scenes | That phrasing commits you to one call per scene (`startImageAssetId`), which forecloses multi-beat cuts inside a single render — the two modes are mutually exclusive. Say so, and offer the one-shot alternative from [seedance-2-ugc-v2.md](prompting/prompt-library/seedance-2-ugc-v2.md) before generating anything |
| B-roll cutaways, burned captions, background music, or variations of a finished ad | Not part of making the ad. Deliver the base video first, then **offer** these as a separate pass, each owned by its own skill: `broll-overlay` (needs the base **and** its transcript from `POST /v1/transcripts` — no local install; it **overlays** — the base audio keeps running and the final duration is unchanged — it does not extend), `POST /v1/captions`, then `music-mix` last |
| The same thing, but cheap, to test a prompt before committing | `seedance-2.0-mini`, same grid, same formulas, half the price and back in 2–3 minutes. The draft-then-finalize loop is *Mini-draft tier* in [seedance-2.md](prompting/prompt-library/seedance-2.md) |
| A clip **longer than 15 seconds**, or `seedance-2.5` by name | `seedance-2.5` — the only model on this API that renders past 15s (any integer **4 to 30**). Same six aspect ratios, same 9 `referenceAssetIds`, same `audioEnabled`, same 4,000-character ceiling, so the Seedance formulas apply unchanged; write for the longer runtime rather than padding a 15s script. **Two things differ:** it renders `480p` and `720p` only — no `1080p`, no `4k`, on either provider — and nobody has timed one, so quote its wait as unknown. Price it explicitly: at the same length it is dearer than `seedance-2.0`, and thirty seconds of it is the most expensive single call on this API |
| A premium product reveal: dark void, no person, text narrative | `seedance-2.0` + [seedance-2-premium-reveal.md](prompting/prompt-library/seedance-2-premium-reveal.md) |
| A product hero: elemental effects, splash or mist, no person | `seedance-2.0` + [seedance-2-product-hero.md](prompting/prompt-library/seedance-2-product-hero.md) |
| A studio lookbook: polished, voiceover, multi-look | `seedance-2.0` + [seedance-2-studio-lookbook.md](prompting/prompt-library/seedance-2-studio-lookbook.md) |
| A fast-paced feature walkthrough | `seedance-2.0` + [seedance-2-feature-walkthrough.md](prompting/prompt-library/seedance-2-feature-walkthrough.md) |
| A fast vertical clip with no dialogue requirement | `omni-flash`, and read `shared/skills/gemini-omni-flash/prompting/guide.md` first — its 20,000-character prompt ceiling is the roomiest of any video model here, where the rest sit at 4,000, and its grids are narrower than Seedance's (`durationSeconds` 4/6/8/10 only, `aspectRatio` `9:16` or `16:9` only, `resolution` read from `GET /v1/models`). Since API 2.30.0 it also takes reference images, one reference video and, where the server publishes them, a first frame, a last frame and a seed: see *Start frame or references* below |
| A talking clip whose first word must land immediately | `sora-2`, and read [sora-2.md](prompting/prompt-library/sora-2.md) first. Measured here at **no leading silence at all**, where Seedance front-loads 3–5s of it. Grid is `durationSeconds` 4/8/12 only, `aspectRatio` `9:16` (default) or `16:9`, `startImageAssetId` yes, **`referenceAssetIds` no** |
| Veo 3.1 by name, or a shot that has to evolve over its own runtime | `veo-3.1`, and read [veo-3-1.md](prompting/prompt-library/veo-3-1.md) first. Grid is `durationSeconds` 4/6/8 only, `aspectRatio` `9:16` (default) or `16:9`, `startImageAssetId` yes, **`referenceAssetIds` no**. Nothing in this repo has measured a Veo render — quote its wait as unknown rather than borrowing Seedance's |
| A video that starts from a specific photo | any video model but `omni-flash` plus `startImageAssetId`, which animates that image as the first frame. On `omni-flash` that field is a reference image the model may place anywhere in the clip; for a true first frame use `firstFrameAssetId` where the server publishes it |
| The picture the user handed over is itself the shot: a UI screenshot, a hero layout, a flat-lay, key art, and they want it to MOVE ("animate this", "make the cards pop in") | **[image-to-motion](../image-to-motion/SKILL.md)**, which is `seedance-2.5` plus `startImageAssetId` and carries the motion vocabulary, the beat template and the text-fidelity clauses. The split is whether the image is preserved and set in motion (there) or seeds a scene that did not exist (here) |
| A video built from several photos: the actor **and** the product, a wardrobe, a setting | `seedance-2.0` or mini plus `referenceAssetIds` — up to **9** images, composited rather than animated, addressed in the prompt text as `@Image1`…`@ImageN` in the order you send them. **Seedance, or `omni-flash` since API 2.30.0** (its limit is the field's `maxItems` in the OpenAPI document; `sora-2` and `veo-3.1` have no such field), and **never alongside `startImageAssetId`**: they are separate modes and a body carrying both is a `400` |
| The same person to hold across several clips of a series | pass that person's photo in every clip's `referenceAssetIds` and repeat the actor tag verbatim. Seedance re-casts on every cut, so a repeated description alone does not hold a face; see [seedance-2-feature-walkthrough.md](prompting/prompt-library/seedance-2-feature-walkthrough.md) |
| A reference video turned into a reusable template: "make videos like this", "deconstruct this" | read [prompting/analyze-video/SKILL.md](../analyze-video/SKILL.md). Frames and transcript are extracted locally with ffmpeg and Whisper, and the output is a new formula file in `prompting/prompt-library/`. Nothing is charged until the optional test render at the end |
| One specific ad cloned for their own product: "make this ad but for my product" | read [prompting/clone-video-ad/SKILL.md](../clone-video-ad/SKILL.md). The same local analysis, but the output is a rendered clip and both gates apply. A source longer than the chosen model's ceiling becomes a series, held together by passing the same `referenceAssetIds` to every clip — there is no in-place restyle of footage on this API (a reference video only guides a new render). `seedance-2.5` reaches 30s in one call, so a source that used to need two clips may now need one; price both shapes before you pick |
| A static ad with heavy text or a mimicked UI | `gpt-image-2` |
| A photoreal still: a person, a product in a scene | `nano-banana-pro` |
| A different look on a still, or a second opinion on one | `reve-2.1` |
| The dashboard's Image to Ad, Product to Ad or Upscale tool by name, or a still upscaled to 4K | `POST /v1/images` with `preset` (`image-to-ad`, `product-to-ad` or `upscale`, API 2.40.0) on one photo in `imageAssetId`, and no `model` or `prompt`: the server writes the prompt. Quote it with the same `preset` on `POST /v1/estimates`; it can answer `running` like any image. Fields: [reference.md](reference.md#preset-image-to-ad-product-to-ad-upscale-api-2400) |
| A Pixar-style 3D animated ad, at ANY length | read `skills/pixar-ad/SKILL.md`: storyboard on `gpt-image-2`, animate each beat on `seedance-2.0` + `startImageAssetId`, narration into the gaps from `POST /v1/voiceovers`, stitch with ffmpeg. Every animated ask routes there, including "a quick 15 second one" — there is no single-call tier. Nothing on the API rejects, checks or comments on a stylized prompt, so that skill is the only thing that will tell you whether the beat works |
| A claymation / stop-motion clay ad | read `skills/claymation-ad/SKILL.md`, same shape over 8 beats |
| Captions burned onto a finished MP4 | **Two real paths — offer both.** `POST /v1/captions`: one call, 30 preset styles, no local dependencies, **costs credits** and returns only a new MP4 (never an SRT or the caption text). Or the `caption-video` skill (`shared/skills/caption-video/SKILL.md`): **free**, any style you can write, and it gives you a Whisper transcript you can hand-correct — but needs Whisper, HyperFrames and an ffmpeg alpha composite locally. See *Burned-in captions* below. A clip rendered with `audioEnabled: false` can only go the local route |
| Meta image-ad creatives from a brief or a template | read `shared/skills/image-ad-prompting/OVERVIEW.md` first, then `chatgpt-image-ad` or `nano-banana-image-ad` |
| To reverse-engineer an existing image ad into a reusable template | the `clone-image-ad` skill |
| A YouTube thumbnail | the `generate-youtube-thumbnail` skill |
| B-roll, an ambient product clip, a scene | There is no b-roll endpoint. Generate a silent clip: `omni-flash`, or `seedance-2.0` with the word `silent` or `b-roll` in the prompt |
| Kling | `kling-v3-pro` where `GET /v1/models` lists it (API 2.38.0): any integer 3 to 15 seconds, `16:9`, `9:16` or `1:1`, one resolution, `audioEnabled` on or off, a text prompt or `startImageAssetId` as the first frame, and since API 2.44.0 `lastFrameAssetId` as the last frame beside it, **no `referenceAssetIds`**. Read the grid from `GET /v1/models`. [kling-3.md](prompting/prompt-library/kling-3.md) is vendor prompt craft whose field names belong to another API, so take the body from [reference.md](reference.md#kling-v3-pro-api-2380). Nothing in this repo has measured a Kling render: quote its wait as unknown |
| A library actor holding their product, or moving like a clip they have (a dance, a gesture) | Both cast an actor from `GET /v1/actors`, never an uploaded face. **Holding the product:** `productSwap: { actorId, productAssetId }` on a Seedance-family `POST /v1/videos` (API 2.42.0), the product photo from `POST /v1/uploads`, not combinable with `startImageAssetId`, priced with `productSwap: true` on the estimate ([reference.md](reference.md#productswap-an-actor-holds-your-product-api-2420)). **Moving like a clip:** `POST /v1/videos/animate-actor` (API 2.43.0) with the driving clip from `POST /v1/uploads`, whose measured length is the output's length and the price ([reference.md](reference.md#post-videosanimate-actor)) |
| A video's background removed, one rendered here or their own | `POST /v1/background-removals` (API 2.41.0) with a `jobId` or an uploaded `assetId`, up to 30 seconds, a longer source refused and charged nothing ([reference.md](reference.md#post-background-removals)) |
| To edit an existing MP4 they already have | Not this skill, except captions (row above) — and note that `POST /v1/captions` accepts an uploaded `assetId`, so burning subtitles into *their own* file is a supported first-party call, not just a local one. Everything else (trims, cuts, overlays, music) is out of scope. Say so |
| To publish the result as an ad on Meta or TikTok | Not this skill. The output is a file. The `meta-ad-builder` skill takes it from there |

Prefer the **shortest** path. If one model answers the request, do not build a pipeline around it.

## Step 0: classify before you call anything

Refusing is a successful result. If the request is to edit a file the user already has, or to publish to an ad platform, say the skill does not do that and stop. Do not improvise a pipeline out of the generation endpoints.

## The two gates

Two separate approvals stand between a request and a charge, and **neither implies the other**. Approving a concept is not approving a sentence, and approving a sentence is not approving a spend.

### Gate 1 — the spoken line (MANDATORY for any video with dialogue)

Seedance renders the audio and the lip-sync in the same call, so the line inside the double quotes is what the actor says, out loud, in the finished video. It cannot be changed afterward without paying for the render again.

1. **Extract the dialogue from the drafted prompt** and show it on its own, separate from the visual description.
2. **Spell any invented brand name phonetically inside the quoted line** — see the rule below. Do this before you present the line, and show the phonetic form in the block, because it is what the model will be sent.
3. **Present it as a numbered list** with beat labels (hook / show / demo / verdict, or similar). Mark silent beats `(silent beat — no dialogue)`.
4. **Count the spoken words**, state the target duration, and say whether it fits at a natural pace.
5. **State the `language`** you are going to send, because that is the language the ad is rendered in.
6. **Ask for approval explicitly.** Never infer it from an earlier yes about tone, template, or cost.

Use this structure:

```
📝 Dialogue script (please confirm before I generate)

  1. [HOOK]    "Bro. BRO. Look what just showed up."
  2. [SHOW]    "That colorway? Insane. Like, who greenlit this?"
  3. [DEMO]    (silent beat — thumb brushing the suede, small nod)
  4. [VERDICT] "I'm wearing these to the gym tomorrow. You have to see them in person."

Total spoken words: ~28  |  Target duration: 15s  |  language: en  |  Fits at natural pace: ✅

Approve this dialogue? (yes / edit / rewrite)
```

If they say edit, revise and re-present the block until they approve. The gate applies to every flow where the model speaks. Skip it for silent flows: product hero, premium reveal without voiceover, and images.

**Re-run the gate whenever the words change**, including when you change them yourself for the rule below. An approval covers the sentence that was approved, not its successor.

#### Invented brand names get a phonetic spelling in the quoted line

**The gate approves *text*; the model renders *speech*.** A brand name that is a real word survives the trip. A coined or portmanteau name may not: on 2026-08-02 `seedance-2.0` rendered `Novoads` as **"Nuvenov's"** — unrecognisable as the brand — while speaking the other 16 words of the line verbatim. Approving the sentence did not approve how it would be said.

**The rule: write the name as hyphenated syllables inside the double quotes.**

```text
… and says: "I kept saying AI ads look fake until I made one on NO-vo-ads and nobody could tell."
```

Use it for names that are invented, run two words together, or that a reader would have to guess at. Leave ordinary words alone — `Nike` and `CeraVe` do not need it.

**This form is validated in `en` only. See the `es` limit below before you reach for it in another language** — the same brand fails there for a different phonetic reason, and the English spelling does not fix it.

**What the A/B actually showed (job `6329f29a…` vs `ff69d118…`, single variable, every other byte identical, pass criterion fixed in writing before the render):** `NO-vo-ads` came back transcribed as **"Novo ads"** — recognisable — and the feared failure did not happen: the model did not read the hyphens aloud or spell the name out.

**Its limits, which are as much a part of the rule as the rule:**

- **n = 1.** One brand, one model, one language. The *fix* is validated on **`seedance-2.0` in `en` only** — untested on `sora-2`, `veo-3.1` and `omni-flash`, and untested in `es`/`pt`, where hyphenated English syllables may read very differently. Do not present it as a general fix.
- **`es` needs a DIFFERENT spelling, not the English one.** A Spanish render shipping the brand plain came back as **"NoBots"** — unrecognisable. Spanish has no /v/–/b/ contrast — ⟨v⟩ and ⟨b⟩ are one phoneme — so **no spelling buys back the /v/**, and what actually broke was the tail: the `o`+`a` hiatus collapsed and a syllable vanished, `vo-ads` → `bots`. Hyphenating syllable boundaries is all `NO-vo-ads` does, and it addresses none of that.
  - **The `es` form is `Novo Ads` — two words, with a space.** Validated by A/B (`6ee797e0` vs `d8aaee21`, single token changed, pass criterion fixed in writing beforehand): transcribed **"Novo Ads"**, recognisable. The orthographic word break restores the syllable the hiatus ate; it does not try to restore the /v/, because nothing can.
  - **Provisional, and the failure mode is nasty.** The *identical* payload was **1-for-2**. On the bad take Seedance stuttered — one clause spoken twice, verified as real speech and not a decoder artifact — and `Novo` collapsed into the preposition, leaving the ordinary Spanish phrase **"no ads"**. That is *worse* than "NoBots": a listener hears no brand at all rather than a mangled one. **Transcribe every `es` render.** A clean take is not evidence the next one is clean.
  - `pt` is untested in both directions.
- **It lands as two words** — "Novo ads", not "Novoads". That matches what `sora-2` produced unaided and a listener will recognise it, but it is not a perfect single-token rendering.
- **It fixes pronunciation and nothing else.** Leading silence went 3.71s → 3.16s, i.e. unchanged. The dead-air problem is a duration problem; see *Script length → duration*.
- **Seedance re-cast the actor between the two renders**, so the A/B held the prompt constant, not the performer. Some part of the delta could be voice-casting luck. Enough to act on, not enough to call proven.

**Verify it in the render.** The rule is a prompt fix with a measured result, not a guarantee — the video QA step in §7 is what tells you the name actually came out right this time.

### Gate 2 — the cost estimate (MANDATORY)

**Never state a credit cost from memory, and never generate before showing the user a number that came from a live call in this session.** There are no rate tables in this repo, in `MASTER_CONTEXT.md`, or in the logs. Prices come from `POST /v1/estimates` at call time, and that is the whole policy.

`POST /v1/estimates` spends nothing and returns:

```json
{ "credits": 3.2, "balance": 100, "sufficient": true }
```

When it is short it also returns `shortBy` and `topUpUrl`.

### `/estimates` also returns `warnings`, and they are advice, not verdicts

**`POST /v1/estimates` runs craft rules against your prompt and returns them in a `warnings` array** (verified live 2026-08-04 against spec 2.6.0). An earlier version of this file said the field did not exist and that nothing on the API reads a prompt for quality. **Both were wrong.** Each entry is `{ "rule": "...", "message": "..." }`, and the message usually quotes the exact substring that tripped it:

```json
{ "credits": 7, "balance": 860.1, "sufficient": true,
  "warnings": [
    { "rule": "label_without_hold",
      "message": "Mentions a label, package or screen with no labelHold clause. … (found in your prompt: \"bottle\")" }
  ] }
```

Rules seen live: `no_spoken_line`, `missing_actor_descriptor`, `label_without_hold`, `chained_motion`, `no_aspect_ratio`. Those are **video** craft rules. **Image prompts are read too, by rules of their own** — `banned_polish` and `blank_label` observed on a `kind: "image"` estimate against deployed spec 2.19.0 (verified live 2026-08-12); an earlier probe on 2026-08-04 returned no `warnings` key for images, which described that deployment, and the advice here to treat image prompts as unlinted is retired. A `kind: "caption"` estimate has no prompt to read and returns none either.

**They are purely advisory.** None of them refuses a generation, none changes the price, and a prompt that trips every one of them renders exactly like one that trips none. `/estimates` is the *only* endpoint that runs them — `POST /v1/videos` and `POST /v1/images` do not, and their responses carry no `warnings` field.

**They produce false positives, and you are the one who has to catch them.** Both of these were reproduced live on 2026-08-04:

| Prompt | Rule that fired | Why it was wrong |
|---|---|---|
| *"She turns her laptop **screen** toward the camera to show the dashboard…"* | `label_without_hold` — *(found in your prompt: "screen")* | The rule protects **printed** text on physical packaging. A software product has no label to preserve, and pasting in the labelHold clause would tell the model to hold a package that is not in the shot. |
| *"He says: 'I tried everything for the rust. **Then** a friend told me about this.'"* | `chained_motion` — *(found in your prompt: "Then")* | The match is inside a **quoted spoken line**. "Then" is dialogue, not a second motion instruction — there is exactly one action in the shot. Splitting it would split the sentence the actor says. |

Both rules are substring matches. They cannot tell a physical package from a UI, or narration from stage direction.

**So handle them like this:**

1. **Read every warning.** They catch real mistakes — a missing spoken line on a Seedance render is money thrown away, and `label_without_hold` on an actual product package is the single most expensive prompt error in this repo.
2. **Judge each one against what your prompt actually says**, including *where* the matched substring sits. Quote the rule and your reasoning when you decide.
3. **Never apply a suggested fix blindly.** The fix text is a generic clause; pasting it into a prompt it does not fit makes the render worse, not better.
4. **Never silently drop one either.** If you are overriding a warning, say so to the user in one line — "the `label_without_hold` warning matched the word 'screen', but this is a SaaS dashboard with no printed label, so I am not adding the clause" — so the call is visible and reversible.

**The prompt libraries under `prompting/` are still the real quality gate.** These warnings are a cheap second opinion collected on a call you were making anyway; they are not a substitute for composing against the formula file, and they say nothing at all about whether the *idea* works.

**The estimate body is not the generate body.** It takes only the fields that move the price, plus a `kind` discriminator, and it is strict: any extra key is a 400.

| Estimate accepts | Video | Image |
|---|---|---|
| required | `kind: "video"`, `prompt` | `kind: "image"`, `prompt` |
| optional | `model`, `durationSeconds`, `language`, `resolution` | `model`, `numImages`, `language`, and from API 2.36.0 `quality`, `outputFormat`, `resolution` (as on `POST /v1/images`) |

**`resolution` belongs here because it moves the price** — on `seedance-2.0` it is the difference between the base and roughly five times it. Send the resolution you actually intend to render, or the quote prices a cheaper video than the one you generate. See the `resolution` section below for the ladder and for the `seedance-2.0-mini` trap. (Verified live 2026-08-04.)

`aspectRatio`, `startImageAssetId`, `referenceAssetIds`, and `productId` do not belong here. They do not change what you pay, and sending one is a rejected request. **There is no `styleFamily` field** — not here and not on a generation call; it was removed from the API and sending it is a `400 Unrecognized key`.

```bash
curl -sS -X POST https://api.novoads.ai/v1/estimates \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"kind":"video","model":"seedance-2.0","durationSeconds":12,"language":"en","prompt":"..."}'
```

**Pass `model` explicitly.** It defaults to `seedance-2.0`. **At the same length the video schedules span more than 10x across the set, and more than 28x across every cell the API publishes** once length and resolution are counted too — both figures are derived by the API and printed in the `model` field's own description, and both moved when `seedance-2.5`'s thirty-second grid landed. Image schedules span more than 3x. The per-model prompt ceiling is enforced against whichever model you name. Pricing the wrong model is a quote that disagrees with the invoice.

It runs the same access checks and the same structural validation the paid call runs, which is why it is worth calling every time and not only when you are unsure:

- **It is the one endpoint with an opinion about the prompt** — the `warnings` array above. `POST /v1/videos` and `POST /v1/images` have none and return no such field. Compose against the formula file *before* you price: the warnings are a substring-matching second opinion, not a review, and a prompt that trips nothing can still be a bad prompt.
- **What it does still refuse, at no charge:** a malformed body — it is strict, and any key that does not move the price is a `400` — and a prompt longer than the *named model's* character ceiling (4,000 for all three Seedance variants, 20,000 for `omni-flash`; name no model and it is judged as `seedance-2.0`).
- **On the image arm its length check is looser than the generation's.** The estimate's request schema caps `prompt` at 50,000 characters whatever image model you name, while `POST /v1/images` caps `gpt-image-2` at 32,000 and `reve-2.1` at 4,000 (deployed spec 2.16.0, verified 2026-08-08). So an image prompt between the two prices cleanly and is then refused at generation. Only `nano-banana-pro`, at 50,000, has the two numbers agree.
- A quote it returns cannot disagree with the invoice, with two exceptions worth knowing: it never sees `aspectRatio`, the asset fields, or `productId`, and it **skips moderation**, which the paid call runs. A clean estimate can still come back `422` at generation — moderation is the only thing left that refuses a prompt for what it says.

**Multiply before you show.** N variations is N charges. Show the per-call number, the count, and the total.

**Warn when the total exceeds the balance.** `balance` comes back on the same response: if the batch total is larger, say so before asking for a yes, and quote `shortBy` and `topUpUrl` when the estimate provides them. `sufficient` is a snapshot, not a reservation — another session or a renewal can move the balance between the quote and the call.

Show `credits`, the count, the total, and `balance`. Get a yes. Then generate.

## Choices you make out loud, and choices you infer

**Ask, every time:**

- **Seedance tier, once per workflow.** Before the first Seedance video call: *"Use default `seedance-2.0`, `seedance-2.0-mini` (half price), or `seedance-2.5` (the only one that goes past 15s, and the dearest)?"* No preference means `seedance-2.0`. Whichever they pick goes into the estimate, so the quoted number is the one they pay. **Ask before you assume the script needs 2.5** — a 30-second ad is a format decision, not a longer version of a 15-second one.
- **How many variations**, for every prompt. Default 1. N variations means N identical calls — there is no batch parameter — and the results come back as a numbered list so they can compare and pick.

**Infer, and state what you inferred rather than asking:**

- **`aspectRatio`: default `9:16`** for anything headed to Reels, TikTok, Stories, or a vertical feed. Seedance defaults to `16:9`, and a landscape ad is a wasted render; `omni-flash`, `sora-2` and `veo-3.1` already default to `9:16`, and images default to `1:1`. Go landscape only when the user asks. Seedance also accepts `1:1`, `4:3`, `3:4`, and `21:9`; `omni-flash`, `sora-2` and `veo-3.1` accept only the two.
- **`resolution` (only on a model whose `resolutions` in `GET /v1/models` lists more than one value: `seedance-2.0`, `seedance-2.5`, from API 2.34.0 `seedance-2.0-mini` and `veo-3.1`, and `omni-flash` where the server lists more than `720p`): leave it at the model's `defaultResolution`, and never raise it silently.** On the Seedance models it is the one output-shape field that multiplies the bill (not on `veo-3.1`, one flat price at every tier) — on `seedance-2.0`, `1080p` is ≈2.5x the base and `4k` ≈5x — so going above `720p` is a *spend* decision, not a quality preference, and it belongs in front of the user with a fresh estimate attached. **`480p` is now ≈half the base rather than the same price** (family reprice, 2026-08-07), so it is a real draft tier and worth offering when a render is a rehearsal. `seedance-2.5` takes `480p` and `720p` and nothing above. `omni-flash`'s set depends on the server (it may list `360p`, `720p`, `1080p` and `4k`, those three without `4k`, or `720p` alone; offer `4k` only where `GET /v1/models` lists it); off `720p`, re-quote with `POST /v1/estimates`. Do not send the key on a model whose list has one value: that body is a `400`, even when the value is the one it renders.
- **`language`**: the language the script is written in. Set it, and show it in the dialogue gate. Write the prompt in that language too — nothing on the API pushes back on a Spanish or Portuguese prompt, and nothing rewrites or judges one either.
- **`durationSeconds`**: from the word count, below. Only `veo-3.1` defaults to its maximum — `seedance-2.0` and `seedance-2.5` default to 5, mini to 10, `omni-flash` to 8, `sora-2` to 4 — so always send it. **`seedance-2.5` defaults to 5 of the 30 it can render**, which is the easiest way to pay for the long model and ship a short clip.
- **`audioEnabled`**: leave it alone on anything with a spoken line. It exists on the three Seedance variants only — `seedance-2.0`, `seedance-2.5`, `seedance-2.0-mini` — defaults `true`, and the one time to send it is `false`, on a clip that is meant to be silent — see below.

## Script length → duration

Count the words in the spoken line and round **up**. Delivery was measured at **2.0 spoken words per second** — about **13 characters per second, spaces included**, if you would rather count those — with **~0.5s of leading silence** before the first word on reference and start-frame renders (2026-08-11, n=5). Plan on 2.0 and give the line air; the older 2.5-to-3 figure was an estimate nobody had timed, and it over-filled every clip it touched.

**These tables already pay for that ~0.5s.** Whether it is the right budget depends on the render mode — read the scoping note under the first one before you trust it on another.

### `seedance-2.0` and `seedance-2.0-mini` — any integer 4 to 15

| Script length | Duration |
|---|---|
| 1–8 words | 4–5s |
| 9–15 words | 6–8s |
| 16–23 words | 9–12s |
| 24–29 words | 13–15s |
| **30+ words** | **Too long** — offer to split |

**Leading silence is mode-dependent, and the two things measured here disagree by seconds. Scope the budget to the mode you are actually rendering — do not add both.**

| What was measured | Leading silence observed | Plan on |
|---|---|---|
| **Reference or start-frame renders** — `referenceAssetIds` or `startImageAssetId` | 0.0s and 0.44s (n=2), then 0.515s, 0.529s and 0.482s (2026-08-11, n=5 total) | **~0.5s.** The tables above already pay it |
| **Six `seedance-2.0` renders whose mode nobody wrote down** (2026-08-02/03) | **3.2–3.7s in `en`**; in `es`, **5.24s, 0.97s and 4.80s on three byte-identical prompts** — same body, same duration, three answers | **+4s `en`, +5s `es`** and any unmeasured language, on top of speech |

**The working rule: budget ~0.5s when you have a reference or a start frame, and check the render.** In that mode the table and the arithmetic already agree — **`2.0 × (D − 0.5)`** is exactly the word cap on every rung from 9 words up, and the 1–8 row is deliberately one word tighter than the formula's 9 at 5s — so there is nothing to add. If the result runs past 15s on these two models, the fix is a shorter line, a split, or `seedance-2.5` — not a longer clip on a model that does not render one.

**When a render does come back with multi-second silence, trim is the remedy, not a bigger budget.** Leading silence is trimmable in post; a line clipped by an over-long draw is not. The reserve in the second row is the *planning* allowance for that mode — reach for it when you have neither a reference nor a start frame, or when you are committing to a duration you cannot re-cut. It costs words: **`words ÷ 2.0` plus the reservation, rounded into the grid, leaves 22 words at 15s in `en` and 20 in `es`, against the table's 29.** That gap is the mode, not a rounding error.

**How close the reserved case gets is not theoretical.** The first `es` render fit only because rounding up took 12.4s to 13s, and the line finished at **12.88s of 13.07s** — a fifth of a second of margin, on a budget that drew near its worst. The silence is drawn fresh every time, in either mode, so **the only thing that tells you what you got is the QA step in §7.** Check the first `silence_end` on every render.

If the hook has to land in the first second, drop the eye-contact-break beat from the prompt — that is the beat being paid for. `sora-2` measured **no leading silence at all** on the same prompt, so it is the other way out.

For no-dialogue styles (product hero, premium reveal), default to **15s**. The silence budget does not apply: there is no speech to delay.

### `seedance-2.5` — any integer 4 to 30

Same family, same craft, twice the room. The table above still holds for anything up to 15s; past
it, keep planning at **2.0 words per second** — the rows below are the same `2.0 × (D − 0.5)`
arithmetic. Nobody has measured 2.5's leading silence separately, so the mode scoping above is the
working rule here too: budget ~0.5s with a reference or start frame, the reserve without one.

| Script length | Duration |
|---|---|
| 30–39 words | 16–20s |
| 40–49 words | 21–25s |
| 50–59 words | 26–30s |
| **60+ words** | **Too long even here** — split, or cut the script |

**A longer clip is not a longer script poured into the same ad.** Thirty seconds wants more beats,
not slower delivery: a second location, a demo the actor actually performs, a reaction. If the
script only fills 15s, render 15s — on `seedance-2.0`, which is cheaper at that length.

**Nobody here has timed a `seedance-2.5` render.** Do not quote `seedance-2.0`'s 3-to-8-minute
fleet range for it; say the wait is unknown and poll.

### `omni-flash` — enum 4, 6, 8, 10

| Script length | Duration |
|---|---|
| 1–8 words | 4s |
| 9–12 words | 6s |
| 13–16 words | 8s |
| 17–20 words | 10s |
| **21+ words** | **Too long** — split, or move to Seedance |

Silence behavior is unmeasured on this model, so this is the 2.0-words-per-second arithmetic and nothing more: the budget is a flat `2.0 × duration`, which assumes no leading silence rather than having found none. Verify against your first render — if it front-loads the way Seedance can, the last line is what gets clipped.

### `sora-2` — enum 4, 8, 12

| Script length | Duration |
|---|---|
| 1–8 words | 4s |
| 9–16 words | 8s |
| 17–24 words | 12s |
| **25+ words** | **Too long** — split, or move to Seedance |

No silence budget: the one measured render spoke continuously from the first frame. The grid is coarse — there is no 6s and no 10s — so a line that lands between two rungs goes **up**, never down.

### `veo-3.1` — enum 4, 6, 8

| Script length | Duration |
|---|---|
| 1–8 words | 4s |
| 9–12 words | 6s |
| 13–16 words | 8s |
| **17+ words** | **Too long** — 8s is this model's ceiling. Split, or move to Seedance |

Unmeasured here, so these are the 2.0-words-per-second arithmetic and nothing more — and with no leading silence to pay for, the budget is a flat `2.0 × duration` rather than the Seedance form. Budget no silence and promise no wait until someone has timed one.

### `resolution`: only where `GET /v1/models` lists more than one tier, and it moves the price

**`seedance-2.0` takes `480p`, `720p`, `1080p`, `4k`; `seedance-2.5` takes `480p` and `720p` and nothing above.** Both default to `720p` (2.0 verified live 2026-08-04 against spec 2.6.0; 2.5 read off deployed spec 2.13.0 on 2026-08-07). It is the one output-shape field that is **not** free — unlike `aspectRatio`, the tiers are separate credit schedules:

| `resolution` | `seedance-2.0` | `seedance-2.5` |
|---|---|---|
| `480p` | **≈half** the base | **≈half** the base |
| `720p` (default) | base | base |
| `1080p` | **≈2.5x** base | **`400` — does not exist on this model** |
| `4k` | **≈5x** base | **`400` — does not exist on this model** |

**`480p` used to cost the same as `720p` and no longer does** (family reprice, 2026-08-07). The old advice here — "no draft discount, so there is no reason to ask for it" — is retired: it is now roughly half, which makes it the honest tier for a rehearsal render whose only job is to check whether the prompt works.

**2.5's missing high tiers are a provider fact, not a rollout gap.** Neither provider serves the model above 720p, so it is not coming. Never carry a `resolution` across a model switch: `1080p` that priced clean on `seedance-2.0` is a rejected request on `seedance-2.5`.

**These are ratios, not a rate card. Never quote a credit number from this table** — it exists so you can warn a user that 4k is a five-fold decision before they ask for it. The number they approve comes from `POST /v1/estimates` on the exact cell, in this session, like every other price here (gate 2).

Ask for what will actually ship. `720p` is right for Reels, TikTok and Stories, where the platform re-encodes anyway; `1080p` and `4k` are for a client deliverable, a placement with a quality floor, or a render you intend to crop into.

**`omni-flash` depends on the server:** `GET /v1/models` lists `360p`, `720p` and `1080p` for it where the server enables them, and `4k` as well where the server publishes that tier (API 2.31.0; never assume it, read the list). Then send `resolution`, default `720p`, and re-quote with `POST /v1/estimates` off it; Omni's tiers are its own schedule, so never carry the Seedance ratios above over to it. Or it lists `720p` alone, and then a body carrying the key is a `400`, `720p` included. From API 2.34.0 `seedance-2.0-mini` and `veo-3.1` list more than one tier too (mini adds `480p`, Veo adds `720p`): send `resolution` there and quote the tier with `POST /v1/estimates`, never with the Seedance ratios. On `veo-3.1` the tier does not move the quote (one flat price), so never offer `720p` as a cheaper option; quote it all the same. **`sora-2` is fixed at 720p and has no `resolution` field**, and sending it the key is a `400`. Read the live set from **`GET /v1/models`** (`resolutions` and `defaultResolution` per model) rather than hardcoding this paragraph.

**The `seedance-2.0-mini` trap, before API 2.34.0 only (from 2.34.0 mini takes the key):** `POST /v1/estimates` accepts `resolution: "720p"` for mini and prices it (identically to omitting it), but answers `400 invalid_input` — *"resolution must be one of 720p for seedance-2.0-mini"* — for `480p`, `1080p` or `4k` (all four verified live 2026-08-04). `POST /v1/videos` does not accept the key for mini **at all**: mini's request variant has no `resolution` property, and a body carrying one was observed returning `400 Unrecognized key: "resolution"` (observed 2026-08-04, not re-verified — re-checking it costs a paid render). **So, against a server whose mini `resolutions` is `["720p"]`, never send `resolution` on a mini call.** An estimate that passed is not evidence the generate call will.

Output size, measured at `9:16`: `seedance-2.0` at its `720p` default and `sora-2` both came back **720x1280** (2026-08-02). `omni-flash` and `veo-3.1` are unmeasured — do not quote a number for them.

### Splitting a long script

1. **Tell the user** the script is too long for one clip and show the word-and-duration math.
2. **Offer two options:** split at natural sentence boundaries into chunks that each fit, or move to the model with more room (**`seedance-2.5` tops out at 30s and is the longest single clip here**; `seedance-2.0` and mini stop at 15). Price both shapes — one 30s call is not automatically cheaper than two 15s ones, and it is a different ad.
3. If they split, each chunk is its own generation call — and the variation count applies to *each* chunk.
4. **Offer to stitch** with ffmpeg: download the segments, `ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4`, re-encoding if the codecs differ. Hand back both the stitched file and the individual segments.

## The full sequence

### 0. Resolve the product (once per session)

`GET /v1/products`. **The products come back under `items`, not `products`** (verified live 2026-08-04) — it is the same paginated envelope as `GET /v1/generations`, so read `.items` and expect `total`, `limit`, `offset` and `hasMore` alongside it:

```bash
curl -sS https://api.novoads.ai/v1/products \
  -H "Authorization: Bearer $NOVOADS_API_KEY" | jq -r '.items[] | "\(.id)  \(.name)"'
```

Default to the product named in `MASTER_CONTEXT.md` under "My workspace". If no default is set: with exactly one product, auto-populate `MASTER_CONTEXT.md` with its id and name; with several, ask the user once and save the choice. With none, omit `productId` — it is optional.

Pass `productId` on every generation call. It is what makes `GET /v1/generations?productId=…` a useful history later. There is no dated-folder ritual to run here: folders are read-only on this API and there are no projects on it at all.

### 1. Upload the reference or start frame (skip if there is none)

```bash
curl -sS -X POST https://api.novoads.ai/v1/uploads \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contentType":"image/jpeg","sizeBytes":248193}'
```

Returns `assetId`, `uploadUrl`, `method`, and `headers`.

Then PUT the raw bytes to `uploadUrl`, sending **exactly** the headers it returned:

```bash
curl -sS -X PUT "$UPLOAD_URL" \
  -H "Content-Type: image/jpeg" \
  -H "Content-Length: 248193" \
  --data-binary @product.jpg
```

Both headers are signed into the URL. `image/jpeg; charset=utf-8` is a 403, and so is a `Content-Length` that does not match the bytes you send. `sizeBytes` must be the real file size, so measure it, do not estimate it.

**Upload once, reuse it forever.** The `assetId` is durable and reusable across calls and across models, which is what makes prototyping on `seedance-2.0-mini` and finalizing on `seedance-2.0` cheap. The presigned *upload URL* expires in 900 seconds; the `assetId` does not.

**Start frame or references, not both.** `startImageAssetId` animates one image as the first frame (on `omni-flash` it is a reference instead, below). `referenceAssetIds` (up to **9** on Seedance, up to its own limit on `omni-flash`, images only; Seedance video and audio references have their own fields, below) composites the images as visual references, addressed positionally in the prompt text as `@Image1`…`@ImageN` in the order you send them. They select different modes on the model, so a body carrying both is a `400`.

**Four models take `referenceAssetIds`**: the three Seedance variants (`seedance-2.0`, `seedance-2.5`, `seedance-2.0-mini`) and, since API 2.30.0, `omni-flash`. `sora-2`, `veo-3.1` and `kling-v3-pro` have no such field and their bodies are strict, so sending it is a `400`. Every video model takes `startImageAssetId`, but **on `omni-flash` it is a reference image the model may place anywhere in the clip, not a first frame**. `omni-flash` also takes one `referenceVideoAssetId` (where the server also publishes `firstFrameAssetId`, the clip's length bounds `durationSeconds`) and, only where the server publishes them, `firstFrameAssetId` (the true first frame), `lastFrameAssetId` (needs a first frame) and `seed`; `startImageAssetId` beside `firstFrameAssetId` is a `400`. Since API 2.35.0 the three Seedance variants also take `referenceVideoAssetIds` (mp4) and `referenceAudioAssetIds` (mp3), not combinable with `startImageAssetId`, capped per kind and in total as the OpenAPI document (`GET /v1/openapi.json`) publishes, and priced the same as without them; see *Seedance video and audio references* in the reference. Read which fields a deployment takes from the OpenAPI document it serves, not the version number, and the full rules under *`omni-flash` inputs* in [reference.md](reference.md).

### 2. Price it (gate 2)

`POST /v1/estimates` with `kind`, `prompt`, `model`, and the duration or image count. See gate 2 above for the exact field list, and remember it rejects any field that does not move the price.

### 3. Confirm the spoken line (gate 1)

See gate 1 above. Both gates must be satisfied, in either order, before anything is submitted.

### 4. Generate

```bash
curl -sS -X POST https://api.novoads.ai/v1/videos \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedance-2.0",
    "prompt": "...",
    "durationSeconds": 12,
    "aspectRatio": "9:16",
    "language": "en",
    "startImageAssetId": "...",
    "productId": "..."
  }'
```

Returns `202` with `jobId`, `status`, `creditsCharged`, and `model`. **No `warnings`** — this endpoint does not run the prompt rules at all. If you want them, they came back on the estimate you already made (gate 2); there is no second chance to collect them here.

**Set `aspectRatio` explicitly.** Seedance defaults to `16:9` and an ad that ships landscape is a wasted render. **Set `durationSeconds` explicitly** too: `seedance-2.0` and `seedance-2.5` default to 5, mini to 10, `omni-flash` to 8, `sora-2` to 4, `veo-3.1` to 8. On `seedance-2.5` that default is 5 of a possible 30 — the long model rendering a short clip at the long model's price.

### `audioEnabled` — the one field that only belongs on a silent clip

`audioEnabled` is a boolean on **the three Seedance variants only** — `seedance-2.0`, `seedance-2.5`, `seedance-2.0-mini`. It defaults to `true`, so omitting it renders exactly what this endpoint rendered before the field existed. `omni-flash`, `sora-2` and `veo-3.1` have no such property and their bodies are strict, so sending it to one of them is a `400`, not a field quietly dropped on the way to a paid render.

**Send `audioEnabled: false` when the clip is meant to be silent** — a pixar or claymation beat that gets its voice-over laid in post, a product cutaway built to run muted. Otherwise the model generates a voice track and sound effects that get thrown away, or worse, an invented narrator over a film that was supposed to be wordless.

**It does not change the price**, which is why `POST /v1/estimates` does not take the field — sending it there is a `400` on an otherwise valid estimate body.

**Keep the silence sentence in the prompt as well.** The prose clause (`a silent product film with no spoken dialogue`) and the flag are belt and suspenders and do different jobs: the flag mutes the render, the clause stops the model from *staging* a talking shot in the first place — an actor mouthing nothing, billed in full. Dropping the clause because you set the flag trades a composition fix for a mute button.

For N variations, fire the identical payload N times. **Five generations per organization may be in flight at once** — fire at most five, then start the next as each one reaches a terminal state. A sixth submission comes back `429` with `error.details.reason` of `concurrency_limit`, which is a different problem from a rate limit and takes a different response: wait for a slot, do not lengthen the backoff.

**Log each submission immediately**: one line appended to `logs/novoads-api.jsonl` with the timestamp, endpoint, model, `jobId`, `productId`, **`creditsCharged` from this `202`**, and the request config (duration, aspectRatio, language, reference counts, prompt **word count**). The charge goes on the line *now* — the poll payload does not carry it, so a line written without it can never be completed. Never log the prompt text, the key, or the Authorization header. The log is observability — latency and spend after the fact. **It is never a pricing source.** Prices come from `/v1/estimates`, always. The file is gitignored: it is the user's session history, not repo content.

### 5. Poll

```bash
curl -sS https://api.novoads.ai/v1/generations/$JOB_ID \
  -H "Authorization: Bearer $NOVOADS_API_KEY"
```

`status` is one of `queued`, `running`, `finalizing`, `succeeded`, `failed`, `blocked`, `canceled`. The last four are terminal. `queued` means charged and submitted but not yet rendering, which is normal and not a stall.

**Poll until TERMINAL, not until `succeeded`.** A loop that waits only for `succeeded` never returns on a job that failed, and the user watches a spinner forever on a render that is already dead.

**Poll every 15 seconds.** Not 5: five concurrent jobs at a 5-second interval is 60 calls a minute, exactly the per-key rate limit, with no headroom left for the calls that do real work.

Tell the user the wait up front, per model, so they do not think it hung — and quote it as a range, never as a promise:

- `seedance-2.0`: fleet range **3 to 8 minutes**, median around 5. **Observed here: ~171s, ~171s, ~154s** on three renders (2026-08-02/03).
- `seedance-2.0-mini`: fleet range **2 to 3 minutes**.
- `seedance-2.5`: nothing published and nothing measured. Say unknown — do not lend it `seedance-2.0`'s range on the strength of the family name.
- `sora-2`: no fleet range published. **Observed here: ~123s** (2026-08-02, n=1).
- `omni-flash`, `veo-3.1`: nothing measured and nothing published. Say the wait is unknown rather than borrowing Seedance's.

**Do not promise five minutes.** The two renders anyone here has actually timed both came back under three, and a user told "about five" who gets it in two is fine, while a user told "about five" who waits nine has been misled. Give the range, name the model, and say the numbers are ranges.

When `status` is `succeeded`, `outputUrl` is a presigned download URL valid for `outputUrlExpiresInSeconds` (3600). Read the job again for a fresh one rather than storing it. Update that job's log line with the terminal status and the elapsed time.

**`creditsCharged` is NOT on this payload — do not go looking for it here.** The poll returns exactly `createdAt`, `error`, `jobId`, `kind`, `model`, `outputUrl`, `outputUrlExpiresInSeconds`, `prompt`, `status` (verified live 2026-08-03). The charge is on the **`202` from the submit**, and that is the only place it is ever available. Carry it forward from the line you already wrote; if it is missing there it is gone, and you never reconstruct it from a rate. The keyed, portable line-update recipe is in `logs/README.md` at the repo root — update by `jobId`, not by position, because up to five jobs are in flight and the line you want is often not the last one.

### 6. Download and hand it over

```bash
OUT_DIR="outputs/seedance-ugc-cerave"      # descriptive, not the job id
mkdir -p "$OUT_DIR"                        # outputs/ is gitignored and absent on a fresh clone
curl -sSL -o "$OUT_DIR/ad.mp4" https://api.novoads.ai/v1/generations/$JOB_ID/watch \
  -H "Authorization: Bearer $NOVOADS_API_KEY"
```

**The `mkdir -p` is not boilerplate.** `outputs/` is gitignored, so it does not exist in a fresh clone, and curl's failure when the directory is missing is `curl: (56) Failure writing output to destination, passed 559 returned 4294967295` — which reads like a broken download of a render that actually succeeded and was already billed. Create the directory first and that whole detour disappears.

`/watch` 302s to a URL signed at request time, so it never hands you an expired link. While the job is unfinished it is a `409` naming the current status.

Save under **`outputs/<descriptive-subfolder>/`** — `outputs/seedance-ugc-cerave/`, not the job id — and name the file for what it is. Then **always open the folder** so the user can review immediately: `open "<dir>"` on macOS, `xdg-open` on Linux, `explorer` on Windows. Try `open` first and fall back silently.

Present multiple variations as a numbered list. If a job came back `failed` or `blocked`, say which, and quote the `error` the job carries.

### 7. Video QA (mandatory)

**Run this on every video before you hand it over.** It costs no credits and takes seconds. A video can be technically `succeeded` and still be undeliverable in ways that no frame and no waveform will show you: the brand name spoken as a different word, a third of the clip spent in silence before the hook, captions burned in, a silent track on an ad that was supposed to talk. Watching it back is not enough either — you will hear what you expect to hear, because you wrote the line.

**The failure this catches is real and it is the expensive one.** On 2026-08-02 a `seedance-2.0` render spoke the approved 17-word line verbatim and pronounced "Novoads" as **"Nuvenov's"**. Every frame looked perfect. Only the transcript caught it.

#### 1. Container, stream and duration

```bash
ffprobe -v error -show_entries format=duration -show_entries stream=codec_type,width,height \
  -of default=noprint_wrappers=1 ad.mp4
```

Check: the duration is the one you paid for, `width`/`height` match the `aspectRatio` you sent (`9:16` comes back 720x1280), and there is an `codec_type=audio` stream at all. **No audio stream on a clip with dialogue means the render is dead** — that is not a QA note, that is a re-render.

#### 2. Levels and silence

```bash
ffmpeg -i ad.mp4 -map 0:a -af volumedetect -f null -
ffmpeg -i ad.mp4 -map 0:a -af silencedetect=noise=-35dB:d=0.3 -f null -
```

> **Do NOT add `-v error` to these two.** Both filters print their findings at ffmpeg's `info` level, so `-v error` suppresses the entire result and the command exits `0` having told you nothing. It looks exactly like a clean pass. This is the single easiest way to run video QA and learn nothing from it — verified 2026-08-02: with `-v error` the silencedetect call printed no output at all on a clip carrying 3.7s of leading silence.
>
> `ffprobe` in step 1 is the opposite case: `-v error` there is correct, because `-show_entries` writes to stdout.

Check `mean_volume` is not near-silent (the renders measured here came back −19 to −25 dB), and read the **first `silence_end`** — that is when the first word actually lands. Compare it against the silence budget in *Script length → duration*: on Seedance expect **3–4s in `en`**, and anywhere from 1s to 5s in `es`, drawn fresh each render. Much more than that on a short ad means the hook is gone.

#### 3. Transcribe — the only check that hears the brand name

> Doctrine: [shared/references/craft.md](../../shared/references/craft.md) § 1. The commands
> below are this surface's; the rule is not this skill's.

```bash
ffmpeg -y -v error -i ad.mp4 -ar 16000 -ac 1 -c:a pcm_s16le /tmp/ad-qa.wav
```

Then transcribe `/tmp/ad-qa.wav` with whichever Whisper the machine has — the same one `analyze-video` and `clone-video-ad` use:

```bash
whisper /tmp/ad-qa.wav --model base --output_format txt --output_dir /tmp   # openai-whisper
whisper-cli -m <path/to/ggml-medium.bin> -f /tmp/ad-qa.wav -l en --no-prints  # whisper-cpp
```

Read the transcript against the line the user approved at gate 1, and check three things:

- **The brand name came out as the brand name.** This is the whole reason the step exists. If it did not, the fix is the phonetic spelling in gate 1 — not a re-roll of the same prompt.
- **The words are the approved words.** A dropped or invented clause means the render does not match what was signed off.
- **`language` matches** what was rendered.

#### What to do when QA fails

Say which check failed and show the evidence — the transcript line, the silence figure, the missing stream. Then:

- **A mispronounced invented brand name** → re-render with the phonetic spelling for that language (gate 1): `NO-vo-ads` in `en`, `Novo Ads` in `es`. A prompt fix with a validated result on `seedance-2.0`, not a gamble.
- **A stutter — a clause spoken twice.** Seen once in three `es` renders of the same payload. Re-render the **identical** body: the defect is nondeterministic delivery, not a prompt fault, so re-sampling the same cell is the right move. This is the one exception to "never resend an identical payload", which is about prompt-caused image defects. It still costs credits, so it still goes through gate 2.
- **Leading silence eating the hook** → re-render shorter, or drop the eye-contact-break beat, or move to `sora-2`, which measured none.
- **No audio stream, or a silent track on a talking ad** → re-render. Nothing in the prompt fixes a dead track.
- **Burned-in captions** → the clean-plate clause is missing from the prompt. Add it and re-render.

**Every re-render is a new charge**, and unlike image QA there is no automatic-retry allowance here: a video re-render goes back through gate 2. Show the QA finding, show a fresh estimate, and get a yes.

## Burned-in captions: `POST /v1/captions`

**This API has a first-party captioning endpoint** (verified live 2026-08-04 against spec 2.6.0). It was undocumented in this pack, and the decision tree used to send every caption request to the local ffmpeg skill as though no endpoint existed. Both paths are real — see *Which caption path* below.

**What it does:** takes a video, transcribes its own audio, burns styled subtitles into it, and gives you back **a new MP4**. Asynchronous, exactly like `POST /v1/videos`.

**What it does not do: THIS endpoint never returns caption text, timings, or an SRT.** There is no transcript field anywhere on a caption job — `GET /v1/generations/{jobId}` carries `outputUrl` and nothing else about the words. That is still true and is not a bug to file.

**But the API as a whole does return the words now.** `POST /v1/transcripts` gives you text, word-level timings and an SRT in one synchronous call, on the base video, with no local install — see *POST /v1/transcripts* in [reference.md](reference.md). So "the user wants an SRT" is no longer a reason to leave the API; wanting to **edit the wording before rendering**, or wanting a style outside the 30 presets, still is.

**There is nothing to write.** The text is transcribed from the audio. Your only choice is `preset`.

### The call

```bash
curl -sS -X POST https://api.novoads.ai/v1/captions \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jobId":"<a succeeded video job>","preset":"casper"}'
```

| Field | Notes |
|---|---|
| `jobId` | A video **this API generated**, via `POST /v1/videos`. |
| `assetId` | A video **you uploaded**, via `POST /v1/uploads`. Must be a video, not a still. |
| `preset` | **Required, no default.** One of 30 styles — the tiers are priced differently, so nothing could be a safe default. |

**Exactly one of `jobId` and `assetId`.** Sending both is a `400`, not a guess — captioning the wrong one of two sources still bills you.

`POST /v1/videos/{jobId}/captions` is the same operation with the source in the path. It is the natural call when the source is a job, and it cannot express the upload case at all (an `assetId` contains slashes and is not a path segment). Either one is fine; prefer `POST /v1/captions` if you want one code path for both sources.

Response is `202` with `jobId`, `status`, `creditsCharged`, and `model` (always `captions-v1` — this endpoint has one renderer and it is not in `GET /v1/models`, because a caption is applied to a video rather than generating one). **Poll the returned `jobId` at `GET /v1/generations/{jobId}` to a terminal status, then `…/watch` for the file** — the same sequence as a render, and the caption job is a separate row with its own status and its own refund.

### Presets and price

`GET /v1/caption-presets` lists all **30** styles, each carrying its own `tier` and its own rate. There are two tiers: `basic`, and the costlier `dynamic` (context-aware and animated). **Read the rate off that endpoint and confirm it with the caption arm of `POST /v1/estimates`** — a rate written into this file is a rate that rots, and the one you quote the user must be the one the API just gave you. Its own endpoint rather than a `kind` on `GET /v1/models`, because a caption style generates nothing.

**Billing is per minute of source, rounded up, one-minute minimum** — so everything this API generates (≤30s, on `seedance-2.5`; ≤15s everywhere else) bills exactly one minute at the tier rate. Above the 1080p tier it doubles again, **measured on the short edge**: an ordinary portrait `1080x1920` is 1080p held sideways and is **not** doubled; a true 4K source is, and an `omni-flash` render at `4k` (where `GET /v1/models` lists it) is one, so captioning it bills doubled. Quote it from the caption arm of the estimate, never from this line.

Duration and resolution are read from the file itself at request time, not from anything you declare. **Gate 2 still applies** — price it with the caption arm of the estimate, which charges nothing:

```bash
curl -sS -X POST https://api.novoads.ai/v1/estimates \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"kind":"caption","preset":"casper","jobId":"<source job>"}'
```

**Name the source in the estimate for anything longer than a minute.** A quote without `jobId`/`assetId` is the one-minute minimum, and a 10-minute upload costs ten times it. (Verified live 2026-08-04: sourceless `casper` quoted 0.4, sourceless `glass` quoted 0.8. As always, the number you show the user is the one that came back, not one from this page.) A caption estimate has no prompt, so it returns no `warnings`.

### What bites

- **`409`** — the source job has not succeeded yet, **or it was rendered with `audioEnabled: false`**. No speech, nothing to transcribe, and the API refuses rather than charging you for an empty result. Silent b-roll cannot be captioned.
- **`404`** — a `jobId` from the *dashboard* rather than the API answers 404, identically to one that does not exist. So does an asset outside your organization or an incomplete upload.
- **`400`** — a still passed as `assetId`, both source fields at once, or a file that cannot be measured. **A source we cannot measure charges nothing**, because a file we cannot price is one we cannot bill.
- **Re-captioning the same video in the same style is safe and free.** The second call returns the *first* job's id and charges nothing. A **different** preset on the same video is a new job and a new charge — so iterating on style costs money each time; pick with the user before you call.
- **`429` with `details.reason: caption_concurrency_limit`** — 10 concurrent caption jobs, counted **separately** from the 5-generation render ceiling, so a batch of captions can never block your next render.

### Which caption path — the API or the local skill

Both exist. Present both and let the user pick; do not silently default.

| | `POST /v1/captions` | the `caption-video` skill |
|---|---|---|
| Cost | **Costs credits** (gate 2 applies) | **Free** |
| Setup | None — one API call | **Heavy**: Whisper, HyperFrames, a working Node/npm project, and an ffmpeg alpha composite. Homebrew ffmpeg ships without `libass`, which is the trap the local guide exists to route around |
| Styles | **30 presets**, fixed | Anything you can write in HTML/CSS/GSAP |
| Output | A new MP4, subtitles burned in | A new MP4, subtitles burned in |
| Transcript / SRT | **Not from this endpoint** — but `POST /v1/transcripts` returns text, word timings and an SRT, billed per minute of source and priced through `POST /v1/estimates`, no install | **Yes** — Whisper gives word-level timings you keep and can re-use |
| Control over wording | None — transcribed, not authored | Full — edit the transcript before rendering |
| Source | An API `jobId`, or any video you upload | Any local file |

**Rules of thumb.** One finished clip, a standard look, no local toolchain → the API. A caption style outside the 30, hand-corrected wording (invented brand names are the usual reason), a needed SRT, or a batch big enough that per-minute credits add up → the local skill. If the video was rendered with `audioEnabled: false`, the API cannot caption it at all.

## Images come back in the response, or answer `running`

`POST /v1/images` usually returns the finished images in the response body (`status: "succeeded"`). **Since API 2.39.0 a render still going after about 105 seconds answers `200` with `status: "running"`, the same `jobId` and `images: []`.** That is a paid render in progress, not a failure: never resubmit it. Poll `GET /v1/generations/{jobId}` every 15 seconds to a terminal status; on `succeeded` the job carries `images[]` in order, the same entries the response would have carried, and on `failed` or `blocked` the credits are refunded. Log `creditsCharged` from the first response. There is no `/watch` step for images. The response carries `images[]` with `url`, `expiresInSeconds`, `assetId`, `width`, and `height`, plus `jobId`, `status`, `model`, and `creditsCharged`. **Chain downstream calls from `assetId`, not from `url`** — the URL is a one-hour presign and nothing downstream accepts it. No `warnings` here either. The prompt rules run on `POST /v1/estimates` only — and an image estimate does return them, from rules written for images: `banned_polish` and `blank_label` observed live on deployed spec 2.19.0 (verified 2026-08-12). The older claim here, that an image estimate came back with no `warnings` key at all, described the 2026-08-04 deployment. Read and judge them like the video ones; they are advisory and cannot refuse or reprice anything, so the image prompt libraries are still the real check.

- `referenceAssetIds`: images only, order preserved and addressable positionally by the prompt. Upload each one first — there is no base64 field. **The cap is per model, not one number:** `nano-banana-pro` takes up to **14**, `reve-2.1` up to **8**, `gpt-image-2` up to **4**, and `seedream-5-lite` and `seedream-5-pro` (API 2.39.0) up to **10**; Seedream has no `quality`, `resolution` or `outputFormat`, and its aspect ratios come from `GET /v1/models`. The bodies are strict, so a fifth reference to `gpt-image-2` is a `400`, not a silently dropped image — which is the good outcome, because a dropped reference is a paid render missing the product.
- `numImages`: 1 to 4, and it multiplies the price. `quality` (`high`, `medium`, `low`; default `medium`) and `outputFormat` (`png`, `jpeg`, `webp`; default `png`) on the GPT Image models, `resolution` (`1K`, `2K`, `4K`; default `2K`) on `nano-banana-pro` (API 2.36.0). `quality` and `resolution` move the price: quote the exact cell with `POST /v1/estimates` using the same fields. Read the model's lists from `GET /v1/models`; image `resolution` is matched exactly, so `4k` is a `400`.
- Images take **no `startImageAssetId`**: there is no first-frame concept on a still. A `preset` takes its one photo as `imageAssetId` instead (API 2.40.0, decision tree above).

### Image QA (mandatory)

Images are money already spent, and a defective still is not a deliverable. After each image comes back, **look at it**.

Look for: extra or missing hands or fingers, wrong limb count, distorted or duplicated or merged facial features, melted or fused objects, impossible anatomy, stray limbs, texture and boundary artifacts, and garbled text where text was requested.

If something is wrong, **regenerate with a corrected prompt** that names the defect ("exactly two hands, five fingers each", "a single face, no duplicated features"). Never resend the identical payload expecting a different result.

- **Cap: 2 regenerations per originally requested image**, 3 attempts total. After the cap, stop, show the best attempt, say what still looks wrong, and ask how they want to proceed.
- **No second cost confirmation.** Once the batch is approved, QA retries proceed automatically — the one exception to gate 2.
- **Every retry is billed.** Sum the extra credits and report them when the loop ends.

## The `references/` folder

Check it before asking the user for anything. `references/influencers/` for people, `references/products/` for products, `references/aesthetics/` for style and mood. If a relevant file is already there, offer to use it instead of asking.

### It ships empty. Do not stall on it.

`references/` is gitignored, so on a fresh clone it holds nothing but empty folders. That is the expected state, and **"go find me a photo" is the wrong first move for most requests.** Ask what they are advertising first, then decide whether a photo is needed at all:

| What they are advertising | Does it need a reference? |
|---|---|
| **Software, an app, a SaaS product, a service, a course, an agency** | **No.** There is no physical object to hold. The actor talks to camera and the product never appears — this is the single most common ad shape and it needs nothing in `references/`. Route it and go. |
| A physical product the user sells | **Yes, and it is worth waiting for.** Ask for one photo, put it in `references/products/`, pass it as `startImageAssetId` or in `referenceAssetIds`. Do not invent packaging: the model will render a plausible fake label and charge you for it. |
| A specific person's likeness | **Yes.** `references/influencers/`. Without it Seedance re-casts on every render. |
| A look, a palette, a lighting mood | Optional. A style board sharpens it; prose can carry it. |

**Never substitute a blank or generic product for one the user has not given you.** If they are advertising something physical and have no photo to hand, say what you cannot do rather than rendering a nameless bottle. Nothing on the API will warn you, and the charge lands either way.

Before uploading a reference, if its longest side is under 1024 px, upscale with Lanczos to 1080 px on the long side and re-encode as RGB JPEG at quality 90–95, which strips alpha and keeps the payload sane. (No minimum input size is documented for this API — the practice carries over from a sibling API that answered small images with a 422, and is unverified here.)

## Errors: branch on `error.code`, never on the message

Every error is `{"error":{"code":..., "message":..., "requestId":..., "details":...}}`. Quote `requestId` when reporting a problem; it matches the `x-request-id` response header.

| Status | `code` | What it means | What to do |
|---|---|---|---|
| 400 | `invalid_input` | **The request is malformed** — an unknown key, an out-of-grid `durationSeconds`, a prompt over the model's ceiling. `details.issues` names each bad field. Never a judgement on the writing. | Fix the field. Nothing was charged. |
| 401 | `unauthorized` | Missing, malformed, or revoked key. | Send the user to <https://novoads.ai/dashboard/settings?tab=api> to create a new one. |
| 402 | `insufficient_credits` | `details` carries `required` and `available`. | Tell the user the gap. Do not retry. |
| 403 | `forbidden` | `details.reason` is `plan_required`, `subscription_inactive`, or the API is off for that account. | Say which. These are different fixes. |
| 404 | `not_found` | No such object **for this organization**. | Do not assume it exists elsewhere. |
| 409 | `conflict` | Includes `/watch` on an unfinished job. | Keep polling. |
| 422 | `content_policy` | Moderation blocked it, and this is the **only** way a prompt is refused for what it says. The estimate skips moderation, so it can land on a prompt the estimate priced clean. | Nothing was charged. Rewrite or stop. |
| 429 | `rate_limited` | **Four different causes.** Branch on `details.reason`. | See below. |
| 500 | `internal_error` | | **Do not blindly retry.** See below. |
| 502 | `provider_failed` | A model provider failed. | Credits are refunded automatically. |

**The 400 vs 422 line is simple now, and worth stating because it used to be blurred.** A `400` is a malformed request and nothing else. A `422` is moderation and nothing else. Prompt craft — a missing actor descriptor, no spoken line, a forbidden word — produces no status at all: the API neither refuses it nor mentions it. Do not write a retry loop that expects a rule to stop a bad prompt; the only thing that stops it is you, before you send it.

**A 429 is not always a rate limit.** `details.reason` names which of four ceilings refused you, and they are paced differently:

- `concurrency_limit` — five generations already in flight for the organization (`details.inFlight` says how many). **Waiting is the only fix**: a longer backoff does nothing, a finished job does. Generation endpoints only; reads, estimates, and uploads never hit it.
- `key_limit` — 60 requests a minute on this key. The `X-RateLimit-*` headers track this one. Honor `Retry-After`.
- `organization_limit` — 180 a minute across every key the organization holds. `X-RateLimit-*` will still show room on your key; that is correct, not a broken limiter. Minting another key does not raise it.
- `client_limit` — 1,200 a minute pre-authentication. Carries no `X-RateLimit-*` trio.

Every 429 carries `details.reason` and a `Retry-After` header — sleep on the header, branch on the reason. `details.inFlight` (concurrency refusals) is the only other key the spec names; do not expect one it does not.

**On a 500, do not retry until you have checked.** The generation endpoints charge credits, and a failure can land after the debit committed, so a blind retry can pay twice. Call `GET /v1/generations` first. If the job is there, poll it instead of resubmitting. There are no idempotency keys.

## Guardrails

Append one line per new failure. Forward only. Every bullet is a real thing that went wrong.

- Never write a credit number into a file, a summary, or `MASTER_CONTEXT.md`. Prices come from `/v1/estimates` at call time.
- Never generate without both gates: the spoken line, and the cost.
- Always set `aspectRatio`. The Seedance default is `16:9`.
- Always set `durationSeconds`. `seedance-2.0` and `seedance-2.5` default to 5, mini to 10, `omni-flash` to 8.
- Only `seedance-2.5` renders past 15s (4–30). Asking any other model for 20 is a `400`, never a rounded-down render.
- `seedance-2.5` has no `1080p` and no `4k`. Do not carry a resolution across a model switch.
- `Content-Type` on the presigned PUT must match byte for byte. Adding `; charset=utf-8` is a 403.
- Never resubmit after a 500 without checking `GET /v1/generations` first.
- A 400 is a malformed request. Read `details.issues`, fix the field, and do not go looking for a prompt rule — none of them can 400 anymore. Never send `styleFamily`: the field no longer exists on this API and any body carrying it is a 400.
- Prompt rules exist **only** on `POST /v1/estimates`, as the advisory `warnings` array, and they cannot refuse or reprice anything. **Nothing on the API will stop a weak prompt from being rendered and billed**, so the prompt libraries are still the quality gate. Read every warning, judge it against your prompt (they false-positive — see gate 2), and never apply a suggested fix without checking it fits.
- Never fire more than five generations at once, and poll at 15 seconds, not 5. A QA retry still costs credits: cap at 2, and report the extras.
- **Never hand over a video you have not QA'd.** §7 is free and it is the only thing that hears the brand name. A render that looks perfect frame by frame can still say the wrong word.
- **Never put `-v error` on the `volumedetect` or `silencedetect` calls.** It suppresses the results and the check reports nothing while looking like it passed.
- Spell invented brand names phonetically inside the quoted line, and re-run gate 1 when you do — the words changed.
- `audioEnabled` exists on the three Seedance variants and `kling-v3-pro`. Sending it to `omni-flash`, `sora-2` or `veo-3.1` is a 400, and sending it to `/v1/estimates` is a 400 on any model.
- Image `referenceAssetIds` caps are per model: 14 on `nano-banana-pro`, 8 on `reve-2.1`, 4 on `gpt-image-2`, 10 on each Seedream 5 model. There is no single number.
- Real brands only in prompts. Do not substitute a blank bottle for a product the user has not given you — the API will happily render it and charge for it, and nothing will tell you. Ask for the photo.

## References

- [reference.md](reference.md) — every endpoint, field, limit, and error, plus the dated discrepancy list.
- [prompting/prompt-library/seedance-2-ugc.md](prompting/prompt-library/seedance-2-ugc.md) — the UGC prompt formula, with a worked example that passes validation.
- [prompting/guide.md](prompting/guide.md) — marketing brief → API.
- [prompting/brand-voice-starter.md](prompting/brand-voice-starter.md) — template to copy into `MASTER_CONTEXT.md`.
- The other Seedance formulas: [seedance-2.md](prompting/prompt-library/seedance-2.md) (platform guide), [premium reveal](prompting/prompt-library/seedance-2-premium-reveal.md), [product hero](prompting/prompt-library/seedance-2-product-hero.md), [studio lookbook](prompting/prompt-library/seedance-2-studio-lookbook.md), [feature walkthrough](prompting/prompt-library/seedance-2-feature-walkthrough.md).
- The other video models: [sora-2.md](prompting/prompt-library/sora-2.md), [veo-3-1.md](prompting/prompt-library/veo-3-1.md). [kling-3.md](prompting/prompt-library/kling-3.md) is vendor prompt craft for `kling-v3-pro`; the request body comes from [reference.md](reference.md#kling-v3-pro-api-2380).
- Image and character craft: [ugc-selfie-style.md](prompting/prompt-library/ugc-selfie-style.md), [ugc-product-selfie.md](prompting/prompt-library/ugc-product-selfie.md), [product-showcase.md](prompting/prompt-library/product-showcase.md), [influencer-recreation.md](prompting/prompt-library/influencer-recreation.md), [character-sheet.md](prompting/prompt-library/character-sheet.md), [character-sheet-gpt-image-2.md](prompting/prompt-library/character-sheet-gpt-image-2.md), [nano-banana.md](prompting/prompt-library/nano-banana.md).
- <https://api.novoads.ai/v1/openapi.json> — the spec itself, which is the authority when this file and it disagree.
