---
name: checkbox
description: Använd när du bygger eller granskar checkboxar — ljusläge (standard och detaljerad tabell-ikon-variant) och mörkt läge (dark mode), inklusive samtliga states (enabled/hover/focus/selected/indeterminate/disabled).
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Checkbox-styling (ECO Design System)

Checkboxar följer ECO Design Systems specifikation: total yta **24×24px**, synlig ruta **16×16px**.

### Storleksmodell
- Synlig ruta: `16px × 16px` (`appearance: none`, custom border)
- Marginal: `4px` på alla sidor → total yta 24×24px
- Fokusring: `outline: 2px`, `outline-offset: 2px` → fyller exakt marginalen (2px gap + 2px ring = 4px)

### Tillstånd

| Tillstånd | Visuell regel |
|---|---|
| Enabled | 1.5px solid `#000` border, vit bakgrund |
| Hover | border-width: 2px |
| Focus | Blå fokusring `#0052CC`, 2px, offset 2px |
| Selected | Svart fill `#000`, vit bockmarkering (SVG) |
| Indeterminate | Svart fill `#000`, vit streck (SVG) |
| Disabled | Border `#dad9d7`, vit bakgrund, `cursor: not-allowed` |
| Disabled Selected | Fill `#939595`, border `#939595` |
| Disabled label | Text `#939595` via `:has(input:disabled) span` |

### HTML-struktur
```html
<label class="form-checkbox-item">
  <input type="checkbox" />
  <span>Label</span>
</label>
```

### CSS-mall
```css
.form-checkbox-item { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.form-checkbox-item input[type="checkbox"] {
  appearance: none; width: 16px; height: 16px;
  border: 1.5px solid #000; background: #fff;
  cursor: pointer; flex-shrink: 0; margin: 4px;
}
.form-checkbox-item input[type="checkbox"]:hover { border-width: 2px; }
.form-checkbox-item input[type="checkbox"]:focus-visible { outline: 2px solid #0052CC; outline-offset: 2px; }
.form-checkbox-item input[type="checkbox"]:checked { background-color: #000; border-color: #000; /* + SVG checkmark */ }
.form-checkbox-item input[type="checkbox"]:indeterminate { background-color: #000; border-color: #000; /* + SVG dash */ }
.form-checkbox-item input[type="checkbox"]:disabled { border-color: #dad9d7; cursor: not-allowed; }
.form-checkbox-item input[type="checkbox"]:disabled:checked { background-color: #939595; border-color: #939595; }
.form-checkbox-item:has(input:disabled) { cursor: not-allowed; }
.form-checkbox-item:has(input:disabled) span { color: #939595; }
```

---

## Checkbox-styling (ECO Design System)

Figma-referens: `node-id=6408-8453`

Implementera alltid checkboxar med `<input type="checkbox">` + CSS — aldrig med `<img>` eller SVG-filer.

### States

