---
name: design-rules
description: Universal micro-UI/UX design & engineering rules based on Kole Jain, Chris McCoy, Ran Segall, and Satori Graphics' frameworks. Enforces Pro Typography hacks (-2% tracking, Major Third 1.25x scale, 150% body line-height), 60-30-10 color balance, Material opacity modulation, 12/8/4 column grids, 8pt spacing rhythm, 4-state buttons, scrolling CTA frequency, progressive backdrop blur overlays, Luxury White Space, and the LIFT System with 6 Levels of Visual Flow.
triggers:
  - /design-rules
  - design-rules
  - design rules
  - ui rules
  - typography hack
  - micro UI rules
  - luxury white space
  - lift system
---

# Universal Micro-UI/UX Engineering Rules (`design-rules`)

This skill provides fundamental micro-UI/UX design standards, typography hacks, type scale math, color balance systems, spacing scales, state architectures, conversion rules, luxury white space protocols, and composition flow systems based on Kole Jain, Chris McCoy, Ran Segall (Flux Academy), and Satori Graphics' master specifications.

*Integration Note:* This skill is automatically referenced and enforced by **`design-setup`** during page generation and evaluated by **`design-audit`** during UI reviews.

---

## 🔤 1. Pro Typography Rules, Font Sourcing & Type Scale Math

### 1.1 Font Sourcing (High-Personality Free Fonts)
Instead of defaulting to overused generic fonts, source clean, high-personality open-source fonts from:
* **Fontshare (`fontshare.com`):** Clean, professional, free fonts by Indian Type Foundry (e.g., *Clash Display, General Sans, Cabinet Grotesk, Satoshi, Switzer*).
* **Uncut (`uncut.wtf`):** Contemporary, experimental, high-personality open-source typefaces.
* **Single Font Rule:** For 95% of web projects, **you never need more than one font family**.

### 1.2 📐 Mathematical Type Scale (Major Third Ratio 1.25x)
Do NOT eyeball font sizes. Use the **Major Third (1.25x)** mathematical ratio relative to a base font size of `16px` (`1rem`):

| Text Element | REM Value | Pixel Equivalent | Scaling Ratio | Tailwind / CSS Rule |
| :--- | :--- | :--- | :--- | :--- |
| **Base Body Text** | `1rem` | `16px` | Base (1.0x) | `text-base` |
| **H6 / Subtext** | `1.25rem` | `20px` | 1.25x | `text-xl` |
| **H5 / Card Title** | `1.5625rem` | `25px` | 1.56x | `text-2xl` |
| **H4 / Section Header** | `1.953rem` | `31.25px` | 1.95x | `text-3xl` |
| **H3 / Major Section** | `2.441rem` | `39px` | 2.44x | `text-4xl` |
| **H2 / Page Title** | `3.052rem` | `48.8px` | 3.05x | `text-5xl` |
| **H1 / Hero Title** | `3.815rem` | `61px` | 3.81x | `text-6xl` |

*Shortcut:* Use `type-scale.com` to generate mathematical REM tables automatically.

### 1.3 ⚡ Headline Pro Typography Hack & Body Line-Height
* **Body Text Line-Height:** MUST be set to **150% (1.5x)** of font size for optimal legibility (`line-height: 1.5` or `leading-relaxed`).
* **Headline Pro Tracking & Leading Hack:** For large headings (`h1`, `h2`, hero titles):
  * **Tighten Letter Spacing (Tracking):** Set to `-2%` to `-3%` (`tracking-tight` or `letter-spacing: -0.025em`).
  * **Tighten Line Height (Leading):** Set to `110%` to `120%` (`leading-tight` or `line-height: 1.15`).

```css
/* Headline Pro Hack CSS */
.pro-headline {
  font-family: var(--font-sans);
  letter-spacing: -0.025em; /* -2.5% tracking */
  line-height: 1.12;        /* 112% leading */
}

/* Body Text Legibility CSS */
.pro-body {
  font-size: 1rem;       /* 16px */
  line-height: 1.5;      /* 24px line-height (150%) */
  letter-spacing: 0;     /* Default tracking */
}
```

---

