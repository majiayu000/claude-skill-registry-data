---
name: motion-promo
description: Turn a voiceover into a slick, portfolio-grade motion-graphic promo or ad with Remotion. Works from an MP3, WAV, M4A or a video's audio. It cuts the pauses and throat-clears, masters the audio and finds exact word timings. It captures real screenshots, logos and brand colours from the product's site, then plans one visual beat per phrase. It builds 60 fps animated scenes from a kit of tested motion patterns, reviews its own frames and renders a vertical, square or horizontal MP4. Use this whenever the user wants a motion graphic, animated ad, promo, explainer, launch video, kinetic-typography video or "slick animated video" from a voiceover or audio file, or says "turn this voiceover into a video". Also use it when they ask for Remotion motion graphics for a product, app, course, community or service, even if they never mention Remotion.
---

> **Video Studio:** how this skill runs here (these lines win over the steps below where they differ).
> - **Project folder:** `projects/remotion/motion-promo-<job id or slug>/`, a fresh Remotion project each time as below (`projects/` is never committed). It is its own project, separate from `engines/split-screen`, so it runs whatever `styles/engines.json` says. Run every `npx` command from inside it.
> - **Footage from a studio job:** copy (never move) `jobs/<id>/source.*` into the project's `public/`.
> - **Voiceover:** this skill's own voiceover prep (pause cutting, noise removal, mastering) re-times the audio, so its transcript is the job's one transcript; don't use studio/words-convert.mjs here. Copy its `scripts/words.json` into `jobs/<id>/`.
> - **Colours and fonts:** for Elivate Marketing's own promos, `src/theme.ts` takes `styles/brand.json` (purple #8B5CF6 / #C4B5FD / #4C1D95 on black, Inter + Playfair Display). For a promo about someone else's product, capture that product's colours as below.
> - **Sounds:** its `scripts/sfx.mjs` places sounds; take them from `assets/sfx` (names in `styles/sfx.json`) and follow `styles/SOUND-RULES.md`.
> - **Where it fits:** the motion-promo style (catalog). A voiceover dropped into the studio can rank it next to faceless-sprite.
> - **Remotion licence:** free for individuals and companies of up to 3 people; above that it needs a company licence (remotion.dev/license).
> - **Deliver:** copy the rendered MP4 into the job folder (`jobs/<id>/preview.mp4` while reviewing, `final.mp4` when approved) or `outputs/`, and log what was added in `edits.json` so the review page can take notes on it.

# Motion Promo

This skill makes a clean, fast motion-graphic ad that is built around a voiceover. Every phrase gets its own visual idea that lands on the spoken word. The ad uses real screenshots and logos of the product, and its typography and UI animate at 60 fps on one continuous dark stage. The finished MP4 plays straight in Reels, TikTok, Shorts or Meta ads.

Everything below is plain Node and Remotion. It runs on macOS, Windows and Linux with nothing else installed: no Python and no system ffmpeg.

## Where this came from

The first video was built from this request:

> Create a slick, highly impressive, clean, and smooth motion graphic promo video using a combination of animations and real screenshots or logos to make a beautiful-looking advertisement that ties into this voiceover. Make sure you use Remotion best practices, and make sure that the types of animations are very clean, slick, and look visually appealing. Think of it like a motion graphic portfolio video that showcases a motion graphic designer's best work. There may be some pauses in this transcription which you can remove so that the whole video flows as quickly as possible and feels snappy.

It was then turned into this skill with: "make sure it's dynamic and adaptable so that my Skool community members can use it."

How each part was read:

- **"ties into this voiceover":** every phrase gets a literal visual, and the hero motion of each beat starts on the word. Onsets come from the waveform, because Whisper's timestamps run late.
- **"real screenshots or logos":** headless Chrome captures the product's own site. The mobile shot goes in a phone frame and the desktop shot in a browser frame. Platform logos come from Simple Icons. The brand logo is cropped from the site, and the brand colours are sampled from it.
- **"Remotion best practices":** start from a fresh `create-video` scaffold with Remotion's official agent skills installed and followed. That means `interpolate()`-driven motion, scenes built as `Interactive.withSchema` components and registered as connected compositions, `premountFor`, `staticFile`, `@remotion/google-fonts` and `@remotion/media`.
- **"clean, slick… portfolio":** 60 fps, one dark stage, one accent colour and expo easing, with springs only for pops and landings. Scene hand-offs overlap. Every UI is built in code; there is no stock clip art.
- **"remove pauses… snappy":** pauses are shortened to 0.10 s after commas and list items and to 0.16 s at sentence ends. Non-speech sounds are detected and cut, and the loudness is mastered.
- **"adaptable for members":** nothing is tied to one product. The brand lives in one block of `src/theme.ts`, and the scene plan is written fresh from each voiceover.

The original build was a vertical ad for an "AI Video Editor" download. A staff ID badge dropped in on a lanyard and flipped into a job description. That became a checklist which ticked off each duty while it played as a small animated UI: a waveform turning into a transcript, clips labelled UM being bladed out, a green screen being keyed, graphics flying in, a clipping waveform being limited, and an export that turned into a wall of finished shorts. Then came "I don't sleep / invoice / ghost you" beats, a HIRED stamp, the real community page in a phone, a price slam and a Join button that turned into a download. Borrow that level of craft, not that content.

## What to ask the user

Ask once, and only for what is missing:

1. **The voiceover file** (required). Any audio file, or a video file with the voice in it.
2. **What it promotes, plus a link** (site, app store page, community page, product page). The link provides the real screenshots, the logo and the colours. Without a link, ask for a logo file and a brand colour, or use the neutral default palette.
3. **Format.** Vertical 1080×1920 is the default (Reels, TikTok, Shorts, Meta). Square 1080×1080 and horizontal 1920×1080 are also available.

Everything else (the offer, the price, the CTA wording) comes from the voiceover.

## Workflow

1. Set up the project
2. Prepare the voiceover
3. Gather real assets
4. Plan the scenes, and show the plan
5. Build
6. Review frames, fix, render
7. Deliver

### 1. Set up the project

Scaffold a new project in a fresh folder. Do not reuse other projects on the machine.

```bash
npx create-video@latest --yes --blank --no-tailwind <project-name>
cd <project-name>
npx skills add remotion-dev/skills -a claude-code -y --copy
npx remotion add @remotion/whisper-webgpu @huggingface/transformers mediabunny @mediabunny/server @remotion/google-fonts @remotion/media @remotion/noise
```

Read `.claude/skills/remotion-best-practices/SKILL.md` and the markup rules it links to, and follow them. Where they differ from this kit, the kit wins:

- The kit computes `interpolate()` values in helpers and patterns, and uses `<Img>` for screenshots.
- Real video footage uses `<OffthreadVideo>` from `remotion`, not `@remotion/media`'s `<Video>` (see **Footage** in step 5).
- The user asked for a finished MP4, so render it rather than stopping at a Studio preview.

Then:

- Create every file under **Reference code** below with exactly that content.
- Delete `src/Composition.tsx`.
- Add `"resolveJsonModule": true` to `compilerOptions` in `tsconfig.json`.
- Copy the voiceover to `public/voiceover-raw.<ext>`, keeping its extension.
- Run `node scripts/sfx.mjs`, and `node scripts/logos.mjs youtubeshorts tiktok instagram` for the example scene.

`src/scenes/ExampleScene.tsx` is a working example of the scene structure. Delete it and its registrations once your own scenes exist.

`src/lib/audio.ts` imports `src/voiceover-envelope.json`, which step 2 creates, so typecheck after step 2.

### 2. Prepare the voiceover

```bash
node scripts/find-noises.mjs public/voiceover-raw.mp3
node scripts/prep-voiceover.mjs public/voiceover-raw.mp3 --words scripts/words-raw.json --drop <the ranges find-noises printed>
node scripts/transcribe.mjs public/voiceover.wav scripts/words.json
node scripts/cues.mjs
```

**`find-noises.mjs`** transcribes the raw file into `scripts/words-raw.json` and finds throat-clears, coughs, breaths and filler words. A short sound counts as noise only when two checks agree: Whisper hears no new word when the sound is added to the audio before it, and no word of the full transcript starts there. Leave out `--drop` if it finds nothing.

Read the transcript it prints. Whisper mishears names and jargon. For example, it wrote "school" for "Skool" and "key you out" for chroma-keying the speaker. Spell things correctly on screen and read odd phrases in context. If a phrase is still unclear, re-transcribe that slice with a bigger model, e.g. `node scripts/transcribe.mjs public/voiceover-raw.mp3 scripts/check.json --model medium.en --from 10 --to 13`.

**`prep-voiceover.mjs`** cuts each pause down to a natural length (it reads the punctuation from `--words`), drops the noises, masters the audio to −17 LUFS mono, and writes the timing data:

- If a word start sounds clipped, re-run it with `--soft 36`.
- For an even tighter cut, use `--sentence 0.12 --clause 0.08`.
- To keep the original pacing, use `--no-cut`.

**`cues.mjs`** prints every phrase with its exact start time in seconds and frames, and saves `scripts/cues.json`. This is the timing bible: every scene start and every hit comes from it. Times of words inside a phrase are Whisper's, which run about 0.15 s late. For a hit on a word in the middle of a phrase, subtract about 0.15 s, or use the matching start in `scripts/islands.json`, where each entry is a real onset.

### 3. Gather real assets

```bash
node scripts/capture.mjs inspect <url>
node scripts/capture.mjs inspect <url> --mobile
node scripts/capture.mjs shot <url> public/shots/site-mobile.png --mobile
node scripts/capture.mjs shot <url> public/shots/site-desktop.png
node scripts/capture.mjs element <url> "<logo css selector>" public/logos/brand.png --transparent
node scripts/logos.mjs youtubeshorts tiktok instagram
```

Capture more than the home page. Pricing, features, the dashboard or app, docs, app-store screenshots and the `og:image` are all real material. A real screen of the product beats any illustration.

- **Look at every capture** by reading the PNG. If a cookie banner, popup or loading state ruined it, re-shoot with `--wait 12`, capture a single element instead, or ask the user for a screenshot.
- **Pick the brand colours** from `inspect`. The main button's background is usually the accent. Set `BRAND` in `src/theme.ts`.
  - The accent has to pop on near-black. If the brand colour is dark (navy, forest), use its brightest tint as the accent.
  - `accentInk` is black or white, whichever reads on the accent.
  - If the brand uses a Google Font, swap `SANS` to it.
- **Copy the real buttons.** `inspect` lists each button's text, colours, font, size, border, radius and shadow. Pass them to `CtaMorph`'s `button` so it looks like the button the viewer will actually tap.
- **Focus rectangles** (for the highlight ring): pass the CSS `box` from `inspect` straight to `focus`. Use `inspect --mobile` for phone shots and plain `inspect` for desktop shots. The showcase scales the box itself.
- **Logos that Simple Icons doesn't have** (it dropped Adobe, CapCut, Skool and others): crop them from the brand's site with `element … --transparent`.
  - For an icon plus wordmark, capture the icon on its own by selecting the inner `img` or `svg` (e.g. `".navbar__brand img"`). Square tiles and `EndCard` need the icon alone.
  - Recolour a dark wordmark for the dark stage with `filter: "brightness(0) invert(1)"`, or put it on a white pill.
- **Third-party logos** only appear when the voiceover mentions those platforms or tools. Never imply endorsement.

### 4. Plan the scenes

This is where the video is won. Read the cue sheet as a story (hook → reveal → proof → objections → offer → CTA), then write a plan table:

| # | Cue (s) | Words | What the viewer sees | Pattern or custom build |
|---|---|---|---|---|

Rules:

