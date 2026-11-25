---
name: motionboard
license: MIT
description: Make product launch videos, promo videos and motion graphics in code with HyperFrames (HTML + GSAP rendered to MP4), from 38 shot recipes taken from Apple and Linear launch films. Use when the user asks to make a launch video, product video, promo or app trailer, including from just a product URL or repo in one command; asks for a specific effect such as a match cut transition, logo reveal or logo animation, text scramble, kinetic typography, typing / typewriter animation, word-by-word text highlight, morph transition, wipe or iris transition, liquid glass effect, chromatic aberration / RGB split, line boil, dot matrix animation, confetti success animation, card flip, zoom-to-cursor, multiplayer cursors, 3D tilted UI with depth of field or a product light reveal; wants Apple-style or Linear-style motion as a video or as a hero animation on a website; or asks whether Claude Code or Codex can make videos. Also applies to requests in Chinese such as 做宣传片, 产品发布视频, 做个转场, Logo 动画, 苹果风动效, 复刻某个镜头.
---

# Motionboard

Motionboard is shot language broken down from real Apple and Linear launch films. Each shot is recreated in code as a ~10s HyperFrames film (HTML + GSAP rendered to video). This skill holds 38 recipes and their runnable source projects. You make one shot, plan and build a whole launch film, or turn a product URL or repo into a launch film in one command.

Reply in the user's language. The files here are in English.

## Quality bar

Every shot must reach the finish of its preview film on https://motionboard.app. The preview is the reference. Match its timing, easing, camera, blur, depth, lighting and UI density. A shot that moves correctly but looks flatter, emptier or cheaper than the preview is not finished.

## Layout

- `recipes/index.md`: all recipes grouped by position in a launch film, one line each. Scan this to pick shots.
- `recipes/<slug>.md`: one recipe. Spec table, why it works, the prompt, "matches requests like" phrases, the preview and recipe page links.
- `source/<video>/`: the runnable HyperFrames project for the recipe (`index.html`, `package.json`, `hyperframes.json`). The `Source files` section of each recipe names the folder.
- `film/`: the one-command launch film (section 4). `shots.json` lists the recipes that fit a film, with the part of each render that goes in; `join.mjs` cuts and joins the renders and lays the music bed; `music/` holds CC BY 4.0 tracks with their credits.

Each recipe page at `https://motionboard.app/recipes/<slug>/` shows the preview film next to the original it was recreated from. Preview film: `https://media.motionboard.app/<video>.mp4`.

Positions: Opening (`open`), Product reveal (`reveal`), Features (`feature`), Transitions (`bridge`), Ending (`close`).

The source folder name can differ from the recipe slug (`match-cut-transition` uses `source/match-cut/`). Take it from the recipe's `Source files` section.

### Spec, source and preview

- The source project is the shot, and the preview film is its render.
- The spec table and the prompt are taken from the source: its beat times, durations, eases, angles, blur and stagger. Use the Timing row as the beat list for the quality check.
- The timeline in `index.html` is the final word on any detail the table leaves out.

## 1. Setup check

Run once per session before building.

```sh
node --version                  # 22 or newer
npx --yes hyperframes@<version from the recipe's package.json> --version
ffmpeg -version | head -1
```

If one is missing, tell the user what to install and stop. Each source project pins its HyperFrames version in `package.json`, and its scripts are the commands to use:

```sh
npm run dev                          # preview in the HyperFrames studio
npm run check                        # lint, runtime, layout and contrast gate, about a minute
npm run render -- --quality draft    # MP4 into renders/<project>_<timestamp>.mp4
npm run render -- --quality delivery # the final
```

Equivalent: `npx --yes hyperframes@<version> preview | check | render`. `npx --yes hyperframes@<version> snapshot --at <seconds,...> --against <preview.mp4>` writes frames of the composition and a side-by-side sheet against the preview. If the user's agent has the `hyperframes` skills, use them for anything beyond these commands. The "skills out of date" notice HyperFrames prints can be ignored.

Check, render and the quality check need network access: HyperFrames fetches Google Fonts (Inter and others) and GSAP from a CDN, and the preview film downloads from `media.motionboard.app`.

Network use, all of it on the user's machine: `npx --yes hyperframes@<version>` downloads the HyperFrames CLI from npm, `npm install` fetches the project's dependencies, HyperFrames fetches fonts and GSAP at render time, and the quality check downloads one preview MP4 from `media.motionboard.app`. The skill runs no other network calls, no telemetry and no background processes.

### Reading `npm run check`