| State | Bakgrund | Border | Bock |
|---|---|---|---|
| **Default (unchecked)** | `--color-background-primary` | `1.5px solid --color-border-selected` | — |
| **Checked** | `--color-surface-100` (svart) | `--color-border-selected` | Vit (`stroke="white"`) |
| **Hover (unchecked)** | — | `2px solid --color-border-selected` | — |
| **Hover (checked)** | `--color-text-disabled` (#939595) | `--color-text-disabled` (#939595) | Vit |
| **Disabled unchecked** | `--color-background-primary` | `--color-border-disabled` (#dad9d7) | — |
| **Disabled checked** | `--color-surface-disabled` (#e5e5e5) | ingen (matchar bakgrund) | Grå (`stroke="#939595"`) |
| **Indeterminate** | `--color-surface-100` (svart) | `--color-border-selected` | Vit horisontell linje |

> **OBS:** `disabled:checked` = ljusgrå bakgrund (#e5e5e5) + grå bock (#939595).  
> **Inte** mörk grå bakgrund + vit bock — det är hover-selected-stilen.

### Tabellens check-ikoner

I tabeller används samma `<input type="checkbox">` + CSS med klassen `.check-icon`:

```html
<!-- Aktiv behörighet -->
<td class="check-icon"><input type="checkbox" checked disabled /></td>

<!-- Ingen behörighet -->
<td class="check-icon"><input type="checkbox" disabled /></td>
```

---

## Checkbox – Dark Mode (ECO Design System)

**Figma:** `❖ Form Elements` → COMPONENT_SET `Checkbox/Dark` (node `22256:676`)

> Använd alltid dark mode-varianten av Checkbox när komponenten placeras på mörk bakgrund (`surface-100` #000, `surface-80` #333 eller liknande). Blanda **aldrig** ljuslägesvarianten på mörk yta.

### Variantegenskaper

| Egenskap | Värden |
|---|---|
| `Color Mode` | `Dark` |
| `Version` | `Desktop`, `Mobile` |
| `State` | `Enabled`, `Hover`, `Focus`, `Selected`, `Selected Hover`, `Selected Focus`, `indeterminate`, `Disabled`, `Disabled Selected`, `Inline Menu`, `Inline Menu Hover`, `Inline Menu Selected`, `Inline Menu Selected Hover`, `Inline Menu indeterminate`, `Inline Menu indeterminate Hover` |
| `Size` | `Large`, `Small` |

> `Selected Hover` finns enbart för `Version=Desktop Large` och `Version=Mobile Large`.

### Semantiska tokens (dark mode)

Alla fills och strokes är bundna till variabler ur ECO Design System-samlingen `Semantic: Design Tokens`.

| Element | State | Token | Hex |
|---|---|---|---|
| Checkbox-ruta fill | Enabled / Hover / Focus / Disabled | `color/surface-opacity-white-0` | transparent |
| Checkbox-ruta fill | Selected / Selected Focus / indeterminate | `color/border-action-2` | `#ffffff` |
| Checkbox-ruta fill | Selected Hover | `color/surface-40` | `#939595` |
| Checkbox-ruta fill | Disabled Selected | `color/surface-60` | `#595959` |
| Checkbox-ruta stroke | Enabled / Hover / Focus / Selected | `color/border-action-2` | `#ffffff` |
| Checkbox-ruta stroke | Disabled / Disabled Selected | `color/surface-60` | `#595959` |
| Bock (check) | Selected / Selected Focus | `color/surface-100` | `#000000` |
| Bock | Selected Hover | `color/border-action-2` | `#ffffff` |
| Indeterminate-dash | indeterminate | `color/surface-100` | `#000000` |
| Pil-ikon (Inline Menu) | Alla states | `color/icon-inverted` | `#ffffff` |
| Label-text | Enabled → indeterminate / Inline Menu | `color/text-primary-inverted` | `#ffffff` |
| Label-text | Disabled / Disabled Selected | `color/text-disabled` | `#939595` |
| Message-text | Enabled → indeterminate / Inline Menu | `color/text-tertiary-inverted` | `#999999` |
| Message-text | Disabled / Disabled Selected | `color/text-disabled` | `#939595` |

### CSS-mall

```css
/* Wrapper */
.form-checkbox-item--dark { display: flex; align-items: center; gap: 8px; cursor: pointer; }

/* Checkbox-ruta */
.form-checkbox-item--dark input[type="checkbox"] {
  appearance: none;
  width: 16px;
  height: 16px;
  border: 1.5px solid #ffffff;      /* border-action-2 */
  background: transparent;          /* surface-opacity-white-0 */
  cursor: pointer;
  flex-shrink: 0;
  margin: 4px;
}

/* Hover — tjockare border */
.form-checkbox-item--dark input[type="checkbox"]:hover { border-width: 2px; }

/* Selected */
.form-checkbox-item--dark input[type="checkbox"]:checked {
  background-color: #ffffff;        /* border-action-2 */
  border-color: #ffffff;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 16 16' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M3 8l3.5 3.5L13 5' stroke='%23000000' stroke-width='1.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
}

/* Selected Hover */
.form-checkbox-item--dark input[type="checkbox"]:checked:hover {
  background-color: #939595;        /* surface-40 */
  border-color: #939595;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 16 16' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M3 8l3.5 3.5L13 5' stroke='%23ffffff' stroke-width='1.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
}

/* Focus */
.form-checkbox-item--dark input[type="checkbox"]:focus-visible {
  outline: 2px solid #455efb;       /* border-focus */
  outline-offset: 2px;
}

/* Disabled */
.form-checkbox-item--dark input[type="checkbox"]:disabled {
  border-color: #595959;            /* surface-60 */
  cursor: not-allowed;
}

/* Disabled Selected */
.form-checkbox-item--dark input[type="checkbox"]:disabled:checked {
  background-color: #595959;        /* surface-60 */
  border-color: #595959;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 16 16' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M3 8l3.5 3.5L13 5' stroke='%23939595' stroke-width='1.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
}

/* Label-text */
.form-checkbox-item--dark span {
  color: #ffffff;                   /* text-primary-inverted */
  font-family: 'Breuer Condensed', sans-serif;
}

/* Disabled label */
.form-checkbox-item--dark:has(input:disabled) { cursor: not-allowed; }
.form-checkbox-item--dark:has(input:disabled) span { color: #939595; /* text-disabled */ }
```

### HTML-exempel

```html
<!-- Enabled -->
<label class="form-checkbox-item form-checkbox-item--dark">
  <input type="checkbox" />
  <span>Label</span>
</label>

<!-- Selected -->
<label class="form-checkbox-item form-checkbox-item--dark">
  <input type="checkbox" checked />
  <span>Label</span>
</label>

<!-- Disabled Selected -->
<label class="form-checkbox-item form-checkbox-item--dark">
  <input type="checkbox" checked disabled />
  <span>Label</span>
</label>
```

### Regler

1. **IMPORTANT:** Använd alltid `.form-checkbox-item--dark` på mörk bakgrund – aldrig `.form-checkbox-item` (ljusläge).
2. **IMPORTANT:** Hårdkoda aldrig hex-färger – använd alltid CSS-variabler om projektet har ett token-system: `var(--color-border-action-2)`, `var(--color-surface-60)`, etc.
3. Bock-ikonen implementeras alltid som inline SVG `background-image` eller `<input type="checkbox">` + CSS – aldrig som `<img>` eller extern SVG-fil.
4. Focus-ringen (`#455efb`, `outline-offset: 2px`) ska **alltid** visas vid tangentbordsnavigering (`:focus-visible`).
5. `Disabled Selected`-state: grå ruta (`#595959`) + grå bock (`#939595`) – **inte** mörk bakgrund med vit bock (det är hover-selected-stilen).

---
