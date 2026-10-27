---
name: postrboard-design
description: Apply the Postrboard design language — a refined, airy, code-native aesthetic used across postrboard.com and burkeholland.github.io — when designing or building any website, landing page, UI component, or web app. Use this skill whenever the user asks to design, style, or build a site and wants it to feel polished, modern, and developer-native. Trigger on phrases like "build me a site", "design a landing page", "make it look like postrboard", "use my design language", "create a new site", etc.
---

# Postrboard Design Language

This skill defines the visual design language used across **postrboard.com** and the **burkeholland.github.io** family of sites. It is a **refined, airy, code-native aesthetic** — editorial restraint meets developer credibility.

Use this spec as a creative framework, not a rigid template. Every new site should feel fresh within these constraints — different font pairings, different color mode (light vs dark), different layout rhythm — but always recognizable as part of this family.

---

## Core Philosophy

**"Editorial restraint meets code-native credibility."**

- Type-led design: let typography do the heavy lifting
- Whitespace is a first-class design element
- Components earn their place — no decorative noise
- Code motifs (terminals, monospace, pills) signal technical authenticity
- Motion is ambient and gentle, never performative
- Color is precious — use the signature palette sparingly and intentionally

---

## Color System

### Signature Accent Trio

This coral → azure → sage progression is the cross-site brand signature. It appears as gradients, individual accents, or subtle ambient glows.

```
Coral:  #ff7f50   (warm, energetic, primary attention)
Azure:  #0ea5e9   (cool, trustworthy, secondary accent)
Sage:   #84cc16   (fresh, natural, tertiary or completion state)
```

### The Core Gradient

When using the trio as a gradient:
```css
linear-gradient(135deg, #ff7f50, #0ea5e9)          /* two-stop, most common */
linear-gradient(to right, #ff7f50, #0ea5e9, #84cc16) /* three-stop, signature */
```

Use gradients on:
- Hero highlighted words or wordmarks
- CTA buttons
- Logo marks or decorative periods
- Ambient background glows (heavily blurred)

Avoid gradients on: body text, large background washes (unless very subtle), navigation.

### Light Mode Palette

```
Page background:     #f0f4f8  (cool gray-blue mist) or
                     linear-gradient(to bottom right, #ffffff, #f0f9ff, #f6fff8)
Card/surface:        #ffffff  or rgba(255,255,255,0.7) for glass
Primary text:        #111827  or #0f172a
Secondary text:      #4b5563  or #475569
Tertiary/meta:       #94a3b8
Border:              #e2e8f0  or rgba(255,255,255,0.5) for glass
```

### Dark Mode Palette

```
Page background:     #0b0f14  (near-black with blue cast)
Surface/panel:       #111820
Text:                #e2e8f0
Dim text:            #64748b
Muted text:          #334155
Border:              rgba(255,255,255,0.06)
Ambient glow:        coral top-right, azure bottom-left (blurred blobs, opacity 0.15–0.25)
Grain texture:       subtle noise overlay, opacity 0.02
```

### Soft-tone Tints (for badges, chips, highlights)

```
Coral soft:   #fff0eb
Azure soft:   #e8f7fe
Sage soft:    #f2fde0
```

---

## Typography

### The Two-Font Pattern

Almost every site pairs a **humanist/geometric sans** with a **monospace face** for technical credibility. Pick one pair per project:

| Sans | Mono | Best for |
|------|------|----------|
| Inter | Space Mono | Premium AI/SaaS landing |
| DM Sans | IBM Plex Mono | CLI utility microsites |
| Outfit | JetBrains Mono | Dark terminal-native sites |
| Space Grotesk | (mono optional) | Editorial/gallery |

Never use more than two font families. The sans handles UI and body; the mono handles code, commands, and large display wordmarks.

### Typographic Scale

