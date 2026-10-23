---
name: hyperframes-video
description: Turn websites, product interfaces, and design-system outputs into deterministic HTML-native videos with HyperFrames, its official skills, and the AIgent production contract.
---

# HyperFrames Video

HyperFrames is the preferred open-source route when a website, interface, data story, or design-system surface should become a product tour, launch film, README walkthrough, social ad, or reusable motion-graphics package.

AIgent owns the product, design, asset, rights, and delivery contract. The upstream HyperFrames skills own framework-specific composition syntax, media preparation, linting, inspection, preview, and rendering.

## Read first

1. `PRODUCT.md`
2. `DESIGN.md`
3. the completed asset brief
4. `integrations/hyperframes/README.md`
5. `creative-production/pipelines/hyperframes.md`
6. the upstream HyperFrames skills after installation

## Install the upstream production skills

```bash
npx skills add heygen-com/hyperframes
```

Do not copy or partially reimplement HyperFrames framework rules inside the project. Reuse the maintained upstream skills and CLI.

## Use HyperFrames when

- an existing website or Studio project should become a video;
- HTML, CSS, GSAP, Three.js, Lottie, captions, audio, and data should share one deterministic timeline;
- the same composition must produce landscape, portrait, square, poster, and short-loop variants;
- agents need plain HTML rather than a React-only video project;
- the output must be reproducible in CI or an automated content pipeline.

Use Remotion instead when the production system is already React-first, typed React components are the durable source, or its mature cloud-rendering ecosystem is the deciding requirement.

Use a direct screen recording when the job is only to document a literal interaction and authored motion, reusable variants, captions, or brand translation add no value.

## Production loop

```text
CAPTURE → DESIGN → SCRIPT → STORYBOARD → TIME → BUILD → INSPECT → RENDER → DELIVER
```

### Capture

For an existing website, use the upstream `website-to-hyperframes` workflow. Record the real product state, responsive behavior, important interactions, and approved assets before inventing scenes.

### Design

Translate the project design system into frame rules. Preserve tokens, typography roles, materials, motion character, and anti-patterns, but recompose them for a fixed camera and timed sequence. Use HyperFrames `frame.md` guidance when appropriate.

### Script and storyboard

Define the narrative beats before animation. Each beat records:

- viewer takeaway;
- duration and spoken copy;
- hero frame;
- camera and depth;
- entrance and transition;
- media and sound;
- desktop, portrait, and square implications.

### Build

Start with static hero-frame layout, then add seekable animation. Keep composition timing deterministic. Follow the official HyperFrames contracts for `data-composition-id`, tracks, media, registered timelines, finite repeats, and scene transitions.

### Inspect

```bash
npx hyperframes lint
npx hyperframes inspect
npx hyperframes preview
```

Fix clipping, overflow, track conflicts, unreadable captions, and layout failures before rendering.

### Render

```bash
npx hyperframes render --quality high --output final.mp4
```

Render only the variants the delivery actually needs.

## Required outputs

- landscape master when relevant;
- portrait and square variants when requested;
- poster or thumbnail;
- reduced-motion or static fallback for the website;
- optional short animated README derivative;
- transcript and captions when narration exists;
- asset manifest with source rights and HyperFrames version;
- actual-page verification when the rendered media returns to a website.

## Guardrails

- No fabricated product claims, metrics, testimonials, or interface states.
- No private or authenticated website capture without explicit authority.
- No wall-clock or random animation that breaks deterministic seeking.
- No browser runtime dependency merely because HyperFrames produced the asset.
- No public delivery without rights, attribution, poster, mobile, and failure-state decisions.
- Do not declare completion from prompts or a storyboard; provide rendered outputs or an explicit placeholder contract.
