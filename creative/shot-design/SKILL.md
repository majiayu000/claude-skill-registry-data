---
name: dircreative-shot-design
description: Convert script and breakdown into professional shot list, camera plan, blocking plan, and shot QA.
---

# Shot Design

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/schemas/prompt-ir.schema.json`
- `docs/film-preproduction/prompt-authoring-standard-v1.md`
- `docs/film-preproduction/chat-co-creation-interface.md`
- `docs/film-preproduction/chat-inline-visualization-interface.md`
- `docs/film-preproduction/professional-agent-voice-standard.md`
- `docs/film-preproduction/schemas/shot-list.yaml`
- `docs/film-preproduction/shot-language-standard.md`
- `docs/film-preproduction/research/film-production-glossary.md`
- `docs/film-preproduction/research/audio-design-notes.md`

## Inputs

- script
- script breakdown
- audio policy

## Outputs

- shot list
- camera plan
- blocking plan
- shot QA

## Chat Surface

Deliver the requested shot plan with canonical shot IDs, continuous timecodes,
visible start/action/end, camera motivation, performance, sound and continuity.
A bounded shot revision returns only the affected shot and necessary dependency
changes. Complete technical shot tables use the detailed fields below; a client
narrative board remains at its requested layer. Review internally and continue
requested visual/asset work without a separate shot-approval round.

## Visual Decision Contract

When visualization adds clarity, use `skills/dircreative/assets/visualizations/stage-surface-registry.json#shot-density-timeline`. Keep the inline timeline compact; request fullscreen for 30 or more shots or dense inspection. Bind every displayed shot to the current shot-list artifact and preserve a table fallback.

For two-or-more-person blocking, movement, eyeline or reverse-shot discussion,
use the root `spatial_discussion` layer and its current-host display contract.
Keep world positions fixed across reverse shots: changing the view must not
mirror the room. The displayed layout is presentation-only until a user adopts
it; then update only the affected existing scene/shot facts and mark their
derived references or prompts stale.

## Rules

- One intelligible main event per shot; a causal exchange may contain several
  connected actions. Use `references/prompt-structure.md` when translating it to
  video prose; do not turn readability into a universal one-verb or slow-motion rule.
- Keep the intended action intensity and its preparation, force, contact,
  response and consequence. A single dramatic event can be fast and forceful;
  readability does not require slow, slight or contact-free movement. Storyboard
  the decisive phase as needed instead of making every image a video start pose.
- Derive shot count from information, action and editing needs; explain a decision only when useful.
- Distinguish `12 customer story sections` from the real shot/rhythm plan. Derive shot and panel counts from information, action and editing coverage, not a universal per-minute quota. Legacy client-contract count checks are a separate compatibility constraint, not the creative standard.
- Every shot needs timecode, duration, story beat, narrative purpose, shot type, shot size, angle, lens, lens reason, camera support, camera motion, focus, composition, subject action, structured blocking, scene layers, continuity locks, audio fields, transitions, and model notes.
- For client-facing storyboard/PPT work, every shot also needs seconds, camera position, emotional function, props/characters, asset source, vertical composition consideration, and reference motion or reference video for hero/expression-critical moments.
- The downstream professional storyboard/motion page must have one cell per approved shot and include shot image region, detailed frame description, shot size, focal length, camera position, camera movement, subject blocking, sound, transition, and model risk.
- That cell is an index/representative, not a limit of one action drawing per shot. Detailed/full preproduction adds a `storyboard-coverage` sidecar with ordered action panels and declared reverse/eyeline pairs. A hard cut changes shot ID; successive action phases may share it. See `skills/dircreative/references/storyboard-coverage.md` at that stage.
- Start with a readable narrative panel and action phase—pose, contact, object change and camera relation—then add only the short note or arrow needed to explain it. Annotated line boards can serve human review and a specifically supported storyboard/motion-reference route, never a literal clean-frame slot.
- Keep an actual representative image for every approved shot. A review-approved storyboard panel may supply it only when it genuinely represents that shot and its panel-to-asset lineage is recorded; video-only downstream use does not silently remove that requirement.
- Storyboard page writing must read like a director explaining the film: story purpose first, camera language second, material/source or confirmation point last. Do not make the page feel like a production table.
- PPT storyboard pages may show 3-6 images per page, but the image regions must stay large, non-distorted, crop-safe, and readable. Captions belong under images and must carry story, camera, and source meaning.
- The downstream professional storyboard/motion page must use the visible shot-card template. Do not approve thin cell text that lacks narrative purpose, lens/support/movement, blocking/path, continuity, sound/edit, and model risk.
- Do not let a storyboard page replace the shot list. The page visualizes the approved shot cards; it must not invent new character identity or scene geography.
- Blocking must be structured as start position, end position, path, eyeline, screen direction, and axis note.
- Separate stable world coordinates from each shot's screen projection. Name
  the camera position, viewing direction and visible background at the active
  action phase; a location image cannot lock all later crops and screen sides.
  Use `references/spatial-discussion.md` for constructible changing geography.
