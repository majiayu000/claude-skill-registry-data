---
name: gg
description: "You made a game. gg. Turns a web game into a short trailer played live in its own engine: Claude writes the film, opens it in a studio for you to tweak, and exports the mp4 with its music, poster and share copy. Use when someone says \"/gg\" or \"let's gg this\", or asks for a trailer, teaser, launch video, gameplay montage, \"coming soon\" clip, end card or logo reveal for a web game (three.js, React Three Fiber, canvas, Phaser, DOM). Also for launch films of non-game web projects (component libraries, apps, dev tools), where the engine is the real product UI. Also use to add or fix a take in a trailer studio."
---

# /gg

You made a game. gg. Now it gets a trailer, shot in the game's own engine, not mocked up.

Every film gets its own visual direction, drawn from its project: its titles, end card, motion and music are designed for it, never carried over from Git City or from another film. The kit ships one project's treatment (Git City's, in `kit/src/examples/gitcity/` and `kit/tools/arrangements/gitcity.mjs`) as an example of what a direction looks like in code, not as a default.

The film is data: takes on the music's beat grid. The studio plays it live in the game, and the export renders it frame by frame. The kit ships with this skill in `kit/` (MIT). Its API, the studio and the craft notes are in `kit/README.md`: read it before building. This file covers the order of work, and the rules that each cost a round of rework when they were skipped.

Usage: `/gg [direction] [options]`. Options can be flags or plain language:

| Option | Default |
|---|---|
| `--tone <preset or freeform>` | inferred (see Tones) |
| `--kind teaser\|trailer` | teaser if the game isn't out yet, trailer if it is |
| `--duration <s>` | teaser 12–20s, trailer 20–35s |

The deliverables go to `gg-output/`: `plan.md`, `trailer.mp4`, `trailer.jpg` and `share-copy.txt`. The film itself lives in the app, on a studio route.

**Not a game?** The skill works the same for a component library, an app or a dev tool. The "engine" is the real product UI: the library's components rendered on the stage, the app's real screens with stand-in data. A take drives them as a function of `t` the way a game take drives a camera: type into the real input, open the real dialog, toggle the real theme, resize the real layout. The verb is what a user does with it (compose a form, ship a command palette), the spectacle is what it does best (a hundred components re-theming in one frame, a table with a million rows scrolling). No mockups here either: no Figma frames, no screenshots.

## 0. One question first

Unless the invocation already steers ("a teaser, make it feel like…", `--tone`) or says "just go", ask one question (AskUserQuestion):

> **Do you want to steer this trailer, or should I make a first cut on my own?**
> - **First cut:** I pick the angle, the tone and the moments, and you review it in the studio.
> - **Steer:** you tell me what people should feel at the end, and I pitch 2–3 scripts before building.

- **First cut:** infer everything in steps 2–4, research included, then build straight away. The review happens in the studio (step 6).
- **Steer:** ask two things: what the viewer should feel at the end ("I want to jump in and play", "pick a side"…), and whether it's a teaser or a launch trailer. Do the research in step 3 first. Then pitch 2–3 scripts as tables (time, picture, title card, sound), recommend one, and say why. Build the one they pick, one take at a time, with them watching. Keep the scripts they don't pick in `plan.md` for the next launch.

**Why:** a first cut that nobody can steer, built from a guess about the owner's idea, cost a whole round. Having them choose up front keeps the fast path fast and the owner's idea the owner's.

## 1. Set up the kit (skip if the project has a `Studio` from it)

- Copy `kit/src/` into the app (e.g. `src/trailer-kit/`), keeping `kit/LICENSE` with it, but leave out `examples/gitcity/`: it's Git City's look, read from the skill folder as an example only. Copy `kit/tools/` next to the project's scripts, without `arrangements/gitcity.mjs`.
- Add the scripts: `"trailer:export": "node <tools>/export.mjs"`, and one for the audio (`music.mjs` and `sfx.mjs`, see the README).
- Install the export's dependencies: `npm i -D playwright`, `npx playwright install chromium`, and ffmpeg (`brew install ffmpeg`, or `npm i -D ffmpeg-static`). Add `gg-output/` to `.gitignore`.
- Mount `kit/src/examples/MinimalFilm.tsx` on a route (Next.js: `app/trailer/page.tsx`). Start the dev server and check that the studio plays.
- **Not a React project?** The studio is a React page, and the game runs inside one of its stages. Phaser: create the game on a div the stage owns. Plain three.js or canvas: hand the stage your renderer's canvas. Vite: add `@vitejs/plugin-react` for the trailer route only. Angular, Vue or Svelte UI: mount the real app or components in a stage (a custom element, or the framework's own bootstrap on a div the stage owns). What matters is that code can drive the game: set the camera, place the player, trigger the mechanic; or, for a UI, set state, type, open, toggle.
- Match the studio's panels to the project with the `--tk-*` variables (README, "Styling"). The studio's CSS stops at the stage: what's on the stage is the film's own.

