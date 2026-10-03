---
name: typography
description: >
  Research-grounded typography for any text-bearing surface — web, PDF, email,
  documents. GENERATIVE: apply correct line length, font sizing, contrast, dark mode,
  mobile, and Japanese rules from the start when building any UI, page, layout,
  or document. REVIEW: audit existing CSS/HTML/templates for typography violations.
  Use this skill whenever you are writing CSS that touches font-size, line-height,
  max-width, color, or font-family. Use it when building any frontend component,
  page, or layout — even if the user doesn't mention typography. Use it when
  reviewing any rendered output for readability. Use it when generating PDFs,
  emails, or any formatted document. If text will be read by a human, this skill
  applies.
---

# Typography

Research-grounded decisions for every surface where humans read text. The
philosophy: the browser renders semantic HTML correctly; every typographic
decision on top of that is a bet. This skill records the bets worth making —
each grounded in research — and the ones to skip.

The iA Writer principle applies: fewer decisions, made well, applied consistently.

---

## Modes

### Generative — New Project

When starting a new page, component, or document:

1. **Establish tokens first.** Generate a typography token file (section 6) before writing any component CSS. Every size, color, and spacing value should reference a token.
2. **Detect language.** If the project serves Japanese content, apply the Japanese overrides (section 3) from the start — not as a retrofit.
3. **Set the reading container.** Every text-bearing surface gets a `max-width` constraint. No exceptions.
4. **Ship both color schemes.** Default to `prefers-color-scheme`. Never force one mode.
5. **Verify mobile.** Viewport meta tag, fluid font sizes via `clamp()`, touch targets ≥ 44px.
6. **Reader controls.** For reading-focused interfaces, provide user-facing font size control (e.g., 3 steps: small/default/large via a `--fs-scale` CSS variable multiplier). For Japanese content, offer horizontal/vertical mode toggle with per-content persistence.
7. **Write the project ledger.** Create `TYPOGRAPHY.md` in the project root (see section 7).

### Review — Existing Project

When auditing existing CSS, HTML, or rendered output:

1. **Line length** — is body text constrained to 45–80 CPL (Latin) or 30–40 CPL (Japanese)?
2. **Font size** — is body ≥ 16px on mobile, ≥ 18px on desktop?
3. **Line height** — is body ≥ 1.5 (Latin) or ≥ 1.65 (Japanese)?
4. **Contrast** — does body text meet 4.5:1 minimum? Compute from actual hex values.
5. **Dark mode** — is `#000` background or `#fff` text present? Both are violations.
6. **Japanese** — is `lang="ja"` declared? Is `line-break: strict` set? Is `font-style: italic` absent?
7. **Type scale** — are there more than 6 distinct sizes? Is the ratio consistent?
8. **Mobile** — viewport meta present? Touch targets ≥ 44px?
9. **Prohibitions** — scan for every item in section 4.
10. **Vertical text** — if Japanese content uses `writing-mode: vertical-rl`: is `text-align` set to `start` (not `justify`)? Is column height capped (~22em)? Is `width: max-content` set? Is `overflow-x: hidden` absent from body?
11. **Reader controls** — for reading interfaces: is font size adjustable? For Japanese: is writing mode toggleable with persistence?
12. **Write the project ledger.** Create or update `TYPOGRAPHY.md` in the project root (see section 7).

Report each finding with: **property**, **current value**, **correct value**, **why**.

---

## 1. Core Decisions (Latin / General)

Apply these unless the project brief specifies otherwise.

### 1.1 Line Length
```css
.text-container {
  max-width: min(90vw, 65ch);
  margin-inline: auto;
}
```
- Target: 60–65 CPL for reading. Hard limits: 45 min, 80 max.
- Use `ch` for Latin — scales with font size and zoom.
- Bringhurst: 45–75 CPL. Baymard: sweet spot ~65. Ruder: 50–60 for max speed.
- The tension (Dyson & Haselgrove 2001): speed peaks wider, comprehension peaks narrower. For retention, bias toward 60–65.

### 1.2 Font Size
```css
:root {
  --size-body: clamp(16px, 1.1vw + 14px, 18px);
}
body { font-size: var(--size-body); }
```
- Desktop body: 18px target.
- Mobile minimum: 16px absolute floor.
- Text-heavy surfaces (articles): 18–24px. Interaction-heavy (UI): 14–20px.
- Minimum for any readable text anywhere: 12px.