1. **One visual idea per phrase, literal and specific.** Show the claim, don't caption it. "Hours" becomes a timecode racing to 04:37:12, "cut the ums" becomes clips labelled UM being bladed out, and "$9 a month" becomes a price slam.
2. **Find the script's central object and carry it across scenes.** In the original, "job description" became a staff badge that flipped into a job description, which became the checklist. Others: a recipe card, a case file, a receipt, a boarding pass, a contract, a report card, an app screen.
3. **Map each phrase type to a pattern** (in `src/patterns/`):

   | In the voiceover | Use |
   |---|---|
   | A big number, a time, money, a count | `CountUp` |
   | Introducing the product, character or new hire | `DropFlip` (front: badge, ticket or card) |
   | "Here's what it does / what's inside" | the back of `DropFlip`, a `ChecklistCard` in mode 0 |
   | A list of features, steps or duties | `Stage` + `ChecklistCard` rail + one custom vignette per item (`vignette()`) |
   | Repeated frames ("No X. No Y. No Z.") | `SlotHeadline` + one card per beat (`pushCard()`) |
   | A pain point killed (fees, invoices, waiting) | a real-looking UI card + `Stamp` + `shake()` |
   | Speed, support, "always there" | `ChatThread` |
   | Platforms, tools, integrations | `LogoRow` with `BrandIcon` |
   | Where it lives (site, app, community) | `PhoneShowcase` or `BrowserShowcase`, with a focus ring on the name |
   | The price or offer | `PriceSlam` (a struck "was" price only if the voiceover or the product's page states one) |
   | The CTA (join, download, book, sign up) | `CtaMorph` with the site's real button text and colours |
   | Sign-off | `EndCard` |
   | A voice, a talking product, audio | `VoiceBars` driven by the voiceover |

   List items need custom vignettes: small UIs built in code, like timelines, waveforms, meters, dashboards, forms, inboxes, charts and terminals. Keep each one to a single action that finishes before the next item is spoken. A vignette fills its stage (`stageBox(items.length)` gives the size); it is not a thumbnail floating in the middle.

   Useful pattern props:
   - `CountUp`: `prefix`, `suffix`, `highlightAt`.
   - `ChecklistCard`: `until` (clears the last highlight before a summary beat).
   - `Stage`: `firstNumber`, for a "00 intro" panel.
   - `DropFlip`: `after`, to move the flipped card again, e.g. a document sliding down to become the rail.
   - `CtaMorph`: `inAt`, `labelSize`, and `label` as a node (for a typed-in command).
   - `PhoneShowcase` / `BrowserShowcase`: `scroll` (to a page y), `zoomTo`.
   - `Cursor`: `tip`.
4. **Layout (1080×1920).**
   - Keep key content between y 280 and 1450 and x 80 and 1000, because the platform's UI covers the bottom quarter and the right edge.
   - Use the whole safe area. The centre of mass sits around y 860; don't stack everything at the top and leave the lower third empty.
   - Use one focal point per moment.
   - For square or horizontal formats, rescale positions and keep the same proportional margins.
5. **Scale for a phone.** Hero elements fill 70–90 % of the safe width. When a UI is detailed, push the camera in on the one part that matters instead of showing the whole thing small. The first frame is the feed thumbnail, so the hook must already be visible at frame 0–6 (start entrances at or before 0).
6. **Type.**
   - Keep roughly 3–6 words on screen at once.
   - No word-by-word captions; captions are a separate job. Show key words as designed type.
   - Headlines are 110–180 px heavy sans with −0.05em tracking.
   - Accent words go in the italic serif, and labels in mono caps at 22–30 px.
   - Key text is at least 44 px. Supporting UI text (labels, rails, fake app detail) is at least 30 px.
7. **Colour.** Dark stage, white text, and one accent for what matters (key numbers, checks, the CTA). Use the alert red only for problems. Paper cards ("documents") create contrast moments.
8. **Motion.**
   - Entrances take 0.3–0.6 s with `OUT`. Exits take 0.2–0.25 s with `IN` plus blur. Moves, morphs and flips use `IN_OUT`, and pops and landings use the `POP`/`DROP` springs. Only progress bars and scrolls are linear.
   - The hero motion of each beat starts on its cue (`OUT`, `POP`), or 4–6 frames before it for `IN_OUT` moves and flips, which are slow to leave their start.
   - **Vary the transitions.** Use at least three kinds, and use a shared-element move (one object becoming the next scene's object) at least twice. Save the boldest for the reveal and the CTA. The kit has:
     - `sceneExit()`: blur-push.
     - `whip()`: a fast sideways pan with blur.
     - `iris()`: a circle opening from a click or logo.
     - `zoomThrough()`: the camera pushes into a point and the next scene settles out of it.
     - shared elements: `DropFlip` + `after`, `CtaMorph`, document → rail.
   - Stagger siblings by 40–100 ms.
   - Overlap scenes by 3–15 frames: the old one exits (`sceneExit`) while the new one enters. A new scene must never land on top of an old one that is still sharp.
   - Something should always be moving (slow push-ins, drift, live counters), but only one hero motion at a time.
   - Render at 60 fps. Fast-changing numbers blur themselves (`CountUp` does this), so there is no motion-blur pass.
9. **Sound.**
   - `whoosh`: scene transitions.
   - `mouse-click`: cursor presses.
   - `switch`: checks.
   - `shutter-modern`: stamps and snips.
   - `whip`: slams.
   - `ding`: completion.

   Volumes are 0.2–0.55, so the voice stays on top. For typing or anything else not in the set, the free soundcn library (github.com/kapishdima/soundcn, `assets/`) has more.
10. **Honesty.** On-screen claims come from the voiceover or the product's own page. Illustrative details (an invoice amount, a timecode, a chat message) must read as illustrations, and the user should hear about them.

Show the plan table to the user and wait for a go-ahead or edits. Skip the wait only if they said to just build it.

### 5. Build

- Make one file per scene in `src/scenes/`, starting from `ExampleScene.tsx`. At the top, set `START = <from frame> / 60` and `CUE = { word: <cue-sheet seconds> - START, … }`. Render `<SceneBackdrop />` first, so the scene shows on the real background when opened alone in Studio.
- Place each scene in `Promo.tsx` on its cue frame:
  - `from` is the first cue frame minus a 0–20 frame lead, so the scene enters just before its word.
  - `durationInFrames` runs to the next scene's start plus the overlap.
- Register every scene in `Root.tsx` under the `Scenes` folder (same fps and size), so it opens on its own timeline in Studio.
- Set Promo's `durationInFrames` to the frame where the voiceover ends (`cues.mjs` prints it) plus about 70.
- Add each sound effect as its own `<Audio>` node in `Promo.tsx`, with `from` at the hit frame.
- Patterns are starting points: change sizes, copy and timing freely, and write new vignettes in the same style.
- Typecheck with `npx tsc --noEmit`.

**Footage.** When a scene shows real video clips (a screen recording, a talking head, before-and-after footage), use `<OffthreadVideo>` from `remotion`, not `@remotion/media`'s `<Video>`. Wrap it in `<Sequence from={…} layout="none">` to start it at a scene-local frame. Pick the source point with `trimBefore` (in frames), set the speed with `playbackRate`, and add `muted` unless the clip's own sound belongs in the mix. Keep the element at the clip's native width and height, and move, scale or crop it with a CSS `transform` inside an `overflow: hidden` box. Never animate its `width` or `height`; to grow the clip, animate the box and the `scale`.

```tsx
<div style={{ position: "absolute", left: box.x, top: box.y, width: box.w, height: box.h, overflow: "hidden", borderRadius: 32 }}>
  <Sequence from={startFrame} layout="none">
    <OffthreadVideo
      src={staticFile("clips/demo.mp4")}
      trimBefore={Math.round(sourceSeconds * fps)}
      muted
      style={{ position: "absolute", left: 0, top: 0, width: CLIP_W, height: CLIP_H, transformOrigin: "0 0", transform: `translate(${x}px, ${y}px) scale(${s})` }}
    />
  </Sequence>
</div>
```

Always check footage in the rendered MP4 (step 6), not only in stills: `<Video>` can look perfect in `remotion still` and still drop frames in a full render (see Troubleshooting).

The user can scrub and tweak in Remotion Studio with `npm run dev`. Studio writes edits back to the code.

### 6. Review frames, fix, render

```bash
node scripts/sheet.mjs 0 600 15
```

That renders frames 0–600 at every 15th frame into `out/sheet-0-600.png`. Read it, then go through the whole video sheet by sheet. Zoom into a scene boundary with a smaller step, e.g. `node scripts/sheet.mjs 150 190 4`. Check, in this order:

1. Each beat's hero motion lands on its word.
2. Hand-offs: no new scene arrives over a still-sharp old one, and there are no dead frames.
3. Text: nothing clips or re-wraps mid-animation. Anything that resizes needs a fixed width or `whiteSpace: "nowrap"`, and nothing jumps off-centre when a suffix appears.
4. Sizes: key text is at least 44 px and inside the safe area.
5. Cursor clicks: the cursor reaches the target, presses, and holds about 0.15 s before it moves on.
6. Scale and balance: nothing important is thumbnail-sized, the lower third isn't empty, and frame 0 already shows the hook.
7. Variety: the hand-offs aren't all the same blur-push.

Render:

```bash
npx remotion render Promo out/promo.mp4 --codec=h264 --crf=16 --image-format=png --color-space=bt709 --pixel-format=yuv420p
```

Check the loudness with `npx remotion ffmpeg -i out/promo.mp4 -vn -af loudnorm=print_format=json -f null -`. `input_i` should be near −14 and `input_tp` below −1. (`-vn` is required: Remotion's ffmpeg can't pass video to the null output.)

**Then check the MP4 itself.** The contact sheet and `remotion still` render each frame on its own, so they can look perfect while the full render drops frames. Always grid frames pulled from the rendered file:

```bash
npx remotion ffmpeg -i out/promo.mp4 -r 2 -vf scale=270:-2 out/check/f%03d.png
```

Create `out/check` first. That writes two frames per second; `f001` is 0 s. To look closer at a stretch, for example around footage, use `-ss 4 -i out/promo.mp4 -t 2 -r 10`. Then write `out/check/grid.html`: a `#202020` page with an 8-column CSS grid of 270 px cells, each holding one frame's file name and its `<img>`. Shoot it with:

```bash
node scripts/capture.mjs shot "file://<absolute path>/out/check/grid.html" out/check/grid.png --width 2192 --height <rows × 510> --dpr 1
```

Read `grid.png`. Every frame should show what the contact sheet showed, with no black or blank footage and no corrupted frames. Delete `out/check` when you're done.

### 7. Deliver

Tell the user:

- where the MP4 is, its length and format;
- how much was cut from the voiceover;
- which on-screen details are illustrative;
- how to tweak it: brand in `src/theme.ts`, timing in `src/Promo.tsx`, each scene in its own file, live preview with `npm run dev`.

## Troubleshooting

- **Renders time out at "Waiting for root component to load", or captures hang.** Remotion's bundled headless Chrome can't paint on some machines (seen on macOS 26). Point Remotion at the installed Chrome in `remotion.config.ts`:
  ```ts
  Config.setBrowserExecutable("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"); // Windows: C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe
  Config.setChromeMode("chrome-for-testing");
  ```
- **Footage is black or blank in random frames of the MP4, but stills look fine.** This was seen with an installed Chrome (155, on macOS). Remotion had no shared-memory capture there, so it fell back to encoded screenshots, and `@remotion/media`'s `<Video>` canvases were randomly missing from them in full renders. Single `remotion still` frames and the contact sheet looked fine. `--gl=swangle` doesn't fix it; it corrupted other frames instead. Switch the clips to `<OffthreadVideo>` from `remotion`, wrapped in `<Sequence from={…} layout="none">`. Keep each one at its native size and move it with a `transform` (see **Footage** in step 5). That rendered clean and about 7× faster. Re-check by gridding frames pulled from the MP4 (step 6).
- **Chrome blocked inside Claude Code's sandbox.** Render and capture commands spawn Chrome, which a sandbox can block. Re-run those commands outside the sandbox.
- **`<HtmlInCanvasMotionBlur>` fails** with "No cached paint record" in a regular Chrome. The kit doesn't need it: render at 60 fps, and fast elements blur themselves.
- **Whisper can't run** (no WebGPU; the scripts exit with code 2). Either install whisper.cpp through `@remotion/install-whisper-cpp` (see the installed `remotion-captions` skill), or ask for the script text. Then run `prep-voiceover.mjs` without `--words` and write `scripts/cues.json` by hand: phrases in order, each starting at the matching island in `scripts/islands.json`.
- **Studio won't start from an app's preview launcher.** Run `npm run dev` in a terminal.
- **Windows.** Every script is plain Node: run them from the project folder in PowerShell, and wrap CSS selectors in double quotes.

## Lessons from the first build

- **Whisper misses non-speech.** It skipped a throat-clear on the first pass and only caught it on a later one. `find-noises.mjs` exists because of this. Never trust a single transcript to find noises.
- **Don't flag noise from Whisper's word times alone.** A sound counts as noise only when both checks agree. On its own, the slice test once flagged the end of "shorts", because Whisper completed the word from its soft "sh".
- **Whisper word onsets run 0.1–0.25 s late.** `cues.mjs` snaps each phrase start to the real onset in the waveform.
- **A mono voiceover plays about 3 LU louder as stereo.** That's why the mono master targets −17 LUFS, which lands near −14 in the rendered video.
- **Cards that resize while flipping re-wrap their text.** Lay the back face out at its final width (`DropFlip` does this).
- **A big price jumps off-centre when its suffix arrives.** Position the suffix absolutely and slide the whole group (`PriceSlam`).
- **With expo-out easing the cursor leaves the instant it clicks,** so the click doesn't read. Cursor paths need holds (`CtaMorph`).
- **A new scene that drops in over the old scene before it blurs looks messy.** Start the old scene's exit first.
- **A contact-sheet composition that is 1 frame long renders empty.** Nested sequences get clipped to the parent's length.
- **Remotion's bundled ffmpeg has no `fps`, `tile` or `select` filters and no raw-PCM output.** Contact sheets therefore render through Remotion, and decoding uses Mediabunny.
- **Some pages never finish painting in headless Chrome.** Captures use anti-throttling flags and time out instead of hanging.
- **A blind test run** (a second agent with only this file, a new voiceover and a different product) produced an on-brand ad, and its notes shaped the kit:
  - rail text and safe-area sizing;
  - the per-row highlight wipe and `until`;
  - focus boxes taken straight from `inspect`;
  - `-vn` in the loudness check and a −2 dBTP mastering ceiling;
  - `inAt`, `after` and `suffix`;
  - the transition helpers.

  Its main criticism was that UI looked small and every hand-off was the same blur-push. Hence the scale, balance and variety rules.

## Reference code

Create each file at the path shown, with this exact content.

### Voiceover and asset scripts

#### `scripts/audio-utils.mjs`

```js
// Shared audio helpers for the voiceover scripts. Node only, no Python or system ffmpeg:
// decoding uses Mediabunny, loudness uses the ffmpeg that ships with Remotion.
import { registerMediabunnyServer } from "@mediabunny/server";
import { ALL_FORMATS, Conversion, FilePathSource, Input, NullTarget, Output, WavOutputFormat } from "mediabunny";
import { spawnSync } from "node:child_process";
import { existsSync, statSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

registerMediabunnyServer();

// Decode any audio/video file to a mono Float32Array at `sampleRate`.
export const decodeMono = async (path, sampleRate) => {
  const chunks = [];
  const input = new Input({ formats: ALL_FORMATS, source: new FilePathSource(path) });
  const track = await input.getPrimaryAudioTrack();
  if (!track) throw new Error(`${path} has no audio track`);
  const conversion = await Conversion.init({
    input,
    output: new Output({ format: new WavOutputFormat(), target: new NullTarget() }),
    video: { discard: true },
    audio: (t) =>
      t.id !== track.id
        ? { discard: true }
        : {
            codec: "pcm-f32",
            forceTranscode: true,
            numberOfChannels: 1,
            sampleFormat: "f32",
            sampleRate,
            process: (sample) => {
              const data = new Float32Array(sample.allocationSize({ format: "f32", planeIndex: 0 }) / 4);
              sample.copyTo(data, { format: "f32", planeIndex: 0 });
              chunks.push({ start: Math.round(sample.timestamp * sampleRate), data });
              return sample;
            },
          },
  });
  if (!conversion.isValid) throw new Error(`Cannot decode ${path}`);
  await conversion.execute();
  const length = chunks.reduce((m, c) => Math.max(m, c.start + c.data.length), 0);
  const out = new Float32Array(length);
  for (const c of chunks) {
    const d = Math.max(0, c.start);
    const s = Math.max(0, -c.start);
    const n = Math.min(c.data.length - s, out.length - d);
    if (n > 0) out.set(c.data.subarray(s, s + n), d);
  }
  return out;
};

// Write mono 16-bit PCM WAV.
export const writeWav = (path, samples, sampleRate) => {
  const buf = Buffer.alloc(44 + samples.length * 2);
  buf.write("RIFF", 0);
  buf.writeUInt32LE(36 + samples.length * 2, 4);
  buf.write("WAVEfmt ", 8);
  buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(1, 20);
  buf.writeUInt16LE(1, 22);
  buf.writeUInt32LE(sampleRate, 24);
  buf.writeUInt32LE(sampleRate * 2, 28);
  buf.writeUInt16LE(2, 32);
  buf.writeUInt16LE(16, 34);
  buf.write("data", 36);
  buf.writeUInt32LE(samples.length * 2, 40);
  for (let i = 0; i < samples.length; i++) {
    buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, samples[i])) * 32767), 44 + i * 2);
  }
  writeFileSync(path, buf);
};

// Run Remotion's bundled ffmpeg and return stderr (where ffmpeg logs).
export const ffmpeg = (args) => {
  const win = process.platform === "win32";
  const r = spawnSync(win ? "npx.cmd" : "npx", ["remotion", "ffmpeg", "-hide_banner", ...args], {
    encoding: "utf8",
    shell: win,
    maxBuffer: 64 * 1024 * 1024,
  });
  if (r.status !== 0) throw new Error(`ffmpeg failed:\n${r.stderr}`);
  return r.stderr;
};

// Loudness of each 10 ms window in dBFS.
export const levelsDb = (samples, sampleRate, windowSec = 0.01) => {
  const hop = Math.round(sampleRate * windowSec);
  const n = Math.floor(samples.length / hop);
  const db = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    let sum = 0;
    for (let j = i * hop; j < (i + 1) * hop; j++) sum += samples[j] * samples[j];
    db[i] = 20 * Math.log10(Math.sqrt(sum / hop) + 1e-9);
  }
  return db;
};

export const percentile = (arr, p) => {
  const s = Array.from(arr).sort((a, b) => a - b);
  return s[Math.min(s.length - 1, Math.max(0, Math.floor((p / 100) * s.length)))];
};

// Runs of speech separated by at least `minGap` seconds of quiet, using an adaptive
// threshold 18 dB under the loud parts (never closer than 6 dB to the noise floor).
export const speechIslands = (db, windowSec = 0.01, minGap = 0.1, forcedQuiet = []) => {
  const ref = percentile(db, 95);
  const floor = percentile(db, 10);
  const thresh = Math.max(ref - 18, floor + 6);
  const loud = Array.from(db, (d, i) => {
    const t = i * windowSec;
    if (forcedQuiet.some(([a, b]) => t >= a && t < b)) return false;
    return d > thresh;
  });
  const islands = [];
  let i = 0;
  const gapFrames = Math.round(minGap / windowSec);
  while (i < loud.length) {
    if (!loud[i]) {
      i++;
      continue;
    }
    let j = i;
    while (j < loud.length) {
      if (loud[j]) {
        j++;
        continue;
      }
      let k = j;
      while (k < loud.length && !loud[k]) k++;
      if (k - j >= gapFrames || k >= loud.length) break;
      j = k;
    }
    islands.push({ start: +(i * windowSec).toFixed(3), end: +(j * windowSec).toFixed(3) });
    i = j;
  }
  return { islands, thresh, ref, floor };
};

// onnxruntime (used by Whisper) can abort while Node shuts down, which turns a successful
// run into a non-zero exit. Call this first in a Whisper script: the script re-runs itself
// in a child process, hides that shutdown noise and exits 0 when `outPath` was written.
export const isolate = (scriptUrl, outPath) => {
  if (process.env.MOTION_PROMO_CHILD) return;
  const started = Date.now();
  const r = spawnSync(process.execPath, [fileURLToPath(scriptUrl), ...process.argv.slice(2)], {
    env: { ...process.env, MOTION_PROMO_CHILD: "1" },
    stdio: ["inherit", "inherit", "pipe"],
    encoding: "utf8",
  });
  const err = (r.stderr ?? "")
    .split("\n")
    .filter((l) => l.trim() && !/onnxruntime|libc\+\+abi|DefaultLogger/.test(l))
    .join("\n");
  if (err) process.stderr.write(`${err}\n`);
  const ok = existsSync(outPath) && statSync(outPath).mtimeMs >= started - 1000;
  process.exit(ok ? 0 : 1);
};
```

#### `scripts/whisper.mjs`

```js
// Thin wrapper around @remotion/whisper-webgpu: load once, transcribe many waveforms.
import {
  WHISPER_WEBGPU_SAMPLE_RATE,
  canUseWhisperWebGpu,
  downloadWhisperModel,
  loadWhisperModel,
  toCaptions,
  transcribe,
} from "@remotion/whisper-webgpu";

export const SR = WHISPER_WEBGPU_SAMPLE_RATE;

export const loadWhisper = async (model) => {
  const support = await canUseWhisperWebGpu();
  if (!support.supported) {
    console.error(`Whisper WebGPU unavailable: ${support.detailedReason}`);
    console.error("Fallback: paste the script text, or export an .srt from your editor (see SKILL.md).");
    process.exit(2);
  }
  await downloadWhisperModel({ model });
  await loadWhisperModel({ model });
};

// Words with start/end seconds (offset added so slices keep file-relative times).
export const wordsOf = async (wave, { model, lang = "en", offset = 0 }) => {
  if (wave.length < SR * 0.1) return [];
  const out = await transcribe({ channelWaveform: wave, model, ...(model.endsWith(".en") ? {} : { language: lang }) });
  return toCaptions({ whisperWebGpuOutput: out }).captions.map((c) => ({
    text: c.text.trim(),
    start: +(c.startMs / 1000 + offset).toFixed(3),
    end: +(c.endMs / 1000 + offset).toFixed(3),
  }));
};
```

#### `scripts/find-noises.mjs`

```js
// Transcribe the raw voiceover and find throat-clears, coughs, breaths and fillers that
// a pause cut would leave behind. A short sound with a pause on both sides counts as
// noise only when two checks agree:
//   1. Whisper hears no new word when the sound is added to the audio before it, and
//   2. no word of the full transcript starts there.
// Usage: node scripts/find-noises.mjs public/voiceover-raw.mp3 [--model small.en] [--lang en]
// Writes scripts/words-raw.json (full transcript) and scripts/noises.json, and prints the
// --drop value for prep-voiceover.mjs.
import { writeFileSync } from "node:fs";
import { decodeMono, isolate, levelsDb, speechIslands } from "./audio-utils.mjs";
import { SR, loadWhisper, wordsOf } from "./whisper.mjs";

const args = process.argv.slice(2);
const flag = (name, fallback) => (args.includes(`--${name}`) ? args[args.indexOf(`--${name}`) + 1] : fallback);
const OUT = "scripts/noises.json";
isolate(import.meta.url, OUT);

const model = flag("model", "small.en");
const lang = flag("lang", "en");
const wave = await decodeMono(args[0], SR);
await loadWhisper(model);

const all = await wordsOf(wave, { model, lang });
writeFileSync("scripts/words-raw.json", JSON.stringify(all, null, 1));
console.log(`Transcript: ${all.map((w) => w.text).join(" ")}\n`);

const FILLER = /^(u+m+|u+h+|e+r+m*|a+h+e*m*|h+m+|m+h*|ah|oh)$/;
const clean = (t) => t.toLowerCase().replace(/[^a-z0-9$']/g, "");
const isWord = (t) => !/^[[(]/.test(t) && clean(t) !== "" && !FILLER.test(clean(t));
const counts = (ws) =>
  ws.filter((w) => isWord(w.text)).reduce((m, w) => m.set(clean(w.text), (m.get(clean(w.text)) ?? 0) + 1), new Map());

const { islands } = speechIslands(levelsDb(wave, SR), 0.01, 0.12);
const slice = (a, b) => wave.subarray(Math.round(a * SR), Math.round(b * SR));
const results = [];
for (let i = 1; i < islands.length; i++) {
  const isl = islands[i];
  const before = isl.start - islands[i - 1].end;
  const after = i + 1 < islands.length ? islands[i + 1].start - isl.end : 1;
  if (isl.end - isl.start > 0.45 || before < 0.15 || after < 0.15) continue;
  // Whisper word starts run late, so look a little past the sound too.
  const wordHere = all.some((w) => isWord(w.text) && w.start >= isl.start - 0.3 && w.start <= isl.end + 0.45);
  const from = Math.max(0, isl.start - 2.2);
  const A = counts(await wordsOf(slice(from, islands[i - 1].end + 0.03), { model, lang }));
  const B = counts(await wordsOf(slice(from, isl.end + 0.06), { model, lang }));
  const added = [...B].filter(([t, n]) => n > (A.get(t) ?? 0)).map(([t]) => t);
  const noise = added.length === 0 && !wordHere;
  results.push({ start: isl.start, end: isl.end, noise, added, wordHere });
  console.log(
    `${isl.start.toFixed(2)}-${isl.end.toFixed(2)}s  ${noise ? "NOISE" : "speech"}  (adds: ${added.join(" ") || "nothing"}; transcript word here: ${wordHere ? "yes" : "no"})`,
  );
}
// Filler words ("um", "uh"): Whisper's times run late, so snap each one to the real sound
// it belongs to, and skip it if that sound was already caught above.
const fillers = all.filter((w) => !/^[[(]/.test(w.text) && FILLER.test(clean(w.text)));
for (const w of fillers) {
  const isl = islands.find((i) => i.start >= w.start - 0.4 && i.start <= w.start + 0.1 && i.end - i.start < 0.8);
  if (!isl) {
    console.log(`"${w.text}" near ${w.start.toFixed(2)}s: could not place it. Check by ear, then add --drop by hand.`);
    continue;
  }
  if (results.some((r) => r.noise && r.start === isl.start)) continue;
  results.push({ start: isl.start, end: isl.end, noise: true, added: [], filler: w.text });
  console.log(`${isl.start.toFixed(2)}-${isl.end.toFixed(2)}s  FILLER "${w.text}"`);
}
writeFileSync(OUT, JSON.stringify(results, null, 1));
const drop = results.filter((r) => r.noise).map((r) => `${(r.start - 0.02).toFixed(2)}-${(r.end + 0.03).toFixed(2)}`);
console.log(drop.length ? `\nDrop with:  --drop ${drop.join(",")}` : "\nNo non-speech sounds found.");
process.exit(0);
```

#### `scripts/prep-voiceover.mjs`

```js
// Tighten a voiceover: shorten every pause, optionally drop non-speech (throat-clears,
// breaths, "um"), master the loudness, and write the timing data the video uses.
//
// Usage:
//   node scripts/prep-voiceover.mjs public/voiceover-raw.mp3 --words scripts/words-raw.json
//   node scripts/prep-voiceover.mjs public/voiceover-raw.mp3 --words scripts/words-raw.json --drop 6.55-7.52
// Flags:
//   --words <json>     raw transcript from transcribe.mjs; used to tell sentence ends from commas
//   --drop a-b,c-d     ranges (seconds in the RAW file) to remove completely
//   --sentence 0.16    seconds of air kept after . ! ?
//   --clause 0.10      seconds of air kept after , ; : and between list items
//   --lufs -17         loudness target for the mono file (plays about 3 LU louder as stereo)
//   --no-cut           keep the original pacing, only master + analyse
// Writes:
//   public/voiceover.wav           the edited, mastered voiceover the video plays
//   src/voiceover-envelope.json    loudness 0..1, 60 values per second (drives audio-reactive visuals)
//   scripts/islands.json           speech runs in the edited file (exact onsets for cue timing)
//   scripts/cut-map.json           raw -> edited time map
import { existsSync, readFileSync, unlinkSync, writeFileSync } from "node:fs";
import { decodeMono, ffmpeg, levelsDb, percentile, speechIslands, writeWav } from "./audio-utils.mjs";

const args = process.argv.slice(2);
const flag = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i === -1 ? fallback : args[i + 1];
};
const src = args[0];
const SR = 48000;
const SENTENCE = Number(flag("sentence", 0.16));
const CLAUSE = Number(flag("clause", 0.1));
const LUFS = Number(flag("lufs", -17));
const noCut = args.includes("--no-cut");
const drops = (flag("drop", "") || "")
  .split(",")
  .filter(Boolean)
  .map((r) => r.split("-").map(Number));
const wordsPath = flag("words", null);
const words = wordsPath && existsSync(wordsPath) ? JSON.parse(readFileSync(wordsPath, "utf8")) : [];

const raw = await decodeMono(src, SR);
const rawDur = raw.length / SR;
const rawDb = levelsDb(raw, SR);
const { islands, ref, floor } = speechIslands(rawDb, 0.01, 0.1, drops);
// Soft sounds (s, sh, f, breath tails) sit under the speech threshold. Trim each pause to
// where the audio is truly quiet so they are never clipped.
const low = Math.max(floor + 10, ref - Number(flag("soft", 30)));
const dropped = (t) => drops.some(([a, b]) => t >= a && t < b);
const quiet = (t) => dropped(t) || (rawDb[Math.floor(t * 100)] ?? -200) <= low;
if (islands.length === 0) throw new Error("No speech found");

// Classify each pause by the punctuation of the word just before it.
const kindBefore = (t) => {
  const prev = words.filter((w) => w.start < t + 0.05).pop();
  if (!prev) return null;
  if (/[.!?…]["')\]]*$/.test(prev.text)) return "sentence";
  if (/[,;:—–-]["')\]]*$/.test(prev.text)) return "clause";
  return "mid";
};

const cuts = []; // [start, end) removed from the raw file
const gaps = [];
if (!noCut) {
  cuts.push([0, Math.max(0, islands[0].start - 0.05)]);
  for (let i = 0; i < islands.length - 1; i++) {
    let s = islands[i].end;
    let e = islands[i + 1].start;
    while (s < e && !quiet(s)) s += 0.01;
    while (e > s && !quiet(e - 0.01)) e -= 0.01;
    const dur = e - s;
    const dropped = drops.some(([a, b]) => a < e && b > s);
    let kind = words.length ? kindBefore(s) : dur > 0.45 ? "sentence" : "clause";
    if (dropped && kind === "mid") kind = "clause";
    let keep = kind === "sentence" ? SENTENCE : kind === "clause" ? CLAUSE : dur > 0.3 ? 0.12 : dur;
    keep = Math.min(keep, dur);
    // Pauses under 0.2 s can sit inside a word (a stop consonant); leave them alone.
    if (dur >= 0.2 && dur - keep > 0.02) {
      cuts.push([s + keep * 0.6, e - keep * 0.4]);
      gaps.push({ at: +s.toFixed(2), was: +dur.toFixed(2), kept: +keep.toFixed(2), kind });
    }
  }
  cuts.push([Math.min(rawDur, islands[islands.length - 1].end + 0.3), rawDur]);
}

// Keep everything that is not cut, with 8 ms fades at every join.
const keeps = [];
let cursor = 0;
for (const [a, b] of cuts.filter(([a, b]) => b - a > 0.001).sort((x, y) => x[0] - y[0])) {
  if (a > cursor) keeps.push([cursor, a]);
  cursor = Math.max(cursor, b);
}
if (cursor < rawDur) keeps.push([cursor, rawDur]);

const fade = Math.round(0.008 * SR);
const pieces = [];
const cutMap = [];
let total = 0;
keeps.forEach(([a, b], i) => {
  const seg = raw.slice(Math.round(a * SR), Math.round(b * SR));
  for (let k = 0; k < Math.min(fade, seg.length); k++) {
    const g = k / fade;
    if (i > 0) seg[k] *= g;
    if (i < keeps.length - 1) seg[seg.length - 1 - k] *= g;
  }
  cutMap.push({ rawStart: +a.toFixed(3), rawEnd: +b.toFixed(3), start: +(total / SR).toFixed(3) });
  pieces.push(seg);
  total += seg.length;
});
const edited = new Float32Array(total);
let off = 0;
for (const p of pieces) {
  edited.set(p, off);
  off += p.length;
}

// Two-pass loudness normalisation with Remotion's ffmpeg.
const tmp = "public/.voiceover-cut.wav";
writeWav(tmp, edited, SR);
// TP -2: the stereo AAC render adds ~0.6 dB of true peak, so this lands under -1 dBTP.
const filter = `loudnorm=I=${LUFS}:TP=-2:LRA=11`;
const pass1 = ffmpeg(["-i", tmp, "-af", `${filter}:print_format=json`, "-f", "null", "-"]);
const m = JSON.parse(pass1.slice(pass1.lastIndexOf("{"), pass1.lastIndexOf("}") + 1));
ffmpeg([
  "-y",
  "-i",
  tmp,
  "-af",
  `${filter}:measured_I=${m.input_i}:measured_TP=${m.input_tp}:measured_LRA=${m.input_lra}:measured_thresh=${m.input_thresh}:offset=${m.target_offset}`,
  "-ar",
  "48000",
  "-ac",
  "1",
  "-c:a",
  "pcm_s16le",
  "public/voiceover.wav",
]);
unlinkSync(tmp);

// Analyse the final file: exact speech onsets + a 60 fps loudness envelope.
const final = await decodeMono("public/voiceover.wav", SR);
const finalIslands = speechIslands(levelsDb(final, SR), 0.01, 0.06).islands;
const env60 = levelsDb(final, SR, 1 / 60);
const envRef = percentile(env60, 97);
const envelope = Array.from(env60, (d) => +Math.max(0, Math.min(1, (d - (envRef - 40)) / 40)).toFixed(3));
writeFileSync("src/voiceover-envelope.json", JSON.stringify(envelope));
writeFileSync("scripts/islands.json", JSON.stringify(finalIslands, null, 1));
writeFileSync("scripts/cut-map.json", JSON.stringify(cutMap, null, 1));

// Report.
console.log(`\n${rawDur.toFixed(2)}s -> ${(final.length / SR).toFixed(2)}s  (${gaps.length} pauses shortened)`);
for (const g of gaps) console.log(`  pause at ${g.at}s  ${g.was}s -> ${g.kept}s  (${g.kind ?? "?"})`);
const filler = /^[[(]|^(u+m+|u+h+|e+r+m*|a+h+e+m+|h+m+)[.,!?]*$/i;
const fillers = words.filter((w) => filler.test(w.text) && !drops.some(([a, b]) => w.start < b + 0.4 && w.end > a));
if (fillers.length) {
  console.log("\nFiller words in the transcript (raw seconds). Add the ones you want gone to --drop:");
  for (const w of fillers) console.log(`  ${w.start.toFixed(2)}-${w.end.toFixed(2)}  "${w.text}"`);
}
console.log("\nNext: node scripts/transcribe.mjs public/voiceover.wav scripts/words.json && node scripts/cues.mjs");
```

#### `scripts/transcribe.mjs`

```js
// Local Whisper transcription with word timings (on your GPU, nothing is uploaded).
// Usage: node scripts/transcribe.mjs <audio> <out.json> [--model small.en] [--lang en] [--from 6.4 --to 7.2]
//   --model  small.en (default, English) | small (other languages, add --lang es) | medium.en (slower, more accurate)
//   --from/--to  only transcribe that slice
import { writeFileSync } from "node:fs";
import { decodeMono, isolate } from "./audio-utils.mjs";
import { SR, loadWhisper, wordsOf } from "./whisper.mjs";

const args = process.argv.slice(2);
const flag = (name, fallback) => (args.includes(`--${name}`) ? args[args.indexOf(`--${name}`) + 1] : fallback);
const [src, out] = args;
isolate(import.meta.url, out);

const model = flag("model", "small.en");
const from = Number(flag("from", 0));
const to = flag("to", null);
const wave = await decodeMono(src, SR);
await loadWhisper(model);
const words = await wordsOf(wave.subarray(Math.round(from * SR), to === null ? wave.length : Math.round(Number(to) * SR)), {
  model,
  lang: flag("lang", "en"),
  offset: from,
});
writeFileSync(out, JSON.stringify(words, null, 1));
console.log(words.map((w) => w.text).join(" "));
process.exit(0);
```

#### `scripts/cues.mjs`

```js
// Cue sheet: every phrase of the edited voiceover with the exact second (and frame)
// it starts. Whisper word times run ~0.1-0.25 s late, so each phrase start is snapped
// to the real speech onset found in the waveform (scripts/islands.json).
// Usage: node scripts/cues.mjs [--fps 60]
import { readFileSync, writeFileSync } from "node:fs";

const fpsIdx = process.argv.indexOf("--fps");
const fps = fpsIdx === -1 ? 60 : Number(process.argv[fpsIdx + 1]);
const words = JSON.parse(readFileSync("scripts/words.json", "utf8"));
const islands = JSON.parse(readFileSync("scripts/islands.json", "utf8"));

const snap = (t) => {
  const near = islands.filter((i) => i.start > t - 0.4 && i.start < t + 0.12);
  return near.length ? near[near.length - 1].start : t;
};

const phrases = [];
let cur = null;
for (const w of words) {
  if (!cur) cur = { words: [], start: snap(w.start) };
  cur.words.push(w);
  if (/[.!?,;:…]["')\]]*$/.test(w.text)) {
    phrases.push(cur);
    cur = null;
  }
}
if (cur) phrases.push(cur);

const cues = phrases.map((p, i) => {
  const next = phrases[i + 1];
  const lastWord = p.words[p.words.length - 1];
  const end = Math.min(lastWord.end + 0.15, next ? next.start : Infinity);
  return {
    i: i + 1,
    start: +p.start.toFixed(2),
    end: +end.toFixed(2),
    frame: Math.round(p.start * fps),
    text: p.words.map((w) => w.text).join(" "),
    words: p.words.map((w) => ({ text: w.text, at: +w.start.toFixed(2) })),
  };
});
writeFileSync("scripts/cues.json", JSON.stringify(cues, null, 1));

const last = islands[islands.length - 1];
console.log(`fps ${fps}   voiceover ends at ${last.end.toFixed(2)}s (frame ${Math.round(last.end * fps)})\n`);
console.log(" #   start   frame   text");
for (const c of cues) {
  console.log(`${String(c.i).padStart(2)}  ${c.start.toFixed(2).padStart(6)}  ${String(c.frame).padStart(6)}   ${c.text}`);
}
console.log("\nWord times inside a phrase are Whisper's (about 0.15 s late); phrase starts are exact.");
```

#### `scripts/capture.mjs`

```js
// Real screenshots, logo crops and brand colours from a website, via headless Chrome.
//
//   node scripts/capture.mjs inspect <url> [--mobile]
//       Title, theme colour, icons, images, buttons (text, colours, font, border, radius, shadow).
//       Boxes are CSS px at the capture width (1280 desktop, 430 with --mobile): pass them
//       straight to PhoneShowcase/BrowserShowcase `focus` from the same kind of capture.
//   node scripts/capture.mjs shot <url> <out.png> [--mobile] [--width 430] [--height 1600] [--dpr 3] [--wait 8]
//       Viewport screenshot. --mobile emulates an iPhone (430 px wide by default).
//       Desktop default: --width 1280 --height 1800 --dpr 2.
//   node scripts/capture.mjs element <url> "<css selector>" <out.png> [--dpr 8] [--width 1280] [--transparent]
//       Tight high-resolution crop of one element (a logo, a button, a pricing card).
//       --transparent clears the page/header background behind it (good for logos on dark video).
//
// Finds Chrome, Edge, Brave or Chromium on macOS, Windows or Linux; set CHROME_PATH to
// override. Every step has a timeout, so it never hangs. Only capture pages you are allowed
// to show (your own product, or public pages you are referencing).
import { spawn } from "node:child_process";
import { existsSync, mkdirSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";

const args = process.argv.slice(2);
const flag = (name, fallback) => (args.includes(`--${name}`) ? args[args.indexOf(`--${name}`) + 1] : fallback);
const [mode, url] = args;

const findChrome = () => {
  const env = process.env;
  const candidates = [
    env.CHROME_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    env.PROGRAMFILES && join(env.PROGRAMFILES, "Google/Chrome/Application/chrome.exe"),
    env["PROGRAMFILES(X86)"] && join(env["PROGRAMFILES(X86)"], "Google/Chrome/Application/chrome.exe"),
    env.LOCALAPPDATA && join(env.LOCALAPPDATA, "Google/Chrome/Application/chrome.exe"),
    env["PROGRAMFILES(X86)"] && join(env["PROGRAMFILES(X86)"], "Microsoft/Edge/Application/msedge.exe"),
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ];
  const shellDir = "node_modules/.remotion/chrome-headless-shell";
  if (existsSync(shellDir)) {
    for (const plat of readdirSync(shellDir)) {
      for (const sub of readdirSync(join(shellDir, plat))) {
        for (const exe of ["chrome-headless-shell", "chrome-headless-shell.exe"]) candidates.push(join(shellDir, plat, sub, exe));
      }
    }
  }
  const found = candidates.find((c) => c && existsSync(c));
  if (!found) throw new Error("No Chrome/Edge found. Install Chrome, set CHROME_PATH, or run `npx remotion browser ensure`.");
  return found;
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const withTimeout = (p, ms, what) =>
  Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error(`Timed out: ${what}`)), ms))]);

const port = 9300 + Math.floor(Math.random() * 600);
const profile = join(tmpdir(), `motion-promo-capture-${port}`);
const chrome = spawn(
  findChrome(),
  [
    "--headless=new",
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${profile}`,
    "--no-first-run",
    "--hide-scrollbars",
    "--disable-background-timer-throttling",
    "--disable-renderer-backgrounding",
    "--disable-backgrounding-occluded-windows",
    "about:blank",
  ],
  { stdio: "ignore" },
);
const cleanup = () => {
  chrome.kill();
  setTimeout(() => rmSync(profile, { recursive: true, force: true }), 500);
};
setTimeout(() => {
  console.error("Gave up after 90 s.");
  cleanup();
  process.exit(1);
}, 90000).unref();

