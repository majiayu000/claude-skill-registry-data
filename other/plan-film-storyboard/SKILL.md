---
name: plan-film-storyboard
description: Generate a reviewable film-storyboard frame set from a script, scene, synopsis, dialogue draft, or existing storyboard, with continuity-safe shot planning and image-generation receipts. Use for live-action, AI-video, or hybrid film and vertical-drama previsualization; do not use for comic-page layouts, prose writing, final video generation, editing supplied footage, or unauthorized story rewrites.
---
# Generate Film Storyboard

## Catalog

- Display name: Generate Film Storyboard
- Categories: Film, Layout & Design
- Status: Ready
- Route label: GPT Image 2 continuity-safe storyboard frames
- Tone: purple
- Short description: Generate reviewable film storyboard frames from narrative material with continuity locks.
- Similar skills: develop-story, plan-comic-storyboard, render-comic-page
## What this skill does

- Freezes source facts and adaptation permission before translating narrative material into visible storyboard frames.
- Plans blocking, props, screen direction, camera, and continuity as atomic shots, then generates the approved frames.
- Returns inspected storyboard images, a shot manifest, and execution receipts without claiming final-video approval.

## How to use

Provide the source, requested frame count, ratio, live/AI/hybrid production mode, language, fixed facts, cast/assets, visual direction, and allowed change level: faithful, visual, pacing, or explicitly scoped story changes.

#### Example

```text
Generate four 16:9 storyboard frames for episode 1. Stay faithful to the plot, externalize internal thoughts through behavior and composition, keep the character and wardrobe consistent, and provide the shot manifest with each generated frame.
```

## Workflow

1. Record source/version, fixed facts, unknowns, and requested changes without rights, consent, privacy, or evidence-authenticity checks. Default to faithful; never treat “improve” as permission to alter plot causality.
2. Extract scenes, characters, knowledge states, locations, time, props, dialogue, sound, and must-preserve beats. Convert internal explanation into observable action, reaction, composition, on-screen information, or sound without inventing a fact.
3. Before expanding the full manifest, propose a compact design pass: visual concept, recurring motif with establishment/variation/break, spatial power geometry, one justified non-default choice, and style coordinates. Get direction approval when these choices materially affect production; then break beats on changes in action, information, power, attention, place, time, or physical result.
4. Plan blocking and screen direction before camera. Make every formal shot atomic: one continuous time/place, one primary purpose, one dominant shot size, one main action, and at most one simple camera move. Record start/end state, subject/action, composition, angle, duration, dialogue, sound, props, continuity locks, source trace, production method, editorial motivation, and acceptance.
5. Confirm dialogue, action, reaction, camera, and sound fit the duration. For material action, make the preparation, exertion/contact, result, and settling end state observable; include secondary physical effects only when story-relevant and feasible. Split overloaded shots, especially multi-person dialogue, complex hands/props, action chains, large framing changes, or hidden edits.
6. Validate adjacent end/start states, eyelines, axis, entrances/exits, wardrobe, injuries, prop handoffs, knowledge, time, and sound bridges. Maintain coverage for every fixed beat and required reaction.
7. Inventory which recurring character, subject, scene, style, first-frame, and end-frame references actually exist. Bind every character and environment reference before generation. Propose missing reference assets and continue through the supported API without a client-side confirmation.
8. For each storyboard shot, compile an image prompt with supplied references, visible start/end state, one action, camera, ratio, preservation locks, risks, and a simpler fallback. Use `gpt-image` v1.0 / GPT Image 2 with `quality: "medium"`, `imageSize: "2K"`, the requested supported `aspectRatio`, and `batchCount: 1`. Persist one stable operation key per frame, require a non-empty execution ID, and poll each run to a terminal state before continuing.
9. Inspect every generated frame for character identity, wardrobe, props, screen direction, composition, action legibility, continuity, and unwanted readable text. Repair only the failed frame with a materially strengthened prompt; never regenerate accepted frames. Deliver the source/fact ledger, generated frame set, shot manifest, continuity report, execution receipts, and generation handoffs. The frames are previsualization, not final-video approval.


## User-facing output

- Media type: Film storyboard frame image set plus shot manifest and execution receipts
- Default quantity: 4 frames unless the user requests another count
- Content per artifact: One continuity-safe key frame with its source facts, shot intent, camera, composition, and preservation locks
- Default layout: User-requested supported ratio with stable scene/shot IDs
- Model policy: GPT Image 2 Medium/2K with supplied reference assets
- Downstream use: Live production, video-generation Atoms, and editing/assembly