```
Display/wordmark:   clamp(3.5rem, 10vw, 18rem)  weight 700–800  tracking -0.06em to -0.07em
Hero H1:            56px–64px                   weight 800       tracking -1.5px to -2.5px
Section H2:         clamp(3.5rem, 6vw, 7rem)    weight 700–800   tracking tight
Card title:         24px                        weight 700
Body:               16px–17.6px                weight 400       line-height 1.7–1.85
Meta/label:         12px–14px                  weight 500–600   uppercase, tracking 0.7px
Mono command:       13px–14px                  weight 400
```

### Typographic Principles

- Negative letter-spacing on large display text is essential
- Body copy should breathe — line-height never below 1.6
- Mono text signals "this is a real tool"
- Uppercase labels are used only for meta/category, never for body
- Gradient text-fill on key words creates focal emphasis without adding UI elements

---

## Layout & Spacing

### Max Widths

```
Full editorial layout:   1200px–1400px
Article/utility layout:  880px
Compact/terminal:        680px
```

### Rhythm Vocabulary

```
Section vertical padding:  5rem–7rem (spacious gallery rhythm)
Hero padding:              7rem top, 5rem bottom
Card internal:             24px–32px
Grid gap:                  1.25rem–2rem
Container horizontal:      1.5rem–3rem padding
```

### Grid Patterns

- 3-column card grid: `repeat(auto-fit, minmax(300px, 1fr))`
- Gallery grid: `repeat(5, 1fr)` with tight 8px gaps
- Two-column hero: left editorial, right visual artifact (terminal, mockup)
- Single-column utility: centered, max-width 680–880px

---

## Surface & Depth

### Glassmorphism (Light Mode)

```css
background:      rgba(255, 255, 255, 0.7);
border:          1px solid rgba(255, 255, 255, 0.5);
border-radius:   16px;
backdrop-filter: blur(8px) saturate(1.4);
box-shadow:      0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
```

Use glass surfaces for: sticky navigation, cards over gradient backgrounds.

### Elevation Scale

```
Subtle (body cards):      0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.06)
Medium (interactive):     0 4px 8px rgba(0,0,0,0.06), 0 12px 32px rgba(0,0,0,0.10)
High (terminal/demo):     0 32px 80px rgba(0,0,0,0.22), 0 0 0 1px rgba(255,255,255,0.04)
Dark terminal:            0 24px 60px -12px rgba(0,0,0,0.45), 0 0 0 1px rgba(255,255,255,0.02)
```

Colored button shadows use the accent color:
```css
box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);  /* azure-keyed */
```

---

## Border Radius

There are three distinct corner languages — use one consistently within a surface type:

```
Pill (CTAs, filter pills, tags):  border-radius: 9999px or 100px
Soft (cards, panels, terminals):  border-radius: 16px–18px
Compact (utility, code blocks):   border-radius: 6px–12px
Sharp (gallery tiles):            border-radius: 4px–5px
```

Mix pill buttons with soft cards. Never mix sharp and pill on the same surface tier.

---

## Components

### Navigation

- Sticky, translucent
- Light: `rgba(255,255,255,0.5–0.85)` + `blur(8px–12px) saturate(1.6)`
- Dark: `rgba(11,15,20,0.8)` + `blur(12px)`
- Compact padding, minimal links
- Logo on left, single CTA on right

### Primary CTA Button

```css
background:    linear-gradient(to right, #ff7f50, #0ea5e9, #84cc16);
border-radius: 9999px;
padding:       12px 24px;
font-weight:   600;
color:         white;
box-shadow:    0 4px 12px rgba(14,165,233,0.3);
transition:    all 0.2s ease;
```
Hover: `translateY(-2px)`, shadow spreads.

### Cards

```css
background:      rgba(255,255,255,0.7);
border:          1px solid rgba(255,255,255,0.5);
border-radius:   16px;
padding:         32px;
backdrop-filter: blur(8px);
box-shadow:      0 4px 6px -1px rgba(0,0,0,0.1);
transition:      transform 0.2s ease;
```
Hover: `translateY(-4px)`.

### Pill Tags / Badges

```css
background:    rgba(255,255,255,0.5);
border:        1px solid rgba(0,0,0,0.05);
border-radius: 9999px;
padding:       4px 12px;
font-size:     12px;
```

