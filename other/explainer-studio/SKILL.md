---
name: explainer-studio
description: 'The guided end-to-end path for building an animated explainer video from zero — walks you phase by phase (script → assets → choreography → retention → gates → voiceover → publish), telling you which skill and tool to use at each step and what "done" means before advancing. Use when starting a new explainer video, when unsure what to do next mid-build, or when someone asks to be guided through the process.'
user-invocable: true
---

# Explainer Studio — the guided build path

Seven phases, in order, each with an **exit checklist**. Never advance with an unchecked box — every skipped gate here has cost a rebuild in production. The three companion skills are your phase manuals: **explainer-assets** (make the things), **gsap-explainer** (move the things), **retention-pass** (make people keep watching). When guiding a person, announce the phase, do the work, show the checklist result, then ask to advance.

## Phase 0 — Topic & Promise (15 min)
Decide: WHO is this for, WHAT one payoff do they get, and what does the PEAK scene show? Write three sentences: the hook's promise (a question, never the answer), the peak that pays it (must visually rhyme with the hook), and the next-video chain for the CTA.
**Exit:** ☐ hook promise written ☐ peak described in one sentence ☐ hook and peak use the same visual language ☐ CTA chains somewhere named.

## Phase 1 — Shot Script (1-2 hrs)
One markdown doc, one block per scene: timestamp · duration · VISUAL (what literally happens) · ON-SCREEN text · VO line. Write VO at **~2.5 words/sec × duration** (real TTS/readers run ~2.6 w/s). 8-12 scenes for 3-4 min; scene ceiling ~30s. Enumerations must list items in the order visuals will land. End with an accuracy checklist — verify every factual claim now, not after animation.
**Exit:** ☐ every scene has all five fields ☐ word counts ≈ 2.5×duration ☐ facts verified ☐ second-to-last scene is a peak/drill, not wrap-up.

## Phase 2 — Assets & Components (invoke **explainer-assets**)
BEFORE any animation: inventory every visual the script demands — components (chips/bars/cards), props (per scene), characters (host + minions), environment moods. Build in this order: **component system first** (one CSS recipe elevates everything), then props (silhouette → light → depth → detail → motion hooks), then character factories, then environment variants. Decide every prop's animation class and pivot (`svgOrigin`) NOW.
**Exit:** ☐ all assets render in static scenes ☐ silhouette test at thumbnail size ☐ one light direction everywhere ☐ no flat fills ☐ every asset has its motion hook class + planned pivot ☐ selector inventory written down.

## Phase 3 — Choreography (invoke **gsap-explainer**)
Copy `scaffold.html`, run `inline-gsap.py`, confirm it plays untouched. Replace scenes ONE at a time using the pattern library (drop-with-weight, forced-overlap proof, pour/morph-fuse, stamp slam — adapt, never invent). Keep the VO-sync contract from the first scene: the named object moves ON its name; enumerations reveal with the roll-call; payoffs resolve WITH their reasoning. `node --check` + freeze-frame QA after every scene before starting the next.
**Exit:** ☐ full playthrough, zero console errors ☐ every ACTS starts with resets (replay/seek test each scene) ☐ every VO content phrase has a beat within ±1.5s ☐ each scene's hero moment freeze-framed and eyeballed.

## Phase 4 — Retention Pass (invoke **retention-pass**, 3 rounds)
Round 1 structure (hook/peak loop, trim scenes to choreography), Round 2 beat coverage (`tools/beat-audit.mjs` — fill dead zones with content beats, not ambient), Round 3 polish (loop-naming kickers, stakes accents, exit velocity).
**Exit:** ☐ beat-audit: last beat at 70-85% of every scene, no >4s true dead zones ☐ hook loop closed BY NAME at the peak ☐ first beat ≤0.5s ☐ nothing announces duration or wrap-up early.

## Phase 5 — The Gates (zero tolerance)
Run all six pre-publish gates from gsap-explainer, headline: **overlap audit at 0.5s steps** (`tools/overlap-audit.js`) — nothing overlaps anything unless it IS the lesson (whitelist those pairs explicitly). Plant a fake overlap first to prove the tool sees your file. Then replay-reset audit, selector inventory, beat-audit no-regression.
**Exit:** ☐ overlap audit returns zero non-whitelisted at 0.5s ☐ fake-overlap control was caught ☐ replay/seek sweep clean ☐ syntax + selectors green.

## Phase 6 — Voiceover (tools/vo-generate.py)
Generate one clip per scene (ElevenLabs or any TTS; voice id is yours). Check every clip vs its scene: target **85-94% fill**; on overrun EXTEND the scene to clip+1.5-2s (extending never strands beats — trimming does). Build the `-vo.html` preview variant (master stays silent); wire clip-per-scene playback so seeking restarts narration cleanly.
**Exit:** ☐ every scene 85-94% narrated (CTA may be short) ☐ no clip overruns ☐ pause/seek/replay all behave with audio.

## Phase 7 — Human Watch-Through & Publish
The one gate no tool replaces: watch the whole video in a real browser at real speed, sound on. You are looking for: anything overlapping, any beat landing before/after its line, any prop that reads wrong at a glance. Fix, re-gate (Phase 5), publish. Keep the master silent version for re-recording; export = screen-record or your pipeline of choice.
**Exit:** ☐ full real-time watch with zero winces ☐ re-gated after any fix ☐ published + versioned.

## If you're lost mid-build
Ask: "does it exist?" → Phase 2. "Does it move?" → Phase 3. "Does it hold attention?" → Phase 4. "Is it clean?" → Phase 5. "Does it talk?" → Phase 6. The most common failure is starting Phase 3 with Phase 2 half-done — animating assets that then get rebuilt, breaking every tween that targeted them.