### 1.3 Line Height
```css
body          { line-height: 1.5; }  /* at 65ch column */
h1, h2        { line-height: 1.1; }
h3, h4        { line-height: 1.2; }
caption, label { line-height: 1.3; }
```
Line height couples to column width — wider columns need more vertical space for accurate return sweeps:
- 45ch → 1.4
- 65ch → 1.5
- 80ch → 1.6

Mobile body: 1.55–1.6 (screens held closer, read in varied conditions).

### 1.4 Type Scale (1.25 major third from 16px)
```css
:root {
  --size-xs:   0.75rem;    /* 12px — captions, fine print */
  --size-sm:   0.875rem;   /* 14px — labels, metadata */
  --size-base: 1rem;       /* 16px — body, inputs, nav */
  --size-md:   1.25rem;    /* 20px — lead, section intro */
  --size-lg:   1.5625rem;  /* 25px — H3, card titles */
  --size-xl:   1.953rem;   /* 31px — H2 */
  --size-2xl:  2.441rem;   /* 39px — H1 */
  --size-3xl:  3.052rem;   /* 49px — hero/display */
}
```
- 1.25 for standard web UI. 1.333 for editorial/reading layouts. 1.125 for dense dashboards.
- Maximum 5–6 distinct sizes per interface. More signals a missing design system.

### 1.5 Color and Contrast
```css
:root {
  color-scheme: light dark;
  --color-text:           #1a1a1a;
  --color-text-secondary: #595959;
  --color-text-disabled:  #8a8a8a;
  --color-bg:             #f5f5f5;
  --color-surface:        #ffffff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --color-text:           #e8e8e8;
    --color-text-secondary: #a0a0a0;
    --color-text-disabled:  #606060;
    --color-bg:             #121212;
    --color-surface:        #1e1e1e;
  }
}
```
- Light: target 7:1–10:1. Dark: target ~14:1.
- WCAG AA body text minimum: 4.5:1. Never drop below.
- Dark mode surfaces: `#121212` (base), `#1e1e1e` (+1), `#252525` (+2), `#2c2c2c` (+3).
- Dark mode accents: desaturate 20–40%. Never mechanically invert light-mode colors.

### 1.6 Font Weight as Hierarchy
| Weight | Value | Use for |
|--------|-------|---------|
| Regular | 400 | Body, most UI text |
| Medium | 500 | Active nav states |
| Semi-bold | 600 | Nav labels, buttons, subheadings |
| Bold | 700 | H1–H2, critical alerts only |
| Heavy | 800+ | Display/hero only |

Reserve bold for the top of hierarchy. Bold everywhere flattens the signal.

### 1.7 Spacing
```css
p + p { margin-block-start: 1.1em; }
h2    { margin-block-start: 2em; margin-block-end: 0.5em; }
h3    { margin-block-start: 1.75em; margin-block-end: 0.4em; }
```
Space above heading ≈ 2× space below — binds heading to its content.

### 1.8 Mobile
```css
/* Always include: <meta name="viewport" content="width=device-width, initial-scale=1"> */
:root {
  --size-h1: clamp(28px, 4vw + 16px, 48px);
  --size-h2: clamp(22px, 2.5vw + 16px, 32px);
  --size-h3: clamp(18px, 1.5vw + 14px, 25px);
}
a { padding-block: 0.25em; } /* Expand touch target without visual shift */
```
- Portrait: line length resolves naturally. Landscape: `min(90vw, 65ch)` caps it.
- Touch targets: 44×44px minimum (Apple HIG, WCAG 2.5.5).
- Use `rem` for font sizes, `em` for spacing, `px` only for borders.

### 1.9 Font Selection and Loading

**Selection quick picks** (for full detail, pairing guidance, and personality taxonomy: read `references/font-knowledge.md`):

| Context | Top pick | Runner-up |
|---------|----------|-----------|
| Web UI | Inter | Source Sans 3 |
| Long-form reading | Literata | Charter |
| Code | JetBrains Mono | Fira Code |
| Display headings | Fraunces (serif) / Space Grotesk (sans) | Playfair Display |
| Japanese sans | Noto Sans JP | M PLUS 1 |
| Japanese serif | Shippori Mincho | Zen Old Mincho |
| "Just pick a system" | Source superfamily (Sans + Serif + Code) | IBM Plex superfamily |

**System font stacks** (zero loading cost — use for performance-critical or native-feeling UIs):
```css
/* Sans-serif (UI) */
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", sans-serif;

/* Serif (reading/editorial) */
font-family: Georgia, "Times New Roman", serif;
```

