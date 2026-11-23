---
name: product-spotlight
description: "Product Spotlight video style for Claude: Studio product shot: your product image floats on a spotlight, feature callouts draw in with arrows. Use for e-commerce, product launches, merch, physical products, catalogue reels. Builds a finished 9:16 motion-graphics video (no camera footage needed) with the video-studio-core engine."
license: MIT
---

# Product Spotlight

Studio product shot: your product image floats on a spotlight, feature callouts draw in with arrows.

- **Best for:** e-commerce, product launches, merch, physical products, catalogue reels
- **Category:** Product / app promo
- **Default format:** 9:16 (change with `--format 9:16 | 1:1 | 4:5 | 16:9`)
- **Needs camera footage:** no
- **Text behind the speaker:** no

## Before you start

This style runs on the **video-studio-core** skill, which must be installed in the same skills folder.

- `CORE` = the `video-studio-core` folder next to this one (e.g. `~/.claude/skills/video-studio-core`).
- `STYLE` = this skill's folder (it holds `theme.json` and `theme.css`).
- First time on a machine: `python CORE/scripts/check_env.py`, and fix anything it reports.
- If `CORE` is missing, tell the user to install `video-studio-core` from the same pack.

## Make the edit

```bash
python CORE/scripts/run.py - --style STYLE --work edit-product-spotlight --stop-after plan \
    --no-source --image product.png --title "Product name" --cta "Shop now" --duration 10
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-product-spotlight/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-product-spotlight/plan.json
python CORE/scripts/finish.py edit-product-spotlight/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- Product centred and floating, soft spotlight behind. 3-4 feature callouts appear one by one with hand-drawn arrows pointing at the product.
- Name at the top, CTA at the end. Clean pop sounds.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Pass `--no-source --image product.png --title "Product name" --cta "Shop now" --duration 10`. Use a PNG with transparent background if possible.
- Add 3-4 `chip` callouts (class `ps-call`) with features the user names, plus a `scribble` arrow from each chip to the product, staggered 1.2 s.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Product spotlight video for my new bottle."
- "Show my product with feature callouts."
- "Clean e-commerce reel from my product photo."