Use soft tints (`#fff0eb`, `#e8f7fe`, `#f2fde0`) for categorized/themed badges.

### Terminal / Code Block

Dark mode, regardless of site mode:
```css
background:    #0d1117 or #0c0e14;
border-radius: 10px–18px;
padding:       20px 24px;
font-family:   monospace;
font-size:     13px;
box-shadow:    0 24px 60px -12px rgba(0,0,0,0.45);
```

Include macOS traffic-light dots (`#ef4444`, `#f59e0b`, `#22c55e`) for realism.

### Ambient Background Glows (Dark Mode)

```css
/* Two blurred color blobs for atmospheric depth */
.glow-coral {
  position: absolute;
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(255,127,80,0.2) 0%, transparent 70%);
  top: -200px; right: -200px;
  filter: blur(80px);
}
.glow-azure {
  background: radial-gradient(circle, rgba(14,165,233,0.15) 0%, transparent 70%);
  bottom: -200px; left: -200px;
}
```

Add `grain overlay` (SVG or CSS noise filter) at `opacity: 0.02` for texture.

---

## Motion

All transitions are **ambient and micro** — never distracting.

```
Duration:    0.15s–0.2s ease
Hover lift:  translateY(-2px) to translateY(-4px)
Hover scale: 1.02–1.05 (images only)
Pulse/float: subtle keyframe animation for ambient glows only
Cursor blink: for terminal UI chrome
```

**Never use:** parallax, scroll-triggered animations, entrance animations on primary content, dramatic scale transforms.

---

## Code-Native Visual Motifs

These elements signal authenticity to a developer audience:

- **Terminal windows** with traffic-light dots and a dark shell environment
- **Monospace wordmarks** — using the mono font at huge display sizes
- **Command pill CTAs** — styled like shell commands: `$ npm install @tool`
- **Install tab selectors** — npm / pnpm / yarn segmented tabs
- **Version/status badges** — pill chips with soft tints
- **Gradient text** on key technical terms
- **Blinking cursor** in terminal chrome

Use at least one code motif on any developer-facing product site.

---

## Light vs Dark Mode Selection

| Use Light Mode when… | Use Dark Mode when… |
|----------------------|---------------------|
| The product is approachable/broad audience | The product is terminal/CLI/code-native |
| The site has editorial or blog content | The aesthetic is "hacker-friendly" |
| You want warmth and energy | You want focused, immersive, premium-dark |
| Site targets non-developers | Site targets power users / devs |

Both modes share the same accent trio, motion rules, and component language. The mode affects the background, surface colors, and glow strategy.

---

## Do / Don't

| ✅ Do | ❌ Don't |
|-------|---------|
| Use negative letter-spacing on large headings | Use flat, untracked display type |
| Pair one sans with one mono | Use three or more font families |
| Use the coral/azure/sage trio as accents | Use generic blue/gray brand colors |
| Keep hover motion subtle (2–4px lift) | Add slide-in, bounce, or parallax |
| Use terminal mockups for CLI products | Add stock photography |
| Use pill or soft-corner CTAs | Use square buttons |
| Breathe — use generous vertical spacing | Cram sections together |
| Key shadows to the accent color | Use generic `rgba(0,0,0,0.5)` on buttons |
| Add subtle grain/glow texture in dark mode | Use dark mode without atmospheric depth |
| Limit gradient use to focal points | Gradient entire page backgrounds |

---

## Applying This Skill

When designing a new site:

1. **Choose a mode** — light (glassmorphic, airy) or dark (terminal, atmospheric)
2. **Choose a font pair** from the table above
3. **Pick a layout personality** — spacious gallery (Max), compact utility (CPM/CPT), editorial (blog), or band-based (Paper)
4. **Apply the accent trio** at one or two focal points only
5. **Build one code motif** into the hero or feature section if the audience is developer-facing
6. **Write the CSS tokens** using the values in this spec as your starting point
7. **Let typography and spacing carry the design** — resist adding decorative elements