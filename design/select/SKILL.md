---
name: select
description: Använd när du bygger eller granskar select-fält/dropdowns — storlekar, states och dropdown-pil enligt ECO Design System.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Select – Storlekar & Tillstånd (ECO Design System)

Select används för att låta användaren välja ett alternativ ur en lista. Komponentens storlek och tillstånd följer samma system som inputfält.

> Alla select-fält delar: `font-family: 'Breuer Condensed', sans-serif`, `font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1`, `border-radius: 0` (raka hörn), `appearance: none` (dold native pil), och en custom dropdown-pil (24px, Material Symbols `arrow_drop_down`).

---

### Storlekar per breakpoint

#### Desktop (`md:`, 769px+)

| Storlek | Höjd | Padding | Pil-ikon | Label | Select-text |
|---|---|---|---|---|---|
| **Large** | 48px | `8px` vert, `12px` horiz | 24px | `label-md`: 16px/16px, 0.48px, Bold, uppercase | `body-md`: 16px/24px, 0.32px, Regular |
| **Small** | 40px | `8px` alla sidor | 24px | `label-sm`: 14px/14px, 0.56px, Bold, uppercase | `body-sm`: 14px/20px, 0.28px, Regular |
| **XSmall** | 32px | `8px` alla sidor | 24px | `label-sm`: 14px/14px, 0.56px, Bold, uppercase | `body-sm`: 14px/20px, 0.28px, Regular |

#### Mobile / Tablet (`xs`/`sm`, 0–768px)

| Storlek | Höjd | Padding | Pil-ikon | Label | Select-text |
|---|---|---|---|---|---|
| **Large** | 40px | `8px` alla sidor | 24px | `label-md` (mobil): 14px/14px, 0.42px, Bold, uppercase | `body-md` (mobil): 16px/22px, 0.32px, Regular |
| **Small** | 32px | `8px` alla sidor | 24px | `label-sm` (mobil): 12px/12px, 0.48px, Bold, uppercase | `body-sm`: 14px/20px, 0.28px, Regular |

> Dropdown-pilen är placerad absolut: `right: 12px`, `top: 50%`, `transform: translateY(-50%)`. Höger padding på select måste vara minst `40px` för att ge utrymme åt pilen.

---

### Tillstånd (States)

Alla tillstånd ska implementeras varje gång ett select-fält skapas.

#### 1. Enabled (standard)
| Egenskap | Värde |
|---|---|
| Border | `1px solid var(--color-border-input-default)` → `#939595` |
| Bakgrund | `var(--color-surface-raised-primary)` → `#ffffff` |
| Placeholder-text | `var(--color-text-tertiary)` → `#737373` |
| Hint/meddelande | `var(--color-text-tertiary)` → `#737373` |

#### 2. Hover
| Egenskap | Värde |
|---|---|
| Border | `1px solid var(--color-border-dark)` → `#333333` |
| Bakgrund | `var(--color-surface-raised-primary)` → `#ffffff` |

#### 3. Active (alternativ valt)
| Egenskap | Värde |
|---|---|
| Border | `1px solid var(--color-border-selected)` → `#000000` |
| Bakgrund | `var(--color-surface-raised-primary)` → `#ffffff` |
| Select-text | `var(--color-text-primary)` → `#000000` |

> **Active state för select** kan inte detekteras med `:not(:placeholder-shown)`. Använd JS för att lägga till klassen `.is-active` på `.form-select-wrap` när ett icke-default alternativ väljs: `select.addEventListener('change', e => wrap.classList.toggle('is-active', e.target.selectedIndex !== 0))`.

#### 4. Focus (tangentbordsfokus)
| Egenskap | Värde |
|---|---|
| Border (selectruta) | `1px solid var(--color-border-input-default)` → `#939595` |
| Fokusring (utanför) | `2px solid var(--color-border-focus)` → `#455efb`, `inset: -3px` |
| Bakgrund | `var(--color-surface-raised-primary)` → `#ffffff` |

> Fokusringen visas **enbart** vid tangentbordsnavigering (Tab). Implementeras via `body.keyboard-nav .input-wrap:focus-within::after { opacity: 1; }`. Klick öppnar dropdown utan ring.

#### 5. Error
| Egenskap | Värde |
|---|---|
| Border | `1px solid var(--color-border-danger-default)` → `#d90000` |
| Bakgrund | `var(--color-surface-raised-primary)` → `#ffffff` |
| Meddelande | `var(--color-text-danger-default)` → `#d90000` + felikon 20px (`error`, filled) till vänster |

#### 6. Success
| Egenskap | Värde |
|---|---|
| Border | `1px solid var(--color-border-success-default)` → `#248616` |
| Bakgrund | `var(--color-surface-raised-primary)` → `#ffffff` |
| Meddelande | `var(--color-text-success)` → `#248616` |

#### 7. Disabled
| Egenskap | Värde |
|---|---|
| Border | `1px solid var(--color-border-disabled)` → `#dad9d7` |
| Bakgrund | `var(--color-surface-raised-secondary)` → `#f6f6f6` |
| Select-text | `var(--color-text-disabled)` → `#939595` |
| Cursor | `not-allowed` |

---

### Hint/meddelande-text (alla storlekar)
- `body-sm`: 14px/20px, letter-spacing 0.28px, Regular
- `font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1`
- Vänster-ikon vid fel: 20px Material Symbols `error` (filled, wght 300)

---

### CSS-mall (Desktop Large – alla tillstånd)

```css
/* Wrapper — hanterar fokusring och pil-ikon */
.form-select-wrap {
  position: relative;
}

/* Fokusring (se input-sektion — samma mekanism) */
.input-wrap.form-select-wrap::after {
  content: '';
  position: absolute;
  inset: -3px;
  border: 2px solid var(--color-border-focus);
  pointer-events: none;
  opacity: 0;
  transition: opacity var(--duration-fast-2) var(--ease-standard);
}
body.keyboard-nav .input-wrap.form-select-wrap:focus-within::after { opacity: 1; }

/* Select */
.form-select {
  height: 48px;                   /* Desktop Large */
  padding: 8px 40px 8px 12px;     /* extra höger-padding för pil */
  border: 1px solid var(--color-border-input-default);
  background: var(--color-surface-raised-primary);
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 16px;                /* body-md */
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.32px;
  color: var(--color-text-primary);
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
  appearance: none;
  cursor: pointer;
  width: 100%;
  box-sizing: border-box;
  outline: none;
  transition: border-color var(--duration-fast-3) var(--ease-standard);
}

/* Dropdown-pil */
.form-select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  width: 24px;
  height: 24px;
}

/* Hover */
.form-select:hover { border-color: var(--color-border-dark); }

/* Active (alternativ valt) — togglad via JS */
.form-select-wrap.is-active .form-select { border-color: var(--color-border-selected); }

/* Focus (cursor i fält) */
.form-select:focus { border-color: var(--color-border-selected); }

/* Error */
.form-select--error { border-color: var(--color-border-danger-default) !important; }

/* Success */
.form-select--success { border-color: var(--color-border-success-default) !important; }

/* Disabled */
.form-select:disabled {
  background: var(--color-surface-raised-secondary);
  border-color: var(--color-border-disabled);
  color: var(--color-text-disabled);
  cursor: not-allowed;
}
```

---
