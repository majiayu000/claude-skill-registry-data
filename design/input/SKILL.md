---
name: input
description: Använd när du bygger eller granskar textinputfält — storlekar (Large/Small/XSmall), samtliga states (enabled/hover/active/focus/error/success/disabled) och label/hint-mönster enligt ECO Design System.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Inputfält – Storlekar & Tillstånd (ECO Design System)

Inputfält används för att mata in fritext, nummer eller annan data. De kan kombineras med ikoner, ledtext och felmeddelanden.

> Alla inputfält delar: `font-family: 'Breuer Condensed', sans-serif`, `font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1` och `border-radius: 0` (raka hörn).

---

### Storlekar per breakpoint

#### Desktop (`md:`, 769px+)

| Storlek | Höjd | Padding | Ikon | Label | Input-text |
|---|---|---|---|---|---|
| **Large** | 48px | `12px` horiz, `8px` vert | 24px | `label-md`: 16px/16px, 0.48px, Bold, uppercase | `body-md`: 16px/24px, 0.32px, Regular |
| **Small** | 40px | `8px` alla sidor | 20px | `label-sm`: 14px/14px, 0.56px, Bold, uppercase | `body-sm`: 14px/20px, 0.28px, Regular |
| **XSmall** | 32px | `8px` alla sidor | 20px | `label-sm`: 14px/14px, 0.56px, Bold, uppercase | `body-sm`: 14px/20px, 0.28px, Regular |

#### Mobile / Tablet (`xs`/`sm`, 0–768px)

| Storlek | Höjd | Padding | Ikon | Label | Input-text |
|---|---|---|---|---|---|
| **Large** | 40px | `8px` alla sidor | 24px | `label-md` (mobil): 14px/14px, 0.42px, Bold, uppercase | `body-md` (mobil): 16px/22px, 0.32px, Regular |
| **Small** | 32px | `8px` alla sidor | 20px | `label-sm` (mobil): 12px/12px, 0.48px, Bold, uppercase | `body-sm`: 14px/20px, 0.28px, Regular |

> **Tumregel:** Desktop Large = 48px (standardformulär), Desktop Small = 40px (kompakta ytor), Mobile Large = 40px (standardformulär på mobil). Välj alltid den storlek som passar breakpointen.

**Hint/meddelande-text** (under inputfältet, alla storlekar):
- `body-sm`: 14px/20px, letter-spacing 0.28px, Regular
- Vänster-ikon: 20px (Material Symbols Outlined, wght 300)

---

### Tillstånd (States)

Alla tillstånd ska implementeras varje gång ett inputfält skapas. Tillstånden styr border, bakgrund, textfärg och hjälptexter.

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
| Placeholder-text | `var(--color-text-tertiary)` → `#737373` |
| Hint/meddelande | `var(--color-text-tertiary)` → `#737373` |

#### 3. Active (ifyllt / focus med värde)
| Egenskap | Värde |
|---|---|
| Border | `1px solid var(--color-border-selected)` → `#000000` |
| Bakgrund | `var(--color-surface-raised-primary)` → `#ffffff` |
| Input-text | `var(--color-text-primary)` → `#000000` |
| Rensa-ikon | Visas (cancel-ikon fylld, 20px) + divider `1px, var(--color-border-tertiary)` |
| Hint/meddelande | `var(--color-text-tertiary)` → `#737373` |

#### 4. Focus (tangentbordsfokus, ingen ring på selekt)
| Egenskap | Värde |
|---|---|
| Border (inputruta) | `1px solid var(--color-border-input-default)` → `#939595` |
| Fokusring (utanför) | `2px solid var(--color-border-focus)` → `#455efb`, `inset: -3px` (offset utanför) |
| Bakgrund | `var(--color-surface-raised-primary)` → `#ffffff` |
| Placeholder-text | `var(--color-text-tertiary)` → `#737373` |

> Fokusringen placeras som ett absolut element `inset: -3px` utanför inputrutan – inte som `outline` på input-elementet självt.

#### 5. Error
| Egenskap | Värde |
|---|---|
| Border | `1px solid var(--color-border-danger-default)` → `#d90000` |
| Bakgrund | `var(--color-surface-raised-primary)` → `#ffffff` |
| Input-text | `var(--color-text-primary)` → `#000000` |
| Meddelande | `var(--color-text-danger-default)` → `#d90000` + felikon 20px (error) till vänster om texten |