**Loading defaults:**
- Self-host fonts. Cache partitioning killed the CDN advantage.
- woff2 only. Drop all other formats.
- `font-display: optional` as default — eliminates FOUT/FOIT. Use `swap` only for brand-critical display text.
- Variable fonts when using 2+ weights of the same family (smaller total than separate static files).
- Font budget: < 100KB total per page. High-performance target: < 50KB.
- Subset aggressively. Use `unicode-range` or `glyphhanger`.
- Enable `font-optical-sizing: auto` when using variable fonts.

**Pairing rule:** Two typefaces maximum. One for headings, one for body. Superfamilies (Source, IBM Plex, Noto) eliminate pairing risk entirely. When pairing across families, match x-height and proportions; contrast by category (serif + sans). For specific pairings and the full personality taxonomy, read `references/font-knowledge.md`.

**Anti-patterns to flag in review mode:**
- Montserrat + Roboto (or any "top of Google Fonts by popularity" combo) without a stated reason
- Display faces (Playfair, Lobster, Pacifico) used for body text
- More than 2 weight files loaded but only 1-2 used
- Faux italic (no true italic in the font; browser synthesizes oblique)
- Two fonts from the same category (e.g. two geometric sans) — looks like a mistake, not a choice
- Full Japanese font loaded without subsetting (2MB+)

---

## 2. Heading Line Length

Headings follow different CPL rules than body text:

| Level | Max CPL |
|-------|---------|
| Hero / H1 | 30–40 |
| H2 | 40–60 |
| H3 | 50–65 |
| Microcopy (CTAs) | 20–35 |

Long H1s dilute the message. Cap hero text at ~35 characters.

---

## 3. Japanese Typography Overrides

**Activate when:** `lang="ja"` is present, Japanese characters appear in content, or the project brief mentions Japanese.

**First action:** verify `lang="ja"` is set on `<html>` or the containing element. Without it, browser-level typography features (kinsoku, auto-phrase, text-autospace) do not activate.

### 3.1 Block Defaults (Horizontal)
```css
:lang(ja) {
  max-width: min(90vw, 38em);    /* em, not ch — ch measures ASCII '0' */
  line-height: 1.7;              /* kanji have no ascenders/descenders */
  letter-spacing: 0.05em;        /* aids character discrimination */
  text-align: justify;           /* horizontal only — no word spaces = no rivers */
  text-align-last: left;
  line-break: strict;            /* JIS X 4051 kinsoku */
  word-break: keep-all;
  overflow-wrap: break-word;
}
```
Note: `text-align: justify` applies to horizontal mode only. In vertical mode (`writing-mode: vertical-rl`), use `text-align: start` — justify stretches short columns to fill the height. See §3.8.

### 3.2 Headings
```css
:lang(ja) h1, :lang(ja) h2, :lang(ja) h3 {
  line-height: 1.25;
  letter-spacing: 0;
  word-break: auto-phrase;  /* phrase-boundary breaks, Chrome 119+ */
}
```

### 3.3 Font Stacks
```css
/* Gothic (sans-serif — UI, digital) */
:lang(ja) {
  font-family:
    'Hiragino Kaku Gothic ProN', 'ヒラギノ角ゴ ProN',
    'Yu Gothic', '游ゴシック体', YuGothic,
    'Meiryo', 'メイリオ',
    'Noto Sans JP', sans-serif;
}

/* Mincho (serif — reading, editorial) */
.reading-content:lang(ja) {
  font-family:
    'Hiragino Mincho ProN', 'ヒラギノ明朝 ProN',
    'Yu Mincho', '游明朝体', YuMincho,
    'Noto Serif JP', serif;
}
```

### 3.4 Mixed Content
```css
/* Japanese primary, Latin inline */
:lang(ja) .latin-inline { font-size: 1.1em; }

/* Latin primary, Japanese inline */
:lang(ja) span.ja-inline { font-size: 0.9em; }

/* Inter-script spacing (progressive) */
@supports (text-autospace: ideograph-alpha) {
  :lang(ja) { text-autospace: ideograph-alpha ideograph-numeric; }
}
```

### 3.5 Punctuation Spacing
```css
/* Native CSS (Chrome 118+) */
:lang(ja) { text-spacing-trim: trim-start; }
```
For broader support, consider the Yaku Han JP library for half-width punctuation.

### 3.6 Emphasis (not italics)
```css
/* Japanese emphasis = bōten dots, not italic */
.emphasis-ja {
  text-emphasis: filled circle;
  text-emphasis-position: over right;
}
```

