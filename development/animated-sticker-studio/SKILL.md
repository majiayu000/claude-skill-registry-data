---
name: animated-sticker-studio
description: Turn a character image (mascot, OC, pet photo, 3D render, or just a text description) into a full pack of animated chat stickers — real keyframe animation plus motion, captions and effects — exported to the exact spec of WeChat 表情开放平台, Telegram, LINE, Discord, Slack, WhatsApp or plain GIF, auto-compressed under each size limit, visually verified and zipped. Use for 表情包/动态表情/贴纸/sticker pack requests of any size (8 to 100+), for redoing single stickers, or for converting an existing pack to another platform.
---

# Animated Sticker Studio · 动态表情包工坊

Pipeline: **plan → reference → atlases → cut → build → look → fix → deliver**. Scripts live in `scripts/` (Python 3 + Pillow; ffmpeg for Telegram/MP4). Run every script with `--help` before first use.

## 1. Plan (manifest.json)

Ask only what you cannot default. Defaults: 16 stickers, Simplified Chinese captions, `generic` GIF; add `wechat` if they mention 微信表情开放平台/上架, `telegram`/`line`/`discord`/`slack`/`whatsapp` if named. WeChat albums take any 8–24 stickers; LINE packs must be 8, 16 or 24.

Write `manifest.json` next to the work (format: [references/manifest.md](references/manifest.md)). Pick captions from [references/phrases.md](references/phrases.md) unless the user gave their own, and give every entry:

- `pose` — what the body does, in English, concrete enough to draw (arms, props, expression). Two entries may never share the same pose with only new text.
- `motion` + `icon` + optional `caption_fx` — chosen to match the line (table in phrases.md).
- For the 4–8 stickers where the gesture IS the joke (挥手, 鼓掌, 打字, 干饭, 点赞, 哭, 打哈欠, 比心…) put them in a group with `"keys": 4` and write four `key_poses`. These become real frame-by-frame animation. Single poses get procedural motion only.

Show the user the plan as a short table (编号 / 文案 / 动作) before spending on generation when the pack is ≥24 or the user seems picky; otherwise go.

## 2. Reference

- User image → copy into `ref/`, set `character.reference`. Write `character.anchors`: one English sentence listing what must never change (shape, colours, markings, accessories).
- 3D model → render a front/three-quarter view with the face visible, use that.
- Only a description → `gen_atlas.py manifest.json --provider hiapi --make-reference "<description>"`, show the result, get a yes.
- Use only art the user owns or may adapt. Do not recreate a third party's character from memory.

## 3. Atlases

One sheet per group (≤16 cells). Either:

- **Your own image tool** (Codex `image_gen`, etc.): `gen_atlas.py manifest.json --print-prompts`, generate each sheet with the reference attached, save as the printed path, then set the group's `atlas` and `grid`.
- **Bundled providers**: `gen_atlas.py manifest.json --provider hiapi|openai` (keys only from env: `HIAPI_API_KEY`, or `OPENAI_API_KEY` + optional `OPENAI_BASE_URL`/`OPENAI_IMAGE_MODEL`). Skips groups that already have an atlas; `--group N` redraws one. Never print or echo a key.

Open every sheet at full size. Reject and redraw (`--group N`) when the identity drifts, a cell is missing or doubled, limbs are clipped, or two poses are the same.

## 4. Cut

`cut_atlas.py manifest.json` — removes solid or fake-checkerboard backgrounds, finds each sprite by its pixels (not by a rigid grid), writes `sprites/` and fills every entry's `sprites` list. **Open each `atlases/*.index.png`** and confirm number N shows the pose written for entry N. If the model swapped cells, fix by editing `sprites` paths in the manifest — never by renaming captions to fit wrong art.

## 5. Build

```sh
python3 scripts/build_pack.py manifest.json out --mp4          # platforms from manifest
python3 scripts/build_pack.py manifest.json out --only 3,7-9   # quick re-render of a few while iterating
```

Fonts are found automatically (PingFang/Hiragino/Noto CJK/YaHei); `--font` overrides. Each platform file is re-encoded until it fits that platform's byte limit; `report.json` records the setting used.

## 6. Look (required — you cannot watch a GIF, so look at these)

- `out/review/motion-XX.png`: every sticker as 4 frames side by side on alternating white/dark rows. Check: the motion reads as the caption's emotion, keyframes don't jitter sideways, nothing clipped, no white halo on dark rows, captions legible, accents not covering the face.
- `out/review/contact.png`: whole pack at once — check variety and that no two look alike.
- The build's JSON summary: `failing` (per-platform spec failures) and `pack_issues` (near-duplicate poses, wrong pack size, stickers that barely move). Fix all of them or tell the user exactly which remain and why.

Fix loop: wrong motion/icon/caption → edit manifest, `--only`; bad art → redraw that group or cell; then rebuild everything once at the end.

## 7. Deliver

Give the user: the ZIP path, `预览.html` (opens offline; light/dark/checker backgrounds and a chat mock-up), the MP4 if made, and a one-line pass/fail per platform from the summary. Mention platform limits that still need a human: WeChat needs a 750×400 banner and copyright paperwork, LINE/Telegram need account-side upload. Specs are in [references/platforms.md](references/platforms.md); say they are as of 2026-11 and the platform console wins.

Keep the original reference and atlases out of the ZIP unless asked.
