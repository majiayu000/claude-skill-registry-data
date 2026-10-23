---
name: cinematic-studio
description: Route a cinematic website from product context through asset production, runtime selection, implementation, and QA. Use when the request spans design direction, generated or sourced media, 3D, video, motion, or full Awwwards-style website production.
---

# Cinematic Studio

Use this as the umbrella workflow for the repository.

## Read first

1. `PRODUCT.md`
2. `DESIGN.md`
3. the target project's product and design context
4. `creative-production/README.md`
5. `integrations/catalog.json`

## Route the work

### Direct

Use `cinematic-web-director` to determine:

- surface mode
- visitor success
- product proof
- visual world
- dominant composition
- one signature motion idea
- anti-references

### Produce

Use `creative-asset-director` when the required media does not exist.

It routes to:

- `video-asset-pipeline`
- `web-3d-asset-pipeline`
- `hyperframes-video`
- `remotion-web-assets`
- Spline or Three.js scene production

Use HyperFrames when an existing website, HTML interface, design system, or agent-authored page should become deterministic video. Install and reuse the official upstream HyperFrames skills rather than recreating its composition and CLI rules.

Use Remotion when a React-first composition is already the correct durable source. Use a literal screen recording when authored motion and reusable variants do not earn their cost.

### Build

Choose only the runtime the requirement earns:

- native CSS and `modules/motion.js`
- GSAP
- `model-viewer`
- Spline
- Three.js
- React Three Fiber
- Rive

HyperFrames and Remotion are usually build-time media producers, not website runtime dependencies.

### Verify

Use:

- `asset-provenance-audit`
- `cinematic-site-qa`
- `npm run assets`
- `npm run catalogs`
- `npm run audit`
- `npm run smoke`

## Deliverable contract

A complete result includes:

- product-specific page
- production media or a clearly labeled replaceable demonstration asset
- desktop and mobile states
- reduced motion
- source and license manifest
- optimized web outputs
- browser verification
- no credentials, private URLs, or personal records

Do not declare a cinematic page complete when only prompts or asset suggestions exist. The page needs usable outputs in hand or an honest explicit placeholder contract.