In Git City it's already set up: `@trailer-kit/*`, with films at `/trailer/minimal`, `/trailer/demo` and `/trailer/towns`.

## 2. Inspect the project

Read the code: the entry point, levels and maps, the player controller, the camera, the main mechanic, the assets (models, sprites, sounds, music), the logo, the palette and fonts, and the README or store copy. For a library or app: the components or screens, the theme tokens, the demo or docs site, and what users build with it. Skip `.env*`, keys and credentials. Nothing secret or personal goes on screen: if real player data would show, use made-up stand-ins and say so in the plan.

Answer these before planning:
1. What is it, in one sentence?
2. What's the verb: what does the player (or user) do, over and over?
3. What's the fantasy: what does using it feel like?
4. What's the most spectacular thing it can stage (a crash, a boss, a thousand units, a jump; a whole UI re-theming, a table of a million rows)?
5. What does only this project have?
6. Teaser or trailer, and which tone?
7. What should the viewer feel or do at the end?
8. What's the one-line caption for the post?

## 3. Research and direction (before any plan)

Study the project's own language first, then how films for products like it look. Do both before writing a single take.

1. **The project.** Its product and audience, brand, logo, palette, type (the actual font files and weights), motion language (how its UI and site animate: springs or steps, fast or slow, how things enter), sound if it has any, and the copy on its site and README (sentence case or caps, terse or playful). Open its site or docs if it has one and look at it.
2. **References.** Find launch films of similar products and watch them (WebSearch, the product's site, X, YouTube): for a UI library, the launch films of Linear, Vercel, shadcn/ui, Raycast and Framer; for a dev tool or app, the products its users already use; for a game, trailers in its genre and at its scale. For each, note how it opens, how type moves, how it ends, what the music does.
3. **Direction.** Write in `plan.md`: the findings (5–8 bullets), 2–3 references with links and what to take from each, then the visual direction derived from them: the type and how it moves, the palette, the motion (eased or stepped, speed), how titles appear, how the end card lands, what the hits look like (a flash or not, which color), and the music brief (genre, instruments, tempo, mood).

The direction must come from this project and its references, not from Git City: don't carry over its slanted title bars, the stamped sub-title, the white flash, uppercase pixel type, stepped motion or the synthwave song unless this project's own language calls for each one. A calm UI library might want sentence-case type easing in, no flash, and soft keys under it.

**Why:** the kit once shipped Git City's styling as the starting point, and a component library's film came out with Git City's slanted bars, stamp, white flash, caps and racing song. Nothing in it said what the library was.

## 4. Plan

Add to `gg-output/plan.md`: the angle, the hook, the takes as a table (beats, picture, title, sound), the end card and its button, the tone, the BPM, and a draft caption. The takes have to add up to the target length.

**Shape:** a hook in the action (2s) → 2–4 takes of escalation → the climax → a hard cut → the name alone → a button (a short gag after the logo). A teaser withholds: one idea, a few flashes cut at their peak, a freeze with the music dropping out, then the name.

## 5. Build the film

Take the minimal film's structure (it has no look on purpose), with the project's own scenes as the stages (README, "A film of your own").
- Write the takes on the beat grid. Shot recipes are pure functions of `t` that drive the project's real objects: its camera, its player, its world, its components.
- **Design the titles, the end card and the music for this project**, in the direction from step 3. Write your own title renderer for the studio's `titles` slot and your own end card component, in the project's type, palette and motion. `examples/gitcity/` shows how one project did it; read it for the mechanics (driven by the clock in beats, stays mounted), never copy its look.
- Generate the music from the direction's music brief (`music.mjs` with a brief JSON, or an arrangement module of your own; `kit/tools/arrangements/README.md`), at the film's BPM, with its freeze and card beats. Never reuse `arrangements/gitcity.mjs`. Make the effects with `sfx.mjs`, and use the project's own sounds wherever it has them.
- Put every visual hit on a beat, with a sound (`film.sounds`). A flash is a choice of the direction, not a default: decide whether the hits flash and in what color (`--tk-flash`).
- **Before showing anything, step through every take beat by beat** at 0.25× (Home, then Shift+→). Screenshot each beat, look at every screenshot, and fix what they show.

**Why:** several "done" takes were broken (a lost branch, an empty street, a car hidden behind a wall), and only the frames showed it.

## 6. Open it in the studio

Never export the first pass. Give the owner the studio URL and one sentence on the angle, then say: pick a scene to loop it, scrub, and tell me what to change (re-roll a take, another tone, a title). When it's right, press **Export mp4**, or tell me to export.

The owner's corrections, which also apply to your own cuts:
- **Open in the action**, with `trim`, and put the hit on a beat.
- **Keep screen direction across a cut.** If the cars leave going away from the camera, the next take doesn't come toward it.
- **"Make it longer" means rethink how the take opens.** Never just let it run on at the end.
- **When a camera change is rejected, go back** to the version that worked. Don't invent a third.
- **Nothing between the camera and the subject.** Check the line of sight against the map.
- **A sound the owner calls bad gets rebuilt from scratch**, not re-pitched.
- A reference the owner shows (a social card, a profile) is for colors and type only. Don't copy its layout.

## 7. Export and deliver

`npm run trailer:export -- <studio url> --poster <s>` renders every frame headless on a virtual clock, mixes the song and effects from the film's cues, and bakes the poster in as frame 0, the frame every platform uses as the thumbnail.
- **Poster:** pick the strongest settled frame: the name on the end card, or the climax freeze. Never pick a frame mid-transition.
- **Keep old exports:** if `gg-output/trailer.mp4` exists, pass `--out gg-output/trailer-2.mp4`.
- **Look at the export before handing it over.** Make a contact sheet (`ffmpeg -i trailer.mp4 -vf fps=3,scale=400:-1,tile=6x6 -frames:v 1 sheet.jpg`), read it, and check the sound is there.
- **`gg-output/share-copy.txt`:** 1–3 sentences, postable as they are, specific to the game, in the film's tone. No "excited to share".
- **Tell the owner** where the video and the caption are, and offer to re-roll a take or try another tone.

## Creative laws

- **Short.** A teaser is 12–20s, a trailer 20–35s. Not a second more without a reason.
- **The hook is everything.** The first 2 seconds decide whether anyone keeps watching. Open mid-action, never on a logo or a menu.
- **Show the game running.** Everything on screen comes from the real engine and the real assets. No mockups, no screenshots panned over, and no abstract filler.
- **Sell a feeling, not features.** A montage of features reads as a list. Give the takes cause and effect and someone to root for.
- **Titles carry stakes, not verbs.** "Drift / Fire" cards are feature cards. Use 3–4 cards of 2–4 words at most, none in a teaser. A card holds long enough to read (about 0.3s a word, 0.8s at least).
- **Every hit lands on a beat, with a sound.**
- **Silence before the name.** The music drops out (or holds one note) right before the end card, so the name lands in the quiet.
- **Hard cut to the end.** The last hit cuts straight to the card, no fade or dissolve.
- **The name alone.** The end card is a film ending, not a web page: the name, big and by itself, then at most one short line and an optional button (a short gag after the logo). No footer, chips, frames or URL: the post carries the link. How the name arrives (eased, stepped, typed, drawn, with or without a sub-title) comes from the project's direction.
- **Specific.** It must look made for this project, in its own palette, type, motion and sound. Nothing from another film's treatment, Git City's included.
- **Funny earns its place.** The humor comes from the game itself, not from trying.
- **Every frame is postable.** Any frame, frozen, should be worth sharing.

## Tones

Presets are defaults. Freeform direction ("a 90s console ad", "a Nintendo Direct reveal") maps to the nearest preset for pacing and keeps its own words in the plan.

| Tone | Feel | Pacing, titles, sound |
|---|---|---|
| `hype` (default) | Launch-day energy, punchy | 5–7 takes of 1–2.4s; 2–3 stakes cards; drop on the first hit |
| `teaser` | One idea, withheld | 3–4 flashes cut at their peak; freeze and silence; name, "coming soon"; no cards |
| `story` | A protagonist and a turn | Hook, act break, escalation, climax; see the README's Invasion, Grudge match and Scoreboard skeletons |
| `cinematic` | Epic, slow, wide | 3–5 long takes; low drone, then one big hit; huge type |
| `arcade` | Loud and fast | Cuts under 1s, flashes, score counters ticking; chiptune energy |
| `mobile-ad` | A parody of mobile game ads, played straight | A fake "fail" run, "only 1% can…", a big finger, then the real game |
| `deadpan` | Calm and dry | Long holds, empty space; the game's absurdity carries it |
| `product` | A product launch film | 4–6 takes of the real UI doing its best thing; calm type, one idea per take; music under, not over |

## Engine pitfalls (so they don't recur)

- **Anything with a canvas stays mounted the whole film.** Remounting it drops the WebGL context within a few loops.
- **Shot recipes are pure functions of `t`**, and particles only emit while the clock moves, so a paused frame stays clean.
- **Declare timeline constants before using them.** Lists built at module load (sounds, flashes) fail at runtime, not at build.
- **Reset what a take breaks** in `onReset`. The studio calls it on a pick, a loop, a seek back, and at the start of a recording or an export.
- **The export only hears `film.sounds` and `film.song`.** Sounds the game plays on its own through Web Audio aren't recorded, so cue them in the film.
- **The export controls time, not video files.** A `<video>` inside the stage plays on real time. Draw it from code, or leave it out.
- **Seed any randomness** that has to look the same in the studio and in the export.
