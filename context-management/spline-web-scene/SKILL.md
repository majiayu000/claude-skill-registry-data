---
name: spline-web-scene
description: Author, optimize, embed, and verify a Spline scene for a cinematic scroll website with clear focal points, mobile behavior, poster fallbacks, and plan-aware export rules.
---

# Spline Web Scene

Use Spline when visual 3D authoring is more valuable than custom renderer control.

## Read

- `integrations/spline/README.md`
- `templates/spline-scroll-landing/`
- project context and page composition

## Author

- one visual focal point
- one scene progression
- simple hierarchy
- restrained lights and post-processing
- reusable materials
- limited object count
- named scene states
- intentional pointer behavior

## Integrate

- choose runtime or viewer export
- verify current plan and watermark/export rights
- load behind complete semantic content
- prevent the canvas from intercepting ordinary page scroll
- map scroll through a small shared state layer
- create poster and loading states
- provide reduced motion and mobile fallback

## Optimize

Remove invisible objects, unused states, oversized textures, unnecessary interactions, and expensive effects.

## Verify

Check:

- first useful paint
- mobile crop
- touch scroll
- GPU and memory
- focus order
- scene failure
- reduced motion
- end state at the bottom of the page

Do not use a Spline scene simply because a scene URL is available.
