---
name: inline-link
description: Använd när du bygger en länk inuti en mening eller ett textblock — alltid understruken i enabled-läge, aldrig med ikon.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Inline Link (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=1671-52629

Används **inuti meningar och textblock**. Understruken i Enabled-tillståndet — understrykningen **tas bort** vid hover, ersatt av färgbyte. Kombineras **aldrig** med ikoner.

### Skillnad mot Action Link

| Egenskap | Inline Link | Action Link |
|---|---|---|
| Placering | I löptext | Fristående |
| Understrykning | Enabled: ja. Hover: nej (tas bort) | Enabled: nej. Hover: ja (läggs till) |
| Ikoner | Aldrig | Valfria (vänster/höger) |
| `display` | `inline` | `inline-flex` |

---

### Storlekar

#### Desktop (`md:`, 769px+)

| Storlek | Typografi-token | Font-size | Line-height | Letter-spacing | Weight |
|---|---|---|---|---|---|
| **Large** | `body-lg` | 20px | 28px | 0px | 400 |
| **Medium** | `body-md` | 16px | 24px | 0.32px | 400 |
| **Small** | `body-sm` | 14px | 20px | 0.28px | 400 |
| **Small Bold** | `body-sm` | 14px | 20px | 0.28px | **700** |

#### Mobile / Tablet (`xs`/`sm`, ≤768px)

| Storlek | Font-size | Line-height | Letter-spacing |
|---|---|---|---|
| **Large** | 18px | 24px | 0px |
| **Medium** | 16px | 22px | 0.32px |
| **Small / Small Bold** | 14px | 20px | 0.28px |

---

### Färgvarianter

| Variant | Enabled-färg | Hover-färg |
|---|---|---|
| **Text Primary** | `#000000` (`text-action-primary`) | `#737373` (`text-action-primary-hover`) |
| **Text Secondary** | `#4f4f4f` (`text-secondary`) | `#737373` (`text-action-secondary-hover`) |
| **Text Tertiary** | `#737373` (`text-tertiary`) | `#939595` (`text-action-tertiary-hover`) |
| **Text Primary Inverted** | `#ffffff` (`text-primary-inverted`) | `rgba(255,255,255,0.78)` (`text-action-primary-inverted-hover`) |

---

### Tillstånd (States)

| Tillstånd | Understrykning | Textfärg |
|---|---|---|
| **Enabled** | `text-decoration: underline` | Per variant ovan |
| **Hover** | `text-decoration: none` (tas bort) | Per variant ovan |
| **Enabled Accordion Link** | `text-decoration: underline` | Som Text Primary |
| **Hover Accordion Link** | `text-decoration: none` | Som Text Primary hover |

> Transition: `color` med `duration-fast-3` (150ms) och `ease-standard`. `text-decoration` transiteras inte.

---

### font-feature-settings

| Storlek | Värde |
|---|---|
| Large (`body-lg`) | `'ss02' 1, 'ss03' 1` |
| Medium (`body-md`) | `'ss02' 1, 'ss03' 1, 'ss06' 1` |
| Small / Small Bold (`body-sm`) | `'ss02' 1, 'ss03' 1, 'ss06' 1` |

---

### CSS-mall

```css
.inline-link {
  color: #000000;          /* text-action-primary — default */
  text-decoration: underline;
  font-family: 'Breuer Condensed', Arial, sans-serif;
  font-weight: 400;
  cursor: pointer;
  transition: color 150ms cubic-bezier(.35,0,.35,1); /* duration-fast-3, ease-standard */
}

/* Hover — understrykning tas bort */
.inline-link:hover { color: #737373; text-decoration: none; }

/* Storlekar — desktop */
.inline-link--large  { font-size: 20px; line-height: 28px; letter-spacing: 0px;    font-feature-settings: 'ss02' 1, 'ss03' 1; }
.inline-link--medium { font-size: 16px; line-height: 24px; letter-spacing: 0.32px; font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1; }
.inline-link--small  { font-size: 14px; line-height: 20px; letter-spacing: 0.28px; font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1; }

/* Small Bold */
.inline-link--small-bold { font-size: 14px; line-height: 20px; letter-spacing: 0.28px; font-weight: 700; font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1; }
.inline-link--small-bold:hover { color: #737373; text-decoration: none; }

/* Färgvarianter */
.inline-link--secondary { color: #4f4f4f; }
.inline-link--secondary:hover { color: #737373; }

.inline-link--tertiary { color: #737373; }
.inline-link--tertiary:hover { color: #939595; }

.inline-link--inverted { color: #ffffff; }
.inline-link--inverted:hover { color: rgba(255,255,255,0.78); }

/* Mobile */
@media (max-width: 768px) {
  .inline-link--large  { font-size: 18px; line-height: 24px; }
  .inline-link--medium { font-size: 16px; line-height: 22px; }
}
```

### HTML-exempel

```html
<!-- I löptext — Text Primary, Medium -->
<p>Läs mer om våra produkter på
  <a href="#" class="inline-link inline-link--medium">produktsidan</a>.
</p>

<!-- Text Secondary -->
<p>Se <a href="#" class="inline-link inline-link--medium inline-link--secondary">fullständiga villkor</a> för mer info.</p>

<!-- Small Bold -->
<a href="#" class="inline-link inline-link--small-bold">Läs mer</a>

<!-- Inverted, i mörk kontext -->
<p style="color:#fff">Kontakta oss via
  <a href="mailto:info@example.com" class="inline-link inline-link--medium inline-link--inverted">info@example.com</a>.
</p>
```

---
