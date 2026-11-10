---
name: open-design-social-post
description: Design a social media post (X, Instagram, LinkedIn, Xiaohongshu, Stories/Reels, YouTube thumbnail or video) and export upload-ready files — use whenever the user wants something to post on social media (an X/Twitter image, Instagram or LinkedIn post or carousel, Xiaohongshu cards, a Story/Reels cover, a YouTube thumbnail or video), even if they don't mention Open Design
---

<!-- generated:open-design-agent-kit -->

Design a social media post with Open Design and export files that are ready to upload.

Brief: the rest of the user's message (if there is none, ask the user: "What should the post say, and for which platform?")

**How to talk to the user.** Many people using Open Design don't write code, so:
- Use the user's own words. If they say "artifact", "design tokens" or give a file path, use those terms back; otherwise use the plain words below.
- Keep the machinery out of replies: no tool names, no ids like `od:prototype:poster-hero`, no internal files (`.artifact.json`, `.comments.json`, `config.json`), and not the words "register", "manifest", "sidecar", "entry" or "surface", unless the user used them first.
- Explain a print term the first time it comes up, in one short clause, and not again.
- Say where a file is the way the user would find it ("in your Open Design folder, under seed-swap-flyer"). Give a raw path only where the user can click it (Claude Code, Claude Desktop's Code tab, VS Code) or asks for it.
- End each reply that finishes a step with one line on what they can do next, with at most two options ("Want it in Instagram sizes too, or is it ready to print?").

| Instead of | Say |
|---|---|
| artifact, entry, registered | your design, saved |
| design system, active design system | your style (the first time: "a saved style: colours, fonts and spacing") |
| surface, skill, template, recipe | kind of design, starting layout, or nothing |
| workspace, output directory | your folder, your Open Design folder |
| bleed | print edge ("a few millimetres extra that the printer trims off") |
| trim size | final size |
| preflight findings, errors | "I checked it and fixed…", "one thing to look at:" |
| export | save as PDF, save as an image |
| inline preview, MCP App | the preview above |

## 1. Pick the platform and format

If the brief names a platform or format, use it. Otherwise ask the user to pick one of the rows below before doing anything else. Don't guess.

| Format | Canvas | skillId | Export |
|---|---|---|---|
| X single image | 1600×900 | `od:prototype:card-twitter` | `preset: "x-image"` |
| X post mock (for a video overlay or quote) | card element | `od:prototype:social-x-post-card` | `selector: "[data-od-card]"`, `maxBytes: 5000000` |
| Square carousel (Instagram / LinkedIn) | 1080×1080 per card | `od:prototype:social-carousel` | `preset: "ig-square"` |
| Instagram portrait | 1080×1350 | `od:prototype:poster-hero` | `preset: "ig-portrait"` |
| Story / Reels / TikTok cover | 1080×1920 | `od:prototype:poster-hero` | `preset: "story"` |
| Xiaohongshu cards | 1080×1440 per card | `od:prototype:card-xiaohongshu` | `preset: "xhs-card"` |
| YouTube thumbnail | 1280×720 | `od:prototype:social-youtube-thumbnail` | `preset: "yt-thumbnail"` |
| YouTube video | 1920×1080 MP4 | `od:video:hyperframes` | MP4 via the HyperFrames CLI (see step 4) |

A preset fills in the canvas size, `selector: "[data-od-card]"` and the platform's upload limit (X 5 MB, Instagram 8 MB, YouTube thumbnail 2 MB).

For several platforms at once, run steps 2–4 once per format and keep each one as its own artifact.

## 2. Generate

Call `prepare_open_design_brief` with the row's `skillId`, the brief, and `format` set to the row's preset id (leave it out for the X post mock and YouTube video). Call `list_open_design_design_systems` first if the user names a brand or visual direction, or `recommend_open_design_design_systems` if they name none and no design system is active. For the X post mock, say in the brief that it is one card element.

Author the files yourself with your own file-editing tools, following the returned instructions, and add these rules for social posts:

- Each card or canvas is a fixed-size element at exactly the table's size with `overflow: hidden`, and carries a `data-od-card` attribute. For multi-card formats, stack the cards vertically in one HTML file, one `data-od-card` element per card.
- Use real copy from the brief, with no lorem ipsum. Keep text inside a 48px safe margin, and make the hook readable at thumbnail size.
- No external image URLs unless the user supplied them.
- No emoji as key visuals. They render from the exporting machine's fonts and can come out as empty boxes. Draw icons and subjects as inline SVG.

## 3. Register

Call `register_open_design_artifact` with the entry path, kind `html`, a title, `sourceSkillId` set to the row's `skillId`, and the same `format` you passed to the brief, so the export can find the right size.

## 4. Export

- **Image formats**: call `export_open_design_artifact` with the entry path and the row's export arguments. If its preflight reports errors (text cut off, a card that isn't the canvas size) or it returns warnings (failed fonts or images, over budget), fix the artifact and export again. Before exporting, call `check_open_design_artifact` to see the post as an image with its preflight findings, without writing files; fix every error first.
- **YouTube video**: follow the brief's "Host override" section. Render with `npx hyperframes render … --output <artifact-dir>/exports/<name>.mp4`, and check `ffmpeg -version` first.

## 5. Report

List each exported file's path, pixel size, and file size, and remind the user of the post's copy (caption and hashtags) if you wrote any. Don't post anything anywhere yourself.