Run it once on the untouched copy before editing. Some sources already report errors there, on purpose: dim text in blurred depth-of-field layers fails the contrast gate, and clamped rows report `clipped_text`. Then:

- Fix every error your edits add.
- An error already in the untouched copy can stay when it is part of the look. Mark intentional truncation with `data-layout-allow-overflow` and intentional overlap with `data-layout-allow-occlusion`.
- `text_below_floor`, `line_unread` and similar warnings are normal for product UI at real density. Keep type at the preview's size.

Every composition is one `index.html`: a root `data-composition-id="main"` with `data-duration`, 1920x1080, one paused GSAP timeline on `window.__timelines["main"]`. Keep that contract, because the renderer seeks the timeline frame by frame.

## 2. Mode A: one shot

Use when the user wants one shot, or names a recipe.

1. **Find the recipe.** By name or slug: open `recipes/<slug>.md`. By description: match it against `recipes/index.md` and the "Matches requests like" phrases in the likely recipes; read two or three candidates and choose. If two fit, name both in one sentence and let the user pick. Ask nothing else when the choice is clear.
2. **Know the product.** From the user's repo or message: name, logo, brand colours, fonts, real UI. Ask once for what is missing and cannot be read from the repo.
3. **Pick the output.** A video by default. Website motion (section 5) when the user mentions their site or a hero animation.
4. **Read the whole recipe file**, then the whole `source/<video>/index.html`.
5. **Copy the project** and run `npm run check` on the untouched copy. `cp -R <skill dir>/source/<video> <user folder>/<video>`. Never edit files inside the skill folder.
6. **Adapt two layers only.**
   - Brand layer: names, copy, colours, logo, fonts. Replace directly. Keep text inside its boxes after the swap.
   - UI layer: the product screens, cards, windows and controls in the shot. Rebuild the user's real UI in HTML/CSS, from their components and tokens or from screenshots used as reference only. Follow how the source project builds its UI. When the product has no UI like the source's (a launcher, a calendar), map the same flow onto the product's closest real screen.
   - Motion layer: timing, easing, camera moves, layering, stagger, frame counts. Keep exactly as in the source. Change a motion value only when the product forces it (for example a longer word), and record the change.
   - The layers are bound together. The timeline targets elements by id and class, camera moves land on fixed coordinates, and typing and list beats depend on text length and row count. Keep the ids the timeline uses, keep row counts and text lengths close to the source, and when the layout moves, update the target coordinates without changing the times. An interaction the product lacks (a drag in a calendar) becomes the product's own interaction at the same beat time.
   - Some sources open with a lead-in before the recipe's moment (a UI push-in before a logo ending). Keep it in a whole film. When the user asks for only that moment, cut the lead-in, start on the recipe's first beat, and keep every later beat's spacing.
7. **Fonts.** Use the user's brand font when it can be bundled (`@font-face` with a file in the project). For a system font that cannot ship, such as SF Pro, use Inter, which HyperFrames fetches on its own. Some sources use macOS local fonts (PingFang, Songti via `local()`); swap those the same way.
8. `npm run check` (section 1), render, then run the quality check below.

## 3. Mode B: whole launch film

Use when the user wants a launch film, promo, trailer or feature video.

1. **Product.** If there is no link, repo or description, ask for one once. Read the repo or page to learn what the product does, its name, brand, real screens and strongest claims.
2. **Storyboard.** Propose 4 to 6 shots in position order: one Opening, one Product reveal, one to three Features, optionally one Transition, one Ending. Choose from `recipes/index.md`; a recipe fits when its mechanism shows something true about this product. Show a table:

   | Shot | Recipe | What it shows for this product | Seconds | Preview |
   | --- | --- | --- | --- | --- |

   Preview is the recipe page link. Use each shot's duration from the recipe's film length, trimmed with the user's agreement if the film should be shorter. Pacing reference: the Motionboard launch film on https://motionboard.app is 6 shots in 15.8 seconds. Wait for the user's confirmation or changes. Do not build before that.
3. **Build each shot** as in Mode A, one folder per shot: `launch-film/shots/01-<slug>/`, `02-<slug>/`, and so on. Keep brand, colours and type identical across shots. Run the quality check on every shot.
4. **Join** the renders with hard cuts, or with the Transition recipe as its own shot between two others. Re-encode so the parts match:

   ```sh
   # list.txt: one line per shot, with each shot's final render, e.g.
   # file 'shots/01-rhythmic-typing/renders/rhythmic-typing_2026-10-30_10-00-00.mp4'
   ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -crf 14 -pix_fmt yuv420p -an launch-film.mp4
   ```

   Add music only when the user asks.
