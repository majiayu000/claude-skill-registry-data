---
name: opendesigner-paint
description: Original art painted in code in the brand's palette. A hero or launch film, a celebration loop, or a still in watercolour, pointillism, charcoal, sketch, woodcut or 2D cel.
license: MIT
compatibility: Python 3.10+ (standard library) for the bridge. Painting runs the bundled engine in a film project and needs Node 18+, npm packages, Playwright's Chromium and ffmpeg, installed with the person's OK.
metadata:
  version: "0.3.1"
  homepage: "https://github.com/ckryptickunal/OpenDesigner"
---

# OpenDesigner: painted art and films

Use this when someone wants original art made by code rather than found art. Typical asks: a painted hero, a launch film or reel, an animated brand moment, a celebration loop, a painted link-preview image, or "something that looks hand-made, in our colours". It is also an answer for three designer hooks when the person has nothing:
- `H-motion`: a signature animation.
- `H-illus`: original illustration, when open-library art would read generic.
- `H-motif`: painted grounds and textures.

Everything is in this folder:
- **The bridge** (`scripts/paint.py`, Python standard library, offline). It reads the design system and writes a brief, a palette and rules. It scaffolds film projects, checks scenes, and brings finished work into the app with accessibility safeguards and a ledger.
- **The painting engine** (`engine/`, `styles/`, `scripts/new-film.sh`). It is vendored from generative-painting-skills (MIT, commit 1ff8212; `THIRD-PARTY.md` lists what changed). It plans shots, paints plates procedurally with p5.js and p5.brush, edits them with hard cuts, adds particle motion and a quiet score, and exports MP4, WAV and lossless PNG files that must pass automated checks.

Talk plainly: one idea and one question per message, and recommend one option with its reason. The first time a term appears, give its plain meaning plus "Designers: X · Code: Y" (`references/rules.md` in the opendesigner skill).

