---
name: ad-ladder
description: "Ad ladder editor for Claude: turns one commercial shoot (talent takes, product shots, supers, a licensed track) into a full ad package - a 60 s or 30 s story master, a 15 s cutdown and a rebuilt 6 s bumper, each frame-exact, in 16:9, 1:1, 4:5 and 9:16, captioned and textless, mixed to platform or broadcast loudness. Use when the user says 'cut a 30 and a 15', 'make ad cutdowns', 'we need a 6 second bumper', 'versions for every placement', 'TV spot and social versions', 'ad package', or hands over a commercial shoot with a script. Runs on video-studio-core (selects, story, timeline, colour, mix, deliver, QC)."
license: MIT
---

# Ad Ladder

One idea, told at every length: the 30 sells the story, the 15 sells the benefit, the 6 sells the brand.

- **Best for:** TV and online commercials, paid social campaigns, YouTube pre-roll and bumpers, product launches
- **Inputs:** script/board, talent and product takes, logo PNG, legal supers text, brand colours/fonts, licensed music
- **Default skin:** `kinetic-launch` · alternatives `product-spotlight`, `minimal-mono`, `ugc-ad-kit` (selfie-style ads)
- **Formats:** 16:9 master; 1:1, 4:5 and 9:16 versions of every length
- **Durations (frame-exact):** 60 s, 30 s, 15 s, 6 s bumper (YouTube bumpers are non-skippable and max 6 s)
- **Genre preset:** `--genre ad-ladder` (`python CORE/scripts/editor.py genre ad-ladder`)

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run on a machine: `python CORE/scripts/check_env.py` and fix what it reports.
- Ask for: the single-minded proposition, the mandatory supers (legal lines, offer terms, URL), where each version
  runs (TV, YouTube, Meta, TikTok), the music licence terms (lengths and territories), and the brand guide.
- Claims, prices and offers come only from the client's approved script. Never invent a price, a rating or a result.

## How a pro cuts this

**The ladder is rebuilt, not trimmed.** Each length has its own structure. Cutting the 30 down to 6 by trimming gives a
bumper with no idea in it; build the 6 around one image, one line and the logo.

| length | structure | rule of thumb |
| --- | --- | --- |
| 60 s | hook 0-3 s → situation → tension → product as the turn → proof → offer → logo + CTA | room for a mini-story and a second proof beat |
| 30 s | hook 0-2 s → problem → product → benefit shown → offer/CTA → logo (last 3-4 s) | one story, one proof |
| 15 s | hook 0-1.5 s → benefit shown → product → logo + CTA (last 3 s) | drop the setup, keep the payoff |
| 6 s | one striking image → product/benefit line → logo | one idea; brand visible by 2 s, logo on screen ≥ 1.5 s |

**Pacing.** ASL 1-2.5 s; a visual change every ~2 s; the 6 s holds 2-4 shots. Product and logo shots get the longest
holds. Brand visible early (within the first 5 s of a 30, 2 s of a 6) for skippable placements.

**Cut rules.** Cut on action and motion; match cuts between product moments; smash cut into the reveal. Picture leads,
VO follows: J-cut voice under the incoming shot by 2-4 frames. No dead frames at the head or tail.

**Frame-exact lengths.** A 30 is 30.00 s (900 frames at 30 fps), not 29.7 or 30.4. Check each output with `qc.py`
(duration row) and fix by adjusting the last shot, never by speeding the whole spot.

**Supers (legal text).** Readable: hold at least 3 s plus 1 s per extra line (about 15 cps), inside title-safe,
contrast against the footage. A super that flashes by fails legal review.

**Music and sound.** Track leads (bed about -18 dB, ducked about 8 dB under VO); every length ends on a resolved bar
(`music_fit.py` per length, `"endButton": true`). Logo sting or a soft hit on the logo; whooshes only on real motion.

**Colour.** Product true to its real colour first (match to a reference frame of the product), then a light look:
`clean-commercial`, `food-pop` (food), `cool-corporate` (tech), intensity 0.4-0.6. Skin protected.