### 3.7 Font Subsetting
Japanese fonts are 2MB+. Always subset:
```css
@font-face {
  font-family: 'Noto Sans JP';
  src: url('...') format('woff2');
  unicode-range: U+3000-9FFF, U+F900-FAFF, U+FF00-FFEF;
}
```

### 3.8 Vertical Text (縦書き Tategaki)

Vertical Japanese text uses `writing-mode: vertical-rl` — columns flow top-to-bottom, right-to-left. This inverts many layout assumptions. Everything below was learned through implementation, not theory.

**When to offer vertical mode:** Reading interfaces serving Japanese literary or editorial content should offer both horizontal and vertical as a reader preference, with per-content persistence (localStorage). Vertical is not purely an author decision — it is a legitimate reader choice for Japanese.

```css
/* Vertical reading container */
.vertical-content {
  writing-mode: vertical-rl;
  max-width: none;                         /* width is unconstrained — content flows horizontally */
  width: max-content;                      /* REQUIRED — auto collapses in flex contexts */
  height: min(calc(100dvh - 7rem), 22em);  /* 20 chars/column ≈ genkōyōshi standard */
  font-family: var(--font-ja);
  line-height: var(--lh-body-ja);
  letter-spacing: 0.05em;
  text-align: start;                       /* NOT justify — justify stretches short columns */
}

/* Scroll container for vertical text */
.vertical-scroll {
  overflow-y: hidden;
  overflow-x: auto;                        /* horizontal scroll = "read forward" */
  -webkit-overflow-scrolling: touch;
  display: flex;
  justify-content: center;                 /* center when content is shorter than viewport */
  align-items: center;                     /* vertical centering of capped-height columns */
}
```

**Critical implementation traps:**

| Trap | Why it breaks | Fix |
|------|--------------|-----|
| `height` controls column length, not `max-width` | Axis inversion — vertical-rl swaps the meaning of width/height | Use `height` to cap characters per column |
| `width: auto` on vertical content | Collapses to zero in flex contexts | Use `width: max-content` |
| `display: flex` on parent | Constrains vertical-rl children unpredictably | Use `display: block`, or add `flex-shrink: 0` on the vertical child |
| `body { overflow-x: hidden }` | Common CSS reset clips vertical-rl overflow entirely | Remove or scope the reset; never apply globally when vertical text is present |
| `text-align: justify` | Stretches short columns vertically to fill the height | Use `text-align: start` for vertical mode |
| No scroll affordance | Users don't expect horizontal scrolling — "read forward" direction is invisible | Add a scroll hint (fade-out indicator) or swipe gesture cue |
| Column height shorter than viewport | Text block hangs at top of viewport | Center vertically with flex `align-items: center` |

**Column height target:** 20 characters per column ≈ 22em (with 0.05em letter-spacing). This follows the genkōyōshi (原稿用紙) manuscript paper standard. It is the vertical equivalent of `max-width: 65ch` for horizontal Latin text.

### 3.9 Rule Inversions Summary

| Property | Latin | Japanese (horizontal) | Japanese (vertical) |
|----------|-------|-----------------------|---------------------|
| CPL target | 60–65 | 30–40 | 20 chars/column |
| Column constraint | `max-width` | `max-width: 38em` | `height: 22em` |
| Width unit | `ch` | `em` | `em` |
| Line-height (body) | 1.5 | 1.7 | 1.7 |
| Letter-spacing (body) | 0 | 0.05em | 0.05em |
| Text alignment | left | justify | start |
| Overflow/scroll | vertical | vertical | horizontal (right-to-left) |
| Container width | constrained | constrained | `max-content` |
| Parent layout | flex works | flex works | block safer |
| Italics | available | never — use weight or text-emphasis | never |
| `word-break` | default | `keep-all` | `keep-all` |
| `line-break` | default | `strict` | `strict` |

---

## 4. Absolute Prohibitions

These are categorical. Flag as errors when auditing. Never produce them when generating.

### Latin
1. `text-align: justify` on Latin text
2. `font-size` below 12px for any readable text
3. `#000` on `#fff` for body text — soften both values
4. `#000` as dark mode background — use `#121212`
5. More than 6 distinct font sizes without documented reason
6. Letter-spacing on mixed-case body text — only ALL-CAPS labels, max `0.05em`
7. Full-width liquid layout for long-form reading
8. Mechanical dark mode inversion — create dark-specific tokens
9. ALL-CAPS for text longer than 4–5 words
10. Omitting viewport meta tag for mobile-served pages

