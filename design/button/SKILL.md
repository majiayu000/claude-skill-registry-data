---
name: button
description: Använd när du bygger, ändrar eller granskar knappar (<button>, CTA:er) i swedol-ui-prototype — alla varianter (Primary/Secondary/Blank/Destructive/Accent/System), storlekar och states (hover/focus/disabled) enligt ECO Design System.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Knapp-styling (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=2007-68126

### Varianter

| Variant | Bakgrund | Text | Border |
|---|---|---|---|
| **Primary** | `#000` | `#fff` | — |
| **Primary Inverted** | `#fff` | `#000` | — |
| **Secondary** | transparent | `#000` | `1px solid #000` |
| **Secondary Inverted** | transparent | `#fff` | `1px solid #fff` |
| **Blank** | transparent | `#000` | — |
| **Blank Inverted** | transparent | `#fff` | — |
| **Destructive** | `#d90000` | `#fff` | — |
| **Accent** | `#c7d300` | `#000` | — |
| **System** | transparent | `#000` | `1px solid rgba(0,0,0,0.10)` = `border-action-3` |
| **System Selected** | `rgba(0,0,0,0.12)` | `#000` | `1px solid rgba(0,0,0,0.10)` = `border-action-3` |
| **Disabled** (alla varianter) | `#e5e5e5` | `#939595` | — |
| **Disabled Blank** | transparent | `#939595` | — |

> **System** används för knappar som agerar på systemnivå (t.ex. filter, sortering, verktygsval). Skiljer sig från Secondary genom den subtila semitransparenta bordern (`border-action-3`) istället för solid svart.
> **System Selected** är aktivt/valt läge av System — samma border men med `rgba(0,0,0,0.12)` bakgrund som markerar valt tillstånd.

### Storlekar — Desktop (`min-width: 769px` / breakpoint `lg-md`)

| Storlek | Höjd | Padding (button) | Inre padding (text) | Font |
|---|---|---|---|---|
| **lg** | 56px | `16px` | `px-8px py-3px` | label-lg: 18px Bold, 0.18px spacing |
| **md** | 48px | `12px` | `px-8px py-3px` | label-lg: 18px Bold, 0.18px spacing |
| **sm** | 40px | `8px` | `px-8px py-4px` | label-md: 16px Bold, 0.48px spacing |
| **xs** | 32px | `6px` | `px-4px py-3px` | label-sm: 14px Bold, 0.56px spacing |

### Storlekar — Mobil (default / breakpoint `sm-xs`)

| Storlek | Höjd | Padding (button) | Font |
|---|---|---|---|
| **lg** | 48px | `12px` | label-lg: 16px Bold, 0.32px spacing |
| **md** | 40px | `8px` | label-lg: 16px Bold, 0.32px spacing |
| **sm** | 32px | `6px` | label-md: 14px Bold, 0.48px spacing |
| **xs** | 32px | `6px` | label-sm: 14px Bold, 0.56px spacing |

### Tillstånd (States)

| Tillstånd | Visuell regel |
|---|---|
| **Enabled** | Grundstil per variant ovan |
| **Hover – Primary / Destructive / Accent** | `background-image: linear-gradient(90deg, rgba(255,255,255,0.2), rgba(255,255,255,0.2)), linear-gradient(90deg, [basefärg], [basefärg])` — white 20% overlay över solid bakgrundsfärg. |
| **Hover – Secondary** | `background: rgba(0,0,0,0.05)` — subtil mörk overlay på transparent bakgrund. |
| **Hover – Blank / ikonknappar på ljus bakgrund** | `background: rgba(0,0,0,0.05)` — samma som Secondary hover. Används på `Blank`-knappar och ikonknappar på vit/ljus bakgrund. |
| **Focus** | Fokusring visas **bara vid tangentbordsnavigering** (Tab). Samma mekanism som form-element: `body.keyboard-nav button:focus::after { opacity: 1 }`. Ring: `border: 2px solid #455efb`, `inset: -3px`, `border-radius: 0`, `opacity: 0` som default med transition. |
| **Disabled** | Bg `#e5e5e5`, text `#939595`, `cursor: not-allowed` |

> Fokusringen implementeras som en global `button::after`-regel med `opacity: 0` som default. `body.keyboard-nav` sätts via JS när användaren trycker Tab och tas bort vid `mousedown`/`touchstart`. Använd **aldrig** `:focus-visible` för knappar — använd alltid `body.keyboard-nav`-mönstret för konsekvent beteende med form-elementen.

### Typografi (alla knappar)
- Font: `Breuer Condensed Bold`, sans-serif
- `text-transform: uppercase`
- `white-space: nowrap`
- `font-feature-settings: 'ss02' 1, 'ss03' 1` (för label-lg/md)

### CSS-mall (Primary)
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
  border: none;
  cursor: pointer;
  font-family: 'Breuer Condensed', Arial, sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  white-space: nowrap;
}

/* Storlekar – Desktop */
.btn--lg { height: 56px; padding: 16px; font-size: 18px; letter-spacing: 0.18px; }
.btn--md { height: 48px; padding: 12px; font-size: 18px; letter-spacing: 0.18px; }
.btn--sm { height: 40px; padding: 8px;  font-size: 16px; letter-spacing: 0.48px; }
.btn--xs { height: 32px; padding: 6px;  font-size: 14px; letter-spacing: 0.56px; }

/* Storlekar – Mobil (default, override med desktop: om behövs) */
/* lg-mobil = 48px, md-mobil = 40px, sm/xs-mobil = 32px */

/* Varianter */
.btn--primary           { background: #000; color: #fff; }
.btn--secondary         { background: transparent; color: #000; border: 1px solid #000; }
.btn--destructive       { background: #d90000; color: #fff; }
.btn--accent            { background: #c7d300; color: #000; }
.btn--blank             { background: transparent; color: #000; }

/* Hover */
.btn--primary:hover     { background-image: linear-gradient(90deg,rgba(255,255,255,.2),rgba(255,255,255,.2)), linear-gradient(90deg,#000,#000); }
.btn--destructive:hover { background-image: linear-gradient(90deg,rgba(255,255,255,.2),rgba(255,255,255,.2)), linear-gradient(90deg,#d90000,#d90000); }

/* Focus — outline-metoden, INTE ::after med inset.
   Orsak: ::after med inset positioneras från padding-kanten, inte border-kanten.
   Knappar med border (t.ex. Secondary 1px solid) tappar gapet (inset -3px - 1px border - 2px ring = 0px gap).
   outline mäter alltid från den yttre border-kanten → konsekvent 2px gap oavsett knappvariant. */
button { position: relative; outline: 2px solid transparent; outline-offset: 2px; transition: outline-color 100ms cubic-bezier(.35,0,.35,1); /* duration-fast-2, ease-standard */ }
body.keyboard-nav button:focus { outline-color: #455efb; /* border-focus */ }

/* Disabled */
.btn:disabled, .btn--disabled { background: #e5e5e5; color: #939595; cursor: not-allowed; border: none; }
.btn--blank:disabled           { background: transparent; }
```

---
