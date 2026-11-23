---
name: ugc-ad-kit
description: "UGC Ad Kit video-editing style for Claude: Native-looking ad: selfie footage, TikTok-style text hook, product callout cards and a strong end card. Use for paid social ads, product reviews, unboxings, testimonial-style ads (with the user's own footage). Turns a raw clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# UGC Ad Kit

Native-looking ad: selfie footage, TikTok-style text hook, product callout cards and a strong end card.

- **Best for:** paid social ads, product reviews, unboxings, testimonial-style ads (with the user's own footage)
- **Category:** Product / app promo
- **Default format:** 9:16 (change with `--format 9:16 | 1:1 | 4:5 | 16:9`)
- **Needs camera footage:** yes, a raw talking clip
- **Text behind the speaker:** no

## Before you start

This style runs on the **video-studio-core** skill, which must be installed in the same skills folder.

- `CORE` = the `video-studio-core` folder next to this one (e.g. `~/.claude/skills/video-studio-core`).
- `STYLE` = this skill's folder (it holds `theme.json` and `theme.css`).
- First time on a machine: `python CORE/scripts/check_env.py`, and fix anything it reports.
- If `CORE` is missing, tell the user to install `video-studio-core` from the same pack.

## Make the edit

```bash
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-ugc-ad-kit --stop-after plan --image product.png --cta "Shop now"
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-ugc-ad-kit/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-ugc-ad-kit/plan.json
python CORE/scripts/finish.py edit-ugc-ad-kit/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- Looks native: white text with black outline, a plain white hook box, no heavy branding until the end.
- Structure: hook (0-3 s), problem, product in use with 2-3 callouts, proof, call to action (last 2.5 s).
- Product image card pops in when the product is named.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Read `words.json` and rewrite the hook (first 2-3 s) into a short, specific promise.
- Replace weak auto-picked key words with the words that carry the meaning (numbers, results, names, contrasts).
- Fix any mis-heard words in the `words` array (keep their times).
- Ask for a product photo (PNG) and pass `--image product.png`; it shows as a callout card when the product is named. Move its start to that word.
- Add 2-3 `chip` callouts for benefits (3-5 words each).
- Only use real claims and real prices the user gives you.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Make this a UGC-style ad for my product."
- "TikTok ad edit, hook in 2 seconds, end with 'Shop now'."
- "Turn my unboxing into an ad."
