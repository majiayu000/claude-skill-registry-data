---
name: collapsible
description: Använd när du bygger en radbaserad expanderbar komponent/ackordion, t.ex. en "Vanliga frågor"-sektion (FAQ) — header + animerat innehåll.
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Collapsible / Ackordion (ECO Design System)

En rad-baserad expanderbar komponent — klick på headern togglar innehållet öppet/stängt med en animerad `max-height`-övergång. Används t.ex. för "Vanliga frågor"-sektioner (FAQ).

### Anatomi

```
.collapsible-wrap                              ← en rad, har bottenlinje mellan raderna
  .collapsible-item                            ← klickbar header (onclick="toggleCollapsible(this)")
    .collapsible-item__left
      .collapsible-item__label                 ← title-md
    .collapsible-item__chevron                 ← "expand_more"-ikon, roterar 180° när öppen
  .collapsible-item__content                   ← body-lg, max-height animeras via JS
```

Flera `.collapsible-wrap` staplas i en gemensam wrapper (t.ex. `.ehp-faq`) för att bilda en lista.

### Typografi

| Element | Token | Mobil | Desktop |
|---|---|---|---|
| `.collapsible-item__label` | `title-md` | 18px/22px, 0px, weight 600 | 20px/24px, 0px, weight 600 |
| `.collapsible-item__content` | `body-lg` | 18px/24px, 0px, weight 400 | 20px/28px, 0px, weight 400 |

`.collapsible-item__content` använder `color: var(--color-text-tertiary)` (`#737373`).

### Tillstånd (States)

| Tillstånd | Labelfärg |
|---|---|
| **Enabled** | `text-primary` (`--black`, `#000000`) |
| **Hover** (hela `.collapsible-item`) | `text-action-primary-hover` (`#737373`) |

> Transition: `color` med `duration-fast-3` (150ms) och `ease-standard` — samma mekanism som Inline/Action Link.

### Regler

1. **Bottenlinje mellan rader** — varje `.collapsible-wrap` har `border-bottom: 1px solid var(--color-border-primary)` som separator mot nästa rad i listan.
2. **Sista raden i en lista som avslutar en sektion döljer sin bottenlinje** — om `.collapsible-wrap`-listan är sektionens sista/enda innehållsblock (dvs. inget, t.ex. en `.section-cta`-rad, kommer efter listan i samma `<section>`) ska den sista radens bottenlinje **inte** visas. Annars hänger en linje utan syfte kvar precis ovanför sektionens egen bottenpadding. Regeln är villkorad på att listans FÖRÄLDER (t.ex. `.ehp-faq`) själv är sektionens sista barn — bordern behålls som vanligt om listan följs av annat innehåll i samma sektion.
3. **`min-height`, inte `height`, på `.collapsible-item`** — headern måste kunna växa om titeln radbryts.
4. **`max-height`-animationen sköts av JS**, inte CSS — `toggleCollapsible()` sätter `content.style.maxHeight` till `content.scrollHeight + 'px'` (öppna) eller `null` (stänga), eftersom CSS inte kan transitionera till/från `auto`.

### CSS-mall

```css
.collapsible-wrap {
  border-bottom: 1px solid var(--color-border-primary);
  transition: padding-bottom var(--duration-fast-4) var(--ease-standard);
}
/* Sista collapsible-wrap i en lista döljer sin bottom border NÄR
   listan är sektionens sista/enda innehåll (dvs. inget — t.ex.
   en CTA-rad — kommer efter den i samma <section>) — annars hade
   en linje utan syfte hängt kvar precis ovanför sektionens egen
   bottenpadding. Villkorat på att listans FÖRÄLDER (t.ex. .ehp-faq)
   själv är sektionens sista barn, så bordern behålls som vanligt om
   listan följs av annat innehåll i samma sektion. */
section > *:last-child .collapsible-wrap:last-child { border-bottom: none; }

.collapsible-wrap--open { padding-bottom: 32px; }

.collapsible-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 0;
  cursor: pointer;
  min-height: 72px;
  box-sizing: border-box;
}
.collapsible-item__left {
  display: flex;
  align-items: center;
  gap: 8px;
}
.collapsible-item__left .ms { color: var(--black); }

/* title-md (ECO Design System): mobil 18px/22px, desktop 20px/24px, 0px spacing, weight 600 */
.collapsible-item__label {
  font-size: 18px;
  font-weight: 600;
  line-height: 22px;
  letter-spacing: 0;
  color: var(--black);
  transition: color var(--duration-fast-3) var(--ease-standard);
}
.collapsible-item:hover .collapsible-item__label { color: var(--color-text-action-primary-hover); }
@media (min-width: 769px) {
  .collapsible-item__label { font-size: 20px; line-height: 24px; }
}

.collapsible-item__chevron .ms {
  color: var(--black);
  font-size: 24px;
  transition: transform var(--duration-fast-4) var(--ease-standard);
}
.collapsible-wrap--open .collapsible-item__chevron .ms { transform: rotate(180deg); }

/* body-lg (ECO Design System): mobil 18px/24px, desktop 20px/28px, 0px spacing, weight 400 */
.collapsible-item__content {
  max-height: 0;
  overflow: hidden;
  transition: max-height var(--duration-fast-4) var(--ease-standard);
  font-size: 18px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0;
  color: var(--color-text-tertiary);
}
@media (min-width: 769px) {
  .collapsible-item__content { font-size: 20px; line-height: 28px; }
}
```

```js
function toggleCollapsible(header) {
  const wrap = header.parentElement;
  const content = header.nextElementSibling;
  const isOpen = wrap.classList.contains('collapsible-wrap--open');
  wrap.classList.toggle('collapsible-wrap--open', !isOpen);
  content.style.maxHeight = isOpen ? null : content.scrollHeight + 'px';
}
```

### HTML-exempel

```html
<div class="collapsible-wrap">
  <div class="collapsible-item" onclick="toggleCollapsible(this)">
    <div class="collapsible-item__left">
      <span class="collapsible-item__label">Vad kostar det att sätta upp en kundunik webbshop?</span>
    </div>
    <span class="collapsible-item__chevron"><span class="ms" aria-hidden="true">expand_more</span></span>
  </div>
  <div class="collapsible-item__content">Det beror på omfattning och vilka funktioner ni behöver. Kontakta er lokala säljrepresentant så tar vi tillsammans fram en lösning som passar er verksamhet och er budget.</div>
</div>
```

---
