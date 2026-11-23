---
name: product-review
description: "Product-review editor for YouTube and social: verdict teased up front, what it is and the price, readable spec graphics, hands-on and macro B-roll over the talking, pros and cons cards, a final score, and a sponsorship / free-sample disclosure card, in 16:9 plus a 9:16 verdict cutdown. Use when the user says: edit my review, tech review, product review video, unboxing and review, pros and cons video, gadget review, rate this product, sponsored review. Reviews must be honest and disclosed (FTC / ASCI). Default skin product-spotlight over a talking head, or any Video Studio skin."
license: MIT
---

# Product Review

Talking head plus clean product B-roll, structured so the verdict is clear and the trust is earned.

- **Best for:** tech, gear, beauty, kitchen, car, app reviews; unboxing + review
- **Inputs:** the talking A-roll, product B-roll (macro, hands-on, in use) in a folder named by what each shot shows, specs sheet, price, sponsorship status
- **Default skin:** `chapter-pro` · alternatives `product-spotlight` (product-led), `data-story` (spec-heavy), `split-proof` (comparisons)
- **Formats:** 16:9 1920x1080 master, 9:16 verdict cutdown (30-60 s), chapters, thumbnail stills
- **Duration target:** 4-15 min; genre preset `product-review`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre product-review`.
- The `--genre` preset sets autocut's pause cut (0.45 s) and run.py respects it; pass `--max-gap` only to override.
- **Ethics:** ask whether the product was paid for, sent free, or sponsored. Any of the last two needs a clear disclosure on screen near the start and in the description. The score and the cons are the reviewer's real opinion: never edit a negative into a positive.

## How a pro cuts this

| beat | % | what happens |
| --- | --- | --- |
| verdict tease | 0-5 | "This is the best X under $500 - with one big catch" + hero shot |
| disclosure + what it is | 5-13 | sponsor/free-sample card, name, price, who it's for |
| specs | 13-25 | the 3-6 specs that matter, as a card or bars, not a spec dump |
| hands-on | 25-60 | real use, macro B-roll every claim, comparisons |
| pros / cons | 60-84 | separate cards, balanced |
| verdict + score | 84-96 | who should buy, who shouldn't, score |
| end screen | 96-100 | next review |

- **Pacing:** ASL 3-6 s; B-roll over at least half of the talking; a change every 4-5 s.
- **Cut rules:** jump cuts on the presenter are fine; cover the ones mid-explanation with the product shot of what is being said. B-roll must show *the thing being described* (not decoration).
- **J/L cuts:** L-cut the presenter's line over the macro shot; J-cut the product sound (click, hum) before its shot.
- **Transitions:** cuts; a whip or slide only on section changes. Speed ramp on one hero reveal.
- **Music/SFX:** clean bed 24 LU under; UI ticks on spec items; a soft impact on the score.
- **Colour:** product colour must be true: correct, then `clean-commercial` 0.4. Skin on the presenter stays natural.
- **Captions:** sidecar SRT; on-screen text for specs, prices (with date), pros/cons and the score.
- **Client judges:** trust, a clear verdict, clean product B-roll, readable spec graphics.
- **Common mistakes:** spec dumps read off a sheet, a verdict only at minute 12, prices without a date, B-roll of the wrong model/colour, missing disclosure, cons edited out.

## Make the edit

```bash
python CORE/scripts/run.py review.mp4 --style SKILLS/chapter-pro --genre product-review --smart-cuts \
  --retakes --broll broll/ --model small --prompt "Product Name, brand terms" --work rev --stop-after plan
python CORE/scripts/story.py outline --work rev --genre product-review      # find the verdict line for the tease
python CORE/scripts/editor.py review rev/plan.json --genre product-review --fix
python CORE/scripts/render.py rev/plan.json --frames 2,30,120,300
python CORE/scripts/render.py rev/plan.json
python CORE/scripts/finish.py rev/plan.json --platform youtube
```

If the verdict line was said at the end, cold-open on it with `story.py reorder --work rev --order "s58-s59,s1-s57,s60-s70"` and rebuild via `run.py - --timeline rev/story_timeline.json ...` (this is normal entertainment reordering; keep the line's meaning intact).

## Refine the plan

- **Disclosure:** `{"type": "chip", "text": "Sponsored by BRAND", "start": 6.0, "end": 11.0, "x": 60, "y": 60, "anchor": "top-left"}` (or "Sent free by BRAND - no money, no review approval").
- **Product + price:** `{"type": "card", "kicker": "Reviewed", "title": "Model X2", "body": "$499 (price on 17 Nov 2026)", "image": "{image}"}` - pass `--image product.png` to run.py.
- **Specs:** `{"type": "bars", "title": "Battery (hours)", "items": [{"label": "X2", "value": 31, "highlight": true}, {"label": "Rival", "value": 24}]}` or a `card` with `items` and `at` times.
- **Pros / cons:** two `checklist` elements ("Pros", "Cons") with items timed to when they are said.
- **Score:** `{"type": "counter", "from": 0, "to": 8.5, "decimals": 1, "suffix": "/10", "label": "Verdict"}` + `"sfx": [{"t": 512.0, "kind": "impact", "gain": 0.5}]`.
- **Comparisons:** `compare` (before/after images) or `split` with two panes.
- **Look/sound:** `"color": {"look": "clean-commercial", "intensity": 0.4}`, `"music": {"src": "bed.mp3", "under": 24, "duck": "speech-aware"}`.
- **Chapters:** top-level `"chapters"` for verdict, specs, hands-on, pros, cons, verdict.

## Deliver

```bash
python CORE/scripts/deliver.py rev/plan.json --to youtube --out-dir rev/deliver
python CORE/scripts/qc.py rev/deliver/final_youtube.mp4 --plan rev/plan.json --platform youtube
```

- 9:16 verdict cutdown: `retention-reel` on the verdict section (`prep.py review.mp4 --work rev-short --start S --end E`).
- Description: disclosure text first, then `chapters.txt`; check thumbnails show the actual product.

## Check before delivering

- Disclosure on screen in the first minute and in the description whenever money or free product was involved.
- Every spec, price and model name verified; price dated.
- B-roll matches the model/colour talked about; product colour accurate on a contact sheet.
- Pros and cons both present; score matches what was said.
- `qc.py` passes; tell the user structure, chapters and files.

## Example requests

- "Edit my phone review - tease the verdict first, spec cards, pros and cons, score at the end."
- "Sponsored headphone review, add the disclosure and macro B-roll over the talking."
- "Unboxing + review into a 10-minute video and a 45-second verdict Short."