let targets;
for (let i = 0; i < 75 && !targets; i++) {
  try {
    targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
  } catch {
    await sleep(200);
  }
}
const ws = new WebSocket(targets.find((t) => t.type === "page").webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0;
const pending = new Map();
ws.addEventListener("message", (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) {
    pending.get(m.id)(m.error ? Promise.reject(new Error(m.error.message)) : m.result);
    pending.delete(m.id);
  }
});
const send = (method, params = {}) =>
  withTimeout(
    new Promise((r) => {
      const i = ++id;
      pending.set(i, r);
      ws.send(JSON.stringify({ id: i, method, params }));
    }),
    30000,
    method,
  );
const evaluate = async (expression) => (await send("Runtime.evaluate", { expression, returnByValue: true })).result.value;

const mobile = args.includes("--mobile");
const width = Number(flag("width", mobile ? 430 : 1280));
const height = Number(flag("height", mobile ? 1600 : 1800));
const dpr = Number(flag("dpr", mode === "element" ? 8 : mobile ? 3 : 2));
await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: dpr, mobile });
if (mobile) {
  await send("Emulation.setUserAgentOverride", {
    userAgent:
      "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
  });
}
await send("Page.enable");
await send("Page.navigate", { url });
await sleep(Number(flag("wait", 8)) * 1000);