#### 6. Success
| Egenskap | Värde |
|---|---|
| Border | `1px solid var(--color-border-success-default)` → `#248616` |
| Bakgrund | `var(--color-surface-raised-primary)` → `#ffffff` |
| Input-text | `var(--color-text-primary)` → `#000000` |
| Meddelande | `var(--color-text-success)` → `#248616` |

#### 7. Disabled
| Egenskap | Värde |
|---|---|
| Border | `1px solid var(--color-border-disabled)` → `#dad9d7` |
| Bakgrund | `var(--color-surface-raised-secondary)` → `#f6f6f6` |
| Placeholder-text | `var(--color-text-disabled)` → `#939595` |
| Meddelande | `var(--color-text-disabled)` → `#939595` |
| Cursor | `not-allowed` |

---

### Anatomi

```
[Label]                      ← label-md/sm, uppercase, text-primary
[Ikon] [Input-text...]  [✕|⊕] ← inputruta med valfri vänster-ikon + höger clear+divider+action
[Hint/felmeddelande]         ← body-sm, tertiary / danger / success
```

- **Label**: Alltid uppercase, font Bold. Placeras ovanför inputrutan med `gap: 4px`.
- **Vänster-ikon** (valfri): Material Symbols Outlined, wght 300, 24px (Large) / 20px (Small/XSmall).
- **Höger clear-ikon**: Visas enbart i `Active`-tillståndet. Ikonstorlek 20px (cancel filled). Separeras från övriga höger-ikoner av en 1px divider (`border-tertiary`, 16px hög).
- **Meddelande**: Alltid `body-sm` (14px), visas under inputrutan med `gap: 4px`.

---

### CSS-mall (Desktop Large – alla tillstånd)

```css
/* Wrapper */
.form-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* Label */
.form-label {
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 16px;          /* Desktop Large: label-md */
  font-weight: 700;
  line-height: 16px;
  letter-spacing: 0.48px;
  text-transform: uppercase;
  color: var(--color-text-primary);
  font-feature-settings: 'ss02' 1, 'ss03' 1;
}

/* Input wrapper (position: relative för fokusring) */
.input-wrap { position: relative; }

/* Fokusring (absolut, utanför) — animeras med opacity */
.input-wrap::after {
  content: '';
  position: absolute;
  inset: -3px;
  border: 2px solid var(--color-border-focus);
  pointer-events: none;
  opacity: 0;
  transition: opacity var(--duration-fast-2) var(--ease-standard);
}
/* Ring visas bara vid tangentbordsnavigering — body.keyboard-nav sätts via JS */
body.keyboard-nav .input-wrap:focus-within::after { opacity: 1; }

/* Input */
.form-input {
  height: 48px;                  /* Desktop Large */
  padding: 8px 12px;
  border: 1px solid var(--color-border-input-default);
  background: var(--color-surface-raised-primary);
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 16px;               /* body-md */
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.32px;
  color: var(--color-text-primary);
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
  width: 100%;
  box-sizing: border-box;
  outline: none;
}

/* Placeholder */
.form-input::placeholder {
  color: var(--color-text-tertiary);
}

/* Hover */
.form-input:hover { border-color: var(--color-border-dark); }

/* Active (har värde — placeholder visas ej) */
.form-input:not(:placeholder-shown) { border-color: var(--color-border-selected); }

/* Focus — inner border stays border-input-default; only the blue ring (::after) appears */
.form-input:focus { border-color: var(--color-border-input-default); }

/* Error */
.form-input--error { border-color: var(--color-border-danger-default); }

/* Success */
.form-input--success { border-color: var(--color-border-success-default); }

/* Disabled */
.form-input:disabled {
  background: var(--color-surface-raised-secondary);
  border-color: var(--color-border-disabled);
  color: var(--color-text-disabled);
  cursor: not-allowed;
}

/* Hint/meddelande */
.form-helper {
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 14px;               /* body-sm */
  font-weight: 400;
  line-height: 20px;
  letter-spacing: 0.28px;
  color: var(--color-text-tertiary);
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
}
.form-helper--error   { color: var(--color-text-danger-default); display: flex; align-items: center; gap: 4px; }
.form-helper--success { color: var(--color-text-success); }
.form-helper--disabled{ color: var(--color-text-disabled); }

/* Mobile Small override (32px) */
@media (max-width: 768px) {
  .form-input--sm {
    height: 32px;
    font-size: 14px;
    line-height: 20px;
    letter-spacing: 0.28px;
  }
  .form-label--sm {
    font-size: 12px;
    line-height: 12px;
    letter-spacing: 0.48px;
  }
}
```

---