Run `paint.py` (`scripts/paint.py`) from the person's project root. Knowledge:
| File | Read it when |
|---|---|
| `references/flow.md` | First: the whole process, what the person does and what exists after each step |
| `references/brand-to-paint.md` | Explaining or overriding any line of the brief |
| `references/painting-workflow.md` | Planning and painting: shot list, plates, motion, sound, export (the engine's own guide) |
| `references/choosing-and-mixing-styles.md`, `styles/<style>/STYLE.md` | Choosing or mixing styles; how each material works |
| `references/editing.md`, `drawing-kit.md`, `motion-in-the-medium.md`, `sound.md`, `widescreen-and-titles.md`, `verifying.md`, `experimenting.md`, `adding-a-style.md` | The step you are on |
| The images each `styles/<style>/STYLE.md` lists under "See it first" (`styles/<style>/examples/`, `references/*.jpg`) | Before choosing a style: what each one looks like |

## Hard rules
- **Ask before installing.** Each film project needs `npm ci` (p5, p5.brush, Vite and Playwright, every package pinned by `engine/package-lock.json`) and `npx playwright install chromium`. Both download code. `paint.py scaffold` prints them and never runs them: get a yes first. `scripts/new-film.sh` installs at once, so it is for people running it by hand.
- **Structure, never identity.** The watercolour scene library reconstructs one earlier film; three ported sketches of unknown authorship are left out. Use the library for composition, rhythm and archetypes only. Every shipped plate needs this product's own subject and the brand palette. `paint.py lint` flags library scenes left in their original colours (`guardrails.md`).
- **The brand palette only.** Scenes take colours from `src/brand.js`, one family per plate. Pigment mixing makes in-between colours; that is the medium, not drift.
- **No text painted into plates.** Words go in a fixed-anchor phrase track, measured at 4.5:1 under the glyph mask (WCAG 2.2 AA is locked). The font must be licensed for rendering into video and images; never guess a licence.
- **Motion stays where motion belongs.** Films and loops go in marketing, onboarding and celebration moments, never on functional screens (DC-L05-21, STD-when-to-animate-11; over 1 s only because it is illustrative, STD-easing-duration-09). In the app a film is:
  - muted;
  - shown as a still for `prefers-reduced-motion`;
  - given a pause control past 5 s (WCAG 2.2.2).
  `paint.py ingest` writes all three.
- **Determinism is the engine's contract.** All randomness goes through the seeded kit, never `Math.random`. Plates are painted once and held. Integer frames are the source of truth.
- **Report what was checked.** Say what the export measured, and what you actually looked at or listened to.

## 1. Look
- `paint.py doctor`: the engine and styles here, Node, npm, ffmpeg and Python.
- Read DESIGN.md and `opendesigner/state.json`:
  - the dials;
  - the answers to `Q-img-04`, `Q-img-06` and `Q-img-07`;
  - the `H-motion`, `H-illus` and `H-motif` hooks;
  - the product, its audience and its "memorable thing".
- **Without a design system:** use `--accent '#hex'`, and offer the opendesigner interview first.

## 2. Brief
```
python3 paint.py brief --slot hero|launch|onboarding|celebration|og-image|empty-state|background [--message "..."] [--style ...]
```
It writes `opendesigner/paintings/<slot>/brief.md` and `brief.json`:
- the recommended style and why (from the dials, or `Q-img-04`);
- whether mixing styles is allowed;
- 7-9 palette families (one more per extra accent ramp) built only from the token ramps, each marked for legible text;
- the font decision;
- the slot's size and length (the engine paints 600x600 squares; other sizes need the compositor in `references/widescreen-and-titles.md` §2);
- the motion, sound and identity rules.

Show the style and a line per family, then ask: this style, or another?

## 3. Scaffold (ask first)
```
python3 paint.py scaffold <film-dir> --style <style> [--id <film-id>]      engine + demo + src/brand.js + BRIEF.md; installs nothing
cd <film-dir> && npm ci --no-audit --no-fund && npx playwright install chromium        only after the person's yes
```
The demo scenes are placeholders. `npm run export` once confirms the machine works.

## 4. Plan and paint
Follow `references/painting-workflow.md`:
1. Shot list: show it and get it approved.
2. One scene per plate, started from the closest scene-library recipe, with colours from `src/brand.js`:
   ```js
   import { family } from '../brand.js';
   const F = family('brand-night');
   ```
3. `npm run plates -- --only <id>`, then look at each plate at full size.
4. Motion and sound. Particle colours live in `src/particles.js`: recolour the palettes of the motions you use from `src/brand.js` (`lint` checks them).

For charcoal and sketch, set `PLATES[id].material.paper` to the brief's paper colour.

## 5. Check
```
python3 paint.py lint <film-dir>     brand colours (scenes and particles), seeded randomness, no text in plates, no unadapted library scenes, length
npm run export                       the engine's checks; it refuses to finish if one fails
```
Then do a visual review (`references/verifying.md`) and judge as `opendesigner-illustrate/references/ranking.md` asks. `python3 tools/cut_audit.py out/<film>` needs numpy and scipy.

## 6. Bring it into the product
```
python3 paint.py ingest <film-dir> --to src/components/brand --as react [--poster <plate-id>] [--label "..."]
python3 paint.py ingest <film-dir> --to public/art --as img
```
`ingest` does four things:
- **Refuses** a failed export.
- **Copies** the MP4 and a poster: a plate from `npm run plates`, or else the film's anchor frame for that plate.
- **Writes** the component: muted, a reduced-motion still, and a pause control past 5 s. Decorative art gets `aria-hidden`; meaningful art gets `--label`.
- **Logs** a ledger row and `CREDITS.md`.

Then:
- Look at it in the running app, on phone and desktop, light and dark, with reduced motion on and off. The opendesigner-review skill does this with evidence.
- `engine.py set hooks.H-motion.status '"tool"' --why "painted with opendesigner-paint"` (or `H-illus`), then `engine.py review`.

## Hosts
- **Claude Code, Codex, Cursor:** everything above, once the person agrees to the installs.
- **claude.ai:** the sandbox usually cannot install Chromium or ffmpeg. Write the brief and the scenes there; paint and export on the person's machine.
- **No code:** the brief works as a written commission for a person or a tool.

If something was missing, wrong or confusing, record it with `engine.py feedback "..." --kind gap|bug|confusing|idea` (`references/improve.md` in the opendesigner skill). Nothing is posted without the person's OK.
