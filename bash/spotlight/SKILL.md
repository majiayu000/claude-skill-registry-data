---
name: spotlight
description: Turn a website, a code project, footage or photos, and a description into a short video that brags (a launch), promotes a point (a promo), or explains a topic (a presentation as a video), with music, on-screen text in any language, a poster and a caption. Use when someone says "/spotlight", "make a video about this", "launch video", "brag about this", "promo from these photos/videos", "reel from this footage", "explainer video", "presentation video", or points at a site, folder or topic and wants a video.
---

# spotlight

You make the whole video yourself: find the story, pick the material, set the type, mix the sound, render, check, and have it critiqued. The scripts and the render kit handle everything with sharp edges.

`<skill-dir>` is the folder holding this SKILL.md. Below, `F=<skill-dir>/scripts/footage.py`.

Usage: `/spotlight [url | folder | files | project | "description"]… [options]`. Flags or plain language.

| Option | Default |
|---|---|
| `--mode brag\|promo\|explain` | inferred (table below) |
| `--tone <preset or freeform>` | inferred per mode |
| `--format vertical\|landscape\|square` | vertical for brag/promo, landscape for explain; 1080×1920 / 1920×1080 / 1080×1080, 30 fps |
| `--duration <s>` | brag 20, promo 20, explain 90 |
| `--lang <code>` | from the brief → the site's `lang` → text in the footage → ask |
| `--music <file>\|none` | an audio file in the inputs, otherwise a bundled track matched to the tone (`references/sound.md`) |
| `--voice` | off; on reads narration aloud with local Piper TTS (`references/sound.md`) |
| `--no-sfx` | effects on, placed by the sound rules |
| `--no-ai` | AI images on when the bridge works |

Deliverables go to `spotlight-output/` (timestamped `spotlight-output-YYYY-MM-DD-HHmmss/` if it exists): `video.mp4` (poster embedded as cover art), `music-only.mp4` (when the mix has effects or narration), `poster.jpg`, `caption.txt`, `plan.md`, `sources.md`, and `work/`. Below, `OUT` is that folder's absolute path; create `$OUT/work` first and run the commands from there. **Never modify, move or delete anything in the user's inputs.** Before anything else run `bash <skill-dir>/scripts/doctor.sh`; if it reports a missing required tool, say which and stop.

## Modes
| Mode | When | Read |
|---|---|---|
| `brag` | a code project or a website, nothing else | `references/brag.md` |
| `promo` | footage or photos are the main material | `references/promo.md` |
| `explain` | a topic or argument, data files, or the user says presentation/explainer | `references/explain.md` |

Inputs mix freely: a promo can quote the brand's site, an explainer can use footage. Read exactly one mode file (plus the Inventory and Footage sections of `references/promo.md` whenever footage or photos are in the mix), plus `references/sound.md`, `references/quality-bar.md` and `references/critic.md` when you reach those steps, and `references/visuals.md` when the plan has a chart, a diagram or a 3D shot.

## 1. Gather
- **Media:** `python3 $F prep $OUT/work <files…>` → manifest, upright sRGB stills, contact sheets (see the mode file).
- **Website:** in `$OUT/work`, `npm i --prefix . playwright-core`, then `node <skill-dir>/scripts/site.mjs <url> . --size <W>x<H>` → `site/copy.json`, `site/brand.json`, `site/screens/`, `site/full.png`, `site/assets/`.
- **Project:** read the code the way `references/brag.md` describes.
- **Data:** read `*.csv` / `*.json` inputs; numbers on screen come only from them.

## 2. Brief → `work/brief.md`
What it is, who it's for, the one message, the one action (CTA), the facts you'll show **with their source** (brief, site page, footage file, data file), and the don'ts. If the name, the CTA or the language is still unknown, ask **one** question listing everything missing; if nobody can answer (a headless run), decide the most sensible answer and say so in your report. Never guess a phone number, a price or an address. Only public addresses go on screen: never `localhost`, `127.0.0.1`, a LAN address or a file path. Data and log files often hold local paths (`"file": "/home/…"`), so quote only the keys you cite. With no public URL, end on the name and the action.

