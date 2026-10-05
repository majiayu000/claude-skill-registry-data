---
name: pov-short-film-generator
description: Create one complete immersive first-person short film from a locked subjective-camera premise, supplied references, POV-specific storyboard, atomic clips, continuity-safe assembly, and final film QC. Use when the protagonist's subjective view, visible fragments, and first-person action grammar are the final film's governing invariants. Unlike plan-film-storyboard (relationship 0.77), this owns generation and finished media; unlike generate-video (0.69), it owns a multi-clip first-person narrative rather than one shot. It may hand planned clips to generate-video and accepted results to combine-videos (0.44). Do not use for a generic GoPro shot, general storyboard, music-led edit, or third-person character showcase.
---
# POV Short Film Generator

## Catalog

- Display name: POV Short Film Generator
- Categories: Film, Video
- Status: Ready
- Featured: yes
- Route label: Subjective narrative film composition
- Tone: purple
- Short description: Produce a coherent first-person narrative short with POV-specific continuity and final-film QC.
## What this skill does

- Converts a premise into a locked first-person viewpoint contract instead of a third-person camera plan.
- Builds and generates atomic subjective actions with visual, sound, and continuity anchors.
- Assembles one finished film and verifies the viewpoint never breaks unintentionally.

## How to use

Provide the premise, intended feeling, duration, ratio, supplied references, POV identity/action constraints, visual direction, audio plan, required moments, and forbidden elements.

#### Example

```text
Create a 20-second 16:9 first-person short film of someone entering an abandoned greenhouse to rescue a trapped bird. The view is always their eyes; show only hands or partial body when needed, with rain on the glass and no third-person face reveal.
```

## Workflow

1. Lock the final film, protagonist's subjective role, premise, audience feeling, duration, ratio, first-person rules, permitted protagonist fragments, references, style, audio, required beats, and forbidden views. Reject a premise that requires unapproved identity recreation or cannot maintain subjective point of view.
2. Write a POV film specification: what “I” see, hear, touch, and do; what is visible at the frame edge; where attention moves; and which third-person shots, face reveals, or camera resets are forbidden.
3. Assign reference roles and build a timed storyboard. Every clip has one subjective action, view direction, visible fragment if any, external object, start/end state, camera/body movement, style anchor, sound evidence, continuity anchors, and acceptance. Continue to the supported generation route without a client-side payment confirmation.
4. Select one current cataloged model per clip: Kling V3 Omni for complex/motion references, Kling 3.0 for precise frame control, Seedance 2.5 for audiovisual/artistic work, Veo 3.1 for eligible source-image synchronous dialogue/SFX, Seedance 2.0 for routine motion, and H3 for justified large movement. Use one `operationKey` per clip, require `executionId`, poll terminal state, and never re-create an unknown outcome.
5. Prompt subjective action language, concrete scene/object anchors, body/camera motion, start/end state, sound behavior, and forbidden third-person framing. Avoid overloaded action and style-adjective piles.
6. Inspect every accepted clip at first, middle, and last frames for POV integrity, action, references, screen direction, camera/body motion, duration, ratio, audio, and accidental protagonist reveal. Repair only the failed clip with a linked new key.
7. Assemble accepted clips in storyboard order with `combine-videos`. Watch the completed film for continuous subjective grammar, narrative clarity, pacing, audio continuity, cut boundaries, technical integrity, and no unwanted watermark. Do not add a client-side publication confirmation; follow the API result.


## User-facing output

- Media type: One final MP4 plus POV spec, storyboard, continuity manifest, and operation receipts
- Default quantity: 1 finished POV short
- Content per video: A multi-clip first-person narrative with one continuous subjective contract
- Default layout: User-requested duration, ratio, visual direction, and audio plan
- Model policy: Kling Omni complex references; Kling 3 precise frames; Seedance 2.5 audiovisual/artistic; Veo eligible synchronous audio; Seedance 2.0 routine; H3 justified large motion
- Downstream use: Human creative, continuity, safety, and publication review
