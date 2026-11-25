---
name: launch-film
description: "Make a short, result-first launch film for a product, feature or skill: a 15 to 30 second 1920x1080 MP4 with the payoff on screen in the first seconds, one object carried across every beat, cuts on a 128 BPM grid, an optional motion pass (depth field from the real UI, story camera, light scene changes) measured for pace and read time, an original synthesized score and a locked brand kit. Renders HTML to MP4 with the bundled Playwright renderer or HyperFrames, no video editor. Use when someone asks for a launch video, product teaser, feature reveal or a short social video for a launch. Not for narrated explainers, talking heads or editing existing footage."
license: Apache-2.0
metadata:
  version: "1.1.0"
  author: Floom
---

# Launch Film

Make the viewer want the capability before explaining the mechanism. Deliver a playable MP4 and its editable source, not a storyboard. Keep the brand exact and every claim sourced.

## Read first

1. [Film language](references/film-language.md): editing, typography, motion and audio.
2. [Brand kit](references/brand-kit.md): what to lock before the first frame, and the bundled example kit.
3. [Evidence rules](references/evidence.md): claims, sources, recordings, ownership and labels.
4. [The one-stage film](references/one-stage-film.md): the HyperFrames build behind the example films, with the traps that cost re-renders.
5. [Delivery and QA](references/delivery-qa.md): render, inspect and package.
6. [Motion kit](references/motion-kit.md): the depth field, story camera, rack focus, flares, iris, kinetic type and odometers in `assets/motion/motion-kit.js`, and the rules that keep it readable.
7. [Pace and digestibility](references/pace-and-digestibility.md): the pace metric, the read-time rule and our before and after numbers.

Read the user's brief and available assets before asking questions. Keep decisions they already approved. Default to a 16 to 30 second, 1920×1080, 30 fps film that works with the sound off. Vertical crops need their own composition, not a centre crop.

## Workflow

### 1. Inspect and classify the assets

Reuse a working project, renderer or asset set before building another. Inventory every item with its path, source, author, date, role and status, and tell apart:
- a real agent recording and its real output;
- a creator showcase;
- a newly authored demonstration;
- a workflow visualization;
- reference-only footage;
- material that is only linked, not present.

A filename or link does not prove the bytes are present, and public availability does not grant redistribution rights. Never present a design mockup as a product capture.

### 2. Lock the brand

Get the user's logo SVG, colour tokens and type (see the brand kit reference). If they have none, use a neutral palette and ask before inventing anything that looks like a brand. Never regenerate a logo with an image model. Check the font actually loaded before any render.

### 3. Choose one demonstration

Write the one-sentence promise and name the visual that fulfils it. One task, one product or skill, one result. A strong uninterrupted result beats several weak ones. Do not claim a live run, an automatic pick or a speed-up unless this film shows that real run.

If the real recording is not available, build a clearly labelled first cut, record the gap once, and keep going.

### 4. Build the cut

| Beat | About | Job |
| --- | --- | --- |
| Hook | 0 to 3 s | The pain or the result is readable on frame 0. One short line. |
| Problem or source | 3 to 6 s | Show the bad draft, the full inbox, the real source. No invented engagement. |
| Request and pick | 6 to 10 s | The exact request is typed; the tool or skill that handles it attaches to it. |
| Payoff | 10 to 13 s (longer in a 30 s film) | The output takes over and visibly works. |
| Why it matters | 13 to 15 s | One line. |
| End card | last 1.5 to 2 s | Logo, one line, one confirmed destination. Locked. |

Cut on the beat grid. Carry one object (a card, a frame, a highlight) from beat to beat so every change is motivated. One thought per shot, no em dashes in new copy.

### 5. Add motion (optional, after the flat cut works)

Check every beat against the read-time rule in [pace and digestibility](references/pace-and-digestibility.md) first and cut words where a beat is short: copy density, not motion, sets the digestibility score. Then add the motion layer with `assets/motion/motion-kit.js` (see [motion kit](references/motion-kit.md)):

- a depth field built from crops of the film's own UI, never stock or someone else's footage;
- a camera on the content plane with every key on a story cue, landing in 0.65 s or less;
- rack focus, a flare and ring at each event point, and an iris from the click into the next scene;
- glyph springs on one or two statement lines and odometers on real, sourced values only;
- one short sound per event from `kit.events()`, under the score.

The camera rests while text is read, text never moves while it is read, and there are 0 flashes. Pilot the busiest 6 to 8 seconds first, run `python scripts/pace.py` on the flat film and on the pilot, look at stills, then render the whole film. Brand colours come from the user's tokens.

### 6. Render

Two paths, both HTML to MP4:

**Starter (canvas, bundled renderer).** A working 30-second starter is in `templates/film/` with the example brand kit:

```bash
python scripts/prepare.py ./my-film
# edit my-film/brief.js and brief.json: replace every REPLACE line
python scripts/synthesize_audio.py --out ./my-film/audio/original-score.wav
python scripts/preflight.py ./my-film --mode preview
python scripts/render.py ./my-film --out ./my-film.mp4
```

The template exposes `window.renderAt(seconds)` and `window.__ready`. The renderer supports `--fps`, `--width`, `--height`, `--duration`, `--chromium` and `--stills`. Its ORBIT sculpture is an original procedural motion study, not a Three.js build and not an agent output.

**One-stage film (HyperFrames).** For product UI stories (a prompt, a document, an inbox, a result), build one live HTML stage with one GSAP timeline and render it with HyperFrames, locally or in the cloud. Follow [the one-stage film](references/one-stage-film.md). This is how the example films in `examples/README.md` were made.

### 7. Inspect and correct

Render stills first, then the whole film. Look at the first frame, every transition, the result, the small print and the end card at phone-feed size. Check typography, motion continuity, frame count, audio, and that nothing flashes or goes blank. With a motion pass, report the pace numbers (mean, p50, static share, flashes) before and after. Fix what you see before adding flourishes. Check stills from the real render, not only the local browser: render machines can lack fonts and emoji.

For an evidence-led release run `python scripts/preflight.py PROJECT --mode final`. It passes only with local evidence and cleared assets for the claims made. Passing preview does not make a film publication-ready.

### 8. Deliver

Return the MP4, the editable project and a short note: is it a recording-based demonstration, a creator showcase or a labelled first cut, and what evidence or rights gap remains. Do not publish, upload, post or change any account unless asked.

## Hard constraints

- No fabricated prompts, posts, ratings, tool receipts, benchmarks, creators or endorsements.
- No simulated result presented as an observed run.
- No music taken from a reference film. Use a cleared track or the synthesized score.
- No font binaries, credentials or private files in the project you hand over.
- Real people and companies appear on screen only with permission; otherwise use fictional ones.
- No em dashes in new copy.
- Do not stop at an image board when the user asked for a video.