### Japanese
1. `word-break: break-all` on Japanese text — catastrophic
2. `font-style: italic` on Japanese text — never
3. `ch` units for Japanese column width — use `em`
4. Omitting `lang="ja"` — mandatory for correct rendering
5. Full Japanese font without subsetting — 2MB+ unacceptable
6. Default browser font for Japanese — MS Mincho is unusable
7. `text-align: justify` without `text-align-last: left` (horizontal only)
8. Ignoring punctuation spacing — full-width stacking creates gaps
9. `text-align: justify` on vertical Japanese text — stretches short columns to fill height; use `start`
10. `overflow-x: hidden` on `body` when vertical text is present — clips the entire reading surface
11. `width: auto` on `writing-mode: vertical-rl` containers in flex contexts — collapses; use `max-content`

---

## 5. Non-Web Surfaces

The same principles apply to PDF, email, and document generation. The implementation changes.

### PDF Generation
- Line length: 60–65 characters per line. Set column width to achieve this.
- Font size: 11–12pt body (print equivalent of 16–18px screen).
- Line height: 1.4–1.5 for body (print needs slightly less than screen).
- Contrast: ensure sufficient contrast for both screen viewing and print.
- Japanese: 30–40 CPL, 1.6–1.7 line height.

### Email Templates
- Body font size: 16px minimum — email clients don't support `clamp()`.
- Line length: constrain with `max-width` on the content table/div, target 550–600px.
- Use inline styles — email clients strip `<style>` blocks unpredictably.
- Dark mode: many email clients auto-invert. Test with and without `color-scheme: light dark`.
- System font stacks only — web fonts are unreliable in email.
- Japanese email: inline `lang="ja"` on the wrapping element; use Noto Sans JP as web font if the ESP supports it, otherwise rely on system Gothic stack.

### Document Generation (Markdown, DOCX, etc.)
- Same CPL and line-height targets as web.
- For Markdown rendered to HTML: the CSS token file (section 6) applies directly.
- For DOCX: set paragraph style to equivalent values (11pt body, 1.5 line spacing, 6pt paragraph spacing).

---

## 6. CSS Token File

When starting a new web project, generate this token file as the typography foundation:

```css
/* typography-tokens.css */
:root {
  /* Scale (1.25 major third) */
  --size-xs:   0.75rem;
  --size-sm:   0.875rem;
  --size-base: 1rem;
  --size-md:   1.25rem;
  --size-lg:   1.5625rem;
  --size-xl:   1.953rem;
  --size-2xl:  2.441rem;
  --size-3xl:  3.052rem;

  /* Line height */
  --lh-body:     1.5;
  --lh-heading:  1.1;
  --lh-subhead:  1.2;
  --lh-label:    1.3;
  --lh-body-ja:  1.7;

  /* Japanese font stack */
  --font-ja: 'Hiragino Kaku Gothic ProN', 'Yu Gothic', '游ゴシック体', YuGothic, 'Meiryo', 'Noto Sans JP', sans-serif;

  /* Color — light */
  --color-text:           #1a1a1a;
  --color-text-secondary: #595959;
  --color-text-disabled:  #8a8a8a;
  --color-bg:             #f5f5f5;
  --color-surface:        #ffffff;

  /* Reader font size control */
  --fs-scale: 1;           /* multiplier — toggle between 0.85, 1, 1.15 */

  /* Vertical Japanese */
  --column-height-ja: 22em; /* 20 chars/column ≈ genkōyōshi */

  /* Spacing */
  --paragraph-gap: 1.1em;

  color-scheme: light dark;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-text:           #e8e8e8;
    --color-text-secondary: #a0a0a0;
    --color-text-disabled:  #606060;
    --color-bg:             #121212;
    --color-surface:        #1e1e1e;
  }
}

body {
  font-size: calc(clamp(16px, 1.1vw + 14px, 18px) * var(--fs-scale));
  line-height: var(--lh-body);
  color: var(--color-text);
  background-color: var(--color-bg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", sans-serif;
  font-optical-sizing: auto;
}

.reading-content {
  max-width: min(90vw, 65ch);
  margin-inline: auto;
}

.reading-content p + p { margin-block-start: var(--paragraph-gap); }

h1 { font-size: clamp(28px, 4vw + 16px, 48px); line-height: var(--lh-heading); }
h2 { font-size: clamp(22px, 2.5vw + 16px, 32px); line-height: var(--lh-heading);
     margin-block-start: 2em; margin-block-end: 0.5em; }
h3 { font-size: clamp(18px, 1.5vw + 14px, 25px); line-height: var(--lh-subhead);
     margin-block-start: 1.75em; margin-block-end: 0.4em; }

/* Japanese overrides */
:lang(ja) {
  max-width: min(90vw, 38em);
  line-height: var(--lh-body-ja);
  letter-spacing: 0.05em;
  text-align: justify;
  text-align-last: left;
  line-break: strict;
  word-break: keep-all;
  overflow-wrap: break-word;
  font-family: var(--font-ja);
}

:lang(ja) h1, :lang(ja) h2, :lang(ja) h3 {
  line-height: 1.25;
  letter-spacing: 0;
  word-break: auto-phrase;
}

a { padding-block: 0.25em; }

/* Vertical Japanese reading */
.vertical-content:lang(ja) {
  writing-mode: vertical-rl;
  max-width: none;
  width: max-content;
  height: min(calc(100dvh - 7rem), var(--column-height-ja));
  text-align: start;
  line-height: var(--lh-body-ja);
  letter-spacing: 0.05em;
}
```