- Audio must be structured as dialogue, voiceover, ambience, SFX, foley, music, and silence policy.
- Camera motion must name a physical start target and end target. Do not write only `slow push`, `camera follows`, or `cinematic movement`.
- Composition must name foreground, midground, background, and the product/face/readable-text zone.
- Composition must also name the visual center, subject hierarchy, negative space, movement room, leading lines or occlusion, perspective depth, screen direction, and the narrative purpose of the chosen grammar. Do not mechanically apply rule of thirds, center framing, or symmetry.
- For every frame intended for storyboard generation, also lock viewer task and
  viewer position, dominant/secondary read, frozen action phase, action vector
  and counterforce, foreground/midground/background jobs, crop pressure,
  parallax/occlusion, exaggeration budget with one protected anchor, and one
  quiet region. These fields form the `storyboard_frame_to_jingzao_v1` handoff;
  canonical assets constrain truth but do not flatten camera direction.
- Apply those fields by `shot_class` and function. Static product, identity,
  interview, dialogue, observation, or deliberately calm frames may set action
  vector/counterforce, crop pressure, parallax, or exaggeration to
  `not_applicable` with a concrete reason. Viewer task/position, dominant read,
  depth organization, and camera motivation still remain explicit. Never invent
  motion or resistance merely to fill the contract.
- When a subject or camera moves, state which composition relationships stay locked and which change at the beat.
- Shot cards must include conditional render-look cues for lighting, optics, atmosphere, and grade. Each enabled cue needs condition, effect, intensity, preserve, and exit/continuity; unused layers must be marked none by design.
- Shot cards must give the image-prompt compiler concrete visual evidence for subject, blocking, environment, light, composition, camera, color/material, proportion, and generation intent.
- Do not invent visual facts that belong in the visual bible or reference pack. Mark unresolved wardrobe, product, text, location, or material decisions as blockers for the next stage.
- Lens choices must have a production reason, not just a focal length.
- Model notes must say whether the shot is safe as a single video generation or should be split/converted into clean frames.
- Do not approve generic phrases such as `cinematic close-up`, `warm lighting`, `hero shot`, or `worker drinks` unless the full shot card makes them production-specific.
- Across a generated storyboard sequence, reject unmotivated repetition of
  viewer position, subject/frame ratio, camera height, visual center, horizon,
  attention path, and depth pattern. Do not impose a fixed wide/medium/close
  quota; repeated grammar is valid only when motivated.
- When action changes the environment, carry the trigger, affected material,
  force direction, deformation/fracture/spray and persistent result into the
  scene state and frame handoff. Effects need a physical or established fictional
  cause. Do not add destruction to quiet beats or erase it to obtain a clean frame.
- Do not write image or video prompts.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Record shot gate status, overloaded shots, continuity risks, and `next_recommended_skill: visual-bible`.
