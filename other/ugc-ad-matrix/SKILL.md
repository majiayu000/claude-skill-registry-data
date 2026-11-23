---
name: ugc-ad-matrix
description: "Performance-ad editor for UGC (creator-style) ads: builds a test matrix of 3-5 hook variants x one body x one or two CTAs, cut native to TikTok/Reels (selfie framing, platform-style captions, fast 1-2.5 s shots), and renders every combination in 9:16, 4:5 and 1:1 with captioned, clean and raw Spark/Partnership versions. Use when the user says: make UGC ads, test hooks, ad variations, creative testing, cut my creator footage into ads, TikTok ad, Meta ad, hook matrix, Spark ads. Real customers/creators only; paid partnerships disclosed. Default skin ugc-ad-kit."
license: MIT
---

# UGC Ad Matrix

One body, many hooks: an editor's test matrix of native-looking UGC ads, every ratio, every version.

- **Best for:** creator / customer selfie ads, app installs, DTC products, lead gen
- **Inputs:** separate takes for each hook (`hook1.mp4`...), the body (`body.mp4`), CTA take(s), product B-roll (optional), the offer text
- **Default skin:** `ugc-ad-kit` · alternatives `split-proof`, `before-after`, `bold-bounce`
- **Formats:** 9:16 1080x1920 master; 4:5 and 1:1; captioned + clean + raw (no graphics) for Spark / Partnership ads
- **Duration target:** 15-30 s (9-15 s cutdowns); genre preset `ugc-ad-matrix`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre ugc-ad-matrix`.
- The `--genre` preset sets autocut's pause cut (0.25 s) and run.py respects it; pass `--max-gap` only to override.
- **Ethics:** the person on camera must be a real customer or a disclosed paid creator. Never present an actor as a customer, never invent ratings or results. Paid content gets an "Ad" / "Paid partnership" label (FTC / ASCI). Ask the user what claims are approved.

## How a pro cuts this

| beat | % (of 20-30 s) | what happens |
| --- | --- | --- |
| hook (variant) | 0-12 | thumb-stop in 1-1.5 s: problem, bold claim, result shown first, "POV", reaction |
| problem | 12-25 | the pain in the viewer's words |
| demo | 25-60 | product in hand, doing the thing; close-ups, B-roll every 1.5-2 s |
| proof | 60-80 | real result, real review, before/after (only if true) |
| offer + CTA | 80-100 | offer on screen, one CTA, product visible |

- **The matrix:** 3-5 hooks x 1 body x 1-2 CTAs = 3-10 ads. Hooks differ in *angle* (pain, result, curiosity, social proof), not just wording. Everything after the hook is identical so the test is fair.
- **Pacing:** ASL 1-2.5 s, a change at least every 2 s. Hook lands by 1.5 s with text on screen (most plays start muted).
- **Cut rules:** tight jump cuts are native here; remove every breath between sentences in the hook, keep a natural feel in the body. Keep it looking like a phone video: no cinematic grade, no letterbox.
- **Transitions:** hard cuts and zoom punches only. A whoosh at most once.
- **Music/SFX:** a light trending-style bed 22-26 LU under, ducked; pop / ding on the offer. Licensed music only (platform libraries for Spark).
- **Colour:** correct only; `clean-commercial` <= 0.4. True product colour matters.
- **Captions:** preset `boxed` or `hormozi`, 2-3 words, <= 15 cps, inside the ad safe zone (top 14 %, bottom 35 % on Meta Reels ads - keep key text in the middle band).
- **Client judges:** thumb-stop rate (3 s views), hold to 50 %, CTR, CPA - per hook.
- **Common mistakes:** hooks that are all the same angle, a logo first, text under the CTA button area, fake "customer" voices, offer not on screen, a body edited differently per variant (ruins the test).

## Make the edit

Cut the shared body once and look at it:

```bash
python CORE/scripts/run.py body.mp4 --style SKILLS/ugc-ad-kit --genre ugc-ad-matrix --smart-cuts --retakes \
  --work ad-body --stop-after cut
