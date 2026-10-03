---
name: action-link
description: Använd när du bygger en fristående klickbar länk med valfri vänster-/höger-ikon som INTE ligger i löptext — t.ex. "Visa alla produkter →".
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Action Link (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=1671-52811

En klickbar länk med valfri vänster-ikon och höger-pil. Används för navigering och nedladdning.

---

### Anatomi

```
[Vänster-ikon (valfri)] [Länktext] [→ chevron-ikon]
```

- Länktexten är **inte** understruken i Enabled-läge — understrykning visas **enbart** vid hover.
- Höger-ikon: `chevron_right` (Large: 24px, Medium/Small: 20px)
- Vänster-ikon (valfri, t.ex. `file_download`): Large: 24px, Medium/Small: 20px
- **IMPORTANT:** Ikoner får **aldrig** understrykning på hover — endast länktexten ska understrykas. Sätt `text-decoration: none` explicit på ikon-elementet (`.action-link .ms`), annars ärver ikonen `text-decoration: underline` från den hover:ade länken.

---

### Storlekar

#### Desktop (`md:`, 769px+)

| Storlek | Typografi-token | Font-size | Line-height | Letter-spacing | Gap | Ikon |
|---|---|---|---|---|---|---|
| **Large** | `body-lg` | 20px | 28px | 0px | 8px | 24px |
| **Medium** | `body-md` | 16px | 24px | 0.32px | 4px | 20px |
| **Small** | `body-sm` | 14px | 20px | 0.28px | 4px | 20px |

#### Mobile / Tablet (`xs`/`sm`, ≤768px)

| Storlek | Font-size | Line-height | Letter-spacing |
|---|---|---|---|
| **Large** | 18px | 24px | 0px |
| **Medium** | 16px | 22px | 0.32px |
| **Small** | 14px | 20px | 0.28px |

> Small har samma värden på desktop och mobil.

---

### Varianter

| Variant | Enabled-färg | Hover-färg |
|---|---|---|
| **Text Primary** | `#000000` (`text-action-primary`) | `#737373` (`text-action-secondary-hover`) |
| **Text Primary Inverted** | `#ffffff` (`text-primary-inverted`) | `rgba(255,255,255,0.78)` (`text-action-primary-inverted-hover`) |

**Font-weight:** Regular (400) eller Bold (700). Båda varianterna finns i alla storlekar.

---

### Tillstånd (States)

| Tillstånd | Understrykning | Textfärg |
|---|---|---|
| **Enabled** | Ingen | `text-action-primary` / `text-primary-inverted` |
| **Hover** | `text-decoration: underline` | `text-action-secondary-hover` / `text-action-primary-inverted-hover` |

> Transition: `color` och `text-decoration-color` med `duration-fast-3` (150ms) och `ease-standard`.

---

### font-feature-settings

| Storlek | Värde |
|---|---|
| Large (`body-lg`) | `'ss02' 1, 'ss03' 1` |
| Medium (`body-md`) | `'ss02' 1, 'ss03' 1, 'ss06' 1` |
| Small (`body-sm`) | `'ss02' 1, 'ss03' 1, 'ss06' 1` |

---

### CSS-mall

```css
.action-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;                /* Large */
  text-decoration: none;
  color: #000000;          /* text-action-primary */
  font-family: 'Breuer Condensed', Arial, sans-serif;
  font-weight: 400;
  cursor: pointer;
  transition: color 150ms cubic-bezier(.35,0,.35,1); /* duration-fast-3, ease-standard */
}

/* Storlekar */
.action-link--large  { font-size: 20px; line-height: 28px; letter-spacing: 0px;    font-feature-settings: 'ss02' 1, 'ss03' 1; }
.action-link--medium { font-size: 16px; line-height: 24px; letter-spacing: 0.32px; font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1; gap: 4px; }
.action-link--small  { font-size: 14px; line-height: 20px; letter-spacing: 0.28px; font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1; gap: 4px; }

/* Hover */
.action-link:hover { color: #737373; text-decoration: underline; }

/* Ikoner ska aldrig understrykas, bara länktexten */
.action-link .ms { text-decoration: none; }

/* Inverted (på mörk bakgrund) */
.action-link--inverted       { color: #ffffff; }
.action-link--inverted:hover { color: rgba(255,255,255,0.78); }

/* Bold-variant */
.action-link--bold { font-weight: 700; }

/* Mobile */
@media (max-width: 768px) {
  .action-link--large  { font-size: 18px; line-height: 24px; }
  .action-link--medium { font-size: 16px; line-height: 22px; }
}
```

### HTML-exempel

```html
<!-- Large, Regular, med ikon -->
<a href="#" class="action-link action-link--large">
  <span class="material-symbols-outlined" style="font-size:24px">file_download</span>
  Ladda ner dokument
  <span class="material-symbols-outlined" style="font-size:24px">chevron_right</span>
</a>

<!-- Medium, Regular -->
<a href="#" class="action-link action-link--medium">
  Visa alla produkter
  <span class="material-symbols-outlined" style="font-size:20px">chevron_right</span>
</a>

<!-- Small, Bold, Inverted -->
<a href="#" class="action-link action-link--small action-link--bold action-link--inverted">
  Läs mer
  <span class="material-symbols-outlined" style="font-size:20px">chevron_right</span>
</a>
```

---