## 🎨 2. 60-30-10 Color System & Material Opacity Modulation

### 2.1 The 60-30-10 Rule for Visual Balance
Limit project colors to 2-3 intentional hues. Allocate visual real estate using the 60-30-10 distribution:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        60 - 30 - 10 COLOR DISTRIBUTION                                 │
├───────────────────────────────────┬───────────────────────────┬────────────────────────┤
│ 60% Dominant Neutrals             │ 30% Secondary Surfaces    │ 10% Accent Color       │
│ • Page Backgrounds (White/Slate)  │ • Cards & Container Bg    │ • Primary CTAs & Focus │
│ • Primary Body Text               │ • Section Divider Backgrounds | • Active Status Badges  │
└───────────────────────────────────┴───────────────────────────┴────────────────────────┘
```

### 2.2 Material Opacity Modulation Hack
Instead of adding 5 random colors to a palette, modulate the opacity of 1 primary color to create harmonious monochromatic surface layers (Google Material Design technique):

```html
<!-- Opacity Modulation Example -->
<div class="bg-primary/10 border border-primary/20 text-primary"> Subtle Card Background </div>
<button class="bg-primary/90 hover:bg-primary text-white"> Primary Accent CTA </button>
```

### 2.3 WCAG Contrast Ratios & Extraction
* **Small Body Text:** Minimum **4.5:1** contrast ratio against background.
* **Large Headlines:** Minimum **3.0:1** contrast ratio.
* **Color Extraction Tool:** Use Chrome DevTools `CSS Overview` (`Ctrl+Shift+I` ➔ `...` ➔ `More Tools` ➔ `CSS Overview`) to extract color palettes, font stacks, and type scales from reference sites.

---

## 📐 3. Grid Systems & 8pt Spacing Rhythm

### 3.1 Responsive Column Grid Standard
* **Desktop (≥1024px):** 12-Column Grid (`grid-cols-12`).
* **Tablet (640px - 1023px):** 8-Column Grid (`grid-cols-8`).
* **Mobile (<640px):** 4-Column Grid (`grid-cols-4`).

### 3.2 8pt Spacing System
All element spacing, padding, margin, gap, and container heights MUST follow exact 8pt grid multiples (`8px`, `16px`, `24px`, `32px`, `48px`, `64px`, `96px`).

### 3.3 Intentional Grid Breaking Rule
Align 80-90% of elements strictly to the grid for structure, but **let 1 key focal element intentionally break out of the grid** (e.g., overlapping columns or rotated at a 45° angle) to create instant visual contrast and intrigue.

---

## 🌙 4. Dark Mode Elevation & Surface Rules

Dark mode operates under different physical design rules than Light Mode:

### 4.1 Depth via Lighter Surface Colors (NO Dark Shadows)
In Dark Mode, **drop shadows are invisible**. Create visual depth by making higher elevation surfaces **slightly lighter in background color** rather than relying on shadows.

```
Base Background (Z-Index 0):   #09090b (Darkest Slate/Black)
Card Surface (Z-Index 1):      #18181b (Slightly Lighter Zinc)
Popover / Modal (Z-Index 2):   #27272a (Lighter Surface)
```

### 4.2 Dark Mode Borders & Saturation
* **Borders:** Lower border opacity to avoid harsh white lines (`border-white/10` or `border-neutral-800`).
* **Badges / Chips:** Dim down background saturation & brightness, while keeping the text bright for contrast (e.g., `bg-emerald-950/50 text-emerald-400 border border-emerald-800/50`).

---

## 🔘 5. Buttons, Inputs & State Architecture

### 5.1 The 4 Mandatory Button States
Every interactive button MUST implement at least 4 distinct visual states:

1. **Default State:** Base styling with clear hierarchy (Primary Filled vs Secondary Ghost).
2. **Hover State:** Slight background brightness shift or subtle scale (`hover:bg-primary-dark` or `hover:scale-[1.02]`).
3. **Active / Pressed State:** Pressed inset feel (`active:scale-[0.98]`).
4. **Disabled State:** Reduced opacity (`opacity-50 cursor-not-allowed`) with interactions blocked.
5. *(Optional)* **Loading State:** Displays a inline spinner while disabling clicks.

### 5.2 Button Dimension & Padding Ratio
* A well-proportioned button has a **width approximately double its height**.
* *Example:* Height `40px` ➔ Horizontal Padding `px-5` (`20px` each side) total width `~100px+`.

### 5.3 Icon Sizing Rule (Match Text Line-Height)
* The height/width of an icon MUST match the **line-height of adjacent text**.
* *Example:* For text with a `24px` line-height (`text-base leading-6`), set icon size to `24px` (`w-6 h-6` or `size-6`).

---

## 🎯 6. Conversion CTA Frequency & Placement Rules

A high-converting webpage MUST follow the **Scrolling CTA Frequency Rule**:

1. **Hero CTA:** 1 prominent primary Call-to-Action button visible in the Hero section above the fold.
2. **Navigation Header CTA:** 1 sticky/fixed CTA button in the main navigation bar.
3. **Scrolling Frequency Rule:** Expose a visible CTA **every 2 to 3 seconds of scrolling** (approximately every `600px` to `800px` of vertical page distance).

---

## 💎 7. The Luxury White Space & Figure-Ground Protocol

Based on Ran Segall's (Flux Academy) framework for creating high-end, premium UIs:

### 7.1 "Space is Wealth" (White Space as Extravagant Value)
* **Never treat empty canvas as wasted real estate.** Generous white space signals high value, elegance, and exclusivity.
* **Eliminate Graphic Noise:** Avoid unnecessary divider lines (`<hr>`), heavy background boxes, or arbitrary decorative borders. Let white space separate content sections naturally.

### 7.2 Figure-Ground Relationship Isolation
* Isolate focal elements (products, hero shots, key metrics) against plain, uncluttered backgrounds. Removing background noise forces instant visual focus without needing directional arrows or labels.

---

## 🌊 8. The LIFT System & 6 Levels of Visual Flow

Based on Satori Graphics' masterclass framework for composition and eye choreography:

### 8.1 The 6 Levels of Movement & Flow
1. **Level 1 — Direct Guidance:** Literal path indicators (directional arrows, pointing vectors, visual bridges).
2. **Level 2 — Hierarchy Gravity:** Invisible gravity using size/contrast (Headline ➔ Subtitle ➔ Body).
3. **Level 3 — Micro-Routes & Fractal Loops:** Sub-card detail loops that let the eye explore extra info then reconnect to the main flow.
4. **Level 4 — Implied Motion:** Suggesting movement in static media (progressive scaling, directional gradients, blurred overlays).
5. **Level 5 — Flow Disruption:** Deliberate pattern breaks (e.g. rotated elements) forcing the brain to pause and re-engage.
6. **Level 6 — Temporal Flow (Musical Rhythm of Time):** Choreographing the temporal experience:
   * **Impact (Punch):** Hero image/headline hits hard and fast.
   * **Linger (Slow):** Detailed copy blocks where the eye slows down.
   * **Release (Pulse):** Vast open white space surrounding the CTA where the eye rests.

### 8.2 The LIFT System Blueprint

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE LIFT COMPOSITION SYSTEM                               │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ L — Leverage Point       │ I — Internal Rhythm      │ F — Friction & Flow (Seasoning)  │
│ • Single dominant hero   │ • Choreographed eye path │ • Flow = Smooth reading zones    │
│ • Pushes back competition│ • Predictable + surprise │ • Friction = Intentional tension │
├──────────────────────────┴──────────────────────────┴──────────────────────────────────┤
│ T — Transferability & Scalability (Holds up when shrunk to thumbnail / dark-light bg)   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

* **Friction Rule:** Treat visual friction (tight line-heights, overlapping text, skewed badges) like seasoning—just enough adds rich flavor, too much creates chaotic noise.

---

## 🖼️ 9. Progressive Overlay & Backdrop Blur

Never place text over a raw image or use a flat, heavy black overlay that ruins image quality.

* **Progressive Linear Gradient:** Use a linear gradient that transitions smoothly from transparent at the top to solid background color at the text baseline.
* **Backdrop Blur:** Combine with progressive `backdrop-blur-md` for a modern, high-end editorial feel.
