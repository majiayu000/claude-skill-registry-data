---
name: creative-suite
description: Creative content generation — ASCII art/video, architecture diagrams, infographics, comic strips, pixel art,
  p5.js sketches, design systems, image/video generation (ComfyUI, TouchDesigner), and music/songwriting. Covers 14+ creative
  tools and styles.
version: 1.0.0
author: Hermes Agent (curator consolidation)
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - creative
    - ascii
    - diagram
    - infographic
    - comic
    - pixel-art
    - p5js
    - design
    - comfyui
    - music
lane: worker-vision
reasoning_effort: xhigh
---
# Creative Suite

Covers: ASCII art/video, architecture diagrams, infographics, comics, pixel art, p5.js, design systems, ComfyUI, TouchDesigner, music generation, and more.

## ASCII Art & Video
```bash

set -euo pipefail
# pyfiglet
figlet -f slant "Hello"

# cowsay
cowsay "Moo"

# ASCII video
ascii-video input.mp4 output.gif
```

## Architecture Diagrams (Dark SVG)
```bash

set -euo pipefail
# Generate dark-themed SVG/HTML architecture diagrams
# See references/architecture-diagram.md
```

## Infographics (Baoyu)
```bash

set -euo pipefail
# 21 layouts × 21 styles
# See references/baoyu-infographic.md
```

## Comics (Baoyu)
```bash

set -euo pipefail
# Knowledge comics: educational, biography, tutorial
# See references/baoyu-comic.md
```

## Pixel Art
```bash

set -euo pipefail
# Era palettes: NES, Game Boy, PICO-8
# See references/pixel-art.md
```

## p5.js Sketches
```bash

set -euo pipefail
# Generative art, shaders, interactive 3D
# See references/p5js.md
```

## Design Systems (Popular Web Designs)
```bash

set -euo pipefail
# 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS
# See references/popular-web-designs.md
```

## Excalidraw (Hand-Drawn Diagrams)
```bash

set -euo pipefail
# JSON-based hand-drawn diagrams: arch, flow, seq
# See references/excalidraw.md
```

## Image/Video Generation (ComfyUI)
```bash

set -euo pipefail
# ComfyUI workflow for images, video, audio
# See references/comfyui.md
```

## TouchDesigner MCP
```bash

set -euo pipefail
# Control TouchDesigner via MCP
# See references/touchdesigner-mcp.md
```

## Music & Songwriting
```bash

set -euo pipefail
# Suno AI prompts, HeartMuLa generation
# See references/songwriting.md
```

> **Pro-tip (2026-07-04):** Wenn der User "im Stil von X" sagt und du Zugriff auf X's echtes Material hast (Soundtrack-Album, eigene Library), nutze `references/style-derivation-from-reference-tracks.md` — misst echte Tracks via ffprobe und leitet daraus Suno-HeartMuLa-Style-Felder ab. Ergibt deutlich bessere Matches als reine Vibes-Schätzungen.

## Manim (Math Videos)
```bash

set -euo pipefail
# 3Blue1Brown-style math animations
# See references/manim.md
```

## Design.md (Google Design Tokens)
```bash

set -euo pipefail
# Author/validate/export DESIGN.md token spec files
# See references/design-md.md
```

## Pretext (Browser Demos)
```bash

set -euo pipefail
# Creative browser demos with @chenglou/pretext
# See references/pretext.md
```

## Humanizer
```bash

set -euo pipefail
# Strip AI-isms and add real voice
# See references/humanizer.md
```

## Sketch (HTML Mockups)
```bash

set -euo pipefail
# 2-3 design variants to compare
# See references/sketch.md
```

## UI-Factory (Atoms → Molecules → Organisms)

KIMI K2 UI-Factory-Pattern (2026-06-30) — komponierbare Skills für UI-Generierung.

**Atoms (Skills) — die 4 ui-* Skills:**

| Skill | Was | Reihenfolge |
|-------|-----|-------------|
| `ui-color-system` | Accessible Color-Paletten + WCAG-Checks | **1 — first** |
| `ui-design-system` | Token-Generation (JSON + CSS + TS) | 2 |
| `ui-component-library` | Button/Input/Card/Modal/Nav mit A11y | 3 |
| `ui-dashboard` | KPI-Grid + Charts + Tables + Filters | 4 — last |

**Molecules (Agents/SOUL.md):** ui-builder, ui-designer, ui-a11y, ui-responsive, ui-qa — bündeln mehrere Atoms mit fokussierter Persona.

**Organisms (Loops):** Cron/Webhook-Automation — nightly a11y-scan, design-system-drift-detection, PR-review.

**Showcase:** `~/yuno-cockpit/index.html` ist ein live gebautes Yuno-Cockpit-Dashboard, das die 4 Skills als Beispiel einsetzt (Yuno-Purple/Pink-Theme via ui-color-system-Pattern, KPI-Cards via ui-dashboard-Pattern).

**Wann nutzen:**
- User fragt nach "design system", "UI kit", "component library", "dashboard", "monitoring"
- Kette: `ui-color-system` → `ui-design-system` → `ui-component-library` → `ui-dashboard`
- Tokens fließen von oben nach unten, jede Skill baut auf der vorherigen auf

**Pitfall:** Nicht von oben anfangen — ohne Color-System keine Design-Tokens, ohne Tokens keine Component-Library, ohne Library kein Dashboard.

## Claude Design
```bash

set -euo pipefail
# One-off HTML artifacts (landing, deck, prototype)
# See references/claude-design.md
```

## Avatar / Icon Generation (ImageMagick)

```bash

set -euo pipefail
# Generate circular user icons from screenshots/photos
# 3 styles: Google (gradient ring), Dark/Neon, Minimal (monochrome)
# Supports batch generation + montage preview
# See references/icon-generation.md
```

## 🧭 Related Skills (Cross-Cluster Navigation)

- **`skill-navigator`** (orchestration/) — Meta-Navigator for all 169 active Hermes skills. **Load FIRST when unsure which skill applies.** Maps 10 domain-clusters and 60+ singletons. Useful for picking the right creative sub-skill (e.g. ui-design-system vs claude-design vs popular-web-designs).
- **`multi-agent-pitfalls-cheatsheet`** (orchestration/) — TRIGGER-WATCHLIST for `delegate_task` calls. Load BEFORE spawning subagents for creative audits (e.g. parallel review of multiple UI components).
- **`multi-agent-orchestration`** (orchestration/) — The 3-Expert Research PATTERN. Useful for design-variant comparisons (3 parallel designers → synthesis → pick winner).