---

## 7. Project Ledger — `TYPOGRAPHY.md`

Every project this skill touches gets a `TYPOGRAPHY.md` file in the project root. This is the typography decision record for that project — what was found, what was changed, and why. It persists across sessions so anyone reading the project later understands the typographic choices without re-auditing.

**Create it** at the end of every generative or review session. If it already exists, **append** a new session entry — never overwrite previous entries.

### Structure

Use this template. Fill in only the sections that apply to the current session.

```markdown
# Typography

Project-specific typography decisions and audit history.

---

## Current State

<!-- Updated each session. This is a snapshot — overwrite on each visit. -->

| Property | Value | Status |
|----------|-------|--------|
| Body CPL | e.g. 65ch | conforming / non-conforming / not set |
| Body font size | e.g. clamp(16px, 1.1vw + 14px, 18px) | ... |
| Body line-height | e.g. 1.5 | ... |
| Light contrast | e.g. #1a1a1a on #f5f5f5 (~10:1) | ... |
| Dark mode | e.g. #e8e8e8 on #121212 (~14:1) | ... |
| Type scale | e.g. 1.25 major third, 6 sizes | ... |
| Mobile viewport | present / missing | ... |
| Touch targets | ≥44px / undersized / not checked | ... |
| Japanese support | yes / no / partial | ... |
| Token file | e.g. typography-tokens.css | present / absent |

## Session Log

### YYYY-MM-DD — [Generative | Review | Update]

**Mode:** Generative / Review
**Surfaces touched:** e.g. main layout CSS, dark mode tokens, email template

#### Before
<!-- What existed before this session. For new projects, write "Greenfield — no prior typography." -->

#### Decisions
<!-- What was set or changed, and the reasoning. Reference skill rule numbers. -->

| Decision | Value chosen | Basis |
|----------|-------------|-------|
| e.g. Body CPL | 65ch | Skill §1.1 — Baymard sweet spot |
| e.g. Dark bg | #121212 | Skill §1.5 — Material Design, depth cues |

#### Violations Found
<!-- Review mode only. Leave blank for generative. -->

| Property | Was | Should be | Fixed? |
|----------|-----|-----------|--------|
| e.g. Dark bg | #000000 | #121212 | yes |

#### After
<!-- What the project looks like now. -->

#### Open Items
<!-- Anything deferred, blocked, or needing user input. -->
```

### Rules

- **Current State table:** overwrite each session with the latest snapshot. This is the "at a glance" view.
- **Session Log entries:** append-only. Newest first. Never edit previous entries.
- **Be specific.** Write actual hex values, actual pixel sizes, actual `clamp()` expressions — not "improved contrast" or "fixed font size."
- **Cite the skill.** Reference section numbers (e.g., "Skill §1.1", "Skill §4, prohibition #3") so decisions trace back to their basis.
- **Greenfield projects** still get a Before section — write "Greenfield — no prior typography" so the record is complete.

---

## 8. Detailed Reference

For full rationale, research citations, and extended CSS examples:
- Latin typography: read `references/latin-typography.md`
- Japanese typography: read `references/japanese-typography.md`
- Font selection, pairing, personality, loading, and licensing: read `references/font-knowledge.md`

Consult these when a decision is not covered above, when advising on font selection, or when explaining a rule's basis to the user.
