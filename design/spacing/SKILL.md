---
name: spacing
description: Använd när du sätter marginal, padding eller gap — den fasta Spacing Scale (space-0…space-120) och de brytpunktsanpassade space-sm/space-md/space-lg-tokens.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Spacing (ECO Design System)

Spacing-tokens skapar ett förutsägbart och harmoniskt avståndssystem. Tokens appliceras på alla marginaler, padding och positionskoordinater – både horisontellt och vertikalt.

> Majoriteten av värdena är multipler av 8px. Värdena 1px, 2px och 4px används enbart för detaljnivå. 12px är ett komplement när det behövs.

### Spacing Scale

| Token | Värde | Användning |
|---|---|---|
| `space-0` | 0px | Nollställ avstånd |
| `space-1` | 1px | Detaljnivå – mycket fina justeringar |
| `space-2` | 2px | Detaljnivå – borders, fina justeringar |
| `space-4` | 4px | Detaljnivå – inre padding i täta komponenter |
| `space-8` | 8px | Bas-enhet. Inre padding, gap i täta layouter |
| `space-12` | 12px | Komplement. Paragraph-spacing, täta listor |
| `space-16` | 16px | Standard padding. Mobil sidmarginal |
| `space-24` | 24px | Medium spacing. Gutter på desktop |
| `space-32` | 32px | Tablet/desktop-marginal. Sektionsavstånd |
| `space-40` | 40px | Desktop sidmarginal (lg). Sektionsavstånd |
| `space-48` | 48px | Stora sektionsavstånd |
| `space-56` | 56px | Komponenthöjd lg-knapp på desktop |
| `space-64` | 64px | Stora layoutavstånd |
| `space-72` | 72px | Stora layoutavstånd |
| `space-80` | 80px | Hero-sektioner, stora vertikala avstånd |
| `space-112` | 112px | Extra stora layoutavstånd |
| `space-120` | 120px | Grid margin på desktop |

### Layout Vertical Whitespace (per brytpunkt)

Utöver den flata Spacing Scale ovan finns en semantisk, **brytpunktsanpassad** skala (T-shirt-storlekar: sm/md/lg) för vertikalt avstånd mellan element i en layout — t.ex. `gap` i en flex-column-sektion (som `.compare-intro`) eller `padding-top` framför en avslutande CTA-rad (`.section-cta`). Till skillnad från `space-24`/`space-48` osv. (fasta pixelvärden, samma på alla brytpunkter) ändras `space-sm`/`space-md`/`space-lg` HÄR i pixelvärde beroende på brytpunkt:

| Token | `breakpoint-xs` | `breakpoint-sm` | `breakpoint-md` | `breakpoint-lg` | `breakpoint-xl` |
|---|---|---|---|---|---|
| `space-lg` | 32px | 40px | 48px | 56px | 56px |
| `space-md` | 24px | 32px | 40px | 48px | 48px |

> Använd `space-lg`/`space-md` (denna tabell) för luft MELLAN sektionens egna innehållsblock (t.ex. rubrik → kort-grid → CTA-knappar i samma sektion) — inte för `space-24`/`space-40` osv. (fasta Spacing Scale-värden ovan), som passar bättre för layout-marginaler och gutter som INTE ska variera lika finkornigt per brytpunkt.

```css
/* Exempel: gap i en flex-column-sektion, space-lg */
.hero {
  display: flex;
  flex-direction: column;
  gap: 32px;                              /* xs: space-lg */
}
@media (min-width: 640px) {
  .hero { gap: 40px; }                    /* sm: space-lg */
}
@media (min-width: 769px) {
  .hero { gap: 48px; }                    /* md: space-lg */
}
@media (min-width: 1024px) {
  .hero { gap: 56px; }                    /* lg: space-lg */
}
@media (min-width: 1281px) {
  .hero { gap: 56px; }                    /* xl: space-lg */
}
```

---

### Hur tokens används

Spacing appliceras genom att kombinera ett **token** (storlek) med en **konsumentklass** (var avståndet ska appliceras).

#### Konsumentklasser

**Margin**
| Klass | CSS-property |
|---|---|
| `mt-space` | `margin-top` |
| `mr-space` | `margin-right` |
| `mb-space` | `margin-bottom` |
| `ml-space` | `margin-left` |
| `mx-space` | `margin-left` + `margin-right` |
| `my-space` | `margin-top` + `margin-bottom` |

**Padding**
| Klass | CSS-property |
|---|---|
| `pt-space` | `padding-top` |
| `pr-space` | `padding-right` |
| `pb-space` | `padding-bottom` |
| `pl-space` | `padding-left` |
| `px-space` | `padding-left` + `padding-right` |
| `py-space` | `padding-top` + `padding-bottom` |

**Gap (layoutavstånd)**
| Klass | CSS-property |
|---|---|
| `gap-space` | `gap` (rad + kolumn) |
| `gap-x-space` | `column-gap` |
| `gap-y-space` | `row-gap` |

### Exempel

```css
/* Padding: space-16 */
.card { padding: 16px; }

/* Margin: space-24 vertikalt, space-8 horisontellt */
.item { margin: 24px 8px; }

/* Gap i grid: space-24 */
.grid { display: grid; gap: 24px; }
```

```html
<!-- Typiska kombinationer per breakpoint -->
<!-- xs: space-16 sidmarginal, space-8 gap -->
<section style="padding: 0 16px;">
  <div style="display:grid; gap:8px;">...</div>
</section>

<!-- sm/md: space-32 sidmarginal, space-16 gap -->
<section style="padding: 0 32px;">
  <div style="display:grid; gap:16px;">...</div>
</section>

<!-- lg: space-40 sidmarginal, space-24 gap -->
<section style="padding: 0 40px;">
  <div style="display:grid; gap:24px;">...</div>
</section>
```

---
