---
name: hallmark
description: "Use when designing, building, redesigning, or auditing websites and web pages that refuse to look AI-generated. Enforces anti-AI-slop design rules, non-waivable floor constraints, tokenized design systems, 48 curated themes/materials, and automated sloplint verification."
domain: content
author: Nutlope
license: MIT
subdomain: design
tags:
  - design
  - anti-slop
  - ui
  - frontend
  - css
  - themes
  - web-design
version: 2.0.0
category: content
triggers:
- "hallmark"
- "anti-ai-slop"
- "anti slop"
- "design a website"
- "redesign page"
- "sloplint"
- "material theme"
- "revamp page"
- "restyle website"
- "visual overhaul"
---
# Hallmark — Anti-AI-Slop Web Design Engine

Hallmark is an anti-AI-slop design system created by Nutlope and Together AI for Claude Code, Cursor, Codex, and autonomous web engineering agents. It enforces a strict, non-waivable floor against machine-generated defaults, provides a catalog of forty-eight material themes across four genres, aligns layout anatomy to user jobs, and validates rendered output through automated sloplint verification and fresh-context reviews.

## Overview

AI-generated web interfaces suffer from recognizable algorithmic tropes: purple-to-blue linear gradients, tracked-capital labels, eyebrows stacked above headings, three identical feature cards, cards nested inside cards, middle-dot punctuation (`A · B · C`), arrows glued to button copy (`Get Started →`), unearned floating blur orbs, and fabricated metrics.

Hallmark halts these defaults. It treats design as material selection rather than decorative templating:
- **The Floor**: Non-waivable baseline rules governing color tokens, typography scales, accessibility, viewport boundaries, and layout integrity.
- **Job-Driven Anatomy**: Pages built around their primary functional purpose (a booking page books, a SaaS console operates, a publication reads).
- **Material Themes**: 48 distinct palettes, typography hierarchies, and surface textures categorized into Modern Minimal, Editorial, Atmospheric, and Playful genres.
- **Multi-Width Viewport Discipline**: Specific constraints across 320px, 375px, 1280px, 1440px, and 1920px viewports with an 80-word visual budget per screen.
- **Sloplint & Verification**: Static and rendered linting catching visual clichés, coupled with cold-context subagent reviews.


## Companion Design Framework: Impeccable

