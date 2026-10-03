---
name: tile-link
description: Använd när du bygger en grafisk/prominent länk som presenteras som ett kort eller en knapp — varumärkeslogotyper, ikon+label-plattor. Ersätter inte vanliga knappar eller länktyper i löptext.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Tile Link (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=1671-53188

Används som **kort eller knapp** när länken behöver presenteras grafiskt och prominent — t.ex. varumärkeslogotyper som länkgrupp eller ikoner med text. Ska **inte** ersätta vanliga knappar eller länktyper i löptext.

---

### Varianter

| Variant | Innehåll | Placering |
|---|---|---|
| **Brand** | Varumärkeslogotyp (bild) | Horizontal |
| **Label + Icon** | Material Symbol (24px/20px) + textlabel | Vertical eller Horizontal |
| **Label Only** | Textlabel utan ikon | Horizontal |

### Storlekar

| Storlek | Typ | Beskrivning |
|---|---|---|
| **Large** | Alla varianter | Större yta, tydligare hierarki |
| **Small** | Label + Icon, Label Only | Kompakt yta |

### Bakgrundsfärger

| Färg | Bakgrund | Enabled border | Hover border |
|---|---|---|---|
| **White** | `#ffffff` (`surface-action-2`) | `#e5e5e5` (`border-primary`) | `#333333` (`border-hover`) |
| **Grey** | `#f6f6f6` (`surface-raised-secondary`) | `#e5e5e5` (`border-primary`) | `#333333` (`border-hover`) |
| **Black** | `#000000` (`surface-action-1`) | `#000000` (`border-action-1`) | `#000000` + white 20% overlay |

---

### Tillstånd (States)

| Tillstånd | Border | Textfärg | Bakgrund |
|---|---|---|---|
| **Enabled** | `1px solid border-primary` (#e5e5e5) | `text-primary` (#000) | Per färgvariant |
| **Hover** | `1px solid border-hover` (#333) | `text-action-primary-hover` (#737373) | Per färgvariant |
| **Hover – Black** | `1px solid border-action-1` (#000) | Ikon/text förblir vit | `linear-gradient(rgba(255,255,255,0.2), rgba(255,255,255,0.2)), linear-gradient(#000,#000)` |

> Bordern implementeras som ett absolut positionerat element (`inset: 0`) inuti tile-länken — inte som `border` på container-elementet direkt. Detta gör att bordern inte påverkar layoutens dimensioner.

---

### Mått per variant och breakpoint

#### Brand

| Version | Höjd | Padding (horisontell) | Logotyp |
|---|---|---|---|
| **Desktop Large** | 112px | `px-48px` | 48×99px |
| **Mobile Large** | 80px | `px-32px` | 24×50px |

#### Label + Icon — Desktop (`769px+`)

| Storlek | Placering | Padding | Ikon | Gap |
|---|---|---|---|---|
| **Large** | Vertical | `px-16px py-10px` | 24px | `gap: 4px` |
| **Large** | Horizontal | `px-16px py-8px` | 20px | `gap: 8px` |
| **Small** | Vertical | `px-16px py-8px` | 24px | `gap: 4px` |
| **Small** | Horizontal | `px-16px py-6px` | 20px | `gap: 8px` |

#### Label + Icon — Mobile (`≤768px`)

| Storlek | Placering | Padding | Ikon | Gap |
|---|---|---|---|---|
| **Large** | Vertical | `px-16px py-9px` | 24px | `gap: 4px` |
| **Large** | Horizontal | `px-16px py-9px` | 20px | `gap: 4px` |
| **Small** | Vertical | `px-8px py-6px` | 24px | `gap: 4px` |
| **Small** | Horizontal | `px-8px py-6px` | 20px | `gap: 4px` |

#### Label Only — Desktop (`769px+`)

| Storlek | Padding |
|---|---|
| **Large** | `px-16px py-8px` |
| **Small** | `px-16px py-6px` |

#### Label Only — Mobile (`≤768px`)

| Storlek | Padding |
|---|---|
| **Large** | `px-16px py-9px` |
| **Small** | `px-8px py-6px` |

---

### Typografi

| Storlek | Token | Desktop | Mobile | `font-feature-settings` |
|---|---|---|---|---|
| **Large** | `body-md` | 16px / 24px / 0.32px | 16px / 22px / 0.32px | `'ss02' 1, 'ss03' 1, 'ss06' 1` |
| **Small** | `body-sm` | 14px / 20px / 0.28px | 14px / 20px / 0.28px | `'ss02' 1, 'ss03' 1, 'ss06' 1` |

Textfärg Enabled: `text-primary` (#000). Textfärg Hover: `text-action-primary-hover` (#737373). Font: Breuer Condensed Regular.

---

### CSS-mall

```css
/* Tile Link — wrapper (ger rätt display-beteende) */
.tile-link {
  display: inline-flex;
  position: relative;
  cursor: pointer;
  text-decoration: none;
}

/* Inner tile (borderns container) */
.tile-link__inner {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;           /* White — default */
  transition: border-color 150ms cubic-bezier(.35,0,.35,1);
}

/* Vertikal placering */
.tile-link--vertical .tile-link__inner { flex-direction: column; gap: 4px; }

/* Horisontell placering */
.tile-link--horizontal .tile-link__inner { flex-direction: row; }

/* Border (absolut, påverkar inte layouten) */
.tile-link__inner::before {
  content: '';
  position: absolute;
  inset: 0;
  border: 1px solid #e5e5e5;    /* border-primary — Enabled */
  pointer-events: none;
  transition: border-color 150ms cubic-bezier(.35,0,.35,1);
}

/* Hover */
.tile-link:hover .tile-link__inner::before { border-color: #333333; /* border-hover */ }

/* Bakgrundsvarianter */
.tile-link--grey .tile-link__inner  { background: #f6f6f6; }
.tile-link--black .tile-link__inner { background: #000000; }
.tile-link--black .tile-link__inner::before { border-color: #000000; }

/* Hover Black — white 20% overlay */
.tile-link--black:hover .tile-link__inner {
  background-image: linear-gradient(90deg, rgba(255,255,255,0.2), rgba(255,255,255,0.2)),
                    linear-gradient(90deg, #000, #000);
}

/* Label */
.tile-link__label {
  font-family: 'Breuer Condensed', Arial, sans-serif;
  font-weight: 400;
  color: #000000;                /* text-primary */
  white-space: nowrap;
  text-align: center;
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;

  /* Large desktop */
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.32px;
}
.tile-link--small .tile-link__label { font-size: 14px; line-height: 20px; letter-spacing: 0.28px; }

/* Hover — label färg */
.tile-link:hover .tile-link__label { color: #737373; /* text-action-primary-hover */ }

/* Black variant — label alltid vit */
.tile-link--black .tile-link__label { color: #ffffff; }
.tile-link--black:hover .tile-link__label { color: #ffffff; }

/* Ikon */
.tile-link__icon {
  font-size: 24px;               /* Large Vertical */
  color: #000000;
}
.tile-link--horizontal .tile-link__icon { font-size: 20px; }
.tile-link--small.tile-link--vertical .tile-link__icon { font-size: 24px; }
.tile-link:hover .tile-link__icon { color: #737373; }
.tile-link--black .tile-link__icon,
.tile-link--black:hover .tile-link__icon { color: #ffffff; }

/* Storlekar — Desktop */
.tile-link--large.tile-link--vertical  .tile-link__inner { padding: 10px 16px; }
.tile-link--small.tile-link--vertical  .tile-link__inner { padding: 8px 16px; }
.tile-link--large.tile-link--horizontal .tile-link__inner { padding: 8px 16px; gap: 8px; }
.tile-link--small.tile-link--horizontal .tile-link__inner { padding: 6px 16px; gap: 8px; }

/* Mobile */
@media (max-width: 768px) {
  .tile-link__label { line-height: 22px; }     /* body-md mobile: 22px */

  .tile-link--large.tile-link--vertical  .tile-link__inner { padding: 9px 16px; }
  .tile-link--small.tile-link--vertical  .tile-link__inner { padding: 6px 8px; }
  .tile-link--large.tile-link--horizontal .tile-link__inner { padding: 9px 16px; gap: 4px; }
  .tile-link--small.tile-link--horizontal .tile-link__inner { padding: 6px 8px;  gap: 4px; }
}

/* Brand-variant */
.tile-link--brand.tile-link--large .tile-link__inner {
  height: 112px;
  padding: 0 48px;
}

@media (max-width: 768px) {
  .tile-link--brand.tile-link--large .tile-link__inner {
    height: 80px;
    padding: 0 32px;
  }
}
```

### HTML-exempel

```html
<!-- Label + Icon, Large, Vertical, White -->
<a href="#" class="tile-link tile-link--large tile-link--vertical tile-link--white">
  <div class="tile-link__inner">
    <span class="material-symbols-outlined tile-link__icon">bolt</span>
    <span class="tile-link__label">Elverk</span>
  </div>
</a>

<!-- Label + Icon, Small, Horizontal, Grey -->
<a href="#" class="tile-link tile-link--small tile-link--horizontal tile-link--grey">
  <div class="tile-link__inner">
    <span class="material-symbols-outlined tile-link__icon">search</span>
    <span class="tile-link__label">Sök</span>
  </div>
</a>

<!-- Label Only, Large, White -->
<a href="#" class="tile-link tile-link--large tile-link--horizontal tile-link--white">
  <div class="tile-link__inner">
    <span class="tile-link__label">Elverk</span>
  </div>
</a>

<!-- Brand, Large, White -->
<a href="#" class="tile-link tile-link--brand tile-link--large tile-link--white">
  <div class="tile-link__inner">
    <img src="brand-logo.svg" alt="Björnkläder" style="height:48px;" />
  </div>
</a>

<!-- Brand, Large, Black -->
<a href="#" class="tile-link tile-link--brand tile-link--large tile-link--black">
  <div class="tile-link__inner">
    <img src="brand-logo-white.svg" alt="Björnkläder" style="height:48px;" />
  </div>
</a>
```

---