```

Write one timeline spec per hook (times in source seconds, from each take's transcript or by eye), e.g. `ad-h1.json`:

```json
{"format": "9:16", "fps": 30,
 "clips": [{"src": "hook1.mp4", "in": 0.4, "out": 2.6},
           {"src": "body.mp4", "in": 1.1, "out": 19.8},
           {"src": "cta.mp4", "in": 0.2, "out": 3.4}]}
```

Then render each variant in its own work folder (same skin, same body times):

```bash
python CORE/scripts/run.py - --timeline ad-h1.json --style SKILLS/ugc-ad-kit --genre ugc-ad-matrix \
  --smart-cuts --work ad-h1 --stop-after plan
python CORE/scripts/editor.py review ad-h1/plan.json --genre ugc-ad-matrix --fix
python CORE/scripts/render.py ad-h1/plan.json --frames 0.5,1.5,6,14
python CORE/scripts/render.py ad-h1/plan.json
python CORE/scripts/finish.py ad-h1/plan.json --platform tiktok --formats 4:5,1:1
# repeat for ad-h2 ... ad-h5; copy the refined body elements from ad-h1/plan.json (shift times by the hook length difference)
```

Product B-roll: add `--broll broll/` (name files after what they show: `serum-dropper.mp4`).

## Refine the plan

- **Hook text:** <= 6 words on screen from 0.0 s ("I stopped using razors"). Different text per variant; same position and size.
- **Captions:** `{"type": "captions", "preset": "boxed", "cpsMax": 15, "dodgeFace": true}`.
- **Native UI moments:** `notification` (`"app": "Bank", "title": "Refund received"` only if true), `searchbar`, `chat` with real messages the user supplies, `socialpost` as a generic card (never imitate a real platform or person).
- **Proof:** `compare` with real before/after photos, `stars` only for real reviews the user gives you, a `quote` with the reviewer's real words.
- **Offer:** a `card` or `tile` with the price/offer 2-3 s before the end; `"sfx": [{"t": 21.0, "kind": "cash-register", "gain": 0.4}]`.
- **Disclosure:** `{"type": "chip", "text": "Paid partnership", "start": 0, "end": 3, "x": 120, "y": 230, "anchor": "top-left"}` when paid.
- **Raw Spark version:** copy the plan, remove every element except captions (or all), `"outputFile": "ad-h1_raw.mp4"`.
- **Colour/sound:** `"color": {"look": "clean-commercial", "intensity": 0.35}`, `"music": {"src": "bed.mp3", "under": 24, "duck": true}`.

## Deliver

```bash
python CORE/scripts/deliver.py ad-h1/plan.json --to tiktok,reels,facebook --out-dir ad-h1/deliver --no-post
python CORE/scripts/qc.py ad-h1/deliver/final_tiktok.mp4 --plan ad-h1/plan.json --platform tiktok --strict
```

- Name every file by the matrix cell: `brand_ugc_h1-pain_b1_c1_9x16_captions.mp4`, `..._clean.mp4`, `..._raw.mp4`.
- Write a `matrix.md`: hook text, angle, length, file names per cell, so the media buyer can map results back.
- `finish.py --formats 4:5,1:1` gives the extra ratios; check each on a contact sheet (re-render at that format if text crops).

## Check before delivering

- Hook text on screen by 0.5 s and spoken/shown by 1.5 s in every variant; body identical across variants.
- Real person, real words, real results; disclosure on paid ads; claims approved by the client.
- Key text and offer inside the safe band of every ratio; product visible at the CTA.
- `qc.py` passes for each file (-14 LUFS, -1 dBTP, length within platform limits).
- Tell the user: the matrix table, which hook you expect to win and why, every file path.

## Example requests

- "Make 5 UGC ads from these takes - one body, five different hooks, 9:16 and 4:5."
- "Cut my creator footage into TikTok ads with captions plus raw versions for Spark."
- "Hook test: pain hook vs result hook vs curiosity hook, same body and CTA."
