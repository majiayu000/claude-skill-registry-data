---
name: typography-system
description: >
  Design a complete typography system — font pairing, type hierarchy,
  micro-typography (line-height, letter-spacing, measure), web font
  performance (font-display, preload, system stacks), and Vietnamese
  diacritic considerations. Use when the user asks to "choose fonts",
  "set up typography", "fix text spacing", "font pairing", "type scale",
  or "web font loading". Do NOT use when a design token system already
  exists — extend it instead. Works standalone or as a layer on top of
  design-system-gen output.
origin: yamtam
version: 1.0.0
compatibility: "Any frontend stack. Outputs CSS custom properties + @font-face / Google Fonts import."
---

<!-- Original YAMTAM skill. Typography rules derived from public typographic
     principles (Bringhurst, Google Fonts knowledge base, web.dev/fonts).
     No code ported. All structure and content original. -->

## When to Use

- Use when: user asks "what font should I use for X"
- Use when: text feels cramped, too loose, hard to read, or generic
- Use when: setting up a new project's text baseline
- Use when: deploying web fonts and worried about layout shift / FOIT
- Do NOT use for full design token generation — use `design-system-gen`
- Do NOT use for aesthetic mood selection — use `aesthetic-anchor` first, then this

---

## Step 1 — Font Pairing

### The two-role rule
Every type system needs exactly **two roles**. Three is usually one too many.

| Role | Purpose | Where |
|---|---|---|
| **Display** | Headings, hero text, brand moments | h1–h3, large callouts |
| **Body** | Paragraphs, labels, UI copy | p, small, inputs, captions |

Optional third: **Mono** for code, data, technical values only.

### Pairing principles

| Principle | Rule |
|---|---|
| Contrast, not conflict | Pair a geometric sans with a humanist serif, or a slab with a grotesque. Never two fonts from the same sub-family. |
| Shared proportions | Fonts pair well when their x-heights are similar — text won't feel mismatched at body sizes. |
| One personality font | Display font can be expressive. Body font must be neutral and highly legible. |
| Weight range | Prefer families with ≥ 4 weights (Regular, Medium, SemiBold, Bold). Synthetic bold breaks spacing. |

### Pairing reference by product type

| Product | Display | Body |
|---|---|---|
| SaaS / Dev tool | Inter, Geist, DM Sans | Same family, different weight |
| Fintech | Sora, IBM Plex Sans | IBM Plex Sans or Source Sans |
| Healthcare | Nunito, Source Sans | Source Sans, Open Sans |
| E-commerce | Poppins, Plus Jakarta Sans | Inter, Outfit |
| Creative | Clash Display, Cabinet Grotesk | Satoshi, General Sans |
| Editorial | Playfair Display, Lora | Source Serif, Spectral |
| AI / Data | Space Grotesk, Geist | Geist Mono (data), Inter (prose) |

---

## Step 2 — Type Hierarchy (Without Color)

Hierarchy through type alone — weight, size, spacing. Do not rely on color as the only differentiator.

```
Level 1 — Page title:    font-size: 2.25–3rem  / weight: 700–800 / tracking: -0.02em
Level 2 — Section head:  font-size: 1.5–1.875rem / weight: 600–700 / tracking: -0.01em
Level 3 — Subsection:    font-size: 1.125–1.25rem / weight: 600   / tracking: 0
Level 4 — Body:          font-size: 1rem          / weight: 400   / tracking: 0
Level 5 — Caption/label: font-size: 0.75–0.875rem / weight: 500   / tracking: +0.01em
```

Rules:
- Headings compress tracking (negative letter-spacing) — large text optically needs tightening
- Small text opens tracking (positive letter-spacing) — small text needs breathing room
- Never go below `font-size: 0.75rem` (12px) for readable text
- Avoid more than 3 font sizes on a single screen

---

## Step 3 — Micro-Typography

### Line-height (leading)

```
Display (h1–h2):   line-height: 1.1–1.2   — tight, intentional
Heading (h3–h4):   line-height: 1.3–1.4
Body text:         line-height: 1.5–1.65  — optimal reading range
Small/caption:     line-height: 1.4–1.5   — slightly tighter than body
Code/mono:         line-height: 1.6–1.75  — needs extra room
```

### Vietnamese typography adjustment
Vietnamese uses stacked diacritics (ắ, ộ, ữ) that extend far above and below the baseline. Standard Western line-heights clip these marks.

