---
name: toast-ecom
description: Använd när du bygger en e-handelstoast — t.ex. "produkt tillagd i varukorgen" (Add to cart-variant med produktbild) eller "lades till i favoritlistan" (Informational-variant, svart bakgrund).
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Notifikation – E-Com Toast (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=13377-22983

### Används när
- En e-handelsåtgärd bekräftas utan att blockera sidan: produkt lagd i varukorg, produkt lagd i favoritlista
- Kortlivad feedback direkt kopplad till produktinteraktion

### Används INTE när
- Systemfel eller statusmeddelanden → använd **System Toast** (med statusfärg)
- Åtgärden kräver bekräftelse → använd **E-Com Modal**

---

### Två varianter

| Variant | Bakgrund | Användning |
|---|---|---|
| **Add to cart** | `#ffffff` vit | Produkt lagd i varukorg — visar produktbild + två CTA-knappar |
| **Informational** | `#000000` svart | Kortlivad info, t.ex. "lagd i favoritlistan" — text + valfri länk |

> Position, animation och auto-hide följer **samma regler som System Toast** (slides in från höger, `cubic-bezier(0.16, 0, 0.16, 1)`, 300ms, auto-hide 3000ms, `position: fixed`).

---

### Bredd och padding per breakpoint

| | Desktop (`md:` 769px+) | Tablet/Mobile (≤768px) |
|---|---|---|
| **Add to cart** bredd | `440px` | `375px` |
| **Informational** bredd | `375px` | `375px` |
| Padding | `24px` | `16px` |

---

### Add to cart — Anatomi

```
[Produktbild 40×40px]  [Produktnamn Bold] brödtext Regular   [✕ stäng]

[Välj tillbehör      ] [Gå till Varukorgen                 ]
```

- Produktbild: `40×40px`, `object-fit: contain`
- Gap bild–text: `16px`
- **Produktnamn**: Bold, `body-md` 16px/18px, `#000`
- **Brödtext**: Regular, `body-md` 16px/24px, `0.32px`, `#000`
- **Stäng-knapp**: `close`-ikon 20px, `padding: 2px`, svart
- **Knappar** (`pt-16px` under texten, `gap: 8px`, båda `flex: 1`):
  - Secondary ("Välj tillbehör"): `border: 1px solid #000`, transparent
  - Primary ("Gå till Varukorgen"): `background: #000`, vit text
  - Desktop: `label-sm` 14px, 0.56px / Tablet+Mobile: `label-md` 14px, 0.42px
  - Desktop knapp-padding: `6px` / Tablet+Mobile: `4px`
- **Shadow**: `elevation-b-80` = `0px 8px 16px 0px rgba(0,0,0,0.10), 0px 0px 1px 0px rgba(0,0,0,0.05)`

---

### Informational — Anatomi

```
[Produktnamn Bold] brödtext Regular         [Visa]  [✕]
```

- Bakgrund: `#000000`
- Border: `1px solid #f6f6f6` (`border-secondary`) — subtil kant på svart yta
- Alla textelement: `color: #ffffff` (`text-primary-inverted`)
- **Text**: Bold produktnamn + Regular beskrivning, `body-md` 16px/24px desktop, 16px/22px mobil
- **"Visa"-länk** (valfri): understruken, `body-md` Regular, `#ffffff`
- **Stäng-knapp**: `close`-ikon 20px, `padding: 2px`, vit
- Gap text–länk–stäng: `12px`
- **Shadow**: `elevation-b-80`

---

### CSS-mall

```css
/* Gemensam bas */
.ecom-toast {
  position: relative;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.10),
              0px 0px 1px 0px rgba(0,0,0,0.05); /* elevation-b-80 */
  width: 440px;        /* Add to cart desktop */
}

/* Add to cart */
.ecom-toast--cart {
  background: #ffffff;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

/* Informational */
.ecom-toast--info {
  background: #000000;
  border: 1px solid #f6f6f6;
  padding: 24px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  width: 375px;
}

/* Mobile/Tablet */
@media (max-width: 768px) {
  .ecom-toast--cart { padding: 16px; width: 375px; }
  .ecom-toast--info { padding: 16px; }
}

/* --- Add to cart header --- */
.ecom-toast__header {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  width: 100%;
}

.ecom-toast__image-text {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  flex: 1;
}

.ecom-toast__img {
  width: 40px;
  height: 40px;
  object-fit: contain;
  flex-shrink: 0;
}

.ecom-toast__product-text {
  flex: 1;
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 16px;
  color: #000;
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
}

.ecom-toast__product-name {
  font-weight: 700;
  line-height: 18px;
  font-feature-settings: 'ss02' 1, 'ss03' 1;
}

.ecom-toast__product-desc {
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.32px;
}

/* --- Add to cart footer --- */
.ecom-toast__footer {
  display: flex;
  gap: 8px;
  align-items: center;
  padding-top: 16px;
  width: 100%;
}

.ecom-toast__btn-secondary {
  flex: 1;
  background: transparent;
  border: 1px solid #000;
  cursor: pointer;
  padding: 6px;
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  line-height: 14px;
  letter-spacing: 0.56px;
  text-transform: uppercase;
  color: #000;
  white-space: nowrap;
  font-feature-settings: 'ss02' 1, 'ss03' 1;
}

.ecom-toast__btn-primary {
  flex: 1;
  background: #000;
  border: none;
  cursor: pointer;
  padding: 6px;
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  line-height: 14px;
  letter-spacing: 0.56px;
  text-transform: uppercase;
  color: #fff;
  white-space: nowrap;
  font-feature-settings: 'ss02' 1, 'ss03' 1;
}

@media (max-width: 768px) {
  .ecom-toast__btn-secondary,
  .ecom-toast__btn-primary { padding: 4px; letter-spacing: 0.42px; }
}

/* --- Informational content --- */
.ecom-toast__info-content {
  flex: 1;
}

.ecom-toast__info-text {
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 16px;
  color: #ffffff;
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
}

.ecom-toast__info-name {
  font-weight: 700;
  line-height: 18px;
  font-feature-settings: 'ss02' 1, 'ss03' 1;
}

.ecom-toast__info-desc {
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.32px;
}

@media (max-width: 768px) {
  .ecom-toast__info-desc { line-height: 22px; }
}

.ecom-toast__info-link {
  font-family: 'Breuer Condensed', sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0.32px;
  color: #ffffff;
  text-decoration: underline;
  cursor: pointer;
  white-space: nowrap;
  font-feature-settings: 'ss02' 1, 'ss03' 1, 'ss06' 1;
}

.ecom-toast__close {
  flex-shrink: 0;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 2px;
  font-size: 20px;
}

/* Svart stäng-knapp (Add to cart) */
.ecom-toast--cart .ecom-toast__close { color: #000; }
/* Vit stäng-knapp (Informational) */
.ecom-toast--info .ecom-toast__close { color: #ffffff; }
```

### HTML-exempel

**Add to cart:**
```html
<div class="ecom-toast ecom-toast--cart">
  <div class="ecom-toast__header">
    <div class="ecom-toast__image-text">
      <img class="ecom-toast__img" src="product.jpg" alt="Produktnamn" />
      <p class="ecom-toast__product-text">
        <span class="ecom-toast__product-name">Carpenter soul hantverksbyxa stretch svart</span>
        <span class="ecom-toast__product-desc"> har lagts till i varukorgen.</span>
      </p>
    </div>
    <button class="ecom-toast__close" aria-label="Stäng">
      <span class="material-symbols-outlined">close</span>
    </button>
  </div>
  <div class="ecom-toast__footer">
    <button class="ecom-toast__btn-secondary">Välj tillbehör</button>
    <button class="ecom-toast__btn-primary">Gå till Varukorgen</button>
  </div>
</div>
```

**Informational:**
```html
<div class="ecom-toast ecom-toast--info">
  <div class="ecom-toast__info-content">
    <p class="ecom-toast__info-text">
      <span class="ecom-toast__info-name">Bälte stretch svart</span>
      <span class="ecom-toast__info-desc"> lades till i favoritlistan.</span>
    </p>
    <a class="ecom-toast__info-link" href="#">Visa</a>
  </div>
  <button class="ecom-toast__close" aria-label="Stäng">
    <span class="material-symbols-outlined">close</span>
  </button>
</div>
```

---