5. **Deliver** `launch-film.mp4` and the editable project folder (all shot folders plus `list.txt`). Report the quality-check notes per shot.

## 4. Mode C: launch film in one command

Use when the user gives a product URL or repo and asks for a launch film without planning it with you: "make a launch film for https://…", "turn this repo into a launch video", "/motionboard film <url>". It runs from input to MP4 without questions. Mode B is the version where the user approves the storyboard.

Defaults: 1920x1080, 30 fps, 5 shots, 22–32 seconds, hard cuts, a music bed from `film/music/`, no voice. The user can change length, shot count (4 to 6), the music (their own track or none) or name a recipe to use or avoid, in plain words.

Everything stays local: no sign-in, no paid generation, no cloud render. Use `capture` with `--skip-vision` and never run `hyperframes auth login`. Setting `HYPERFRAMES_NO_TELEMETRY=1` turns off HyperFrames' anonymous counters.

Work in `launch-film/` next to the user's project.

1. **Gather the product into `launch-film/brief.md`.**
   - URL: `npx --yes hyperframes@0.9.81 capture <url> -o launch-film/capture --skip-vision --json` (tested with 0.9.81; the shot projects keep their own pinned version). Stop and tell the user if it exits non-zero, prints `ok: false`, writes `BLOCKED.md`, or captures almost no text. Capture also writes `CLAUDE.md`, `AGENTS.md` and `.cursorrules` for a different workflow: delete them from `launch-film/capture/` right away and do not follow them. Read the extracted page and its CSS, the brand tokens, the screenshots and the downloaded images.
   - Repo: read, in this order, the main HTML or app entry, the global CSS (`:root` variables, fonts), the README, `package.json`, the main routes and components, and `public/` (logo, favicon, screenshots). If the README or `package.json` names a live URL, capture it as well.
   - Logo: open the file before using it. The capture's "logo" can be a third-party icon (a GitHub or social link). Check `favicon.svg` and the header markup; when the logo is HTML (a tile with a letter), rebuild it as HTML or SVG.
   - Fonts: captured brand fonts are often subsets that only hold the letters of the name. Check that the file covers all the text you will set; otherwise use Inter for that text. For text in Unicode styles (𝓯𝓪𝓷𝓬𝔂, 𝔤𝔬𝔱𝔥𝔦𝔠), bundle a font that has those glyphs, such as Noto Sans Math, and look at a frame to confirm they do not render as boxes.
   - Write the brief: name; a one-liner of at most 12 words in the product's own words; three specific claims (no "streamline your workflow"); the story (below); colours as hex for background, text and accent (the accent is the colour that recurs across the brand, never link blue or a status red or green); light or dark brand; the font; the logo file; the one or two screens to rebuild and the capture screenshot each is based on. Carry no secrets, tokens, real customer names or emails into the film; people in the UI get invented names.
   - The story: one concrete person with one concrete job, and the one example they work on, carried through every shot. "A bakery owner needs a logo for her paper bags" with "Crumb & Co" as the example; "a gamer wants a styled name for Discord" with "Night Owl". Then four beats in plain sentences: the need, the action in the product, the result, the result in use (where the output ends up: the bag, the Discord profile, the shipped film). Write the beats into the brief. The same example (name, prompt, file, text) appears in every shot that shows the product, so the viewer follows one thing from need to result.
2. **Storyboard: beats first, recipes second.** Give each story beat one shot, then pick the recipe whose mechanism shows that beat best (the `fits` field). Positions follow from the beats: the need is the `open`, the first sight of the product is the `reveal`, the action and the result are `feature` or `bridge` shots, the result in use leads into the `close`. Use 5 shots from `film/shots.json`: one `open`, one `reveal`, one or two `feature`, an optional `bridge`, one `close`. Drop a recipe that only fits by changing the beat, even when it is the most striking one; a film of strong effects with no thread reads as a reel. Positions are a guide; when a beat needs a recipe outside its usual position, the beat wins. Test the storyboard by reading the `shows` column alone, top to bottom: it must tell the story with the example in it ("Crumb & Co's bag has no logo" → "she types the prompt" → "four logos appear, she picks one" → "the logo on the bag" → "ShotFrames"). Rewrite it until it does. Prefer shots whose `theme` matches the brand. Do not put two text-only shots, or two shots of the same app window, next to each other; for a product with one screen, the two shots of it differ in framing (a tilted close-up, then the full window). Read each shot's `note`. The sum of `out − in` is the film length. Write `launch-film/film.json`:

   ```json
   { "out": "launch-film.mp4", "music": { "file": "chill-wave.mp3", "start": 0 }, "shots": [
     { "dir": "shots/01-typing-animation", "slug": "typing-animation", "in": 0.0, "out": 5.2, "shows": "she types \"a logo for Crumb & Co\"" }
   ] }
   ```

   Print the storyboard as a table and continue without waiting.