```css
/* Vietnamese text needs extra leading */
:lang(vi), [lang="vi"] {
  line-height: 1.7;          /* minimum — 1.5 clips diacritics */
  word-spacing: 0.05em;      /* slight word spacing improves readability */
}

/* Fonts with good Vietnamese coverage */
/* Preferred: Be Vietnam Pro, Nunito, Source Sans 3, IBM Plex Sans */
/* Avoid: fonts without full Latin Extended Additional block */
```

### Measure (line length)
Optimal reading: **45–75 characters per line** (≈ 60ch ideal).

```css
p, li, blockquote {
  max-width: 65ch;   /* hard limit on prose containers */
}
```

Never let body text span full viewport width on desktop — it breaks reading rhythm.

### Letter-spacing cheat sheet
```css
/* Headings — negative tracking tightens large type */
h1 { letter-spacing: -0.025em; }
h2 { letter-spacing: -0.015em; }
h3 { letter-spacing: -0.01em; }

/* Body — zero is correct, do not add */
p  { letter-spacing: 0; }

/* ALL CAPS labels — always needs positive tracking */
.label-caps { letter-spacing: 0.08em; }

/* Small text (< 14px) — slight opening helps legibility */
small, caption { letter-spacing: 0.01em; }
```

---

## Step 4 — Web Font Performance

### Loading strategy (in order of priority)

```html
<!-- 1. Preconnect to font origin early -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- 2. Preload critical font files (first font only — body weight) -->
<link rel="preload" href="/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
```

```css
/* 3. font-display: swap prevents invisible text (FOIT) */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-400.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;   /* show system font first, swap when loaded */
}
```

### System font stack fallback
Always define a fallback so unstyled text is still readable during load:

```css
--font-body: 'Inter', system-ui, -apple-system, BlinkMacSystemFont,
             'Segoe UI', Roboto, Helvetica, Arial, sans-serif;

--font-mono: 'Geist Mono', 'JetBrains Mono', ui-monospace,
             'SFMono-Regular', Consolas, monospace;

/* Vietnamese fallback — include font with full diacritic coverage */
--font-vi:   'Be Vietnam Pro', 'Nunito', system-ui, sans-serif;
```

### Weight subsetting — load only what you use
```
Google Fonts URL: add &display=swap and limit weights
?family=Inter:wght@400;500;600;700&display=swap

Self-hosted: use fonttools/pyftsubset to strip unused glyphs
```

Never load a full font family (all weights, all subsets) — it adds 200–800 KB per font.

---

## Output Format

```css
/* Typography System — [Product Type] */
/* Generated by YAMTAM typography-system */

@import url('...');  /* Google Fonts import — body weight first */

:root {
  /* Fonts */
  --font-display: 'Poppins', system-ui, sans-serif;
  --font-body:    'Inter', system-ui, -apple-system, sans-serif;
  --font-mono:    'JetBrains Mono', ui-monospace, monospace;

  /* Scale */
  --text-xs:   0.75rem;   /* 12px */
  --text-sm:   0.875rem;  /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg:   1.125rem;  /* 18px */
  --text-xl:   1.25rem;   /* 20px */
  --text-2xl:  1.5rem;    /* 24px */
  --text-3xl:  1.875rem;  /* 30px */
  --text-4xl:  2.25rem;   /* 36px */

  /* Leading */
  --leading-tight:  1.2;
  --leading-snug:   1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.65;

  /* Tracking */
  --tracking-tight:  -0.02em;
  --tracking-normal:  0;
  --tracking-wide:    0.05em;
}

/* Prose container */
.prose { max-width: 65ch; line-height: var(--leading-normal); }

/* Vietnamese override */
:lang(vi) { line-height: 1.7; word-spacing: 0.05em; }
```

---

## Anti-Fake-Pass Rules

Before claiming the typography system is done, you MUST show:
- [ ] Font pairing stated — display + body named, rationale given (1 sentence)
- [ ] Type hierarchy shown — at least 3 levels with size + weight + tracking
- [ ] Line-height values given for body and headings
- [ ] Web font loading: `font-display: swap` and system fallback stack present
- [ ] If content is Vietnamese or multilingual: `:lang(vi)` override present

Reference: `gates/anti-fake-pass-gate.md` | `gates/ui-quality-gate.md`
