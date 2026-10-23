---
name: remotion-web-assets
description: Create deterministic Remotion compositions that render hero loops, title sequences, diagrams, posters, transitions, and aspect-ratio variants for websites.
---

# Remotion Web Assets

Remotion is a build-time production tool. The website normally consumes rendered outputs.

## Read

- `integrations/remotion/README.md`
- `creative-production/pipelines/remotion.md`
- the completed asset brief

## Use when

- code or data drives the visual
- multiple aspect ratios share one composition
- outputs must be regenerated reliably
- website and campaign assets should stay aligned
- motion graphics need exact timing

## Project contract

Keep the render project isolated. Define typed props for:

- copy
- palette
- media
- duration
- frame rate
- aspect ratio
- safe area
- variant

Do not invent product claims or metrics in a demonstration render.

## Outputs

Render:

- desktop master
- mobile master
- poster
- reduced-motion still
- optional transition or sequence outputs
- manifest with composition version

Encode delivery files with the video pipeline. Verify the loop seam and actual page composition.

## License

Check Remotion's current company-size and commercial license before adoption.

Use the installed Remotion plugin skills when building or rendering a Remotion project. This repository skill owns the website asset contract.