**Captions.** Social versions get burned-in captions (`"preset": "clean"` or the skin's style), ≤ 15 cps;
TV versions get none on picture and a separate caption file.

**What the client judges.** Product looks right, logo time, legal supers readable, every version delivered at the exact
length and spec, the message survives in the 6 s.

**Common mistakes.** Bumper trimmed from the 30; logo appearing in the last 0.5 s only; supers too short to read; spots
a few frames long or short; music cut mid-phrase; vertical versions with the product cropped off.

## Make the edit

```bash
# 1. selects from the shoot (takes, retakes, best performance)
python CORE/scripts/selects.py --work sel --input shoot.mp4
#    tick paper_edit.md, then build the 30 s master first
python CORE/scripts/selects.py --work sel --apply --format 16:9
python CORE/scripts/run.py - --timeline sel/selects_spec.json --style SKILLS/kinetic-launch --genre ad-ladder --format 16:9 --no-cut --music track.wav --logo logo.png --duration 30 --work ad30 --stop-after plan
python CORE/scripts/editor.py review ad30/plan.json --genre ad-ladder --fix
python CORE/scripts/render.py ad30/plan.json --frames 0.5,5,12,20,27,29.5
python CORE/scripts/render.py ad30/plan.json
python CORE/scripts/finish.py ad30/plan.json --platform youtube
```

**Each other length** gets its own paper edit and work folder. Re-order the shoot for the length with
`story.py outline --work sel` / `story.py reorder --work sel --order "..." --format 16:9 --out ad15.json` (or write a
`timeline.py` spec by hand: see `CORE/references/timeline.md`), then the same run with `--duration 15` / `--duration 6`.
Cut music to each length on the beat grid:

```bash
python CORE/scripts/music_fit.py track.wav --duration 15 --out track_15.wav
python CORE/scripts/music_fit.py track.wav --duration 6 --out track_06.wav
```

**Aspect versions:** build a vertical master per length with `--format 9:16` (re-frame each shot with
`"reframe": "face"` in the timeline spec, or check product framing by hand), or let `deliver.py` reframe the 16:9.
Always check the product and logo are still in frame in the 9:16 and 4:5 contact sheets.

**Textless:** copy `plan.json` to `plan_textless.json`, delete every text/captions/card element (keep the picture and
mix), render to a separate composite and finish with `--out ad30_textless.mp4`.

## Refine the plan

- **Hook:** first shot is the strongest image, no logo slate. Set the `hook` text element (≤ 6 words) or remove it if
  the picture carries the hook.
- **Supers:** `{"type": "text", "text": "Offer valid till 31 Dec. T&Cs apply.", "start": 25.5, "end": 29.9, "y": "=H*0.88", "w": "=W*0.8", "style": {"fontSize": "30px"}}`
  - hold ≥ 3 s; keep inside title-safe; never over the product.
- **Logo + CTA:** `{"type": "image", "image": "{logo}", "start": 26, "end": 30, "in": "springPop", "w": 520}` and a
  `chip` with the URL; land the logo on a downbeat (`"music": {"fitTo": "beats", "endButton": true}`).
- **Product callouts:** `callout` or `pointer` elements from `references/motion.md` on the feature being shown.
- **Price/offer:** `counter` only for approved numbers; check `prefix`/`suffix`.
- **Colour:** `"color": {"look": "clean-commercial", "intensity": 0.5, "match": "product_ref.png"}`.
- **Audio:** `"audio": {"platform": "youtube", "voice": {"denoise": "light", "eq": "broadcast"}}`,
  `"music": {"src": "track_30.wav", "under": 18, "duck": "speech-aware", "endButton": true}`.
- **Length:** set `"output": {"duration": 30}` exactly; trim or extend the last shot in the timeline spec to match.

## Deliver

```bash
python CORE/scripts/deliver.py ad30/plan.json --to youtube,reels,tiktok,facebook,prores-422hq --out-dir ad30/deliver
python CORE/scripts/deliver.py ad06/plan.json --to youtube,shorts --out-dir ad06/deliver
python CORE/scripts/qc.py ad30/deliver/final_youtube.mp4 --plan ad30/plan.json --platform youtube --strict
```

TV: finish with `--platform broadcast-us` (-24 LKFS, ATSC A/85) or `--platform broadcast-eu` (-23 LUFS, EBU R128) and
deliver `broadcast-xdcam` or `prores-422hq` (`deliver.py --list` shows all presets). Name every file with
length, aspect and version: `brand_spring_30s_16x9_v002.mp4`, `..._textless.mp4`.

## Check before delivering

- Every length is frame-exact (`qc.py` duration row) and every aspect exists for every length that needs it.
- The 6 s has one idea, the brand by 2 s, the logo ≥ 1.5 s.
- Supers readable (≥ 3 s, ≤ 15 cps), inside title-safe, legally approved text only.
- Product colour true; product and logo in frame in vertical versions.
- Loudness per destination (-14 LUFS social, -24 LKFS US TV, -23 LUFS EU TV), true peak within limits; music ends on a bar.
- Textless versions and the caption files delivered alongside.

## Example requests

- "Here's our commercial shoot and script: cut a 30, a 15 and a 6-second bumper, with vertical versions for Reels and TikTok."
- "Make the TV version of this 30-second spot at broadcast loudness, plus a textless master."
- "Rebuild a 6-second YouTube bumper from this ad: one idea, logo on screen at the end."