For full-lifecycle design operating system 24-verb command vocabulary (`shape`, `init`, `critique`, `audit`, `polish`, dual-truth (`PRODUCT.md` `DESIGN.md` `impeccable`). UX 392:| `interface-review` Change-scoped PR, [SKILL.md](../interface-review/SKILL.md)
## When to Use

- Building new websites, landing pages, marketing surfaces, product dashboards, documentation portals, or web applications from scratch.
- Executing redesigns of existing pages via `/hallmark redesign <path>` while preserving existing DOM wiring and content contracts.
- Auditing UI surfaces for machine-generated design tells using `/hallmark audit <path>`.
- Enforcing strict tokenized CSS design systems with zero hardcoded color or font literals outside `:root`.
- Preventing visual convergence and boilerplate monotony across multiple agent-generated frontend codebases.

## When NOT to Use

- Pure backend APIs, database migrations, microservices, or headless command-line tools with no visual presentation layer.
- Non-visual performance optimizations, database indexing, or infrastructure automation scripts.
- Existing frontend projects with an established, client-mandated corporate design system, unless the user explicitly requests an anti-slop audit or redesign.
- Native mobile applications (iOS UIKit/SwiftUI or Android Compose) that follow platform-specific HIG or Material 3 specifications without HTML/CSS.

## Non-Waivable Floor Rules (The Floor)

Every output generated under Hallmark must satisfy these sixteen non-waivable floor requirements:

1. **Tokenized Primitives**: Every color and font must pass through CSS custom properties declared at `:root` or inside declared theme blocks. Zero raw hex values, rgb strings, oklch literals, or font-family names outside the token declaration block.
2. **Animation Discipline**: Never use `transition: all`. Never animate layout-triggering properties (`width`, `height`, `top`, `left`, `margin`, `padding`). Animate only `transform` and `opacity`.
3. **Typography Purity**: Never set a single italic word inside an otherwise roman heading. Never combine conflicting display weights inside a single lockup.
4. **Horizontal Containment**: Declare `overflow-x: clip` on both `html` and `body`. Never use `overflow-x: hidden` as a patch for uncontained elements, and never use `100vw` container widths.
5. **Grid Track Defense**: Every image-bearing grid track must use `minmax(0, 1fr)`. All display headings must carry `overflow-wrap: break-word; min-width: 0`.
6. **Focus Visibility**: Every interactive control must provide an instant, high-contrast `:focus-visible` state with at least 3:1 contrast against adjacent backgrounds.
7. **Motion Accessibility**: Every keyframe animation and transform transition must provide a `@media (prefers-reduced-motion: reduce)` override. Content must remain visible and legible with JavaScript disabled.
8. **Honest Material**: Never fabricate metrics, user testimonials, partner logo walls, customer counts, or case study statistics. Use real project data, client-provided assets, or empty text slots.
9. **No Eyebrows & No Tracked Caps**: Banned: small uppercase labels stacked above main headings, category tags over cards, or tracked-out small caps (`0.05em+`). Labels must use the body typeface in sentence case or lowercase.
10. **Template Punctuation Ban**: Banned: middle-dot separators (`Product · Features · Pricing`), arrows glued to link labels (`Sign Up →`), and decorative status dots before text. Use structural spacing, columns, or hairline borders instead.
11. **Banned Color Slop**: Absolute ban on purple-to-blue, violet-to-cyan, or rainbow gradients. Absolute ban on cards placed inside cards, emojis used as UI icons, and drawn fake OS or browser chrome.
12. **Hero Viewport Fitting**: Headline, one-sentence explanatory lede, and primary call-to-action button must fit completely inside a 1280x800 viewport without scrolling.
13. **80-Word Screen Budget**: No more than 80 words within any 900px vertical window at 1440px viewport. The hero text consists strictly of a headline, one explanatory sentence, and action buttons.
14. **Centered Max-Width Container**: At 1920px viewport, page containers must be capped (between 1360px and 1520px) and centered. Side gutters must expand; grids must not stretch infinitely.
15. **Mandatory CSS Stamp**: Line 1 of the generated CSS stylesheet must be the Hallmark build stamp recording design decisions, critique scores, theme identity, and any justified waivers.
16. **Sloplint Verification**: Run automated static and rendered sloplint verification before delivery. Zero `FAIL` findings on Floor rules; all `REFLEX` findings resolved or formally waived.

## Workflow

```
[0. Pre-Flight] -> [1. Material Ask] -> [2. Shape Anatomy] -> [3. Theme Direction]
       |
       v
[4. The Picks Block] -> [5. Hero Build] -> [6. Page Assembly] -> [7. Sweep & Review]
```

### Step 0: Pre-Flight Audit
Inspect the existing project environment before asking questions:
- Detect existing design tokens, typography styles, utility frameworks (Tailwind, PostCSS, CSS Modules), and framework targets (Next.js, Vite, Astro, static HTML).
- Check for `.hallmark/log.json` to inspect fingerprints of previously generated builds and ensure structural divergence.

### Step 1: Material & Context Ingestion
Collect verified, concrete material from the user or repository:
- Real product screenshots, authentic photography, verified domain data, customer metrics, target audience context, and functional requirements.
- Never invent placeholder numbers, mock logos, or imaginary case studies.

### Step 2: Shape & Job-Driven Anatomy
Commit to a surface anatomy governed by the page's functional job:
- **Monitor / Telemetry**: High-density tables, glanceable status indicators, zero hero marketing pitch.
- **Operate / Console**: Clean tables, action bars, clear selection states, zero decorative fluff.
- **Compare / Pricing**: Aligned columns, structural parity, distinct highlighted differentiator.
- **Decide / Landing**: High-contrast single idea per section, clear hero above the fold, strong terminal action.
- **Explore / Catalog**: Dense result grid, faceted filtering, fast hover inspection.

### Step 3: Material & Theme Direction
Select one theme from the 48 curated materials or create a bespoke direction under the four core genres:
- **Modern Minimal**: Clean geometry, high-legibility sans-serif, monochrome paper tinted by 0.005 chroma, sharp hairline borders (e.g. Cobalt, Terminal, Console, Blueprint).
- **Editorial**: High-contrast serifs, warm tinted paper ground, typographic hierarchy, generous leading, generous whitespace (e.g. Atelier, Almanac, Broadside, Newsprint).
- **Atmospheric**: Immersive dark surfaces, controlled radial blooms, deep contrast, luminous typography (e.g. Dusk, Midnight, Darkroom, Solstice).
- **Playful**: Vibrant character accents, bold display type, expressive rhythm, tactile borders (e.g. Carnival, Sticker, Spore, Hum).

### Step 4: The Picks Block
Declare design decisions in a compact metadata block:
```
Picks:
- Material: Cobalt (Dark slate ground, high-contrast crisp white ink, cyan-950 borders)
- Anatomy: Decide / Landing (Hero -> Feature Split -> Live Code Bench -> Action)
- Display Font: Instrument Serif 56px / 1.08
- Body Font: Inter 16px / 1.55
- Primary Action: Solid cyan-400 fill, dark slate ink, 44px height
```

### Step 5: Hero Construction First
Build and verify the hero section independently before creating lower sections:
- Headline clamped between 44px and 72px.
- Single-sentence lede with max-width between 45ch and 65ch.
- Primary and optional secondary action buttons with explicit height (44px-52px) and instant `:focus-visible`.
- Ensure headline, lede, action buttons, and visual anchor fit entirely above the fold at 1280x800.

### Step 6: Body & Section Rhythm
Assemble the remainder of the page adhering to the surface ladder:
- Vary transitions between sections: alternating between generous whitespace (120px+), hairline borders, and subtle paper tint shifts.
- Keep total copy under the 80-word budget per 900px window.
- Replace drawn placeholder illustrations with authentic product screenshots or credited photography.

### Step 7: Sweep, Sloplint & Fresh-Context Review
- Run static and headless browser sloplint checks against all viewports (320px, 375px, 768px, 1280px, 1440px, 1920px).
- Verify zero `FAIL` statuses. Resolve any `REFLEX` warnings or document explicit waivers in the CSS stamp.
- Inspect rendered DOM to verify touch targets (min 44x44px), contrast ratios (>= 4.5:1 text, >= 3:1 controls), and layout stability.

## Redesign and Audit Modes

### Redesign (`/hallmark redesign <path>`)
Redesigns existing web pages while preserving functional contracts:
1. Records every existing interactive element, anchor link, input name, form handler, and heading before making modifications.
2. Applies Hallmark tokens, typography hierarchy, and floor constraints to the markup.
3. Verifies that zero functional elements or API bindings were dropped during redesign.

### Audit (`/hallmark audit <path>`)
Generates a structured quality report evaluating the target interface against Floor, Reflex, and Finish gates without altering source code.

## Anti-Rationalization

| AI Corner-Cutting Excuse | Hallmark Enforcement Truth | Corrective Action |
|---|---|---|
| "A purple-to-blue gradient makes the hero button look modern and attractive." | Violates Floor Gate 2a. Multi-color gradients are the primary hallmark of cheap AI-generated templates. | Use solid brand fills, high-contrast ink, or subtle translucent dark glass with crisp 1px borders. |
| "Eyebrows like 'NEXT-GEN AI PLATFORM' help users understand the section." | Violates Floor Gate 54. Eyebrows are decorative clutter that dilute heading impact and waste reading attention. | Delete the eyebrow. Integrate the actual value proposition directly into the primary heading in sentence case. |
| "Nesting cards inside a container card makes the layout look neat and structured." | Violates Floor Gate 4. Card-in-card nesting creates visual claustrophobia and layout clutter. | Use a single containment layer with subtle hairline borders, typography scale, or column whitespace. |
| "I'll put placeholder metrics ('99.9% Uptime, 10M+ Users') to make it feel credible." | Violates Floor Gate 46a. Fabricated metrics and fake testimonials destroy user trust and fail production honesty. | Use verified client figures, real repository metrics, or omit the stat section completely. |
| "Using transition: all ease-in-out is convenient and smooth." | Violates Floor Gate 10a. Transitioning all properties causes repaint lag and jank during layout shifts. | List explicit animating properties: `transition: transform 150ms ease, opacity 150ms ease`. |
| "Setting max-width: 100vw prevents horizontal scrollbars." | Violates Floor Gate 34. `100vw` includes the scrollbar gutter width on desktop browsers, forcing horizontal scroll. | Declare `overflow-x: clip` on `html` and `body`, and use `width: 100%` on containers. |
| "I can skip sloplint because Chrome or Puppeteer is not installed in the container." | Static Floor rules (markup, CSS, tokens) still execute statically without a browser engine. | Run `node scripts/sloplint.mjs` in static mode to audit code rules, contrast tokens, and syntax invariants. |

## Code Examples

### 1. Installation & Sloplint CLI Execution

Install Hallmark into your agent harness using `npx skills add nutlope/hallmark -g` or install the browser runner with `npm install -g puppeteer-core`.

```bash
npx skills add nutlope/hallmark -g
npm install -g puppeteer-core

node skills/hallmark/scripts/sloplint.mjs ./src/app --render
node skills/hallmark/scripts/sloplint.mjs ./index.html --genre modern-minimal
```

### 2. Tokenized CSS Foundation with Hallmark Stamp

```css
/* Hallmark · theme: cobalt · genre: modern-minimal · posture: settled · pre-emit: P5 H5 E5 S4 R5 V4 · weakest: S · real metrics wired */

:root {
  --color-paper: oklch(0.14 0.02 240);
  --color-surface: oklch(0.18 0.02 240);
  --color-surface-subtle: oklch(0.22 0.025 240);
  --color-border: oklch(0.28 0.03 240);
  --color-ink: oklch(0.96 0.005 240);
  --color-ink-muted: oklch(0.72 0.015 240);
  --color-accent: oklch(0.75 0.16 205);
  --color-accent-ink: oklch(0.12 0.03 240);
  --font-display: "Space Grotesk", system-ui, sans-serif;
  --font-body: "Inter", system-ui, sans-serif;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 16px;
  --space-4: 24px;
  --space-5: 48px;
  --space-6: 80px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
}

html, body {
  margin: 0;
  padding: 0;
  background-color: var(--color-paper);
  color: var(--color-ink);
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.55;
  overflow-x: clip;
}

.hero-container {
  max-width: 1440px;
  margin: 0 auto;
  padding: var(--space-5) var(--space-4);
  box-sizing: border-box;
}

.hero-title {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 5vw, 4rem);
  line-height: 1.08;
  letter-spacing: -0.02em;
  margin: 0 0 var(--space-3) 0;
  overflow-wrap: break-word;
  min-width: 0;
}

.hero-lede {
  font-size: 1.125rem;
  color: var(--color-ink-muted);
  max-width: 60ch;
  margin: 0 0 var(--space-4) 0;
}

.action-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 0 var(--space-4);
  background-color: var(--color-accent);
  color: var(--color-accent-ink);
  font-weight: 600;
  border-radius: var(--radius-md);
  text-decoration: none;
  border: 1px solid transparent;
  transition: transform 120ms ease, opacity 120ms ease;
}

.action-button:hover {
  opacity: 0.92;
}

.action-button:active {
  transform: scale(0.98);
}

.action-button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 3px;
}

@media (prefers-reduced-motion: reduce) {
  .action-button {
    transition: none;
  }
}
```

### 3. Production Component Implementation (TypeScript / React)

```typescript
import React, { FC } from 'react';

interface HeroProps {
  headline: string;
  lede: string;
  primaryActionLabel: string;
  primaryActionHref: string;
  metricLabel?: string;
  metricValue?: string;
}

export const HeroSection: FC<HeroProps> = ({
  headline,
  lede,
  primaryActionLabel,
  primaryActionHref,
  metricLabel,
  metricValue,
}) => {
  return (
    <header className="hero-container">
      <h1 className="hero-title">{headline}</h1>
      <p className="hero-lede">{lede}</p>
      <div className="action-row">
        <a href={primaryActionHref} className="action-button">
          {primaryActionLabel}
        </a>
        {metricLabel && metricValue && (
          <div className="metric-badge">
            <span className="metric-number">{metricValue}</span>
            <span className="metric-desc">{metricLabel}</span>
          </div>
        )}
      </div>
    </header>
  );
};
```

### 4. Automated Python Validation Harness

```python
import sys
import re
from pathlib import Path

def audit_hallmark_compliance(css_file: Path) -> dict:
    content = css_file.read_text(encoding="utf-8")
    violations = []
    
    if not content.lstrip().startswith("/* Hallmark"):
        violations.append("Missing Hallmark stamp on line 1 of CSS")
    
    if "transition: all" in content or "transition:all" in content:
        violations.append("Banned transition: all detected")
        
    banned_gradients = [
        "from-purple", "to-cyan", "from-violet", "to-blue",
        "linear-gradient(to right, purple", "linear-gradient(90deg, #8b5cf6"
    ]
    for bg in banned_gradients:
        if bg in content.lower():
            violations.append(f"Banned gradient pattern found: {bg}")
            
    if "overflow-x: hidden" in content:
        violations.append("Use overflow-x: clip instead of overflow-x: hidden")
        
    return {
        "file": str(css_file),
        "violations": violations,
        "clean": len(violations) == 0
    }

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("style.css")
    if target.exists():
        result = audit_hallmark_compliance(target)
        if not result["clean"]:
            print(f"FAILED: {len(result['violations'])} violations found")
            for v in result['violations']:
                print(f" - {v}")
            sys.exit(1)
        print("PASSED: Hallmark CSS floor constraints verified clean")
        sys.exit(0)
```

## Verification Checklist

- [ ] **Tokenization**: Every color, font-family, and spacing value is declared as a CSS variable at `:root`. Zero raw hex or literal values in rules.
- [ ] **No Banned Gradients**: Zero purple-to-cyan, violet-to-blue, or rainbow linear/mesh gradients on buttons, text, or backgrounds.
- [ ] **No Eyebrow Clutter**: Zero small uppercase tags or tracked labels placed above primary headings.
- [ ] **No Nested Cards**: Container surfaces maintain a single hierarchy level without cards inside cards.
- [ ] **No Template Punctuation**: Zero middle dots (`·`) joining navigation items, zero glued arrows (`→`), and zero decorative status dots.
- [ ] **Hero Fold Visibility**: Headline, single-sentence lede, and primary CTA button fit completely within 1280x800 viewport without scrolling.
- [ ] **80-Word Window Budget**: Total copy does not exceed 80 words in any 900px vertical window at 1440px viewport.
- [ ] **Horizontal Containment**: Both `html` and `body` declare `overflow-x: clip`. Zero horizontal scrolling at 320px, 375px, 768px, 1280px, 1440px, or 1920px.
- [ ] **Instant Focus Rings**: Every interactive element defines a distinct `:focus-visible` outline with >= 3:1 contrast against its background.
- [ ] **Motion Overrides**: All transitions and animations declare `@media (prefers-reduced-motion: reduce)` fallbacks.
- [ ] **CSS Hallmark Stamp**: First line of stylesheet contains the Hallmark stamp with theme, posture, critique scores, and resolved waivers.
- [ ] **Sloplint Sweep Clean**: Static and rendered sloplint pass with zero open `FAIL` or `REFLEX` findings.

## Sub-Skills & Specialized Playbooks

| Sub-Skill | Trigger / Kasus Penggunaan | Berkas Referensi |
| :--- | :--- | :--- |
| `anti-slop-frontend` | Applying distinctive layout, typography, motion, and spacing constraints against generic AI interfaces | [SKILL.md](../anti-slop-frontend/SKILL.md) |
| `better-interface` | Cross-discipline review across accessibility, layout, writing, typography, color, and UI polish | [SKILL.md](../better-interface/SKILL.md) |
| `interface-review` | Change-scoped review of a branch, PR, or uncommitted work | [SKILL.md](../interface-review/SKILL.md) |

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We'll add the verification evidence later" | Claims without evidence are opinions. Every hallmark must ship with reproducible proof (output, screenshot, test). |
| "The code looks right" | Visual review misses regressions. Run the checklist and paste the terminal output. |
| "It passed once, we're done" | Hallmarks must hold on the current head. Re-run on the latest commit before publishing. |
| "Skipping the checklist saves time" | The checklist is the deliverable, not overhead. Skipping it ships unverifiable claims. |
| "Edge cases are out of scope" | Hallmarks without edge cases are demos. Cover the boundaries or mark the limits explicitly. |