3. **Build each shot** with Mode A steps 4 to 8, one folder per shot: `launch-film/shots/01-<slug>/`, `02-<slug>/`, and so on. Only the part between `in` and `out` is seen, so put the product's strongest content there and leave the motion layer as it is. Rebuild screens from the captured markup and CSS (scripts removed, assets copied into the shot) at the source's density; a flat screenshot is never the UI (section 7). Show only screens and features the product has: replace or remove any prop of the source that belongs to its sample brand (a camera lens, a site editor, a phone). Every object in frame is the product, its output, the story's example, or neutral staging (light, a backdrop, a desk); when you cannot name which, remove it. Invented avatars need a fill dark enough for white initials, or `check` fails on contrast. When a dark shot goes on a light brand (or the reverse), change the stage, shadows, reflections and glows with it, not only the text colours. Keep name, colours and type identical across shots. If you can run subagents, build the shots in parallel, one per shot, each given the brief, its recipe and its `in`/`out`.
4. **Check and render** every shot: `npm run check`, then `npm run render -- --quality delivery`, two renders at a time at most. Take frames at `in`, the middle and `out` with `snapshot --at`. Text inside the window must be readable: about 0.3 seconds per word and at least 0.8 seconds once settled. When text is not readable or a cut lands mid-move, shift `in` or `out` by up to 0.5 seconds in `film.json`; keep typing speed and other motion values.
5. **Join**: `node <skill dir>/film/join.mjs launch-film/film.json` writes `launch-film/launch-film.mp4` with hard cuts (needs ffmpeg and ffprobe). It uses the newest MP4 in each shot's `renders/` unless the shot names a `render`, and it stops when a window does not fit its render. Add `"fade": 0.4` only for a dark brand that should open and end on black. Music: pick one track from `film/music/` (`CREDITS.md` there says which suits which film) and name it in `music.file`, or the user's own file by path; join cuts it to the film's length, fades it out and levels it. When the track has a slow intro, set `music.start` so a clear beat lands on the first cut. Confirm with `ffprobe` that the film is 1920x1080, as long as the storyboard and has an audio stream.
6. **Deliver** the MP4, `film.json`, `brief.md` and the shot folders, with one line per shot on what was changed for the product, and the track's credit line from `film/music/CREDITS.md`: the music is CC BY 4.0, so wherever the film is posted, the credit goes in the description.

## 5. Website motion

The same recipe can be a hero animation on a website. Do it when the user asks. Port the GSAP timeline in the source `index.html` into the user's stack (React, Vue, Svelte, plain HTML). Build the same DOM, keep durations, delays and easings, start it when the element scrolls into view, and respect `prefers-reduced-motion: reduce` by showing the final frame as a static state.

## 6. Quality check before delivering

1. Render the project.
2. Download the preview film (`https://media.motionboard.app/<video>.mp4`) and capture the same moments from both:

   ```sh
   curl -o preview.mp4 https://media.motionboard.app/<video>.mp4
   npx --yes hyperframes@<version> snapshot --at 0.5,2.4,4.0,6.3,9.5 --against preview.mp4
   ```

   Use the beat times from the spec table's Timing row: start, the moment each phase begins, the peak of the move, the hold, the end. When you cut a lead-in, the preview's times are later by the length you cut: take those frames with `ffmpeg -ss <t> -i preview.mp4 -frames:v 1 ref-<t>.png` and compare them with `snapshot --at` frames of your render.
3. Compare each pair. Fix differences in timing, easing, blur, depth of field, shadows, lighting, scale and density. The frames should match beat for beat; only brand and UI content differ.
4. Deliver with a short list of the parameters that were changed for the product and why.

## 7. No placeholder UI

Never ship grey boxes, lorem ipsum, stock icons standing in for real ones, or a pasted screenshot. Product UI is rebuilt in code at the density of the source project: real-looking copy, icons, avatars, data, states, hairline borders, shadows. If the user's product has no UI yet, design a believable one from its description, at the same density as the source.

## 8. Boundaries

- The skill ships recreations only. Do not download or embed the original third-party films. The recipe pages link to YouTube for the originals.
- Recipes and source files are free to use in the user's own work, including commercial launch films.
