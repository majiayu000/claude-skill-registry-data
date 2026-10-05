---
name: fpv-tour-video-generator
description: Create one continuous scene-first FPV flythrough of a supplied architecture, interior, venue, landscape, vehicle, product space, or game environment, optionally using a supplied character as a persistent flying route guide. Use when spatial traversal, landmarks, parallax, and one-take continuity are the deliverable. Unlike generate-video (relationship 0.76), this owns the planned FPV route and continuous spatial handoff; unlike animate-image (0.48), it does not limit motion to one supplied frame. It may call generate-video for atomic route segments and combine-videos (0.36) only when connected segments are necessary. Do not use for generic drone footage, montage trailers, talking heads, or a static product ad.
---
# FPV Tour Video Generator

## Catalog

- Display name: FPV Tour Video Generator
- Categories: Video
- Status: Ready
- Route label: Continuous spatial FPV composition
- Tone: purple
- Short description: Produce one route-planned FPV flythrough with continuous spatial motion and landmark coverage.
## What this skill does

- Separates scene/world references from an optional character identity guide and locks duration, ratio, landmarks, and flight constraints.
- Designs a plausible continuous route rather than a sequence of disconnected aerial shots.
- Generates, assembles only when required, and inspects a final tour for route continuity and reference fidelity.

## How to use

Provide a supplied scene or subject image, duration, ratio, must-show landmarks, route style, difficulty, and any character or motion references. The scene defines the environment, lighting, palette, materials, and spatial layout; a character reference supplies identity only.

#### Example

```text
Create a 12-second 16:9 FPV tour through this boutique hotel lobby. Start outside the entrance, pass through the doors, skim past the central staircase, and finish looking toward the sunlit courtyard. Preserve the lobby materials and lighting; no cuts or impossible wall clipping.
```

## Workflow

1. Lock the supplied references, duration, ratio, start/end positions, must-show landmarks, route style, speed, audio preference, and forbidden moves. Ask for a scene/reference image when no traversable visual environment is available.
2. Map depth, openings, obstacles, scale, light, and route opportunities. Assign each source a role. When both character and scene are supplied, preserve character identity while the scene alone controls world appearance.
3. Write one continuous route: start, altitude curve, close passes, banks, dives, traversals, landmarks, stabilization, and end state. Do not add low-water skimming, face reveals, or unsafe gap threading unless the scene and user request support them. Continue through the supported generation route without a client-side payment confirmation.
4. For each required segment, select one current cataloged model: Kling V3 Omni for several named image roles or motion reference; Kling 3.0 for precise source-frame control; Seedance 2.5 for audiovisual/artistic work; Seedance 2.0 for routine image-led motion; MiniMax H3 only for justified large-amplitude motion. Use one `operationKey` per segment, require `executionId`, and poll to terminal state. Never trial models or resubmit an unknown receipt.
5. Prompt one continuous camera path per segment with its scene anchors, camera orientation, speed, altitude, route geometry, start/end state, and prohibited cuts/resets. Keep an optional character visible as a guide without turning it into a foreground portrait.
6. Inspect first, middle, and last frames for scene fidelity, landmark coverage, plausible route, direction/altitude continuity, character persistence when used, duration, ratio, audio, clipping, cuts, and unwanted additions. Repair only the failed segment with a new linked key.
7. If duration requires connected segments, hand accepted clips in route order to `combine-videos`; otherwise deliver the accepted shot directly. Verify joins preserve speed, lighting, direction, and spatial continuity. Do not add a client-side publication confirmation; follow the API result.


## User-facing output

- Media type: One MP4 FPV tour plus route storyboard, segment manifest, and operation receipts
- Default quantity: 1 continuous tour
- Content per video: One spatially coherent FPV traversal with requested landmarks
- Default layout: User-requested duration, ratio, route style, and audio plan
- Model policy: Kling Omni complex references; Kling 3 precise frames; Seedance 2.5 audiovisual/artistic; Seedance 2.0 routine; H3 justified large motion
- Downstream use: Human creative, spatial-fidelity, and publication review
