---
name: gsap-scroll-choreography
description: Design and implement one coherent GSAP scroll timeline for cinematic websites, pinned media, scene transitions, copy beats, and video state. Use when native reveals no longer express the page sequence clearly.
---

# GSAP Scroll Choreography

Use GSAP for coordination, not decoration.

## Read

- page context and dominant visual idea
- `integrations/gsap/README.md`
- `docs/cinematic-scroll-deck-playbook.md` when video is involved

## Timeline design

Define before code:

- page boundary
- chapter boundaries
- pinned ranges
- approved rest states
- active media
- copy source of truth
- forward and reverse behavior
- mobile adaptation
- reduced-motion state

Build one inspectable timeline per sequence. Do not scatter unrelated ScrollTriggers across every element.

## Rules

- content is readable before it leaves
- copy motion follows composition
- one property owner per state
- use labels for meaningful beats
- video seeks at a bounded cadence
- transitions receive enough distance to read
- reverse travel restores state
- pinning does not trap the page
- mobile does not inherit desktop scroll distances blindly
- reduced motion keeps every chapter available

## Performance

- animate transforms, opacity, masks, clip paths, and deliberate material properties
- avoid layout reads and writes inside repeated callbacks
- do not leave broad `will-change`
- load media near use
- kill timelines and listeners when the surface unmounts

## Verify

Use actual page copy and actual media. Click and scroll through every state at desktop and mobile sizes. Check keyboard controls for guided experiences.

Tool syntax belongs in official GSAP documentation. This skill owns the page choreography and quality bar.
