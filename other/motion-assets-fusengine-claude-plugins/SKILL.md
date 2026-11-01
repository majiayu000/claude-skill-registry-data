---
name: motion-assets
description: "Use when a film needs product visuals — capturing real screenshots at a fixed DPR, the real OS pointer, masking sensitive data with labeled example data, avoiding third-party brand look-alikes, and recording provenance in .motion/assets.json."
versions:
  fuse-motion: "1.0.0"
user-invocable: false
references: references/real-screenshots.md, references/pointer-and-brands.md, references/data-masking.md, references/provenance.md, references/templates/assets-json.md
related-skills: motion-method, motion-craft, motion-render, motion-review, fuse-ai-pilot:fuse-browser-usage
---

<objective>
Stage 3 of the `motion-method` pipeline: every product visual in a film is a real capture of the real product, taken at a fixed device pixel ratio, with sensitive data masked before capture and an "Example data" label wherever placeholder data replaces real values. Each asset is recorded in `.motion/assets.json` with its source URL, capture settings, masking applied, and sha256, so the critic's truth-safety criterion can be checked against a file rather than a promise.

It does not draw UI. A screen the product does not have is "invented UI" — a hard-fail in `motion-review`.
</objective>

# Motion Assets

## Agent Workflow (MANDATORY)

| Step | Who / Tool | What |
|------|-----------|------|
| Before capturing | read `fuse-ai-pilot:fuse-browser-usage` | Tool routing and batching rules for `mcp__fuse-browser__*` |
| Capture N screens | `browser_shots_batch` (one call, N URLs) | Real screenshots — never a per-URL loop |
| DPR must be pinned | CDP `Emulation.setDeviceMetricsOverride` (`deviceScaleFactor`) | Same approach as `docs/demo/statusline-mod/motion-capture.js` |
| After capture | write `.motion/assets.json`, run the check script | Provenance + hash |
| Draft review | `motion-critic` via `motion-review` | Truth-safety criterion uses `assets.json` |

---

## Overview

| Concern | Rule | Reference |
|---------|------|-----------|
| **Real screenshots** | Captured from the running product, fixed DPR, fixed viewport | [real-screenshots.md](references/real-screenshots.md) |
| **Pointer & brands** | Real OS pointer (hotspot, scaled with camera); no third-party brand look-alikes | [pointer-and-brands.md](references/pointer-and-brands.md) |
| **Masking** | Replace sensitive values before capture; label "Example data" | [data-masking.md](references/data-masking.md) |
| **Provenance** | Every asset in `.motion/assets.json` with source, settings, masking, sha256 | [provenance.md](references/provenance.md) |

---

## Critical Rules

1. **Real screenshots only** — no redrawn, mocked, or generated UI standing in for the product.
2. **Fixed DPR and viewport per film** — mixed DPRs give mismatched sharpness between beats.
3. **Mask before capture, not after** — replace values in the page; blur and pixelation are not masking.
4. **Label placeholder data "Example data"** — on screen, wherever real values were replaced.
5. **Sensitive-data list comes from the brief** — plus the user-level banned list; never write literal sensitive values into the repo.
6. **No asset without a provenance entry** — an unlisted file in the scene is treated as invented.
7. **Never client names, never real spend amounts** — in assets, labels, filenames, or examples.
8. **Real OS pointer, never a drawn arrow** — hotspot respected, scaled with the camera, recorded as `kind: pointer`.
9. **No third-party brand look-alikes** — another company's signature color, logo, or app chrome is a trademark risk; use the owner's brand or neutral placeholders.

---

## Architecture

```
<project>/.motion/
├── brief.md            # sensitive-data list (categories)
├── assets/
│   ├── raw/            # NOT committed — pre-mask captures, if any were needed
│   └── <name>@<dpr>x.png  # masked, labeled captures used by the scene
└── assets.json         # provenance (template: assets-json.md)
```

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Real screenshots** | [real-screenshots.md](references/real-screenshots.md) | Capturing product screens; DPR, viewport, state setup |
| **Pointer & brands** | [pointer-and-brands.md](references/pointer-and-brands.md) | A beat shows a cursor; anything borrowed from another company |
| **Data masking** | [data-masking.md](references/data-masking.md) | Anything from the sensitive-data list could appear |
| **Provenance** | [provenance.md](references/provenance.md) | Recording and checking where each asset came from |

### Templates

| Template | When to Use |
|----------|-------------|
| [assets-json.md](references/templates/assets-json.md) | Writing `.motion/assets.json` and its check script |

---

## Best Practices

### DO
- Seed the product with neutral example data before capturing — it removes most masking work.
- Capture all screens of one film in one batch, same DPR, same theme.
- Crop/zoom real captures for legibility instead of redrawing them.
- Re-hash and re-check after any edit to an asset.

### DON'T
- Recreate a screen in HTML because capture was inconvenient.
- Blur a customer name and call it masked.
- Commit pre-mask captures.
- Reuse an asset from another film without its own provenance entry.
- Keep a template's borrowed accent hex or "default logo" from another brand.