const save = (out, data) => {
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, Buffer.from(data, "base64"));
  console.log(`saved ${out}`);
};

if (mode === "shot") {
  save(args[2], (await send("Page.captureScreenshot", { format: "png" })).data);
} else if (mode === "element") {
  const sel = JSON.stringify(args[2]);
  const box = await evaluate(
    `(() => { const el = document.querySelector(${sel}); if (!el) return null; el.scrollIntoView({block: "center"}); const r = el.getBoundingClientRect(); return {x: r.x + scrollX, y: r.y + scrollY, width: r.width, height: r.height}; })()`,
  );
  if (!box) throw new Error(`No element matches ${args[2]}`);
  if (args.includes("--transparent")) {
    await send("Emulation.setDefaultBackgroundColorOverride", { color: { r: 0, g: 0, b: 0, a: 0 } });
    await evaluate(
      `(() => { for (let el = document.querySelector(${sel}); el; el = el.parentElement) { el.style.setProperty("background", "transparent", "important"); el.style.setProperty("box-shadow", "none", "important"); } })()`,
    );
  }
  await sleep(500);
  const shot = await send("Page.captureScreenshot", {
    format: "png",
    captureBeyondViewport: true,
    clip: { ...box, scale: 1 },
  });
  save(args[3], shot.data);
} else if (mode === "inspect") {
  const info = await evaluate(`(() => {
    const box = (el) => { const r = el.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; };
    const colors = {};
    for (const el of document.querySelectorAll("button, a, [class*=btn], [class*=button], header, nav")) {
      const cs = getComputedStyle(el);
      for (const c of [cs.backgroundColor, cs.color]) if (c && !/rgba\\(0, 0, 0, 0\\)/.test(c)) colors[c] = (colors[c] || 0) + 1;
    }
    return {
      title: document.title,
      themeColor: document.querySelector('meta[name="theme-color"]')?.content ?? null,
      ogImage: document.querySelector('meta[property="og:image"]')?.content ?? null,
      icons: [...document.querySelectorAll('link[rel*="icon"]')].map((l) => ({ rel: l.rel, href: l.href, sizes: l.sizes?.value })),
      viewportWidth: innerWidth,
      font: getComputedStyle(document.body).fontFamily,
      buttons: [...document.querySelectorAll("button, a")].filter((b) => b.innerText.trim() && getComputedStyle(b).backgroundColor !== "rgba(0, 0, 0, 0)").slice(0, 12)
        .map((b) => { const cs = getComputedStyle(b); return { text: b.innerText.trim().slice(0, 40), bg: cs.backgroundColor, color: cs.color, font: cs.fontFamily, fontSize: cs.fontSize, fontWeight: cs.fontWeight, border: cs.border, radius: cs.borderRadius, shadow: cs.boxShadow, box: box(b) }; }),
      images: [...document.querySelectorAll("img, svg")].filter((i) => i.getBoundingClientRect().width > 16).slice(0, 25)
        .map((i) => ({ tag: i.tagName, src: i.currentSrc || null, alt: i.getAttribute("alt"), cls: (i.getAttribute("class") || "").slice(0, 60), box: box(i) })),
      topColors: Object.entries(colors).sort((a, b) => b[1] - a[1]).slice(0, 12),
    };
  })()`);
  console.log(JSON.stringify(info, null, 1));
} else {
  console.error("Mode must be inspect, shot or element");
}
ws.close();
cleanup();
process.exit(0);
```

#### `scripts/logos.mjs`

```js
// Fetch brand logos from Simple Icons (3,000+ brands, CC0 SVGs) into public/logos/.
// Usage: node scripts/logos.mjs youtubeshorts tiktok instagram stripe notion
//        node scripts/logos.mjs --search "premiere"     (find a slug)
// Prints each logo's official brand colour. The SVGs are single-colour; tint them with
// <BrandIcon> (src/components/Kit.tsx). Simple Icons drops some brands at the owner's
// request (Adobe, CapCut, Skool...): crop those from the brand's site with capture.mjs.
import { mkdirSync, writeFileSync } from "node:fs";

const VERSION = "16.35.0";
const BASE = `https://cdn.jsdelivr.net/npm/simple-icons@${VERSION}`;
const args = process.argv.slice(2);
const data = await (await fetch(`${BASE}/data/simple-icons.json`)).json();
const slugOf = (d) =>
  d.slug ??
  d.title
    .toLowerCase()
    .replace(/\+/g, "plus")
    .replace(/\./g, "dot")
    .replace(/&/g, "and")
    .normalize("NFD")
    .replace(/[^a-z0-9]/g, "");

if (args[0] === "--search") {
  const q = args[1].toLowerCase();
  for (const d of data.filter((d) => d.title.toLowerCase().includes(q))) console.log(`${slugOf(d).padEnd(28)} ${d.title}  #${d.hex}`);
  process.exit(0);
}

mkdirSync("public/logos", { recursive: true });
for (const slug of args) {
  const meta = data.find((d) => slugOf(d) === slug);
  const res = await fetch(`${BASE}/icons/${slug}.svg`);
  if (!res.ok || !meta) {
    console.log(`${slug}: not in Simple Icons. Try --search, or crop it from the brand's site.`);
    continue;
  }
  writeFileSync(`public/logos/${slug}.svg`, await res.text());
  console.log(`public/logos/${slug}.svg   ${meta.title}   brand colour #${meta.hex}`);
}
```

#### `scripts/sfx.mjs`

```js
// Download Remotion's free sound effects into public/sfx/.
// Usage: node scripts/sfx.mjs            (the standard set)
//        node scripts/sfx.mjs ding whip  (specific ones)
import { mkdirSync, writeFileSync } from "node:fs";

const names = process.argv.slice(2).length
  ? process.argv.slice(2)
  : ["whoosh", "whip", "mouse-click", "switch", "ding", "page-turn", "shutter-modern"];