## 3. Plan → `plan.md`
The angle, the hook, and a shot or section list. Each entry has its source (copy the path from the manifest or site files), in/out points or motion, its on-screen text (verbatim from the sources; the hook question, chapter cards, a promo's mood lines and the CTA are yours to write, each listed in `sources.md` as authored, with the claim it stands for if it makes one), its duration and its transition. Add the music (track and window) and the cue times you'll cut on, the effects (time → file → why, unless `--no-sfx`), with `--voice` the narration lines, plus the AI assets table. With `--voice`, run `voice.py` right after the plan (`references/sound.md`): the line durations set the shot timing. Durations must add up to the target. Write `sources.md` alongside: every line of on-screen text and every number → where it came from, plus the AI ledger (file, prompt, purpose, shot).

## 4. Build
### The page

Start from the kit: copy `<skill-dir>/kit/scene.html` and `<skill-dir>/kit/kit.js` into `work/`, then
- write `work/timeline.js` as `window.SPOTLIGHT = { width, height, duration, end, grain, fonts, shots: [...] }`. Shots come in order, each `{ a, b }` in seconds plus `clip: "frames/s01", n` (from `shot`), `still: "stills/004.jpg"` or `web: "site/full.png", scroll: [y0, y1]` (a captured site page drawn at the output width and scrolled from `y0` to `y1` at a constant speed, in output pixels; keep it at 80 px/s or more, because a slower scroll over flat parts of a page measures frozen), and optionally `panel`, `push: [from, to]`, `origin`, `drift: [x0, x1]` (a sideways drift in % of width), `filter` (e.g. a dimmed, blurred background behind a list card), `grade`, `grain`, and `dip: 0.3` (a transition into the shot through black, or `dipColor`, centred on the cut). On a `web` shot, `origin` sets where `push` zooms within the visible page (`"0% 50%"` keeps a left-aligned page's left edge put). Stills move at a constant speed. A still with a `filter` is a text-card backdrop and gets a stronger push and drift by default, which keeps a photo backdrop moving for cards up to about 5 s; a longer card, or a very smooth backdrop under heavy blur, can still measure frozen, so split the card, blur less, use a more detailed still or a blurred clip. `kit.js` documents every field;
- charts (`.chart`), diagrams (`svg.diagram`) and 3D shots (`three: "three/routes.js"` or `"three/extrude.js"`, with `params`; copy `<skill-dir>/kit/three/` to `work/three/`) are described in `references/visuals.md`;
- put the `@font-face` rules for the downloaded woff2 files in `work/fonts.css` (the template links it; a missing file fails the capture);
- anything custom (a cursor that clicks, a line being typed, a toggle) goes in `scene.html`, driven from t by a `draw` function in `timeline.js` (`SPOTLIGHT.draw = (t) => { … }`), which the kit calls every frame;
- put the captions and the end card in `scene.html`: `.cap.low|.high|.mid` with `data-a`/`data-b` (on screen from/to), each line a `[data-at]` element (when it lands; `data-at="0"` or less is already landed on frame 0, which suits the hook), `data-scrim="top|bottom"`. A caption fades out over its last 0.25 s and each line fades in over 0.4 s, so on a hard cut land the next caption's first line on the cut (or `dip`), or the frames around the cut carry no text; a caption is readable until `data-b` − 0.25. Set the brand tokens (`--ink`, `--paper`, `--accent`, fonts) in `:root`, and add your own CSS at the marked end of the `<style>` block (earlier rules lose to the template's).
The kit keeps every frame a pure function of t, looks up clip frames with the rounding fix (`floor((t - a) * 30 + 1e-6) + 1`), and scales type and safe zones to the format. So the same timeline renders vertical, landscape or square: change `width`/`height` and re-cut the clip frames at the new size. Anything custom you add must also be a pure function of t: no timers, and no CSS transitions or animations of its own.

Capture with the bundled script, run from `work/` after `npm i --prefix . playwright-core`:
- `node <skill-dir>/scripts/capture.mjs stills 1.2 3.4 …` writes PNG stills to `work/check/`.
- `node <skill-dir>/scripts/capture.mjs frames` writes every frame to `work/out/00000.jpg…`, split across parallel pages (4 on a 16-core box; `CAPTURE_WORKERS=n` to change). It uses `/usr/bin/chromium` when present (`CHROMIUM=path` to override) and exits non-zero on any page error.

### Text in any language

- The page draws all text. Never use ffmpeg `drawtext` for on-screen text: most builds have no text shaper and can't join Persian/Arabic letters.
- Set `lang` and `dir` on every text element: `dir="rtl"` for Persian, Arabic, Hebrew, Urdu.
- Inside RTL text, wrap phone numbers, URLs, prices and Latin brand names in `<bdi dir="ltr">` so they don't come out reversed or jumbled. Use the digits the brief uses.
- Font: the brief's font; otherwise a Google Font that covers the script (Vazirmatn for Persian, the matching Noto family otherwise). Fetch the Google Fonts CSS (`https://fonts.googleapis.com/css2?family=…`) with a browser User-Agent (`curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"`), or it serves TTF instead of woff2. For a site, `brand.json` `fonts_loaded` lists the web fonts the page really loaded (`fonts` is only what its CSS asks for). Download the woff2 into `work/` and load it with `@font-face`, so capture never waits on the network.
- **Animate joined scripts (Arabic, Persian, Urdu, Devanagari…) by word or line, never per character.** Per-character spans break the letter joining. Per-character is fine for Latin.
- Safe zones: keep text and the CTA out of the top ~12% and bottom ~20% in vertical (8% / 10% in landscape), where platform UI sits, with ~6% side margins. The kit's `.cap.low` grows upward from that line, so longer text can't cross it.
- No letter-spacing on Arabic-script text: it pulls joined letters apart (the kit already turns it off for `lang="fa|ar|ur"`).

### Brand

Use the logo file and brief colors if given (logo files often sit on a white box or carry a thin frame line; make the background transparent and check the edges); otherwise a restrained palette taken from the footage itself. Titles sit on the footage with a soft scrim for contrast, not on flat color slides.

### AI images (codex bridge)

Optional dependency: [gpt-image-bridge](https://github.com/oakplank/gpt-image-bridge) (installed at `~/.claude/skills/gpt-image-bridge/bin/gpt-image-2`, or `gpt-image-2` on `PATH`) plus a logged-in `codex`. Skip this section, and say so, if `--no-ai` is set, the bridge is missing, or `codex login status` isn't logged in. Edits need a bridge that accepts `--image`; if `grep -q -- --image <bridge>` finds nothing, use gap-fill only.

- **Gap-fill** (prompt only): title or background plates, textures, or a clearly illustrative scene for a beat the footage can't show (e.g. a line-art route map behind a services card).
  - **Frame for the crop:** the bridge makes 2:3 (`--size 1024x1536`) or 3:2 (`--size 1536x1024`), so ask for the subject centred and a quiet middle where text will sit. Say "no text, letters, logos" unless text is the point, because it invents lettering.
  - **Match the footage:** describe its light, palette and grade in the prompt, then finish in the timeline with `grade` (e.g. `saturate(.9) contrast(1.05) sepia(.06)`) and `grain` (~0.1). A clean render next to phone footage looks pasted in.
  - **Cache:** save as `work/ai/<name>.png` with the prompt in `work/ai/<name>.prompt.txt`. Re-cuts and other formats reuse the file unless the prompt changes; don't spend quota twice.
- **Edits** (`--image <source still>`): only to remove or clean up something in a region with no text, logos, faces or product detail. The model re-renders the *whole* image. In testing it removed a toy truck cleanly but changed "31st" to "31th" on an award plaque and shifted the framing (its sizes are 2:3/3:2/1:1, so a 9:16 source gets reframed). So its output is a draft, never the final frame:
  - pad the still to the bridge's aspect (2:3 for a vertical still, 3:2 for a landscape one) and pass the matching `--size 1024x1536` or `--size 1536x1024`, so the result lines up with the source;
  - composite only the edited region back onto the original through a feathered mask;
  - compare every text, face and product area with the source.
  If it won't align or anything else changed, do the edit with ImageMagick/ffmpeg (crop, blur, grade) or skip it. Anything with text on it gets ImageMagick/ffmpeg, not the bridge.
- Each call takes 4–6 minutes and uses the user's ChatGPT quota: **at most 3 per run** unless the user asks for more. Start them in the background right after the plan so they run while you build. Read every result, and reject anything off-brand, uncanny, carrying invented text, or against the Truthful rule. A failed or rejected image never blocks the render; use the plan's footage-only fallback.
- **Label it:** list AI shots in the plan's AI table and in your report, and add a short "Includes AI-generated illustration" line to `caption.txt` (in its language). Some platforms ask for this.

## 5. Sound
Follow `references/sound.md`: pick the music (the user's track, else a bundled one), place the effects (unless `--no-sfx`), add live clip sound where it helps, and the narration lines with `--voice`. Write `work/mix.json` and run, from `$OUT/work`, `uv run <skill-dir>/scripts/mix.py mix.json` → `mix.wav`, `music-only.wav`, `mix-report.txt`. Read the report and fix anything it flags. The music keeps playing until the end card has landed.

## 6. Capture, encode, check
### Check before the full render

The first full capture and encode is the draft (20 s takes about a minute): run `python3 $F check draft.mp4 --end-card <s> --out draft-check` on it, and fix every hold it lists before the final render. If the draft needs no fixes, its frames are the final ones: encode `out/` again with `--poster` instead of capturing again. Capture stills (`capture.mjs stills …`) in the middle of every shot, at every transition, and on the first frame after every cut (clips that were already edited hide dissolves, blurs and light leaks there), and look at them:
- Upright?
- HDR clips not washed out?
- Text joined and running in the right direction, numbers not reversed?
- Inside the safe zones?
- No overflow, collisions or low contrast, and no captions laid over signage or lettering in the footage?

A plain crossfade between two busy shots makes a muddy double exposure: dip through black or the brand color (`dip`), or cut. Fix, re-check, then capture every frame.

### Encode

Pick the poster frame first (see Deliver) and copy the chosen `out/NNNNN.jpg` to `$OUT/poster.jpg`. Don't copy it over frame 0: a settled poster frame followed by the opening frames flashes for one frame at the start and on every loop. Then run `python3 $F encode out mix.wav $OUT/video.mp4 --poster $OUT/poster.jpg`. `--poster` embeds it as cover art, which players and file browsers show. Pass `none` instead of the wav for a silent track (a video with no audio track turns into a GIF on Telegram). With effects or narration in the mix, also run `python3 $F encode out music-only.wav $OUT/music-only.mp4 --poster $OUT/poster.jpg`.

It writes BT.709-tagged H.264 yuv420p + AAC with `+faststart`, exactly frames/30 seconds long, at −14 LUFS: one fixed gain, then a true-peak limiter tuned on the AAC itself, so the true peak lands under −1.5 dBTP even with a narrator's plosives. It refuses a frame folder that mixes PNG and JPG, has gaps in its numbering, or has a file that isn't really the format its name says, and it checks the frame count of what it wrote.

Then run `python3 $F check $OUT/video.mp4 --end-card <s> --out $OUT/work` and fix every failure and every hold it lists. `--end-card` is the end card's length (`duration` minus `end` in `timeline.js`), not the time it starts.

## 7. Critic
Follow `references/critic.md`: a fresh critic reviews the actual render, you fix, a new critic verifies. At most 3 rounds.

## 8. Deliver
- **`poster.jpg`:** the strongest settled frame, embedded as cover art (`encode --poster`), never copied over frame 0.
- **`caption.txt`:** in the video's language, 1–3 sentences plus the CTA, optional hashtags, and a short AI-illustration label if any AI image is used.
- **`music-only.mp4`:** the same video over the music and live sound alone (not ducked), when the mix has effects or narration.
- **`plan.md`, `sources.md`, `work/`** stay.
- **Tell the user:** where the files are, the angle in one sentence, the `check` numbers, the critic's verdict, and which shots are AI. Offer a re-cut, another tone or another format (re-using `work/`).

## Rules

- **Length.** brag 15–25 s, promo 15–30 s, explain 60–180 s; ~20 s is the sweet spot for brag and promo.
- **Hook first.** The first 1–2 seconds decide whether anyone keeps watching.
- **Clear to a stranger.** After one viewing, they know what it is, who it's for and how to get it.
- **Real footage first.** The user's material is the star. Best shots only; no abstract filler.
- **Truthful.** Text and numbers come only from the brief, the footage, the brand's own site, the project or the data files, and each one is listed in `sources.md`. No invented prices, discounts, stats or testimonials. Third-party brands visible in the footage (logos on props, vehicles, screens) stay out of frame or get blurred, so the video doesn't imply a partnership. AI imagery never depicts the actual product, place or people as something they aren't: no fake rooms, dishes or product shots. Edits only remove or clean up; they never extend or re-stage a real scene. Fully generated images appear only as clearly illustrative, title or background elements.
- **Readable.** A line meant to be read stays fully on screen about 0.3s per word (at least ~1s), counted from when the whole line has landed. Fast in, then hold.
- **Private stays private.** The footage, the render and the plan stay on the machine; never upload them. AI images send the prompt, and for edits the source still, to OpenAI through codex, so skip AI (`--no-ai`) for confidential footage. No EXIF locations, stray phone numbers or addresses (unless they're in the brief), and no documents or screens with personal data. Flag licence plates and bystanders' faces in the plan, and blur them if the user wants.
- **Every frame postable.**