mkdirSync("public/sfx", { recursive: true });
for (const n of names) {
  const res = await fetch(`https://remotion.media/${n}.wav`);
  if (!res.ok) {
    console.log(`${n}: not found`);
    continue;
  }
  writeFileSync(`public/sfx/${n}.wav`, Buffer.from(await res.arrayBuffer()));
  console.log(`public/sfx/${n}.wav`);
}
```

#### `scripts/sheet.mjs`

```js
// Render a contact sheet of the Promo: one image with a frame every `step` frames.
// Usage: node scripts/sheet.mjs <fromFrame> <toFrame> [step=15] [cols=8]  -> out/sheet-<from>-<to>.png
// Then open the PNG (Claude: Read it) to check timing, layout and transitions.
import { spawnSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";

const [from, to, step = 15, cols = 8] = process.argv.slice(2).map(Number);
mkdirSync("out", { recursive: true });
writeFileSync("out/.sheet-props.json", JSON.stringify({ from, to, step, cols }));
const out = `out/sheet-${from}-${to}.png`;
const win = process.platform === "win32";
const r = spawnSync(win ? "npx.cmd" : "npx", ["remotion", "still", "ContactSheet", out, "--props=out/.sheet-props.json", "--log=error"], {
  stdio: "inherit",
  shell: win,
});
if (r.status === 0) console.log(`saved ${out}`);
process.exit(r.status ?? 1);
```

### Kit

#### `src/theme.ts`

```ts
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import { loadFont as loadSerif } from "@remotion/google-fonts/InstrumentSerif";
import { loadFont as loadMono } from "@remotion/google-fonts/JetBrainsMono";
import { Easing } from "remotion";

// ─── Brand: the only block to change per video ─────────────────────────────
// Sample these from the product's site/logo (scripts/capture.mjs inspect).
export const BRAND = {
  name: "Your Product",
  accent: "#FED605", // hero colour: highlights, checks, key numbers
  accentInk: "#141414", // text that sits ON the accent colour
  alert: "#FF4D4D", // problems: clipping, crossed-out prices, stamps
  success: "#3CE08A", // online dots, finished states
};

// Display fonts. Swap for the brand's own Google Font if it has one
// (e.g. @remotion/google-fonts/Manrope). Keep one sans, one accent serif, one mono.
export const { fontFamily: SANS } = loadInter("normal", {
  weights: ["500", "600", "700", "800", "900"],
  subsets: ["latin"],
});
export const { fontFamily: SERIF } = loadSerif("italic", { weights: ["400"], subsets: ["latin"] });
export const { fontFamily: MONO } = loadMono("normal", { weights: ["400", "500", "700"], subsets: ["latin"] });

// ─── Palette: dark stage + one accent + paper for contrast moments ─────────
export const C = {
  bg: "#09090B",
  surface: "#121215",
  surface2: "#1A1A1F",
  surface3: "#24242B",
  line: "rgba(255,255,255,0.08)",
  line2: "rgba(255,255,255,0.14)",
  text: "#F6F5F2",
  muted: "#8B8B93",
  dim: "#55555D",
  paper: "#F4F2EC",
  ink: "#141414",
  accent: BRAND.accent,
  accentInk: BRAND.accentInk,
  alert: BRAND.alert,
  success: BRAND.success,
} as const;

export const alpha = (hex: string, a: number) => {
  const n = parseInt(hex.replace("#", ""), 16);
  return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
};

// ─── Motion vocabulary ──────────────────────────────────────────────────────
export const CLAMP = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const OUT = Easing.bezier(0.16, 1, 0.3, 1); // entrances (expo out)
export const IN = Easing.bezier(0.7, 0, 0.84, 0); // exits (expo in)
export const IN_OUT = Easing.bezier(0.87, 0, 0.13, 1); // moves, morphs, flips
export const SOFT = Easing.bezier(0.45, 0, 0.2, 1); // cursor paths, gentle drifts
export const POP = Easing.spring({ damping: 11, mass: 0.7, stiffness: 170 }); // overshoot pops
export const DROP = Easing.spring({ damping: 13, mass: 0.8 }); // things that fall and land

export const SHADOW =
  "0 2px 4px rgba(0,0,0,0.25), 0 24px 60px rgba(0,0,0,0.45), 0 60px 140px rgba(0,0,0,0.35)";
```

#### `src/lib/audio.ts`

```ts
import { createContext, useContext } from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import envelope from "../voiceover-envelope.json";

// Global frame of the main video. Scenes read it so on-screen audio visuals
// follow the voiceover even though their own useCurrentFrame() is local.
export const AudioClock = createContext<number | null>(null);

// 0..1 loudness of the voiceover at a time in seconds (60 samples per second).
export const vo = (sec: number) => {
  const i = sec * 60;
  const a = envelope[Math.max(0, Math.min(envelope.length - 1, Math.floor(i)))] ?? 0;
  const b = envelope[Math.max(0, Math.min(envelope.length - 1, Math.ceil(i)))] ?? 0;
  return a + (b - a) * (i - Math.floor(i));
};

export const useVoTime = () => {
  const local = useCurrentFrame();
  const { fps } = useVideoConfig();
  const global = useContext(AudioClock);
  return (global ?? local) / fps;
};
```

#### `src/components/Background.tsx`

```tsx
import { noise2D } from "@remotion/noise";
import React, { useContext } from "react";
import { AbsoluteFill, Interactive, useCurrentFrame, useVideoConfig, type InteractivitySchema } from "remotion";
import { AudioClock } from "../lib/audio";
import { C, alpha } from "../theme";

// Film grain as an inline SVG tile: no image file needed.
const GRAIN = `url("data:image/svg+xml;utf8,${encodeURIComponent(
  "<svg xmlns='http://www.w3.org/2000/svg' width='256' height='256'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='256' height='256' filter='url(#n)'/></svg>",
)}")`;

type BackgroundProps = { readonly glow: string };

// One continuous dark stage under every scene: drifting brand glow, cool counter-glow,
// faint dot grid, vignette and moving grain. Cuts feel like moves within one space.
const BackgroundInner: React.FC<BackgroundProps> = ({ glow }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const g = Math.floor(frame / 2); // grain changes every other frame, like film
  return (
    <>
      <AbsoluteFill style={{ backgroundColor: C.bg }} />
      <AbsoluteFill
        style={{
          background: `radial-gradient(60% 38% at ${50 + noise2D("gx", t * 0.12, 0) * 22}% ${34 + noise2D("gy", t * 0.12, 0) * 14}%, ${glow}, transparent 70%)`,
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(55% 30% at ${60 + noise2D("cx", t * 0.1, 3) * 25}% ${78 + noise2D("cy", t * 0.1, 3) * 10}%, rgba(110,130,255,0.07), transparent 70%)`,
        }}
      />
      <AbsoluteFill
        style={{
          backgroundImage: "radial-gradient(rgba(255,255,255,0.09) 1.6px, transparent 1.8px)",
          backgroundSize: "54px 54px",
          backgroundPosition: `${(t * 6) % 54}px ${(t * 10) % 54}px`,
          maskImage: "radial-gradient(70% 55% at 50% 45%, black 20%, transparent 80%)",
          WebkitMaskImage: "radial-gradient(70% 55% at 50% 45%, black 20%, transparent 80%)",
          opacity: 0.55,
        }}
      />
      <AbsoluteFill style={{ background: "radial-gradient(120% 80% at 50% 45%, transparent 55%, rgba(0,0,0,0.55) 100%)" }} />
      <AbsoluteFill
        style={{
          backgroundImage: GRAIN,
          backgroundSize: "256px 256px",
          backgroundPosition: `${(g * 97) % 256}px ${(g * 61) % 256}px`,
          mixBlendMode: "overlay",
          opacity: 0.22,
        }}
      />
    </>
  );
};

export const Background = Interactive.withSchema({
  Component: BackgroundInner,
  componentName: "Background",
  schema: {
    glow: { type: "color", default: alpha(C.accent, 0.1), description: "Glow color" },
  } as const satisfies InteractivitySchema,
  wrapInSequence: true,
  layout: "absolute-fill",
});

// Put this first in every scene: it draws the background only when the scene is opened
// on its own in Studio (inside Promo the shared background is already there).
export const SceneBackdrop: React.FC = () => {
  const inPromo = useContext(AudioClock) !== null;
  return inPromo ? null : <Background glow={alpha(C.accent, 0.1)} />;
};
```

#### `src/components/Kit.tsx`

```tsx
import React from "react";
import { Img, interpolate, staticFile } from "remotion";
import { vo } from "../lib/audio";
import { C, CLAMP, MONO, OUT, SANS } from "../theme";

// macOS-style arrow cursor. By default (x, y) is the image's top-left and the tip sits at
// (x + 12, y + 6); pass `tip` to position the tip itself. `press` 0..1 squashes it on click.
export const Cursor: React.FC<{ readonly x: number; readonly y: number; readonly press: number; readonly opacity?: number; readonly tip?: boolean }> = ({
  x,
  y,
  press,
  opacity = 1,
  tip = false,
}) => (
  <svg
    width={64}
    height={64}
    viewBox="0 0 32 32"
    style={{
      position: "absolute",
      left: tip ? x - 12 : x,
      top: tip ? y - 6 : y,
      opacity,
      scale: String(1 - press * 0.14),
      transformOrigin: "6px 4px",
      filter: "drop-shadow(0 6px 10px rgba(0,0,0,0.45))",
      zIndex: 50,
    }}
  >
    <path
      d="M6 3 L6 25 L11.5 19.8 L15.2 28 L19 26.4 L15.4 18.4 L23 18.4 Z"
      fill="#0B0B0C"
      stroke="#FFFFFF"
      strokeWidth={1.8}
      strokeLinejoin="round"
    />
  </svg>
);

// Check mark that draws itself (progress 0..1).
export const Check: React.FC<{ readonly size: number; readonly progress: number; readonly color: string; readonly stroke?: number }> = ({
  size,
  progress,
  color,
  stroke = 3.2,
}) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <path
      d="M5 12.5 L10 17.5 L19.5 7"
      fill="none"
      stroke={color}
      strokeWidth={stroke}
      strokeLinecap="round"
      strokeLinejoin="round"
      pathLength={1}
      strokeDasharray={1}
      strokeDashoffset={1 - progress}
    />
  </svg>
);

// A word that slides up from behind a mask. Pass the parent's time `t` and the start `at`.
export const RevealWord: React.FC<{
  readonly children: React.ReactNode;
  readonly t: number;
  readonly at: number;
  readonly dur?: number;
  readonly style?: React.CSSProperties;
}> = ({ children, t, at, dur = 0.5, style }) => (
  <span style={{ display: "inline-block", overflow: "hidden", verticalAlign: "top", paddingBottom: "0.08em", marginBottom: "-0.08em" }}>
    <span
      style={{
        display: "inline-block",
        translate: `0 ${interpolate(t, [at, at + dur], [105, 0], { ...CLAMP, easing: OUT })}%`,
        ...style,
      }}
    >
      {children}
    </span>
  </span>
);

export const MonoLabel: React.FC<{ readonly children: React.ReactNode; readonly color?: string; readonly size?: number; readonly style?: React.CSSProperties }> = ({
  children,
  color = C.muted,
  size = 24,
  style,
}) => (
  <div style={{ fontFamily: MONO, fontSize: size, letterSpacing: "0.18em", textTransform: "uppercase", color, ...style }}>{children}</div>
);

export const Pill: React.FC<{ readonly children: React.ReactNode; readonly bg?: string; readonly color?: string; readonly style?: React.CSSProperties }> = ({
  children,
  bg = C.surface3,
  color = C.text,
  style,
}) => (
  <div
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 12,
      padding: "12px 24px",
      borderRadius: 999,
      backgroundColor: bg,
      color,
      fontFamily: SANS,
      fontWeight: 600,
      fontSize: 30,
      ...style,
    }}
  >
    {children}
  </div>
);

// Single-colour Simple Icons SVG (public/logos/<slug>.svg), tinted with any colour.
export const BrandIcon: React.FC<{ readonly src: string; readonly size: number; readonly color: string; readonly style?: React.CSSProperties }> = ({
  src,
  size,
  color,
  style,
}) => (
  <div
    style={{
      width: size,
      height: size,
      backgroundColor: color,
      maskImage: `url(${staticFile(src)})`,
      WebkitMaskImage: `url(${staticFile(src)})`,
      maskSize: "contain",
      WebkitMaskSize: "contain",
      maskRepeat: "no-repeat",
      WebkitMaskRepeat: "no-repeat",
      maskPosition: "center",
      WebkitMaskPosition: "center",
      ...style,
    }}
  />
);

// Full-colour logo image (a crop from capture.mjs, or the brand's own PNG/SVG).
export const Logo: React.FC<{ readonly src: string; readonly height: number; readonly radius?: number; readonly style?: React.CSSProperties }> = ({
  src,
  height,
  radius = 0,
  style,
}) => <Img src={staticFile(src)} style={{ height, width: "auto", borderRadius: radius, display: "block", ...style }} />;

// Bars that move with the voiceover's loudness: a talking mouth, a mini waveform, a
// level meter. `voT` is the voiceover time from useVoTime().
export const VoiceBars: React.FC<{
  readonly voT: number;
  readonly bars?: number;
  readonly width: number;
  readonly height: number;
  readonly color: string;
  readonly lag?: number;
}> = ({ voT, bars = 9, width, height, color, lag = 0.012 }) => (
  <div style={{ width, height, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
    {Array.from({ length: bars }, (_, i) => {
      const centre = 1 - Math.abs(i - (bars - 1) / 2) / ((bars - 1) / 2 || 1);
      const level = vo(voT - i * lag);
      return (
        <div
          key={i}
          style={{
            width: (width / bars) * 0.55,
            height: `${Math.min(1, 0.12 + (0.25 + 0.75 * centre) * level) * 100}%`,
            borderRadius: width,
            backgroundColor: color,
          }}
        />
      );
    })}
  </div>
);
```

#### `src/components/Odometer.tsx`

```tsx
import React from "react";
import { Easing } from "remotion";

export type Place = { readonly unit: number; readonly base: number };

const snap = Easing.bezier(0.65, 0, 0.35, 1);

// Continuous digit positions with real odometer carry: a digit only moves while
// the digit below it rolls from its last value back to 0.
export const digitPositions = (value: number, places: readonly Place[]) => {
  const out: number[] = [];
  let lowerPos: number | null = null;
  let lowerBase = 10;
  for (const p of places) {
    const v = value / p.unit;
    const d = Math.floor(v) % p.base;
    let pos: number;
    if (lowerPos === null) {
      const f = v - Math.floor(v);
      pos = d + snap(Math.min(1, Math.max(0, (f - 0.72) / 0.28)));
    } else {
      const lf = lowerPos - Math.floor(lowerPos);
      pos = Math.floor(lowerPos) === lowerBase - 1 ? d + lf : d;
    }
    out.push(pos);
    lowerPos = pos;
    lowerBase = p.base;
  }
  return out;
};

export const DigitColumn: React.FC<{
  readonly pos: number;
  readonly base: number;
  readonly height: number;
  readonly blur: number;
  readonly style?: React.CSSProperties;
}> = ({ pos, base, height, blur, style }) => {
  const digits = Array.from({ length: base + 1 }, (_, i) => i % base);
  return (
    <div
      style={{
        height,
        overflow: "hidden",
        position: "relative",
        ...style,
      }}
    >
      <div
        style={{
          translate: `0 ${-(pos % base) * height}px`,
          filter: blur > 0.3 ? `blur(${blur}px)` : undefined,
        }}
      >
        {digits.map((d, i) => (
          <div
            key={i}
            style={{ height, lineHeight: `${height}px`, textAlign: "center" }}
          >
            {d}
          </div>
        ))}
      </div>
    </div>
  );
};
```

#### `src/components/Phone.tsx`

```tsx
import React from "react";
import { C, SANS } from "../theme";

export const PHONE_W = 540;
export const PHONE_H = 1110;
export const BEZEL = 16;

// iPhone-style frame. Children render inside the screen (below the status bar).
export const Phone: React.FC<{ readonly children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      width: PHONE_W,
      height: PHONE_H,
      borderRadius: 86,
      padding: BEZEL,
      background: "linear-gradient(145deg, #5A5A62, #1E1E22 35%, #2C2C31 70%, #6A6A72)",
      boxShadow:
        "0 0 0 2px rgba(255,255,255,0.08), 0 40px 120px rgba(0,0,0,0.6), 0 10px 30px rgba(0,0,0,0.5), inset 0 0 0 6px #0A0A0B",
      position: "relative",
    }}
  >
    <div
      style={{
        position: "relative",
        width: "100%",
        height: "100%",
        borderRadius: 70,
        overflow: "hidden",
        backgroundColor: "#FFFFFF",
      }}
    >
      {children}
      {/* Status bar */}
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 0,
          height: 52,
          backgroundColor: "#FFFFFF",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "8px 40px 0 48px",
          fontFamily: SANS,
          fontWeight: 600,
          fontSize: 22,
          color: C.ink,
        }}
      >
        <span>9:41</span>
        <span style={{ display: "flex", gap: 6, alignItems: "center" }}>
          <svg width={28} height={18} viewBox="0 0 28 18">
            {[0, 1, 2, 3].map((i) => (
              <rect key={i} x={i * 7} y={14 - i * 4} width={5} height={4 + i * 4} rx={1.2} fill={C.ink} />
            ))}
          </svg>
          <svg width={40} height={20} viewBox="0 0 40 20">
            <rect x={1} y={2} width={33} height={16} rx={5} fill="none" stroke={C.ink} strokeWidth={2} opacity={0.45} />
            <rect x={4} y={5} width={24} height={10} rx={2.5} fill={C.ink} />
            <rect x={35.5} y={7} width={3} height={6} rx={1.5} fill={C.ink} opacity={0.45} />
          </svg>
        </span>
      </div>
      {/* Dynamic island */}
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: 14,
          width: 150,
          height: 42,
          marginLeft: -75,
          borderRadius: 21,
          backgroundColor: "#000",
        }}
      />
    </div>
  </div>
);
```

#### `src/components/BrowserFrame.tsx`

```tsx
import React from "react";
import { C, SANS } from "../theme";

// Desktop browser window (light chrome) for wide screenshots. Children fill the page area.
export const BrowserFrame: React.FC<{
  readonly width: number;
  readonly height: number;
  readonly url: string;
  readonly children: React.ReactNode;
}> = ({ width, height, url, children }) => (
  <div
    style={{
      width,
      height,
      borderRadius: 26,
      overflow: "hidden",
      backgroundColor: "#FFFFFF",
      boxShadow: "0 0 0 1.5px rgba(255,255,255,0.12), 0 40px 120px rgba(0,0,0,0.6), 0 10px 30px rgba(0,0,0,0.45)",
      position: "relative",
    }}
  >
    <div
      style={{
        height: 64,
        display: "flex",
        alignItems: "center",
        gap: 12,
        padding: "0 22px",
        backgroundColor: "#ECECEE",
        borderBottom: "1px solid #D9D9DD",
      }}
    >
      {["#FF5F57", "#FEBC2E", "#28C840"].map((c) => (
        <div key={c} style={{ width: 16, height: 16, borderRadius: 8, backgroundColor: c }} />
      ))}
      <div
        style={{
          flex: 1,
          marginLeft: 18,
          height: 38,
          borderRadius: 12,
          backgroundColor: "#FFFFFF",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 10,
          fontFamily: SANS,
          fontWeight: 500,
          fontSize: 20,
          color: C.ink,
        }}
      >
        <svg width={14} height={18} viewBox="0 0 14 18">
          <rect x={1} y={8} width={12} height={9} rx={2} fill="#6B6B72" />
          <path d="M3.5 8V5.5a3.5 3.5 0 0 1 7 0V8" fill="none" stroke="#6B6B72" strokeWidth={2} />
        </svg>
        {url}
      </div>
    </div>
    <div style={{ position: "absolute", top: 64, left: 0, right: 0, bottom: 0, overflow: "hidden" }}>{children}</div>
  </div>
);
```

### Motion patterns

#### `src/patterns/motion.ts`

```ts
import type React from "react";
import { interpolate } from "remotion";
import { CLAMP, IN, IN_OUT, OUT } from "../theme";

export type Box = { x: number; y: number; w: number; h: number };

// Enter/exit for a panel that lives inside a window [a, b] (seconds): slides in from the
// right with blur, leaves to the left. Use for vignettes that swap inside one stage.
export const vignette = (t: number, a: number, b: number, distance = 140) => {
  const i = interpolate(t, [a, a + 0.32], [0, 1], { ...CLAMP, easing: OUT });
  const o = interpolate(t, [b - 0.24, b], [0, 1], { ...CLAMP, easing: IN });
  return {
    visible: t >= a && t <= b,
    style: {
      position: "absolute",
      inset: 0,
      opacity: i * (1 - o),
      translate: `${(1 - i) * distance - o * distance}px 0`,
      filter: `blur(${(1 - i) * 12 + o * 12}px)`,
    } as React.CSSProperties,
  };
};

// A card that owns one beat: rises in at `at`, is pushed up and out when the next beat
// starts at `next`. Centre it with left 50% / top Y; this adds the translate.
export const pushCard = (t: number, at: number, next: number | null): React.CSSProperties => {
  const a = interpolate(t, [at - 0.08, at + 0.38], [0, 1], { ...CLAMP, easing: OUT });
  const b = next === null ? 0 : interpolate(t, [next - 0.14, next + 0.12], [0, 1], { ...CLAMP, easing: IN });
  return {
    opacity: a * (1 - b),
    translate: `-50% calc(-50% + ${(1 - a) * 240 - b * 200}px)`,
    scale: String((0.9 + a * 0.1) * (1 - b * 0.08)),
    filter: `blur(${(1 - a) * 14 + b * 14}px)`,
  };
};

// Whole-scene exit: push toward camera and blur away (pairs with the next scene's entrance).
export const sceneExit = (t: number, start: number, end: number): React.CSSProperties => {
  const e = interpolate(t, [start, end], [0, 1], { ...CLAMP, easing: IN });
  return { opacity: 1 - e, scale: String(1 + e * 0.12), filter: `blur(${e * 18}px)` };
};

// Decaying shake after an impact (stamp, clip, slam). Returns px.
export const shake = (t: number, at: number, dur = 0.2, amp = 8) =>
  t > at && t < at + dur ? Math.sin(t * 150) * amp * (1 - (t - at) / dur) : 0;

// Damped pendulum angle (deg) for something that drops and swings from a pivot.
export const swing = (t: number, landAt: number, amp = 7.5) => {
  const s = t - landAt;
  return s > 0 ? amp * Math.exp(-2.4 * s) * Math.sin(8.2 * s) : -3 * Math.min(1, t / Math.max(0.01, landAt));
};

export const lerpBox = (a: Box, b: Box, m: number): Box => ({
  x: a.x + (b.x - a.x) * m,
  y: a.y + (b.y - a.y) * m,
  w: a.w + (b.w - a.w) * m,
  h: a.h + (b.h - a.h) * m,
});

// Whip pan between two scenes: the old one flies out sideways with heavy blur while the new
// one flies in from the other side. Use on the outgoing scene (dir 'out') and the incoming
// scene (dir 'in') around the same `at`. Pair with the whip sound.
export const whip = (t: number, at: number, dir: "in" | "out", side: 1 | -1 = 1): React.CSSProperties => {
  if (dir === "out") {
    const p = interpolate(t, [at - 0.16, at], [0, 1], { ...CLAMP, easing: IN });
    return { translate: `${-side * p * 1300}px 0`, filter: `blur(${p * 40}px)`, opacity: 1 - p * 0.6 };
  }
  const p = interpolate(t, [at, at + 0.28], [0, 1], { ...CLAMP, easing: OUT });
  return { translate: `${side * (1 - p) * 1300}px 0`, filter: `blur(${(1 - p) * 40}px)` };
};

// Circle reveal from a point (a click, a button, a logo): the new scene opens out of it.
export const iris = (t: number, at: number, cx: number, cy: number, dur = 0.5): React.CSSProperties => {
  const r = interpolate(t, [at, at + dur], [0, 2300], { ...CLAMP, easing: IN_OUT });
  return { clipPath: `circle(${r}px at ${cx}px ${cy}px)` };
};

// Zoom-through: push the camera into a point until it fills the frame, then cut to the
// next scene, which starts slightly zoomed in and settles (use zoomThrough(t, at, x, y, 'in')).
export const zoomThrough = (t: number, at: number, x: number, y: number, dir: "in" | "out"): React.CSSProperties => {
  if (dir === "out") {
    const p = interpolate(t, [at - 0.3, at], [0, 1], { ...CLAMP, easing: IN });
    return { transformOrigin: `${x}px ${y}px`, scale: String(1 + p * 5), filter: `blur(${p * 16}px)`, opacity: 1 - p * 0.5 };
  }
  const p = interpolate(t, [at, at + 0.45], [0, 1], { ...CLAMP, easing: OUT });
  return { transformOrigin: `${x}px ${y}px`, scale: String(1.6 - p * 0.6), filter: `blur(${(1 - p) * 16}px)` };
};
```

#### `src/patterns/CountUp.tsx`

```tsx
import React from "react";
import { interpolate, interpolateColors } from "remotion";
import { DigitColumn, digitPositions, type Place } from "../components/Odometer";
import { C, CLAMP, MONO, OUT, SANS } from "../theme";

const TIME_PLACES: Place[] = [
  { unit: 1, base: 10 },
  { unit: 10, base: 6 },
  { unit: 60, base: 10 },
  { unit: 600, base: 6 },
  { unit: 3600, base: 10 },
  { unit: 36000, base: 10 },
];

// Rolling odometer that counts to `value` between `start` and `end` (expo-out, so it
// slams up and then settles digit by digit), then keeps ticking at `tickPerSec`.
// mode "timecode": value in seconds -> HH:MM:SS.  mode "number": integer with commas.
// The leading group turns accent-coloured at `highlightAt` (land it on the key word).
export const CountUp: React.FC<{
  readonly t: number;
  readonly value: number;
  readonly start: number;
  readonly end: number;
  readonly mode: "timecode" | "number";
  readonly prefix?: string;
  readonly suffix?: string; // e.g. "+" or "k"; always laid out, so nothing re-centres
  readonly label?: string;
  readonly highlightAt?: number;
  readonly tickPerSec?: number;
  readonly fontSize?: number;
}> = ({ t, value, start, end, mode, prefix = "", suffix = "", label, highlightAt = 999, tickPerSec = 0, fontSize = 208 }) => {
  const at = (sec: number) =>
    interpolate(sec, [start, end], [0, value], { ...CLAMP, easing: OUT }) + Math.max(0, sec - end) * tickPerSec;
  const T = at(t);
  const vel = Math.abs(T - at(t - 1 / 60));
  const digits = mode === "timecode" ? 6 : Math.max(1, String(Math.floor(value)).length);
  const places: Place[] = mode === "timecode" ? TIME_PLACES : Array.from({ length: digits }, (_, i) => ({ unit: 10 ** i, base: 10 }));
  const pos = digitPositions(T, places);
  const H = fontSize * 1.03;
  const W = fontSize * 0.59;
  const hi = interpolateColors(t, [highlightAt - 0.04, highlightAt + 0.2], [C.text, C.accent]);
  // In number mode, leading zeros stay invisible until the count reaches them.
  const lead = (i: number) => (mode === "number" && i > 0 ? Math.min(1, Math.max(0, (T - places[i].unit * 0.9) / (places[i].unit * 0.1))) : 1);
  const col = (i: number, color: string) => (
    <DigitColumn
      key={i}
      pos={pos[i]}
      base={places[i].base}
      height={H}
      blur={Math.min(14, (vel / places[i].unit) * 9)}
      style={{
        width: W,
        color,
        opacity: lead(i),
        maskImage: "linear-gradient(transparent, black 16%, black 84%, transparent)",
        WebkitMaskImage: "linear-gradient(transparent, black 16%, black 84%, transparent)",
      }}
    />
  );
  const sep = (ch: string, key: string) => (
    <div key={key} style={{ width: W * (ch === ":" ? 0.4 : 0.32), height: H, lineHeight: `${H - fontSize * 0.1}px`, textAlign: "center", color: C.dim }}>
      {ch}
    </div>
  );
  const items: React.ReactNode[] = [];
  if (mode === "timecode") {
    items.push(col(5, hi), col(4, hi), sep(":", "a"), col(3, C.text), col(2, C.text), sep(":", "b"), col(1, C.text), col(0, C.text));
  } else {
    for (let i = digits - 1; i >= 0; i--) {
      items.push(col(i, i >= digits - 1 - ((digits - 1) % 3) ? hi : C.text));
      if (i > 0 && i % 3 === 0) items.push(<div key={`c${i}`} style={{ opacity: lead(i) }}>{sep(",", `s${i}`)}</div>);
    }
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      {label && (
        <div
          style={{
            fontFamily: MONO,
            fontSize: 30,
            letterSpacing: "0.22em",
            color: C.muted,
            marginBottom: 6,
            opacity: interpolate(t, [start - 0.1, start + 0.3], [0, 1], CLAMP),
          }}
        >
          {label}
        </div>
      )}
      <div
        style={{
          display: "flex",
          fontFamily: SANS,
          fontWeight: 800,
          fontSize,
          letterSpacing: "-0.04em",
          fontFeatureSettings: '"tnum"',
          color: C.text,
          textShadow: "0 20px 60px rgba(0,0,0,0.5)",
          opacity: interpolate(t, [start - 0.12, start + 0.12], [0, 1], CLAMP),
          scale: String(interpolate(t, [start - 0.12, start + 0.8], [0.9, 1], { ...CLAMP, easing: OUT })),
        }}
      >
        {prefix && <div style={{ height: H, lineHeight: `${H}px`, color: hi }}>{prefix}</div>}
        {items}
        {suffix && <div style={{ height: H, lineHeight: `${H}px`, color: hi }}>{suffix}</div>}
      </div>
    </div>
  );
};
```

#### `src/patterns/DropFlip.tsx`

```tsx
import React from "react";
import { interpolate } from "remotion";
import { C, CLAMP, DROP, IN, IN_OUT, SHADOW } from "../theme";
import { lerpBox, swing, type Box } from "./motion";

// A card that drops in on a strap and swings to rest (lands at `landAt`), then flips over
// at `flipAt` while morphing from box `from` to box `to`. Front = the object (badge, ticket,
// ID, receipt), back = what it "contains" (job description, recipe, plan, invoice).
// Set flipAt to Infinity for a drop-only card. `after` moves the flipped card again (keep
// the same size, or the back re-wraps): e.g. slide a document down to become a rail.
export const DropFlip: React.FC<{
  readonly t: number;
  readonly landAt: number;
  readonly flipAt: number;
  readonly from: Box;
  readonly to: Box;
  readonly front: React.ReactNode;
  readonly back: React.ReactNode;
  readonly strapColor?: string;
  readonly strapText?: string;
  readonly after?: { readonly at: number; readonly box: Box };
}> = ({ t, landAt, flipAt, from, to, front, back, strapColor = C.accent, strapText = "", after }) => {
  const flip = interpolate(t, [flipAt, flipAt + 0.5], [0, 180], { ...CLAMP, easing: IN_OUT });
  const morph = interpolate(t, [flipAt + 0.14, flipAt + 0.66], [0, 1], { ...CLAMP, easing: IN_OUT });
  const moved = after ? interpolate(t, [after.at, after.at + 0.5], [0, 1], { ...CLAMP, easing: IN_OUT }) : 0;
  const box = lerpBox(lerpBox(from, to, morph), after?.box ?? to, moved);
  const angle = swing(t, landAt) * (1 - flip / 180);
  const pivotX = from.x + from.w / 2;
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        transformOrigin: `${pivotX}px -320px`,
        rotate: `${angle}deg`,
        translate: `0 ${interpolate(t, [landAt - 0.42, landAt], [-1600, 0], { ...CLAMP, easing: DROP })}px`,
      }}
    >
      {/* Strap: pulled up and away as the card flips */}
      <div
        style={{
          position: "absolute",
          left: pivotX - 42,
          top: from.y + 58 - 700,
          width: 84,
          height: 700,
          translate: `0 ${interpolate(t, [flipAt - 0.14, flipAt + 0.26], [0, -900], { ...CLAMP, easing: IN })}px`,
          background: `linear-gradient(90deg, rgba(0,0,0,0.12), ${strapColor} 30%, rgba(255,255,255,0.25) 55%, ${strapColor} 75%, rgba(0,0,0,0.15))`,
          backgroundColor: strapColor,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            position: "absolute",
            left: 28,
            top: 0,
            writingMode: "vertical-rl",
            fontFamily: "monospace",
            fontWeight: 700,
            fontSize: 22,
            letterSpacing: "0.3em",
            color: "rgba(20,20,20,0.75)",
            whiteSpace: "nowrap",
          }}
        >
          {`${strapText} · `.repeat(14)}
        </div>
      </div>
      <div style={{ position: "absolute", left: box.x, top: box.y, width: box.w, height: box.h, perspective: 2400 }}>
        <div style={{ position: "absolute", inset: 0, transformStyle: "preserve-3d", transform: `rotateY(${flip}deg)` }}>
          <div
            style={{
              position: "absolute",
              left: "50%",
              top: "50%",
              width: from.w,
              height: from.h,
              marginLeft: -from.w / 2,
              marginTop: -from.h / 2,
              backfaceVisibility: "hidden",
              borderRadius: 46,
              boxShadow: SHADOW,
              overflow: "hidden",
            }}
          >
            {front}
          </div>
          <div
            style={{
              position: "absolute",
              inset: 0,
              backfaceVisibility: "hidden",
              transform: "rotateY(180deg)",
              borderRadius: 40,
              backgroundColor: C.paper,
              boxShadow: SHADOW,
              overflow: "hidden",
            }}
          >
            {/* Lay the back out at its FINAL width so text never re-wraps during the morph */}
            <div style={{ position: "absolute", left: 0, top: 0, width: to.w, height: to.h }}>{back}</div>
          </div>
        </div>
      </div>
    </div>
  );
};
```

#### `src/patterns/Checklist.tsx`

```tsx
import React from "react";
import { interpolate } from "remotion";
import { Check } from "../components/Kit";
import { C, CLAMP, IN_OUT, MONO, OUT, SANS, SHADOW, alpha } from "../theme";
import { lerpBox, type Box } from "./motion";

// For a LIST in the voiceover ("transcribe, cut, key, export"): a paper checklist that
// ticks each item while that item plays as its own vignette in the Stage above it.
//   mode 0 = full document (big title, big rows), 1 = compact rail under the stage.
//   starts[i] = when item i is spoken (cue sheet), ticks[i] = when it gets checked,
//   until = when the last item's highlight clears (default: never).
// The rail sizes itself to the item count and always ends at the safe-area bottom (y 1450);
// the stage fills the space above it. Use stageBox(n) to lay out vignettes.

const SAFE_TOP = 286;
const SAFE_BOTTOM = 1450;
export const DOC_BOX: Box = { x: 80, y: 400, w: 920, h: 1040 };

const railMetrics = (n: number) => {
  const rowH = n >= 5 ? 64 : 74;
  return { rowH, font: n >= 5 ? 40 : 44, check: n >= 5 ? 42 : 46, head: 64 };
};
export const railBox = (n: number): Box => {
  const m = railMetrics(n);
  const h = m.head + n * m.rowH + 28;
  return { x: 80, y: SAFE_BOTTOM - h, w: 920, h };
};
export const stageBox = (n: number): Box => {
  const top = SAFE_TOP;
  return { x: 80, y: top, w: 920, h: railBox(n).y - 36 - top };
};

export const activeIndex = (t: number, starts: readonly number[]) =>
  starts.reduce((acc, s, i) => acc + (i === 0 ? 0 : interpolate(t, [s - 0.06, s + 0.18], [0, 1], { ...CLAMP, easing: IN_OUT })), 0);

export const ChecklistCard: React.FC<{
  readonly t: number;
  readonly items: readonly string[];
  readonly starts: readonly number[];
  readonly ticks: readonly number[];
  readonly mode: number;
  readonly title: string;
  readonly kicker: string;
  readonly subtitle?: string;
  readonly until?: number;
  readonly rowsInAt?: number;
  readonly style?: React.CSSProperties;
}> = ({ t, items, starts, ticks, mode, title, kicker, subtitle, until, rowsInAt = -1, style }) => {
  const n = items.length;
  const m = railMetrics(n);
  const box = lerpBox(DOC_BOX, railBox(n), mode);
  const lerp = (a: number, b: number) => a + (b - a) * mode;
  const rowH = lerp(100, m.rowH);
  const font = lerp(50, m.font);
  const size = lerp(54, m.check);
  const checks = ticks.map((k) => interpolate(t, [k, k + 0.3], [0, 1], { ...CLAMP, easing: OUT }));
  const done = checks.filter((c) => c > 0.5).length;
  // Each row's marker wipes in left-to-right when its item starts and wipes out
  // left-to-right when the next one starts.
  const marker = (i: number) => {
    const a = starts[i];
    const b = i + 1 < starts.length ? starts[i + 1] : (until ?? Infinity);
    const inP = interpolate(t, [a + 0.04, a + 0.36], [0, 1], { ...CLAMP, easing: OUT });
    const outP = Number.isFinite(b) ? interpolate(t, [b - 0.06, b + 0.22], [0, 1], { ...CLAMP, easing: IN_OUT }) : 0;
    return { inP: inP * mode, outP };
  };
  return (
    <div
      style={{
        position: "absolute",
        left: box.x,
        top: box.y,
        width: box.w,
        height: box.h,
        borderRadius: 40,
        backgroundColor: C.paper,
        boxShadow: SHADOW,
        overflow: "hidden",
        fontFamily: SANS,
        color: C.ink,
        ...style,
      }}
    >
      <div style={{ position: "absolute", left: 64, width: DOC_BOX.w - 128, top: 62, opacity: 1 - Math.min(1, mode * 2.2), translate: `0 ${-mode * 60}px` }}>
        <div style={{ fontFamily: MONO, fontSize: 22, letterSpacing: "0.18em", color: "rgba(20,20,20,0.55)" }}>{kicker}</div>
        <div style={{ fontSize: 98, fontWeight: 800, letterSpacing: "-0.045em", lineHeight: 1, marginTop: 34, whiteSpace: "nowrap" }}>{title}</div>
        {subtitle && <div style={{ fontSize: 34, fontWeight: 500, color: "rgba(20,20,20,0.55)", marginTop: 18 }}>{subtitle}</div>}
        <div style={{ height: 2, backgroundColor: "rgba(20,20,20,0.12)", marginTop: 34 }} />
      </div>
      <div
        style={{
          position: "absolute",
          left: 48,
          right: 48,
          top: 24,
          display: "flex",
          justifyContent: "space-between",
          fontFamily: MONO,
          fontSize: 22,
          letterSpacing: "0.18em",
          color: "rgba(20,20,20,0.5)",
          opacity: Math.max(0, mode * 2 - 1),
        }}
      >
        <div>{kicker}</div>
        <div style={{ color: C.ink }}>
          {done}/{n}
        </div>
      </div>
      {items.map((label, i) => {
        const inP = rowsInAt < 0 ? 1 : interpolate(t, [rowsInAt + i * 0.07, rowsInAt + i * 0.07 + 0.45], [0, 1], { ...CLAMP, easing: OUT });
        const mk = marker(i);
        const leaving = mk.outP > 0;
        const shown = leaving ? 1 - mk.outP : mk.inP;
        // Clip window of the marker: grows from the left, then shrinks toward the right.
        const clip = leaving ? `inset(0 -14px 0 ${mk.outP * 100}%)` : `inset(0 ${(1 - mk.inP) * 100}% 0 -14px)`;
        const dimmed = mode > 0.5 && checks[i] < 0.5 && shown < 0.05;
        return (
          <div
            key={label}
            style={{
              position: "absolute",
              left: lerp(64, 48),
              right: 48,
              top: lerp(392, m.head) + i * rowH,
              height: rowH,
              display: "flex",
              alignItems: "center",
              gap: lerp(28, 22),
              opacity: inP * (dimmed ? 0.4 : 1),
              translate: `${(1 - inP) * -40}px 0`,
            }}
          >
            <div
              style={{
                width: size,
                height: size,
                flexShrink: 0,
                borderRadius: size * 0.3,
                border: `3px solid rgba(20,20,20,${0.22 * (1 - checks[i])})`,
                backgroundColor: alpha(C.accent, checks[i]),
                scale: String(1 + Math.sin(checks[i] * Math.PI) * 0.25),
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Check size={size * 0.85} progress={checks[i]} color={C.accentInk} stroke={3.4} />
            </div>
            <div style={{ position: "relative", fontSize: font, fontWeight: 700, letterSpacing: "-0.025em", whiteSpace: "nowrap" }}>
              <span>{label}</span>
              {shown > 0 && (
                <div style={{ position: "absolute", inset: 0, clipPath: clip }}>
                  <div style={{ position: "absolute", left: -10, right: -10, top: "14%", bottom: "4%", borderRadius: 8, backgroundColor: C.accent }} />
                  <span style={{ position: "relative", color: C.accentInk }}>{label}</span>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

// Dark stage panel above the rail. The label rolls to the active item; put vignettes
// inside as children (use vignette() from ./motion for their in/out). Vignettes are
// positioned inside a box of stageBox(items.length).w x .h: fill it, don't leave it empty.
export const Stage: React.FC<{
  readonly t: number;
  readonly items: readonly string[];
  readonly starts: readonly number[];
  readonly children: React.ReactNode;
  readonly firstNumber?: number;
  readonly style?: React.CSSProperties;
}> = ({ t, items, starts, children, firstNumber = 1, style }) => {
  const active = activeIndex(t, starts);
  const box = stageBox(items.length);
  return (
    <div
      style={{
        position: "absolute",
        left: box.x,
        top: box.y,
        width: box.w,
        height: box.h,
        borderRadius: 44,
        backgroundColor: C.surface,
        border: `1.5px solid ${C.line}`,
        boxShadow: SHADOW,
        overflow: "hidden",
        ...style,
      }}
    >
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(80% 60% at 50% 0%, rgba(255,255,255,0.05), transparent 70%)" }} />
      <div style={{ position: "absolute", left: 44, top: 30, height: 40, overflow: "hidden", fontFamily: MONO, fontSize: 26, letterSpacing: "0.18em", color: C.muted, zIndex: 2 }}>
        <div style={{ translate: `0 ${-active * 40}px` }}>
          {items.map((d, i) => (
            <div key={d} style={{ height: 40, lineHeight: "40px", whiteSpace: "pre" }}>
              <span style={{ color: C.accent }}>{String(i + firstNumber).padStart(2, "0")}</span>
              {"  "}
              {d.toUpperCase()}
            </div>
          ))}
        </div>
      </div>
      {children}
    </div>
  );
};
```

#### `src/patterns/Beats.tsx`

```tsx
import React from "react";
import { interpolate } from "remotion";
import { Check } from "../components/Kit";
import { C, CLAMP, IN, MONO, OUT, POP, SANS, SERIF, SHADOW } from "../theme";

// For repeated sentence frames ("I don't sleep. I don't invoice. I don't ghost you"):
// the shared lead stays put, the changing word rolls through a masked slot in the
// accent serif. at[i] = when word i is spoken. Optional tail line under the slot.
export const SlotHeadline: React.FC<{
  readonly t: number;
  readonly lead: string;
  readonly words: readonly string[];
  readonly at: readonly number[];
  readonly tail?: { readonly text: string; readonly at: number };
  readonly top?: number;
}> = ({ t, lead, words, at, tail, top = 300 }) => {
  const H = 190;
  const enter = interpolate(t, [at[0] - 0.08, at[0] + 0.38], [0, 1], { ...CLAMP, easing: OUT });
  const roll = at.slice(1).reduce((acc, a) => acc + interpolate(t, [a - 0.1, a + 0.25], [0, 1], { ...CLAMP, easing: OUT }), 0);
  return (
    <div style={{ position: "absolute", top, left: 0, right: 0, textAlign: "center" }}>
      <div
        style={{
          fontFamily: SANS,
          fontWeight: 800,
          fontSize: 126,
          letterSpacing: "-0.05em",
          lineHeight: 1,
          color: C.text,
          opacity: interpolate(t, [at[0] - 0.15, at[0] + 0.15], [0, 1], CLAMP),
          translate: `0 ${interpolate(t, [at[0] - 0.15, at[0] + 0.3], [40, 0], { ...CLAMP, easing: OUT })}px`,
        }}
      >
        {lead}
      </div>
      <div
        style={{
          height: H,
          overflow: "hidden",
          maskImage: "linear-gradient(transparent, black 18%, black 82%, transparent)",
          WebkitMaskImage: "linear-gradient(transparent, black 18%, black 82%, transparent)",
        }}
      >
        <div style={{ translate: `0 ${-roll * H + (1 - enter) * H}px` }}>
          {words.map((w) => (
            <div key={w} style={{ height: H, lineHeight: `${H}px`, fontFamily: SERIF, fontStyle: "italic", fontSize: 176, letterSpacing: "-0.02em", color: C.accent, whiteSpace: "nowrap" }}>
              {w}
            </div>
          ))}
        </div>
      </div>
      {tail && (
        <div
          style={{
            fontFamily: SANS,
            fontWeight: 800,
            fontSize: 84,
            letterSpacing: "-0.045em",
            color: C.text,
            opacity: interpolate(t, [tail.at, tail.at + 0.25], [0, 1], CLAMP),
            translate: `0 ${interpolate(t, [tail.at, tail.at + 0.4], [30, 0], { ...CLAMP, easing: OUT })}px`,
          }}
        >
          {tail.text}
        </div>
      )}
    </div>
  );
};

// Rubber stamp that slams down at `at` (pair with shake() on the thing it hits).
export const Stamp: React.FC<{ readonly t: number; readonly at: number; readonly text: string; readonly color?: string; readonly size?: number; readonly angle?: number }> = ({
  t,
  at,
  text,
  color = C.alert,
  size = 130,
  angle = -14,
}) => {
  const p = interpolate(t, [at, at + 0.2], [0, 1], { ...CLAMP, easing: IN });
  return (
    <div
      style={{
        position: "absolute",
        left: "50%",
        top: "50%",
        translate: "-50% -50%",
        rotate: `${angle + (1 - p) * -10}deg`,
        scale: String(1 + (1 - p) * 1.5),
        opacity: p,
        padding: "8px 36px",
        border: `${size * 0.07}px solid ${color}`,
        borderRadius: size * 0.17,
        fontFamily: SANS,
        fontWeight: 900,
        fontSize: size,
        letterSpacing: "0.05em",
        color,
        whiteSpace: "nowrap",
        mixBlendMode: "multiply",
      }}
    >
      {text}
    </div>
  );
};

export type ChatMessage = { readonly from: "me" | "them"; readonly text: string; readonly at: number };

// Messaging thread. "them" messages get a typing indicator for 0.4 s before they land.
// "me" = the viewer (accent bubbles, right), "them" = the product/character (left).
export const ChatThread: React.FC<{
  readonly t: number;
  readonly name: string;
  readonly status?: string;
  readonly avatar: React.ReactNode;
  readonly stamp?: string;
  readonly messages: readonly ChatMessage[];
  readonly width?: number;
}> = ({ t, name, status = "online", avatar, stamp, messages, width = 820 }) => (
  <div style={{ width, borderRadius: 48, backgroundColor: C.surface2, border: `1.5px solid ${C.line2}`, boxShadow: SHADOW, overflow: "hidden" }}>
    <div style={{ display: "flex", alignItems: "center", gap: 22, padding: "26px 34px", borderBottom: `1.5px solid ${C.line}` }}>
      {avatar}
      <div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 36, color: C.text }}>{name}</div>
        <div style={{ fontFamily: MONO, fontSize: 22, color: C.success, marginTop: 4 }}>● {status}</div>
      </div>
    </div>
    <div style={{ padding: "26px 34px 40px", display: "flex", flexDirection: "column", gap: 22 }}>
      {stamp && <div style={{ textAlign: "center", fontFamily: MONO, fontSize: 22, color: C.muted, letterSpacing: "0.1em" }}>{stamp}</div>}
      {messages.map((m, i) => {
        const me = m.from === "me";
        const typing = !me && t > m.at - 0.4 && t < m.at;
        const p = interpolate(t, [m.at, m.at + 0.4], [0, 1], { ...CLAMP, easing: POP });
        if (t < m.at - (me ? 0 : 0.4)) return null;
        return (
          <div key={i} style={{ display: "flex", justifyContent: me ? "flex-end" : "flex-start" }}>
            {typing ? (
              <div style={{ display: "flex", gap: 10, padding: "26px 30px", borderRadius: "36px 36px 36px 10px", backgroundColor: C.surface3 }}>
                {[0, 1, 2].map((d) => (
                  <div key={d} style={{ width: 16, height: 16, borderRadius: 8, backgroundColor: C.muted, translate: `0 ${Math.sin(t * 14 - d * 0.9) * 5}px` }} />
                ))}
              </div>
            ) : (
              <div
                style={{
                  maxWidth: width * 0.7,
                  padding: "22px 30px",
                  borderRadius: me ? "36px 36px 10px 36px" : "36px 36px 36px 10px",
                  backgroundColor: me ? C.accent : C.surface3,
                  color: me ? C.accentInk : C.text,
                  fontFamily: SANS,
                  fontWeight: 600,
                  fontSize: 38,
                  lineHeight: 1.25,
                  letterSpacing: "-0.02em",
                  transformOrigin: me ? "100% 100%" : "0% 100%",
                  scale: String(p),
                }}
              >
                {m.text}
              </div>
            )}
          </div>
        );
      })}
    </div>
  </div>
);

// Row of app/platform tiles that pop in one after another (logos as children).
export const LogoRow: React.FC<{ readonly t: number; readonly at: number; readonly tiles: readonly React.ReactNode[]; readonly size?: number }> = ({
  t,
  at,
  tiles,
  size = 156,
}) => (
  <div style={{ display: "flex", justifyContent: "center", gap: 36 }}>
    {tiles.map((tile, i) => {
      const a = at + i * 0.1;
      return (
        <div
          key={i}
          style={{
            width: size,
            height: size,
            borderRadius: size * 0.26,
            backgroundColor: C.surface2,
            border: `1.5px solid ${C.line2}`,
            boxShadow: SHADOW,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            opacity: interpolate(t, [a, a + 0.08], [0, 1], CLAMP),
            scale: String(interpolate(t, [a, a + 0.55], [0.3, 1], { ...CLAMP, easing: POP })),
            translate: `0 ${interpolate(t, [a, a + 0.5], [50, 0], { ...CLAMP, easing: OUT })}px`,
            rotate: `${interpolate(t, [a, a + 0.6], [(i - (tiles.length - 1) / 2) * 14, 0], { ...CLAMP, easing: POP })}deg`,
          }}
        >
          {tile}
        </div>
      );
    })}
  </div>
);

// Small tag with a check that pops next to a vignette ("KEYED", "+5 GRAPHICS").
export const DoneTag: React.FC<{ readonly t: number; readonly at: number; readonly label: string; readonly style?: React.CSSProperties }> = ({ t, at, label, style }) => {
  const p = interpolate(t, [at, at + 0.45], [0, 1], { ...CLAMP, easing: POP });
  return (
    <div
      style={{
        position: "absolute",
        display: "flex",
        alignItems: "center",
        gap: 8,
        padding: "12px 18px 12px 12px",
        borderRadius: 16,
        backgroundColor: C.surface3,
        border: `1.5px solid ${C.line2}`,
        fontFamily: MONO,
        fontWeight: 700,
        fontSize: 22,
        letterSpacing: "0.08em",
        color: C.text,
        scale: String(p),
        opacity: Math.min(1, p * 3),
        ...style,
      }}
    >
      <div style={{ width: 32, height: 32, borderRadius: 10, backgroundColor: C.accent, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Check size={26} progress={interpolate(t, [at + 0.1, at + 0.35], [0, 1], CLAMP)} color={C.accentInk} />
      </div>
      {label}
    </div>
  );
};
```

#### `src/patterns/Showcase.tsx`

```tsx
import React from "react";
import { Img, interpolate, staticFile } from "remotion";
import { BrowserFrame } from "../components/BrowserFrame";
import { BEZEL, PHONE_W, Phone } from "../components/Phone";
import { C, CLAMP, IN_OUT, OUT, alpha } from "../theme";

export type Rect = { x: number; y: number; w: number; h: number };

// A real screenshot inside a phone or browser: rises in with a 3D tilt, scrolls, draws a
// highlight ring around `focus` at `focusAt` and pushes the camera in on it. `dim` 0..1
// sends it into the background (blur + fade + drop) when a headline or price takes over.
//
// `focus` and `scroll.to` are in the CAPTURE's CSS px: exactly the boxes that
// `capture.mjs inspect` prints (use `inspect --mobile` for phone shots). The component
// scales them to the frame. The push-in grows the frame around the focus point, so it
// also covers whatever sits above it: move or fade headlines out of the way first.
type Scroll = { readonly to: number; readonly at: number; readonly dur?: number };

const useShowcase = (t: number, enterAt: number, focusAt: number, dim: number, scale: number, scroll?: Scroll) => ({
  rise: interpolate(t, [enterAt, enterAt + 0.8], [0, 1], { ...CLAMP, easing: OUT }),
  zoom: interpolate(t, [focusAt - 0.04, focusAt + 0.5], [0, 1], { ...CLAMP, easing: IN_OUT }),
  ring: interpolate(t, [focusAt, focusAt + 0.38], [0, 1], { ...CLAMP, easing: OUT }),
  // Default: a slow 60 px drift so the page feels live. With `scroll`, glide to that page y.
  scrollPx: scroll
    ? -interpolate(t, [scroll.at, scroll.at + (scroll.dur ?? 0.8)], [0, scroll.to * scale], { ...CLAMP, easing: IN_OUT })
    : interpolate(t, [enterAt + 0.4, enterAt + 3.6], [0, -60], { ...CLAMP, easing: IN_OUT }),
  dimStyle: { filter: `blur(${dim * 10}px)`, translate: `0 ${dim * 330}px` } as React.CSSProperties,
});

const Ring: React.FC<{ readonly r: Rect; readonly ring: number }> = ({ r, ring }) => (
  <svg width={r.x + r.w + 20} height={r.y + r.h + 20} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
    <rect
      x={r.x}
      y={r.y}
      width={r.w}
      height={r.h}
      rx={12}
      fill={alpha(C.accent, 0.28 * ring)}
      stroke={C.accent}
      strokeWidth={5}
      pathLength={1}
      strokeDasharray={1}
      strokeDashoffset={1 - ring}
    />
  </svg>
);

const pad = (r: Rect, scale: number, dy: number, scrollPx: number): Rect => ({
  x: r.x * scale - 8,
  y: dy + r.y * scale - 8 + scrollPx,
  w: r.w * scale + 16,
  h: r.h * scale + 16,
});

export const PhoneShowcase: React.FC<{
  readonly t: number;
  readonly src: string; // mobile screenshot from `capture.mjs shot <url> <out> --mobile`
  readonly enterAt: number;
  readonly focus?: Rect;
  readonly focusAt?: number;
  readonly zoomTo?: number;
  readonly scroll?: Scroll;
  readonly dim?: number;
  readonly captureWidth?: number; // CSS width of the capture (430 for --mobile)
  readonly top?: number;
}> = ({ t, src, enterAt, focus, focusAt = 999, zoomTo = 1.24, scroll, dim = 0, captureWidth = 430, top = 400 }) => {
  const screenW = PHONE_W - BEZEL * 2;
  const scale = screenW / captureWidth;
  const s = useShowcase(t, enterAt, focusAt, dim, scale, scroll);
  const ring = focus ? pad(focus, scale, 52, s.scrollPx) : null;
  const origin = ring ? `${BEZEL + ring.x + ring.w / 2}px ${BEZEL + ring.y + ring.h / 2}px` : "50% 30%";
  return (
    <div
      style={{
        position: "absolute",
        left: (1080 - PHONE_W) / 2,
        top,
        perspective: 2200,
        ...s.dimStyle,
        opacity: interpolate(t, [enterAt, enterAt + 0.2], [0, 1], CLAMP) * (1 - dim * 0.72),
      }}
    >
      <div
        style={{
          transform: `translateY(${(1 - s.rise) * 1000}px) rotateX(${(1 - s.rise) * 34}deg) rotateY(${(1 - s.rise) * -16}deg) rotateZ(${(1 - s.rise) * 6}deg)`,
          transformStyle: "preserve-3d",
        }}
      >
        <div style={{ transformOrigin: origin, scale: String(1 + s.zoom * (zoomTo - 1) - dim * 0.12) }}>
          <Phone>
            <Img src={staticFile(src)} style={{ position: "absolute", left: 0, top: 52, width: screenW, translate: `0 ${s.scrollPx}px` }} />
            {ring && <Ring r={ring} ring={s.ring} />}
          </Phone>
        </div>
      </div>
    </div>
  );
};

export const BrowserShowcase: React.FC<{
  readonly t: number;
  readonly src: string; // desktop screenshot from `capture.mjs shot <url> <out>`
  readonly url: string;
  readonly enterAt: number;
  readonly focus?: Rect;
  readonly focusAt?: number;
  readonly zoomTo?: number;
  readonly scroll?: Scroll;
  readonly dim?: number;
  readonly captureWidth?: number; // CSS width of the capture (1280 by default)
  readonly width?: number;
  readonly height?: number;
  readonly top?: number;
}> = ({ t, src, url, enterAt, focus, focusAt = 999, zoomTo = 1.35, scroll, dim = 0, captureWidth = 1280, width = 960, height = 1100, top = 400 }) => {
  const scale = width / captureWidth;
  const s = useShowcase(t, enterAt, focusAt, dim, scale, scroll);
  const ring = focus ? pad(focus, scale, 0, s.scrollPx) : null;
  const origin = ring ? `${ring.x + ring.w / 2}px ${64 + ring.y + ring.h / 2}px` : "50% 30%";
  return (
    <div
      style={{
        position: "absolute",
        left: (1080 - width) / 2,
        top,
        perspective: 2200,
        ...s.dimStyle,
        opacity: interpolate(t, [enterAt, enterAt + 0.2], [0, 1], CLAMP) * (1 - dim * 0.72),
      }}
    >
      <div style={{ transform: `translateY(${(1 - s.rise) * 900}px) rotateX(${(1 - s.rise) * 30}deg) rotateZ(${(1 - s.rise) * -5}deg)` }}>
        <div style={{ transformOrigin: origin, scale: String(1 + s.zoom * (zoomTo - 1) - dim * 0.12) }}>
          <BrowserFrame width={width} height={height} url={url}>
            <Img src={staticFile(src)} style={{ position: "absolute", left: 0, top: 0, width, translate: `0 ${s.scrollPx}px` }} />
            {ring && <Ring r={ring} ring={s.ring} />}
          </BrowserFrame>
        </div>
      </div>
    </div>
  );
};
```

#### `src/patterns/Offer.tsx`

```tsx
import React from "react";
import { interpolate } from "remotion";
import { Check, Cursor, RevealWord } from "../components/Kit";
import { C, CLAMP, IN_OUT, MONO, OUT, POP, SANS, SHADOW, SOFT, alpha } from "../theme";

// Price beat: optional old price gets struck through, then the price slams in (scale +
// blur), and the suffix ("/month") slides in while the whole group re-centres.
// Measure suffixOffset once from a frame: about half the suffix width.
export const PriceSlam: React.FC<{
  readonly t: number;
  readonly price: string;
  readonly at: number;
  readonly suffix?: { readonly text: string; readonly at: number };
  readonly was?: string;
  readonly note?: { readonly text: string; readonly at: number };
  readonly top?: number;
  readonly size?: number;
}> = ({ t, price, at, suffix, was, note, top = 560, size = 400 }) => {
  const slam = interpolate(t, [at, at + 0.28], [0, 1], { ...CLAMP, easing: OUT });
  const suf = suffix ? interpolate(t, [suffix.at, suffix.at + 0.33], [0, 1], { ...CLAMP, easing: OUT }) : 0;
  const halfPrice = size * 0.29 * price.length;
  return (
    <div style={{ position: "absolute", top, left: 0, right: 0, fontFamily: SANS }}>
      {was && (
        <div style={{ textAlign: "center", fontWeight: 700, fontSize: 64, letterSpacing: "-0.03em", color: C.muted, opacity: interpolate(t, [at - 0.1, at + 0.1], [0, 1], CLAMP) }}>
          <span style={{ position: "relative" }}>
            {was}
            <span
              style={{
                position: "absolute",
                left: -8,
                top: "54%",
                height: 7,
                borderRadius: 4,
                width: `calc(${interpolate(t, [at + 0.1, at + 0.32], [0, 100], { ...CLAMP, easing: OUT })}% + 16px)`,
                backgroundColor: C.alert,
              }}
            />
          </span>
        </div>
      )}
      <div style={{ position: "relative", height: size, marginTop: 20, translate: `${-suf * (suffix ? suffix.text.length * size * 0.06 : 0)}px 0` }}>
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            textAlign: "center",
            fontWeight: 900,
            fontSize: size,
            letterSpacing: "-0.07em",
            lineHeight: 1,
            color: C.accent,
            opacity: slam,
            scale: String(interpolate(slam, [0, 1], [1.7, 1])),
            filter: `blur(${(1 - slam) * 24}px)`,
            textShadow: `0 0 80px ${alpha(C.accent, 0.45)}`,
          }}
        >
          {price}
        </div>
        {suffix && (
          <div
            style={{
              position: "absolute",
              left: `calc(50% + ${halfPrice}px + 24px)`,
              bottom: size * 0.2,
              fontWeight: 700,
              fontSize: size * 0.24,
              letterSpacing: "-0.04em",
              color: C.text,
              whiteSpace: "nowrap",
              opacity: suf,
              translate: `${(1 - suf) * -40}px 0`,
            }}
          >
            {suffix.text}
          </div>
        )}
      </div>
      {note && (
        <div style={{ textAlign: "center", marginTop: 30, fontFamily: MONO, fontSize: 30, letterSpacing: "0.2em", color: C.muted, opacity: interpolate(t, [note.at, note.at + 0.25], [0, 1], CLAMP) }}>
          {note.text}
        </div>
      )}
    </div>
  );
};

// CTA: a button springs in at `inAt`, the cursor clicks it (press + ripple), then it morphs
// into a result card (download, booking, signup...) whose action button the cursor clicks;
// a progress bar fills and the card turns to done. Copy the site's real button (inspect
// lists its colours, font, border, radius, shadow). `top` is the button's top edge; the
// card grows 50 px above and below it. Keep >= 0.3 s between clickAt and morphAt and
// between morphAt and actionAt so the cursor has time to travel.
export const CtaMorph: React.FC<{
  readonly t: number;
  readonly label: React.ReactNode;
  readonly labelSize?: number;
  readonly inAt?: number;
  readonly button: { readonly bg: string; readonly color: string; readonly font: string; readonly shadow?: string; readonly border?: string; readonly radius?: number };
  readonly clickAt: number;
  readonly morphAt: number;
  readonly actionAt: number;
  readonly doneAt: number;
  readonly card: { readonly icon: React.ReactNode; readonly title: string; readonly idle: string; readonly busy: string; readonly done: string };
  readonly actionIcon?: React.ReactNode;
  readonly top?: number;
}> = ({ t, label, labelSize = 60, inAt = 0, button, clickAt, morphAt, actionAt, doneAt, card, actionIcon, top = 960 }) => {
  const y = top;
  const X = 130;
  const W = 820;
  const H0 = 150;
  const btnIn = interpolate(t, [inAt, inAt + 0.34], [0, 1], { ...CLAMP, easing: POP });
  const press = (at: number) => interpolate(t, [at, at + 0.05, at + 0.16], [0, 1, 0], CLAMP);
  const ripple = interpolate(t, [clickAt, clickAt + 0.5], [0, 1], { ...CLAMP, easing: OUT });
  const morph = interpolate(t, [morphAt, morphAt + 0.26], [0, 1], { ...CLAMP, easing: IN_OUT });
  const prog = interpolate(t, [actionAt + 0.06, doneAt], [0, 1], { ...CLAMP, easing: IN_OUT });
  const done = interpolate(t, [doneAt, doneAt + 0.2], [0, 1], { ...CLAMP, easing: POP });
  const h = H0 + morph * 100;
  const cardTop = y - (h - H0) / 2;
  // Cursor path with holds after each click, so the click reads.
  const p2 = clickAt + 0.16;
  const p3 = Math.max(p2 + 0.08, morphAt + 0.02);
  const p4 = Math.max(p3 + 0.12, actionAt);
  const path = [clickAt - 0.26, clickAt, p2, p3, p4, p4 + 0.3, Math.max(p4 + 0.42, doneAt)];
  const clickX = X + W * 0.53;
  const actionX = X + W - 40 - 60 - 12;
  const curX = interpolate(t, path, [1000, clickX, clickX, actionX - 115, actionX, actionX, 1040], { ...CLAMP, easing: SOFT });
  const curY = interpolate(t, path, [y + 620, y + 70, y + 70, y + 200, y + 95, y + 95, y + 640], { ...CLAMP, easing: SOFT });
  return (
    <>
      <div
        style={{
          position: "absolute",
          left: X,
          top: cardTop,
          width: W,
          height: h,
          borderRadius: (button.radius ?? 22) + morph * (44 - (button.radius ?? 22)),
          backgroundColor: morph < 0.5 ? button.bg : C.surface2,
          border: morph < 0.5 ? (button.border ?? "none") : `1.5px solid ${C.line2}`,
          boxShadow: morph < 0.5 ? (button.shadow ?? `0 18px 50px ${alpha(C.accent, 0.25)}`) : SHADOW,
          overflow: "hidden",
          opacity: interpolate(btnIn, [0, 0.3], [0, 1], CLAMP),
          scale: String((0.7 + 0.3 * btnIn) * (1 - press(clickAt) * 0.05)),
          translate: `0 ${(1 - btnIn) * 120}px`,
        }}
      >
        <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: button.font, fontWeight: 700, fontSize: labelSize, color: button.color, whiteSpace: "nowrap", opacity: 1 - Math.min(1, morph * 2.5) }}>
          {label}
        </div>
        <div
          style={{
            position: "absolute",
            left: clickX - X - ripple * 600,
            top: h / 2 - ripple * 600,
            width: ripple * 1200,
            height: ripple * 1200,
            borderRadius: "50%",
            backgroundColor: "rgba(255,255,255,0.45)",
            opacity: ripple > 0 ? 1 - ripple : 0,
          }}
        />
        <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", gap: 30, padding: "0 40px", opacity: interpolate(morph, [0.5, 1], [0, 1], CLAMP) }}>
          {card.icon}
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 52, letterSpacing: "-0.04em", color: C.text, whiteSpace: "nowrap" }}>{card.title}</div>
            <div style={{ fontFamily: MONO, fontSize: 24, color: C.muted, marginTop: 8 }}>
              {done > 0.5 ? card.done : prog > 0 ? `${card.busy} ${Math.round(prog * 100)}%` : card.idle}
            </div>
            <div style={{ marginTop: 18, height: 12, borderRadius: 6, backgroundColor: "rgba(255,255,255,0.08)", overflow: "hidden" }}>
              <div style={{ width: `${prog * 100}%`, height: "100%", borderRadius: 6, backgroundColor: done > 0.5 ? C.success : C.accent }} />
            </div>
          </div>
          <div
            style={{
              width: 120,
              height: 120,
              flexShrink: 0,
              borderRadius: 60,
              backgroundColor: done > 0.5 ? C.success : C.accent,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              scale: String((1 - press(actionAt) * 0.1) * (1 + Math.sin(done * Math.PI) * 0.15)),
            }}
          >
            {done > 0.5 ? (
              <Check size={72} progress={done} color={C.accentInk} stroke={3.2} />
            ) : (
              actionIcon ?? (
                <svg width={60} height={60} viewBox="0 0 24 24">
                  <path d="M12 4v11M7 10.5l5 5 5-5M5 20h14" fill="none" stroke={C.accentInk} strokeWidth={2.6} strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              )
            )}
          </div>
        </div>
      </div>
      <Cursor x={curX} y={curY} press={Math.max(press(clickAt), press(actionAt))} opacity={interpolate(t, [clickAt - 0.3, clickAt - 0.2, doneAt - 0.2, doneAt], [0, 1, 1, 0], CLAMP)} />
    </>
  );
};

// End card: logo pops with a shine sweep, name reveals word by word, then URL and button.
export const EndCard: React.FC<{
  readonly t: number;
  readonly at: number;
  readonly logo: React.ReactNode; // ~220 px square, rounded
  readonly name: string;
  readonly url?: string;
  readonly button?: React.ReactNode;
  readonly top?: number;
}> = ({ t, at, logo, name, url, button, top = 560 }) => (
  <div style={{ position: "absolute", top, left: 0, right: 0, display: "flex", flexDirection: "column", alignItems: "center", opacity: interpolate(t, [at, at + 0.2], [0, 1], CLAMP) }}>
    <div
      style={{
        position: "relative",
        borderRadius: 53,
        overflow: "hidden",
        scale: String(interpolate(t, [at, at + 0.6], [0.4, 1], { ...CLAMP, easing: POP })),
        rotate: `${interpolate(t, [at, at + 0.6], [-20, 0], { ...CLAMP, easing: POP })}deg`,
        boxShadow: `0 30px 90px ${alpha(C.accent, 0.35)}`,
      }}
    >
      {logo}
      <div
        style={{
          position: "absolute",
          top: -60,
          bottom: -60,
          width: 70,
          left: interpolate(t, [at + 0.35, at + 0.85], [-120, 300], { ...CLAMP, easing: IN_OUT }),
          rotate: "20deg",
          background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.75), transparent)",
        }}
      />
    </div>
    <div style={{ marginTop: 54, fontFamily: SANS, fontWeight: 800, fontSize: 112, letterSpacing: "-0.055em", color: C.text, textAlign: "center", lineHeight: 1.05, padding: "0 60px" }}>
      {name.split(" ").map((w, i) => (
        <React.Fragment key={i}>
          <RevealWord t={t} at={at + 0.1 + i * 0.06}>
            {w}
          </RevealWord>{" "}
        </React.Fragment>
      ))}
    </div>
    {url && (
      <div style={{ marginTop: 26, fontFamily: MONO, fontSize: 34, color: C.muted, letterSpacing: "0.04em", opacity: interpolate(t, [at + 0.35, at + 0.6], [0, 1], CLAMP) }}>{url}</div>
    )}
    {button && (
      <div style={{ marginTop: 44, scale: String(interpolate(t, [at + 0.45, at + 0.85], [0.6, 1], { ...CLAMP, easing: POP })), opacity: interpolate(t, [at + 0.45, at + 0.55], [0, 1], CLAMP) }}>
        {button}
      </div>
    )}
  </div>
);
```

### Composition

#### `src/Promo.tsx`

```tsx
import { Audio } from "@remotion/media";
import React from "react";
import { AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Background } from "./components/Background";
import { AudioClock } from "./lib/audio";
import { ExampleScene } from "./scenes/ExampleScene";
import { C, alpha } from "./theme";

// The whole ad: one continuous background, scenes placed on the voiceover's cue frames
// (scripts/cues.mjs), the voiceover, and sound effects. Each scene is its own JSX node
// with inline timing so Studio can retime it. Overlap neighbours by a few frames: the
// old scene's exit plays while the new one enters.
export const Promo: React.FC = () => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Background name="Background" glow={alpha(C.accent, 0.1)} />
      <AudioClock.Provider value={frame}>
        <ExampleScene name="01 Hook" durationInFrames={172} premountFor={fps} />
        {/* <NextScene name="02 Reveal" from={159} durationInFrames={165} premountFor={fps} /> */}
      </AudioClock.Provider>

      <Audio name="Voiceover" src={staticFile("voiceover.wav")} premountFor={fps} />
      <Audio name="SFX whoosh: into 02" src={staticFile("sfx/whoosh.wav")} from={157} volume={0.35} premountFor={fps} />
    </AbsoluteFill>
  );
};
```

#### `src/Root.tsx`

```tsx
import React from "react";
import { Composition, Folder } from "remotion";
import { ContactSheet, sheetMetadata } from "./ContactSheet";
import { Promo } from "./Promo";
import { ExampleScene } from "./scenes/ExampleScene";

// 60 fps keeps fast UI motion smooth on phones. Promo durationInFrames = the frame where
// the voiceover ends (cues.mjs prints it) + ~70 frames to hold the end card.
// For square use 1080x1080, for horizontal 1920x1080 (and rescale layouts).
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="Promo" component={Promo} durationInFrames={1500} fps={60} width={1080} height={1920} />
      <Folder name="Scenes">
        <Composition id="S01-Hook" component={ExampleScene} durationInFrames={172} fps={60} width={1080} height={1920} />
      </Folder>
      <Folder name="Tools">
        <Composition
          id="ContactSheet"
          component={ContactSheet}
          calculateMetadata={sheetMetadata}
          durationInFrames={1}
          fps={60}
          width={2160}
          height={1028}
          defaultProps={{ from: 0, to: 300, step: 20, cols: 8 }}
        />
      </Folder>
    </>
  );
};
```

#### `src/ContactSheet.tsx`

```tsx
import React from "react";
import { AbsoluteFill, Freeze, Sequence, type CalculateMetadataFunction } from "remotion";
import { Promo } from "./Promo";
import { MONO } from "./theme";

// A grid of Promo frames in one image, so Claude can review motion, layout and scene
// hand-offs without watching the video. Render with: node scripts/sheet.mjs <from> <to> [step]
export type SheetProps = { readonly from: number; readonly to: number; readonly step: number; readonly cols: number };

const CELL_W = 270;
const CELL_H = 480;
const LABEL = 34;

export const sheetMetadata: CalculateMetadataFunction<SheetProps> = ({ props }) => {
  const count = Math.floor((props.to - props.from) / props.step) + 1;
  // The sheet must be at least as long as the frames it shows, or nested sequences get cut.
  return { width: props.cols * CELL_W, height: Math.ceil(count / props.cols) * (CELL_H + LABEL), durationInFrames: props.to + 1 };
};

export const ContactSheet: React.FC<SheetProps> = ({ from, to, step, cols }) => {
  const frames: number[] = [];
  for (let f = from; f <= to; f += step) frames.push(f);
  return (
    <AbsoluteFill style={{ backgroundColor: "#202020" }}>
      {frames.map((f, i) => (
        <div
          key={f}
          style={{ position: "absolute", left: (i % cols) * CELL_W, top: Math.floor(i / cols) * (CELL_H + LABEL), width: CELL_W, height: CELL_H + LABEL }}
        >
          <div style={{ height: LABEL, lineHeight: `${LABEL}px`, paddingLeft: 8, fontFamily: MONO, fontSize: 18, color: "#FFE14D" }}>
            f{f} · {(f / 60).toFixed(2)}s
          </div>
          <div style={{ position: "relative", width: CELL_W, height: CELL_H, overflow: "hidden" }}>
            <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, scale: String(CELL_W / 1080), transformOrigin: "0 0" }}>
              <Sequence width={1080} height={1920} layout="none">
                <Freeze frame={f}>
                  <Promo />
                </Freeze>
              </Sequence>
            </div>
          </div>
        </div>
      ))}
    </AbsoluteFill>
  );
};
```

#### `src/scenes/ExampleScene.tsx`

```tsx
import React from "react";
import { Interactive, interpolate, useCurrentFrame, useVideoConfig, type InteractivitySchema } from "remotion";
import { SceneBackdrop } from "../components/Background";
import { BrandIcon } from "../components/Kit";
import { LogoRow } from "../patterns/Beats";
import { CountUp } from "../patterns/CountUp";
import { sceneExit } from "../patterns/motion";
import { C, CLAMP, OUT, SANS } from "../theme";

// "You spend hours editing your own shorts."
// START = this scene's `from` in Promo.tsx, in seconds. Every CUE is a cue-sheet time minus
// START, so it reads as seconds from the scene's first frame. OUT/POP entrances start on the
// cue; IN_OUT moves and flips start 4-6 frames (~0.08 s) before it, because they are slow to
// leave their start position.
const START = 0 / 60;
const CUE = { hours: 0.76 - START, platforms: 1.78 - START, exit: 2.62 - START };

const ExampleSceneInner: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps; // scene seconds: all timing below is in seconds, so fps can change
  // For audio-reactive parts (VoiceBars, live waveforms): const voT = useVoTime();

  return (
    <>
      <SceneBackdrop />
      <div style={{ position: "absolute", inset: 0, ...sceneExit(t, CUE.exit, CUE.exit + 0.24) }}>
        <div style={{ position: "absolute", top: 360, left: 0, right: 0 }}>
          <CountUp
            t={t}
            value={4 * 3600 + 37 * 60 + 12}
            start={0.02}
            end={1.5}
            mode="timecode"
            label="TIME SPENT EDITING"
            highlightAt={CUE.hours}
            tickPerSec={1}
          />
        </div>
        <div
          style={{
            position: "absolute",
            top: 700,
            left: 0,
            right: 0,
            textAlign: "center",
            fontFamily: SANS,
            fontWeight: 800,
            fontSize: 88,
            letterSpacing: "-0.045em",
            color: C.text,
            opacity: interpolate(t, [CUE.hours, CUE.hours + 0.3], [0, 1], CLAMP),
            translate: `0 ${interpolate(t, [CUE.hours, CUE.hours + 0.5], [40, 0], { ...CLAMP, easing: OUT })}px`,
          }}
        >
          every single week
        </div>
        <div style={{ position: "absolute", top: 1000, left: 0, right: 0 }}>
          <LogoRow
            t={t}
            at={CUE.platforms}
            size={220}
            tiles={[
              <BrandIcon key="yt" src="logos/youtubeshorts.svg" size={120} color="#FF0033" />,
              <BrandIcon key="tt" src="logos/tiktok.svg" size={110} color="#FFFFFF" />,
              <BrandIcon key="ig" src="logos/instagram.svg" size={112} color="#FF0069" />,
            ]}
          />
        </div>
      </div>
    </>
  );
};

// Interactive + wrapInSequence: Studio can select, retime and edit the scene, and it opens
// on its own timeline when registered in Root.tsx (a "connected composition").
export const ExampleScene = Interactive.withSchema({
  Component: ExampleSceneInner,
  componentName: "ExampleScene",
  schema: {} as const satisfies InteractivitySchema,
  wrapInSequence: true,
  layout: "absolute-fill",
});
```

